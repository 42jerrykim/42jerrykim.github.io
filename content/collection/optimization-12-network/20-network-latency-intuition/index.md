---
collection_order: 20
date: 2026-07-14
lastmod: 2026-07-14
draft: false
image: wordcloud.png
title: "[Network 12] 네트워크 지연 직관"
slug: network-latency-intuition-rtt-bandwidth-fundamentals
description: "RTT·대역폭·직렬화 지연이 조합되어 네트워크 지연을 만드는 원리를 정성적·정량적으로 다지는 입문 챕터입니다. Bandwidth-Delay Product 계산과 흔한 오개념을 정리해 이후 소켓·TCP·직렬화 챕터를 읽을 직관을 세웁니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - Networking(네트워킹)
  - OS(운영체제)
  - Linux(리눅스)
  - C++
  - C
  - IO(Input/Output)
  - Benchmark
  - Latency
  - Throughput
  - Profiling(프로파일링)
  - Testing(테스트)
  - Implementation(구현)
  - Best-Practices
  - Debugging(디버깅)
  - System-Design
  - Backend(백엔드)
  - Pitfalls(함정)
  - Hardware(하드웨어)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - RTT
  - Bandwidth-Delay-Product
  - Propagation-Delay
  - Serialization-Delay
  - Queuing-Delay
  - TCP-Window-Scaling
  - Fiber-Optic
  - 왕복시간
  - 대역폭
  - 네트워크지연
---

**네트워크 지연 직관**이란 RTT(왕복시간), 대역폭(bandwidth), 직렬화 지연(serialization delay)이 각각 무엇을 의미하고 어떻게 조합되어 최종 지연시간을 만드는지 정성적·정량적으로 파악하는 능력을 말합니다. 이 트랙의 나머지 챕터들은 소켓 옵션, TCP 혼잡 제어, 직렬화 포맷, 프로토콜 설계처럼 각 영역을 깊이 파고들지만, 그 전에 "지연이 어디서 오는가"에 대한 감이 없으면 어떤 최적화가 실제로 유효한지 판단하기 어렵습니다. 예를 들어 응답이 느릴 때 대역폭을 늘려야 할지, 요청 왕복 횟수를 줄여야 할지, 페이로드 크기를 줄여야 할지는 지연의 구성 요소 중 무엇이 지배적인지에 따라 답이 완전히 달라집니다. 이 장은 그 판단을 위한 최소한의 정신 모델을 세우는 것을 목표로 합니다.

## 이 장을 읽기 전에

**전제 지식**: 이 장은 이 트랙의 진입점 역할을 하므로 특별한 선행 챕터가 필요하지 않습니다. 패킷이 헤더와 페이로드로 구성된다는 것, 대역폭이 초당 비트 수(bps)로 표현된다는 것 정도만 알면 충분합니다.

**이 장의 깊이**: **기초** 난이도로, RTT·대역폭·직렬화 지연의 정의와 이들이 결합하는 방식에 대한 정성적 직관과 간단한 정량 계산까지만 다룹니다. 실제 커널 네트워크 스택 내부에서 각 구간을 정밀하게 분해하고 실측하는 방법은 [01장: 네트워크 지연 구조](/post/network-optimization/network-latency-structure-components/)에서 다룹니다.

**다루지 않는 것**: `TCP_NODELAY`·버퍼 튜닝 같은 소켓 옵션은 [02장](/post/network-optimization/socket-options-tcp-nodelay-buffer-tuning/), Nagle·혼잡 제어·BBR 세부는 [03장](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/), Protocol Buffers·FlatBuffers 등 데이터 포맷 인코딩 비용 비교는 [05장](/post/network-optimization/serialization-performance-protobuf-flatbuffers-capnproto/)에서 각각 다루므로 이 장에서는 그 존재만 언급하고 깊이 들어가지 않습니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | 처음 ~ "흔한 오개념 바로잡기" | RTT·대역폭·직렬화 지연이 서로 다른 개념임을 이해 |
| **중급자** | "대역폭과 Bandwidth-Delay Product" ~ "병목을 진단하는 판단 기준" | BDP를 계산하고 표 기반으로 병목 후보를 좁힐 수 있다 |
| **전문가** | "병목을 진단하는 판단 기준" ~ "비판적 시각" | 단순 모델의 한계를 인지하고 실측(프로파일링)으로 전환할 시점을 판단 |

