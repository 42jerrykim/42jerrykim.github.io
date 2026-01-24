---
draft: true
title: "[Compiler 02] Introduction: Low-latency 컴파일러·빌드 최적화"
slug: getting-started-compiler-build-performance-tuning
description: "Low-latency 컴파일러·빌드 최적화 트랙의 도입 챕터입니다. 옵션 설계와 LTO/PGO, 인라이닝/코드 생성 분석의 책임 범위를 정리하고, 동일 벤치마크로 설정 변경을 검증하는 방법을 안내합니다."
tags:
  - Performance
  - Performance Engineering
  - Performance Optimization
  - Low Latency
  - Low-latency
  - Microsecond
  - Latency
  - Throughput
  - Benchmark
  - Microbenchmark
  - Profiling
  - Flamegraph
  - Optimization
  - Systems Programming
  - C++
  - CPP
  - Compiler
  - Build
  - Toolchain
  - Clang
  - GCC
  - MSVC
  - CMake
  - LTO
  - PGO
  - Optimization Flags
  - -O3
  - Debug Symbols
  - Inlining
  - Codegen
  - Assembly
  - Linker
  - ABI
  - Binary Size
  - CPU
  - Cache
  - Memory
  - Concurrency
  - Regression
  - CI
  - 측정
  - 검증
  - 성능
  - 성능공학
  - 성능 최적화
  - 저지연
  - 마이크로초
  - 레이턴시
  - 처리량
  - 벤치마크
  - 마이크로벤치마크
  - 프로파일링
  - 최적화
  - 시스템 프로그래밍
  - 컴파일러
  - 빌드
  - 툴체인
  - 링커
  - 코드 생성
  - 인라이닝
  - 회귀
  - 자동화
  - CI
---

이 트랙은 "코드를 바꾸지 않고도 성능을 바꾸는 영역"을 책임집니다. µs 최적화에서는 인라이닝/벡터화/분기 형태 같은 코드 생성 결과가 수치에 직접 영향을 주기 때문에, 빌드와 컴파일러를 설계 대상으로 다룹니다.

## 이 트랙이 책임지는 범위

- 최적화 옵션 설계(릴리즈/디버그/프로파일링 빌드 전략)
- LTO/ThinLTO, PGO의 적용/검증
- 인라이닝 실패 원인 분석(가시성, ODR/ABI, 코드 크기)
- 코드 생성 형태 이해(어셈블리 레벨 확인, 함수 경계/호출 규약)

## 이 트랙이 다루지 않는 것 (경계)

- 알고리즘/데이터 구조 선택 자체 (→ 메모리/데이터 구조 트랙 또는 별도 설계)
- 락 경합/스레드 구조 같은 동시성 설계 (→ 동시성 트랙)
- CPU 마이크로아키텍처의 하드 원인 분석 (→ CPU 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | 최적화 플래그 | -O2/-O3/-Ofast 플래그별 동작과 trade-off |
| 02 | LTO/ThinLTO | Link-Time Optimization 실전 적용과 검증 |
| 03 | PGO 워크플로우 | Profile-Guided Optimization 고급 워크플로우 |
| 04 | 컴파일러 비교 | GCC vs Clang vs MSVC 최적화 차이점 |
| 05 | 인라이닝 분석 | 인라이닝 실패 진단 (가시성, ODR, ABI, 코드 크기) |
| 06 | 코드 생성 분석 | 어셈블리 레벨 코드 생성 분석 |
| 07 | 함수 멀티버저닝 | CPU 기능별 함수 다중 버전 생성 |
| 08 | 컴파일러 내장 함수 | 컴파일러 intrinsics 카탈로그 |
| 09 | Sanitizer 오버헤드 | AddressSanitizer/UBSan 등의 성능 영향 |
| 10 | 디버그 정보와 성능 | 디버그 심볼과 성능, 릴리즈 빌드 전략 |

## 측정과 검증 (이 트랙 기준)

- 컴파일 산출물 비교(인라이닝 여부, 코드 크기, hot 함수 형태)
- PGO 전/후, LTO on/off 성능 비교(동일 벤치마크로 검증)
- 회귀 감지: 빌드 설정 변경이 성능에 미치는 영향 자동화

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: `Low-latency C++ Language Optimization` (Course 01), `Memory & Data Layout` (Course 03)
