---
collection_order: 8
date: 2026-03-11
lastmod: 2026-03-11
draft: true
title: "[Compiler 02] 컴파일러 intrinsics 카탈로그"
slug: compiler-intrinsics-catalog
description: "intrinsics의 역할, SIMD·atomic·비트 조작 등 카테고리별 예, GCC/Clang/MSVC·x86/ARM 차이, 인라인·ABI·이식성 주의를 다룹니다."
tags:
  - C++
  - Performance
  - Optimization
  - Compiler
  - CPU
  - Cache
  - Memory
  - Benchmark
  - Profiling
  - CI-CD
  - Testing
  - 성능
  - 최적화
  - 컴파일러
  - 프로파일링
  - 테스트
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Linux
  - Windows
  - OS
  - 운영체제
  - Concurrency
  - 동시성
  - Latency
  - Throughput
  - Backend
  - 백엔드
  - Embedded
  - 임베디드
  - Debugging
  - 디버깅
  - Documentation
  - 문서화
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Best-Practices
  - Git
  - Automation
  - 자동화
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Data-Structures
  - 자료구조
  - Time-Complexity
  - 시간복잡도
  - Complexity-Analysis
  - 복잡도분석
  - Edge-Cases
  - 엣지케이스
  - Pitfalls
  - 함정
  - Error-Handling
  - 에러처리
  - Guide
  - 가이드
  - Reference
  - 참고
  - Technology
  - 기술
  - Tutorial
  - 튜토리얼
  - Advanced
  - Deep-Dive
  - 실습
  - Case-Study
  - Assembly
---

intrinsics는 특정 명령·시맨틱을 컴파일러에 요청하는 API입니다. 이 챕터에서는 카테고리별 예와 플랫폼 차이를 다룹니다.

## intrinsics의 역할

**Intrinsics(내장 함수)**는 C/C++ 함수처럼 호출하지만, 컴파일러가 **특정 CPU 명령 한 개 또는 짧은 시퀀스**로 치환하는 API입니다. 일반 C 코드만으로는 컴파일러가 원하는 SIMD 명령이나 atomic 연산을 내지 못할 때, 프로그래머가 "이 연산은 이 명령으로 만들어라"라고 지시하는 데 씁니다. 인라인되어 호출 오버헤드가 없고, 레지스터 할당·스케줄링은 컴파일러가 하므로, 손으로 어셈블리만 쓰는 것보다 이식성과 유지보수성이 좋습니다.

## 카테고리별 예

- **SIMD**: x86의 SSE/AVX 계열에서는 `_mm_add_ps`, `_mm256_mul_pd`, `_mm512_loadu_ps` 등 벡터 연산·로드/스토어 intrinsics가 있습니다. ARM NEON에서는 `vaddq_f32` 등 비슷한 형태입니다. 벡터화를 "강제"하거나, auto-vectorization이 실패하는 루프를 수동으로 벡터화할 때 사용합니다.
- **Atomic**: `__atomic_load`, `__atomic_store`, `__atomic_compare_exchange` 등은 lock-free 자료 구조나 동기화 프리미티브 구현에 씁니다. 컴파일러가 해당 플랫폼의 atomic 명령(예: x86의 lock 접두사)으로 매핑합니다.
- **비트/바이트**: `__builtin_popcount`, `__builtin_clz`, `__builtin_bswap32` 등은 비트 개수, leading zero, 바이트 스왑 등을 한 번에 처리합니다. 플랫폼에 해당 명령이 있으면 한 instruction으로 내려갑니다.
- **기타**: 메모리 장벽(`__atomic_thread_fence`), CPUID(`__cpuid`), 특수 레지스터 접근 등도 플랫폼별 intrinsics로 제공되는 경우가 있습니다.

각 카테고리마다 수십~수백 개의 intrinsic이 있으므로, 공식 레퍼런스(Intel Intrinsics Guide, ARM, 컴파일러 매뉴얼)를 참고해 필요한 것만 골라 쓰는 것이 좋습니다.

## 컴파일러·플랫폼별 차이

- **GCC / Clang**: 대부분 동일한 intrinsic 이름을 공유합니다(x86의 경우 Intel/AMD 문서와 맞춘 이름). 헤더는 `<xmmintrin.h>`, `<emmintrin.h>`, `<immintrin.h>`(AVX/AVX-512) 등 플랫폼별로 다릅니다.
- **MSVC**: 시맨틱은 비슷하지만 **이름·헤더**가 다를 수 있습니다. 예를 들어 `<intrin.h>`, `<immintrin.h>` 등에서 제공하며, 일부 intrinsic 이름이 GCC/Clang과 다릅니다. 이식성이 필요하면 `#ifdef _MSC_VER` 등으로 분기하거나, SIMD 래퍼 라이브러리(xsimd, highway 등)를 쓰는 방법이 있습니다.
- **ARM**: NEON/SVE intrinsic은 ARM 공식 문서와 컴파일러 매뉴얼을 봅니다. x86과 완전히 다른 세트이므로, 멀티 플랫폼 코드에서는 추상화 레이어를 두는 것이 현실적입니다.

