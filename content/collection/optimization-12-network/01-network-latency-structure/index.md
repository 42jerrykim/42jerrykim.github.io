---
collection_order: 1
date: 2026-07-14
lastmod: 2026-07-14
draft: false
image: wordcloud.png
title: "[Network 12] 네트워크 지연 구조"
slug: network-latency-structure-components
description: "네트워크 지연시간을 전파·전송·처리·큐잉 네 요소로 분해하고 각 요소의 물리적 근거와 계산식을 정리합니다. WAN·데이터센터·혼잡 액세스 링크 등 환경별로 어떤 성분이 지배적인지 판단하는 기준과 흔한 오개념, 이론치와 실측의 간극을 함께 다룹니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - Networking(네트워킹)
  - Latency
  - Throughput
  - Benchmark
  - Profiling(프로파일링)
  - System-Design
  - OS(운영체제)
  - Linux(리눅스)
  - Backend(백엔드)
  - Reliability
  - Scalability(확장성)
  - Comparison(비교)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Hardware(하드웨어)
  - Deep-Dive
  - Advanced
  - C++
  - C
  - IO(Input/Output)
  - Case-Study
  - Documentation(문서화)
  - Guide(가이드)
  - Reference(참고)
  - Implementation(구현)
  - Best-Practices
  - RTT
  - Propagation-Delay
  - Transmission-Delay
  - Processing-Delay
  - Queuing-Delay
  - Queueing-Theory
  - Bandwidth-Delay-Product
  - Kleinrock
---

**네트워크 지연 구조**란 패킷 하나가 송신 호스트를 떠나 수신 호스트에 도착하기까지 걸리는 시간을 전파 지연(propagation delay), 전송 지연(transmission delay), 처리 지연(processing delay), 큐잉 지연(queueing delay) 네 성분으로 분해해 보는 관점을 말합니다. 이 분해가 필요한 이유는 실무에서 마주치는 지연 문제 대부분이 네 성분 중 하나에 집중되어 있는데, 어떤 성분이 지배적인지 모른 채 소켓 옵션이나 커널 파라미터부터 건드리면 노력 대비 효과가 거의 없는 튜닝을 반복하게 되기 때문입니다. 대륙 간 통신에서 버퍼 크기를 늘려봐야 전파 지연은 줄지 않고, 데이터센터 내부 통신에서 회선 배치를 바꿔봐야 처리·큐잉 지연은 그대로입니다. 이 장은 그 판단의 출발점이 되는 네 성분의 정의와 상대적 비중을 정리합니다.

## 이 장을 읽기 전에

**선행 자료**: 이 트랙의 [Introduction: Low-latency 네트워크 최적화](/post/network-optimization/getting-started-network-performance-tuning/)에서 트랙 전체 범위와 진입 순서를 먼저 확인하세요. 별도의 선행 챕터는 없으며, 이 장이 트랙의 실질적인 첫 본문입니다.

**전제 지식**: OSI/TCP-IP 계층 구조에 대한 기초적인 감각(패킷이 링크·라우터를 거쳐 전달된다는 정도)이면 충분합니다. 큐잉 이론의 수식을 미리 알 필요는 없습니다.

**이 장의 깊이**: 이 장은 **기초** 난이도로, 네 지연 성분의 정의·계산식·상대적 비중을 다룹니다. 각 성분을 실제로 줄이는 구체적인 기법(소켓 옵션, 혼잡 제어, 직렬화 포맷, 커널 바이패스)은 여기서 다루지 않고 해당 챕터로 위임합니다.

