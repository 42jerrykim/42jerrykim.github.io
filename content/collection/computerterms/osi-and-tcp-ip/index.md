---
image: "wordcloud.png"
slug: osi-and-tcp-ip
collection_order: 11
draft: false
title: "[Computer Terms] OSI 7계층과 TCP/IP"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "OSI 7계층 모델과 실제 인터넷을 움직이는 TCP/IP 4계층을 비교하고, TCP의 3-way handshake와 UDP의 차이를 실제 소켓 통신 흐름으로 다룹니다. 계층이 나뉘는 이유와 각 계층의 역할을 컴파일 가능한 C 코드와 함께 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Networking(네트워킹)
- OSI(OSI모델)
- TCP-IP
- Protocol(프로토콜)
- Socket(소켓)
- Time-Complexity(시간복잡도)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Debugging(디버깅)
- Performance(성능)
- Distributed-Systems(분산시스템)
- Web(웹)
- Security(보안)
---

## 이 장을 읽기 전에

이전 자료구조 갈래([배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/) ~ [그래프](/post/computerterms/graphs/))와 별개의 새 갈래(시스템)로, "데이터를 어떤 모양으로 들고 있는가"가 아니라 "여러 컴퓨터가 어떻게 데이터를 주고받는가"를 다룬다. 선행 지식 없이 읽을 수 있지만, 뒤에서 다룰 소켓 프로그래밍과 로드밸런싱은 이 챕터의 계층 개념을 전제로 한다.

## 왜 계층으로 나누는가

두 컴퓨터가 통신하려면 "전기 신호를 어떻게 주고받을지"부터 "받은 데이터가 어떤 의미인지"까지 수많은 문제를 풀어야 한다. 이를 하나의 거대한 규약으로 만들면 회선 종류가 바뀔 때마다 애플리케이션까지 전부 다시 설계해야 한다. **OSI 7계층 모델**은 이 문제를 물리(1)·데이터링크(2)·네트워크(3)·전송(4)·세션(5)·표현(6)·응용(7) 계층으로 나눠, 각 계층이 바로 아래 계층의 세부 구현을 몰라도 되게 만든다. 예를 들어 응용 계층의 HTTP는 그 아래가 이더넷인지 와이파이인지 신경 쓰지 않는다.

## OSI는 이론, TCP/IP는 실제

실제 인터넷을 움직이는 것은 OSI 7계층이 아니라 더 단순한 **TCP/IP 4계층**(네트워크 인터페이스 · 인터넷 · 전송 · 응용)이다. OSI의 세션·표현·응용 계층은 TCP/IP에서 응용 계층 하나로 합쳐진다. OSI가 여전히 교육·설계 논의에서 쓰이는 이유는, "이 문제가 몇 계층 문제인가"를 짚는 공용 어휘로서 유용하기 때문이다 — 예를 들어 "이건 3계층 라우팅 문제"라고 하면 IP 주소·경로 설정 범위의 문제임이 바로 전달된다.

| OSI 계층 | 역할 | TCP/IP 대응 | 대표 프로토콜/장비 |
|---|---|---|---|
| 7. 응용 | 사용자 데이터 형식 | 응용 계층 | HTTP, DNS, SMTP |
| 4. 전송 | 종단 간 신뢰성·순서 보장 | 전송 계층 | TCP, UDP |
| 3. 네트워크 | 경로 설정, 주소 지정 | 인터넷 계층 | IP, 라우터 |
| 2. 데이터링크 | 같은 네트워크 내 프레임 전달 | 네트워크 인터페이스 | 이더넷, 스위치 |
| 1. 물리 | 전기·광 신호 | 네트워크 인터페이스 | 케이블, 허브 |

## 전송 계층의 선택: TCP vs UDP

응용 프로그램을 만들 때 실질적으로 가장 자주 마주치는 판단은 전송 계층에서 **TCP**를 쓸지 **UDP**를 쓸지다. TCP는 데이터를 보내기 전에 **3-way handshake**(SYN → SYN-ACK → ACK)로 연결을 맺고, 패킷 순서와 손실 재전송을 보장한다. 웹 페이지 로딩처럼 데이터가 하나라도 빠지면 안 되는 경우에 적합하다. UDP는 이 핸드셰이크와 재전송 보장이 없다 — 대신 오버헤드가 적어, 실시간 영상 스트리밍이나 온라인 게임처럼 "약간의 손실보다 지연이 더 치명적인" 경우에 쓴다.

```c
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

/* TCP 클라이언트 최소 예제: 연결 → 전송 → 수신 → 종료 */
int main(void) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);   /* SOCK_STREAM = TCP */
    if (sock < 0) { perror("socket"); return 1; }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    /* connect()가 내부적으로 3-way handshake를 수행한다 */
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sock);
        return 1;
    }

    const char *msg = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n";
    send(sock, msg, strlen(msg), 0);

    char buffer[1024] = {0};
    recv(sock, buffer, sizeof(buffer) - 1, 0);
    printf("%s\n", buffer);

    close(sock);
    return 0;
}
```

이 코드에서 `SOCK_STREAM`을 `SOCK_DGRAM`으로, `connect()`+`send()`/`recv()`를 `sendto()`/`recvfrom()`으로 바꾸면 UDP 통신이 된다. 핵심 차이는 연결을 맺는 과정(`connect()`)의 유무이며, 이것이 TCP의 신뢰성 보장과 UDP의 낮은 오버헤드를 가르는 지점이다.

## 흔한 오개념

**"TCP가 항상 UDP보다 안전하니 무조건 TCP를 쓰면 된다"** — TCP의 재전송·순서 보장은 지연(latency)이라는 대가를 수반한다. 실시간 음성 통화에서 0.1초 전 패킷을 기다리는 것보다 그냥 버리고 다음 패킷을 재생하는 게 사용자 경험상 낫다 — 이런 상황에서 TCP를 쓰면 오히려 "안전하지만 쓸모없는" 지연이 발생한다.

**"IP 주소가 있으면 바로 통신할 수 있다"** — IP는 네트워크 계층(3계층)의 주소일 뿐이고, 실제 데이터 전달은 데이터링크 계층(2계층)의 MAC 주소를 알아야 완성된다. IP에서 MAC을 알아내는 과정(ARP)이 이 두 계층 사이에 있다는 것을 빼먹으면 "같은 네트워크인데 왜 라우터를 거치나" 같은 혼란이 생긴다.

## 다른 개념과의 연결

다음 챕터에서 다룰 [HTTP와 HTTPS](/post/computerterms/http-and-https/)는 이 챕터의 응용 계층에 해당하며, TCP 위에서 동작한다(HTTPS는 TCP 위의 TLS 위에서 동작). [DNS](/post/computerterms/dns-and-sockets/)는 응용 계층 프로토콜이면서도 IP 주소 해석이라는 네트워크 계층의 문제를 푼다는 점에서 계층 경계가 실무에서는 엄격히 나뉘지 않음을 보여주는 예다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. OSI 7계층과 TCP/IP 4계층의 대응 관계를 설명할 수 있다. TCP와 UDP 중 주어진 상황(파일 전송 vs 실시간 스트리밍)에 맞는 프로토콜을 근거와 함께 선택할 수 있다. 3-way handshake가 무엇을 보장하기 위한 절차인지 설명할 수 있다.

## 참고 자료

> Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.), Chapter 1: Computer Networks and the Internet. Pearson.

- [RFC 793: Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc793) — TCP의 원 사양 문서, 3-way handshake 상태 머신 정의
- [MDN: Sockets and HTTP over TCP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) — 응용 계층 프로토콜이 전송 계층 위에서 동작하는 방식 개요
