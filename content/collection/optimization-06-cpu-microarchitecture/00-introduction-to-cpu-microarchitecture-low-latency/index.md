---
draft: true
title: "[Performance 06] Introduction: CPU 마이크로아키텍처 Low-latency"
slug: getting-started-cpu-microarchitecture-performance-tuning
description: "CPU 마이크로아키텍처 Low-latency 트랙의 도입 챕터입니다. 파이프라인·분기 예측·캐시·ILP 관점의 책임 범위를 정리하고, 하드웨어 이벤트와 지연시간을 연결해 검증하는 흐름을 소개합니다."
tags:
  - Performance
  - Performance Engineering
  - Performance Optimization
  - Low Latency
  - Low-latency
  - Microsecond
  - Latency
  - Benchmark
  - Profiling
  - CPU
  - Microarchitecture
  - Pipeline
  - Branch Prediction
  - Cache
  - Cache Hierarchy
  - Cache Miss
  - L1
  - L2
  - L3
  - ILP
  - Instruction-Level Parallelism
  - Speculation
  - Out-of-Order
  - Frontend
  - Backend
  - TLB
  - Prefetch
  - Memory
  - NUMA
  - Assembly
  - Codegen
  - Regression
  - 측정
  - 검증
  - 성능
  - 성능공학
  - 성능 최적화
  - 저지연
  - 마이크로초
  - 레이턴시
  - 벤치마크
  - 프로파일링
  - CPU
  - 마이크로아키텍처
  - 파이프라인
  - 분기 예측
  - 캐시
  - 캐시 미스
  - ILP
  - 명령 수준 병렬성
  - 추측 실행
  - Out-of-Order
  - TLB
  - 프리페치
  - 메모리
  - NUMA
  - 성능 회귀
---

이 트랙은 “왜 이 코드가 캐시 미스를 내는가”, “왜 분기 예측이 깨지는가” 같은 질문에 답합니다. µs 최적화에서는 CPU 이벤트가 지연시간 분포를 흔들기 때문에, 하드웨어 관점의 비용 모델이 필요합니다.

## 이 트랙이 책임지는 범위

- 파이프라인과 기본 성능 모델(명령 처리 흐름)
- branch predictor 동작과 분기 형태의 비용
- cache hierarchy와 캐시 미스가 지연시간에 미치는 영향
- instruction-level parallelism(ILP)과 병목 형태

## 이 트랙이 다루지 않는 것 (경계)

- 언어 레벨 비용(추상화/할당/수명) (→ C++ 트랙)
- 빌드/옵션/LTO/PGO 같은 컴파일러 설계 (→ 컴파일러 트랙)
- OS 스케줄링/CPU pinning/syscall 비용 (→ OS/런타임 트랙)

## 측정과 검증 (이 트랙 기준)

- 프로파일러/하드웨어 이벤트 기반으로 병목을 “원인”까지 연결
- 코드 변경 전후에 캐시/분기 관련 지표와 레이턴시를 함께 비교
- 과최적화 방지: 지표 개선이 실제 p99 개선으로 이어지는지 검증

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis`
- 병행: `Memory & Allocation & Data Layout`, `Extreme Optimization Techniques`
