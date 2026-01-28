---
draft: true
title: "[Performance 11] Introduction: Low-latency I/O 최적화"
slug: getting-started-io-performance-tuning
description: "Low-latency I/O 최적화 트랙의 도입 챕터입니다. I/O 패턴, 비동기 I/O, zero-copy, memory-mapped I/O의 책임 범위를 정리하고, I/O 병목을 측정·검증하는 기본 접근을 소개합니다."
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
  - Profiling
  - I/O
  - Input Output
  - File I/O
  - Disk I/O
  - Async
  - Asynchronous
  - io_uring
  - epoll
  - IOCP
  - AIO
  - Zero Copy
  - sendfile
  - splice
  - mmap
  - Memory Mapped
  - Page Cache
  - Direct I/O
  - Buffered I/O
  - File System
  - Block Device
  - NVMe
  - SSD
  - Storage
  - Vectored I/O
  - readv
  - writev
  - WAL
  - Write-Ahead Log
  - fsync
  - File Locking
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
  - 프로파일링
  - 입출력
  - 파일 I/O
  - 디스크 I/O
  - 비동기
  - 메모리 매핑
  - 페이지 캐시
  - 파일시스템
  - 스토리지
---

이 트랙은 "데이터가 저장장치를 오가는 경로"의 지연시간을 줄이는 영역을 책임집니다. µs 단위에서는 시스템콜 비용, 복사 횟수, I/O 스케줄링이 지연시간의 상당 부분을 차지합니다.

## 이 트랙이 책임지는 범위

- I/O 패턴과 비용 모델 (동기 vs 비동기, 블로킹 vs 논블로킹)
- 비동기 I/O 기법 (epoll, io_uring, IOCP, AIO)
- Zero-copy 기법 (sendfile, splice, mmap)
- Memory-mapped I/O 최적화
- 파일시스템과 블록 디바이스 특성 이해
- Direct I/O vs Buffered I/O 선택

## 이 트랙이 다루지 않는 것 (경계)

- 네트워크 소켓/프로토콜 최적화 (→ 네트워크 최적화 트랙 Course 12)
- C++ 언어 레벨 최적화 상세 (→ C++ 언어 트랙)
- CPU 파이프라인/캐시의 하드 분석 (→ CPU 트랙)
- OS 스케줄러/affinity의 상세 (→ OS/런타임 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | I/O 패턴과 비용 | 동기/비동기, 블로킹/논블로킹 비용 모델 |
| 02 | 비동기 I/O 기초 | select, poll, epoll, kqueue 비교 |
| 03 | io_uring 심화 | Linux io_uring 아키텍처와 파일 I/O 실전 활용 (개요: Course 07) |
| 04 | IOCP와 Windows I/O | Windows IOCP 모델과 최적화 |
| 05 | Zero-copy 기법 | sendfile, splice, copy_file_range 활용 |
| 06 | Memory-mapped I/O | mmap 활용과 주의사항 |
| 07 | Direct I/O | O_DIRECT와 페이지 캐시 바이패스 |
| 08 | 파일시스템 특성 | ext4, XFS, ZFS 등 성능 특성 |
| 09 | 블록 디바이스 최적화 | NVMe, SSD 특성과 I/O 스케줄러 |
| 10 | I/O 멀티플렉싱 패턴 | Reactor, Proactor 패턴 구현 |
| 11 | Vectored I/O | readv/writev, preadv2/pwritev2 활용 |
| 12 | POSIX AIO vs io_uring | POSIX AIO와 io_uring 성능 비교 |
| 13 | Database I/O 패턴 | WAL, fsync, 저널링 전략과 성능 영향 |
| 14 | File Locking 성능 | 파일 잠금이 성능에 미치는 영향과 대안 |

## 측정과 검증 (이 트랙 기준)

- I/O 처리량(throughput)과 지연시간(latency) 분리 측정
- 시스템콜 횟수/비용 프로파일링 (strace, perf)
- 복사 횟수 추적 (zero-copy 적용 전후)
- IOPS, 대역폭, 지연시간 분포 분석

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05)
- 병행: `OS & Runtime Low-latency` (Course 07), `Memory & Allocation` (Course 03)
- 후행: `Network Optimization` (Course 12)

> **스토리지 시스템, 데이터베이스, 파일 처리 애플리케이션을 다루는 경우 이 트랙이 필수입니다.**
