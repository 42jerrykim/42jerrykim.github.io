---
collection_order: 4
date: 2026-07-14
lastmod: 2026-07-14
draft: false
image: wordcloud.png
title: "[IO 11] IOCP와 Windows I/O"
slug: windows-iocp-io-model-optimization
description: "Windows I/O Completion Port(IOCP)의 동작 원리와 스레드 풀 연동을 다룹니다. OVERLAPPED 구조체, 동시성 값, CreateThreadpoolIo API로 완료 기반 비동기 I/O를 최적화하고 흔한 함정을 피하는 방법을 정리합니다."
tags:
  - Windows(윈도우)
  - OS(운영체제)
  - Kernel
  - C++
  - C
  - Concurrency(동시성)
  - IO(Input/Output)
  - Performance(성능)
  - Optimization(최적화)
  - Latency
  - Throughput
  - Benchmark
  - Profiling(프로파일링)
  - Implementation(구현)
  - Best-Practices
  - Code-Quality(코드품질)
  - Debugging(디버깅)
  - System-Design
  - Backend(백엔드)
  - Networking(네트워킹)
  - Scalability(확장성)
  - IOCP
  - Overlapped-IO
  - Proactor
  - Thread-Pool
  - WinSock
  - IoRing
  - Windows-API
  - GetQueuedCompletionStatus
---

**IOCP(I/O Completion Port)**는 Windows가 제공하는 완료 기반(completion-based) 비동기 I/O 모델로, 파일·소켓 핸들을 하나의 커널 큐에 묶고 소수의 워커 스레드가 완료된 작업만 뽑아 처리하도록 만드는 메커니즘을 말합니다. 연결 수만 개를 스레드 하나씩 대응해서 처리하면 컨텍스트 스위치와 스택 메모리 비용이 스레드 수에 비례해 커지는데, IOCP는 "요청은 커널에 맡기고 완료된 결과만 소수의 스레드가 순번대로 가져간다"는 원칙으로 이 문제를 우회합니다. 이 장에서는 IOCP 객체가 내부적으로 완료 패킷을 어떻게 큐잉·배분하는지, 동시성 값(concurrency value)이 스레드 스케줄링에 어떤 영향을 주는지, 그리고 수동으로 워커 스레드를 관리하는 대신 Windows Thread Pool API(`CreateThreadpoolIo`)에 위임하는 방법을 다룹니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [비동기 I/O 기초: select·poll·epoll·kqueue](/post/io-optimization/async-io-select-poll-epoll-kqueue/)에서 다룬 "이벤트 기반 I/O가 스레드-per-connection보다 유리한 이유"를 전제로 합니다. IOCP는 그 흐름의 Windows판 구현체이므로, epoll이 "준비됨(readiness)"을 알려주는 반면 IOCP는 "완료됨(completion)"을 알려준다는 차이만 먼저 이해하고 오면 충분합니다.

**이 장의 깊이**: 이 장은 **중급**을 대상으로 합니다. IOCP 객체 모델, OVERLAPPED 구조체, 동시성 값, 스레드 풀 연동(`CreateThreadpoolIo`/`StartThreadpoolIo`)까지 실무에서 바로 쓸 수 있는 수준을 다룹니다. **다루지 않는 것**: Reactor/Proactor 패턴 자체의 이론적 비교는 [I/O 멀티플렉싱 패턴: Reactor·Proactor](/post/io-optimization/io-multiplexing-reactor-proactor-patterns/)에서 다루므로 여기서는 IOCP가 Proactor의 대표 구현이라는 점만 짚고 넘어갑니다. 소켓 프로토콜 세부·네트워크 스택 튜닝은 네트워크 최적화 트랙(Tr.12)의 영역이고, Linux io_uring의 내부 구조는 [io_uring 심화](/post/io-optimization/io-uring-advanced-deep-dive/)와 [Tr.07 io_uring 개요](/post/os-optimization/io-uring-overview-fundamentals/)에서 다룹니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "IOCP의 등장 배경" ~ "IOCP 객체 모델과 완료 큐 동작" | 완료 기반 모델이 스레드-per-connection과 다른 이유 이해 |
| **중급자** | "동시성 값과 워커 스레드 풀 설계" ~ "벤치마크" | 동시성 값·스레드 풀 크기·배치 디큐를 실무에 적용 |
| **전문가** | "흔한 오개념" ~ "비판적 시각" | 완료 순서·OVERLAPPED 수명 함정을 진단하고 IoRing 등 대안과 비교 판단 |

