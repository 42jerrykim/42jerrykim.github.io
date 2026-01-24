---
draft: true
title: "[Performance 05] Introduction: Low-latency 프로파일링·성능 분석"
slug: getting-started-profiling-performance-analysis-fundamentals
description: "Low-latency 프로파일링·성능 분석 트랙의 도입 챕터입니다. microbenchmark/프로파일링으로 hot path를 찾고, 지표를 해석해 회귀를 자동화하는 공통 기반을 한 번에 정리합니다."
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
  - Sampling Profiler
  - Tracing
  - Flamegraph
  - Hot Path
  - Optimization
  - Regression
  - Performance Budget
  - CI
  - Observability
  - Metrics
  - Histogram
  - p50
  - p95
  - p99
  - Tail Latency
  - CPU
  - Cache
  - Memory
  - Concurrency
  - Linux
  - Windows
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
  - 트레이싱
  - 플레임그래프
  - 핫패스
  - 최적화
  - 성능 회귀
  - 성능 예산
  - 자동화
  - 관측가능성
  - 메트릭
  - 히스토그램
  - 꼬리 지연시간
  - 운영환경
---

이 트랙은 모든 트랙의 공통 기반입니다. µs 단위 최적화는 "측정→가설→변경→검증→회귀 방지" 루프가 없으면 재현 불가능한 우연이 되기 때문에, 분석 역량을 표준화합니다.

## 이 트랙이 책임지는 범위

- microbenchmark 설계/작성(노이즈 통제, 반복 가능성)
- 프로파일링으로 hot path 식별(샘플링/트레이싱)
- 성능 수치 해석(분포/꼬리 지연시간, p95/p99)
- 회귀 감지 자동화(벤치마크/성능 테스트를 CI에 연결)

## 이 트랙이 다루지 않는 것 (경계)

- "어떤 추상화가 좋은가" 같은 코드 스타일/철학 논쟁 (→ 성능 설계·의사결정 트랙)
- 구체적인 언어/컴파일러/CPU/OS 최적화 기법의 상세 (→ 각 전문 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | Microbenchmark 설계 | 설계 원칙, 노이즈 통제, 반복 가능성 |
| 02 | Google Benchmark | Google Benchmark 실전 활용 |
| 03 | 샘플링 프로파일링 | 샘플링 프로파일러 원리와 활용 (perf, VTune) |
| 04 | 트레이싱 프로파일링 | 트레이싱 프로파일러 (Perfetto, Tracy) |
| 05 | Flame Graph 분석 | Flame Graph 해석과 병목 추적 |
| 06 | Intel VTune 심화 | Intel VTune 심화 활용 |
| 07 | Linux perf 고급 | Linux perf 고급 사용법 |
| 08 | 하드웨어 카운터 | 하드웨어 성능 카운터 활용 |
| 09 | Tail Latency 분석 | 꼬리 지연시간(p95/p99/p999) 분석 |
| 10 | 통계적 벤치마킹 | 벤치마크 통계 분석 (신뢰 구간, 유의성) |
| 11 | 지속적 프로파일링 | 지속적 프로파일링 (production profiling) |
| 12 | 성능 A/B 테스트 | 성능 A/B 테스트 방법론 |

## 측정과 검증 (이 트랙 기준)

- 동일 조건 재현(고정 입력, 반복, 워밍업, 변동성 기록)
- 변경 단위 최소화(한 번에 한 가설만 검증)
- 성능 회귀를 PR 단위로 차단하는 기준선 설정

## 추천 선행/병행 트랙

- 병행: 모든 트랙 (모든 트랙의 기본 도구)

> **이 트랙을 먼저 학습하는 것을 강력히 권장합니다.** 측정 없는 최적화는 추측입니다.
