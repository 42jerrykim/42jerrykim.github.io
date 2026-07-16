---
collection_order: 7
date: 2026-03-11
lastmod: 2026-07-12
draft: false
image: wordcloud.png
title: "[Compiler 03] CPU 기능별 함수 다중 버전"
slug: function-multiversioning-cpu
description: "런타임 CPU 기능 감지에 따라 최적 구현을 선택하는 함수 멀티버저닝을 다룹니다. GCC/Clang의 target·target_clones 속성 사용법, IFUNC 디스패치 비용, AVX2/AVX-512 등 경로별 빌드·배포 설계와 검증 방법을 정리합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Cache
  - Memory(메모리)
  - Benchmark
  - Profiling(프로파일링)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Testing(테스트)
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Linux(리눅스)
  - Windows(윈도우)
  - OS(운영체제)
  - Concurrency(동시성)
  - Latency
  - Throughput
  - Backend(백엔드)
  - Embedded(임베디드)
  - Debugging(디버깅)
  - Documentation(문서화)
  - Refactoring(리팩토링)
  - Clean-Code(클린코드)
  - Best-Practices
  - Git
  - Automation(자동화)
  - Software-Architecture(소프트웨어아키텍처)
  - Design-Pattern(디자인패턴)
  - Data-Structures(자료구조)
  - Time-Complexity(시간복잡도)
  - Complexity-Analysis(복잡도분석)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Error-Handling(에러처리)
  - Guide(가이드)
  - Reference(참고)
  - Technology(기술)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Case-Study
  - Assembly
---

멀티버저닝으로 CPU 기능(AVX2, AVX-512 등)에 맞는 구현을 런타임에 선택할 수 있습니다. 이 챕터에서는 문법과 디스패치 비용을 다룹니다.

## 멀티버저닝 개념

**함수 멀티버저닝(Function Multiversioning)**은 **같은 함수**에 대해 CPU 기능별로 **서로 다른 구현**을 두고, 실행 시점에 CPU가 지원하는 기능을 검사해 **해당하는 버전**을 호출하는 방식입니다. 예를 들어 "기본" 경로는 SSE만 쓰고, "AVX2" 경로는 256비트 SIMD를 쓰고, "AVX-512" 경로는 512비트 SIMD를 쓰도록 만들 수 있습니다. 한 바이너리를 여러 CPU에 배포할 때, 각 CPU에서 가장 적합한 구현이 자동으로 선택되므로, 호환성과 성능을 동시에 잡을 수 있습니다.

## GCC / Clang 문법과 코드 예시

멀티버저닝의 핵심은 **동일한 함수 이름에 서로 다른 target 속성을 붙인 여러 정의**를 두는 것입니다. 컴파일러가 자동으로 디스패치 코드를 생성합니다.

### GCC: `__attribute__((target(...)))`

```cpp
// multiversioning_demo.cc — GCC/Clang 공통 예시
#include <immintrin.h>
#include <cstddef>

// 기본 경로: SSE2 이상만 가정 (구형 CPU에서도 동작)
__attribute__((target("default")))
float dot_product(const float* a, const float* b, size_t n) {
    float sum = 0.0f;
    for (size_t i = 0; i < n; ++i)
        sum += a[i] * b[i];
    return sum;
}

// AVX2 경로: 256비트 SIMD로 8개 float 동시 처리
__attribute__((target("avx2")))
float dot_product(const float* a, const float* b, size_t n) {
    __m256 acc = _mm256_setzero_ps();
    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(a + i);
        __m256 vb = _mm256_loadu_ps(b + i);
        acc = _mm256_fmadd_ps(va, vb, acc);   // FMA: va * vb + acc
    }
    // 수평 합산 + 나머지 스칼라 처리 (생략)
    float buf[8];
    _mm256_storeu_ps(buf, acc);
    float s = buf[0]+buf[1]+buf[2]+buf[3]+buf[4]+buf[5]+buf[6]+buf[7];
    for (; i < n; ++i) s += a[i] * b[i];
    return s;
}
```

이 코드를 `-O2`로 빌드하면 컴파일러가 자동으로 **CPUID 기반 디스패치 코드**를 생성합니다. 프로그램이 AVX2를 지원하는 CPU에서 실행되면 `avx2` 버전이, 그렇지 않으면 `default` 버전이 호출됩니다.

### GCC: `target_clones`로 여러 버전 한 번에 생성

```cpp
// target_clones: 하나의 함수 정의에서 여러 버전 자동 생성
__attribute__((target_clones("avx512f", "avx2", "sse4.2", "default")))
void vector_add(float* dst, const float* src, size_t n) {
    for (size_t i = 0; i < n; ++i)
        dst[i] += src[i];
}
```

`target_clones`는 함수 정의를 한 번만 쓰고, 컴파일러가 각 타겟에 맞는 버전을 자동으로 생성합니다. 내부 루프에 SIMD intrinsic을 직접 쓰지 않아도 **auto-vectorization**이 타겟별로 다르게 적용됩니다.

### Clang: `__attribute__((target_version(...)))`

```cpp
// Clang에서도 비슷한 방식 — target_version 속성 사용
__attribute__((target_version("default")))
int process(int x) { return x * 2; }

__attribute__((target_version("avx2+fma")))
int process(int x) { return x * 3; }  // AVX2+FMA CPU에서 선택되는 버전
```

두 컴파일러 모두 **CPU 디스패치**를 위해 런타임에 CPUID 등을 사용해 "지금 CPU가 어떤 기능을 지원하는지" 확인하고, 그에 맞는 함수 포인터를 선택합니다. 이 선택은 보통 **프로그램 시작 시** 또는 **해당 함수가 처음 호출될 때** 한 번 이루어지고, 이후에는 같은 포인터를 사용합니다.

