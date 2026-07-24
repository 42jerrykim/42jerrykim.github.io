---
image: "wordcloud.png"
slug: load-balancing
collection_order: 27
draft: false
title: "[Computer Terms] 로드 밸런싱 (Load Balancing)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "로드 밸런싱은 하나의 서버로는 감당 못 할 트래픽을 여러 서버에 나눠 처리하는 기법입니다. 라운드 로빈·최소 연결·헬스 체크 알고리즘을 비교하고, L4/L7 계층 구분과 세션 고정 문제의 근본 해법까지 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Networking(네트워킹)
- Load-Balancing(로드밸런싱)
- Scalability(확장성)
- Distributed-Systems(분산시스템)
- HTTP
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
- Performance(성능)
- Reliability(신뢰성)
- Debugging(디버깅)
- Advanced
- How-To
- Tips
---

## 이 장을 읽기 전에

[프로세스와 스레드](/post/computerterms/processes-and-threads/)와 [DNS와 소켓](/post/computerterms/dns-and-sockets/)에서 다룬 "하나의 서버가 여러 연결을 어떻게 받는가"를 안다고 가정한다. 로드 밸런싱은 그 질문을 한 단계 확장해, "서버 한 대로 부족할 때 여러 대에 어떻게 나눠 줄 것인가"를 다룬다.

## 서버 한 대로는 왜 부족해지는가

[CPU 스케줄링](/post/computerterms/cpu-scheduling/)에서 다룬 대로 한 대의 서버가 동시에 처리할 수 있는 연결·요청 수는 CPU·메모리·네트워크 대역폭이라는 물리적 한계에 갇혀 있다. 트래픽이 이 한계를 넘으면 응답 지연이 커지거나 서버가 죽는다. **로드 밸런서(Load Balancer)**는 클라이언트와 서버 사이에 위치해, 들어오는 요청을 여러 서버(백엔드)로 분산시켜 이 한계를 넓힌다. 부가적으로 한 서버가 죽어도 로드 밸런서가 나머지 서버로만 트래픽을 보내 서비스 전체가 멈추지 않게 하는 **가용성** 효과도 있다.

## 분산 알고리즘: 누구에게 보낼 것인가

**라운드 로빈(Round Robin)**은 [CPU 스케줄링](/post/computerterms/cpu-scheduling/)에서 다룬 것과 이름은 같지만 대상이 다르다 — 서버 목록을 순서대로 돌아가며 요청을 하나씩 배정한다. 구현이 단순하지만, 서버마다 처리 시간이 다른 요청이 섞이면 특정 서버에 부하가 몰릴 수 있다. **최소 연결(Least Connections)**은 현재 처리 중인 연결이 가장 적은 서버로 보낸다 — 요청마다 처리 시간이 크게 다른 경우 라운드 로빈보다 균형이 잘 맞는다. **IP 해시(IP Hash)**는 클라이언트 IP를 해시해 항상 같은 서버로 보낸다 — [해시테이블](/post/computerterms/hash-tables/)의 해시 함수를 그대로 응용한 것으로, 같은 사용자가 매번 같은 서버로 연결되게 하려 할 때 쓴다.

```text
라운드 로빈:  요청1→서버A, 요청2→서버B, 요청3→서버C, 요청4→서버A, ...
최소 연결:    현재 연결 수(A:5, B:2, C:8) 중 가장 적은 B로 다음 요청 배정
IP 해시:      hash(클라이언트IP) % 서버수 → 항상 같은 서버로 고정
```

## 헬스 체크: 죽은 서버로 보내지 않기

분산 알고리즘만으로는 부족하다 — 서버 중 하나가 실제로 죽었는데도 그 서버로 계속 요청을 보내면 그 몫의 요청은 전부 실패한다. 로드 밸런서는 주기적으로 각 서버에 **헬스 체크(Health Check)** 요청(예: `GET /health`)을 보내 응답 여부를 확인하고, 응답하지 않는 서버는 분산 대상에서 즉시 제외한다. [CPU 스케줄링](/post/computerterms/cpu-scheduling/)의 라운드 로빈이 정적인 목록을 순회하는 것과 달리, 로드 밸런싱의 라운드 로빈은 이 헬스 체크로 목록 자체가 계속 갱신된다는 차이가 있다.

