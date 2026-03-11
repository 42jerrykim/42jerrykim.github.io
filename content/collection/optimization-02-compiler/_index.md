---
collection_order: 12
draft: true
title: "[Optimization(Compiler)] 02. Low-latency 컴파일러·빌드 최적화 트랙"
slug: compiler-optimization
description: "같은 C++ 코드도 빌드 설정과 컴파일러 최적화에 따라 성능이 달라집니다. 이 트랙에서는 최적화 옵션 설계, LTO/PGO 적용·검증, 인라이닝 실패 원인과 코드 생성 형태를 다루며, 알고리즘·동시성 설계는 경계 밖에 둡니다."
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
  - Deployment
  - 배포
  - Workflow
  - 워크플로우
  - Configuration
  - 설정
  - Troubleshooting
  - 트러블슈팅
  - Comparison
  - 비교
---

이 트랙은 **"코드를 바꾸지 않고도 성능을 바꾸는 영역"**을 책임집니다. µs 단위 최적화에서는 인라이닝·벡터화·분기 형태 같은 코드 생성 결과가 수치에 직접 영향을 주기 때문에, 빌드와 컴파일러를 설계 대상으로 다룹니다.

## 이 트랙의 학습 목표

이 트랙을 마친 후 독자는 다음을 할 수 있어야 합니다.

- **최적화 플래그**(-O0~-Ofast, /O1·/O2·/Ox)의 의미와 trade-off를 설명하고, 릴리즈/디버그/프로파일 빌드 전략을 설계할 수 있다.
- **LTO·ThinLTO**를 활성화하고, LTO on/off 성능·크기 차이를 동일 벤치마크로 검증할 수 있다.
- **PGO** 3단계 워크플로우를 적용하고, 프로파일 대표성과 회귀 검증을 고려할 수 있다.
- **GCC·Clang·MSVC**의 최적화 차이를 영역별(벡터화·인라이닝·루프)로 비교하고, 플랫폼별 선택 근거를 말할 수 있다.
- **인라이닝 실패** 원인(가시성, ODR/ABI, 코드 크기)을 진단하고, 인라이닝 리포트와 Course 01(인라이닝 유도)을 연계할 수 있다.
- **어셈블리 레벨**에서 코드 생성 형태(함수 경계·호출 규약)를 확인하고, hot 함수 형태를 해석할 수 있다.
- **함수 멀티버저닝·컴파일러 내장 함수**를 상황에 맞게 선택하고, Sanitizer 오버헤드와 디버그 정보 전략을 설명할 수 있다.
- **C++20 Modules**와 **빌드 병렬화**(ccache, distcc, sccache)로 빌드 시간을 다루고, **정적 분석** 경고를 성능 회귀와 연계할 수 있다.

## 이 트랙이 책임지는 범위

- 최적화 옵션 설계(릴리즈/디버그/프로파일링 빌드 전략)
- LTO/ThinLTO, PGO의 적용·검증
- 인라이닝 실패 원인 분석(가시성, ODR/ABI, 코드 크기)
- 코드 생성 형태 이해(어셈블리 레벨 확인, 함수 경계/호출 규약)

## 이 트랙이 다루지 않는 것 (경계)