---

## IOCP의 등장 배경

IOCP는 Windows NT 계열 초기(NT 3.5, 1994년 무렵으로 알려짐)부터 서버 애플리케이션이 수천 개의 동시 연결을 소수의 스레드로 처리할 수 있도록 설계된 커널 메커니즘입니다. 당시 대안은 연결마다 스레드를 하나씩 붙이는 방식이었는데, 스레드 수가 늘어날수록 커널 스케줄러의 컨텍스트 스위치 비용과 스레드별 스택 메모리(기본 1MB)가 누적되어 확장성의 한계에 부딪혔습니다. IOCP는 "I/O 요청은 즉시 반환하고, 완료된 결과만 커널 큐에 쌓아 두었다가 소수의 스레드가 순서대로 꺼내 처리한다"는 완료 기반 모델로 이 문제를 해결했고, 이후 IIS·SQL Server를 포함한 Windows 서버 소프트웨어 대부분의 I/O 기반이 되었습니다. Microsoft Learn의 개념 문서는 IOCP를 "다중 프로세서 시스템에서 여러 비동기 I/O 요청을 처리하기 위한 효율적인 스레딩 모델"로 소개합니다.

이 모델은 Reactor/Proactor 분류에서 **Proactor 패턴**의 대표 구현으로 분류됩니다. Reactor는 "I/O가 준비되었으니 네가 직접 read/write를 호출하라"고 알리는 반면, Proactor는 "read/write를 미리 커널에 맡겨 두면 완료된 결과를 통지해 준다"는 차이가 있습니다. 이 차이가 실제 코드 구조에 미치는 영향과 Linux epoll(Reactor형)·io_uring(Proactor에 가까움)과의 비교는 [I/O 멀티플렉싱 패턴](/post/io-optimization/io-multiplexing-reactor-proactor-patterns/)에서 다루므로, 이 장에서는 IOCP 자체의 API와 튜닝에 집중합니다.

## IOCP 객체 모델과 완료 큐 동작

`CreateIoCompletionPort` 함수는 두 가지 역할을 겸합니다. 핸들 인자로 `INVALID_HANDLE_VALUE`를 넘기면 새 IOCP 객체를 생성하고, 이미 만든 IOCP 핸들과 함께 파일·소켓 핸들을 넘기면 그 핸들을 해당 포트에 **연결(association)**합니다. 연결된 핸들에 `ReadFile`·`WriteFile`·`WSARecv`·`WSASend`처럼 `OVERLAPPED` 구조체를 받는 함수를 오버랩드 모드로 호출하면, 커널은 I/O를 백그라운드에서 처리하고 완료되는 즉시 **완료 패킷**을 그 포트의 큐에 적재합니다. 워커 스레드는 직접 완료를 기다리는 대신 `GetQueuedCompletionStatus`를 호출해 이 큐에서 패킷을 꺼내며, 이때 바이트 수·완료 키(completion key)·원래 넘겼던 `OVERLAPPED` 포인터를 함께 돌려받습니다.

