---
collection_order: 10
date: 2026-03-11
lastmod: 2026-03-11
draft: true
title: "[Compiler 02] 디버그 정보와 릴리즈 성능"
slug: debug-info-and-release-performance
description: "디버그 심볼이 코드 생성에 미치는 영향, 릴리즈에서 심볼 유지 전략, strip·FDO·LTO와 디버그 정보 조합 시 주의를 다룹니다."
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

디버그 심볼은 크래시 덤프·프로파일링에 필요하지만, 빌드 설정에 따라 코드 생성이나 크기에 영향을 줄 수 있습니다. 이 챕터에서는 그 경계를 다룹니다.

## 디버그 심볼이 코드 생성에 미치는 영향

일반적으로 **디버그 정보만 추가**하는 옵션(`-g`, `-g3` 등)은 **생성되는 기계어(코드 생성)**를 바꾸지 않습니다. 컴파일러는 소스 라인·변수·타입 정보를 별도 섹션(.debug_*, DWARF 등)에 넣을 뿐, 최적화된 코드는 -g 없이 빌드한 것과 동일하게 나옵니다. 따라서 **릴리즈 최적화(-O2/-O3)와 -g를 함께** 써도 실행 성능은 동일하다고 보면 됩니다.

예외적으로 **빌드/링크 설정**이 잘못되면 성능에 영향을 줄 수 있습니다. 예를 들어 -g를 켰을 때만 특정 최적화가 비활성화되는 레거시 빌드 스크립트가 있거나, 디버그 정보 생성 과정에서 부수적으로 다른 플래그가 바뀌는 경우입니다. **Split DWARF**(-gsplit-dwarf)는 디버그 정보를 별도 .dwo 파일로 빼서 링크 시간과 실행 파일 크기를 줄이는 데 쓰이며, 코드 생성 자체는 바꾸지 않습니다.

## 릴리즈 빌드에서 심볼 유지 전략

프로덕션에서 **크래시 덤프**를 분석하거나 **샘플링 프로파일러**(perf, VTune 등)로 심볼이 있는 스택을 보고 싶다면, 릴리즈 빌드에서도 **디버그 심볼을 포함**한 바이너리를 만든 뒤, 필요에 따라 **strip**으로 분리하는 방식을 씁니다.

- **RelWithDebInfo**: 최적화(-O2) + 디버그 정보(-g)로 빌드합니다. 실행 파일이 커지지만, 크래시 시 addr2line·gdb로 소스 위치를 볼 수 있고, perf report에서 함수명이 보입니다.
- **심볼만 별도 보관**: strip하지 않은 바이너리를 보관해 두거나, **debug symbol 패키지**를 따로 배포합니다. 배포용 바이너리는 strip해 크기를 줄이고, 크래시 덤프는 심볼이 있는 환경에서 열어 분석합니다.

이렇게 하면 **실행 성능은 최적화된 그대로** 유지하면서, 사후 분석만을 위해 심볼을 활용할 수 있습니다.

## strip / 비strip, FDO·LTO와 디버그 정보

- **strip**: `strip` 명령으로 실행 파일에서 디버그 섹션을 제거하면 **파일 크기**가 줄어듭니다. 실행 코드는 그대로이므로 성능 차이는 없고, 단지 심볼이 없어져 크래시 분석이 어려워질 뿐입니다.
- **FDO(Feedback-Directed Optimization) / PGO**: 프로파일 수집 시에는 보통 -g를 켜서 프로파일러가 소스/라인과 매핑할 수 있게 합니다. 최종 PGO 최적화 빌드에서 -g를 유지해도 생성 코드는 동일하고, 심볼만 추가로 들어갑니다.
- **LTO**: LTO 빌드에서 -g를 쓰면 링크 시점에 디버그 정보가 합쳐집니다. 일부 툴체인에서는 LTO + 디버그 정보 조합이 링크 시간을 늘리거나 디버그 품질에 영향을 줄 수 있으므로, 사용하는 컴파일러·버전 문서를 확인하는 것이 좋습니다. 성능 자체는 LTO가 주는 이득을 그대로 받습니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **RelWithDebInfo** | Release with Debug Info; -O2 수준 최적화 + 디버그 심볼(-g). 크래시 분석·perf에 유리 |
| **Split DWARF** | -gsplit-dwarf; 디버그 정보를 별도 .dwo 파일로 분리해 링크 시간·실행 파일 크기 절감 |

## 판단 기준: 디버그 정보와 빌드 타입

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 릴리즈 + 크래시 분석 | -O2 -g(RelWithDebInfo) 또는 심볼 별도 보관 | 릴리즈에서 -g 생략 후 분석 불가 |
| 성능 측정 | -g 유지해도 코드 생성 동일 | -g가 성능을 낮춘다고 오해 |
| 배포 크기 | strip으로 심볼 제거·별도 패키지 | 심볼 포함 배포(보안·크기) |

## 자주 하는 실수

- **strip/심볼 분리 시 주의**: 배포용으로 strip한 바이너리만 남기고 심볼이 있는 복사본을 버리면, 나중에 크래시 덤프를 받아도 소스 위치를 알 수 없다. RelWithDebInfo 빌드나 심볼 패키지는 별도 보관해 두고, 배포용만 strip한다.
- **-g가 성능을 낮춘다고 오해**: 디버그 정보만 추가하는 -g는 코드 생성에 영향을 주지 않는다. 릴리즈 최적화(-O2/-O3)와 -g를 함께 써도 실행 성능은 동일하다. 성능 측정 시 -g를 빼야 한다고 잘못 알고 있지 않도록 한다.

## 학습 성과 목표

- 디버그 정보(**-g**)가 **코드 생성**을 바꾸지 않음을 설명할 수 있다.
- 릴리즈 빌드에서 심볼 유지(RelWithDebInfo·strip 분리) 전략을 적용할 수 있다.
- strip·FDO·LTO와 디버그 정보의 관계를 설명할 수 있다.

## 비판적 시각: 한계와 트레이드오프

디버그 정보는 **분석 편의**를 위한 것이지, 성능을 바꾸지 않는다. 다만 빌드 스크립트가 -g와 다른 플래그를 엮어 두어서, -g를 켰을 때만 최적화가 달라지는 레거시 환경이 있을 수 있다. 그런 경우에는 스크립트를 정리해 "디버그 정보 = 별도 섹션만"이 되도록 하고, 성능에 영향을 주는 요인과 분리하는 것이 좋다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| -g와 성능 | 디버그 정보만 추가 시 생성 기계어 동일; 성능 영향 없음 |
| 릴리즈 전략 | RelWithDebInfo 또는 심볼 별도 보관 후 strip |
| LTO+PGO | -g 유지해도 성능 이득 유지; 툴체인별 링크·품질 확인 |

## 다음 장에서는

**C++20 Modules**가 빌드 시간과 런타임에 미치는 영향, 도입 단계별 전략을 다룹니다.

→ [C++20 Modules](/collection/optimization-02-compiler/11-cpp20-modules/) (챕터 11)
