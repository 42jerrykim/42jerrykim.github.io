---
collection_order: 0
date: 2026-03-24
lastmod: 2026-03-25
draft: false
image: wordcloud.png
title: "[Performance 12] Introduction: Low-latency 네트워크 최적화"
slug: getting-started-network-performance-tuning
description: "Low-latency 네트워크 최적화 트랙의 도입 챕터입니다. 네트워크 지연 직관부터 소켓·직렬화·프로토콜·커널 바이패스까지의 진입 순서를 정리하고, RTT·직렬화 비용·처리량을 분리 측정하는 접근을 소개합니다."
tags:
  - Performance(성능)
  - Profiling(프로파일링)
  - Optimization(최적화)
  - C++
  - Compiler(컴파일러)
  - Memory(메모리)
  - CPU(Central Processing Unit)
  - Cache
  - Concurrency(동시성)
  - Linux(리눅스)
  - Windows(윈도우)
  - OS(운영체제)
  - Networking(네트워킹)
  - IO(Input/Output)
  - Testing(테스트)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Monitoring(모니터링)
  - Benchmark
  - Latency
  - Throughput
  - Backend(백엔드)
  - Embedded(임베디드)
  - Code-Quality(코드품질)
  - Best-Practices
  - Refactoring(리팩토링)
  - Software-Architecture(소프트웨어아키텍처)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Reference(참고)
  - Technology(기술)
  - Deep-Dive
  - Production
  - Scalability(확장성)
  - Reliability
  - Implementation(구현)
  - Documentation(문서화)
  - Debugging(디버깅)
  - Automation(자동화)
  - System-Design
  - Data-Structures(자료구조)
  - Clean-Code(클린코드)
  - 네트워크
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

- 파일 I/O, 디스크 I/O 최적화 (→ I/O 최적화 트랙 Tr.11)
- C++ 언어 레벨 최적화 상세 (→ C++ 언어 트랙)
- CPU 파이프라인/캐시의 하드 분석 (→ CPU 트랙)
- 동시성/멀티스레드 구조 설계 (→ 동시성 트랙)

## 커리큘럼

**난이도 범례**: **기초**(입문) · **중급**(실무 핵심) · **심화**(깊은 분석·전문 주제) · **전문**(극한·니치). **Tr.NN**은 `optimization-NN-*` 트랙을 가리킵니다. **심화(본 트랙)** 행은 Tr.07의 동일 주제 **개요**를 이어 받습니다.

처음 읽는다면 **20 → 01 → 02 → 03 → 05 → 08** 순서로 진입하는 것이 안전합니다. 20은 RTT·직렬화·대역폭의 기본 직관을 만들고, 01~03은 전송 지연과 소켓 옵션의 바닥을 정리하며, 05와 08은 직렬화와 프로토콜 설계의 핵심 비용 모델을 먼저 잡아 줍니다.

네트워크 트랙도 **표 순서는 유지**하는 편이 유리합니다. `10~11`의 커널 바이패스 심화, `12~13`, `15`, `16`, `19` 같은 고급 전송 주제를 장 번호 기준으로 참조하기 쉬워야 하므로, 표는 전체 구조를 보여 주고 추천 순서는 입문자에게 필요한 바닥 개념을 먼저 놓는 역할을 맡습니다.

