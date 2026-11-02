---
collection_order: 8
date: 2026-03-11
lastmod: 2026-10-20
draft: false
image: wordcloud.png
title: "[Compiler 03] 컴파일러 intrinsics 카탈로그"
slug: compiler-intrinsics-catalog
description: "SIMD·원자 연산·비트 조작 intrinsic이 어떤 플래그에서 어떤 명령으로 내려가는지, 기능이 빠졌을 때의 컴파일 오류와 조용한 대체, 인라인 어셈블리와의 차이, GCC·Clang·MSVC 대응을 실제 컴파일 결과로 정리합니다."
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
  - Low-Level(로우레벨)
  - Concurrency(동시성)
  - Lock-Free
  - Bit-Manipulation
  - Linux(리눅스)
  - Windows(윈도우)
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
  - MSVC
  - ARM
  - Intrinsics
---

intrinsic은 함수처럼 호출하지만 컴파일러가 특정 CPU 명령이나 짧은 명령 시퀀스로 바꿔 주는 API입니다. 이 챕터는 SIMD·원자 연산·비트 조작의 세 범주를 카탈로그처럼 훑으면서, 각 intrinsic이 **어떤 컴파일 옵션에서 어떤 명령으로 내려가는지**, 옵션이 맞지 않으면 무슨 일이 생기는지, 컴파일러마다 무엇이 다른지를 다룹니다. SIMD 코드로 알고리즘을 벡터화하는 전략 자체는 SIMD 트랙(Tr.08)의 주제이므로, 여기서는 intrinsic의 형태·헤더·필요 플래그를 확인하는 데 필요한 만큼만 예제를 씁니다. 본문의 어셈블리와 오류 메시지는 2026년 10월 [Compiler Explorer](https://godbolt.org)의 x86-64 gcc 14.2, x86-64 clang 19.1.0, ARM64 gcc 14.2.0에서 얻은 실제 출력입니다.

## intrinsic과 인라인 어셈블리의 차이

<strong>intrinsic(내장 함수)</strong>을 쓰는 이유는 인라인 어셈블리와 비교하면 분명해집니다. 인라인 어셈블리(`asm(...)`)는 컴파일러에게 **불투명한 블록**입니다. 컴파일러는 그 안의 명령이 무엇을 계산하는지 모르므로 상수를 미리 계산하거나, 주변 코드와 합치거나, 명령 순서를 바꿀 수 없고, 입출력 제약에 적힌 대로 레지스터만 맞춰 줍니다. 반면 intrinsic은 컴파일러가 의미를 아는 연산이라 중간 표현 수준에서 다른 코드와 똑같이 최적화됩니다. [MS Learn의 Compiler intrinsics 문서](https://learn.microsoft.com/en-us/cpp/intrinsics/compiler-intrinsics)도 옵티마이저가 intrinsic의 동작을 알고 있어 인라인 어셈블리로는 불가능한 최적화가 가능하다고 설명하고, MSVC는 x64에서 인라인 어셈블리를 아예 지원하지 않으므로 intrinsic이 유일한 수단이라고 밝힙니다.

차이는 작은 예제로 바로 보입니다. 같은 popcount를 내장 함수와 인라인 어셈블리로 각각 감싸고 상수 `0xFF`를 넣었습니다.

```cpp
// fold.cc: 상수 입력에 대한 내장 함수 vs 인라인 어셈블리
#include <cstdint>

static inline int pop_builtin(uint64_t x) { return __builtin_popcountll(x); }
static inline int pop_asm(uint64_t x) {
    uint64_t r;
    asm("popcnt %1, %0" : "=r"(r) : "r"(x));   // 컴파일러에게는 불투명한 블록
    return static_cast<int>(r);
}
int f_builtin() { return pop_builtin(0xFF); }
int f_asm()     { return pop_asm(0xFF); }
```

GCC 14.2 `-O2 -mpopcnt`의 결과입니다. 내장 함수 쪽은 컴파일 시점에 답 8을 계산해 상수만 반환하고, 인라인 어셈블리 쪽은 `popcnt` 명령이 그대로 남습니다.

```text
f_builtin():
        mov     eax, 8
        ret
f_asm():
        mov     eax, 255
        popcnt rax, rax
        ret
```

같은 원리로 intrinsic은 루프 안에서 불변식 이동, 레지스터 할당, 명령 스케줄링의 대상이 됩니다. 손으로 쓴 어셈블리가 의미 있는 경우는 컴파일러가 표현할 수 없는 명령 순서를 강제해야 할 때 정도로 좁혀집니다.

## SIMD intrinsic: 명령어 집합과 빌드 플래그

x86 SIMD intrinsic은 이름이 명령어 집합과 레지스터 폭을 드러냅니다. `_mm_` 접두는 128비트(`__m128` 등, SSE 계열), `_mm256_`은 256비트(`__m256`, AVX 계열), `_mm512_`는 512비트(AVX-512) 연산입니다. 주의할 점은 접두사만으로 필요한 명령어 집합이 정해지지 않는다는 것입니다. 256비트 **부동소수점** 연산인 `_mm256_add_ps`, `_mm256_loadu_ps`, `_mm256_extractf128_ps`는 AVX에 속하고, AVX2가 추가한 것은 주로 256비트 **정수** 연산(`_mm256_add_epi32` 등)과 gather입니다. 수평 덧셈 `_mm_hadd_ps`는 SSE3, 곱셈-누산 `_mm256_fmadd_ps`는 FMA에 속합니다. 어떤 intrinsic이 어떤 기능을 요구하는지는 Intel Intrinsics Guide에서 확인할 수 있고, GCC의 [x86 Built-in Functions 문서](https://gcc.gnu.org/onlinedocs/gcc/x86-Built-in-Functions.html)도 기능 플래그(`-mavx`, `-mavx2` 등)별로 사용 가능한 내장 함수를 나눠 적어 둡니다.

필요한 기능을 켜지 않고 intrinsic을 쓰면 어떻게 될까요. x86 SIMD intrinsic은 헤더에 `always_inline` 함수로 정의되어 있어서, 컴파일러는 호출로 남기는 대신 **컴파일 오류**를 냅니다. 아래 함수를 `-O2`만으로 컴파일하면 두 컴파일러 모두 거부합니다.

```cpp
#include <immintrin.h>
__m256 add8(__m256 a, __m256 b) { return _mm256_add_ps(a, b); }
```

```text
# GCC 14.2
avxintrin.h:147:1: error: inlining failed in call to 'always_inline' '__m256 _mm256_add_ps(__m256, __m256)': target specific option mismatch
# Clang 19.1.0
<source>:2:42: error: always_inline function '_mm256_add_ps' requires target feature 'avx', but would be inlined into function 'add8' that is compiled without support for 'avx'
```

Clang 메시지가 요구하는 기능이 'avx2'가 아니라 'avx'라는 점이 위 설명을 그대로 확인해 줍니다. 해결책은 빌드 전체에 `-mavx`(또는 `-march=`)를 주거나, 해당 함수에만 `__attribute__((target("avx")))`를 붙이는 것입니다. 후자는 다른 CPU에서도 실행되는 바이너리를 만들 때 쓰며, 실행 시점 기능 검사와 함께 쓰는 방법은 [챕터 07 함수 멀티버저닝](/post/compiler-optimization/function-multiversioning-cpu/)에서 다룹니다.

아래 예제는 이 규칙을 반영한 이식형 합산 함수입니다. 컴파일 타깃이 AVX를 지원하면 AVX 경로, AArch64면 NEON 경로, 둘 다 아니면 스칼라 경로를 고릅니다. 세 경로 모두 같은 파일에 정의되어 있어 그대로 컴파일·실행되며, x86-64 gcc 14.2(`-O2 -mavx`와 `-O2`)와 clang 19.1.0(`-O2 -mavx`)에서 실행 결과는 모두 `171.0 171.0`이었고, ARM64 gcc 14.2.0 `-O2`에서는 NEON의 `fadd v.4s`와 `faddp`로 컴파일됐습니다.

```cpp
// portable_sum.cc: 컴파일 타깃에 따라 경로를 고르는 래퍼 (x86 AVX / AArch64 NEON / 스칼라)
#include <cstddef>
#include <cstdio>

static float sum_scalar(const float* arr, std::size_t n) {
    float s = 0.0f;
    for (std::size_t i = 0; i < n; ++i) s += arr[i];
    return s;
}

#if defined(__AVX__)
#include <immintrin.h>
static float sum_simd(const float* arr, std::size_t n) {
    __m256 acc = _mm256_setzero_ps();
    std::size_t i = 0;
    for (; i + 8 <= n; i += 8) acc = _mm256_add_ps(acc, _mm256_loadu_ps(arr + i));
    __m128 s4 = _mm_add_ps(_mm256_castps256_ps128(acc), _mm256_extractf128_ps(acc, 1));
    s4 = _mm_hadd_ps(s4, s4);
    s4 = _mm_hadd_ps(s4, s4);
    return _mm_cvtss_f32(s4) + sum_scalar(arr + i, n - i);
}
#elif defined(__ARM_NEON) && defined(__aarch64__)
#include <arm_neon.h>
static float sum_simd(const float* arr, std::size_t n) {
    float32x4_t acc = vdupq_n_f32(0.0f);
    std::size_t i = 0;
    for (; i + 4 <= n; i += 4) acc = vaddq_f32(acc, vld1q_f32(arr + i));
    return vaddvq_f32(acc) + sum_scalar(arr + i, n - i);   // 4개 레인 수평 합
}
#else
static float sum_simd(const float* arr, std::size_t n) { return sum_scalar(arr, n); }
#endif

int main() {
    float a[19];
    for (int i = 0; i < 19; ++i) a[i] = static_cast<float>(i);
    std::printf("%.1f %.1f\n", sum_simd(a, 19), sum_scalar(a, 19));   // 171.0 171.0
}
```

x86과 ARM의 SIMD intrinsic은 이름 체계가 완전히 다릅니다. x86은 `_mm256_add_ps`처럼 폭과 타입을 접두·접미로 붙이고, ARM NEON은 `vaddq_f32`처럼 연산·레지스터 폭(`q`=128비트)·원소 타입을 이름에 넣습니다. 같은 알고리즘이라도 두 벌을 따로 써야 하는 이유입니다.

## 원자 연산 intrinsic

GCC·Clang의 `__atomic_*` 내장 함수는 C++11 메모리 모델의 메모리 순서를 인자로 받는 원자 연산입니다. [GCC `__atomic` Builtins 문서](https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html)가 정의하는 순서 인자(`__ATOMIC_RELAXED`, `__ATOMIC_ACQUIRE`, `__ATOMIC_SEQ_CST` 등)는 `std::memory_order`와 같은 의미이며, `std::atomic`의 구현도 이 계열 내장 함수로 내려갑니다. 아래는 이를 직접 쓴 카운터입니다.

```cpp
// atomic_example.cc: __atomic_* 내장 함수 기반 lock-free 카운터
#include <cstdint>

struct LockFreeCounter {
    int64_t value = 0;

    void increment() {                       // 순서 보장 없이 원자성만 필요
        __atomic_fetch_add(&value, 1, __ATOMIC_RELAXED);
    }
    int64_t get() const {                    // 이후 읽기가 이 읽기 앞으로 오지 않음
        return __atomic_load_n(&value, __ATOMIC_ACQUIRE);
    }
    bool compare_and_swap(int64_t expected, int64_t desired) {
        return __atomic_compare_exchange_n(
            &value, &expected, desired,
            /*weak=*/false, __ATOMIC_ACQ_REL, __ATOMIC_ACQUIRE);
    }
};
```

x86-64에서 `__atomic_fetch_add`는 반환값을 쓰지 않으면 `lock add`, 쓰면 `lock xadd`로 내려갑니다(GCC 14.2 `-O2` 실측). 같은 함수를 `__ATOMIC_SEQ_CST`로 바꿔도 GCC 14.2의 출력은 똑같이 `lock add`/`lock xadd`였습니다. x86에서는 `lock` 접두 명령 자체가 완전한 장벽 역할을 하기 때문이지만, ARM 같은 약한 메모리 모델에서는 순서 인자에 따라 다른 명령과 장벽이 생성됩니다. 따라서 x86에서 relaxed로 테스트를 통과했다고 해서 ARM에서도 올바르다는 보장은 없습니다. 실무에서는 `std::atomic<T>`가 같은 코드를 이식성 있게 표현하므로, 내장 함수를 직접 쓰는 것은 C 코드나 `std::atomic`으로 감쌀 수 없는 기존 메모리에 원자 연산을 걸어야 할 때로 한정하는 편이 좋습니다.

## 비트 조작 내장 함수: 플래그에 따라 바뀌는 코드

`__builtin_popcountll`, `__builtin_clz`, `__builtin_ctz`, `__builtin_bswap32` 같은 비트 조작 내장 함수는 흔히 "명령 하나로 내려간다"고 소개되지만, 이는 대상 CPU 기능이 켜져 있을 때의 이야기입니다. x86-64 기본 타깃에는 POPCNT와 LZCNT가 포함되지 않으므로, 컴파일 옵션에 따라 생성 코드가 크게 달라집니다.

```cpp
// bit_intrinsics.cc
#include <cstdint>
int count_bits(uint64_t x) { return __builtin_popcountll(x); }
int leading_zeros(uint32_t x) { return x == 0 ? 32 : __builtin_clz(x); }
uint32_t byte_swap(uint32_t x) { return __builtin_bswap32(x); }
```

| 함수 | GCC 14.2 `-O2` | Clang 19.1.0 `-O2` | 둘 다 `-O2 -mpopcnt -mlzcnt` |
|------|----------------|--------------------|------------------------------|
| `count_bits` | libgcc `__popcountdi2` 호출 | 시프트·마스크·곱셈 비트 연산 약 18개 | `popcnt` 한 개 |
| `leading_zeros` | 0 검사 + `bsr` + `xor` | 0 검사 + `bsr` + `xor` | `lzcnt` 한 개(0 검사도 사라짐) |
| `byte_swap` | `bswap` | `bswap` | `bswap` |

`bswap`은 x86-64 기본 명령이라 항상 한 명령이지만, popcount는 기능 플래그 없이는 GCC에서 라이브러리 함수 호출이 됩니다. SIMD intrinsic과 달리 이런 내장 함수는 기능이 없어도 오류가 아니라 **대체 구현으로 조용히 바뀐다**는 점이 차이입니다. 그래서 핫 루프에서 popcount를 쓴다면 `-mpopcnt`나 `-march`가 실제로 켜져 있는지 어셈블리로 확인해야 합니다. `leading_zeros`의 0 검사가 `-mlzcnt`에서 사라진 것도 흥미롭습니다. `lzcnt`는 입력 0에 대해 32를 돌려주도록 정의되어 있어, 컴파일러가 별도 분기를 지운 것입니다. 반면 [GCC Bit Operation Builtins 문서](https://gcc.gnu.org/onlinedocs/gcc/Bit-Operation-Builtins.html)는 `__builtin_clz`에 0을 넣은 결과를 정의하지 않으므로, 소스 코드에서는 이 검사를 생략하면 안 됩니다.

## 컴파일러·플랫폼별 차이

x86 SIMD intrinsic(`_mm_*`, `_mm256_*`)은 Intel이 정한 이름과 `<immintrin.h>` 헤더를 GCC·Clang·MSVC가 공유하므로, 이 부분은 소스 그대로 세 컴파일러에서 통합니다. 차이가 나는 것은 GCC·Clang의 `__builtin_*`·`__atomic_*` 계열입니다. MSVC는 이들 대신 `<intrin.h>`의 자체 intrinsic을 씁니다. 예를 들어 popcount는 [`__popcnt`/`__popcnt64`](https://learn.microsoft.com/en-us/cpp/intrinsics/popcnt16-popcnt-popcnt64), leading zero는 `_BitScanReverse`, 바이트 스왑은 `_byteswap_ulong`, 원자 증가는 `_InterlockedIncrement` 계열입니다. MS Learn 문서는 `__popcnt` 계열이 항상 `popcnt` 명령을 생성하며, 이 명령을 지원하지 않는 하드웨어에서 실행하면 결과를 예측할 수 없으므로 `__cpuid`로 지원 여부를 확인하라고 안내합니다. GCC의 `__builtin_popcountll`이 기능이 없으면 라이브러리 호출로 대체되는 것과 반대 방향의 함정입니다.

ARM 쪽은 NEON(`arm_neon.h`)과 SVE(`arm_sve.h`)가 별도의 intrinsic 세트를 가지며, 이름 규칙은 Arm의 ACLE 명세가 정합니다. x86 코드와 공유되는 부분이 없으므로 여러 아키텍처를 지원하려면 위 예제처럼 `#if`로 경로를 나누거나, 이 분기를 대신 관리해 주는 래퍼 라이브러리를 쓰게 됩니다.

## 카테고리별 요약

| 범주 | GCC·Clang 예 | MSVC 대응 | 빌드 시 확인할 것 |
|------|-------------|-----------|------------------|
| x86 SIMD | `_mm256_add_ps`(AVX), `_mm256_add_epi32`(AVX2), `_mm256_fmadd_ps`(FMA) | 동일 이름·`<immintrin.h>` | 필요한 기능 플래그 또는 `target` 속성(없으면 컴파일 오류) |
| ARM SIMD | `vaddq_f32`, `vaddvq_f32`(AArch64) | 동일 이름·`<arm_neon.h>` | 대상 아키텍처 |
| 원자 연산 | `__atomic_fetch_add`, `__atomic_compare_exchange_n` | `_InterlockedIncrement` 등 | 메모리 순서 인자, 가능하면 `std::atomic` |
| 비트 조작 | `__builtin_popcountll`, `__builtin_clz` | `__popcnt64`, `_BitScanReverse` | `-mpopcnt`/`-mlzcnt`(없으면 대체 코드), 0 입력 처리 |

## 판단 기준: 언제 intrinsic을 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 자동 벡터화가 실패한 핫 루프 | 리포트로 원인 확인 후 필요하면 SIMD intrinsic | 인라인 어셈블리로 직접 작성 |
| 비트 연산이 많은 핫 경로 | 내장 함수 + 기능 플래그 확인 | 플래그 없이 "한 명령"이라고 가정 |
| 원자 연산 | `std::atomic` 우선, 필요할 때만 `__atomic_*` | x86 테스트만으로 메모리 순서 검증 |

## 자주 하는 실수

- **`_mm256_` 접두사면 AVX2가 필요하다고 생각하기**: 256비트 부동소수점 연산은 AVX, 256비트 정수 연산은 AVX2, FMA는 별도 기능이다. 빌드 플래그를 실제 사용한 intrinsic에 맞춘다.
- **intrinsic이면 항상 빠르다고 생각하기**: 내장 함수 popcount도 기능 플래그가 없으면 GCC에서 라이브러리 호출이 된다. intrinsic 코드가 자동 벡터화 결과보다 빠르다는 보장도 없으므로, 측정과 어셈블리 확인 없이 교체하지 않는다.
- **`__builtin_clz(0)`의 결과에 기대기**: GCC 문서상 정의되지 않은 결과다. `lzcnt`가 켜진 빌드에서 우연히 32가 나와도, 다른 빌드에서는 다른 값이 나올 수 있다.

## 학습 성과 목표

- intrinsic이 인라인 어셈블리와 달리 옵티마이저의 대상이 되는 이유를 상수 접기 예로 설명할 수 있다.
- SIMD intrinsic마다 필요한 명령어 집합(SSE3·AVX·AVX2·FMA)을 구분하고, 기능이 빠졌을 때의 컴파일 오류와 비트 조작 내장 함수의 조용한 대체를 구별할 수 있다.
- GCC·Clang 내장 함수와 MSVC intrinsic의 대응을 알고, 플랫폼별 경로를 컴파일 가능한 형태로 나눌 수 있다.

## 비판적 시각: 한계와 트레이드오프

intrinsic은 특정 명령어 집합에 묶인 API라서, 쓰는 순간 코드가 그 아키텍처와 기능 수준에 고정됩니다. 위 합산 예제처럼 x86과 ARM을 함께 지원하면 같은 알고리즘의 구현이 두세 벌이 되고, 각각을 테스트할 장비나 에뮬레이터가 필요합니다. 또 intrinsic으로 고정한 알고리즘 구조는 새 명령어 집합이 나와도 저절로 바뀌지 않습니다. 자동 벡터화된 루프는 `-march`만 올리면 AVX-512 코드로 다시 생성되지만, `_mm256_*`로 쓴 코드는 사람이 `_mm512_*` 버전을 새로 써야 합니다. 이런 이유로 Highway나 xsimd 같은 SIMD 래퍼 라이브러리는 아키텍처별 분기와 런타임 디스패치를 대신 관리하는 추상화를 제공합니다. intrinsic은 자동 벡터화와 이런 라이브러리로 해결되지 않는 핫 경로에 한정해, 어셈블리와 측정으로 효과를 확인하며 쓰는 것이 합리적입니다.

## 다음 장에서는

**Sanitizer**(ASan, UBSan, TSan 등)의 런타임 오버헤드와 디버그/CI vs 릴리즈 전략을 다룹니다.

→ [Sanitizer 오버헤드](/post/compiler-optimization/sanitizer-overhead-performance/) (챕터 09)
