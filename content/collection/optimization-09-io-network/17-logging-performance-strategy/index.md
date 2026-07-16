---
collection_order: 17
date: 2026-07-14
lastmod: 2026-07-14
draft: false
image: wordcloud.png
title: "[IO 09] 로깅 성능 전략"
slug: logging-performance-strategy-async-logger
description: "로깅이 핫패스 지연에 미치는 비용을 락 경합·문자열 포맷팅·시스템 콜 진입·flush 정책으로 분해하고, 비동기 로거의 링 버퍼·배치 flush 설계와 로그 레벨 분리가 I/O에 미치는 영향을 NanoLog·spdlog 사례로 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - IO(Input/Output)
  - OS(운영체제)
  - Linux(리눅스)
  - C++
  - C
  - Concurrency(동시성)
  - Benchmark
  - Latency
  - Throughput
  - Profiling(프로파일링)
  - Implementation(구현)
  - Best-Practices
  - System-Design
  - Backend(백엔드)
  - Production
  - Reliability
  - Logging(로깅)
  - Guide(가이드)
  - Reference(참고)
  - Advanced
  - Comparison(비교)
  - Pitfalls(함정)
  - Documentation(문서화)
  - Async-Logger
  - Ring-Buffer
  - Lock-Free-Queue
  - NanoLog
  - spdlog
  - Log-Levels
  - Hot-Path
  - Batching
  - Backpressure
  - SPSC-Queue
---

**로깅 성능 전략**이란 애플리케이션이 실행 중 남기는 로그 메시지가 핫패스의 지연시간과 처리량에 주는 영향을, 로깅 경로 자체의 설계(호출 지점의 비용, 버퍼링 방식, 실제 I/O를 수행하는 시점)를 통해 최소화하는 접근을 말합니다. 로그는 장애 원인을 사후에 재구성하기 위한 사실상 유일한 기록이지만, 초당 수십만~수백만 건의 이벤트를 처리하는 매칭 엔진이나 시장 데이터 처리기에서는 로그 한 줄을 기록하는 데 걸리는 몇 마이크로초가 전체 지연 예산을 잠식할 수 있습니다. 이 장은 "로그를 켜둘 것인가 끌 것인가"라는 이분법 대신, 핫패스에서 지불하는 비용의 구성 요소를 분해하고 그 비용을 실제 I/O 경로 밖으로 옮기는 설계를 다룹니다.

## 이 장을 읽기 전에

**선행 지식**: 이 장은 [01장: I/O 비용 직관](/post/io-optimization/io-cost-intuition-sync-async-copy-fundamentals/)에서 다룬 "동기/비동기와 복사 횟수가 지연에 미치는 그림"과 [1장: I/O 패턴과 비용](/post/io-optimization/io-patterns-blocking-nonblocking-cost-model/)에서 다룬 시스템 콜 진입 비용·대기 방식 모델을 전제로 합니다. 스레드 간 동기화(뮤텍스, 원자적 연산)의 기본 개념도 필요합니다. **이 장의 깊이**: **중급**입니다. 동기 로깅이 핫패스에서 지불하는 비용의 종류, 로그 레벨 분리가 I/O에 미치는 영향, 비동기 로거의 링 버퍼·배치 설계를 다룹니다. **다루지 않는 것**: 특정 로깅 라이브러리(spdlog, glog, quill 등)의 전체 API 튜토리얼, 로그 수집·색인·검색 인프라(ELK 스택 등 중앙화 로깅 파이프라인), 여러 스레드가 같은 로그 파일에 `flock`으로 잠그는 상황의 세부 비용([15장: File Locking 성능](/post/io-optimization/file-locking-performance-impact-alternatives/)에서 다룹니다), WAL·fsync 기반 내구성 보장 전략([14장: Database I/O 패턴](/post/io-optimization/database-io-wal-fsync-journaling-strategy/)에서 다룹니다)입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "로그가 왜 병목이 되는가" ~ "동기 로깅의 핫패스 비용 분해" | 로깅이 지연에 끼어드는 지점을 구성 요소로 나눠 이해 |
| **중급자** | "로그 레벨 분리와 I/O 영향" ~ "비동기 로거의 구조" | 레벨 필터링과 비동기 큐로 핫패스 비용을 옮기는 방법 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 백프레셔 정책·유실 위험을 워크로드 SLA에 맞춰 판단 |

