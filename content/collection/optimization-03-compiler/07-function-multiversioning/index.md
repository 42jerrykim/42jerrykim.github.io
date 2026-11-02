---
collection_order: 7
date: 2026-03-11
lastmod: 2026-10-20
draft: false
image: wordcloud.png
title: "[Compiler 03] CPU 기능별 함수 다중 버전"
slug: function-multiversioning-cpu
description: "GCC·Clang의 target/target_clones로 CPU 기능별 함수 버전을 만들고, resolver·ELF IFUNC 디스패치 동작과 __builtin_cpu_supports 수동 디스패치, 간접 호출·인라이닝 손실 비용, 버전별 검증 절차를 실제 컴파일 결과로 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Hardware(하드웨어)
  - Assembly(어셈블리)
  - SIMD(단일명령다중데이터)
  - Vectorization(벡터화)
  - Floating-Point(부동소수점)
  - Low-Level(로우레벨)
  - Linux(리눅스)
  - Testing(테스트)
  - Benchmark
  - Comparison(비교)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - GCC
  - Clang
  - x86-64
  - AVX
  - IFUNC
---

한 바이너리를 여러 세대의 CPU에 배포하면서도 최신 CPU에서는 AVX2나 AVX-512를 쓰고 싶을 때, 선택지는 둘입니다. 가장 오래된 CPU에 맞춰 `-march`를 낮게 잡고 성능을 포기하거나, 같은 함수를 CPU 기능별로 여러 벌 만들어 두고 실행 시점에 고르는 것입니다. 이 챕터는 후자인 **함수 멀티버저닝**을 다룹니다. GCC·Clang의 `target`/`target_clones` 문법, 컴파일러가 만드는 resolver와 ELF IFUNC의 동작, 직접 디스패치하는 방법, 그리고 디스패치 비용과 검증 절차를 순서대로 봅니다. 본문의 컴파일 결과와 실행 결과는 2026년 10월 [Compiler Explorer](https://godbolt.org)의 x86-64 gcc 14.2, x86-64 clang 19.1.0에서 얻은 것입니다.

## 멀티버저닝의 개념과 전제 조건

<strong>함수 멀티버저닝(Function Multiversioning, FMV)</strong>은 같은 이름의 함수를 CPU 기능 조합별로 따로 컴파일해 두고, 실행 시점에 CPU가 지원하는 기능을 검사해 그중 하나를 호출하는 방식입니다. 예를 들어 기본 버전은 x86-64 기본 명령어(SSE2)만 쓰고, AVX2 버전은 256비트 레지스터로 float 8개(double 4개)를, AVX-512 버전은 512비트 레지스터로 float 16개(double 8개)를 한 번에 처리하도록 만들 수 있습니다. 호출하는 쪽 코드는 평범한 함수 호출처럼 쓰고, 어느 버전이 실행될지는 런타임이 정합니다.

이 기능에는 플랫폼 전제가 있습니다. [GCC Function Multiversioning 문서](https://gcc.gnu.org/onlinedocs/gcc/Function-Multiversioning.html)는 FMV가 ELF 표준의 indirect function(IFUNC) 확장에 의존하므로 Binutils 2.20.1 이상과 GNU C Library 2.11.1이 필요하다고 밝힙니다. 즉 자동 FMV는 Linux 같은 ELF·glibc 환경의 기능이고, 이 속성 자체가 GCC·Clang의 확장이라 MSVC에는 대응하는 문법이 없습니다. Windows나 다른 libc 환경에서는 뒤에서 볼 수동 디스패치를 써야 합니다. 또 같은 문서에 따르면 x86에서 `target` 속성으로 정의를 여러 개 두는 방식은 C++에서만 허용되고, C에서는 정의 하나로 여러 버전을 만드는 `target_clones`를 써야 합니다.

## x86 문법 1: 정의를 여러 개 두는 `target`

x86에서는 GCC와 Clang이 같은 문법을 씁니다. 같은 시그니처의 함수에 서로 다른 `target` 문자열을 붙여 여러 번 정의하고, 그중 하나는 반드시 `"default"`여야 합니다. [Clang Attribute Reference](https://clang.llvm.org/docs/AttributeReference.html)도 ELF 기반 x86/x86-64에서 이 방식의 멀티버저닝을 지원하며, 모든 멀티버전 함수는 default 구현을 가져야 하고 첫 사용 이후에 멀티버전으로 바뀔 수 없다고 설명합니다.

아래 예제는 그대로 컴파일·실행되는 완결된 프로그램입니다. 핵심은 AVX2 버전의 `target` 문자열이 `"avx2,fma"`라는 점입니다. 이 함수 안에서 쓰는 `_mm256_fmadd_ps`는 AVX2가 아니라 FMA 명령어 집합에 속하므로, `target("avx2")`만 주면 GCC 14.2는 "inlining failed in call to 'always_inline' '_mm256_fmadd_ps': target specific option mismatch", Clang 19.1.0은 "requires target feature 'fma'" 오류로 컴파일을 거부합니다. intrinsic은 `always_inline` 함수라서, 호출하는 함수에 해당 기능이 켜져 있지 않으면 경고가 아니라 오류가 됩니다.

```cpp
// fmv_demo.cc — GCC/Clang 공통(x86-64 ELF, C++)
#include <immintrin.h>
#include <cstddef>
#include <cstdio>
#include <vector>

// 기본 경로: x86-64 기본 명령어(SSE2)만 가정
__attribute__((target("default")))
float dot_product(const float* a, const float* b, std::size_t n) {
    float sum = 0.0f;
    for (std::size_t i = 0; i < n; ++i)
        sum += a[i] * b[i];
    return sum;
}

// AVX2+FMA 경로: 256비트 레지스터로 float 8개씩 곱셈-누산
__attribute__((target("avx2,fma")))
float dot_product(const float* a, const float* b, std::size_t n) {
    __m256 acc = _mm256_setzero_ps();
    std::size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(a + i);
        __m256 vb = _mm256_loadu_ps(b + i);
        acc = _mm256_fmadd_ps(va, vb, acc);   // va * vb + acc
    }
    float buf[8];                              // 8개 레인을 스칼라로 합산
    _mm256_storeu_ps(buf, acc);
    float s = buf[0] + buf[1] + buf[2] + buf[3] + buf[4] + buf[5] + buf[6] + buf[7];
    for (; i < n; ++i) s += a[i] * b[i];      // 8의 배수가 아닌 나머지
    return s;
}

int main() {
    std::vector<float> a(1000, 1.0f), b(1000, 2.0f);
    std::printf("%.1f\n", dot_product(a.data(), b.data(), a.size()));
}
```

```bash
g++ -O2 fmv_demo.cc -o fmv_demo && ./fmv_demo     # 출력: 2000.0
```

두 버전은 같은 입력에 같은 값을 돌려줘야 합니다. 다만 AVX2 버전은 8개 레인에 나눠 누산한 뒤 합치므로 덧셈 순서가 기본 버전과 다르고, FMA는 곱셈 결과를 반올림하지 않고 더하므로, 일반 입력에서는 마지막 비트가 다를 수 있습니다. 이 예제의 입력(모두 1.0과 2.0)은 정확히 표현되는 값이라 두 컴파일러의 실행 결과가 모두 `2000.0`이었지만, 검증 테스트는 비트 일치가 아니라 허용 오차로 비교해야 합니다.

## x86 문법 2: 정의 하나로 여러 벌을 만드는 `target_clones`

같은 소스를 기능별로 다시 컴파일하기만 하면 되는 경우에는 `target_clones`가 간편합니다. 정의는 한 번만 쓰고, 나열한 각 타깃에 대해 컴파일러가 복제본을 만들어 자동 벡터화를 타깃별로 다시 적용합니다. GCC와 Clang 모두 x86에서 이 속성을 지원합니다.

```cpp
// target_clones_demo.cc
#include <cstddef>

__attribute__((target_clones("avx512f", "avx2", "default")))
void vector_add(float* __restrict dst, const float* __restrict src, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i)
        dst[i] += src[i];
}
```

여기에는 실측으로 확인한 함정이 하나 있습니다. GCC 14.2에서 이 파일을 `-O2`로 컴파일하면 `avx512f`, `avx2`, `default` 세 복제본과 resolver가 모두 생기지만, 세 복제본 모두 스칼라 `vaddss`/`addss` 루프였습니다. GCC의 `-O2`는 벡터화 비용 모델이 `very-cheap`이라 반복 횟수를 모르는 이 루프의 에필로그를 허용하지 않기 때문입니다([챕터 04](/post/compiler-optimization/compiler-comparison-gcc-clang-msvc/) 참고). `-O3`로 올리자 `avx512f` 복제본은 `vaddps zmm`, `avx2` 복제본은 `vaddps ymm`을 쓰는 벡터 루프가 됐고, Clang 19.1.0은 `-O2`에서 이미 두 복제본을 각각 `zmm`·`ymm` 벡터 루프로 만들었습니다. `target_clones`는 명령어 집합을 열어 줄 뿐 벡터화를 보장하지 않으므로, 복제본의 어셈블리나 벡터화 리포트를 반드시 확인해야 합니다.

AArch64는 문법이 다릅니다. Clang Attribute Reference는 AArch64에서 `target_version` 속성과 ACLE(Arm C Language Extensions)의 기능 이름으로 멀티버저닝을 지원한다고 설명하고, GCC 매뉴얼도 `target_version`을 AArch64·LoongArch·RISC-V용으로 설명합니다. `target_version`은 x86의 문법이 아니므로, x86 코드에 쓰지 않도록 주의합니다.

## 디스패치 메커니즘: resolver와 IFUNC

컴파일러는 멀티버전 함수마다 각 버전의 본문과 함께 **resolver** 함수를 만듭니다. GCC 문서의 설명대로 resolver는 동적 링커가 아키텍처 지원 여부를 확인하고 알맞은 버전을 고르는 데 쓰입니다. 위 `fmv_demo.cc`를 GCC 14.2 `-O2`로 컴파일한 어셈블리에는 다음 심볼들이 나타납니다(맹글링된 이름).

```text
        .type   _Z11dot_productPKfS0_m, @function
        .type   _Z11dot_productPKfS0_m.avx2_fma, @function
        .type   _Z11dot_productPKfS0_m.resolver, @function
        .type   _Z22_Z11dot_productPKfS0_mPKfS0_m, @gnu_indirect_function
```

기본 버전, `avx2_fma` 버전, resolver가 각각 일반 함수로 있고, 마지막 줄의 심볼은 타입이 `@gnu_indirect_function`, 즉 IFUNC입니다. `main`의 `dot_product` 호출은 이 IFUNC 심볼을 향합니다. Clang 19.1.0은 같은 구조를 만들되 IFUNC 심볼 이름을 `_Z11dot_productPKfS0_m.ifunc`로 붙였습니다. 이름 형식은 컴파일러마다 다르므로, 실제 바이너리에서는 `nm -C ./fmv_demo | grep dot_product`나 `objdump -d -C`로 확인합니다.

resolver 본문은 단순합니다. GCC 14.2가 만든 resolver는 `__cpu_indicator_init`을 호출해 CPU 기능 정보를 채운 뒤, `__cpu_model` 구조체의 기능 비트를 검사해 AVX2와 FMA가 모두 있으면 `avx2_fma` 버전의 주소를, 아니면 기본 버전의 주소를 반환합니다. 동적 링커는 IFUNC 심볼을 재배치할 때 이 resolver를 **한 번** 호출하고, 반환된 주소를 GOT(Global Offset Table) 슬롯에 기록합니다. 이후의 모든 호출은 PLT를 거쳐 GOT에 기록된 주소로 가는 간접 호출입니다. 따라서 CPU 기능 검사는 매 호출마다 일어나지 않고, 비용은 "간접 호출 한 번"으로 고정됩니다.

## 수동 디스패치: `__builtin_cpu_supports`

IFUNC를 쓸 수 없는 환경이거나, 선택 로직을 직접 통제하고 싶을 때는 함수 포인터로 디스패치를 구현합니다. GCC·Clang은 `__builtin_cpu_supports("avx2")` 같은 내장 함수로 실행 중인 CPU의 기능을 조회할 수 있습니다. [GCC x86 Built-in Functions 문서](https://gcc.gnu.org/onlinedocs/gcc/x86-Built-in-Functions.html)는 CPU 감지 코드가 매우 높은 우선순위의 생성자에서 자동 실행되므로, `__builtin_cpu_init`은 다른 생성자가 실행되기 전에 이 검사를 해야 하는 함수에서만 부르면 된다고 설명합니다. 아래 예제는 전역 변수 초기화(정적 초기화) 시점에 선택하므로 안전하게 `__builtin_cpu_init`을 먼저 부릅니다.

```cpp
// manual_dispatch.cc — 컴파일러 자동 디스패치 대신 직접 고르기
#include <cstddef>
#include <cstdio>

__attribute__((target("avx2,fma")))
static float dot_avx2(const float* a, const float* b, std::size_t n) {
    float s = 0.0f;                         // 이 함수 안에서는 AVX2·FMA 코드 생성 허용
    for (std::size_t i = 0; i < n; ++i) s += a[i] * b[i];
    return s;
}

static float dot_scalar(const float* a, const float* b, std::size_t n) {
    float s = 0.0f;
    for (std::size_t i = 0; i < n; ++i) s += a[i] * b[i];
    return s;
}

using DotFn = float (*)(const float*, const float*, std::size_t);

static DotFn pick_dot() {
    __builtin_cpu_init();                   // 정적 생성자 등 이른 시점 호출 대비
    if (__builtin_cpu_supports("avx2") && __builtin_cpu_supports("fma"))
        return dot_avx2;
    return dot_scalar;
}

static const DotFn dot = pick_dot();        // 프로그램 시작 시 한 번만 선택

int main() {
    float a[4] = {1, 2, 3, 4}, b[4] = {1, 1, 1, 1};
    std::printf("%s: %.1f\n", dot == dot_avx2 ? "avx2" : "scalar", dot(a, b, 4));
}
```

Compiler Explorer의 실행 환경에서는 GCC 14.2와 Clang 19.1.0 모두 `avx2: 10.0`을 출력했습니다. 이 방식은 선택된 버전을 로그로 남기기 쉽고, 환경 변수로 특정 버전을 강제하는 테스트 훅을 넣기도 쉽다는 장점이 있습니다. 비용 구조는 IFUNC와 같아서, 선택은 한 번이고 이후에는 함수 포인터를 통한 간접 호출입니다. MSVC에서는 `__builtin_cpu_supports` 대신 `__cpuid` intrinsic으로 기능 비트를 읽어 같은 구조를 만듭니다.

## 디스패치 비용과 사용 시점

디스패치 결정은 한 번이지만, 그 대가로 모든 호출이 간접 호출이 되고 **인라이닝이 막힙니다**. 호출자는 컴파일 시점에 어느 버전이 실행될지 모르므로 본문을 펼쳐 넣을 수 없고, 따라서 호출자 쪽의 상수 전파나 루프 융합도 함께 사라집니다. 원소 수천 개를 처리하는 커널이라면 호출 한 번의 간접 분기 비용은 본문 실행 시간에 묻히지만, 원소 몇 개를 처리하는 작은 함수를 핫 루프 안에서 반복 호출한다면 이 비용과 인라이닝 손실이 SIMD 이득을 넘을 수 있습니다.

그래서 멀티버저닝의 경계는 가능한 한 바깥에 둡니다. 원소 하나를 처리하는 함수가 아니라 배열 전체를 처리하는 루프를 감싼 함수를 멀티버전으로 만들고, 그 안의 작은 함수들은 같은 `target` 속성을 공유해 버전 내부에서 인라인되도록 합니다. `target` 문자열이 다른 함수끼리는 인라인되지 않는다는 점도 이 설계를 강제합니다.

## 버전별 설계와 검증

버전마다 같은 의미를 지키는 것이 첫째 조건입니다. 각 버전은 SIMD 폭에 맞춰 루프를 구성하고(AVX2는 float 8개·double 4개, AVX-512는 float 16개·double 8개), 폭의 배수가 아닌 나머지 원소를 처리하는 꼬리 루프를 반드시 갖춰야 합니다. 앞에서 본 것처럼 부동소수점 리덕션은 버전마다 덧셈 순서가 달라지므로, 정확성 테스트는 기본 버전 결과와 허용 오차 안에서 같은지를 확인합니다.

검증의 어려움은 테스트 머신에서 실행되는 버전이 하나뿐이라는 데 있습니다. AVX-512가 있는 CI 머신에서는 기본 버전이 한 번도 실행되지 않을 수 있습니다. 수동 디스패치라면 강제 선택 훅을 두어 모든 버전을 같은 머신에서 테스트할 수 있고, 자동 FMV라면 Intel SDE 같은 에뮬레이터나 기능이 다른 여러 머신에서 테스트를 돌려야 합니다. 성능은 실제 대상 CPU에서 기본 버전 대비 측정해, 각 버전이 코드와 테스트 매트릭스를 늘리는 만큼의 이득을 내는지 확인합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **target / target_clones** | GCC·Clang(x86 ELF)의 멀티버저닝 속성. 전자는 정의를 여러 개, 후자는 정의 하나로 여러 복제본을 만든다 |
| **target_version** | AArch64(ACLE) 등에서 쓰는 멀티버저닝 속성. x86 문법이 아니다 |
| **resolver** | CPU 기능을 검사해 실행할 버전의 주소를 반환하는 컴파일러 생성 함수 |
| **IFUNC** | ELF의 indirect function. 동적 링커가 resolver를 한 번 호출해 결과 주소를 GOT에 기록한다 |
| **`__builtin_cpu_supports`** | 실행 중인 CPU의 기능 지원 여부를 반환하는 GCC·Clang 내장 함수 |

## 판단 기준: 언제 멀티버저닝을 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 여러 CPU 세대에 단일 바이너리 배포 | 무거운 커널만 멀티버전, 나머지는 기본 `-march` | 최신 CPU용 `-march`로 전체 빌드 |
| 배열 전체를 처리하는 SIMD 커널 | `target_clones`(GCC는 `-O3`) 또는 intrinsic 버전 + `target` | 원소 단위 작은 함수의 멀티버전화 |
| Windows·비 glibc 환경 | `__builtin_cpu_supports`/`__cpuid` 기반 수동 디스패치 | IFUNC 기반 자동 FMV 가정 |

## 자주 하는 실수

- **`target_version`을 x86에 쓰기**: x86의 멀티버저닝 문법은 `target`과 `target_clones`다. `target_version`은 AArch64 등에서 쓰는 속성이다.
- **`target("avx2")`가 FMA를 포함한다고 생각하기**: AVX2와 FMA는 별개의 기능이다. `_mm256_fmadd_ps`를 쓰려면 `"avx2,fma"`처럼 둘 다 켜야 하며, 빠뜨리면 컴파일 오류가 난다.
- **디스패치가 매 호출마다 일어난다고 생각하기**: 기능 검사는 resolver가 한 번 한다. 실제 비용은 매 호출의 간접 호출과 인라이닝 불가다.
- **`target_clones`가 벡터화를 보장한다고 생각하기**: GCC `-O2`에서는 복제본이 모두 스칼라일 수 있다. 복제본의 어셈블리나 벡터화 리포트로 확인한다.

## 학습 성과 목표

- GCC·Clang의 `target`/`target_clones` 문법과 플랫폼 전제(ELF IFUNC, glibc, C++ 전용 다중 정의)를 설명하고 컴파일 가능한 멀티버전 함수를 작성할 수 있다.
- resolver·IFUNC·GOT로 이어지는 디스패치 메커니즘과 그 비용(간접 호출, 인라이닝 불가)을 설명할 수 있다.
- `__builtin_cpu_supports`로 수동 디스패치를 구현하고, 버전별 정확성·성능을 검증하는 절차를 설계할 수 있다.

## 비판적 시각: 한계와 트레이드오프

멀티버저닝은 바이너리 크기와 테스트 부담을 버전 수만큼 늘립니다. 버전이 셋이면 정확성 테스트도 세 벌이 필요한데, 대부분의 CI는 그중 하나만 실행합니다. 자동 FMV는 ELF IFUNC에 묶여 있어 정적 링크나 비 glibc 환경에서 제약을 받고, 이식성이 필요하면 결국 수동 디스패치를 따로 유지해야 합니다. 대안도 있습니다. 배포 대상 CPU가 충분히 새롭다면 x86-64 마이크로아키텍처 레벨(예: `-march=x86-64-v3`)로 전체를 빌드하는 편이 단순하고 인라이닝 손실도 없습니다. Highway나 xsimd 같은 SIMD 라이브러리는 디스패치까지 포함한 추상화를 제공합니다. 멀티버저닝은 이런 대안으로 해결되지 않는 소수의 핫 커널에 한정해 쓰는 도구로 보는 것이 맞습니다.

## 다음 장에서는

**컴파일러 내장 함수(intrinsics)** 카탈로그, SIMD·원자성 등 사용 시 주의와 대안을 다룹니다.

→ [컴파일러 내장 함수](/post/compiler-optimization/compiler-intrinsics-catalog/) (챕터 08)
