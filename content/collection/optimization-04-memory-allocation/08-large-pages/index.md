---
collection_order: 8
date: 2026-07-13
lastmod: 2026-10-23
draft: false
image: wordcloud.png
title: "[Memory 04] Large Pages·Huge Pages"
slug: huge-pages-large-pages-mthp
description: "HugeTLB와 THP(Transparent Huge Pages)의 동작 원리, madvise 모드별 선택 기준, 채택이 넓어지고 있는 mTHP(multi-size THP)까지 TLB 미스·페이지 폴트 관점에서 판단 기준과 벤치마크로 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - Memory(메모리)
  - Cache
  - CPU(Central Processing Unit)
  - C++
  - OS(운영체제)
  - Linux(리눅스)
  - Windows(윈도우)
  - Benchmark
  - Latency
  - Profiling(프로파일링)
  - Best-Practices
  - Advanced
  - Deep-Dive
  - Pitfalls(함정)
  - Hardware(하드웨어)
  - Kernel
  - Huge-Pages
  - THP
  - mTHP
  - HugeTLB
  - madvise
  - khugepaged
  - TLB
  - Virtual-Memory
---

<strong>Large Pages(대형 페이지, Huge Pages)</strong>란 가상 주소를 물리 주소로 변환할 때 TLB(Translation Lookaside Buffer) 엔트리 하나가 담당하는 메모리 범위를 표준 4KB 대신 x86-64 기준 2MB·1GB, 또는 아키텍처별로 정의된 더 큰 단위로 확장해 페이지 테이블 계층을 순회하는 비용과 TLB 미스 빈도를 줄이는 메모리 관리 기법을 말합니다. 핫패스가 수백 메가바이트에서 수 기가바이트 크기의 버퍼를 랜덤에 가깝게 순회할 때, 4KB 페이지 하나로는 TLB가 커버하는 주소 범위(TLB reach)가 금방 바닥나 페이지 워크(page walk)가 접근마다 반복되고, 이 비용은 µs 단위 예산을 조용히 갉아먹는 지연으로 쌓입니다. 이 장에서는 관리자가 정적으로 예약하는 HugeTLB, 커널이 자동으로 관리하는 THP(Transparent Huge Pages), 그리고 채택이 넓어지고 있는 mTHP(multi-size THP)를 각각 언제 선택하고 언제 피할지 다룹니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [07장: 구조체 패딩과 정렬](/post/memory-optimization/struct-padding-alignment-optimization/)에서 다룬 캐시 라인·정렬 개념과, [15장: 메모리·수명·캐시 라인 직관](/post/memory-optimization/memory-lifetime-cache-line-intuition-fundamentals/)에서 다룬 가상 메모리·페이지의 기본 그림을 전제로 합니다. "페이지 테이블"과 "TLB"가 무엇인지, 가상 주소가 물리 주소로 바뀌는 대략의 흐름만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **심화** 난이도로, HugeTLB와 THP의 구조적 차이부터 시작해 `madvise` 모드별 실전 선택, 그리고 2025–2026년 커널·표준 라이브러리에서 실무 채택이 넓어지고 있는 mTHP까지를 다룹니다. **다루지 않는 것**: NUMA 노드별 대형 페이지 배치는 [09장: NUMA 메모리 할당·지역성](/post/memory-optimization/numa-memory-allocation-locality/)에서, `madvise`의 다른 힌트(`MADV_DONTNEED`, `MADV_FREE` 등)와 ARM MTE는 [13장: Virtual Memory 관리 힌트](/post/memory-optimization/virtual-memory-hints-madvise-mte/)에서, 큰 버퍼를 미리 확보해 두는 아레나 설계 자체는 [02장: 할당 전략](/post/memory-optimization/pool-arena-allocation-strategy/)에서 다룹니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "Huge Pages 도입 배경" ~ "HugeTLB: 정적 대형 페이지" | TLB reach와 페이지 워크가 지연에 기여하는 원리 이해 |
| **중급자** | "THP: 투명 대형 페이지와 madvise 모드" ~ "측정: TLB 미스와 페이지 폴트로 확인하기" | madvise 모드별 차이와 실측 방법 습득 |
| **전문가** | "mTHP" ~ "비판적 시각" | mTHP 적용 판단과 THP의 tail latency 트레이드오프 평가 |

---

## Huge Pages 도입 배경