여기서 실무에 자주 영향을 주는 세부 동작이 하나 있습니다. 완료 패킷은 큐에 **FIFO**로 쌓이지만, 큐를 기다리던 스레드들은 **LIFO**로 깨어납니다. 즉 가장 최근에 대기 상태로 들어간 스레드가 먼저 깨어나 가장 오래된 완료 패킷을 처리하는데, 이는 최근에 실행되어 캐시가 아직 따뜻한 스레드를 우선 재사용해 컨텍스트 스위치와 캐시 미스를 줄이려는 의도적 설계입니다. 완료 키는 보통 연결·파일별 컨텍스트 구조체를 가리키는 포인터로 채워, 완료를 처리하는 스레드가 어떤 연결의 어떤 요청인지 즉시 식별하도록 씁니다.

```cpp
#include <winsock2.h>
#include <mswsock.h>
#include <windows.h>

// 연결별 컨텍스트: 완료 키로 전달되어 워커 스레드가 어떤 소켓인지 식별하는 데 쓰인다.
struct ConnectionContext {
  SOCKET socket;
  OVERLAPPED overlapped;   // OVERLAPPED는 반드시 구조체 첫 멤버로 두어 CONTAINING_RECORD로 되짚을 수 있게 한다.
  char buffer[4096];
  WSABUF wsabuf;
};

// IOCP 생성과 소켓 연결(association)을 한 번에 보여주는 최소 예시.
HANDLE create_iocp_and_associate(SOCKET client_socket, DWORD concurrency_value) {
  HANDLE iocp = CreateIoCompletionPort(INVALID_HANDLE_VALUE, nullptr, 0, concurrency_value);
  if (!iocp) return nullptr;
  // completion key로 컨텍스트 포인터를 그대로 등록해 두면 완료 시 바로 캐스팅해 쓸 수 있다.
  auto* ctx = new ConnectionContext{client_socket, {}, {}, {}};
  CreateIoCompletionPort(reinterpret_cast<HANDLE>(client_socket), iocp,
                         reinterpret_cast<ULONG_PTR>(ctx), 0);
  return iocp;
}
```

이 코드에서 `concurrency_value`로 넘긴 값은 다음 절에서 다루는 **동시성 값**이며, 소켓을 연결할 때 넘기는 마지막 인자(위 예시의 `0`)는 무시되고 최초 생성 시 지정한 값만 유효합니다. `ConnectionContext`처럼 요청마다 별도로 힙에 할당한 구조체를 완료 키나 `OVERLAPPED` 포인터로 전달하는 패턴은 이후 절의 함정과도 직결되므로 잘 봐 둘 필요가 있습니다.

## 동시성 값과 워커 스레드 풀 설계

`CreateIoCompletionPort`의 `NumberOfConcurrentThreads` 인자, 이른바 **동시성 값**은 그 포트에 대해 동시에 "실행 가능(runnable)" 상태일 수 있는 스레드 수의 상한입니다. 실행 중인 스레드 수가 이 값에 도달하면, 이미 큐에 완료 패킷이 쌓여 있어도 시스템은 추가 워커 스레드를 깨우지 않고 대기시킵니다. Microsoft Learn 문서는 "가장 무난한 상한값은 CPU 코어 수"라고 권장하며, 계산량이 많은 처리라면 그보다 크게 잡아 더 많은 스레드가 동시에 돌게 할 수 있다고 설명합니다. 다만 워커 스레드 풀 자체는 동시성 값보다 **크게** 만드는 것이 정석인데, 스레드가 `GetQueuedCompletionStatus` 대기 상태뿐 아니라 동기 호출·페이지 폴트·락 대기 등 다른 이유로도 블록될 수 있기 때문입니다. 같은 문서는 "CPU 코어 수의 최소 2배" 정도를 스레드 풀 크기의 경험적 기준으로 제시합니다.