**다루지 않는 것**: TCP_NODELAY·버퍼 크기 등 소켓 옵션 튜닝(→ [02장](/post/network-optimization/socket-options-tcp-nodelay-buffer-tuning/)), Nagle·혼잡 제어·BBR(→ [03장](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/)), UDP 신뢰성 계층 설계(→ [04장](/post/network-optimization/udp-optimization-reliability-layer-design/)), 직렬화 포맷별 처리 비용 비교(→ [05장](/post/network-optimization/serialization-performance-protobuf-flatbuffers-capnproto/)), 프로토콜·프레이밍 설계(→ [08장](/post/network-optimization/low-latency-binary-protocol-design-principles/)), RTT·대역폭에 대한 직관적 감 잡기(→ [20장](/post/network-optimization/network-latency-intuition-rtt-bandwidth-fundamentals/))입니다. 이 장은 그 모든 구체적 기법이 "결국 어느 지연 성분을 겨냥하는가"를 판단하는 틀을 제공합니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "네 가지 지연 성분" ~ "각 성분의 계산식" | 전파·전송·처리·큐잉 지연을 구분하고 정의할 수 있다 |
| **중급자** | "환경별 상대적 비중" ~ "판단 기준" | 상황(WAN/LAN/데이터센터)에 따라 어떤 성분이 지배적인지 판단할 수 있다 |
| **전문가** | "흔한 오개념" ~ "비판적 시각" | 이론적 모델과 실측치의 괴리, 큐잉 지연의 비선형성을 설명할 수 있다 |

---

## 역사·배경: 지연을 성분으로 쪼개는 관점

패킷 지연을 성분별로 분해하는 접근은 컴퓨터 네트워킹 교재에서 공통적으로 쓰는 표준 모델이며, 그 이론적 뿌리는 1960년대 초 회선이 아닌 **메시지(패킷) 단위 교환망의 지연을 큐잉 이론으로 분석**한 연구로 거슬러 올라갑니다. Leonard Kleinrock은 1961년 MIT 박사논문 제안서에서 메시지를 작은 조각으로 나누어 전달하는 방식을 처음으로 분석했고, 1962년 박사논문 "Message Delay in Communication Nets with Storage"에서 저장 후 전달(store-and-forward) 방식 통신망의 메시지 지연을 큐잉 이론으로 정식화했습니다. 이 작업은 1964년 저서로 출간되었고, Donald Davies가 1966년 이 기법을 실제 패킷 교환망 설계에 적용하면서 이론이 실무로 넘어왔습니다. 이후 ARPANET 설계에 이 큐잉 이론이 직접 반영되었습니다.