## 세션 고정 문제

[인증과 인가](/post/computerterms/authentication-and-authorization/)에서 다룬 세션 기반 인증을 여러 서버로 분산하면 새로운 문제가 생긴다. 로그인 시 서버 A가 세션을 만들어 자신의 메모리에 저장했는데, 다음 요청이 로드 밸런서에 의해 서버 B로 가면 서버 B는 그 세션을 모른다. 이 문제를 **세션 고정(Session Affinity, Sticky Session)**으로 완화할 수 있다 — 같은 클라이언트의 요청을 항상 같은 서버로 보내도록(위의 IP 해시가 이 목적으로도 쓰인다) 강제하는 것이다. 다만 이는 특정 서버에 부하가 쏠리는 문제와 상충하므로, 더 근본적인 해법은 세션 자체를 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 공유 키-값 저장소(Redis 등)로 옮겨 어느 서버가 요청을 받아도 같은 세션을 조회할 수 있게 만드는 것이다.

## 비교: 세 가지 분산 알고리즘

| 알고리즘 | 구현 복잡도 | 부하 균형 | 세션 고정 |
|---|---|---|---|
| 라운드 로빈 | 낮음 | 요청 처리 시간이 균일할 때만 좋음 | 불가능(매번 다른 서버) |
| 최소 연결 | 중간 | 처리 시간이 불균일해도 좋음 | 불가능 |
| IP 해시 | 낮음 | 클라이언트 분포에 따라 편차 가능 | 가능(같은 IP는 항상 같은 서버) |

## 흔한 오개념

**"로드 밸런서만 두면 서버를 무한히 늘려도 된다"** — 서버가 상태(세션, 로컬 캐시)를 갖고 있으면 서버를 늘려도 그 상태가 서버마다 흩어져 일관성 문제가 생긴다. 진짜 수평 확장이 되려면 각 서버가 어떤 요청이 와도 같은 결과를 내는 **무상태(Stateless)** 설계([HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP 자체의 무상태성)와, 상태를 공유 저장소로 분리하는 작업이 함께 필요하다.

**"헬스 체크가 성공하면 그 서버는 안전하다"** — 헬스 체크 엔드포인트만 가볍게 응답하고 실제 비즈니스 로직 경로(DB 연결 등)는 막혀 있는 경우가 있다. 실무에서는 헬스 체크가 실제 의존성(데이터베이스, 캐시 서버 연결 상태)까지 확인하도록 설계해야, "헬스 체크는 통과했는데 실제 요청은 다 실패하는" 상황을 막을 수 있다.

## 다른 개념과의 연결

로드 밸런싱은 [OSI 7계층과 TCP/IP](/post/computerterms/osi-and-tcp-ip/)에서 다룬 계층 중 어디서 동작하느냐에 따라 L4(전송 계층, IP·포트 기준 분산)와 L7(응용 계층, HTTP 헤더·경로 기준 분산)로 나뉜다. 다음 챕터에서는 여러 서버로 나뉜 상태에서 데이터 자체를 어떻게 분산·복제하는지(샤딩·복제) 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 로드 밸런싱이 필요한 이유(단일 서버의 한계, 가용성)를 설명할 수 있다. 라운드 로빈·최소 연결·IP 해시 각각의 장단점과 적합한 상황을 구분할 수 있다. 세션 고정이 필요한 이유와, 더 근본적인 해법(무상태 설계 + 공유 저장소)이 무엇인지 설명할 수 있다.

## 참고 자료

> Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.), Chapter 2: Application Layer. Pearson.

- [NGINX Documentation: Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/) — 실제 로드 밸런서 소프트웨어의 알고리즘·헬스 체크 설정
- [AWS: What Is Load Balancing?](https://aws.amazon.com/what-is/load-balancing/) — L4/L7 로드 밸런싱 구분과 실무 아키텍처 예시