완료 패킷을 꺼내는 API도 두 가지입니다. `GetQueuedCompletionStatus`는 한 번에 패킷 하나만 반환하지만, `GetQueuedCompletionStatusEx`는 `OVERLAPPED_ENTRY` 배열과 `ulCount`를 받아 **여러 완료를 한 번의 호출로 배치 반환**합니다. 초당 처리해야 할 I/O가 많은 서버에서는 호출 하나당 커널 전환(user/kernel mode transition) 비용이 고정 비용으로 붙기 때문에, 배치 크기를 늘려 호출 횟수를 줄이는 쪽이 유리한 경우가 많습니다. 이는 Linux `epoll_wait`의 `maxevents`나 io_uring의 배치 제출·완료와 같은 발상으로, [비동기 I/O 기초](/post/io-optimization/async-io-select-poll-epoll-kqueue/)·[io_uring 심화](/post/io-optimization/io-uring-advanced-deep-dive/)에서 다룬 배치 처리 원칙이 Windows에서도 그대로 적용됩니다.

```cpp
#include <windows.h>
#include <vector>

// GetQueuedCompletionStatusEx로 최대 batch_size개의 완료를 한 번에 꺼내는 워커 루프.
void worker_loop_batched(HANDLE iocp, ULONG batch_size) {
  std::vector<OVERLAPPED_ENTRY> entries(batch_size);
  for (;;) {
    ULONG removed = 0;
    BOOL ok = GetQueuedCompletionStatusEx(iocp, entries.data(),
                                          batch_size, &removed, INFINITE, FALSE);
    if (!ok) break;  // 핸들이 닫혔거나 오류; 실제 코드는 GetLastError로 원인을 구분한다.
    for (ULONG i = 0; i < removed; ++i) {
      // entries[i].lpCompletionKey, entries[i].lpOverlapped로 컨텍스트를 되짚어 처리한다.
    }
  }
}
```

한 번의 호출로 여러 완료를 받는 만큼 각 완료 처리가 다음 배치 수신을 지연시키므로, 배치 크기와 처리 로직의 무게를 함께 프로파일링하며 균형점을 찾아야 합니다.

## Thread Pool API로 스레드 관리 위임하기

앞 절의 `GetQueuedCompletionStatus(Ex)` 루프를 직접 짜는 방식은 스레드 생성·종료·부하에 따른 크기 조절까지 애플리케이션이 모두 책임져야 합니다. Windows Vista부터는 **Thread Pool API**의 `CreateThreadpoolIo`로 이 책임을 시스템 기본 스레드 풀에 위임할 수 있습니다. `CreateThreadpoolIo`는 파일 핸들과 콜백 함수를 묶어 `TP_IO` 객체를 만들고, 이후 시스템이 알아서 워커 스레드를 늘리거나 줄이며 완료 시 콜백을 호출해 줍니다. 이 방식에는 반드시 지켜야 하는 규칙이 하나 있는데, 오버랩드 I/O를 시작하기 **직전에 매번** `StartThreadpoolIo`를 호출해야 한다는 점입니다.

**깨진 코드**: 아래는 이 규칙을 어긴 예입니다. `StartThreadpoolIo`를 최초 한 번만 호출하고 이후 반복되는 `ReadFile` 호출마다 다시 호출하지 않습니다.

```cpp
// 깨진 코드: StartThreadpoolIo를 첫 요청에서만 호출하고 이후 요청에서 생략함
void submit_read_broken(PTP_IO tp_io, HANDLE file, ConnectionContext* ctx, bool first_call) {
  if (first_call) {
    StartThreadpoolIo(tp_io);  // 두 번째 이후 read에는 호출되지 않음
  }
  ReadFile(file, ctx->buffer, sizeof(ctx->buffer), nullptr, &ctx->overlapped);
}
```