- 알고리즘/데이터 구조 선택 자체 (→ 메모리/데이터 구조 트랙 또는 별도 설계)
- 락 경합/스레드 구조 같은 동시성 설계 (→ 동시성 트랙)
- CPU 마이크로아키텍처의 하드 원인 분석 (→ CPU 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 00 | Introduction | 트랙 범위·측정 기준·선수/병행 트랙 |
| 01 | 최적화 플래그 | -O2/-O3/-Ofast 플래그별 동작과 trade-off |
| 02 | LTO/ThinLTO | Link-Time Optimization 실전 적용과 검증 |
| 03 | PGO 워크플로우 | Profile-Guided Optimization 고급 워크플로우 |
| 04 | 컴파일러 비교 | GCC vs Clang vs MSVC 최적화 차이점 |
| 05 | 인라이닝 진단 | 컴파일러 관점 인라이닝 실패 진단 (가시성, ODR, ABI, 코드 크기) |
| 06 | 코드 생성 분석 | 어셈블리 레벨 코드 생성 분석 |
| 07 | 함수 멀티버저닝 | CPU 기능별 함수 다중 버전 생성 |
| 08 | 컴파일러 내장 함수 | 컴파일러 intrinsics 카탈로그 |
| 09 | Sanitizer 오버헤드 | AddressSanitizer/UBSan 등의 성능 영향 |
| 10 | 디버그 정보와 성능 | 디버그 심볼과 성능, 릴리즈 빌드 전략 |
| 11 | C++20 Modules | Modules 빌드 시간과 런타임 성능 영향 |
| 12 | 빌드 병렬화 전략 | ccache, distcc, sccache 활용과 빌드 시간 최적화 |
| 13 | Static Analyzer | 성능 관련 정적 분석 경고와 활용 |

## 트랙 구성 원칙

- **코드 변경 없이 빌드·컴파일러만으로 얻는 이득**에만 초점을 둡니다. 알고리즘·자료 구조·동시성 설계는 다른 트랙에서 다룹니다.
- **측정 기반**: 모든 권장사항은 "동일 벤치마크로 비교한 결과"를 전제로 하며, 환경·워크로드에 따라 결과가 달라질 수 있음을 명시합니다.
- **실무 적용**: 각 챕터에서 "언제 쓸지/피할지" 판단 기준과 적용 체크리스트를 제시해, 독자가 상황에 맞게 선택할 수 있도록 합니다.

## 측정과 검증 (이 트랙 기준)

- 컴파일 산출물 비교(인라이닝 여부, 코드 크기, hot 함수 형태)
- PGO 전/후, LTO on/off 성능 비교(동일 벤치마크로 검증)
- 회귀 감지: 빌드 설정 변경이 성능에 미치는 영향 자동화

## 추천 선행/병행 트랙

- **선행**: Low-latency Profiling & Performance Analysis (Course 05)
- **병행**: Low-latency C++ Language Optimization (Course 01), Memory & Data Layout (Course 03)

## 평가 기준 (이 트랙을 마친 후)

- 최적화 레벨과 LTO/PGO를 상황에 맞게 선택하고, 그 근거를 설명할 수 있는가?
- 인라이닝 실패 원인을 리포트와 어셈블리로 진단할 수 있는가?
- 동일 벤치마크로 빌드 설정 변경 전후 성능을 측정·비교할 수 있는가?
- 컴파일러·빌드 도구 선택 시 trade-off(속도·크기·빌드 시간·회귀 위험)를 고려할 수 있는가?

## 핵심 메시지

같은 소스 코드라도 **최적화 플래그·LTO·PGO·컴파일러 선택**에 따라 생성되는 기계어와 성능이 달라집니다. 이 트랙은 그 선택을 **측정 가능하게** 하고, **언제 무엇을 쓸지** 판단할 수 있도록 구성되어 있습니다. 챕터 00부터 순서대로 읽으면 트랙 범위·측정 기준·커리큘럼을 한눈에 파악할 수 있습니다.

## 읽는 순서와 각 챕터 역할

00(Introduction)에서 트랙 범위·측정 기준·학습 목표를 파악한 뒤, 01(최적화 플래그)부터 순서대로 진행하는 것을 권장합니다. 01·02·03은 빌드 설정의 기초(플래그·LTO·PGO)를 다루고, 04(컴파일러 비교) 이후에는 인라이닝 진단·코드 생성·멀티버저닝·내장 함수·Sanitizer·디버그 정보·Modules·빌드 병렬화·정적 분석으로 이어집니다. 각 챕터 말미의 "다음 장에서는" 링크로 선후 관계를 따라가면 됩니다.

## 게시 전 확인 (체크리스트)

- 트랙 학습 목표와 커리큘럼이 명확히 드러나는가?
- 측정·검증이 "동일 벤치마크" 전제임이 강조되어 있는가?
- 평가 기준(이 트랙을 마친 후 달성할 것)이 구체적으로 나열되어 있는가?
- 다음 단계(챕터 00 링크)가 있는가?

## 다음 단계

→ [Introduction: Low-latency 컴파일러·빌드 최적화](/collection/optimization-02-compiler/00-introduction/) (챕터 00)에서 트랙 범위와 측정 기준을 자세히 다룹니다.
