---
draft: true
title: "[Performance 07] Introduction: OS·런타임 Low-latency 운영환경"
slug: getting-started-os-runtime-performance-tuning
description: "OS·런타임 Low-latency 운영환경 트랙의 도입 챕터입니다. context switch/syscall/affinity/realtime scheduling의 책임 경계를 정리하고, 환경 변화가 지연시간 분포에 미치는 영향을 검증하는 방법을 소개합니다."
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
  - OS
  - Operating System
  - Runtime
  - Linux
  - Windows
  - Scheduling
  - Realtime
  - RT
  - Context Switch
  - Syscall
  - CPU Pinning
  - Affinity
  - IRQ
  - Timer
  - Clock
  - Timekeeping
  - HFT
  - cgroups
  - cgroups v2
  - mlock
  - mlockall
  - Signal Handling
  - Game Engine
  - Realtime Media
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
  - 프로파일링
  - 운영체제
  - 런타임
  - 리눅스
  - 윈도우
  - 스케줄링
  - 실시간
  - 컨텍스트 스위치
  - 시스템콜
  - CPU 고정
  - CPU affinity
  - 인터럽트
  - 타이머
  - 클럭
  - 시간 측정
  - HFT
  - 성능 회귀
  - 유지보수
---

이 트랙은 "코드는 빠른데 프로세스가 느린 이유"를 운영환경에서 찾고 고칩니다. µs 단위에서는 context switch, syscall, 스케줄링 정책, 코어 배치가 지연시간의 바닥을 결정합니다.

## 이 트랙이 책임지는 범위

- context switch 비용과 회피 전략(스레드/코어 배치)
- syscall 비용과 경로 단축(가능한 범위의 사용자 공간 설계)
- CPU pinning/affinity 전략, NUMA 고려
- realtime scheduling의 개념과 적용 시 고려사항
- 타이밍/클럭/시간 측정 이슈(정확한 시간 기반 검증)

## 이 트랙이 다루지 않는 것 (경계)

- 커널/스케줄러 구현을 직접 수정하는 수준의 튜닝 (→ 필요 시 별도 심화)
- C++ 언어/컴파일러/데이터 구조 자체의 최적화 상세 (→ 각 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | Context Switch 비용 | Context switch 비용 분석과 회피 전략 |
| 02 | Syscall 최적화 | Syscall 비용과 최소화 기법 |
| 03 | CPU Pinning/Affinity | CPU pinning/affinity 전략 |
| 04 | NUMA CPU Affinity | NUMA 아키텍처에서의 CPU affinity와 스레드 배치 (메모리 할당: Course 03) |
| 05 | Realtime 스케줄링 | Realtime 스케줄링 적용 |
| 06 | 정밀 시간 측정 | RDTSC, clock_gettime 등 정밀 타이밍 |
| 07 | 커널 바이패스 개요 | 커널 바이패스 개념과 적용 판단 기준 (심화: Course 11, 12) |
| 08 | io_uring 개요 | io_uring 아키텍처 개요와 OS 관점 이해 (심화: Course 11) |
| 09 | XDP/eBPF 개요 | XDP, eBPF 기반 OS 레벨 최적화 개요 (네트워크 심화: Course 12) |
| 10 | Huge TLB Pages | Huge TLB Pages 활용 |
| 11 | 컨테이너 성능 | 컨테이너/가상화 성능 고려사항 |
| 12 | IRQ 최적화 | IRQ 처리와 인터럽트 최적화 |
| 13 | cgroups v2 | cgroups v2 기반 리소스 제어와 성능 영향 |
| 14 | Memory Locking | mlock/mlockall을 활용한 메모리 고정 전략 |
| 15 | Signal Handling | Signal handling 오버헤드와 회피 전략 |
| 16 | Process vs Thread | 프로세스 vs 스레드 아키텍처 선택 기준 |

## 측정과 검증 (이 트랙 기준)

- 운영환경 변경(affinity/scheduler) 전후 레이턴시 분포 비교
- 동일 하드웨어에서 재현 가능한 기준선 확보(변수 최소화)
- 시스템 레벨 회귀를 자동화(환경/런타임 설정 포함)

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: `Concurrency` (Course 04), `CPU Microarchitecture` (Course 06)
