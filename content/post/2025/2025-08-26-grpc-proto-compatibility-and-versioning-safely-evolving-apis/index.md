---
title: "[gRPC] gRPC/Proto 호환성과 버저닝 - 안전한 API 진화"
description: "서버·클라이언트 배포 주기가 달라도 gRPC/Proto API를 추가·삭제할 때 호환성이 깨지지 않도록 하는 원칙과 절차를 정리한다. wire-safe/unsafe·compatible, ProtoJSON 주의, 패키지 버전·reserved·UNIMPLEMENTED 대응까지."
date: 2025-08-26
lastmod: 2025-08-27
categories:
- "Tech"
- "gRPC"
- "Protobuf"
tags:
- "gRPC"
- "Protocol-Buffers"
- "Protobuf"
- "Proto3"
- "Schema-Evolution"
- "Backward-Compatibility"
- "Forward-Compatibility"
- "Binary-Wire-Format"
- "ProtoJSON"
- "JSON-Mapping"
- "Unknown-Fields"
- "Reserved-Fields"
- "Reserved-Names"
- "Deleting-Fields"
- "Adding-Fields"
- "Enum-Values"
- "Enum-Compatibility"
- "Oneof"
- "Oneof-Compatibility"
- "Breaking-Change"
- "Non-Breaking-Change"
- "Wire-Safe"
- "Wire-Unsafe"
- "Wire-Compatible"
- "Field-Number"
- "Field-Renumbering"
- "Service-Versioning"
- "Package-Versioning"
- "v1"
- "v2"
- "UNIMPLEMENTED"
- "Behavior-Compatibility"
- "Buf"
- "buf-breaking"
- "CI-Checks"
- "Google-API-Design"
- "AIP"
- "Microsoft-gRPC"
- "ASP.NET-Core-gRPC"
- "Go-gRPC"
- "Java-gRPC"
- "Csharp-gRPC"
- "Python-gRPC"
- "Node-gRPC"
- "API-Lifecycle"
- "Deprecation"
- "Semantic-Versioning"
- "Server-Rollout"
- "Client-Rollout"
- "Transcoding"
- "REST-Interop"
- "Ignore-Unknown-Fields"
- "Enum-as-Int"
- "Data-Corruption-Risk"
- "PII-Risk"
- "Best-Practices"
- "버전관리"
- "하위호환"
- "상위호환"
- "필드예약"
- "스키마진화"
- "서비스버전"
- "프로토버프"
- "지속적통합"
- "안정적-배포"
- "롤링-업데이트"
image: "wordcloud.png"
---

gRPC/Protobuf에서 API를 추가·삭제할 때의 호환성 영향과 안전한 롤아웃 방법을 정리한다.

## 핵심 요약
- **추가(대체로 안전)**: 새 서비스/메서드/필드/enum 값 추가는 바이너리 레벨에서 안전. 단, 서버가 새 필드를 즉시 강제하면 구버전 클라이언트가 실패할 수 있다.
- **삭제(대체로 파괴적)**: RPC 삭제 시 클라이언트는 **UNIMPLEMENTED**를 받는다. 메시지 필드 삭제는 번호/이름을 반드시 `reserved`로 고정해야 재사용에 따른 손상을 방지한다.
- **JSON 경유 주의**: ProtoJSON은 미지 필드 보존이 없어 추가/삭제가 파싱 오류로 이어질 수 있다. 필요 시 "Ignore unknown fields" 옵션으로 완화한다.

## 서버 개발 체크리스트 (배포 주기 불일치 전제)
- 요청 스키마 추가 시 기본값 허용: 새 필드는 미설정이어도 성공해야 함. 필수화는 전면 배포 완료 후에 단계적 강제.
- 응답 스키마 추가 시 구버전 안전 확인: 구버전 클라이언트가 미지 필드를 무시(바이너리)하도록 하고, 앱 로직의 완전 `switch`/매핑 누락을 점검.
- 삭제는 즉시 금지, 단계적 절차 적용: deprecate → 유예 공지 → 실제 삭제 + `reserved`(번호·이름) 고정.
- 메서드/서비스 변경: 이름·패키지 변경은 URL 해시에 영향 → 구버전은 `UNIMPLEMENTED`가 나가므로 `v1/v2` 동시 호스팅으로 이행.
- ProtoJSON 경로 보호: 서버가 JSON을 생산하거나 게이트웨이를 쓴다면 구버전 클라이언트에 "Ignore unknown fields" 설정 배포 완료 전까지 새 필드 값을 쓰지 않음.
- Enum 값 추가 시 서버 방어: 알 수 없는 enum 값 입력에 대한 기본 처리(무시/매핑/에러) 정의.
- CI 규칙: 필드 번호 재사용 금지, renumber 금지, 삭제 시 `reserved` 강제, `oneof`로의 이동은 새 `oneof`에 한정.