지금 통용되는 "전파-전송-처리-큐잉" 4성분 분해는 이 큐잉 이론 전통을 라우터 한 홉(hop)의 지연 모델로 정리한 것입니다. 한 홉을 지나는 총 지연은 $d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$로 표현됩니다. 같은 큐잉 이론 전통은 패킷 교환망의 종단 지연 근사 연구에서도 이어지는데, Kleinrock의 독립성 가정(independence assumption)과 위상형(phase-type) 분포를 이용해 홉을 거친 종단 지연을 근사하는 접근이 그 예입니다([End-to-End Delay Approximation in Packet-Switched Networks, arXiv:2003.08780](https://arxiv.org/pdf/2003.08780)). 여러 홉을 거치는 종단 간(end-to-end) 지연은 이 네 성분을 홉 수만큼 더한 값에 가깝습니다.

## 네 가지 지연 성분

### 전파 지연 (Propagation Delay)

**전파 지연**은 신호가 물리 매체(구리선·광섬유·무선)를 통과하는 데 걸리는 시간으로, 매체의 길이를 신호 전파 속도로 나눈 값입니다. 신호는 진공 중 광속(약 $3 \times 10^8$ m/s)보다 느리게 이동하며, 표준 단일모드 광섬유의 굴절률은 약 1.468이라서 실제 전파 속도는 진공 광속의 약 3분의 2 수준인 약 $2 \times 10^8$ m/s입니다. 이를 환산하면 광섬유 1km를 통과하는 데 대략 4.9µs가 걸립니다. 전파 지연은 **매체의 물리적 길이에만 비례**하고 대역폭·트래픽 양과는 무관하므로, 서버 스펙을 아무리 올려도 줄지 않습니다. 유일한 개선 수단은 거리 자체를 줄이는 것(엣지 로케이션, CDN, 지리적으로 가까운 리전 선택)입니다.

전파 지연을 "직선거리 ÷ 광속"으로 계산하면 실측치보다 낙관적인 값이 나오는 경우가 흔합니다. 미국 내 120개 주요 인구 중심지 간 광섬유 경로를 분석한 연구는, 실제 회선이 직선 경로가 아니라 기존 도로·철도망을 따라 깔리기 때문에 "직선거리 × 2.1 ÷ 광속"이 관행적인 추정 방식이었다고 보고합니다. 이 연구는 회선 배치를 최적화하면 이 계수를 중앙값 1.3까지 낮출 여지가 있다고 계산했지만, 동시에 실제 CDN·백본 사업자의 지연이 케이블 길이만으로 예측한 값보다 훨씬 높은 경우가 많다는 점도 함께 보고합니다([Dissecting Latency in the Internet's Fiber Infrastructure, arXiv:1811.10737](https://arxiv.org/pdf/1811.10737)). 즉 전파 지연의 "이론적 하한"과 "실제 관측값" 사이에는 회선 경로의 우회, 중계 장비, 라우팅 정책이 만드는 상당한 간극이 있습니다.

### 전송 지연 (Transmission Delay)

**전송 지연**은 패킷의 모든 비트를 링크에 밀어 넣는 데 걸리는 시간으로, 패킷 크기(비트)를 링크 대역폭(bps)으로 나눈 값입니다. 1500바이트(12000비트) 패킷을 1Gbps 링크에 실으면 약 12µs, 10Gbps 링크에서는 약 1.2µs, 100Gbps 링크에서는 약 0.12µs가 걸립니다. 전송 지연은 **대역폭이 커질수록 선형적으로 줄어들며**, 전파 지연과 달리 링크 자체의 물리적 길이와는 무관합니다. 저대역폭 액세스 회선(가정용 인터넷, 위성 백홀 등)에서는 전송 지연이 무시하기 어려운 비중을 차지하지만, 데이터센터 내부의 10~400Gbps급 링크에서는 개별 패킷의 전송 지연이 수백 나노초~수 마이크로초 수준으로 작아져 다른 성분에 비해 상대적으로 덜 중요해집니다. 페이로드 크기 자체를 줄이는 직렬화·압축 선택은 전송 지연에 직접 영향을 주며, 이 트레이드오프는 [05장](/post/network-optimization/serialization-performance-protobuf-flatbuffers-capnproto/)과 [21장](/post/network-optimization/network-compression-lz4-zstd-snappy-tradeoffs/)에서 다룹니다.

### 처리 지연 (Processing Delay)

**처리 지연**은 라우터·스위치·수신 호스트가 패킷 헤더를 검사하고 체크섬을 검증하고 다음 홉을 결정하는 데 걸리는 시간입니다. 하드웨어 포워딩 경로를 쓰는 전용 라우터·스위치에서는 이 지연이 수백 나노초 이하로 매우 작지만, 범용 OS의 네트워크 스택을 거치는 종단 호스트에서는 이야기가 달라집니다. 시스템 콜 진입, 컨텍스트 스위치, 커널 내부 버퍼 복사, 소켓 계층의 락 경합이 누적되면 애플리케이션이 체감하는 처리 지연이 수 마이크로초에서 수십 마이크로초까지 늘어날 수 있습니다. 이 비용은 패킷 크기나 링크 거리와 무관하게 **호스트당 고정 비용에 가깝다는 점**이 전파·전송 지연과 다른 특징입니다. 커널 네트워크 스택을 우회해 이 처리 지연을 줄이는 기법(DPDK, XDP/eBPF)은 [10장](/post/network-optimization/dpdk-advanced-deep-dive-smartnic-dpu/)과 [11장](/post/network-optimization/xdp-ebpf-network-packet-processing-advanced/)에서 심화하며, 그 개요는 Tr.07의 [커널 바이패스 개요](/post/os-optimization/kernel-bypass-overview/)를 참고하세요.

### 큐잉 지연 (Queueing Delay)

**큐잉 지연**은 패킷이 링크로 전송되기 전에 라우터·스위치·NIC의 출력 버퍼에서 대기하는 시간입니다. 다른 세 성분과 달리 큐잉 지연은 **링크 자체의 물리적 특성이 아니라 그 순간의 트래픽 부하에 의해 결정**됩니다. 링크 이용률(utilization) $\rho$가 낮을 때는 대기가 거의 없지만, $\rho$가 1에 가까워질수록 대기 시간은 완만하지 않고 급격히(비선형적으로) 늘어납니다. 가장 단순한 M/M/1 큐잉 모델에서 평균 대기 시간은 $\rho / (1-\rho)$에 비례하는 형태를 띠므로, 이용률이 90%에서 95%로 늘어나는 것만으로도 평균 대기 시간이 대략 두 배가 됩니다. 실제 네트워크 트래픽은 M/M/1이 가정하는 포아송 도착과 다르게 버스트성(bursty)이 강해서, 평균 이용률이 낮아 보여도 순간적인 버스트가 큐를 채워 꼬리 지연(p99·p999)을 크게 키우는 경우가 흔합니다. 이 특성 때문에 큐잉 지연은 네 성분 중 가장 예측하기 어렵고, 혼잡 제어·버퍼 크기 조정으로 직접 다루는 영역은 [03장](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/)에서 심화합니다.

패킷 하나가 여러 홉을 거치는 경로 전체의 지연을 그림으로 보면 다음과 같습니다. 각 홉마다 전송·전파 지연이 링크에서, 처리·큐잉 지연이 노드(라우터)에서 발생합니다.

```mermaid
flowchart LR
  client["송신 호스트"] -->|"전송 지연 dTrans"| link1["링크 1"]
  link1 -->|"전파 지연 dProp"| router["라우터/스위치"]
  router -->|"처리 지연 dProc"| queue["출력 버퍼"]
  queue -->|"큐잉 지연 dQueue"| link2["링크 2"]
  link2 -->|"전파 지연 dProp"| server["수신 호스트"]
```

## 환경별 상대적 비중

네 성분의 절대 크기는 환경에 따라 자릿수 단위로 달라지므로, "어느 성분이 지배적인가"라는 질문의 답은 매번 다시 확인해야 합니다. 대략적인 감을 잡는 데는 잘 알려진 순서-크기 비교표가 유용합니다. 같은 데이터센터 내부 왕복은 대략 500µs, 캘리포니아와 네덜란드 간 왕복은 대략 150ms 수준이며 이 차이의 근본 원인은 광속이라는 물리적 제약이라는 점이 반복적으로 확인되어 왔습니다([Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html)). 이 수치는 하드웨어 세대에 따라 계속 바뀌므로 절대값 자체보다는 "물리 거리가 지배하는 구간"과 "그렇지 않은 구간"을 구분하는 감각으로 활용하는 편이 안전합니다.

| 환경 | 지배적 성분 | 근거 |
|------|-----------|------|
| 대륙 간 WAN 통신 | 전파 지연 | 거리가 수천 km이므로 광속 제약이 다른 성분을 압도 |
| 혼잡한 액세스 링크(가정용 회선 등) | 큐잉 지연 | 이용률이 높은 구간에서 버퍼 대기가 급격히 증가(bufferbloat) |
| 데이터센터 내부(수 µs~수백 µs RTT) | 처리·큐잉 지연 | 거리가 짧아 전파 지연은 무시할 만하고, 커널 스택·버퍼 경합이 상대적으로 부각 |
| 저대역폭 위성/모바일 백홀 | 전송 지연 + 전파 지연 | 대역폭이 낮아 개별 패킷 전송 시간 자체가 크고, 위성 구간은 거리도 김 |
| 초고대역폭 백본(100Gbps+) 소규모 패킷 | 처리 지연 | 전송 지연이 나노초 단위로 작아져 라우터 처리 비용이 상대적으로 부각 |

실측으로 이 표를 검증하고 싶다면, 지연 성분 자체보다 왕복 시간의 분포(p50/p95/p99)를 먼저 재는 것이 순서입니다. 아래는 루프백 또는 같은 서브넷 대상으로 TCP 왕복 시간을 반복 측정해 최소값·중앙값·p95를 뽑는 최소 골격입니다. 실제 값은 OS, NIC, 커널 버전, 방화벽·NAT 유무에 따라 달라지므로 절대 수치가 아니라 성분 구분의 출발점으로만 사용합니다.

```c
// rtt_probe.c — 지정한 호스트:포트로 짧은 TCP 연결을 반복해 왕복 시간을 측정한다.
// 빌드: gcc -O2 -o rtt_probe rtt_probe.c
// 실행: ./rtt_probe 127.0.0.1 7 200   (호스트, 포트, 반복 횟수)
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

static double now_us(void) {
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return ts.tv_sec * 1e6 + ts.tv_nsec / 1e3;
}

static int cmp_double(const void* a, const void* b) {
  double d = *(const double*)a - *(const double*)b;
  return d < 0 ? -1 : d > 0 ? 1 : 0;
}

int main(int argc, char** argv) {
  const char* host = argc > 1 ? argv[1] : "127.0.0.1";
  int port = argc > 2 ? atoi(argv[2]) : 7;
  int iters = argc > 3 ? atoi(argv[3]) : 200;
  struct sockaddr_in addr = {0};
  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  inet_pton(AF_INET, host, &addr.sin_addr);

  double* samples = malloc(sizeof(double) * iters);
  int ok = 0;
  for (int i = 0; i < iters; i++) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    int one = 1;
    setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &one, sizeof(one));  // Nagle 영향 배제
    double t0 = now_us();
    if (connect(fd, (struct sockaddr*)&addr, sizeof(addr)) == 0) {
      samples[ok++] = now_us() - t0;  // 핸드셰이크 왕복(전파+처리+큐잉)만 측정
    }
    close(fd);
  }
  qsort(samples, ok, sizeof(double), cmp_double);  // p50/p95 추출을 위한 정렬
  printf("n=%d min=%.1fus p50=%.1fus p95=%.1fus\n", ok, samples[0],
         samples[ok / 2], samples[(int)(ok * 0.95)]);
  free(samples);
  return 0;
}
```

이 코드는 TCP 3-way handshake 하나의 왕복 시간만 재므로, 실제 애플리케이션 메시지의 왕복 시간에는 페이로드 크기에 따른 전송 지연과 애플리케이션 처리 시간이 추가로 얹힙니다. 표본 수가 적으면 p95·p99가 튀는 값 하나에 크게 흔들리므로 최소 수백~수천 회 반복하고, 결과가 방화벽·conntrack 상태에 영향을 받을 수 있다는 점도 감안해야 합니다.

## 흔한 오개념

**"지연시간은 결국 대역폭 문제다"**: 대역폭을 올리면 전송 지연은 줄지만 전파 지연과 처리 지연은 전혀 줄지 않습니다. 대륙 간 통신처럼 전파 지연이 지배적인 구간에서는 회선을 10배 넓혀도 왕복 시간이 거의 그대로입니다. 어느 성분이 병목인지 먼저 확인하지 않고 대역폭부터 늘리는 것은 흔한 낭비입니다.

**"직선거리로 전파 지연을 정확히 예측할 수 있다"**: 실제 광섬유 회선은 도로·철도·기존 공동구를 따라 깔리므로 직선 경로가 아닙니다. 앞서 인용한 연구처럼 실제 회선 길이가 직선거리의 1.3~2.1배에 이르는 경우가 흔하고, 여기에 중계 장비(리제너레이터, EDFA)의 처리 지연까지 더해지므로 "직선거리 ÷ 광속"은 하한선이지 예측값이 아닙니다.

**"큐잉 지연은 링크 용량이 충분하면 항상 작다"**: 평균 이용률이 낮아도 순간적인 트래픽 버스트가 출력 버퍼를 채우면 큐잉 지연이 급격히 튑니다. 평균만 보고 여유가 있다고 판단하면 p99 지연에서 예상치 못한 급증을 겪게 되며, 이 비선형성은 이용률이 임계점(대략 80~90% 이상)을 넘는 순간부터 두드러집니다.

## 판단 기준

| 관찰된 증상 | 우선 의심할 성분 | 다음 행동 |
|------------|----------------|----------|
| 지리적으로 먼 리전과 통신 시 RTT가 크고 일정함 | 전파 지연 | 대역폭 튜닝 대신 지리적 배치(엣지/CDN/리전 선택) 검토 |
| 부하가 낮을 때는 빠르지만 트래픽이 몰리면 p99가 급증 | 큐잉 지연 | 버퍼·혼잡 제어 튜닝([03장](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/)) |
| 대용량 페이로드 전송 시에만 지연이 큼 | 전송 지연 | 직렬화 크기 축소·압축 검토([05장](/post/network-optimization/serialization-performance-protobuf-flatbuffers-capnproto/), [21장](/post/network-optimization/network-compression-lz4-zstd-snappy-tradeoffs/)) |
| 짧은 메시지를 자주 주고받을 때 호스트 측 오버헤드가 큼 | 처리 지연 | 소켓 옵션([02장](/post/network-optimization/socket-options-tcp-nodelay-buffer-tuning/)), 커널 바이패스([10장](/post/network-optimization/dpdk-advanced-deep-dive-smartnic-dpu/)/[11장](/post/network-optimization/xdp-ebpf-network-packet-processing-advanced/)) 검토 |
| 어떤 성분인지 감이 안 잡힘 | 측정 부재 | 성분별로 분리 측정하기 전에는 어떤 튜닝도 추측일 뿐 |

## 비판적 시각: 한계와 트레이드오프

4성분 분해는 한 홉의 지연을 설명하는 데는 유용하지만, 실제 종단 간 경로는 수십 개의 홉과 다양한 미들박스(방화벽, NAT, 로드밸런서)를 거치며 각 홉의 성분이 독립적이지 않고 서로 상호작용합니다. 특히 TCP의 재전송·혼잡 제어는 큐잉 지연과 강하게 얽혀 있어서, 큐잉 지연이 늘면 재전송이 늘고 재전송이 다시 큐를 채우는 되먹임 구조가 생깁니다. 이 상호작용은 [03장](/post/network-optimization/tcp-performance-nagle-congestion-control-bbr/)에서 다루는 혼잡 제어 알고리즘의 영역이며, 4성분 모델만으로는 설명되지 않습니다. 또한 이 모델은 정적인 스냅샷이라서, 실제 트래픽 패턴(자기 유사성·버스트성)이 M/M/1 같은 단순 큐잉 모델의 가정을 자주 벗어난다는 점도 감안해야 합니다. 마지막으로, 환경별 상대적 비중 표는 일반적인 경향일 뿐 특정 배포 환경에서 그대로 성립한다는 보장이 없으므로, 실제 의사결정 전에는 반드시 해당 환경에서 직접 측정해야 합니다. 이 측정 방법론 자체는 Tr.05의 [프로파일링·성능 분석 개요](/post/profiling-analysis/getting-started-profiling-performance-analysis-fundamentals/)에서 더 다룹니다.

## 마무리

이 장을 통해 다음을 할 수 있어야 합니다.

- [ ] 전파·전송·처리·큐잉 네 지연 성분을 각각 정의하고 계산식을 쓸 수 있다.
- [ ] 환경(WAN/혼잡 액세스 링크/데이터센터/저대역폭 백홀)에 따라 지배적 성분이 달라짐을 설명할 수 있다.
- [ ] 큐잉 지연이 트래픽 부하에 비선형적으로 반응하는 이유를 설명할 수 있다.
- [ ] 이론적 전파 지연 하한과 실측치 사이에 간극이 생기는 이유를 설명할 수 있다.
- [ ] 증상만 보고 어느 성분을 먼저 프로파일링해야 하는지 판단할 수 있다.

**다음 장에서는** 이 네 성분 중 호스트 측 처리 지연과 관련이 깊은 소켓 계층으로 내려갑니다. `TCP_NODELAY`, `SO_SNDBUF`/`SO_RCVBUF` 같은 옵션이 실제로 어느 지연 성분에 영향을 주는지, 그리고 버퍼 크기 조정이 전송 지연·큐잉 지연과 어떻게 얽히는지를 다룹니다.

→ [소켓 옵션 튜닝](/post/network-optimization/socket-options-tcp-nodelay-buffer-tuning/)