**원인**: `StartThreadpoolIo`는 "이번 I/O 완료 시 콜백이 호출될 것"이라고 스레드 풀에 미리 알리는 카운터 증가 호출입니다. 이 카운터를 갱신하지 않은 채 완료가 도착하면 스레드 풀은 그 완료를 자신이 추적하지 않는 이벤트로 간주해 콜백을 누락하거나, 내부 카운터 불일치로 메모리 손상을 일으킬 수 있습니다. Microsoft Learn 문서는 이 함수의 Remarks에서 "오버랩드 I/O 완료 콜백을 받으려면 `StartThreadpoolIo`를 호출하라"고 명시하며, 매 호출을 요구하는 규칙입니다.

**올바른 구현**: 매 I/O 요청 직전에 항상 호출하고, 요청이 동기적으로 즉시 실패한 경우에는 `CancelThreadpoolIo`로 카운터를 되돌립니다.

```cpp
#include <threadpoolapiset.h>

void submit_read_fixed(PTP_IO tp_io, HANDLE file, ConnectionContext* ctx) {
  StartThreadpoolIo(tp_io);  // 매 I/O 시작 직전에 반드시 호출
  BOOL ok = ReadFile(file, ctx->buffer, sizeof(ctx->buffer), nullptr, &ctx->overlapped);
  if (!ok && GetLastError() != ERROR_IO_PENDING) {
    CancelThreadpoolIo(tp_io);  // 동기 실패 시 카운터를 되돌려 불일치를 막는다
  }
}
```

**검증 도구**: 이런 카운터 불일치·use-after-free류 버그는 평소 재현이 어렵고 부하가 몰릴 때만 드러나는 경우가 많습니다. Windows에서는 Application Verifier(`appverif.exe`)의 핸들·힙 검사를 활성화해 실행하면 잘못된 핸들 재사용이나 힙 손상을 즉시 중단시켜 잡아낼 수 있고, MSVC의 `/fsanitize=address` 빌드로도 `ConnectionContext` 같은 힙 버퍼의 use-after-free를 재현 시점에 감지할 수 있습니다.

## 벤치마크: 동시성 값과 배치 디큐 효과 측정

동시성 값과 배치 디큐 크기가 실제로 처리량에 얼마나 영향을 주는지는 플랫폼·워크로드마다 달라지므로 항상 대상 환경에서 직접 측정해야 합니다. 아래는 로컬 루프백 소켓에 대해 고정된 워커 스레드 수로 짧은 요청을 반복 처리하면서 `QueryPerformanceCounter`로 처리량을 측정하는 최소 골격입니다(Windows 10/11, MSVC `cl /O2`, x64 기준).

```cpp
#include <windows.h>
#include <cstdio>

// concurrency_value·batch_size를 바꿔가며 실행해 초당 완료 처리 건수를 비교한다.
// 실제 측정에서는 create_iocp_and_associate()로 만든 IOCP와 다수의 소켓 컨텍스트를 사용한다.
void run_benchmark(HANDLE iocp, ULONG batch_size, int duration_ms) {
  LARGE_INTEGER freq, start, now;
  QueryPerformanceFrequency(&freq);
  QueryPerformanceCounter(&start);
  long long completions = 0;
  std::vector<OVERLAPPED_ENTRY> entries(batch_size);
  do {
    ULONG removed = 0;
    if (GetQueuedCompletionStatusEx(iocp, entries.data(), batch_size, &removed, 100, FALSE)) {
      completions += removed;
    }
    QueryPerformanceCounter(&now);
  } while ((now.QuadPart - start.QuadPart) * 1000 / freq.QuadPart < duration_ms);
  double seconds = duration_ms / 1000.0;
  std::printf("batch=%lu completions/sec=%.0f\n", batch_size, completions / seconds);
}
```

`g++`이 아닌 MSVC 환경에서는 `cl /O2 bench.cpp ws2_32.lib`로 빌드하며, 동시성 값은 `CreateIoCompletionPort` 생성 시점 인자로, 배치 크기는 `batch_size`로 바꿔가며 반복 측정합니다. 코어 수·연결 수·요청 크기에 따라 최적 조합이 달라지므로, 이 골격은 "직접 재현해 볼 시작점"으로만 쓰고 특정 배수(예: 2배)를 정답으로 단정하지 않는 것이 안전합니다.