## 클라이언트 개발 체크리스트
- 미지 필드 무시 확인: 바이너리 포맷에서는 기본적으로 안전. JSON 경로는 파서 설정에 "Ignore unknown fields" 지원/활성화.
- 새 필드에 대한 기본 동작: 서버가 새 필드를 요구하기 전까지는 기본값으로 정상 동작하도록 가드.
- Enum 확장 대비: 완전 `switch` 사용 시 default 분기 추가 및 알 수 없는 값 로깅.
- 서비스/메서드 삭제/이동 대비: `UNIMPLEMENTED` 수신 시 재시도 전략 또는 버전 업그레이드 경로로 유도.
- 재시도/백오프/Wait-for-Ready 정책: 일시적 실패(`UNAVAILABLE`, `DEADLINE_EXCEEDED`)와 프로토콜 실패를 구분 처리.
- ProtoJSON 사용 시 정밀 설정: 정수 인코딩(문자열/숫자) 호환성, enums-as-ints 필요 여부 점검.

## 상세 가이드
### 추가 시 안전 조건
- **요청에 새 필드**: 서버는 미설정(기본값)도 허용해야 한다.
- **응답에 새 필드**: 구버전 클라이언트는 미지 필드로 무시한다(바이너리).
- **enum 값 추가**: 직렬화는 안전하나 앱 로직(완전 `switch`)은 재점검 필요.

### 삭제 시 위험과 대응
- **서비스/메서드 삭제**: 호출 시 `UNIMPLEMENTED` (프로토콜 파괴적). 
- **메시지 필드 삭제**: 동일 번호/이름 재사용 금지 → `reserved`로 봉인(재사용 시 데이터 손상/PII 누출 위험).

### JSON(ProtoJSON) 경유 시
- 미지 필드를 보존하지 않으므로, 새 필드를 "쓰기 시작"하기 전 구버전 파서에 **Ignore unknown fields** 설정 배포 완료 상태를 보장한다.

## 버저닝/롤아웃 전략
- **패키지 버전**: `package foo.v1`, `foo.v2`로 동시 호스팅 → 점진 이행 후 구버전 종료.
- **삭제는 단계적**: deprecate → 유예기간 공지 → 삭제 + `reserved`(번호·이름) 고정.
- **CI 검증**: 필드 번호 변경/재사용 금지, 삭제 필드의 `reserved` 강제 규칙 검사.

### 추가/삭제 롤아웃 절차 템플릿
- 추가(요청 필드)
  1) 서버: 새 필드 비필수로 추가, 기본값 허용 배포
  2) 클라이언트: 읽기/쓰기 지원 배포(쓰기는 비활성)
  3) JSON 경로: 모든 소비자에 "Ignore unknown fields" 배포 확인
  4) 서버: 점진적으로 새 필드 요구(페이즈드 강제)

- 추가(응답 필드/enum 값)
  1) 서버: 응답에 새 필드/enum 값 추가 배포
  2) 클라이언트: 미지 필드 무시/enum default 분기 확인 및 배포
  3) 로깅/모니터링으로 구버전 영향 확인

- 삭제(필드/메서드)
  1) 서버: deprecate 표시 및 공지, 소비자 식별
  2) 스키마: 번호·이름 `reserved`로 고정
  3) 서버: `v2`로 대체 제공, `v1`은 유지
  4) 소비자 전환 완료 후 `v1` 제거 → 구호출은 `UNIMPLEMENTED`

## gRPC 상태 코드 참조(운영 동작 설계에 반영)
- UNIMPLEMENTED: 메서드 미존재/압축 미지원 → 버전 전환 진행 신호
- UNAVAILABLE: 일시적 불가 → 재시도/백오프 적용
- DEADLINE_EXCEEDED: 타임아웃 → 타임아웃/부하 재설계 필요
- UNKNOWN/INTERNAL: 직렬화/파싱 실패 등 → 스키마/게이트웨이 설정 확인