---

## RTT와 대역폭-지연 곱, 감각의 뿌리

지연을 정량적으로 다루려는 시도는 TCP 자체의 역사와 함께 시작되었습니다. 1988년 Van Jacobson과 Michael Karels는 SIGCOMM에 발표한 "Congestion Avoidance and Control" 논문에서 RTT를 지속적으로 샘플링해 재전송 타임아웃(RTO)을 추정하는 알고리즘을 제시했고, 이는 이후 모든 TCP 구현의 기반이 되었습니다. 같은 해 Jacobson과 Braden은 RFC 1072에서 대역폭과 지연의 곱이 큰 경로("long fat network", LFN)에서 16비트 윈도우 필드가 처리량의 병목이 된다는 문제를 처음 정식화했습니다. 이 아이디어는 1992년 RFC 1323을 거쳐 현재는 RFC 7323으로 이어졌고, 이 문서는 지금도 원인을 다음과 같이 명시합니다.

> "This document specifies a set of TCP extensions to improve performance over paths with a large bandwidth * delay product and to provide reliable operation over very high-speed paths." — [RFC 7323: TCP Extensions for High Performance](https://www.rfc-editor.org/rfc/rfc7323) (IETF, 2014)

한편 지연을 "체감 가능한 예산"으로 다루는 관점은 통신 표준에서도 자리 잡았습니다. [ITU-T의 음성 품질 권고안 G.114](https://www.itu.int/rec/T-REC-G.114/en)는 편도(one-way) 지연이 150ms 이하면 대부분의 사용자가 지연을 느끼지 못하고, 150~400ms는 체감은 되지만 사용 가능한 범위, 400ms를 넘으면 대화가 어려워진다는 기준을 제시합니다. 이 숫자 자체는 음성 통화를 염두에 둔 것이지만, "지연에는 사람이 느끼는 예산이 있고 그 예산 안에서 각 구성 요소가 얼마를 차지하는지 나눠 봐야 한다"는 사고방식은 RPC·게임·트레이딩 시스템에도 그대로 적용됩니다.

## RTT를 구성하는 네 가지 지연

패킷 하나가 클라이언트에서 서버로 갔다가 돌아오는 데 걸리는 시간, 즉 **RTT(Round-Trip Time)**는 하나의 원인이 아니라 서로 성격이 다른 네 가지 지연이 누적된 결과입니다. 이 네 가지를 구분하지 못하면 "네트워크가 느리다"는 진단은 항상 막연할 수밖에 없습니다.

### 전파 지연과 직렬화(전송) 지연

**전파 지연(propagation delay)**은 신호가 물리적 매체를 실제로 이동하는 데 걸리는 시간으로, 거리를 매체 내 신호 속도로 나눈 값입니다. 광섬유 안에서 빛은 진공 중 속도(약 299,792km/s)보다 느리게 이동하는데, 표준 단일모드 광섬유(SMF-28 계열)의 굴절률이 약 1.47이기 때문에 실제 속도는 약 200,000km/s 수준이고, 흔히 "1km당 약 5µs" 정도로 근사합니다. 다만 실제 대륙간 경로는 직선 거리를 그대로 따라가지 않고 실제 광케이블 도관(conduit) 경로를 따라 우회하므로, Duke University·ETH Zürich 등 공동 연구진의 2018년 논문 [Dissecting Latency in the Internet's Fiber Infrastructure](https://arxiv.org/abs/1811.10737)는 현재 경로가 직선거리 대비 중앙값 약 2.1배의 지연을 보이며, 기존 도관을 그대로 활용해 경로만 최적화해도 이를 약 1.3배까지 줄일 수 있다고 보고합니다. 즉 지도 위 직선거리만으로 RTT를 예측하면 항상 낙관적인 하한선만 얻게 됩니다.

**직렬화 지연(serialization delay, 또는 전송 지연)**은 패킷 전체를 링크에 비트 단위로 실어 보내는 데 걸리는 시간으로, "패킷 크기(bit) ÷ 링크 대역폭(bit/s)"으로 계산합니다. 아래 함수는 이 계산을 그대로 코드로 옮긴 것입니다.

```cpp
#include <cstdint>

// 직렬화 지연(전송 지연): 패킷 전체를 링크에 실어 보내는 데 걸리는 시간(초)
// packet_bits: 패킷 크기(bit 단위), bandwidth_bps: 링크 대역폭(bit/s 단위)
double serialization_delay_sec(uint64_t packet_bits, uint64_t bandwidth_bps) {
  return static_cast<double>(packet_bits) / static_cast<double>(bandwidth_bps);
}
```

1500바이트(12,000비트) 패킷을 기준으로 계산하면 1Gbps 링크에서는 약 12µs, 10Gbps에서는 약 1.2µs, 100Gbps에서는 약 0.12µs가 걸립니다. 반대로 64바이트(512비트)짜리 작은 RPC 요청은 10Gbps 링크에서 채 0.1µs도 걸리지 않습니다. 이 계산이 중요한 이유는, 대역폭을 올리는 것이 직렬화 지연은 줄여 주지만 전파 지연에는 전혀 영향을 주지 않는다는 것을 수치로 보여 주기 때문입니다.

### 큐잉 지연과 처리 지연

**큐잉 지연(queuing delay)**은 패킷이 스위치·라우터·NIC 링 버퍼에서 다른 트래픽에 밀려 대기하는 시간이고, **처리 지연(processing delay)**은 커널 네트워크 스택과 애플리케이션이 패킷 헤더를 해석하고 데이터를 전달하는 데 걸리는 시간입니다. 이 둘은 전파·직렬화 지연과 달리 물리 법칙이 아니라 시스템 상태(부하, 큐 깊이, 인터럽트 처리 방식, 스케줄러 정책 등 커널·드라이버 구현에 따라 달라지는 값)에 좌우되며, 트래픽이 몰릴 때 크게 늘어나고 지터(jitter)의 주된 원인이 됩니다.

네 지연을 하나의 흐름으로 보면 다음과 같습니다.

```mermaid
flowchart LR
  clientApp["클라이언트 애플리케이션"] --> clientNic["송신 NIC:</br>직렬화 지연"]
  clientNic --> wireOut["전송 매체:</br>전파 지연"]
  wireOut --> hop["스위치/라우터:</br>큐잉 + 처리 지연"]
  hop --> wireIn["전송 매체:</br>전파 지연"]
  wireIn --> serverNic["수신 NIC:</br>역직렬화"]
  serverNic --> serverApp["서버 애플리케이션 처리"]
  serverApp -->|"응답 경로(대칭 가정)"| clientApp
```

### 직접 측정하기: 루프백 RTT 벤치마크

수식으로 이해하는 것과 실제로 측정해 보는 것은 다릅니다. 아래는 루프백 TCP 에코 서버를 대상으로 왕복시간을 1000회 측정하고 p50/p95/p99을 출력하는 최소 클라이언트입니다. 서버는 `socat -u TCP-LISTEN:9000,reuseaddr,fork EXEC:/bin/cat` 같은 명령으로 대체할 수 있습니다.

```cpp
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <vector>

int main() {
  const int kIterations = 1000;
  const char payload[8] = "ping";
  char buf[8];

  int fd = socket(AF_INET, SOCK_STREAM, 0);
  sockaddr_in addr{};
  addr.sin_family = AF_INET;
  addr.sin_port = htons(9000);
  inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
  if (connect(fd, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) != 0) {
    perror("connect");
    return 1;
  }

  std::vector<double> rtts_us;
  rtts_us.reserve(kIterations);
  for (int i = 0; i < kIterations; ++i) {
    auto t0 = std::chrono::steady_clock::now();
    send(fd, payload, sizeof(payload), 0);
    recv(fd, buf, sizeof(buf), 0);
    auto t1 = std::chrono::steady_clock::now();
    rtts_us.push_back(std::chrono::duration<double, std::micro>(t1 - t0).count());
  }

  std::sort(rtts_us.begin(), rtts_us.end());
  auto pct = [&](double p) { return rtts_us[static_cast<size_t>(p * (rtts_us.size() - 1))]; };
  std::printf("p50=%.1fus p95=%.1fus p99=%.1fus\n", pct(0.50), pct(0.95), pct(0.99));
  close(fd);
  return 0;
}
```

`g++ -O2 -std=c++17 rtt_client.cpp -o rtt_client` (Linux 기준)로 빌드합니다. 루프백에서는 전파 지연이 사실상 0이므로 측정값은 커널 스택 처리 지연과 컨텍스트 스위칭 비용을 반영할 뿐, 실제 WAN 구간의 RTT를 대표하지 않습니다. 실제 두 호스트 간 RTT나 프로덕션 환경의 분포 분석은 [Tr.05 프로파일링·성능 분석](/post/profiling-analysis/getting-started-profiling-performance-analysis-fundamentals/)의 도구와 방법론을 따르는 것이 안전합니다. 참고로 일반적인 `ping` 출력은 다음과 같은 형태입니다(예시 값이며 실제 수치는 경로마다 다릅니다).

```text
$ ping -c 4 example.com
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=12.3 ms
64 bytes from 93.184.216.34: icmp_seq=2 ttl=56 time=11.9 ms
64 bytes from 93.184.216.34: icmp_seq=3 ttl=56 time=12.7 ms
64 bytes from 93.184.216.34: icmp_seq=4 ttl=56 time=12.1 ms
```

## 대역폭과 Bandwidth-Delay Product

**대역폭(bandwidth)**은 링크가 초당 실어 나를 수 있는 최대 비트 수이고, **처리량(throughput)**은 실제로 그 링크에서 관측되는 전송 속도입니다. 두 값은 자주 혼용되지만, 대역폭이 처리량의 상한선일 뿐 그 값을 보장하지는 않는다는 점이 다릅니다. 처리량이 대역폭에 못 미치는 가장 흔한 원인 중 하나가 바로 **Bandwidth-Delay Product(BDP)**입니다.

BDP는 "대역폭(bit/s) × RTT(s)"로 계산되며, 파이프를 쉬지 않고 채우기 위해 확인응답(ACK) 없이 동시에 전송 중이어야 하는 데이터량을 의미합니다. 예를 들어 10Gbps 링크에 대륙간 RTT 80ms를 대입하면 BDP는 10×10⁹ × 0.08 = 8×10⁸비트, 바이트로 환산하면 약 1억 바이트(약 95.4MiB)에 이릅니다. 문제는 TCP의 원래 윈도우 필드가 16비트라서 최대 64KiB밖에 표현하지 못한다는 점인데, 이 값은 방금 계산한 BDP의 1/1000도 되지 않습니다. 윈도우가 BDP보다 작으면 송신자는 ACK를 기다리느라 링크를 계속 놀리게 되고, 대역폭을 아무리 늘려도 처리량은 그대로입니다. 이 문제를 해결하는 윈도우 스케일링과 혼잡 제어의 구체적인 동작은 [03장: TCP 성능 최적화](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/)에서 다룹니다.

## 흔한 오개념 바로잡기

**"대역폭을 늘리면 지연이 줄어든다"**는 절반만 맞는 말입니다. 대역폭 증가는 직렬화 지연을 줄이고 BDP가 큰 대용량 전송의 처리량을 개선하지만, 전파 지연·큐잉 지연·처리 지연에는 영향을 주지 못합니다. 특히 페이로드가 수십~수백 바이트 수준인 RPC 호출에서는 직렬화 지연 자체가 RTT의 극히 일부에 불과하므로, 회선을 10배 빠른 것으로 바꿔도 체감 지연은 거의 변하지 않는 경우가 흔합니다.

**"직렬화 지연(serialization delay)과 (데이터) 직렬화 비용은 같은 개념이다"**도 흔한 혼동입니다. 이 장에서 다룬 직렬화 지연은 이미 만들어진 비트열을 링크에 밀어내는 물리 계층의 전송 시간을 가리키는 반면, "직렬화"라는 단어가 더 자주 쓰이는 맥락은 구조체를 바이트열로 인코딩·디코딩하는 애플리케이션 레벨 비용입니다. 후자는 Protocol Buffers·FlatBuffers·Cap'n Proto의 CPU 비용을 비교하는 [05장: 직렬화 성능 비교](/post/network-optimization/serialization-performance-protobuf-flatbuffers-capnproto/)의 주제이며, 이 장의 "직렬화 지연"과는 완전히 다른 계층의 이야기입니다.

**"ping의 RTT가 곧 애플리케이션이 체감하는 지연이다"**라는 가정도 위험합니다. ICMP echo는 커널이 최소한의 처리만으로 즉시 응답하지만, 실제 애플리케이션 요청은 TLS 핸드셰이크([16장](/post/network-optimization/tls-ssl-handshake-optimization-pqc/)), 연결 수립·재사용 정책([17장](/post/network-optimization/connection-pooling-keep-alive-reuse-strategy/)), gRPC 등 RPC 프레임워크의 직렬화·역직렬화([14장](/post/network-optimization/grpc-performance-tuning-optimization/))처럼 여러 단계를 추가로 거칩니다. `ping`이 보여 주는 것은 어디까지나 네트워크 경로의 하한선이지, 애플리케이션이 실제로 체감하는 지연의 전부가 아닙니다.

## 병목을 진단하는 판단 기준

지연 문제를 접했을 때 어떤 구성 요소가 지배적인지 좁히는 것이 최적화 방향을 정하는 첫걸음입니다.

| 증상 | 의심되는 지배 요인 | 확인 방법 | 관련 챕터 |
|------|-------------------|-----------|-----------|
| 페이로드 크기를 줄여도 지연이 거의 그대로 | 전파 지연(거리) 또는 왕복 횟수 | `traceroute`로 홉 수·경로 확인, RTT 요청 횟수 세기 | [17장](/post/network-optimization/connection-pooling-keep-alive-reuse-strategy/), [09장](/post/network-optimization/message-framing-length-prefix-delimiter-fixed-size/) |
| 페이로드가 커질수록 지연이 선형에 가깝게 증가 | 직렬화(전송) 지연 | 위 `serialization_delay_sec` 계산과 실측 비교 | [09장](/post/network-optimization/message-framing-length-prefix-delimiter-fixed-size/), [21장](/post/network-optimization/network-compression-lz4-zstd-snappy-tradeoffs/) |
| RTT는 낮은데 대용량 전송 처리량이 기대에 못 미침 | 윈도우 부족(BDP 대비) | `ss -i`로 소켓 윈도우·재전송 확인 | [02장](/post/network-optimization/socket-options-tcp-nodelay-buffer-tuning/), [03장](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/) |
| 지연이 들쭉날쭉하고 부하가 늘 때 더 심해짐 | 큐잉 지연·지터 | 부하 구간별 RTT 분포(p50 대비 p99) 비교 | [Tr.05 프로파일링](/post/profiling-analysis/linux-perf-advanced/) |
| 연결마다 첫 요청만 유독 느림 | 핸드셰이크(TCP+TLS) 비용 | 첫 요청과 후속 요청의 RTT 배수 비교 | [16장](/post/network-optimization/tls-ssl-handshake-optimization-pqc/), [17장](/post/network-optimization/connection-pooling-keep-alive-reuse-strategy/) |

## 비판적 시각: 단순 모델의 한계

이 장에서 다룬 "RTT = 전파 + 직렬화 + 큐잉 + 처리"라는 분해는 의도적으로 단순화한 정신 모델입니다. 실제 네트워크에서는 왕복 경로가 비대칭적으로 라우팅되어 왕복 각 방향의 지연 구성비가 다를 수 있고, TCP 재전송이나 혼잡 제어 알고리즘의 개입이 지연에 비선형적인 영향을 주며, 멀티패스·로드밸런서 뒤에서는 같은 목적지라도 매 요청마다 다른 경로를 탈 수 있습니다. 이 단순 모델로 병목의 "종류"를 추정하는 것은 유효하지만, 정확한 수치를 예측하는 용도로 쓰면 실제 측정과 어긋나기 쉽습니다.

"지연은 결국 빛의 속도가 지배한다"는 말도 절반만 맞습니다. 대륙간 통신처럼 거리가 지배적인 경로에서는 사실이지만, 같은 데이터센터 안이나 마이크로서비스 간 호출에서는 커널 네트워크 스택 처리, 애플리케이션 직렬화, 스레드 스케줄링 지연이 전파 지연보다 훨씬 큰 비중을 차지하는 경우가 많습니다. 이런 환경에서 "물리적으로 더 가깝게 배치"하는 시도는 실제 병목을 놓치게 만들 수 있으며, 이 장의 계산만으로 결론을 내리지 말고 실제 프로파일링으로 확인해야 합니다.

## 마무리

이 장을 통해 다음을 확인할 수 있어야 합니다.

- [ ] RTT를 구성하는 전파·직렬화·큐잉·처리 지연을 각각 설명하고, 어떤 것이 물리 법칙에 의해 고정되고 어떤 것이 시스템 상태에 좌우되는지 구분할 수 있다.
- [ ] 패킷 크기와 링크 대역폭으로 직렬화 지연을 직접 계산할 수 있고, 이 값이 RTT 전체에서 차지하는 비중이 상황마다 크게 다르다는 것을 안다.
- [ ] Bandwidth-Delay Product를 계산하고, 이 값이 TCP 윈도우 크기·처리량과 어떤 관계에 있는지 설명할 수 있다.
- [ ] "직렬화 지연"과 "데이터 직렬화 비용"이 서로 다른 계층의 개념임을 구분할 수 있다.
- [ ] 증상만 보고 병목 후보(거리·직렬화·윈도우·큐잉·핸드셰이크)를 좁히는 진단 표를 실제 상황에 적용할 수 있다.

**이전 장**: [HTTP/2와 HTTP/3](/post/network-optimization/http2-http3-multiplexing-quic-comparison/) (챕터 19). 다만 이 장은 커리큘럼상 진입점 역할도 겸하므로, 트랙을 처음 읽는다면 01장보다 먼저 이 장을 봐도 무방합니다.

다음 장에서는 지금까지 다진 지연 직관을 바탕으로, 페이로드 크기를 줄여 직렬화 지연과 대역폭 사용량을 함께 낮추는 실무 기법을 다룹니다. LZ4·zstd·Snappy 같은 압축 알고리즘이 CPU 비용과 전송 비용을 어떻게 맞바꾸는지, 그리고 이 트레이드오프를 지연 예산 안에서 어떻게 선택할지 살펴봅니다.

→ [21장: 네트워크 압축 전략](/post/network-optimization/network-compression-lz4-zstd-snappy-tradeoffs/)