## 흔한 오개념 교정

**"완료 패킷은 요청한 순서대로 처리된다"**는 잘못된 전제입니다. 큐잉은 FIFO이지만 스레드 언블록은 LIFO이고, 애초에 커널 드라이버·디스크 스케줄러가 여러 오버랩드 요청을 반드시 제출 순서대로 끝낸다는 보장도 없습니다. 요청-응답 순서가 의미를 갖는 프로토콜이라면 완료 키나 컨텍스트에 시퀀스 번호를 직접 넣어 애플리케이션 레벨에서 순서를 재구성해야 합니다.

**"동시성 값은 클수록 성능이 좋다"**도 흔한 오해입니다. 동시성 값은 "동시에 실행 가능한 스레드 수의 상한"이지 처리량 목표치가 아닙니다. 값을 필요 이상으로 키우면 코어 수보다 많은 스레드가 동시에 실행 가능해져 컨텍스트 스위치와 캐시 미스가 늘 수 있고, Microsoft Learn 문서도 "CPU 코어 수"를 기본 상한으로 권장합니다. 계산 비중이 큰 완료 처리 로직처럼 예외적인 경우에만 신중하게 늘립니다.

**"OVERLAPPED와 그 컨텍스트는 요청을 건 함수가 끝나면 정리해도 된다"**는 위험한 가정입니다. `ReadFile`·`WSASend` 같은 함수는 `ERROR_IO_PENDING`을 반환한 시점에 이미 커널이 그 메모리를 계속 참조하고 있으므로, 완료 패킷이 도착하기 **전까지** `OVERLAPPED`와 버퍼는 살아 있어야 합니다. 로컬 스택 변수에 `OVERLAPPED`를 두고 함수가 반환된 뒤 완료가 도착하면 이미 해제된 스택 메모리를 커널과 워커 스레드가 함께 건드리는 use-after-free가 됩니다.

## 판단 기준: IOCP 경로 선택

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 연결 수백~수만, 세밀한 제어 필요 | 수동 `GetQueuedCompletionStatus(Ex)` 루프 + 직접 관리하는 워커 풀 | 연결마다 스레드 하나씩 |
| 스레드 풀 크기·확장을 직접 관리하고 싶지 않을 때 | `CreateThreadpoolIo`/`StartThreadpoolIo` | 매번 수동으로 스레드 생성·종료 관리 |
| 초당 완료 건수가 매우 많은 서버 | `GetQueuedCompletionStatusEx`로 배치 디큐 | 완료마다 개별 `GetQueuedCompletionStatus` 호출 |
| 요청-응답 순서가 프로토콜상 중요 | 컨텍스트에 시퀀스 번호를 두고 애플리케이션에서 재정렬 | 완료 순서가 곧 제출 순서라고 가정 |
| Windows 11/Server 2022 이상 전용, 최신 완료 큐 모델 실험 | `IoRing` API 검토(호환성 확인 후) | 구버전 서버 지원이 필요한데 IoRing에만 의존 |

## 비판적 시각: 한계와 트레이드오프

IOCP의 가장 큰 실무 비용은 API 자체의 장황함과 `OVERLAPPED`·컨텍스트 수명 관리의 난이도입니다. 요청마다 힙에 컨텍스트를 할당하고, 완료 시점에 정확히 해제하는 코드를 직접 관리해야 하므로 use-after-free·이중 해제 같은 버그가 구조적으로 발생하기 쉽고, 이는 Linux io_uring이 서브미션/완료 큐를 통해 유사한 문제를 안고 있는 것과 근본적으로 다르지 않습니다. Thread Pool API(`CreateThreadpoolIo`)가 스레드 관리 부담은 줄여주지만, 시스템 기본 스레드 풀의 확장·축소 정책은 애플리케이션에서 세밀하게 제어할 수 있는 노출면이 크지 않아, 지연시간 분포의 꼬리(tail latency)를 극한까지 다듬어야 하는 워크로드에서는 수동 관리가 여전히 선호되기도 합니다.

