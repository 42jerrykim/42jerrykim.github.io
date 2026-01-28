---
draft: true
title: "[Performance 01] Introduction: Low-latency C++ 언어 최적화"
slug: getting-started-cpp-language-performance-tuning
description: "Low-latency C++ 언어 최적화 트랙의 도입 챕터입니다. 이 트랙이 책임지는 범위와 경계를 명확히 하고, microbenchmark 기반 측정·검증 루프로 추상화 비용을 줄이는 흐름을 정리합니다."
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
  - Modern C++
  - STL
  - Templates
  - constexpr
  - Virtual Function
  - Inlining
  - Copy Elision
  - Move Semantics
  - RAII
  - Object Lifetime
  - std::variant
  - std::optional
  - std::expected
  - std::span
  - Lambda
  - Closure
  - Small Buffer Optimization
  - SBO
  - Parameter Passing
  - Memory
  - Allocation
  - Allocator
  - pmr
  - Data Layout
  - Cache Locality
  - Compiler
  - Codegen
  - Assembly
  - CPU
  - Cache
  - Branch Prediction
  - Concurrency
  - Multithreading
  - Mutex
  - Atomic
  - Lock-free
  - False Sharing
  - Memory Model
  - Linux
  - Windows
  - OS
  - Runtime
  - Scheduling
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
  - 메모리
  - 할당
  - 데이터 레이아웃
  - 캐시 지역성
  - 동시성
  - 멀티스레드
  - 락
  - 원자 연산
  - 락프리
  - 메모리 모델
  - 운영체제
  - 런타임
  - 스케줄링
  - 성능 회귀
  - 유지보수
  - 시스템 설계
  - 의사결정
  - 타입 안전
  - 옵셔널
  - 뷰 패턴
  - 람다
  - 클로저
  - 소형 버퍼 최적화
  - 매개변수 전달
---

이 트랙은 "C++를 더 잘 쓰면 해결되는 성능"에 집중합니다. µs 단위에서는 작은 추상화/할당/복사 비용이 누적되어 핫패스를 지배하므로, 언어 레벨 비용을 수치로 확인하고 제거하는 능력이 핵심입니다.

## 이 트랙이 책임지는 범위

- 언어 추상화 비용(가상화, RTTI, 예외, 캡슐화 경계)
- STL/표준 라이브러리 사용 비용(컨테이너, 알고리즘, string)
- 객체 수명/복사/이동 비용, 임시 객체 제거
- 메모리 할당/해제 비용과 회피(가능한 범위)
- 템플릿/constexpr 기반의 비용 제어와 인라이닝 유도(언어 관점)

## 이 트랙이 다루지 않는 것 (경계)

- CPU 파이프라인/분기 예측/캐시 미스 "원인"의 하드 분석 (→ CPU 트랙)
- OS 스케줄링, CPU pinning, syscall 비용 (→ OS/런타임 트랙)
- 락 경합/메모리 모델/false sharing 같은 동시성 구조 (→ 동시성 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | 추상화 비용 분석 | 가상 함수/RTTI/예외 처리의 정량적 비용, devirtualization |
| 02 | STL 컨테이너 비용 | vector/map/unordered_map 비용 모델, 캐시 효율성 |
| 03 | 문자열 최적화 | SSO, string_view, 문자열 처리 최적화 기법 |
| 04 | 객체 수명 최적화 | Copy Elision, RVO/NRVO, 이동 의미론 심화 |
| 05 | 임시 객체 제거 | 임시 객체 생성 진단, 제거 패턴 |
| 06 | 템플릿/constexpr | constexpr/consteval, 컴파일 타임 계산 전략 |
| 07 | Modern C++ 기능 | C++17/20/23 성능 관련 기능 (ranges, concepts, modules) |
| 08 | 코루틴 성능 | C++20 코루틴의 성능 특성과 오버헤드 |
| 09 | 예외 처리 심화 | zero-cost exception의 실제, noexcept 전략 |
| 10 | 인라이닝 유도 기법 | 코드 레벨 인라이닝 유도 기법, inline/forceinline 활용 (진단: Course 02) |
| 11 | std::variant/optional/expected | 타입 안전 유니온과 옵셔널 타입의 성능 특성, 오버헤드 분석 |
| 12 | std::span과 뷰 패턴 | 안전한 뷰 패턴, span/string_view 활용과 성능 이점 |
| 13 | 람다 표현식 성능 | 캡처 비용 (by-value vs by-reference), 클로저 최적화 |
| 14 | Small Buffer Optimization | SBO 패턴 상세, std::function/std::any 내부 구조 |
| 15 | Parameter Passing 전략 | by value vs const ref vs rvalue ref 정량 분석 |

## 측정과 검증 (이 트랙 기준)

- 마이크로벤치마크로 "추상화 1개"의 비용을 분리 측정
- 컴파일 결과(인라이닝/코드 크기)와 런타임 수치를 함께 확인
- 변경 전/후 회귀 검증(최소한의 자동화 포함)

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: `Compiler & Build Optimization` (Course 02), `Memory & Allocation` (Course 03), `Concurrency` (Course 04)
