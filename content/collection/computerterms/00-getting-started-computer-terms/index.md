---
draft: false
image: "wordcloud.png"
collection_order: 0
slug: getting-started-computer-terms
title: "[Computer Terms] 00. 컴퓨터 용어 사전 개요와 읽는 법"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "컴퓨터 과학 용어를 왜 사전 형태로 정리하는지, 알고리즘부터 개발 프로세스까지 14개 갈래 105챕터가 어떤 순서로 이어지는지, 각 챕터를 읽고 나면 무엇을 할 수 있게 되는지를 정리한 Computer Terms 컬렉션의 개요 챕터."
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Data-Structure(자료구조)
- Time-Complexity(시간복잡도)
- Database(데이터베이스)
- Networking(네트워킹)
- Operating-System(운영체제)
- Security(보안)
- Reference(참고)
- Documentation(문서화)
- Glossary(용어집)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Concurrency(동시성)
- Caching(캐싱)
- Software-Engineering(소프트웨어공학)
- Fundamentals(기초)
- Distributed-Systems(분산시스템)
- Web(웹)
- Best-Practices
- Case-Study
- Deep-Dive
---

## 이 컬렉션을 왜 만드는가

실무에서 마주치는 CS 용어는 대부분 한 문장짜리 정의만으로는 부족하다. "시간 복잡도가 O(n log n)이다"라는 문장을 이해하려면 그 정의가 어떤 문제(자원의 한계)를 풀기 위해 등장했는지, 다른 개념(공간 복잡도, 자료구조 선택)과 어떻게 이어지는지를 함께 알아야 실제 코드 리뷰나 설계 논의에서 판단 근거로 쓸 수 있다. Computer Terms 컬렉션은 이런 용어를 낱개로 나열하는 사전이 아니라, 알고리즘·자료구조·컴퓨터 구조·네트워크·운영체제·데이터베이스·분산시스템·동시성·캐싱·보안·웹/프로토콜·소프트웨어 설계·프로그래밍 언어론·개발 프로세스라는 14개 CS 대분류를 기준으로 빠진 영역 없이 채운 것을 목표로 한다.

## 챕터 구성과 필요성

컬렉션은 14개 갈래, 총 105챕터(이 개요 챕터 포함)로 구성된다. 알고리즘 갈래는 문제를 "어떻게 푸는가"와 "얼마나 잘 푸는가"를 다루고, 나머지 갈래는 "무엇으로 어떻게 만드는가"를 다룬다. 갈래를 나눈 이유는 실무에서 각 갈래가 서로 다른 판단 상황에서 쓰이기 때문이다. 알고리즘 갈래는 "이 코드가 왜 느린가"를 진단할 때, 그 외 갈래는 "이 시스템을 어떻게 구성해야 하는가"를 설계할 때 필요하다.

