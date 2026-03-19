---
collection_order: 9
date: 2026-03-11
lastmod: 2026-03-11
draft: true
title: "[Compiler 02] Sanitizer 성능 오버헤드"
slug: sanitizer-overhead-performance
description: "AddressSanitizer, UBSan, TSan 등 동작 개요와 런타임 오버헤드, 디버그/CI vs 릴리즈 전략, 성능 측정 시 비활성화 필요성을 다룹니다."
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

Sanitizer는 메모리·미정의 동작·데드락 검사에 유용하지만 런타임 비용이 큽니다. 이 챕터에서는 오버헤드와 사용 전략을 다룹니다.

## Sanitizer 종류와 동작 개요

- **AddressSanitizer(ASan)**: 힙 버퍼 오버플로우, use-after-free, 이중 해제 등을 검사합니다. 할당 시 주변에 "빨간 구역(redzone)"을 두고, 접근 시 해당 영역이 유효한지 검사합니다. 메모리 접근마다 체크가 들어가고, 할당 구조가 바뀌어 **메모리 사용량**이 크게 늘어납니다(보통 2~3배). **속도**도 2~5배 정도 느려지는 경우가 많습니다.
- **UndefinedBehaviorSanitizer(UBSan)**: 정수 오버플로우, null 역참조, 잘못된 캐스트 등 **미정의 동작**이 일어나는 순간을 잡습니다. 해당 연산이 실행될 때만 검사가 들어가므로, ASan보다는 오버헤드가 적지만, 핫 경로에 해당 연산이 많으면 눈에 띄게 느려질 수 있습니다.
- **ThreadSanitizer(TSan)**: 데이터 레이스(두 스레드가 동시에 같은 메모리를 접근하고 그중 하나는 쓸 때)를 검사합니다. 메모리 접근과 동기화 이벤트를 기록하므로 **메모리·속도** 모두 상당한 오버헤드가 듭니다(수 배 느려지고 메모리도 많이 씀).
- **MemorySanitizer(MSan)**: 초기화되지 않은 메모리 읽기를 찾습니다. 미초기화 비트맵을 유지해야 해서 오버헤드가 큽니다.

이들 도구는 **디버깅·CI**에서 버그를 찾는 데 매우 유용하지만, **릴리즈 빌드**나 **성능 측정용 빌드**에는 사용하지 않는 것이 원칙입니다.

## 역사·배경

**AddressSanitizer(ASan)**는 2010년대 초 Google에서 개발되어 LLVM/Clang에 통합되었고, **UndefinedBehaviorSanitizer(UBSan)**·**ThreadSanitizer(TSan)**도 LLVM 생태계에서 표준화되었습니다. GCC도 비슷한 Sanitizer 옵션을 제공합니다. 이들은 메모리 오류·미정의 동작·데이터 레이스를 빌드 시 계측으로 잡아 주지만, 런타임 오버헤드가 크기 때문에 프로덕션에서는 사용하지 않고 디버그·CI에 한정해 사용합니다.

## 런타임 오버헤드 정량

- **ASan**: 벤치마크에 따라 다르지만, 전형적으로 **2~3배 메모리**, **1.5~3배 실행 시간** 증가가 보고됩니다. I/O 위주 워크로드에서는 상대적으로 덜 느려질 수 있고, 메모리 접근이 많은 수치 코드에서는 크게 느려집니다.
- **UBSan**: 검사되는 연산이 적으면 1.1배 미만으로 끝나지만, 정수 연산·캐스트가 많은 경로에서는 1.5배 이상 나올 수 있습니다.
- **TSan**: 멀티스레드 벤치마크에서 **5~15배** 느려지고 메모리도 수 배 늘어나는 경우가 있습니다.

정확한 수치는 워크로드와 플랫폼에 따라 다르므로, 자신의 핵심 경로에서 Sanitizer on/off를 켜고 끄며 한 번 측정해 두면 기준이 됩니다.

## 디버그/CI vs 릴리즈 전략

