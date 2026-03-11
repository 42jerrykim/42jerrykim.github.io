---
collection_order: 11
date: 2026-03-11
lastmod: 2026-03-11
draft: true
title: "[Compiler 02] C++20 Modules와 빌드·성능"
slug: cpp20-modules-build-performance
description: "C++20 Modules가 빌드 시간에 미치는 영향(헤더 반복 파싱 감소), 런타임 성능과의 관계(인라인·코드 생성), 점진적 모듈화와 기존 헤더 혼용 전략을 다룹니다. 컴파일러·버전별 모듈 지원과 도입 시 판단 기준을 제시합니다."
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

C++20 Modules는 헤더 대신 모듈 단위로 컴파일해 빌드 시간과 의존성을 바꿉니다. 이 챕터에서는 빌드·런타임 영향과 도입 전략을 다룹니다.

## 역사·배경

C++20에서 **Modules**가 표준에 도입되었습니다. 표준 문서에서는 모듈의 목적을 다음과 같이 밝힙니다.

> "Modules provide a way to partition the program into logical parts that have well-defined interfaces. A module interface is compiled once and the result is reused by every translation unit that imports that interface." — ISO/IEC 14882 (C++20), [cppreference — Modules](https://en.cppreference.com/w/cpp/language/modules) 기존 `#include`는 헤더를 반복 파싱하게 해 대형 프로젝트에서 컴파일 시간이 급증하는 문제가 있어, "한 번만 컴파일한 인터페이스"를 재사용하는 모듈 모델이 제안·채택되었습니다. MSVC가 초기 실험적 지원을 했고, GCC·Clang도 C++20 모듈 지원을 단계적으로 추가했습니다. 빌드 시스템(CMake 등)과 IDE 지원은 아직 프로젝트마다 다르므로, 도입 시 툴체인·버전을 확인하는 것이 좋습니다.

## Modules가 빌드 시간에 미치는 영향

전통적인 **헤더** 방식에서는 `#include`될 때마다 헤더 전체가 다시 파싱됩니다. 큰 헤더나 헤더가 깊게 중첩되면, 여러 TU에서 같은 헤더를 반복 파싱하게 되어 **컴파일 시간**이 크게 늘어납니다.

**C++20 Modules**에서는 모듈 단위로 **한 번만** 컴파일한 결과(BMI, Compiled Module Interface)를 재사용합니다. 모듈을 import하는 쪽에서는 "이미 컴파일된 인터페이스"만 읽으므로, 헤더를 매번 파싱하는 것보다 **빌드 시간**이 줄어드는 경우가 많습니다. 특히 대형 프로젝트에서 헤더 의존성이 많을수록 모듈 전환 시 컴파일 시간 감소 효과가 두드러질 수 있습니다. 다만 모듈 자체의 빌드 순서·캐시 전략이 제대로 설정되어야 하고, 아직 도구 지원(CMake, IDE 등)이 프로젝트마다 다르므로 실제 수치는 환경에 따라 달라집니다.

## 런타임 성능 영향

Modules는 **빌드 모델**을 바꾸는 것이지, 언어 시맨틱을 바꾸는 것이 아닙니다. 같은 코드를 헤더로 쓰든 모듈로 쓰든 **최종적으로 생성되는 기계어**는 이론적으로 동일하게 나올 수 있습니다. 따라서 **인라인·코드 생성** 관점에서 "모듈이면 더 빠르다"와 같은 보장은 없습니다. 다만 빌드가 빨라지면 **PGO·LTO** 같은 무거운 최적화를 더 자주 돌리기 쉬워지고, 의존 경계가 명확해져 컴파일러가 최적화할 때 유리한 구조를 만들 여지는 있습니다. 런타임 성능 자체는 기존처럼 최적화 플래그·코드 구조·LTO/PGO에 의해 결정된다고 보면 됩니다.

## 도입 단계별 전략

- **점진적 모듈화**: 한 번에 전체를 모듈로 바꾸지 않고, **새로 추가하는 코드**나 **자주 바뀌는 라이브러리**부터 모듈로 만듭니다. 기존 헤더는 그대로 두고, 모듈과 헤더가 혼재하는 상태를 허용하면서 점차 모듈 비중을 늘립니다.
- **기존 코드와 혼용**: C++20에서는 `import`와 `#include`를 같은 TU에서 쓸 수 있습니다. 헤더 전용 서드 파티는 그대로 두고, 자체 코드만 모듈로 옮기는 방식이 현실적입니다. 빌드 시스템에서 모듈 단위 컴파일·BMI 캐시가 지원되는지 확인한 뒤 도입하는 것이 좋습니다.
- **컴파일러·버전**: MSVC, GCC, Clang 모두 C++20 모듈 지원이 진행 중이지만, 버전과 플랫폼에 따라 완성도가 다릅니다. 도입 시 사용할 툴체인의 모듈 지원 상태를 확인하고, 필요하면 실험적 빌드로 먼저 검증합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **BMI** | Compiled Module Interface; 모듈을 한 번 컴파일한 결과. import 시 재사용됨 |
| **점진적 모듈화** | 한 번에 전부가 아니라 새 코드·자주 바뀌는 부분부터 모듈로 전환하는 전략 |

## 판단 기준: 언제 Modules를 도입할지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 대형 프로젝트·컴파일 시간 | 점진적 모듈화·새 코드부터 | 한 번에 전면 전환 |
| 도구 지원 | CMake·컴파일러 버전 확인 후 | 미지원 환경에서 강행 |
| 런타임 성능 | 기대 시 LTO/PGO·코드 구조에 의존 | "모듈 = 더 빠름" 가정 |

## 자주 하는 실수

- **한 번에 전면 모듈 전환**: 대형 프로젝트를 한꺼번에 모듈로 바꾸면 빌드 순서·BMI 캐시·헤더와의 혼용에서 깨지기 쉽다. 점진적으로 새 코드·자주 바뀌는 부분부터 모듈로 옮기고, 빌드 시스템과 도구 지원을 확인한 뒤 범위를 넓힌다.
- **도구·버전 미확인**: CMake·컴파일러 버전에 따라 C++20 모듈 지원이 다르다. 도입 전에 사용할 툴체인의 모듈 지원 상태를 확인하고, 실험적 빌드로 검증한 뒤 본격 도입한다.

## Modules 전환 시 주의

기존 헤더 기반 코드를 모듈로 바꿀 때 다음을 지키면 빌드 깨짐과 디버깅 부담을 줄일 수 있다.

- **빌드 순서·BMI 캐시**: 모듈 인터페이스는 그것을 import하는 TU보다 먼저 컴파일되어야 한다. 빌드 시스템이 의존 순서를 올바르게 잡고, BMI(Compiled Module Interface)가 캐시되는지 확인한다. 순서가 꼬이면 "모듈을 찾을 수 없음" 같은 오류가 난다.
- **헤더와 혼용 시**: 같은 TU에서 `import`와 `#include`를 섞을 때, 전처리기와 모듈 로딩 순서가 툴체인마다 다를 수 있다. 헤더 전용 서드 파티는 그대로 두고, 자체 코드만 모듈로 옮기며 점진적으로 전환한다.
- **CI·캐시**: BMI와 오브젝트 캐시 키에 모듈 소스 해시·컴파일러 버전을 넣어, 모듈 인터페이스가 바뀌면 재컴파일이 되도록 한다. 캐시 키가 너무 넓으면 잘못된 BMI가 재사용될 수 있다.

## 학습 성과 목표

- **C++20 Modules**가 빌드 시간에 미치는 영향(헤더 반복 파싱 감소)을 설명할 수 있다.
- 런타임 성능은 모듈 자체보다 최적화 플래그·구조에 의함을 설명할 수 있다.
- 점진적 모듈화·기존 헤더와 혼용 전략을 적용할 수 있다.

## 비판적 시각: 한계와 트레이드오프

Modules는 **빌드 모델**을 바꾸는 것이지, 런타임 성능을 보장하는 마법이 아니다. "모듈로 옮기면 더 빨라진다"는 보장이 없고, 실제 성능은 여전히 최적화 플래그·코드 구조·LTO/PGO에 의해 결정된다. 도구 지원도 프로젝트·플랫폼마다 다르므로, 도입 시 툴체인·버전을 확인하고 점진적으로 넓히는 것이 현실적이다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 빌드 시간 | 모듈 단위 재사용으로 컴파일 시간 감소 가능 |
| 런타임 | 생성 기계어는 동일할 수 있음; LTO/PGO와 연계 |
| 도입 | 점진적·도구 지원 확인 |

## 다음 장에서는

**빌드 병렬화**(ccache, sccache, distcc)와 CI 캐시·분산 전략을 다룹니다.

→ [빌드 병렬화 전략](/collection/optimization-02-compiler/12-build-parallelization/) (챕터 12)