| 갈래 | 다루는 질문 | 현재 챕터 |
|---|---|---|
| 알고리즘 | 문제를 얼마나 효율적으로 푸는가 | [알고리즘](/post/computerterms/algorithm/), [알고리즘 효율성](/post/computerterms/algorithm-efficiency/), [알고리즘 분류](/post/computerterms/algorithm-classification/), [시간 복잡도](/post/computerterms/time-complexity/), [정렬 알고리즘](/post/computerterms/sorting-algorithms/), [탐색 알고리즘](/post/computerterms/searching-algorithms/), [최단 경로 알고리즘](/post/computerterms/shortest-path-algorithms/), [동적 계획법](/post/computerterms/dynamic-programming/), [그리디 알고리즘](/post/computerterms/greedy-algorithms/) |
| 자료구조 | 데이터를 어떤 모양으로 들고 있는가 | [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/), [스택과 큐](/post/computerterms/stacks-and-queues/), [트리](/post/computerterms/trees/), [해시테이블](/post/computerterms/hash-tables/), [그래프](/post/computerterms/graphs/), [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/), [트라이](/post/computerterms/tries/), [유니온-파인드](/post/computerterms/union-find/), [세그먼트 트리](/post/computerterms/segment-trees/), [스킵 리스트](/post/computerterms/skip-lists/) |
| 네트워크 | 컴퓨터끼리 어떻게 데이터를 주고받는가 | [OSI 7계층과 TCP/IP](/post/computerterms/osi-and-tcp-ip/), [HTTP와 HTTPS](/post/computerterms/http-and-https/), [DNS와 소켓](/post/computerterms/dns-and-sockets/), [로드 밸런싱](/post/computerterms/load-balancing/), [CDN](/post/computerterms/content-delivery-networks/), [방화벽과 NAT](/post/computerterms/firewalls-and-nat/), [프록시: 정방향과 역방향](/post/computerterms/forward-and-reverse-proxies/), [HTTP/3와 QUIC](/post/computerterms/http3-and-quic/), [웹훅](/post/computerterms/webhooks/) |
| 운영체제 | 하나의 컴퓨터 위에서 여러 작업을 어떻게 함께 돌리는가 | [프로세스와 스레드](/post/computerterms/processes-and-threads/), [CPU 스케줄링](/post/computerterms/cpu-scheduling/), [메모리 관리와 가상 메모리](/post/computerterms/memory-management/), [파일 시스템](/post/computerterms/file-systems/), [인터럽트와 시스템 콜](/post/computerterms/interrupts-and-system-calls/), [데몬과 좀비 프로세스](/post/computerterms/daemons-and-zombie-processes/), [컨테이너와 가상화](/post/computerterms/containers-and-virtualization/), [시그널](/post/computerterms/signals/), [프로세스 간 통신(IPC)](/post/computerterms/inter-process-communication/) |
| 컴퓨터 구조 | CPU 안에서 명령어가 실제로 어떻게 처리되는가 | [CPU 구조와 파이프라이닝](/post/computerterms/cpu-and-pipelining/), [레지스터와 명령어 집합 구조](/post/computerterms/registers-and-isa/), [캐시 계층: L1/L2/L3](/post/computerterms/cache-hierarchy/), [SIMD](/post/computerterms/simd/), [부동소수점 표현](/post/computerterms/floating-point-representation/), [폰 노이만 구조](/post/computerterms/von-neumann-architecture/) |
| 데이터베이스 | 데이터를 어떻게 안전하고 빠르게 저장·조회하는가 | [ACID Transactions](/post/computerterms/acid-transactions/), [정규화와 인덱스](/post/computerterms/normalization-and-indexes/), [NoSQL과 쿼리 최적화](/post/computerterms/nosql-and-query-optimization/), [샤딩과 복제](/post/computerterms/sharding-and-replication/), [트랜잭션 격리 수준](/post/computerterms/transaction-isolation-levels/), [MVCC](/post/computerterms/mvcc/), [쿼리 플래너 내부](/post/computerterms/query-planner-internals/), [전문검색 인덱스](/post/computerterms/full-text-search-indexes/), [시계열 데이터베이스](/post/computerterms/time-series-databases/) |
| 분산시스템 | 여러 서버로 나뉜 시스템에서 일관성을 어떻게 다루는가 | [CAP 정리와 합의 알고리즘](/post/computerterms/cap-theorem-and-consensus/), [벡터 시계](/post/computerterms/vector-clocks/), [멱등성](/post/computerterms/idempotency/), [서킷 브레이커](/post/computerterms/circuit-breaker/), [메시지 큐](/post/computerterms/message-queues/), [이벤트 소싱](/post/computerterms/event-sourcing/) |
| 동시성 | 공유 자원에 여러 실행 흐름이 동시에 접근할 때 무엇이 깨지는가 | [레이스 컨디션과 락](/post/computerterms/race-conditions-and-locks/), [데드락](/post/computerterms/deadlocks/), [세마포어와 모니터](/post/computerterms/semaphores-and-monitors/), [원자적 연산과 CAS](/post/computerterms/atomic-operations-and-cas/), [코루틴과 async/await](/post/computerterms/coroutines-and-async-await/), [스레드풀](/post/computerterms/thread-pools/), [ABA 문제](/post/computerterms/aba-problem/) |
| 캐싱 | 반복되는 조회를 어떻게 빠르게 만드는가 | [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/), [CDN 캐싱 전략](/post/computerterms/cdn-caching/), [멀티레벨 캐싱](/post/computerterms/multilevel-caching/), [Write-Through와 Write-Back](/post/computerterms/write-through-and-write-back/) |
| 보안 | 데이터와 접근을 어떻게 지키는가 | [암호화와 해싱](/post/computerterms/encryption-and-hashing/), [인증과 인가](/post/computerterms/authentication-and-authorization/), [웹 취약점](/post/computerterms/web-vulnerabilities/), [OAuth와 OpenID Connect](/post/computerterms/oauth-and-oidc/), [웹 방화벽(WAF)](/post/computerterms/web-application-firewalls/), [디지털 서명과 인증서](/post/computerterms/digital-signatures-and-certificates/), [레이트 리미팅](/post/computerterms/rate-limiting/), [제로 트러스트 보안 모델](/post/computerterms/zero-trust-security/) |
| 웹/프로토콜 | 클라이언트-서버가 데이터를 어떤 형식·통로로 주고받는가 | [REST와 GraphQL](/post/computerterms/rest-and-graphql/), [웹소켓과 CORS](/post/computerterms/websockets-and-cors/), [gRPC](/post/computerterms/grpc/), [서버센트이벤트](/post/computerterms/server-sent-events/), [쿠키와 로컬 스토리지](/post/computerterms/cookies-and-local-storage/), [콘텐츠 협상](/post/computerterms/content-negotiation/) |
| 소프트웨어 설계 | 코드 구조를 어떤 기준으로 판단하는가 | [결합도와 응집도](/post/computerterms/coupling-and-cohesion/), [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/), [디자인 패턴 개요](/post/computerterms/design-patterns-overview/), [리팩토링과 코드 스멜](/post/computerterms/refactoring-and-code-smells/), [옵저버 패턴](/post/computerterms/observer-pattern/), [팩토리 패턴](/post/computerterms/factory-pattern/), [헥사고날 아키텍처](/post/computerterms/hexagonal-architecture/), [MVC와 MVVM](/post/computerterms/mvc-and-mvvm/), [이벤트 드리븐 아키텍처](/post/computerterms/event-driven-architecture/) |
| 프로그래밍 언어론 | 소스 코드가 어떻게 실행 가능한 형태로 바뀌는가 | [컴파일러와 인터프리터](/post/computerterms/compilers-and-interpreters/), [타입 시스템](/post/computerterms/type-systems/), [가비지 컬렉션](/post/computerterms/garbage-collection/), [클로저와 스코프](/post/computerterms/closures-and-scope/), [함수형 프로그래밍 패러다임](/post/computerterms/functional-programming-paradigm/), [제네릭과 다형성](/post/computerterms/generics-and-polymorphism/), [메모리 안전성과 소유권](/post/computerterms/memory-safety-and-ownership/) |
| 개발 프로세스 | 코드가 어떻게 관리·검증·배포되는가 | [버전 관리의 내부 구조](/post/computerterms/version-control-internals/), [CI/CD와 테스트 유형](/post/computerterms/ci-cd-and-testing-types/), [코드 리뷰](/post/computerterms/code-review/), [시맨틱 버저닝](/post/computerterms/semantic-versioning/), [피처 플래그](/post/computerterms/feature-flags/) |