Windows 11/Server 2022부터 제공되는 `IoRing` API는 제출·완료 큐를 애플리케이션과 커널이 공유 메모리로 주고받는 구조로, 개념적으로 Linux io_uring과 유사한 최신 완료 큐 모델입니다. 다만 지원 최소 버전이 Windows Build 22000 이상으로 제한되어 있어 구버전 Windows Server를 지원해야 하는 환경에서는 아직 선택지가 아니며, IOCP와 IoRing 중 어느 쪽이 유리한지는 워크로드·API 성숙도에 따라 계속 바뀌는 영역이므로 이 장에서는 존재와 방향성만 짚어 둡니다. 소켓 처리량을 극한까지 끌어올려야 하는 경우 Winsock의 Registered I/O(RIO) 확장을 함께 검토할 수 있지만, 소켓·프로토콜 세부 튜닝은 네트워크 최적화 트랙(Tr.12)의 범위이므로 여기서는 IOCP의 대안 축이 있다는 점만 밝힙니다.

## 마무리

이 장을 읽고 나면 다음을 스스로 확인할 수 있어야 합니다.

```mermaid
flowchart LR
  appThread["애플리케이션 스레드"] -->|"ReadFile/WSARecv(OVERLAPPED)"| kernelDriver["커널 I/O 드라이버"]
  kernelDriver -->|"비동기 처리 완료"| completionQueue["IOCP 완료 큐</br>(FIFO 적재)"]
  completionQueue -->|"LIFO로 언블록"| workerThread["워커 스레드 풀"]
  workerThread -->|"GetQueuedCompletionStatus(Ex)"| handler["완료 처리 로직"]
```

- [ ] IOCP가 연결마다 스레드를 두는 방식과 어떻게 다른지, 완료 기반 모델의 동작을 설명할 수 있다.
- [ ] 완료 패킷이 FIFO로 쌓이고 스레드가 LIFO로 깨어나는 이유와 그 결과 순서 보장이 없다는 점을 설명할 수 있다.
- [ ] 동시성 값과 워커 스레드 풀 크기를 구분하고, 각각 어떤 기준으로 정할지 말할 수 있다.
- [ ] `GetQueuedCompletionStatusEx`의 배치 디큐가 유리한 상황을 설명할 수 있다.
- [ ] `CreateThreadpoolIo`/`StartThreadpoolIo` 규칙과 `OVERLAPPED` 수명 관리의 함정을 진단할 수 있다.

**더 읽을 거리**: [Microsoft Learn: I/O Completion Ports](https://learn.microsoft.com/en-us/windows/win32/fileio/i-o-completion-ports), [Microsoft Learn: GetQueuedCompletionStatusEx](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatusex), [Microsoft Learn: CreateThreadpoolIo](https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-createthreadpoolio), [Microsoft Learn: CreateIoRing](https://learn.microsoft.com/en-us/windows/win32/api/ioringapi/nf-ioringapi-createioring).

**이전 장**: [io_uring 심화](/post/io-optimization/io-uring-advanced-deep-dive/) (챕터 03)

완료 기반 I/O로 시스템콜을 줄였다면, 다음 단계는 커널과 사용자 공간 사이의 **복사 자체**를 줄이는 것입니다. 다음 장에서는 `sendfile`·`splice`·`copy_file_range` 등 zero-copy 기법으로 데이터가 페이지 캐시와 소켓 버퍼 사이를 오갈 때 발생하는 불필요한 복사를 제거하는 방법을 다룹니다.

→ [Zero-copy 기법](/post/io-optimization/zero-copy-sendfile-splice-copy-file-range/) (챕터 05)