| 챕터 | 제목 | 난이도 | 핵심 내용 |
|------|------|--------|-----------|
| 01 | 네트워크 지연 구조 | 기초 | 네트워크 지연시간 구성 요소 분석 |
| 02 | 소켓 옵션 튜닝 | 중급 | TCP_NODELAY, SO_SNDBUF, 버퍼 최적화 |
| 03 | TCP 성능 최적화 | 중급 | Nagle 알고리즘, Delayed ACK, 혼잡 제어, BBRv3(IETF 표준화 진행 중) |
| 04 | UDP 최적화 | 중급 | UDP 활용과 신뢰성 레이어 설계 |
| 05 | 직렬화 성능 비교 | 중급 | Protocol Buffers, FlatBuffers, Cap'n Proto |
| 06 | Zero-copy 직렬화 | 심화 | FlatBuffers, Cap'n Proto zero-copy 활용 |
| 07 | 차세대 Zero-copy 직렬화 포맷 동향(YaFF 등) | 심화 | Yandex YaFF(2026-06 공개) 등 신흥 zero-copy 포맷과 기존 FlatBuffers/Cap'n Proto 비교 판단 기준 |
| 08 | 프로토콜 설계 | 중급 | 저지연 바이너리 프로토콜 설계 원칙 |
| 09 | 메시지 프레이밍 | 중급 | Length-prefix, delimiter, fixed-size 전략 |
| 10 | 네트워크 DPDK 심화 | 전문 | 심화(본 트랙); 개요는 Tr.07; NVIDIA BlueField-4 등 최신 SmartNIC/DPU 오프로드 동향 포함 |
| 11 | 네트워크 XDP/eBPF | 전문 | 심화(본 트랙); 개요는 Tr.07 |
| 12 | RDMA 기초 | 심화 | RDMA/InfiniBand 개념과 활용 |
| 13 | Ultra Ethernet Consortium(UEC)과 차세대 저지연 이더넷 | 전문 | 2025-06 발표된 UEC Specification 1.0, PFC 없는 무손실 저지연 이더넷과 RoCEv2/InfiniBand 대비 위치 |
| 14 | gRPC 최적화 | 중급 | gRPC 성능 튜닝 |
| 15 | QUIC 프로토콜 | 심화 | QUIC 성능 특성, 0-RTT 연결, UDP 기반 전송 |
| 16 | TLS/SSL 최적화 | 심화 | TLS 핸드셰이크 최적화, 세션 재개, 0-RTT, PQC 하이브리드 키교환이 핸드셰이크 지연에 미치는 영향 |
| 17 | Connection Pooling | 중급 | 연결 풀링 전략, Keep-alive, 연결 재사용 |
| 18 | WebSocket 최적화 | 중급 | WebSocket 성능 튜닝, 압축, 메시지 배치 |
| 19 | HTTP/2와 HTTP/3 | 심화 | HTTP/2 멀티플렉싱, HTTP/3 QUIC 기반 성능 비교, WebTransport는 2026-03 Baseline 도달했으나 실무 채택은 준비 단계 |
| 20 | 네트워크 지연 직관 | 기초 | RTT·대역폭·직렬화 비용이 지연에 미치는 그림 잡기 (선행: 챕터 01 전에 읽기 권장) |
| 21 | 네트워크 압축 전략 | 중급 | LZ4/zstd/snappy in-transit 압축의 CPU-대역폭 트레이드오프와 선택 기준 |

## 측정과 검증 (이 트랙 기준)

- 네트워크 왕복시간(RTT) 분포 분석 (p50/p95/p99)
- 처리량(throughput)과 지연시간(latency) trade-off 분석
- 직렬화/역직렬화 벤치마크 (메시지 크기별)
- 패킷 캡처를 통한 프로토콜 오버헤드 분석

## 추천 선행/병행 트랙

- **선행**: Low-latency 프로파일링·성능 분석 (Tr.05), I/O 최적화 (Tr.11)
- **병행**: OS·런타임 (Tr.07), 동시성 (Tr.04)

> **네트워크 서버·마이크로서비스·분산 시스템·HFT**에서 이 트랙이 핵심이 됩니다.

## 왜 이 트랙인가 (동기)

RTT·직렬화·프로토콜 오버헤드·커널 스택 비용이 겹치면, 애플리케이션 로직만 최적화해도 한계가 빨리 옵니다. Tr.07의 XDP/eBPF·커널 바이패스 **개요**를 읽은 뒤, 이 트랙에서는 **패킷 처리 심화·RDMA·QUIC·TLS**까지 확장합니다. Tr.04와 함께 보면 수락 루프·스레드 모델과의 상호작용까지 설계할 수 있습니다.

