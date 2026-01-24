---
draft: true
title: "[Performance 04] Introduction: Low-latency 동시성·멀티스레드"
slug: getting-started-concurrency-multithreading-performance-tuning
description: "Low-latency 동시성·멀티스레드 트랙의 도입 챕터입니다. mutex/atomic/lock-free의 비용 경계를 정의하고, 경합·false sharing을 측정해 p99 지연시간을 안정화하는 기본 접근을 정리합니다."
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
  - Optimization
  - Systems Programming
  - Concurrency
  - Multithreading
  - Threading
  - Synchronization
  - Mutex
  - Spinlock
  - Atomic
  - Lock-free
  - Wait-free
  - Memory Model
  - Acquire Release
  - False Sharing
  - Cache Line
  - Contention
  - Queue
  - Ring Buffer
  - SPSC
  - MPMC
  - NUMA
  - CPU Pinning
  - Scheduling
  - Linux
  - Windows
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
  - 동시성
  - 멀티스레드
  - 스레딩
  - 동기화
  - 뮤텍스
  - 스핀락
  - 원자 연산
  - 락프리
  - 메모리 모델
  - False Sharing
  - 캐시 라인
  - 경합
  - 성능 회귀
  - 유지보수
---

이 트랙은 "스레드가 늘어날수록 느려지는 이유"를 비용 관점으로 설명하고 통제합니다. µs 시스템에서는 lock 경합, cache line ping-pong, 잘못된 atomic 사용이 지연시간의 지배항이 되기 쉽습니다.

## 이 트랙이 책임지는 범위

- `mutex`/`spinlock`/`atomic`의 비용과 선택 기준
- lock-free 설계의 적용 판단(필요/위험/유지보수 비용)
- false sharing 회피, cache line 단위 데이터 분리
- C++ 메모리 모델의 실무적 해석(acquire/release 등)
- 큐/링버퍼(SPSC/MPMC) 등 기본 동시성 구조의 비용 모델

## 이 트랙이 다루지 않는 것 (경계)

- OS 스케줄러 "구현"과 커널 내부 튜닝 (→ OS/런타임 트랙)
- CPU 파이프라인/분기/캐시 계층의 하드 분석 (→ CPU 트랙)
- 알고리즘 자체의 시간 복잡도 선택 (→ 설계/의사결정 트랙 또는 별도)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | 동기화 비용 분석 | mutex/spinlock/atomic 비용 정량 분석 |
| 02 | Lock 선택 기준 | 동기화 프리미티브 선택 가이드 |
| 03 | False Sharing 회피 | False sharing 탐지와 해결 |
| 04 | 메모리 모델 실무 | C++ 메모리 모델 실무 해석 (acquire/release/seq_cst) |
| 05 | Lock-free 기초 | Lock-free 설계 기초와 적용 판단 |
| 06 | Lock-free 자료구조 | Lock-free 큐, 스택, 해시맵 구현 |
| 07 | Hazard Pointers/RCU | Hazard Pointers와 RCU 패턴 |
| 08 | SPSC/MPMC 큐 | SPSC/MPMC 큐와 링버퍼 구현 |
| 09 | C++20 Atomics | C++20 atomic wait/notify 활용 |
| 10 | 스레드 풀 최적화 | 스레드 풀 최적화와 워크 스틸링 |
| 11 | 코루틴 동시성 | 코루틴 기반 동시성 패턴 |
| 12 | Wait-free 프로그래밍 | Wait-free 프로그래밍 기초 |

## 측정과 검증 (이 트랙 기준)

- 경합(락 대기/스핀) 시간을 수치로 분리해서 측정
- 스레드 수 변화에 따른 레이턴시 분포(p50/p95/p99) 확인
- false sharing 개선 전/후를 microbenchmark로 재현/검증

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: `Memory & Allocation & Data Layout` (Course 03), `OS & Runtime Low-latency Tuning` (Course 07)
