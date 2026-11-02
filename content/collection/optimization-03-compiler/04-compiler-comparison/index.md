---
collection_order: 4
date: 2026-03-11
lastmod: 2026-10-20
draft: false
image: wordcloud.png
title: "[Compiler 03] GCC vs Clang vs MSVC 최적화 차이"
slug: compiler-comparison-gcc-clang-msvc
description: "GCC/Clang/MSVC가 같은 -O2에서도 다른 코드를 내는 이유를 벡터화 비용 모델·부동소수점 의미론·인라이닝 정책으로 설명하고, Compiler Explorer 실제 출력과 벡터화 리포트, Google Benchmark 측정 절차로 컴파일러를 비교·선택하는 방법을 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Assembly(어셈블리)
  - SIMD(단일명령다중데이터)
  - Vectorization(벡터화)
  - Floating-Point(부동소수점)
  - IEEE-754(부동소수점표준)
  - Numerical-Computing(수치계산)
  - Low-Level(로우레벨)
  - Benchmark
  - Comparison(비교)
  - History(역사)
  - Open-Source(오픈소스)
  - Cache
  - Linux(리눅스)
  - Windows(윈도우)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Testing(테스트)
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
  - LLVM
  - MSVC
---

같은 C++ 코드라도 **컴파일러**에 따라 생성 코드와 성능이 달라집니다. **GCC**, **Clang**, **MSVC**는 최적화 수준별로 켜는 패스, 부동소수점 의미론을 지키는 방식, 인라이닝 휴리스틱이 서로 달라서 "같은 -O2"라는 말이 같은 기계어를 뜻하지 않습니다. 이 챕터에서는 세 컴파일러가 실제로 어디서 갈라지는지를 Compiler Explorer의 실제 출력으로 확인하고, 그 차이를 자신의 워크로드에서 재현 가능하게 측정하는 절차와 플랫폼별 선택 기준을 다룹니다.

## 역사·배경

세 컴파일러는 서로 다른 필요에서 출발했고, 그 출발점이 오늘날의 기본값 차이로 이어집니다.

