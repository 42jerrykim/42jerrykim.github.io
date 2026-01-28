---
draft: true
title: "[Performance 08] Introduction: 극한 Low-latency 최적화 특수기술"
slug: getting-started-extreme-performance-optimization-techniques
description: "극한 Low-latency 최적화 특수기술 트랙의 도입 챕터입니다. SIMD/asm/prefetch/branchless를 언제 써야 하는지 경계를 명확히 하고, 노이즈 통제된 측정·검증 루프를 전제로 한 적용 원칙을 정리합니다."
tags:
  - Performance
  - Performance Engineering
  - Performance Optimization
  - Low Latency
  - Low-latency
  - Microsecond
  - Latency
  - Benchmark
  - Microbenchmark
  - Profiling
  - Optimization
  - SIMD
  - Vectorization
  - Intrinsics
  - Assembly
  - Hand-written ASM
  - Prefetch
  - Branchless
  - Finite State Machine
  - FSM
  - CPU
  - Cache
  - Pipeline
  - Branch Prediction
  - Memory
  - Data Layout
  - Codegen
  - Regression
  - Safety
  - ARM NEON
  - NEON
  - Highway
  - xsimd
  - Eigen
  - Portable SIMD
  - Cache-oblivious
  - GPU
  - CUDA
  - OpenCL
  - SYCL
  - Heterogeneous Computing
  - 측정
  - 검증
  - 성능
  - 성능공학
  - 성능 최적화
  - 저지연
  - 마이크로초
  - 레이턴시
  - 벤치마크
  - 마이크로벤치마크
  - 프로파일링
  - 최적화
  - SIMD
  - 벡터화
  - 인트린식
  - 어셈블리
  - 프리페치
  - 브랜치리스
  - 상태 머신
  - CPU
  - 캐시
  - 파이프라인
  - 분기 예측
  - 메모리
  - 데이터 레이아웃
  - 코드 생성
  - 성능 회귀
  - 포터블 SIMD
  - 캐시 독립 알고리즘
  - 이기종 컴퓨팅
  - GPU 오프로딩
---

이 트랙은 "정말로 필요할 때만" 접근하는 특수 기술 묶음입니다. 잘못된 조기 진입은 복잡도만 키우고 회귀를 부르기 쉬우므로, 반드시 목표/측정/검증이 준비된 상황에서 사용합니다.

## 이 트랙이 책임지는 범위

- SIMD/인트린식 기반 최적화(벡터화 전략)
- hand-written asm의 적용 판단과 위험 관리
- prefetch/branchless 설계(조건 분기 최소화)
- 극한 수준의 핫패스 튜닝에서 "유지보수 가능성"까지 포함한 설계

## 이 트랙이 다루지 않는 것 (경계)

- 기본적인 언어/컴파일러/메모리/동시성 최적화의 기초 (→ Course 01-04 선행 권장)
- 운영환경(스케줄링/affinity) 변경 중심의 튜닝 (→ OS/런타임 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | SIMD 기초 | SIMD 기초 (SSE, AVX) |
| 02 | SIMD Intrinsics | SIMD intrinsics 실전 활용 |
| 03 | AVX-512 최적화 | AVX-512 최적화 기법 |
| 04 | 자동 벡터화 | 자동 벡터화 유도와 검증 |
| 05 | Prefetch 전략 | Prefetch 전략과 적용 판단 |
| 06 | Branchless 프로그래밍 | Branchless 프로그래밍 기법 |
| 07 | Hand-written ASM | Hand-written 어셈블리 적용과 위험 관리 |
| 08 | Lookup Table 최적화 | Lookup Table 최적화 |
| 09 | 비트 조작 최적화 | 비트 조작 최적화 기법 |
| 10 | 핫패스 극한 튜닝 | 핫패스 극한 튜닝 사례 |
| 11 | 유지보수성 균형 | 극한 최적화와 유지보수성 균형 |
| 12 | ARM NEON 최적화 | ARM NEON intrinsics, Apple Silicon/ARM 서버 대응 |
| 13 | SIMD 라이브러리 | Highway, xsimd, Eigen 등 포터블 SIMD 라이브러리 활용 |
| 14 | Cache-oblivious 알고리즘 | 캐시 크기 독립적인 알고리즘 설계 기법 |
| 15 | GPU Offloading 기초 | CUDA/OpenCL/SYCL 개념과 CPU-GPU 협업 판단 기준 |

## 측정과 검증 (이 트랙 기준)

- microbenchmark로 단일 변경의 효과를 재현(노이즈 통제 필수)
- p99/p999 같은 꼬리 지연시간까지 개선되는지 확인
- 회귀 방지: 특수기술은 "되돌리기 비용"이 크므로 자동화 강화

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05), `CPU Microarchitecture` (Course 06)
- 병행: `Memory & Allocation & Data Layout` (Course 03), `Compiler & Build Optimization` (Course 02)

> **주의**: 이 트랙은 측정 기반 최적화의 마지막 단계입니다. Course 01-06을 먼저 완료하는 것을 권장합니다.
