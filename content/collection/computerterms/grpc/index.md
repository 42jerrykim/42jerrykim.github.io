---
image: "wordcloud.png"
slug: grpc
collection_order: 88
draft: false
title: "[Computer Terms] gRPC"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "gRPC는 HTTP/2 위에서 Protocol Buffers로 이진 직렬화하고 .proto 스키마로 클라이언트·서버 코드를 자동 생성하는 RPC 프레임워크입니다. REST와 비교해 원리와 적합한 상황을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Web(웹)
- API(Application Programming Interface)
- REST(Representational State Transfer)
- HTTP(HyperText Transfer Protocol)
- Microservices(마이크로서비스)
- Networking(네트워킹)
- Backend(백엔드)
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
- Concurrency(동시성)
- System-Design
- gRPC
- Protocol-Buffers
---

## 이 장을 읽기 전에

[REST와 GraphQL](/post/computerterms/rest-and-graphql/)에서 다룬 두 API 설계 스타일 — URL·메서드로 자원을 표현하는 REST, 쿼리로 필요한 필드를 지정하는 GraphQL — 을 안다고 가정한다. gRPC는 이 둘과 마찬가지로 클라이언트-서버가 데이터를 주고받는 방식이지만, HTTP 텍스트 메시지 대신 이진 형식을 쓰고 함수 호출처럼 통신을 설계한다는 점에서 접근이 다르다.

## 원격 프로시저 호출이라는 오래된 아이디어

REST와 GraphQL은 모두 "자원" 또는 "쿼리"라는 데이터 중심 모델로 통신을 설계한다. 반면 **RPC(Remote Procedure Call)**는 네트워크 너머의 서버 함수를 마치 로컬 함수처럼 호출하는 모델이다. `getUser(42)`를 로컬에서 부르듯 원격 서버의 `getUser` 함수를 부르면, 그 요청과 응답을 네트워크로 실어 나르는 세부 사항은 프레임워크가 감춘다. **gRPC**는 구글이 사내에서 쓰던 RPC 프레임워크를 2015년 오픈소스로 공개한 것으로, HTTP/2와 Protocol Buffers라는 두 기술 위에 이 RPC 모델을 구현했다.

## Protocol Buffers: 이진 직렬화로 크기와 속도를 얻다

REST·GraphQL은 보통 JSON으로 데이터를 직렬화한다. JSON은 사람이 읽기 쉽지만, 키 이름을 매 메시지마다 텍스트로 반복해서 싣고 숫자도 문자열로 표현하므로 크기가 커지고 파싱 비용도 든다. **Protocol Buffers(줄여서 Protobuf)**는 구글이 설계한 이진 직렬화 포맷으로, 필드 이름 대신 짧은 번호를 메시지에 싣고 정수·문자열 같은 타입을 이진 그대로 인코딩해 JSON보다 메시지 크기가 작고 인코딩·디코딩 속도가 빠르다. 이 크기·속도 이득은 필드 수가 많고 호출 빈도가 높은 서버 간 통신에서 특히 두드러진다.

Protobuf 메시지의 구조는 `.proto` 파일이라는 **강타입 스키마**로 미리 정의한다.

```protobuf
// user.proto
syntax = "proto3";

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
}

message GetUserRequest {
  int32 id = 1;
}

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
}
```

`= 1`, `= 2`는 필드 이름이 아니라 이진 인코딩에 쓰이는 **필드 번호**다. 메시지를 전송할 때는 이 번호와 값만 실리므로, 필드 이름 문자열을 매번 반복하는 JSON보다 페이로드가 작아진다. `service` 블록은 이 서버가 제공하는 원격 함수(RPC 메서드) 목록을 선언한다.

## 스키마에서 코드 생성까지

`.proto` 파일 하나를 `protoc`(Protobuf 컴파일러)와 gRPC 플러그인에 넣으면, 여러 언어의 클라이언트·서버 코드가 자동으로 생성된다. 서버 개발자는 `GetUser` 메서드의 실제 로직만 구현하면 되고, 클라이언트 개발자는 생성된 스텁(stub)의 `GetUser(request)`를 로컬 함수처럼 호출하면 된다 — 요청 직렬화, HTTP/2 프레임 전송, 응답 역직렬화는 생성된 코드가 처리한다.

```text
$ protoc --go_out=. --go-grpc_out=. user.proto
  → user.pb.go       (User, GetUserRequest 등 구조체)
  → user_grpc.pb.go  (UserServiceClient, UserServiceServer 인터페이스)
```

이 코드 생성 덕분에 클라이언트와 서버가 주고받는 메시지 구조가 스키마 한 곳에서 강제된다. REST에서는 API 문서(OpenAPI 스펙 등)와 실제 서버 구현이 어긋나도 컴파일 타임에는 알 수 없지만, gRPC는 `.proto`가 바뀌면 생성 코드의 타입도 함께 바뀌므로 필드 이름 오타나 타입 불일치가 컴파일 단계에서 드러난다.

## HTTP/2 위에서: 스트리밍과 다중화