- **디버그 빌드·로컬 테스트**: ASan, UBSan을 켜서 메모리 오류·미정의 동작을 조기에 잡습니다. TSan은 동시성 버그가 의심될 때 사용합니다.
- **CI**: PR마다 또는 매일 ASan/UBSan(및 필요 시 TSan) 빌드를 돌려, 릴리즈 빌드에서는 드러나지 않는 버그를 자동으로 걸러냅니다. CI 시간이 길어지므로, 빠른 체크용 빌드와 Sanitizer 빌드를 단계로 나누는 경우가 많습니다.
- **릴리즈**: Sanitizer는 **끕니다**. 오버헤드와 호환성(일부 환경에서 Sanitizer 라이브러리 미지원) 때문에 프로덕션에서는 사용하지 않습니다.

## 성능 측정 시 Sanitizer 비활성화

**성능 벤치마크·프로파일링**을 할 때는 반드시 **Sanitizer가 꺼진** 빌드로 측정해야 합니다. 그렇지 않으면 측정 결과가 실제 릴리즈 성능을 전혀 반영하지 못합니다. 빌드 스크립트에서 "benchmark" 또는 "release" 설정은 Sanitizer 플래그를 넣지 않도록 하고, 실수로 Sanitizer가 켜진 상태로 벤치마크한 결과를 릴리즈 판단에 쓰지 않도록 합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **redzone** | ASan이 할당 주변에 두는 "빨간 구역"; 접근 시 유효성 검사에 사용 |
| **instrumented 빌드** | Sanitizer 계측이 삽입된 빌드; 실행 시 검사·기록으로 오버헤드 발생 |

## 판단 기준: 언제 Sanitizer를 쓸지 / 피할지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 디버그·로컬 테스트 | ASan, UBSan(필요 시 TSan) | 릴리즈 빌드에 Sanitizer |
| CI | ASan/UBSan(및 TSan) 별도 타겟 | 성능 측정용 빌드에 Sanitizer |
| 릴리즈·벤치마크 | Sanitizer 끔 | Sanitizer 켠 상태로 성능 판단 |

## 자주 하는 실수

- **Sanitizer 켠 채로 벤치마크**: 성능 숫자는 Sanitizer가 꺼진 빌드에서만 의미 있다. 실수로 ASan/UBSan/TSan이 켜진 상태로 측정한 결과를 "릴리즈 성능"으로 보고하면 안 된다. 벤치 타겟에서는 Sanitizer 플래그를 넣지 않도록 빌드 스크립트를 분리한다.
- **릴리즈 빌드에 Sanitizer 포함**: 프로덕션 바이너리에 Sanitizer를 켜면 오버헤드(2~수 배 느려짐, 메모리 증가)와 호환성 문제(일부 환경 미지원)가 생긴다. 디버그·CI 전용으로만 사용한다.

## 학습 성과 목표

- **ASan·UBSan·TSan** 등 Sanitizer의 오버헤드(메모리·속도)를 설명할 수 있다.
- 디버그/CI에서는 Sanitizer를 켜고, 릴리즈·성능 측정에서는 끄는 전략을 적용할 수 있다.
- 성능 벤치마크 시 Sanitizer 비활성화가 필수임을 설명할 수 있다.

## 비판적 시각: 한계와 트레이드오프

Sanitizer는 **버그 찾기용 도구**이지, 성능 개선 도구가 아니다. 오버헤드가 크기 때문에 프로덕션에서는 쓰지 않고, 디버그·CI에서만 제한적으로 사용한다. "ASan을 켜두면 안전하다"는 식으로 릴리즈에 포함하면 안 되며, 성능 측정 시에는 반드시 Sanitizer를 끈 빌드로만 숫자를 본다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 오버헤드 | ASan 2~3배 메모리·1.5~3배 시간; TSan 수 배~수십 배 |
| 사용 | 디버그·CI에서 버그 검사; 릴리즈에서는 미사용 |
| 벤치마크 | Sanitizer 끈 빌드로만 측정 |

## 다음 장에서는

**디버그 정보와 성능**의 관계, 릴리즈 빌드에서 심볼 유지 전략을 다룹니다.

→ [디버그 정보와 성능](/collection/optimization-02-compiler/10-debug-info-and-performance/) (챕터 10)