---

## 로그가 왜 병목이 되는가 (역사·배경)

초기 유닉스 프로그램은 디버깅을 위해 `printf`/`fprintf`를 표준 출력이나 파일에 직접 썼고, 이 호출은 그 자리에서 포맷팅과 `write` 시스템 콜을 모두 수행했습니다. 여러 프로세스가 로그를 남겨야 하는 서버 환경이 늘면서 4.2BSD(1983)는 `syslog()`를 도입해 로그 메시지를 별도의 데몬(`syslogd`)으로 보내는 방식을 표준화했습니다([man7.org: syslog(3)](https://man7.org/linux/man-pages/man3/syslog.3.html)). 이 구조는 "로그를 남기는 호출자"와 "실제로 디스크에 쓰는 주체"를 분리한다는 점에서 이후 비동기 로거의 원형이라 할 수 있습니다. 2000년대 들어 Log4j 계열은 `AsyncAppender`로 애플리케이션 스레드용 로깅 API와 실제 출력을 큐로 분리하는 패턴을 널리 퍼뜨렸고, C++ 진영에서는 spdlog(2014~)가 헤더 전용 라이브러리로 동일한 패턴(스레드 풀 기반 비동기 로거)을 제공하기 시작했습니다([GitHub: gabime/spdlog](https://github.com/gabime/spdlog)). 2018년 스탠퍼드 연구진이 발표한 NanoLog는 한 걸음 더 나아가, 로그 문자열의 정적인 부분을 **컴파일 타임에 미리 분해**하고 런타임에는 가변 인자만 압축된 이진 형식으로 기록한 뒤 오프라인 도구로 재조립하는 방식을 제안해, 호출당 오버헤드를 한 자릿수 나노초 수준까지 낮췄다고 보고합니다([GitHub: PlatformLab/NanoLog](https://github.com/PlatformLab/NanoLog)). 이 흐름은 공통적으로 "로그를 남기는 지점"과 "로그를 실제로 저장 매체에 쓰는 지점"을 최대한 멀리 떼어놓는 방향으로 수렴합니다.

## 동기 로깅의 핫패스 비용 분해

동기 로깅 호출 하나가 핫패스 스레드에서 실제로 지불하는 비용은 최소 네 가지로 나눌 수 있습니다. 첫째, **락 경합**입니다. 여러 스레드가 같은 로그 파일 핸들이나 로거 객체를 공유하면 뮤텍스로 직렬화되고, 스레드 수가 늘수록 대기 시간이 커집니다. 둘째, **문자열 포맷팅과 힙 할당**입니다. `operator+`나 `std::ostringstream`으로 로그 라인을 조립하면 매 호출마다 임시 문자열과 할당이 발생하며, 이는 C++ 언어 트랙에서 다루는 문자열 반복 연결 비용과 정확히 같은 구조의 문제입니다. 셋째, **시스템 콜 진입 비용**입니다. `write`는 [1장](/post/io-optimization/io-patterns-blocking-nonblocking-cost-model/)에서 다룬 것과 동일한 사용자-커널 전환 비용을 매 호출마다 지불합니다. 넷째, **flush 정책**입니다. 매 줄마다 `fflush`나 `fsync`를 호출하면 커널이 버퍼를 실제로 디스크(또는 파이프)에 밀어내는 비용까지 매번 지불하게 되어, 사실상 로그 한 줄이 동기 I/O 한 번과 같아집니다.

이 네 가지가 겹친 전형적인 안티패턴과, 그 원인을 코드로 확인해 보겠습니다.

```cpp
// bad_sync_logger.cpp — 안티패턴: 매 호출마다 락 + 문자열 조립 + 강제 flush
// g++ -O2 -std=c++17 -pthread bad_sync_logger.cpp -o bad_sync_logger
#include <cstdio>
#include <mutex>
#include <string>

std::mutex log_mutex;
FILE* log_file = std::fopen("app.log", "a");

void log_trade(int order_id, double price, int qty) {
  std::lock_guard<std::mutex> lock(log_mutex);  // (1) 호출 스레드 전체가 직렬화됨
  std::string line = "order=" + std::to_string(order_id) +
                      " price=" + std::to_string(price) +
                      " qty=" + std::to_string(qty) + "\n";  // (2) 매 호출마다 임시 문자열·힙 할당
  std::fwrite(line.data(), 1, line.size(), log_file);        // (3) write 진입 비용
  std::fflush(log_file);  // (4) 매 줄마다 커널로 강제 flush — 사실상 동기 I/O 한 번
}
```

원인을 정리하면, 이 함수는 로그 한 줄마다 "락 대기 + 문자열 할당 + 시스템 콜 + 강제 flush"라는 네 가지 비용을 모두 핫패스 스레드가 직접 떠안는 구조입니다. 호출 빈도가 낮으면 문제되지 않지만, 초당 수만 건 이상 호출되는 경로에서는 이 네 비용이 그대로 지연 분포의 꼬리(tail latency)를 키웁니다. 해결의 핵심은 "핫패스 스레드가 하는 일"을 로그 레코드를 큐에 넣는 것만으로 줄이고, 나머지 세 비용(포맷팅·시스템 콜·flush)을 별도 스레드로 옮기는 것입니다.

## 로그 레벨 분리와 I/O 영향

로그 레벨(TRACE/DEBUG/INFO/WARN/ERROR)을 나누는 목적은 "필요한 상세도만 실제로 저장 매체까지 내려보내는 것"입니다. 여기서 자주 놓치는 부분은 **필터링이 언제 일어나는가**입니다. 런타임에 `if (level >= current_level) log(...)`처럼 검사 자체는 있지만 `log(...)`의 인자를 함수 호출 규약대로 먼저 평가한다면, 인자를 만드는 데 드는 비용(문자열 포맷, 객체를 문자열로 변환하는 `to_string` 호출 등)은 레벨과 무관하게 이미 지불된 뒤입니다. 매크로나 지연 평가(lazy evaluation, 람다·표현식 템플릿)로 감싸 레벨 검사를 통과하지 못하면 인자 평가 자체를 건너뛰게 만들어야 진짜 이득이 생깁니다. 더 극단적으로는 컴파일 타임에 특정 레벨 이하를 코드에서 아예 제거하는 방식(빌드 매크로로 `if constexpr` 분기 또는 매크로 확장을 빈 문장으로 치환)을 쓰면, 프로덕션 빌드에는 디버그 로그 호출의 흔적조차 남지 않습니다. 로그 레벨이 I/O에 미치는 영향은 결국 "얼마나 많은 바이트가 실제로 `write` 시스템 콜까지 도달하는가"로 귀결되며, 레벨을 낮춰도 인자 평가와 포맷팅이 살아있다면 I/O 이전 단계의 비용은 그대로 남는다는 점을 구분해야 합니다.

## 비동기 로거의 구조

**비동기 로거**의 핵심 아이디어는 핫패스 스레드(생산자)가 로그 레코드를 **락 없는 큐**에 밀어넣기만 하고, 실제 포맷팅·시스템 콜·flush는 별도의 백그라운드 스레드(소비자)가 배치로 처리하도록 분리하는 것입니다. 이렇게 하면 핫패스가 지불하는 비용은 큐에 값을 복사하는 몇 나노초 수준으로 줄고, 나머지 세 비용은 지연 예산에서 자유로운 백그라운드 스레드로 옮겨갑니다. 다음은 단일 생산자-단일 소비자(SPSC) 링 버퍼를 이용한 개념 골격입니다.

```cpp
// async_logger.h — 개념 스켈레톤: 핫패스는 push만, 백그라운드 스레드가 실제 I/O 수행
#include <array>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>

struct LogRecord { int order_id; double price; int qty; };

template <size_t N>
class SpscRingBuffer {
 public:
  bool push(const LogRecord& r) {
    size_t head = head_.load(std::memory_order_relaxed);
    size_t next = (head + 1) % N;
    if (next == tail_.load(std::memory_order_acquire)) return false;  // 큐 가득참
    buf_[head] = r;
    head_.store(next, std::memory_order_release);
    return true;
  }
  bool pop(LogRecord& out) {
    size_t tail = tail_.load(std::memory_order_relaxed);
    if (tail == head_.load(std::memory_order_acquire)) return false;  // 빔
    out = buf_[tail];
    tail_.store((tail + 1) % N, std::memory_order_release);
    return true;
  }
 private:
  std::array<LogRecord, N> buf_{};
  std::atomic<size_t> head_{0}, tail_{0};
};

inline SpscRingBuffer<1 << 16> g_queue;
inline std::atomic<bool> g_running{true};
inline std::atomic<uint64_t> g_dropped{0};

void log_trade_hot_path(int order_id, double price, int qty) {
  if (!g_queue.push({order_id, price, qty})) {
    g_dropped.fetch_add(1, std::memory_order_relaxed);  // 정책: drop + 카운터 (아래 판단 기준 참고)
  }
}

void logger_thread_main(FILE* out) {
  LogRecord r;
  char line[128];
  while (g_running.load(std::memory_order_relaxed)) {
    bool drained_any = false;
    while (g_queue.pop(r)) {
      int n = std::snprintf(line, sizeof(line), "order=%d price=%.2f qty=%d\n",
                             r.order_id, r.price, r.qty);
      std::fwrite(line, 1, static_cast<size_t>(n), out);
      drained_any = true;
    }
    if (drained_any) std::fflush(out);  // 배치로 모아 flush 횟수를 최소화
    else std::this_thread::sleep_for(std::chrono::microseconds(200));
  }
}
```

핫패스 함수 `log_trade_hot_path`는 원자적 연산 몇 개로 이루어진 `push` 하나만 호출하므로, 포맷팅·락·시스템 콜·flush를 모두 백그라운드 스레드로 미룬 상태입니다. 소비자 스레드는 큐를 비운 뒤에만 `fflush`를 한 번 호출해, 앞서의 안티패턴이 매 줄마다 지불하던 flush 비용을 배치 단위로 나눕니다. 다만 이 구조는 두 가지를 명시적으로 결정해야 합니다. 큐가 가득 찼을 때 무엇을 할지(여기서는 drop-with-counter를 선택했습니다), 그리고 프로세스가 크래시할 때 큐에 남아 있던 레코드는 유실된다는 사실입니다. 두 흐름을 그림으로 정리하면 다음과 같습니다.

```mermaid
flowchart LR
  hotPath["핫패스 스레드</br>(주문 처리 등)"]
  ringBuffer["Lock-free 링 버퍼"]
  loggerThread["백그라운드 로거 스레드"]
  diskFile["로그 파일"]
  hotPath -->|"push(LogRecord)"| ringBuffer
  ringBuffer -->|"배치 pop"| loggerThread
  loggerThread -->|"snprintf + write 배치"| diskFile
  ringBuffer -.->|"큐 가득참: drop/counter"| hotPath
```

**두 방식의 호출당 비용 차이**를 격리해서 측정하면 다음과 같습니다. 아래는 앞서의 `log_trade`(동기, 락+fflush)와 `log_trade_hot_path`(비동기, 링 버퍼 push)를 같은 조건으로 반복 호출해 비교하는 Google Benchmark 코드입니다.

```cpp
// bench_logging.cpp — g++ -O2 -pthread bench_logging.cpp -lbenchmark -lpthread
#include <benchmark/benchmark.h>
#include "async_logger.h"  // log_trade_hot_path 선언 포함, log_trade는 별도 헤더로 분리했다고 가정

static void BM_SyncLockFlushLog(benchmark::State& state) {
  for (auto _ : state) {
    log_trade(1, 101.25, 100);
  }
}
BENCHMARK(BM_SyncLockFlushLog);

static void BM_AsyncRingBufferPush(benchmark::State& state) {
  for (auto _ : state) {
    log_trade_hot_path(1, 101.25, 100);
  }
}
BENCHMARK(BM_AsyncRingBufferPush);

BENCHMARK_MAIN();
```

절대 수치는 CPU 세대·커널 버전·디스크(또는 tmpfs) 조합에 따라 달라지므로 반드시 대상 환경에서 재현해야 하지만, 방향성은 분명합니다. NanoLog의 자체 비교 표는 정적으로 문자열을 컴파일 타임에 분해하는 방식이 spdlog·glog·Log4j2 대비 호출당 수십 배에서 수백 배 낮은 지연을 낸다고 보고합니다.

> "Nanolog is an extremely performant nanosecond scale logging system for C++ that exposes a simple printf-like API and achieves over 80 million logs/second at a median latency of just over 7 nanoseconds." — [GitHub: PlatformLab/NanoLog README](https://github.com/PlatformLab/NanoLog) (Yang, Park, Ousterhout, USENIX ATC 2018 연구의 구현체 저장소).

이 장의 SPSC 링 버퍼 방식은 NanoLog만큼 극단적이지는 않지만(문자열을 컴파일 타임에 분해하지 않고 구조체를 그대로 복사하므로), 매 호출마다 락과 flush를 지불하는 동기 방식보다는 한 자릿수~두 자릿수 배 낮은 호출당 비용을 기대할 수 있습니다. `perf stat -e futex-wait`나 `strace -c -e write,fsync`로 락 대기·시스템 콜 횟수를 실측해 교차 검증하는 것이 좋습니다.

## 흔한 오개념

**"로그 레벨만 낮추면 핫패스 비용이 사라진다"**는 정확하지 않습니다. 레벨 검사가 인자 평가보다 나중에 일어나는 구조라면, 걸러진 로그도 포맷팅·객체 변환 비용을 이미 지불한 뒤입니다. 지연 평가나 컴파일 타임 제거 없이 레벨만 조정하는 것은 I/O 이전 단계의 비용을 그대로 남겨둡니다.

**"비동기 로깅은 항상 안전(무손실)하다"**는 것도 흔한 오해입니다. 큐가 가득 차거나 프로세스가 크래시하면 아직 소비되지 않은 레코드는 유실됩니다. 감사·컴플라이언스 목적으로 "반드시 남아야 하는" 로그는 순수 비동기 drop 정책이 아니라, [14장](/post/io-optimization/database-io-wal-fsync-journaling-strategy/)에서 다루는 그룹 커밋·fsync 기반의 내구성 보장과 유사한 전략이 필요합니다.

**"printf 계열이 iostream보다 항상 빠르다"** 또는 반대로 **"로깅 자체가 항상 병목이다"**라는 일반화도 과합니다. 실제 비용은 호출 빈도, 락 경합 여부, flush 정책의 조합에서 나오며, 호출 빈도가 낮은 초기화 코드에서는 어떤 방식을 써도 차이가 무의미합니다. 프로파일러로 실제 호출 빈도와 지연 기여도를 먼저 확인한 뒤 최적화 대상을 정하는 것이 순서입니다.

## 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 초당 수만 건 이상 로그가 발생하는 핫패스 | 링 버퍼 기반 비동기 로거 + 배치 flush | 매 호출마다 락 + `fflush` |
| 감사·컴플라이언스용 필수 보존 로그 | 동기 기록 또는 그룹 커밋형 내구성 전략(→[14장](/post/io-optimization/database-io-wal-fsync-journaling-strategy/)) | 순수 drop 정책의 비동기 큐 |
| 여러 스레드가 같은 로그 파일에 직접 기록 | 전용 로거 스레드로 단일화해 락 경합 제거 | 스레드마다 개별 lock+write (→[15장](/post/io-optimization/file-locking-performance-impact-alternatives/)) |
| 디버그 레벨 로그가 프로덕션 빌드에도 존재 | 컴파일 타임 매크로/`if constexpr`로 호출 자체 제거 | 런타임 `if`만으로 인자 평가는 방치 |
| 큐 오버플로우 정책이 미정 | drop-with-counter 또는 명시적 백프레셔(블로킹 여부를 SLA로 결정) | 정책 없이 무한정 블로킹하며 핫패스로 전파 |

## 비판적 시각: 한계와 트레이드오프

비동기 로깅은 핫패스 비용을 줄이는 대신 몇 가지를 대가로 치릅니다. 첫째, 프로세스가 크래시하면 링 버퍼에 남아 있던 마지막 몇 줄이 유실될 수 있어, 정작 장애 직전 상황을 재구성해야 할 때 가장 필요한 로그가 사라지는 역설이 생깁니다. 일부 로거는 시그널 핸들러에서 flush를 시도하지만, 시그널 핸들러 안에서 안전하게 호출할 수 있는 함수(async-signal-safe)가 제한적이라 완전한 해결책은 아닙니다. 둘째, 백그라운드 로거 스레드도 결국 같은 머신의 코어와 캐시 대역폭을 공유하므로 "공짜"가 아니며, NUMA 환경에서는 로거 스레드의 코어 배치가 핫패스 스레드의 캐시 지역성에 영향을 줄 수 있습니다. 셋째, NanoLog류의 컴파일 타임 정적 로그 압축은 극단적인 성능을 내는 대신 런타임에 임의로 조합한 문자열을 그대로 기록하는 유연성을 희생하고, 로그를 사람이 읽으려면 오프라인 재조립 도구를 거쳐야 해 운영 파이프라인이 한 단계 늘어납니다. 마지막으로, drop 정책과 블로킹 정책 사이의 선택 자체가 "관측성을 희생할 것인가, 핫패스 지연을 희생할 것인가"라는 트레이드오프이며, 이 장에서 제시한 판단 기준표는 출발점일 뿐 워크로드의 실제 SLA로 검증해야 합니다.

## 마무리

이 장을 읽고 나면 다음을 스스로 확인할 수 있어야 합니다.

- [ ] 동기 로깅 호출이 핫패스에서 지불하는 네 가지 비용(락 경합, 포맷팅/할당, 시스템 콜 진입, flush)을 구분해 설명할 수 있다.
- [ ] 로그 레벨 필터링이 인자 평가보다 먼저 일어나야 실제 이득이 생긴다는 점을 설명할 수 있다.
- [ ] 링 버퍼 기반 비동기 로거가 핫패스 비용을 소비자 스레드로 옮기는 구조를 코드로 그릴 수 있다.
- [ ] "비동기 로깅=항상 안전"이라는 오개념을 교정하고, 크래시 시 유실 위험과 백프레셔 정책의 트레이드오프를 설명할 수 있다.
- [ ] 워크로드 특성(빈도, 보존 요구, 스레드 경합)에 따라 동기/비동기 로깅 전략을 판단 기준표로 선택할 수 있다.

이 장으로 이 트랙(Low-latency I/O 최적화)의 세부 챕터를 마칩니다. **다음으로 이어갈 곳**은 전체 시리즈의 다른 트랙입니다. I/O 경로에서 확보한 지연 예산을 CPU·메모리 쪽으로 더 밀어붙이고 싶다면 프로파일링 방법론을 다루는 [프로파일링·성능 분석 트랙](/post/profiling-analysis/getting-started-profiling-performance-analysis-fundamentals/)이나 할당 전략을 다루는 [메모리·할당 트랙](/post/memory-optimization/getting-started-memory-allocation-data-layout-tuning/)으로, 로그가 네트워크로 전송되는 경로까지 최적화하려면 네트워크 최적화 트랙으로 넘어가는 것을 권장합니다.

→ [Low-latency 최적화 시리즈 개요](/post/low-latency-optimization-series/getting-started-low-latency-optimization-series-overview/)
