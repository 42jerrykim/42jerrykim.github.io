---
draft: true
title: "[Performance 12] Introduction: Low-latency 네트워크 최적화"
slug: getting-started-network-performance-tuning
description: "Low-latency 네트워크 최적화 트랙의 도입 챕터입니다. 소켓 최적화, 프로토콜 설계, 직렬화 성능, 커널 바이패스의 책임 범위를 정리하고, 네트워크 병목을 측정·검증하는 기본 접근을 소개합니다."
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
  - Network
  - Networking
  - Socket
  - TCP
  - UDP
  - RDMA
  - InfiniBand
  - Kernel Bypass
  - DPDK
  - XDP
  - eBPF
  - Serialization
  - Deserialization
  - Protocol Buffers
  - FlatBuffers
  - Cap'n Proto
  - MessagePack
  - Binary Protocol
  - Text Protocol
  - JSON
  - HTTP
  - gRPC
  - Nagle
  - TCP_NODELAY
  - Buffer
  - Congestion Control
  - RTT
  - QUIC
  - TLS
  - SSL
  - TLS Handshake
  - 0-RTT
  - Session Resumption
  - Connection Pooling
  - Keep-alive
  - WebSocket
  - HTTP/2
  - HTTP/3
  - Multiplexing
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
  - 네트워크
  - 소켓
  - 직렬화
  - 역직렬화
  - 바이너리 프로토콜
  - 커널 바이패스
  - 혼잡 제어
  - 연결 풀링
  - 세션 재개
  - 멀티플렉싱
  - 웹소켓
  - TLS 핸드셰이크
---

이 트랙은 "데이터가 네트워크를 오가는 경로"의 지연시간을 줄이는 영역을 책임집니다. µs 단위에서는 프로토콜 오버헤드, 직렬화 비용, 커널 네트워크 스택 지연이 전체 지연시간의 상당 부분을 차지합니다.

## 이 트랙이 책임지는 범위

- 소켓 옵션과 버퍼 튜닝 (TCP_NODELAY, SO_SNDBUF, SO_RCVBUF)
- 프로토콜 설계 (바이너리 vs 텍스트, 메시지 프레이밍)
- 직렬화/역직렬화 성능 (Protocol Buffers, FlatBuffers, Cap'n Proto)
- 커널 바이패스 기법 (DPDK, XDP, eBPF)
- TCP 혼잡 제어와 튜닝
- RDMA/InfiniBand 기초

## 이 트랙이 다루지 않는 것 (경계)

- 파일 I/O, 디스크 I/O 최적화 (→ I/O 최적화 트랙 Course 11)
- C++ 언어 레벨 최적화 상세 (→ C++ 언어 트랙)
- CPU 파이프라인/캐시의 하드 분석 (→ CPU 트랙)
- 동시성/멀티스레드 구조 설계 (→ 동시성 트랙)

## 커리큘럼

| 챕터 | 제목 | 핵심 내용 |
|------|------|-----------|
| 01 | 네트워크 지연 구조 | 네트워크 지연시간 구성 요소 분석 |
| 02 | 소켓 옵션 튜닝 | TCP_NODELAY, SO_SNDBUF, 버퍼 최적화 |
| 03 | TCP 성능 최적화 | Nagle 알고리즘, Delayed ACK, 혼잡 제어 |
| 04 | UDP 최적화 | UDP 활용과 신뢰성 레이어 설계 |
| 05 | 직렬화 성능 비교 | Protocol Buffers, FlatBuffers, Cap'n Proto |
| 06 | Zero-copy 직렬화 | FlatBuffers, Cap'n Proto zero-copy 활용 |
| 07 | 프로토콜 설계 | 저지연 바이너리 프로토콜 설계 원칙 |
| 08 | 메시지 프레이밍 | Length-prefix, delimiter, fixed-size 전략 |
| 09 | 네트워크 DPDK 심화 | 네트워크 관점 DPDK 아키텍처와 패킷 처리 (개요: Course 07) |
| 10 | 네트워크 XDP/eBPF | 네트워크 패킷 처리를 위한 XDP, eBPF 심화 (개요: Course 07) |
| 11 | RDMA 기초 | RDMA/InfiniBand 개념과 활용 |
| 12 | gRPC 최적화 | gRPC 성능 튜닝 |
| 13 | QUIC 프로토콜 | QUIC 성능 특성, 0-RTT 연결, UDP 기반 전송 |
| 14 | TLS/SSL 최적화 | TLS 핸드셰이크 최적화, 세션 재개, 0-RTT |
| 15 | Connection Pooling | 연결 풀링 전략, Keep-alive, 연결 재사용 |
| 16 | WebSocket 최적화 | WebSocket 성능 튜닝, 압축, 메시지 배치 |
| 17 | HTTP/2와 HTTP/3 | HTTP/2 멀티플렉싱, HTTP/3 QUIC 기반 성능 비교 |

## 측정과 검증 (이 트랙 기준)

- 네트워크 왕복시간(RTT) 분포 분석 (p50/p95/p99)
- 처리량(throughput)과 지연시간(latency) trade-off 분석
- 직렬화/역직렬화 벤치마크 (메시지 크기별)
- 패킷 캡처를 통한 프로토콜 오버헤드 분석

## 추천 선행/병행 트랙

- 선행: `Low-latency Profiling & Performance Analysis` (Course 05), `I/O Optimization` (Course 11)
- 병행: `OS & Runtime Low-latency` (Course 07), `Concurrency` (Course 04)

> **네트워크 서버, 마이크로서비스, 분산 시스템, HFT를 다루는 경우 이 트랙이 필수입니다.**
