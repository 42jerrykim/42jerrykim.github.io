---
draft: true
title: "[Performance 09] Introduction: Low-latency 성능 설계·의사결정"
slug: getting-started-performance-design-decision-making
description: "Low-latency 성능 설계·의사결정 트랙의 도입 챕터입니다. 최적화의 시작/중단 기준과 팀 합의, trade-off 판단을 정리하고, 다른 트랙과의 경계(책임 분리)를 명확히 하는 프레임을 제공합니다."
tags:
  - Performance
  - Performance Engineering
  - Performance Optimization
  - Low Latency
  - Low-latency
  - Microsecond
  - Latency
  - Throughput
  - Profiling
  - Benchmark
  - Optimization
  - Trade-off
  - Decision Making
  - Architecture
  - System Design
  - Design Review
  - Code Review
  - Performance Budget
  - SLO
  - SLA
  - Maintainability
  - Readability
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
  - 프로파일링
  - 벤치마크
  - 최적화
  - 트레이드오프
  - 의사결정
  - 아키텍처
  - 시스템 설계
  - 설계 리뷰
  - 코드 리뷰
  - 성능 예산
  - SLO
  - SLA
  - 유지보수성
  - 가독성
  - 성능 회귀
  - 팀 합의
  - 기준선
---

이 트랙은 "기술의 경계를 정하는 트랙"입니다. µs 요구가 들어오면 모든 레이어가 얽히기 때문에, 무엇을 어떤 트랙이 책임지는지 합의하지 않으면 최적화가 끝나지 않습니다.

## 이 트랙이 책임지는 범위

- 언제 최적화를 시작해야 하는가(측정/병목/목표의 정의)
- 언제 멈춰야 하는가(효과 대비 비용, 리스크, 유지보수)
- 가독성과 성능의 trade-off 판단 기준
- 팀 단위 성능 합의 기준(예: latency budget, SLO, PR 규칙)

## 이 트랙이 다루지 않는 것 (경계)

- C++/컴파일러/메모리/동시성/CPU/OS의 구체 기법 상세 (→ 각 트랙)
- "벤치마크를 어떻게 짜는가" 같은 도구 상세 (→ 프로파일링 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | 최적화 시작 시점 | 언제 최적화를 시작해야 하는가 |
| 02 | 최적화 중단 시점 | 언제 멈춰야 하는가 (비용/효과/리스크) |
| 03 | 가독성 vs 성능 | 가독성과 성능의 trade-off 판단 기준 |
| 04 | 성능 예산 수립 | 성능 예산 수립 방법론 |
| 05 | SLO/SLA 정의 | SLO/SLA 정의와 팀 합의 |
| 06 | 지연시간 vs 처리량 | 지연시간 vs 처리량 아키텍처 결정 |
| 07 | Low-latency 아키텍처 | Low-latency 아키텍처 패턴 |
| 08 | 캐싱 전략 | 캐싱 전략과 성능 영향 |
| 09 | 데이터베이스 접근 | 데이터베이스 접근 최적화 전략 |
| 10 | 팀 성능 문화 | 팀 단위 성능 문화 구축 |
| 11 | 성능 코드 리뷰 | 성능 관점 코드 리뷰 가이드 |

## 측정과 검증 (이 트랙 기준)

- 목표 지표 정의(p50/p95/p99, worst-case, budget)
- 성능 변경을 받아들이는 기준(유의미한 개선/악화의 정의)
- 팀 운영 규칙으로 회귀를 차단(자동화/리뷰 프로세스)

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: Course 01-08 전부 (경계 설정과 우선순위 결정을 위해)

> **이 트랙은 모든 기술 트랙을 아우르는 관리자/리드 관점의 내용입니다.**