## Phase별 학습 궤적

**Phase A — 전송·TCP/UDP (챕터 01~04)** 지연 구성 요소와 소켓 옵션을 이해합니다.

**Phase B — 직렬화·프로토콜 (챕터 05~09, 14, 17~19, 21)** 메시지 설계는 CPU(Tr.06), 언어 표현(Tr.01), 할당·레이아웃(Tr.03)과 만나는 지점입니다. 챕터 07의 신흥 zero-copy 포맷 동향은 06의 기존 포맷 비교 감각을 먼저 잡은 뒤 읽으면 판단이 쉬워집니다. 압축(21)까지 포함해 CPU-대역폭 trade-off를 함께 봐야 합니다.

**Phase C — 커널 바이패스·고급 전송 (챕터 10~13, 15~16)** DPDK·XDP/eBPF **심화(본 트랙)**는 Tr.07 개요 위에 실전을 얹습니다. RDMA(12) 직후에 배치한 UEC(13)는 RoCEv2/InfiniBand 대안으로서 같은 맥락에서 비교하며 읽는 편이 좋습니다. QUIC·TLS 0-RTT는 **심화~전문**에 가깝습니다.

## 이 트랙을 마친 후 달성할 목표

- **측정**: RTT·처리량·직렬화 비용을 분리해 벤치마크할 수 있다.
- **설계**: 바이너리 프로토콜·프레이밍을 지연 예산에 맞게 선택할 수 있다.
- **연계**: Tr.07 개요와 본 트랙 심화의 역할을 팀에 설명할 수 있다.

## 평가 기준과 이 장을 읽은 후 확인

- [ ] Tr.07 챕터 07·09(커널 바이패스·XDP/eBPF 개요)와 본 트랙 챕터 10·11(DPDK·XDP/eBPF 심화)의 난이도·목적 차이를 말할 수 있는가?
- [ ] Tr.11 파일 I/O와 네트워크 I/O의 병목 지표가 어떻게 다른지 예시를 들 수 있는가?

## 범위와 경계

```mermaid
flowchart LR
  subgraph inScope [이 트랙]
    A["소켓·TCP·UDP"]
    B["직렬화·프로토콜"]
    C["DPDK·XDP 심화"]
  end
  subgraph outScope [경계 밖]
    D["디스크 I/O Tr.11"]
    E["동시성 구조 Tr.04"]
    F["CPU 미세 Tr.06"]
  end
  inScope --> outScope
```

## 심화·전문가 확장 궤적

DPDK·XDP/eBPF는 운영·보안·배포 정책(Tr.09)과 충돌할 수 있습니다. **전문** 난이도 챕터는 스테이징·카나리(Tr.10) 전제를 권장합니다. 중급 실무 확장 후보로는 **DNS/service discovery 지연**, **service mesh 오버헤드**, **배치·압축·연결 재사용의 데이터센터 내부 통신 패턴**을 이어서 검토할 수 있습니다.

## 시리즈 전체 로드맵

12개 트랙의 권장 순서·심화 진입 조건은 **[Low-latency 최적화 시리즈 개요](/post/low-latency-optimization-series/getting-started-low-latency-optimization-series-overview/)**를 참고하세요.

## 지금 바로 이어 읽을 곳

**20 → 01 → 02 → 03** 순으로 읽으면 네트워크 지연 직관에서 지연 구조·소켓 옵션·TCP 성능 최적화까지 이어집니다.

- [네트워크 지연 직관](/post/network-optimization/network-latency-intuition-rtt-bandwidth-fundamentals/) (챕터 20)
- [네트워크 지연 구조](/post/network-optimization/network-latency-structure-components/) (챕터 01)
- [소켓 옵션 튜닝](/post/network-optimization/socket-options-tcp-nodelay-buffer-tuning/) (챕터 02)