gRPC는 HTTP/2를 전송 계층으로 쓴다. [HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP/1.1은 한 연결에서 요청-응답을 순서대로 처리하지만, HTTP/2는 하나의 TCP 연결 위에서 여러 요청·응답 스트림을 동시에 주고받는 **다중화(Multiplexing)**를 지원한다. gRPC는 이 스트림 구조를 활용해 단순 요청-응답 외에도 서버가 하나의 요청에 여러 응답을 순차적으로 흘려보내는 **서버 스트리밍**, 클라이언트가 여러 메시지를 보내고 서버가 하나로 응답하는 **클라이언트 스트리밍**, 양쪽이 동시에 메시지를 주고받는 **양방향 스트리밍**까지 네 가지 호출 방식을 표준으로 제공한다.

## 왜 브라우저에서 직접 쓰기 어려운가

gRPC가 REST를 대체하지 못하는 가장 큰 이유는 브라우저 호환성이다. 브라우저의 표준 `fetch`나 `XMLHttpRequest` API는 HTTP/2의 저수준 프레임을 직접 제어할 수 없고, gRPC가 요구하는 트레일러(trailer, 응답 본문 뒤에 오는 상태 코드)도 다루지 못한다. 이 때문에 브라우저에서 gRPC를 쓰려면 gRPC-Web이라는 별도 프로토콜과 프록시(Envoy 등)를 거쳐야 한다 — 이 우회 경로 자체가 REST 대비 진입장벽이다. 반면 서버끼리 통신하는 환경(마이크로서비스 간 호출)은 이런 제약이 없고, Protobuf의 크기·속도 이득과 강타입 스키마의 이점을 그대로 누릴 수 있다. 그래서 gRPC는 주로 마이크로서비스 내부 서비스 간 통신에, REST·GraphQL은 브라우저·모바일 클라이언트를 마주하는 공개 API에 쓰이는 역할 분담이 자리 잡았다.

## 비교: REST vs GraphQL vs gRPC

| 특성 | REST | GraphQL | gRPC |
|---|---|---|---|
| 직렬화 형식 | 보통 JSON(텍스트) | 보통 JSON(텍스트) | Protobuf(이진) |
| 스키마 강제 | 선택(OpenAPI 등, 강제 아님) | 있음(GraphQL 스키마) | 있음(.proto, 컴파일 타임 검증) |
| 코드 자동 생성 | 도구에 따라 다름 | 도구에 따라 다름 | 표준 기능(protoc) |
| 브라우저 직접 호출 | 쉬움 | 쉬움 | 어려움(gRPC-Web·프록시 필요) |
| 스트리밍 지원 | 제한적(SSE 등 별도 필요) | 구독(subscription) 확장 필요 | 표준 기능(단방향·양방향) |
| 주 사용처 | 공개 API, 브라우저·모바일 클라이언트 | 프런트엔드 데이터 요구가 다양한 서비스 | 서버 간 통신(마이크로서비스) |

## 흔한 오개념

**"gRPC가 REST보다 항상 빠르다"** — Protobuf의 이진 인코딩과 HTTP/2의 다중화는 분명 오버헤드를 줄이지만, 이 이득은 필드 수가 많고 호출 빈도가 높은 서버 간 통신에서 두드러진다. 필드가 몇 개뿐인 단순 요청이나, 캐싱(CDN)이 중요한 공개 API에서는 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 URL 기반 HTTP 캐싱을 gRPC가 활용하기 어렵다는 점이 오히려 불리하게 작용할 수 있다. "더 빠르다"는 벤치마크 조건(메시지 크기, 호출 빈도, 캐싱 가능 여부)에 따라 달라지는 주장이지 절대 법칙이 아니다.

**"프로토콜 버퍼는 압축이다"** — Protobuf는 필드 이름을 번호로 대체하고 타입을 이진으로 인코딩해 크기를 줄이지만, gzip 같은 **압축 알고리즘**과는 다른 층위의 기술이다. 실제로 gRPC 서버는 Protobuf로 직렬화한 메시지에 추가로 gzip 압축을 적용할 수도 있다 — 직렬화(구조를 바이트로 바꾸는 것)와 압축(바이트를 더 작게 줄이는 것)은 서로 보완적인 별개 단계다.

## 다른 개념과의 연결

gRPC의 HTTP/2 다중화는 [웹소켓과 CORS](/post/computerterms/websockets-and-cors/)에서 다룬 서버-클라이언트 양방향 통신과 목적이 겹치지만, 웹소켓은 브라우저 친화적인 반면 gRPC 스트리밍은 서버 간 통신에 최적화되어 있다는 차이가 있다. 다음 챕터에서는 웹소켓의 양방향 통신만큼 복잡한 인프라 없이, 서버가 클라이언트에게 단방향으로 실시간 데이터를 흘려보내는 더 가벼운 대안인 서버센트이벤트(SSE)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. gRPC가 HTTP/2와 Protocol Buffers를 어떻게 결합해 통신하는지 설명할 수 있다. `.proto` 스키마에서 클라이언트·서버 코드가 자동 생성되는 과정과 그 이점을 설명할 수 있다. gRPC가 브라우저에서 직접 호출되기 어려운 이유와, 그래서 주로 서버 간 통신에 쓰이는 이유를 설명할 수 있다.

## 참고 자료

> "In gRPC, a client application can directly call a method on a server application on a different machine as if it were a local object, making it easier for you to create distributed applications and services." — gRPC Authors, *gRPC Documentation: Introduction to gRPC*, grpc.io

- [gRPC Official Documentation](https://grpc.io/docs/what-is-grpc/introduction/) — gRPC 개념·아키텍처 공식 소개
- [Protocol Buffers Documentation](https://protobuf.dev/overview/) — Protobuf 인코딩 방식과 스키마 문법 공식 가이드