## C# 예제
### proto: v1 → v2로 안전 추가/삭제
```proto
syntax = "proto3";

package greet.v1;

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}

service Greeter {
  rpc SayHello(HelloRequest) returns (HelloReply);
}
```

```proto
syntax = "proto3";

package greet.v2;

message HelloRequest {
  string name = 1;
  optional string locale = 2; // 추가된 필드: 비설정도 허용
  reserved 3, 4;              // 삭제된 필드 번호를 재사용 금지
  reserved "legacy_id";       // JSON/TextFormat 대비 이름도 예약
}

message HelloReply {
  string message = 1;
}

service Greeter {
  rpc SayHello(HelloRequest) returns (HelloReply);
}
```

### 서버: v1/v2 동시 호스팅, 새 필드 기본값 허용
```csharp
using Grpc.Core;
using greet.v1;
using greet.v2;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddGrpc();
var app = builder.Build();

app.MapGrpcService<GreeterServiceV1>(); // greet.v1
app.MapGrpcService<GreeterServiceV2>(); // greet.v2

app.Run();

public sealed class GreeterServiceV1 : greet.v1.Greeter.GreeterBase
{
    public override Task<greet.v1.HelloReply> SayHello(greet.v1.HelloRequest request, ServerCallContext context)
        => Task.FromResult(new greet.v1.HelloReply { Message = $"Hello, {request.Name}" });
}

public sealed class GreeterServiceV2 : greet.v2.Greeter.GreeterBase
{
    public override Task<greet.v2.HelloReply> SayHello(greet.v2.HelloRequest request, ServerCallContext context)
    {
        // locale 미설정(기본값)도 허용 → 구버전 클라이언트와 호환
        var locale = string.IsNullOrWhiteSpace(request.Locale) ? "en-US" : request.Locale;
        var greeting = locale.StartsWith("ko", StringComparison.OrdinalIgnoreCase) ? "안녕하세요" : "Hello";
        return Task.FromResult(new greet.v2.HelloReply { Message = $"{greeting}, {request.Name}" });
    }
}
```

### 클라이언트: UNIMPLEMENTED 처리 및 v1로 폴백
```csharp
using Grpc.Net.Client;
using Grpc.Core;

var channel = Grpc.Net.Client.GrpcChannel.ForAddress("https://localhost:5001");
var clientV2 = new greet.v2.Greeter.GreeterClient(channel);

try
{
    var reply = await clientV2.SayHelloAsync(new greet.v2.HelloRequest { Name = "Jerry", Locale = "ko-KR" });
    Console.WriteLine(reply.Message);
}
catch (RpcException ex) when (ex.StatusCode == StatusCode.Unimplemented)
{
    // 서버에 v2가 없거나 메서드가 제거된 경우 → v1로 폴백
    var clientV1 = new greet.v1.Greeter.GreeterClient(channel);
    var reply = await clientV1.SayHelloAsync(new greet.v1.HelloRequest { Name = "Jerry" });
    Console.WriteLine(reply.Message);
}
```

### JSON 경로: 미지 필드 무시 설정(ProtoJSON)
```csharp
using Google.Protobuf;
using Google.Protobuf.Reflection;
using Google.Protobuf.WellKnownTypes;

var settings = new JsonParser.Settings(recursionLimit: 100, typeRegistry: TypeRegistry.Empty, ignoreUnknownFields: true);
var parser = new JsonParser(settings);

string json = "{\"name\":\"Jerry\",\"locale\":\"ko-KR\",\"unknown\":123}";
var req = parser.Parse<greet.v2.HelloRequest>(json); // unknown 필드는 무시
```

## 참고 문서
- [protobuf: Updating/Wire safety](https://protobuf.dev/programming-guides/proto3/#updating)
- [ProtoJSON wire safety](https://protobuf.dev/programming-guides/json/#json-wire-safety)
- [Microsoft: Versioning gRPC services](https://learn.microsoft.com/en-us/aspnet/core/grpc/versioning)
- [gRPC: Error handling/Status Codes](https://grpc.io/docs/guides/error/#status-codes)
- [Google Cloud: API Versioning Guide](https://cloud.google.com/apis/design/versioning)