## 사용 시 주의

- **인라인**: 대부분의 intrinsic은 인라인되어 한두 instruction으로 내려가지만, 컴파일러·플래그에 따라 인라인되지 않을 수 있습니다. 핫 경로에서는 어셈블리로 실제로 인라인되었는지 확인하는 것이 좋습니다.
- **ABI**: 일부 intrinsic이 넘기는 타입(예: `__m256`)은 레지스터나 스택 레이아웃과 직결됩니다. 다른 컴파일러·버전과 혼합 링크할 때 ABI 호환에 유의합니다.

## 실전 시나리오: intrinsic 선택 시

- **SIMD**: Intel Intrinsics Guide, ARM NEON 문서에서 필요한 연산(로드·연산·스토어)에 맞는 intrinsic을 찾는다. 컴파일러·플랫폼별 헤더(`<immintrin.h>` 등)와 이름 차이를 확인한다.
- **Atomic**: lock-free 큐·카운터 등에서는 `__atomic_*` 시리즈를 사용하고, 메모리 순서(memory_order)를 필요에 맞게 선택한다.
- **이식성**: x86과 ARM 등 여러 플랫폼을 지원할 때는 래퍼 라이브러리(xsimd, highway 등)로 추상화하거나, 플랫폼별 분기로 각각 구현한다.

## 한눈에 보기: 카테고리별 intrinsics

| 카테고리 | 예 | 용도 |
|----------|-----|------|
| SIMD | _mm_add_ps, _mm256_mul_pd | 벡터화 강제·수동 SIMD |
| Atomic | __atomic_load, __atomic_compare_exchange | lock-free·동기화 |
| 비트/바이트 | __builtin_popcount, __builtin_clz | 비트 개수·leading zero |
| 기타 | __atomic_thread_fence, __cpuid | 메모리 장벽·CPU 정보 |

## 판단 기준: 언제 intrinsics를 쓸지 / 대안

| 상황 | 권장 | 비권장 |
|------|------|--------|
| auto-vectorization 실패·세밀 제어 | 수동 SIMD intrinsics | 어셈블리 직접(이식성 낮음) |
| lock-free 구조 | __atomic_* | 인라인 어셈블리(ABI·이식성) |
| 이식성 필요 | 래퍼 라이브러리(xsimd 등) 또는 플랫폼 분기 | 단일 플랫폼 intrinsic만 사용 |

## 자주 하는 실수

- **플랫폼·컴파일러 차이 무시**: 같은 이름의 intrinsic이라도 MSVC와 GCC/Clang에서 헤더·ABI가 다를 수 있다. 여러 플랫폼을 지원할 때는 래퍼 라이브러리나 `#ifdef` 분기로 각각 맞추고, 지원하지 않는 CPU에서는 런타임 검사 후 대체 구현을 쓰는 것이 안전하다.
- **핫 경로에서 인라인 여부 미확인**: intrinsic은 대부분 인라인되지만, 컴파일러·플래그에 따라 호출로 남을 수 있다. 핫 루프에서는 어셈블리로 실제로 한두 instruction으로 내려가는지 확인한다.

## 학습 성과 목표

- **intrinsics**의 역할(SIMD·atomic·비트 등)과 카테고리별 예를 설명할 수 있다.
- 컴파일러·플랫폼별 헤더·이름 차이를 알고, 사용 시 인라인·ABI 주의를 적용할 수 있다.
- 필요 시 공식 레퍼런스(Intel Intrinsics Guide 등)에서 적절한 intrinsic을 골라 쓸 수 있다.

## 비판적 시각: 한계와 트레이드오프

intrinsics는 **플랫폼에 묶인 API**다. x86 전용 코드는 ARM에서 돌지 않고, 컴파일러·버전에 따라 인라인·ABI가 달라질 수 있다. "최고 성능"을 위해 intrinsic만 쓰다 보면 이식성과 유지보수가 나빠지므로, 멀티 플랫폼이 필요하면 래퍼 라이브러리(xsimd, highway 등)로 추상화하거나, 플랫폼별 경로를 명확히 나누는 설계가 필요하다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| intrinsics | 특정 CPU 명령으로 치환되는 API; SIMD·atomic·비트 등 |
| 주의 | 인라인·ABI; 플랫폼별 헤더·이름 차이 |
| 대안 | 래퍼 라이브러리로 이식성 확보 |

## 다음 장에서는

**Sanitizer**(ASan, UBSan, TSan 등)의 런타임 오버헤드와 디버그/CI vs 릴리즈 전략을 다룹니다.

→ [Sanitizer 오버헤드](/collection/optimization-02-compiler/09-sanitizer-overhead/) (챕터 09)