챕터 순서는 난이도가 아니라 **의존 관계**를 기준으로 정했다. 각 갈래는 기초 개념(예: 자료구조의 배열·연결리스트, 동시성의 레이스 컨디션·락)을 먼저 두고, 그 위에서만 이해되는 심화 주제(세그먼트 트리, ABA 문제 등)를 뒤에 배치했다. 갈래 사이의 순서도 마찬가지다 — 캐싱 갈래는 운영체제의 메모리 계층 개념을 전제로 운영체제 갈래 이후에, 분산시스템 갈래는 데이터베이스 갈래의 샤딩·복제를 전제로 그 다음에, 소프트웨어 설계 갈래의 디자인 패턴·리팩토링은 그 갈래 안의 결합도·응집도·SOLID를 전제로 마지막 순서에 둔다. 각 챕터 본문의 "이 장을 읽기 전에" 절에서 실제로 전제하는 선행 챕터를 명시하므로, 이 표의 순서를 따르지 않고 필요한 챕터만 골라 읽어도 그 절이 부족한 배경지식을 짚어준다.

## 이 컬렉션을 다 읽으면 할 수 있는 것

각 챕터는 정의를 암기시키는 대신, 그 용어가 실무 코드나 시스템 설계 논의에서 어떤 질문에 답하는 데 쓰이는지를 함께 다룬다. 컬렉션을 따라 읽으면 "이 알고리즘의 시간 복잡도를 정확히 표기하고 대안과 비교할 수 있다", "트랜잭션이 깨지는 상황을 ACID 4속성 중 무엇이 실패했는지로 진단할 수 있다", "결합도·응집도 기준으로 코드 리뷰에서 설계 문제를 구체적으로 지적할 수 있다", "SQL 인젝션·XSS·CSRF가 각각 어떤 정상 메커니즘을 악용하는지 구분해 막을 수 있다", "REST와 GraphQL 중 서비스 특성에 맞는 쪽을 근거를 갖고 선택할 수 있다", "CAP 정리에서 CP와 AP 중 서비스 특성에 맞는 선택을 할 수 있다", "락·세마포어·CAS 중 상황에 맞는 동시성 제어 도구를 고를 수 있다"처럼, 용어를 설명이 아니라 판단의 근거로 쓸 수 있게 되는 것을 목표로 한다.
