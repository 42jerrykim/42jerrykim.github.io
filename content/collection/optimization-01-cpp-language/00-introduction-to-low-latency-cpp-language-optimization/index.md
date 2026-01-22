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
---

이 트랙은 “C++를 더 잘 쓰면 해결되는 성능”에 집중합니다. µs 단위에서는 작은 추상화/할당/복사 비용이 누적되어 핫패스를 지배하므로, 언어 레벨 비용을 수치로 확인하고 제거하는 능력이 핵심입니다.

## 이 트랙이 책임지는 범위

- 언어 추상화 비용(가상화, RTTI, 예외, 캡슐화 경계)
- STL/표준 라이브러리 사용 비용(컨테이너, 알고리즘, string)
- 객체 수명/복사/이동 비용, 임시 객체 제거
- 메모리 할당/해제 비용과 회피(가능한 범위)
- 템플릿/constexpr 기반의 비용 제어와 인라이닝 유도(언어 관점)

## 이 트랙이 다루지 않는 것 (경계)

- CPU 파이프라인/분기 예측/캐시 미스 “원인”의 하드 분석 (→ CPU 트랙)
- OS 스케줄링, CPU pinning, syscall 비용 (→ OS/런타임 트랙)
- 락 경합/메모리 모델/false sharing 같은 동시성 구조 (→ 동시성 트랙)

## 측정과 검증 (이 트랙 기준)

- 마이크로벤치마크로 “추상화 1개”의 비용을 분리 측정
- 컴파일 결과(인라이닝/코드 크기)와 런타임 수치를 함께 확인
- 변경 전/후 회귀 검증(최소한의 자동화 포함)

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis`
- 병행: `Low-latency Compiler & Build Optimization`, `Memory & Data Layout`, `Concurrency`