<strong>GCC(GNU Compiler Collection)</strong>는 Richard Stallman이 GNU 프로젝트의 일부로 만든 컴파일러로, [GCC 릴리스 기록](https://gcc.gnu.org/releases.html)에 따르면 첫 베타(0.9)가 1987년 3월 22일, 1.0이 같은 해 5월 23일에 나왔습니다. 수십 년 동안 매우 많은 아키텍처를 지원하는 것이 핵심 목표였기 때문에, 최적화 수준별 기본값도 "어느 타깃에서나 안전하게 이득이 나는 쪽"으로 보수적으로 잡혀 있는 경우가 많습니다. 뒤에서 볼 `-O2`의 벡터화 비용 모델이 대표적인 예입니다.

**Clang**은 2007년 Apple이 주도해 공개한 LLVM 기반 C/C++ 프론트엔드입니다. 모듈화된 컴파일러 인프라, 빠른 컴파일과 읽기 쉬운 진단, 라이브러리로서의 재사용성이 설계 목표였습니다. 최적화는 프론트엔드가 아니라 LLVM IR 위의 공통 파이프라인에서 일어나므로, Rust·Swift 등 다른 LLVM 언어와 같은 벡터라이저·인라이너를 공유합니다.

<strong>MSVC(Microsoft Visual C++)</strong>는 Windows 개발 도구로 발전해 왔고, Visual Studio 통합과 Windows ABI·DLL 모델 호환이 최우선입니다. GCC/Clang이 `-O` 수준과 `-f` 플래그 체계를 공유하는 것과 달리 MSVC는 `/O2`, `/Ob`, `/fp`, `/arch` 같은 자체 옵션 체계를 쓰므로, 같은 의도를 표현하려면 옵션을 하나씩 대응시켜야 합니다.

## 차이가 생기는 세 지점

컴파일러 간 성능 차이를 "누가 더 똑똑한가"로 보면 원인을 찾기 어렵습니다. 실제로는 대부분 아래 세 지점 중 하나에서 갈라지고, 각 지점은 문서화된 기본값으로 설명됩니다.

### 1. 최적화 수준이 켜는 패스와 비용 모델

GCC는 12 버전부터 `-O2`에서도 루프 벡터화(`-ftree-loop-vectorize`)를 켜지만, [GCC Optimize Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) 문서의 `-O2` 목록에 함께 적힌 것은 `-fvect-cost-model=very-cheap`입니다. 같은 문서는 very-cheap 모델을 "데이터 의존성이나 정렬에 대한 런타임 검사가 필요하면 벡터화하지 않고, 에필로그 루프의 벡터화도 끈다"는 취지로 정의합니다. 반복 횟수 `n`을 컴파일 시점에 모르는 루프는 벡터 본체 뒤에 남은 원소를 처리할 에필로그가 필요한 경우가 많아서, GCC `-O2`에서는 벡터화가 포기되기 쉽습니다. `-O3`는 더 관대한 dynamic 모델을 씁니다.

Clang은 [LLVM Vectorizers](https://llvm.org/docs/Vectorizers.html) 문서대로 Loop Vectorizer와 SLP Vectorizer가 기본으로 켜져 있고, `-O2`에서도 런타임 검사와 스칼라 에필로그를 붙여 벡터화합니다. 그래서 "GCC -O2와 Clang -O2를 비교"하면 사실상 "벡터화하지 않은 코드와 벡터화한 코드"를 비교하게 되는 루프가 생깁니다. 이 차이는 컴파일러의 능력 차이가 아니라 **기본값의 차이**이므로, 비교할 때는 `-O3`끼리 맞추거나 GCC에 `-fvect-cost-model=dynamic`을 명시해 조건을 통일해야 합니다.

### 2. 부동소수점 의미론

부동소수점 덧셈은 결합법칙이 성립하지 않으므로, 순차 합산을 8개 레인으로 나눠 더하는 벡터화는 결과를 바꿀 수 있습니다. LLVM Vectorizers 문서는 이 때문에 LLVM이 부동소수점 리덕션을 "대부분의 타깃에서 최소한 `-fassociative-math -fno-signed-zeros -fno-trapping-math`가 켜졌을 때만" 벡터화한다고 밝힙니다. GCC 문서도 `-fassociative-math`를 "부동소수점 연산 피연산자의 재결합을 허용"하는 옵션으로 설명하고 기본값을 `-fno-associative-math`로 둡니다. MSVC는 [`/fp` 문서](https://learn.microsoft.com/en-us/cpp/build/reference/fp-specify-floating-point-behavior)에서 기본값 `/fp:precise`가 비트 단위로 같은 결과를 보장할 수 없는 재결합을 하지 않으며, `/fp:fast`가 결합법칙·분배법칙을 이용한 재배치를 허용한다고 설명합니다.

즉 세 컴파일러 모두 **기본 설정에서는 float 합산 루프를 벡터화하지 않습니다.** 이 사실을 모르고 한 컴파일러에만 `-ffast-math`를 켜서 비교하면, 차이의 원인을 컴파일러 탓으로 잘못 돌리게 됩니다.

### 3. 인라이닝 정책

인라이닝은 이후의 상수 전파·벡터화가 가능한지를 결정하는 관문이라, 임계값 차이가 생성 코드 전체로 번집니다. MSVC는 [`/Ob` 문서](https://learn.microsoft.com/en-us/cpp/build/reference/ob-inline-function-expansion)에서 `/O1`·`/O2`의 기본값을 `/Ob2`로 두고, Visual Studio 2019부터 더 공격적인 `/Ob3`를 제공합니다. GCC는 `-finline-functions`를 `-O2`부터 켜고 `-O3`에서 비용 한도를 더 높게 씁니다. Clang은 LLVM 인라이너의 비용 모델을 쓰므로 같은 함수라도 인라인 여부가 GCC와 다를 수 있습니다. 인라이닝 결정을 직접 확인하는 방법은 [다음 챕터](/post/compiler-optimization/inlining-diagnostics/)에서 다룹니다.

## 실제 출력으로 확인하기: float 합산 루프

아래 함수를 세 컴파일러로 컴파일해 보면 위의 두 지점(비용 모델, 부동소수점 의미론)이 그대로 드러납니다. 출력은 2026년 10월 [Compiler Explorer](https://godbolt.org)에서 x86-64 gcc 14.2, x86-64 clang 19.1.0, x64 msvc v19.latest로 얻었으며, 재현성을 위해 `-march=native` 대신 `-mavx2`를 썼습니다.

```cpp
// sum.cc: 컴파일러별 벡터화 차이를 관찰하기 위한 최소 예시
float sum_array(const float* arr, int n) {
    float s = 0.0f;
    for (int i = 0; i < n; ++i)
        s += arr[i];
    return s;
}
```

```bash
# 어셈블리 추출 (AT&T 문법)
g++     -O2 -mavx2 -S sum.cc -o sum_gcc.s
clang++ -O2 -mavx2 -S sum.cc -o sum_clang.s
# 벡터화 여부는 접미사로 판별: vaddps(packed) = 벡터, vaddss(scalar) = 스칼라
grep -E "vadd(ps|ss)" sum_gcc.s sum_clang.s
```

먼저 기본 설정인 `-O2 -mavx2`입니다. 두 컴파일러 모두 `vaddss`, 즉 **스칼라** 덧셈만 냅니다. 차이는 언롤링 폭뿐으로, GCC는 2회, Clang은 8회 펼쳤습니다. AVX가 켜지면 스칼라 연산도 VEX 인코딩이라 `v` 접두사가 붙으므로, 접두사가 아니라 `ps`/`ss` 접미사와 레지스터 폭으로 벡터화를 판단해야 합니다.

```text
# GCC 14.2 -O2 -mavx2 (루프 본체)
.L3:
        vaddss  (%rdi), %xmm0, %xmm0
        addq    $8, %rdi
        vaddss  -4(%rdi), %xmm0, %xmm0
        cmpq    %rax, %rdi
        jne     .L3

# Clang 19.1.0 -O2 -mavx2 (루프 본체, 일부)
.LBB0_9:
        vaddss  (%rdi,%rcx,4), %xmm0, %xmm0
        vaddss  4(%rdi,%rcx,4), %xmm0, %xmm0
        ...                                  # 같은 패턴 8회
        vaddss  28(%rdi,%rcx,4), %xmm0, %xmm0
        addq    $8, %rcx
        cmpq    %rcx, %rdx
        jne     .LBB0_9
```

Clang이 왜 벡터화하지 않았는지는 `-Rpass-analysis=loop-vectorize`로 물어보면 컴파일러가 직접 답합니다. 실제 출력은 다음과 같습니다.

```text
<source>:4:11: remark: loop not vectorized: cannot prove it is safe to reorder floating-point operations; allow reordering by specifying '#pragma clang loop vectorize(enable)' before the loop or by providing the compiler option '-ffast-math' [-Rpass-analysis=loop-vectorize]
```

이제 재결합을 허용하면(`-ffast-math`, MSVC는 `/fp:fast`) 결과가 갈라집니다. Clang은 `-O2`에서 곧바로 256비트 `vaddps`를 4개 누산기로 펼친 벡터 루프를 만듭니다. MSVC도 `/O2 /arch:AVX2 /fp:fast`에서 `vaddps ymm` 루프를 냅니다. 반면 GCC는 `-O2 -ffast-math`에서도 여전히 스칼라 루프였고, `-O3 -ffast-math`나 `-O2 -ffast-math -fvect-cost-model=cheap`으로 비용 모델을 풀어 줘야 `vaddps`가 나왔습니다. 앞에서 본 very-cheap 비용 모델이 에필로그가 필요한 이 루프를 거부한 것입니다.

```text
# Clang 19.1.0 -O2 -mavx2 -ffast-math (벡터 본체)
.LBB0_5:
        vaddps  (%rdi,%rsi), %ymm0, %ymm0
        vaddps  32(%rdi,%rsi), %ymm1, %ymm1
        vaddps  64(%rdi,%rsi), %ymm2, %ymm2
        vaddps  96(%rdi,%rsi), %ymm3, %ymm3
        subq    $-128, %rsi
        cmpq    %rsi, %rdx
        jne     .LBB0_5

# GCC 14.2 -O3 -mavx2 -ffast-math (벡터 본체)
.L4:
        vaddps  (%rax), %ymm0, %ymm0
        addq    $32, %rax
        cmpq    %rax, %rdx
        jne     .L4

; MSVC v19.latest /O2 /arch:AVX2 /fp:fast (벡터 본체, Intel 문법)
$LL4@sum_array:
        movsxd  rax, r8d
        add     r8d, 16
        vaddps  ymm1, ymm1, YMMWORD PTR [rcx+rax*4]
        vaddps  ymm2, ymm2, YMMWORD PTR [rcx+rax*4+32]
        cmp     r8d, r9d
        jl      SHORT $LL4@sum_array
```

같은 "벡터화 성공"이라도 모양은 다릅니다. Clang은 반복당 32개 float를 4개 독립 누산기로 처리해 `vaddps`의 지연 시간을 숨기고, MSVC는 누산기 2개로 16개, GCC `-O3`는 누산기 1개로 8개를 처리합니다. 누산기가 하나뿐이면 매 반복이 직전 덧셈 결과를 기다려야 하므로, 데이터가 L1 캐시에 들어가는 크기에서는 이 구조 차이가 처리량 차이로 이어질 수 있습니다. 다만 그 크기는 CPU의 `vaddps` 지연·처리량에 달려 있으므로 숫자를 추정하지 말고 아래 절차로 측정해야 합니다.

| 설정 | GCC 14.2 | Clang 19.1.0 | MSVC v19.latest |
|------|----------|--------------|-----------------|
| 기본(`-O2`/`/O2`, AVX2) | 스칼라 `vaddss`, 2회 언롤 | 스칼라 `vaddss`, 8회 언롤 | 스칼라 `vaddss` |
| 재결합 허용(`-ffast-math`/`/fp:fast`), `-O2` | 스칼라(very-cheap 모델) | `vaddps ymm` × 4 누산기 | `vaddps ymm` × 2 누산기 |
| 재결합 허용, GCC `-O3` | `vaddps ymm` × 1 누산기 | – | – |

[Compiler Explorer](https://godbolt.org)에 같은 소스를 열고 컴파일러 탭을 여러 개 띄우면 이 표를 몇 분 안에 직접 만들 수 있습니다. 플래그 한 개를 바꿀 때마다 어느 줄이 바뀌는지 바로 보이므로, 벤치마크를 돌리기 전에 "차이가 존재하는가"를 확인하는 첫 단계로 쓰기 좋습니다.

## 벡터화 리포트로 원인 묻기

어셈블리를 읽는 것보다 빠른 방법은 컴파일러에게 이유를 묻는 것입니다. 세 컴파일러 모두 벡터화 결과를 보고하는 옵션을 제공하지만 이름과 출력 형식이 다릅니다. Clang은 LLVM Vectorizers 문서가 설명하는 `-Rpass=loop-vectorize`(성공), `-Rpass-missed=loop-vectorize`(실패), `-Rpass-analysis=loop-vectorize`(실패한 이유가 된 문장)를 씁니다. GCC는 `-fopt-info-vec-optimized`와 `-fopt-info-vec-missed`를 쓰는데, 실패 메시지가 내부 분석 단계를 그대로 드러내는 경우가 많아 Clang보다 해석이 어렵습니다. MSVC는 [`/Qvec-report:1`·`/Qvec-report:2`](https://learn.microsoft.com/en-us/cpp/build/reference/qvec-report-auto-vectorizer-reporting-level)로 벡터화된 루프만, 또는 벡터화되지 않은 루프와 이유 코드까지 출력합니다.

```bash
clang++ -O2 -mavx2 -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize -c sum.cc
g++     -O3 -mavx2 -fopt-info-vec-missed -c sum.cc
# MSVC: cl /O2 /arch:AVX2 /Qvec-report:2 /c sum.cc
```

다중 컴파일러 비교에서 리포트가 특히 유용한 이유는, 한 컴파일러만 벡터화에 실패한 루프를 찾았을 때 그 원인이 재결합 금지인지, 별칭(aliasing) 검사 비용인지, 비용 모델인지 바로 구분해 주기 때문입니다. 원인이 재결합이면 `-ffast-math` 전체 대신 해당 루프에 `#pragma omp simd reduction(+:s)` 같은 국소적 허용을 거는 편이 다른 코드의 정밀도를 지킬 수 있습니다.

## 동일 벤치마크로 컴파일러별 수치 비교

어셈블리와 리포트는 차이가 "있다"는 것을 보여 줄 뿐, 그 차이가 실행 시간에 얼마나 반영되는지는 측정해야 압니다. 아래는 [Google Benchmark](https://github.com/google/benchmark)로 위 함수를 측정하는 완결된 예제입니다. 결과가 상수로 접혀 사라지지 않도록 `benchmark::DoNotOptimize`로 반환값을 붙잡고, 입력 크기를 L1에 들어가는 1K부터 메모리 대역폭이 지배하는 1M까지 바꿔 가며 측정합니다.

```cpp
// benchmark.cc
#include <benchmark/benchmark.h>
#include <vector>

float sum_array(const float* arr, int n) {
    float s = 0.0f;
    for (int i = 0; i < n; ++i)
        s += arr[i];
    return s;
}

static void BM_sum(benchmark::State& state) {
    const int n = static_cast<int>(state.range(0));
    std::vector<float> v(n, 1.0f);
    for (auto _ : state) {
        float r = sum_array(v.data(), n);
        benchmark::DoNotOptimize(r);
    }
    state.SetItemsProcessed(state.iterations() * n);
}
BENCHMARK(BM_sum)->RangeMultiplier(8)->Range(1 << 10, 1 << 20);

BENCHMARK_MAIN();
```

```bash
# 1. 같은 소스, 컴파일러만 바꿔 빌드 (Google Benchmark 설치 경로는 환경에 맞게)
g++     -O2 -mavx2 benchmark.cc -o bench_gcc   -lbenchmark -lpthread
clang++ -O2 -mavx2 benchmark.cc -o bench_clang -lbenchmark -lpthread
# 같은 조건에 재결합 허용을 추가한 변형
g++     -O3 -mavx2 -ffast-math benchmark.cc -o bench_gcc_fast   -lbenchmark -lpthread
clang++ -O2 -mavx2 -ffast-math benchmark.cc -o bench_clang_fast -lbenchmark -lpthread
# Windows MSVC: cl /O2 /arch:AVX2 /EHsc benchmark.cc /I<include> /link benchmark.lib

# 2. 반복 측정 후 집계만 JSON으로 저장
for b in bench_gcc bench_clang bench_gcc_fast bench_clang_fast; do
  taskset -c 2 ./$b --benchmark_repetitions=10 \
    --benchmark_report_aggregates_only=true \
    --benchmark_out=$b.json --benchmark_out_format=json
done
```

측정에서 지켜야 할 원칙은 "컴파일러 외에는 아무것도 바꾸지 않는다"입니다. 같은 소스 트리와 의존성, 같은 최적화 수준과 부동소수점 옵션을 쓰고, `taskset`으로 코어를 고정하며, 반복 측정의 평균과 표준편차(또는 중앙값과 분산)를 함께 기록합니다. 두 바이너리의 차이가 반복 간 표준편차보다 작으면 의미 있는 차이로 보지 않는 것이 안전합니다. 결과 JSON을 저장소에 남겨 두면 컴파일러를 업그레이드할 때 같은 명령으로 전후를 비교할 수 있고, CI에 다중 컴파일러 빌드 단계를 두면 특정 컴파일러에서만 성능이 깨지는 변경을 조기에 잡을 수 있습니다.

## 플랫폼별 선택

Linux에서는 GCC가 배포판의 기본 시스템 컴파일러인 경우가 많고, 배포 대상의 glibc·libstdc++ 버전과 ABI를 맞추기 쉽다는 실무적 이점이 있습니다. Clang은 같은 libstdc++를 그대로 쓸 수 있어 전환 비용이 낮고, sanitizer·LTO·PGO 도구가 LLVM 생태계 안에서 일관되게 동작한다는 장점이 있습니다. 두 컴파일러 모두 쉽게 설치되므로, Linux에서는 양쪽으로 빌드해 보고 측정 결과로 고르는 것이 비용 대비 효과가 가장 큽니다.

Windows에서는 MSVC가 Visual Studio·Windows SDK와 통합된 기본 선택입니다. clang-cl은 MSVC의 명령줄 옵션과 ABI를 흉내 내는 Clang 드라이버라서, 빌드 시스템을 거의 건드리지 않고 컴파일러만 바꿔 비교할 수 있습니다. MSVC의 명령어 집합 지원은 [`/arch` (x64) 문서](https://learn.microsoft.com/en-us/cpp/build/reference/arch-x64)대로 단계적으로 늘어 왔습니다. `/arch:AVX2`는 Visual Studio 2013 Update 2에서 도입됐고, `/arch:AVX512`는 Visual Studio 2017에서 제한적으로 지원되기 시작해 2019에서 확장됐으며, `/arch:AVX10.1`은 Visual Studio 2022(17.13)에서 추가됐습니다. 사용하는 Visual Studio 버전이 목표 명령어 집합을 지원하는지부터 확인해야 합니다.

타깃 CPU가 정해져 있으면 GCC/Clang의 `-march`·`-mtune`, MSVC의 `/arch`로 명령어 집합을 명시합니다. 단 `-march=native`로 빌드한 바이너리는 빌드 머신의 CPU 기능을 가정하므로, 다른 CPU에 배포할 때는 쓸 수 없습니다. 여러 CPU 세대를 한 바이너리로 지원하는 방법은 [함수 멀티버저닝](/post/compiler-optimization/function-multiversioning-cpu/) 챕터에서 다룹니다.

## 실전 시나리오: 컴파일러 선택 결정 과정

Linux 서버용 수치 처리 서비스를 새로 빌드한다고 가정합니다. 먼저 GCC와 Clang으로 같은 `-O2`와 같은 부동소수점 옵션을 써서 두 바이너리를 만들고, 핫패스를 덮는 벤치마크를 각 10회 이상 실행합니다. 두 결과의 차이가 반복 간 표준편차 안에 있으면 팀의 도구 체인과 CI 환경에 더 잘 맞는 쪽을 고르면 됩니다.

차이가 크게 나면 바로 빠른 쪽을 채택하지 말고 원인부터 확인합니다. 핫 함수에 벡터화 리포트를 걸어 한쪽만 벡터화에 실패했는지 보고, 원인이 앞서 본 GCC `-O2` 비용 모델처럼 기본값 차이라면 플래그로 조건을 맞춘 뒤 다시 측정합니다. 기본값을 맞춘 뒤에도 차이가 남는다면 그때 비로소 컴파일러의 코드 생성 차이로 볼 수 있습니다. 선택한 컴파일러와 버전, 플래그는 CI에 고정하고, 툴체인을 올릴 때마다 저장해 둔 벤치마크 JSON과 비교해 회귀를 감지합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **auto-vectorization** | 컴파일러가 루프를 자동으로 SIMD 명령으로 바꾸는 최적화 |
| **리덕션(reduction)** | 여러 원소를 하나의 값으로 모으는 연산(합, 곱, 최대값 등). 부동소수점 합은 재결합 허용이 있어야 벡터화된다 |
| **cost model** | 벡터화가 이득인지 판단하는 컴파일러 내부 모델. GCC `-O2`는 very-cheap, `-O3`는 dynamic |
| **packed / scalar** | `vaddps`처럼 레지스터의 모든 레인을 쓰는 연산과 `vaddss`처럼 최하위 레인 하나만 쓰는 연산 |
| **YMM** | 256비트 AVX 레지스터. float 8개 또는 double 4개를 담는다 |

## 판단 기준: 언제 어떤 컴파일러를 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| Linux 배포 | GCC·Clang 양쪽 빌드 후 측정으로 선택 | 비교 없이 한 컴파일러로 고정 |
| Windows 네이티브 | MSVC 기본, clang-cl로 교차 확인 | 다른 플랫폼 측정 결과를 그대로 적용 |
| 수치 커널 비교 | `-O` 수준·`-ffast-math`/`/fp`를 세 컴파일러에 동일하게 | 한쪽에만 `-ffast-math`를 켜고 비교 |
| 표준 준수·버그 검출 | 다중 컴파일러 빌드를 CI에 상시 유지 | 한 컴파일러의 경고만 신뢰 |

## 자주 하는 실수

- **기본값 차이를 컴파일러 성능 차이로 오해하기**: GCC `-O2`와 Clang `-O2`는 벡터화 비용 모델이 달라, 같은 루프에서 한쪽만 벡터화될 수 있다. 비교 전에 벡터화 리포트로 조건이 같은지부터 확인한다.
- **한쪽에만 `-ffast-math`를 켜기**: float 리덕션은 재결합 허용 없이는 세 컴파일러 모두 벡터화하지 않는다. 플래그가 다르면 컴파일러가 아니라 부동소수점 의미론을 비교하게 된다.
- **`v` 접두사로 벡터화를 판단하기**: AVX가 켜진 빌드에서는 스칼라 연산도 `vaddss`처럼 `v`로 시작한다. `ps`/`pd` 접미사와 ymm/zmm 레지스터를 확인한다.
- **컴파일러 전환 후 성능 회귀를 측정하지 않기**: 툴체인을 바꾼 뒤 단위 테스트만 돌리면, 특정 컴파일러에서만 느려지는 경로를 놓친다.

## 학습 성과 목표

- 동일 소스에서 GCC·Clang·MSVC의 생성 코드가 갈라지는 세 지점(비용 모델, 부동소수점 의미론, 인라이닝)을 문서화된 기본값으로 설명할 수 있다.
- 어셈블리의 `ps`/`ss` 접미사와 컴파일러별 벡터화 리포트로 벡터화 성공·실패와 그 원인을 판별할 수 있다.
- Google Benchmark로 컴파일러만 바꾼 바이너리를 재현 가능하게 측정하고, 차이가 유의미한지 판단할 수 있다.

## 비판적 시각: 한계와 트레이드오프

이 챕터의 예제는 의도적으로 단순한 루프 하나라서, 실제 코드베이스에서 컴파일러 간 차이가 어디서 얼마나 나는지는 대표하지 못합니다. 큰 프로그램의 성능은 인라이닝 연쇄, 분기 배치, 레지스터 할당처럼 단일 루프로 관찰하기 어려운 요인에 좌우되며, 그 경우에는 프로파일러로 핫 함수를 찾은 뒤 그 함수만 비교하는 편이 현실적입니다. 또 `-ffast-math`로 얻은 속도는 NaN·무한대·부호 있는 0의 처리와 결과의 비트 재현성을 포기한 대가이므로, "벡터화가 됐다"는 사실만으로 채택해서는 안 됩니다. 마지막으로 컴파일러 비교 결과는 버전에 묶여 있어서, 이 글의 GCC 14.2·Clang 19.1.0 출력도 다음 릴리스에서 바뀔 수 있습니다. 결론보다 위의 확인 절차를 재사용하는 것이 이 챕터의 목적입니다.

## 다음 장에서는

**인라이닝 실패** 원인(가시성, ODR/ABI, 코드 크기), 인라이닝 리포트 확인 방법, Tr.02 연계를 다룹니다.

→ [인라이닝 실패 진단](/post/compiler-optimization/inlining-diagnostics/) (챕터 05)