### 어셈블리에서 디스패치 확인

멀티버저닝을 적용하면 링크된 바이너리에 **ifunc resolver** 또는 유사한 간접 호출 메커니즘이 나타납니다.

```bash
# objdump로 resolver 함수와 여러 버전 확인
objdump -d ./app | grep -E "(dot_product|resolver)"
# dot_product.default:  -> 기본 경로
# dot_product.avx2:     -> AVX2 경로
# dot_product.ifunc:    -> 디스패치 포인터
```

## 디스패치 비용과 사용 시점

- **비용**: 디스패치는 보통 한 번만 이루어지므로, **함수가 매우 많이 호출되는 핫 경로**에서는 디스패치 비용은 무시할 수 있습니다. 다만 디스패치 결과(함수 포인터)가 **간접 호출**로 이어지므로, 인라인은 되지 않고 호출 비용은 남습니다. 그래서 멀티버저닝된 함수 자체가 작고 루프 안에서 반복 호출되면, 그 호출 비용이 누적될 수 있습니다.
- **사용 시점**: 대량의 수치 연산·SIMD로 이득이 큰 루프를 멀티버저닝하는 경우가 많습니다. 한 번 호출에 오래 걸리는 "무거운" 함수면 디스패치·간접 호출 비용은 상대적으로 작습니다. 가벼운 함수를 멀티버저닝하면, "버전 선택 + 간접 호출" 비용이 이득을 깎아먹을 수 있으므로, 벤치마크로 확인하는 것이 좋습니다.

## 공급 경로별 설계와 검증

- **설계**: "default", "avx2", "avx512" 등 **공급 경로(타겟)**별로 동일 시맨틱의 구현을 작성합니다. AVX2 버전에서는 4-wide float/double, AVX-512에서는 8-wide 등으로 루프를 구성합니다. 메모리 정렬·테일 처리(tail)를 각 타겟에 맞게 작성해야 합니다.
- **검증**: 각 타겟에서 실제로 해당 버전이 선택되는지(로깅 또는 CPUID 확인), 그리고 **정확성**이 기본 경로와 동일한지(같은 입력에 같은 출력) 단위 테스트로 확인합니다. 성능은 해당 CPU가 있는 머신에서 벤치마크해, default 대비 AVX2/AVX-512 버전이 기대만큼 빨라지는지 봅니다. 구형 CPU에서는 default만 타는지도 확인하면 안전합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **target_clones** | GCC에서 여러 CPU 타겟에 대해 각각 함수 버전을 생성하도록 지정하는 속성 |
| **CPUID** | CPU가 지원하는 기능(SSE, AVX2 등)을 런타임에 조회하는 명령; 디스패치 시 사용 |

## 판단 기준: 언제 멀티버저닝을 쓸지 / 피할지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 대량 수치·SIMD 이득 큰 루프 | 멀티버저닝으로 AVX2/AVX-512 경로 추가 | 가벼운 함수만 멀티버저닝 |
| 다양한 CPU에 배포 | default + AVX2 등으로 호환·성능 동시 확보 | 단일 최신 CPU만 가정 |
| 디스패치·간접 호출 비용 | 무거운 함수·적은 호출 빈도에 사용 | 핫 루프 내부 가벼운 함수 다중 버전 |

## 자주 하는 실수

- **가벼운 함수를 과하게 멀티버저닝**: 작은 함수를 AVX2/AVX-512 버전으로 나누면 디스패치·간접 호출 비용이 이득을 상쇄할 수 있다. 무거운 루프나 호출 빈도가 낮은 함수에 적용하고, 벤치로 이득이 나는지 확인한다.
- **구형 CPU에서 선택·정확성 미검증**: default 경로만 타는지, 해당 CPU에서 정확히 같은 결과가 나오는지 테스트하지 않으면 배포 후 크래시나 잘못된 결과가 나올 수 있다. 각 타겟에서 선택·정확성·성능을 검증한다.

## 학습 성과 목표

- **함수 멀티버저닝** 개념과 GCC/Clang **target** 속성 사용법을 설명할 수 있다.
- 디스패치 비용과 **언제 멀티버저닝이 이득인지**를 설명할 수 있다.
- 공급 경로별 구현·검증(선택·정확성·성능) 절차를 적용할 수 있다.

## 비판적 시각: 한계와 트레이드오프

멀티버저닝은 **SIMD 이득이 큰 무거운 경로**에만 가치가 있다. 가벼운 함수를 여러 버전으로 나누면 코드 복잡도와 유지보수 비용이 늘어나는 반면, 디스패치·간접 호출로 인한 손해가 이득을 넘을 수 있다. "AVX-512가 있으면 무조건 쓰자"가 아니라, 벤치마크로 해당 워크로드에서 실제로 빨라지는지 확인한 뒤 도입하는 것이 전문가다운 선택이다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 멀티버저닝 | CPU 기능별 구현을 런타임에 선택; 호환성·성능 동시 확보 |
| 비용 | 디스패치 1회·간접 호출; 무거운/적은 호출에 유리 |
| 검증 | 타겟별 선택·정확성·성능 벤치 확인 |

## 다음 장에서는

**컴파일러 내장 함수(intrinsics)** 카탈로그, SIMD·원자성 등 사용 시 주의와 대안을 다룹니다.

→ [컴파일러 내장 함수](/post/compiler-optimization/compiler-intrinsics-catalog/) (챕터 08)
