---
draft: true
title: "[Performance 03] Introduction: Low-latency 메모리·할당·레이아웃"
slug: getting-started-memory-allocation-data-layout-tuning
description: "Low-latency 메모리·할당·데이터 레이아웃 트랙의 도입 챕터입니다. 컨테이너/할당/레이아웃 설계의 책임 경계를 정리하고, allocation·레이턴시 변화를 벤치마크로 검증하는 기본 흐름을 제공합니다."
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
  - STL
  - Memory
  - Allocation
  - Allocator
  - pmr
  - Object Pool
  - Arena Allocator
  - Data Layout
  - AoS
  - SoA
  - Cache Locality
  - Cache Line
  - Prefetch
  - NUMA
  - Page Fault
  - TLB
  - Fragmentation
  - CPU
  - Cache
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
  - 메모리
  - 할당
  - 할당자
  - 데이터 레이아웃
  - 캐시 지역성
  - 캐시 라인
  - NUMA
  - 파편화
  - 페이지 폴트
  - TLB
  - 성능 회귀
  - 유지보수
---

이 트랙은 "메모리 접근 패턴과 할당 정책을 설계해서 지연시간을 줄이는 영역"을 책임집니다. 핫패스에서 allocation 1회, 캐시 라인 1개가 µs 예산을 소모하는 상황을 전제로, 데이터 구조를 비용 관점으로 재구성합니다.

## 이 트랙이 책임지는 범위

- 컨테이너 선택 기준(STL 포함)과 비용 모델 수립
- allocation 제거/감소(풀/arena, 재사용, 수명 그룹화)
- 데이터 레이아웃 설계(AoS/SoA, padding, alignment)
- allocator/`std::pmr`/custom allocator 적용 판단
- 캐시 친화적인 접근 패턴(순차 접근, stride, batching)

## 이 트랙이 다루지 않는 것 (경계)

- SIMD/hand-written asm/명령 수준 튜닝 (→ 극한 최적화 트랙)
- 분기 예측/파이프라인 같은 CPU 하드 분석 (→ CPU 트랙)
- 락 경합/false sharing 중심의 동시성 구조 (→ 동시성 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | 컨테이너 비용 모델 | STL 컨테이너 비용 모델과 선택 기준 |
| 02 | 할당 전략 | 풀/아레나 할당, 객체 재사용 패턴 |
| 03 | 커스텀 할당자 | 커스텀 할당자 구현 패턴 (선형, 풀, 스택) |
| 04 | std::pmr 활용 | polymorphic_allocator 실전 활용 |
| 05 | AoS vs SoA | 데이터 레이아웃 설계와 성능 영향 |
| 06 | 캐시 친화적 패턴 | 순차 접근, stride, batching 전략 |
| 07 | 패딩과 정렬 | 구조체 패딩과 정렬 최적화 |
| 08 | Large Pages | Huge Pages / Large Pages 활용 |
| 09 | NUMA 인식 할당 | NUMA 아키텍처에서의 메모리 할당 |
| 10 | 메모리 단편화 | 단편화 분석과 대응 전략 |
| 11 | 메모리 대역폭 | 메모리 대역폭 최적화 기법 |

## 측정과 검증 (이 트랙 기준)

- allocation 카운트/크기/핫패스 내 위치를 수치로 확인
- 캐시/메모리 관련 지표(가능한 범위)와 레이턴시 변화를 연결
- 컨테이너/레이아웃 변경 전후 회귀를 벤치마크로 검증

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: `Low-latency C++ Language Optimization` (Course 01), `Concurrency` (Course 04)