HugeTLB는 Linux에서 오래전부터 존재해 온 기능으로, 관리자가 부팅 파라미터나 `/proc/sys/vm/nr_hugepages` sysctl로 대형 페이지 풀을 미리 예약해 두면 `hugetlbfs`를 마운트하거나 `MAP_HUGETLB` 플래그로 그 풀에서 페이지를 떼어 쓰는 방식입니다. THP(Transparent Huge Pages)는 이후 Linux 2.6.38에서 등장했고(`madvise(2)` 매뉴얼이 `MADV_HUGEPAGE`를 2.6.38부터로 표기), 관리자 개입 없이 `khugepaged` 데몬이 백그라운드에서 인접한 4KB 페이지들을 찾아 2MB PMD(Page Middle Directory) 크기로 자동 병합(collapse)하는 방식을 취합니다. 같은 릴리스에서 `MADV_HUGEPAGE`·`MADV_NOHUGEPAGE` 플래그가 함께 도입되어, 애플리케이션이 특정 영역에 대해서만 THP 후보 여부를 힌트로 줄 수 있게 되었습니다.

전통적 THP는 2MB(x86-64 PMD 크기) 한 가지만 다뤘기 때문에, 4KB보다는 훨씬 크지만 2MB에는 못 미치는 할당(64KB–512KB급 버퍼 등)은 콜랩스 대상이 되지 못하고 그대로 4KB로 남는 경우가 많았습니다. multi-size THP(mTHP)가 이 틈을 겨냥해 6.x 계열 커널에서 도입되었고, 크기별 sysfs 인터페이스가 추가되었습니다. 현행 [커널 문서](https://docs.kernel.org/admin-guide/mm/transhuge.html)에 따르면 `khugepaged`는 기본 페이지를 PMD 크기뿐 아니라 mTHP 크기로도 콜랩스할 수 있지만, 설정 조건(후술)이 붙고 커널 버전에 따라 지원 범위가 다릅니다. Windows에서도 `VirtualAlloc`에 `MEM_LARGE_PAGES`를 지정하고 `SeLockMemoryPrivilege` 권한을 확보하면 대형 페이지를 예약할 수 있지만, 이는 HugeTLB에 가까운 정적 모델이며 THP처럼 커널이 자동으로 콜랩스해 주는 투명한 메커니즘은 아닙니다.

## HugeTLB: 정적 대형 페이지

**HugeTLB**는 관리자가 미리 정해 둔 개수만큼의 대형 페이지를 부팅 시 또는 런타임에 예약해 두는 풀 기반 메커니즘입니다. `nr_hugepages`로 예약된 페이지는 `HugePages_Rsvd`(예약)와 실제 사용량이 구분되어 관리되며, 한 번 예약된 페이지는 스왑되지 않고(pinned) 다른 용도로 전용되지도 않습니다. 이 예측 가능성 때문에 데이터베이스 버퍼 풀, JVM 힙, RDMA 등록 메모리처럼 "이 크기만큼은 절대 스왑되면 안 된다"는 요구가 있는 워크로드에 적합합니다.

애플리케이션에서는 `hugetlbfs`를 마운트해 그 위에 파일을 만들고 `mmap`하거나, 익명 매핑에 `MAP_HUGETLB` 플래그를 추가해 접근합니다. 아래 코드는 사전에 예약된 HugeTLB 풀에서 256MB를 요청하는 최소 예제입니다.

```cpp
#include <sys/mman.h>
#include <cstdio>
#include <cstdlib>

int main() {
  constexpr size_t kSize = 256ull << 20;  // 256MB, 2MB HugeTLB 페이지 128개에 해당
  void* p = mmap(nullptr, kSize, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB, -1, 0);
  if (p == MAP_FAILED) {
    perror("mmap(MAP_HUGETLB)");  // nr_hugepages 예약이 부족하면 여기서 실패한다
    return EXIT_FAILURE;
  }
  munmap(p, kSize);
  return EXIT_SUCCESS;
}
```

이 코드는 `nr_hugepages`가 요청량만큼 미리 예약되어 있어야만 성공합니다. 예약된 페이지는 실제로 쓰이지 않아도 물리 메모리를 점유하므로, 예약량을 과도하게 잡으면 다른 프로세스가 쓸 수 있는 메모리가 그만큼 줄어든다는 트레이드오프가 있습니다.

## THP: 투명 대형 페이지와 madvise 모드

**THP**는 `/sys/kernel/mm/transparent_hugepage/enabled`가 `always`·`madvise`·`never` 중 무엇으로 설정되어 있는지에 따라 동작 범위가 달라집니다. `always`는 시스템 전역에서 THP를 시도하고, `madvise`는 `MADV_HUGEPAGE`로 명시적으로 표시된 영역에만 적용하며, `never`는 완전히 끕니다. 여기에 `defrag` 설정(`always`/`defer`/`defer+madvise`/`madvise`/`never`)이 더해져, THP를 만들 물리 메모리가 부족할 때 즉시 직접 회수·압축을 수행할지 아니면 백그라운드로 미룰지를 결정합니다. `MADV_COLLAPSE`(Linux 6.1 이상)는 전역 정책과 무관하게 지정한 범위를 동기적으로 즉시 콜랩스하도록 강제하는 별도의 힌트입니다.

애플리케이션 코드에서는 전역 정책이 `madvise`일 때만 의미가 있는 `MADV_HUGEPAGE` 힌트를 특정 버퍼에만 선택적으로 걸어 줄 수 있습니다.

```cpp
#include <sys/mman.h>

#include <cstddef>

// 성공하면 0, 실패하면 -1(errno 설정). 힌트라서 실패해도 프로그램은 4KB 페이지로 계속 동작한다.
int mark_hot_arena_for_thp(void* addr, std::size_t len) {
  // 전역 정책이 madvise일 때만 유효한 힌트: 이 영역만 THP 후보로 표시한다
  return madvise(addr, len, MADV_HUGEPAGE);
}
```

전역 정책이 `never`면 이 힌트는 그냥 무시되고, `always`면 이미 모든 영역이 후보이므로 호출 자체는 무해하지만 별다른 효과도 없습니다. 즉 이 힌트는 "전역은 보수적으로 두고, 정말 큰 이득이 예상되는 버퍼만 골라서 켠다"는 `madvise` 정책과 짝을 이룰 때 가장 유용합니다.

```mermaid
flowchart TD
  request["대용량 버퍼 접근 시작"] --> policy{"THP enabled 정책"}
  policy -->|"never"| basePage["4KB 기본 페이지</br>TLB reach 작음"]
  policy -->|"madvise + MADV_HUGEPAGE"| fault["페이지 폴트 시점에</br>활성화된 크기로 할당 시도"]
  policy -->|"always"| fault
  fault --> sizeCheck{"연속 물리 페이지 확보 가능?"}
  sizeCheck -->|"2MB 확보"| pmdHuge["PMD 크기 THP</br>2MB 매핑"]
  sizeCheck -->|"작은 mTHP 크기 확보"| mthp["mTHP</br>크기별 sysfs로 설정"]
  sizeCheck -->|"확보 실패"| basePage
  basePage -.->|"이후 조건이 맞으면"| collapse["khugepaged가 스캔해</br>PMD 또는 mTHP 크기로 콜랩스"]
```

현재 THP로 실제 매핑되어 있는지는 `/proc/<pid>/smaps`의 `AnonHugePages` 필드로 확인할 수 있습니다. 커널 문서는 이 필드가 역사적 이유로 전통적인 PMD 크기 THP만 집계하며 `AnonHugePmdMapped`라고 불렸어야 했다고 설명합니다.

```bash
cat /sys/kernel/mm/transparent_hugepage/enabled
grep AnonHugePages /proc/self/smaps_rollup
```

## mTHP: 여러 크기를 지원하는 THP

<strong>mTHP(multi-size THP)</strong>는 앞서 언급한 "4KB와 2MB 사이의 틈"을 메우기 위해 16KB·32KB·64KB처럼 2의 거듭제곱 크기의 huge page를 개별적으로 켜고 끌 수 있게 확장한 기능입니다. 각 크기는 `/sys/kernel/mm/transparent_hugepage/hugepages-<size>kB/enabled` 경로에서 `always`·`madvise`·`never`·`inherit`(상위 전역 값을 따름) 중 하나로 독립 설정됩니다. 기본값은 PMD 크기만 `inherit`이고 나머지 크기는 `never`이므로, mTHP는 명시적으로 옵트인해야만 동작합니다.

```bash
for f in /sys/kernel/mm/transparent_hugepage/hugepages-*kB/enabled; do
  echo "$f: $(cat "$f")"
done
```

위 스크립트로 나열되는 각 크기별 파일에 원하는 정책을 써 넣으면 되지만, 주의할 점이 있습니다. 커널 문서에 따르면 `MADV_COLLAPSE`(`madvise_collapse`)는 PMD 크기 THP로만 콜랩스하고 mTHP 콜랩스는 시도하지 않으며, `khugepaged`의 mTHP 콜랩스는 `max_ptes_none`이 0 또는 `HPAGE_PMD_NR - 1`일 때만 지원되고 공유되었거나 스왑된 페이지가 들어 있는 영역은 건너뜁니다. mTHP를 활용해 할당 정책 자체를 크기별로 나누고 싶다면 [16장: 전역 할당자·jemalloc·tcmalloc](/post/memory-optimization/global-allocator-jemalloc-tcmalloc-tuning-expert/)에서 다루는 아레나 단위 튜닝과 함께 검토하는 것이 자연스럽습니다.

## 측정: TLB 미스와 페이지 폴트로 확인하기

Huge page 적용 효과는 주장이 아니라 측정으로 확인해야 합니다. 아래는 큰 익명 매핑을 만들어 캐시 라인 단위 랜덤 접근을 반복하면서, 인자로 THP 힌트 사용 여부를 바꾸는 최소 벤치마크입니다. 끝에서 `/proc/self/smaps_rollup`의 `AnonHugePages`를 읽어 THP가 실제로 적용됐는지도 함께 출력하므로, 시간이 줄었다는 결과와 THP가 켜졌다는 사실을 한 번에 대조할 수 있습니다. Linux(x86-64)에서 `-std=c++17` 이상으로 빌드합니다.

```cpp
#include <sys/mman.h>

#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <random>
#include <string>

// /proc/self/smaps_rollup에서 PMD 크기 THP로 매핑된 양(kB)을 읽는다.
static long anon_huge_kb() {
  std::FILE* f = std::fopen("/proc/self/smaps_rollup", "r");
  if (!f) return -1;
  char line[256];
  long kb = -1;
  while (std::fgets(line, sizeof line, f))
    if (std::sscanf(line, "AnonHugePages: %ld kB", &kb) == 1) break;
  std::fclose(f);
  return kb;
}

int main(int argc, char** argv) {
  constexpr std::size_t kSize = std::size_t{1} << 27;  // 128MiB
  void* buf = mmap(nullptr, kSize, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (buf == MAP_FAILED) { std::perror("mmap"); return 1; }

  const bool use_thp = argc > 1 && std::string(argv[1]) == "thp";
  madvise(buf, kSize, use_thp ? MADV_HUGEPAGE : MADV_NOHUGEPAGE);
  std::memset(buf, 1, kSize);  // 페이지 폴트를 미리 유발해 워밍업 (THP는 이때 할당된다)

  std::mt19937_64 rng(42);
  std::uniform_int_distribution<std::size_t> dist(0, kSize / 64 - 1);
  std::uint64_t sink = 0;
  const auto* base = static_cast<const unsigned char*>(buf);

  constexpr std::size_t kIters = 10'000'000;
  const auto t0 = std::chrono::steady_clock::now();
  for (std::size_t i = 0; i < kIters; ++i) sink += base[dist(rng) * 64];  // 캐시 라인 단위 랜덤 접근
  const auto t1 = std::chrono::steady_clock::now();

  std::printf("mode=%s elapsed_ms=%lld AnonHugePages=%ld kB sink=%llu\n",
              use_thp ? "thp" : "nothp",
              static_cast<long long>(std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count()),
              anon_huge_kb(), static_cast<unsigned long long>(sink));
  munmap(buf, kSize);
  return 0;
}
```

`g++ -O2 -std=c++17 thp_bench.cpp -o thp_bench`로 빌드해 Compiler Explorer의 샌드박스(x86-64 GCC 13.2)에서 `nothp`와 `thp`를 번갈아 세 번씩 실행한 결과는 다음과 같습니다(공유 서버 한 대의 값이므로 절댓값이 아니라 경향으로만 읽습니다).

```text
mode=nothp elapsed_ms=316 AnonHugePages=0 kB sink=10000000
mode=thp elapsed_ms=223 AnonHugePages=131072 kB sink=10000000

mode=nothp elapsed_ms=273 AnonHugePages=0 kB sink=10000001
mode=thp elapsed_ms=225 AnonHugePages=131072 kB sink=10000001

mode=nothp elapsed_ms=270 AnonHugePages=0 kB sink=10000002
mode=thp elapsed_ms=213 AnonHugePages=131072 kB sink=10000002
```

두 번째와 세 번째 실행은 서버가 이전 결과를 재사용하지 않도록 반복 횟수를 1, 2회 늘려서 `sink`가 달라졌습니다(`sink`는 반복 횟수와 같습니다).

`thp` 모드에서만 `AnonHugePages`가 버퍼 크기인 128MiB(131072kB) 전체로 잡혔으므로 THP가 실제로 적용되었고, 랜덤 접근 시간이 세 번 모두 줄었습니다(213–225 ms 대 270–316 ms, 약 18–29%). 반대로 `kSize`를 64MiB, 반복을 5,000,000회로 줄여 한 번 돌렸을 때는 `mode=nothp elapsed_ms=85`, `mode=thp elapsed_ms=110`으로 오히려 `thp`가 느렸는데, 작은 워킹셋에서는 TLB reach 문제가 크지 않고 측정 변동이 이득보다 컸기 때문으로 보입니다. 이 샌드박스에는 `perf`가 없어 TLB 미스 카운터는 재지 못했습니다. 로컬에서는 다음처럼 `dTLB-load-misses`와 `page-faults`를 함께 비교할 수 있고, 수치는 CPU 세대·커널 버전·`enabled`/`defrag` 설정·워킹셋 크기에 따라 크게 달라지므로 직접 재현해야 합니다.

```bash
perf stat -e dTLB-load-misses,page-faults ./thp_bench nothp
perf stat -e dTLB-load-misses,page-faults ./thp_bench thp
```

이 벤치마크는 순수 랜덤 접근이라 huge page의 이득이 과장되게 보일 수 있습니다. 실제 서비스의 접근 패턴이 순차에 가깝다면 TLB 미스 자체가 애초에 적어 개선 폭이 훨씬 작을 수 있으니, 프로파일러로 확인한 실제 워킹셋과 접근 패턴을 재현해서 측정하는 것이 중요합니다. 힙 전체의 페이지·할당 프로파일을 함께 보고 싶다면 [Tr.01 ch20: 메모리 프로파일링: 힙 분석](/post/profiling-analysis/memory-profiling-heap-analysis/)에서 다루는 heaptrack 계열 도구와 병행하는 것을 권장합니다.

## 흔한 오개념

<strong>"THP를 켜면 무조건 빨라진다"</strong>는 흔한 오해입니다. `khugepaged`의 스캔·콜랩스 작업 자체가 CPU 사이클을 쓰고, `defrag=always` 조합에서는 THP 확보를 위해 직접 메모리 압축(compaction)이 할당 경로에 끼어들어 지연 스파이크를 유발할 수 있습니다. 이 때문에 저지연을 요구하는 일부 운영 환경에서는 `enabled=madvise`로 두고 지연에 민감한 버퍼에만 `MADV_HUGEPAGE`를 걸거나, THP는 `never`로 끄고 HugeTLB만 쓰는 구성을 택하기도 합니다. `never`에서는 `MADV_HUGEPAGE`가 무시된다는 점에 주의합니다.

<strong>"Huge Pages는 메모리를 아낀다"</strong>도 정확하지 않습니다. 2MB 페이지 하나에 실제로는 몇 바이트만 쓰이더라도 나머지 공간은 그대로 점유되는 내부 단편화(internal fragmentation)가 발생합니다. 작은 크기의 산발적 할당이 많은 워크로드에 THP나 HugeTLB를 무분별하게 적용하면 오히려 상주 메모리(RSS)가 늘어날 수 있습니다.

<strong>"HugeTLB와 THP는 같은 메커니즘이다"</strong>라는 혼동도 흔합니다. HugeTLB는 관리자가 정적으로 예약해 스왑되지 않는 pinned 풀이고, THP는 커널이 동적으로 콜랩스·디콜랩스하며 필요하면 스왑도 가능한 별개의 서브시스템입니다. 두 메커니즘은 sysfs 인터페이스도, 실패 모드도 다르므로 같은 도구로 취급하면 안 됩니다.

## 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 크기가 고정된 대형 버퍼(DB 버퍼 풀, 공유 메모리, RDMA 등록 영역) | HugeTLB(`hugetlbfs`, `MAP_HUGETLB`) | THP `always`에만 의존 |
| 범용 워크로드, 운영 부담 최소화가 우선 | THP `madvise` + 필요한 버퍼에만 `MADV_HUGEPAGE` | THP `always`(전역 오버커밋 위험) |
| 4KB–2MB 사이 크기의 산발적 버퍼(예: 64KB–512KB) | 대상 크기의 mTHP sysfs 항목을 `madvise`로 활성화 | 전통 THP만 두고 방치(콜랩스 대상이 아님) |
| latency tail이 critical한 서비스(저지연 거래, 실시간 서버) | `enabled=madvise` + 특정 아레나에만 `MADV_HUGEPAGE`, 또는 THP `never` + 명시적 HugeTLB | THP `always` + `defrag=always` |
| 메모리 압박이 심한 컨테이너·공유 호스트 | 신중한 opt-in과 cgroup 단위 모니터링 | 무분별한 전역 `always` 적용 |

## 비판적 시각: 한계와 트레이드오프

mTHP는 THP를 켜느냐 끄느냐의 이분법을 크기별 설정으로 세분화한 발전이지만, 커널·배포판 버전에 따라 sysfs 인터페이스의 세부 동작과 `khugepaged`의 mTHP 콜랩스 지원 조건이 다릅니다. 따라서 "mTHP가 실무 표준이 되었다"는 말은 커뮤니티의 관심과 채택이 넓어졌다는 뜻이지, 특정 커널의 기본 설정이 바뀌었다는 뜻은 아니라는 점을 구분해서 받아들여야 합니다.

HugeTLB는 예측 가능하지만 유연성이 떨어집니다. 사전에 크기를 정해 예약해야 하고, 예약량을 잘못 잡으면 유휴 메모리로 낭비되거나 반대로 필요할 때 `mmap`이 실패합니다. 또한 이 장에서 제시한 벤치마크 수치는 접근 패턴(순차 vs 랜덤), 워킹셋 크기, CPU 세대별 TLB 계층 구조에 크게 좌우되므로, 일반화된 "N% 개선" 주장을 그대로 받아들이기보다 항상 대상 환경에서 재현해 검증하는 것이 안전합니다.

## 참고 자료

- Linux 커널 문서, [Transparent Hugepage Support](https://docs.kernel.org/admin-guide/mm/transhuge.html) — THP·mTHP 설정, `khugepaged` 제어, 모니터링 필드
- Linux 커널 문서, [HugeTLB Pages](https://docs.kernel.org/admin-guide/mm/hugetlbpage.html) — `nr_hugepages`, `hugetlbfs`, `MAP_HUGETLB`
- Linux man-pages, [madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html) — `MADV_HUGEPAGE`(2.6.38부터)와 `MADV_COLLAPSE`(6.1부터)

## 마무리

- [ ] HugeTLB(정적 예약)와 THP(동적 콜랩스)의 관리 방식 차이를 설명할 수 있는가?
- [ ] THP의 `always`/`madvise`/`never` 정책과 `MADV_HUGEPAGE`/`MADV_COLLAPSE`의 역할을 구분할 수 있는가?
- [ ] mTHP가 해결하는 문제(4KB와 2MB 사이의 틈)와 PMD 크기 외에는 기본적으로 옵트인이라는 점을 설명할 수 있는가?
- [ ] `perf stat` 등으로 TLB 미스·페이지 폴트 변화를 실측해 huge page 적용 효과를 검증할 수 있는가?
- [ ] latency-critical 워크로드에서 THP를 언제 끄고 언제 선택적으로 켤지 판단할 수 있는가?

다음 장에서는 이 장에서 다룬 huge page 정책이 **NUMA 토폴로지**와 만났을 때 어떤 문제가 생기는지, 메모리를 어느 노드에 배치해야 지역성을 지킬 수 있는지를 다룹니다. HugeTLB·THP·mTHP 모두 NUMA 노드 경계를 넘나드는 배치가 가능하므로, 이 장의 내용과 다음 장의 노드 배치 전략은 함께 적용해야 완전한 그림이 됩니다.

→ [NUMA 메모리 할당·지역성](/post/memory-optimization/numa-memory-allocation-locality/) (챕터 09)
