---
collection_order: 8
date: 2026-07-14
lastmod: 2026-11-02
draft: false
image: wordcloud.png
title: "[Extreme 08] Lookup Table 최적화"
slug: lookup-table-optimization-techniques
description: "룩업 테이블(Lookup Table)로 반복 연산을 메모리 접근으로 치환하는 기법을 다룹니다. 테이블 크기와 캐시 적중률의 트레이드오프, 분기 대체 판단 기준, 그리고 비밀 의존 인덱스가 낳는 캐시 타이밍 부채널 위험까지 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - C++
  - CPU(Central Processing Unit)
  - Cache
  - Memory(메모리)
  - Latency
  - Throughput
  - Benchmark
  - Profiling(프로파일링)
  - Data-Structures(자료구조)
  - Best-Practices
  - Code-Quality(코드품질)
  - Implementation(구현)
  - Pitfalls(함정)
  - Advanced
  - Deep-Dive
  - Case-Study
  - Comparison(비교)
  - Hardware(하드웨어)
  - Lookup-Table
  - LUT
  - Precomputation
  - Branchless
  - Cache-Timing-Attack
  - Branch-Misprediction
  - Table-Driven
  - perf
  - VTune
---

**Lookup Table(룩업 테이블) 최적화**란 실행 시점마다 반복적으로 계산해야 하는 연산 결과를 미리 계산해 배열에 저장해 두고, 런타임에는 그 계산 대신 인덱싱 한 번으로 값을 가져오는 기법을 말합니다. 나눗셈·삼각함수·다중 조건 분기처럼 CPU 사이클을 소모하는 연산을 매번 반복하는 대신 `table[index]` 한 번으로 대체할 수 있다면 명령어 수와 분기 예측 실패를 크게 줄일 수 있지만, 이 교환은 공짜가 아닙니다. **연산 비용을 메모리 계층 비용으로 옮기는 것**이 이 기법의 본질이며, 테이블이 캐시에 상주하지 못하는 순간 이득은 손실로 뒤집힙니다. 이 장은 그 치환이 언제 이기고 언제 지는지를 캐시 적중률과 테이블 크기의 관계로 설명합니다.

## 이 장을 읽기 전에

이 장은 캐시 계층과 접근 지연에 대한 기초 감각을 전제로 합니다. L1/L2/LLC의 크기·지연 차이를 아직 정리하지 못했다면 [Tr.04 캐시 친화적 접근 패턴](/post/memory-optimization/cache-friendly-access-patterns/)을 먼저 읽는 것이 좋습니다. 분기 예측 실패 비용을 수치로 이해하고 싶다면 [Tr.05 분기 예측 메커니즘과 비용](/post/cpu-optimization/branch-prediction-mechanisms-cost/)을 참고하세요.

**이 장의 깊이**: 스칼라 코드에서 LUT를 설계하는 원리, 테이블 크기와 캐시 적중률의 트레이드오프, 분기를 LUT로 대체할지 판단하는 기준을 다룹니다. **다루지 않는 것**: `gather` 기반의 대규모 테이블 조회와 SIMD 전체 구현은 [Tr.08 02장](/post/extreme-optimization/simd-intrinsics-practical-usage/)의 셔플·퍼뮤트 규칙을 전제로 하므로, 이 장은 그 입구에 해당하는 '벡터 레지스터에 들어갈 만큼 작은 테이블'까지만 사례 3에서 다룹니다. 분기 자체를 없애는 일반적인 branchless 기법은 [Tr.08 06장](/post/extreme-optimization/branchless-programming-techniques/)에 위임하고, 테이블 대신 비트 연산으로 같은 문제를 푸는 방법은 [Tr.08 09장](/post/extreme-optimization/bit-manipulation-optimization-techniques/)에서, 캐시 크기에 독립적인 알고리즘 설계는 [Tr.08 15장](/post/extreme-optimization/cache-oblivious-algorithm-design/)에서 각각 이어집니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자(입문)** | "역사와 배경" ~ "핵심 개념" | LUT가 연산을 메모리 접근으로 바꾸는 원리와 캐시 적중의 관계 이해 |
| **중급자(응용)** | "흔한 오개념" ~ "판단 기준" | 언제 LUT가 이득이고 언제 손해인지 스스로 판단 |
| **전문가** | "비판적 시각" | 캐시 타이밍 부채널, 멀티코어 경합, 유지보수 비용까지 평가 |

---

## 역사와 배경: 계산을 메모리로 미룬다는 발상

룩업 테이블은 컴퓨터보다 오래된 아이디어입니다. 삼각함수표·로그표는 계산기가 없던 시절 사람이 손으로 계산할 나눗셈·곱셈을 미리 표로 만들어 둔 것이었고, 초기 컴퓨터의 부동소수점 연산이 느렸던 시절에도 `sin`/`cos`/`sqrt` 근사값을 표로 미리 만들어 두는 방식이 널리 쓰였습니다. 소프트웨어 공학에서 이 발상이 가장 정교하게 다듬어진 사례 중 하나가 CRC(순환 중복 검사) 계산입니다. Dilip V. Sarwate는 1988년 *Communications of the ACM* 31권 8호에 실린 「Computation of cyclic redundancy checks via table look-up」에서, 다항식 나눗셈을 매 비트마다 반복하는 대신 바이트 하나에 대한 8비트 연산 결과를 256개 항목의 테이블에 미리 계산해 두고 조회하는 방법을 제시했습니다. 이 "바이트 단위 테이블 조회" 방식은 소프트웨어 CRC 구현의 대표적인 기법이 되었고, 여러 바이트를 한 번에 처리하는 slice-by-N 계열의 확장판으로 이어졌습니다.

CPU 명령어 집합도 같은 트레이드오프를 반영해 왔습니다. 예를 들어 1비트 개수를 세는 popcount 연산은 오랫동안 8비트 또는 16비트 단위의 룩업 테이블로 구현되다가, 인텔이 2008년 Nehalem 마이크로아키텍처의 SSE4.2에 `POPCNT` 명령어를 추가하면서 하드웨어가 직접 이 연산을 지원하기 시작했습니다. 이 사례는 "룩업 테이블은 임시방편이 아니라, 하드웨어가 그 연산을 직접 지원하기 전까지 쓰는 합리적 대안"이라는 점을 보여줍니다. 하드웨어 명령어와 비트 연산 트릭으로 같은 문제를 푸는 방법은 [09장: 비트 조작 최적화 기법](/post/extreme-optimization/bit-manipulation-optimization-techniques/)에서 다룹니다.

## 핵심 개념: 연산을 메모리 접근으로 치환하기

LUT의 핵심 조건은 입력 도메인이 유한하고 실용적인 크기여야 한다는 것입니다. 함수 `f(x)`의 입력 `x`가 가질 수 있는 값의 개수가 작다면(바이트 하나, 16비트 인덱스 등) `table[x] = f(x)`를 미리 채워 두고, 런타임에는 `f(x)`를 재계산하는 대신 `table[x]`를 읽기만 하면 됩니다. 문제는 이 읽기가 공짜가 아니라는 점입니다. 테이블이 L1 데이터 캐시(대개 32–48KB)에 상주한다면 접근은 수 cycle 안에 끝나지만, 테이블이 L1을 벗어나 L2(수백 KB–1MB급)나 LLC(수 MB급)까지 밀려나면 접근 지연은 수십에서 수백 cycle로 늘어나고, 캐시 밖 DRAM까지 나가면 수십–수백 ns가 추가됩니다. 정확한 지연 수치는 마이크로아키텍처·클럭·메모리 구성에 따라 달라지는 구현 정의 영역이므로, 이 장에서는 상대적 크기 관계만 다루고 절대 수치는 [Tr.05 CPU 마이크로아키텍처 트랙](/post/cpu-optimization/getting-started-cpu-microarchitecture-performance-tuning/)의 측정 방법으로 직접 확인하는 것을 전제로 합니다.

아래 다이어그램은 이 판단 흐름을 정리한 것입니다. 연산 비용이 메모리 접근보다 충분히 클 때만 LUT로 옮기는 것이 이득이고, 그다음에는 테이블이 상위 캐시에 상주하는지가 실제 승패를 가릅니다.

```mermaid
flowchart TB
  input["입력 값 x"] --> decide{"매 호출마다</br>재계산해야 하는가?"}
  decide -- "예: 연산 비용이 큼" --> lut["table[x] 조회"]
  decide -- "아니오: 이미 저렴함" --> compute["직접 연산 f(x)"]
  lut --> cacheCheck{"테이블이 L1/L2에</br>상주하는가?"}
  cacheCheck -- "예" --> fastHit["수 cycle 내 반환"]
  cacheCheck -- "아니오" --> slowMiss["수십~수백 cycle 지연"]
```

### 사례 1: CRC32 — 비트 루프를 테이블 조회로 압축

CRC32를 순진하게 구현하면 바이트 하나당 8번의 비트 반복(조건부 XOR)이 필요합니다. 아래는 그 비트 단위 구현입니다.

```cpp
#include <cstdint>
#include <cstddef>

// 비권장: 바이트 하나마다 8회의 비트 반복과 조건부 XOR을 수행
uint32_t crc32_bitwise(uint32_t crc, const uint8_t* data, size_t len) {
  crc = ~crc;
  for (size_t i = 0; i < len; ++i) {
    crc ^= data[i];
    for (int bit = 0; bit < 8; ++bit) {
      uint32_t mask = -(crc & 1u);
      crc = (crc >> 1) ^ (0xEDB88320u & mask);
    }
  }
  return ~crc;
}
```

이 8회 반복을 미리 계산해 두면 바이트당 반복 없이 테이블 조회 한 번으로 줄일 수 있습니다. 256개 항목(각 4바이트, 총 1KB)이면 어떤 L1 데이터 캐시에도 여유 있게 상주하므로, 이 테이블은 "크기 대 캐시 적중률" 트레이드오프에서 거의 항상 이기는 쪽에 속합니다.

```cpp
#include <array>
#include <cstdint>
#include <cstddef>

// 256개 항목: 바이트값 하나에 대한 8비트 반복 계산 결과를 컴파일 타임에 미리 확정
constexpr std::array<uint32_t, 256> make_crc32_table() {
  std::array<uint32_t, 256> table{};
  for (uint32_t i = 0; i < 256; ++i) {
    uint32_t crc = i;
    for (int bit = 0; bit < 8; ++bit) {
      uint32_t mask = -(crc & 1u);
      crc = (crc >> 1) ^ (0xEDB88320u & mask);
    }
    table[i] = crc;
  }
  return table;
}

constexpr auto kCrc32Table = make_crc32_table();  // 런타임 초기화 비용 0, 바이너리에 상수로 포함

uint32_t crc32_table(uint32_t crc, const uint8_t* data, size_t len) {
  crc = ~crc;
  for (size_t i = 0; i < len; ++i) {
    // 8회의 비트 루프를 테이블 조회 1회로 치환
    crc = (crc >> 8) ^ kCrc32Table[(crc ^ data[i]) & 0xFFu];
  }
  return ~crc;
}
```

`constexpr` 함수로 테이블을 만들면 컴파일 타임에 값이 확정되어 런타임 초기화 비용이 없다는 장점이 있지만, 이 테이블은 프로그램 전체 수명 동안 정적 메모리를 차지하므로 여러 스레드가 같은 테이블을 동시에 읽더라도 읽기 전용이라 데이터 경쟁은 없습니다. 두 구현을 같은 입력으로 비교하면 차이를 직접 확인할 수 있습니다.

```cpp
#include <benchmark/benchmark.h>
#include <vector>
#include <cstdint>

// crc32_bitwise, crc32_table, kCrc32Table의 정의는 위 코드를 이 파일(bench.cpp) 앞부분에 그대로 붙여 넣는다

static void BM_Crc32Bitwise(benchmark::State& state) {
  std::vector<uint8_t> data(4096, 0xAB);
  for (auto _ : state) {
    uint32_t r = crc32_bitwise(0, data.data(), data.size());
    benchmark::DoNotOptimize(r);
  }
}
BENCHMARK(BM_Crc32Bitwise);

static void BM_Crc32Table(benchmark::State& state) {
  std::vector<uint8_t> data(4096, 0xAB);
  for (auto _ : state) {
    uint32_t r = crc32_table(0, data.data(), data.size());
    benchmark::DoNotOptimize(r);
  }
}
BENCHMARK(BM_Crc32Table);

BENCHMARK_MAIN();
```

`g++ -O2 -std=c++17 bench.cpp -lbenchmark -lpthread`로 빌드해 실행하면(x86-64, GCC 13, `-O2` 기준 예시), `BM_Crc32Table`이 `BM_Crc32Bitwise`보다 빠를 것으로 예상하지만, 이 글은 실행 결과를 싣지 않았으므로 직접 측정해 확인해야 합니다. 차이는 바이트당 8회의 분기·시프트가 1KB 테이블에 대한 L1 히트 한 번으로 줄어든 데서 옵니다. 정확한 배율은 컴파일러·플래그·데이터 크기에 따라 달라지므로 실제 환경에서 직접 재현해 확인해야 하며, 프로덕션 zlib류 구현은 여기서 한 걸음 더 나아가 슬라이스 단위를 늘린 더 큰 테이블로 처리량을 추가로 끌어올립니다.

### 사례 2: 분기를 인덱싱으로 대체하기

LUT는 산술 연산뿐 아니라 다중 조건 분기를 대체하는 데도 쓰입니다. 문자 하나를 숫자·알파벳·공백·기타로 분류하는 코드를 조건문으로 짜면 문자마다 최대 세 번의 비교·분기가 필요합니다.

```cpp
#include <cstdint>

enum class CharClass : uint8_t { kOther, kDigit, kAlpha, kSpace };

// 비권장: 문자 하나마다 최대 3회의 범위 비교와 분기
CharClass classify_branch(unsigned char c) {
  if (c >= '0' && c <= '9') return CharClass::kDigit;
  if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) return CharClass::kAlpha;
  if (c == ' ' || c == '\t' || c == '\n') return CharClass::kSpace;
  return CharClass::kOther;
}
```

같은 분류를 256바이트짜리 테이블로 미리 만들어 두면 분기 없이 인덱싱 한 번으로 끝낼 수 있습니다. 256바이트는 어떤 캐시 라인 구성에서도 무시할 만한 크기이므로 캐시 적중률 걱정 없이 적용할 수 있습니다.

```cpp
#include <array>
#include <cstdint>

constexpr std::array<CharClass, 256> make_class_table() {
  std::array<CharClass, 256> table{};
  for (int c = 0; c < 256; ++c) {
    if (c >= '0' && c <= '9') table[c] = CharClass::kDigit;
    else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) table[c] = CharClass::kAlpha;
    else if (c == ' ' || c == '\t' || c == '\n') table[c] = CharClass::kSpace;
    else table[c] = CharClass::kOther;
  }
  return table;
}
constexpr auto kClassTable = make_class_table();

// 권장: 분기 없이 인덱싱 한 번으로 분류
CharClass classify_table(unsigned char c) {
  return kClassTable[c];
}
```

다만 이 대체가 항상 이기는 것은 아닙니다. 입력이 거의 항상 숫자인 파서처럼 분기 예측기가 이미 거의 완벽하게 예측하는 패턴이라면, `classify_branch`의 분기 비용은 이미 거의 0에 가깝고 `classify_table`이 얻는 이득은 미미하거나 오히려 캐시 라인 하나를 추가로 점유하는 손해로 바뀔 수 있습니다. 실제 입력 분포에서 두 버전을 벤치마크로 비교하기 전에는 어느 쪽이 이기는지 단정할 수 없습니다. 조건 분기 자체를 없애는 더 일반적인 기법(마스크·산술 연산 기반)은 [06장: Branchless 프로그래밍 기법](/post/extreme-optimization/branchless-programming-techniques/)을 참고하세요.

### 사례 3: 벡터 레지스터 안에 들어가는 테이블

테이블이 아주 작으면 메모리를 거치지 않고 레지스터 안에서 조회할 수도 있습니다. 16개 항목짜리 바이트 테이블은 128비트 레지스터 하나에 통째로 들어가고, SSSE3의 `pshufb`(`_mm_shuffle_epi8`)는 인덱스 레지스터의 각 바이트를 하위 4비트만큼의 위치로 해석해 테이블 레지스터에서 값을 골라 줍니다. 즉 16바이트를 한 명령으로 동시에 조회하는 병렬 룩업이며, 이때 테이블은 캐시 계층이 아니라 레지스터에 있으므로 앞에서 다룬 캐시 적중률 문제가 사라집니다. Agner Fog의 *Optimizing software in C++*도 룩업 테이블과 벡터 퍼뮤트 명령을 다루는 참고 자료로 함께 읽을 만합니다(해당 절의 정확한 서술은 원문에서 확인하세요).

```cpp
#include <immintrin.h>  // SSSE3 필요: g++ -O2 -mssse3 hex16.cpp
#include <cstdint>
#include <cstdio>

// 16바이트 입력을 32개의 16진 ASCII 문자로 바꾼다.
void bytes_to_hex16(const uint8_t* in, char* out) {
  const __m128i table = _mm_setr_epi8('0', '1', '2', '3', '4', '5', '6', '7',
                                      '8', '9', 'a', 'b', 'c', 'd', 'e', 'f');
  const __m128i low_mask = _mm_set1_epi8(0x0F);
  __m128i v = _mm_loadu_si128(reinterpret_cast<const __m128i*>(in));
  __m128i hi = _mm_and_si128(_mm_srli_epi16(v, 4), low_mask);  // 상위 nibble
  __m128i lo = _mm_and_si128(v, low_mask);                     // 하위 nibble
  __m128i hi_chars = _mm_shuffle_epi8(table, hi);  // 바이트마다 table[nibble]
  __m128i lo_chars = _mm_shuffle_epi8(table, lo);
  // 상·하위 문자를 교대로 배치: hi0 lo0 hi1 lo1 ...
  _mm_storeu_si128(reinterpret_cast<__m128i*>(out), _mm_unpacklo_epi8(hi_chars, lo_chars));
  _mm_storeu_si128(reinterpret_cast<__m128i*>(out + 16), _mm_unpackhi_epi8(hi_chars, lo_chars));
}

int main() {
  uint8_t in[16];
  for (int i = 0; i < 16; ++i) in[i] = static_cast<uint8_t>(i * 17);  // 0x00, 0x11, ..., 0xFF
  char out[33] = {};
  bytes_to_hex16(in, out);
  std::printf("%s\n", out);  // 00112233445566778899aabbccddeeff 가 출력되어야 한다
  return 0;
}
```

`pshufb`는 인덱스 바이트의 최상위 비트가 켜져 있으면 해당 결과 바이트를 0으로 만들고, 그렇지 않으면 하위 4비트만 인덱스로 씁니다. 그래서 위 코드는 `_mm_srli_epi16`으로 밀어낸 뒤 `0x0F` 마스크를 씌워 바이트마다 순수한 nibble을 만든 다음에 조회합니다(16비트 단위 시프트는 인접 바이트의 비트를 끌어오므로 마스크가 필요합니다). 이 장은 이 코드를 직접 컴파일해 실행하지 않았으므로 기대 출력은 코드를 읽고 계산한 값이며, 실제 도입 전에는 대상 CPU에서 스칼라 LUT와 비교 측정해야 합니다. 더 큰 테이블이나 AVX2 이상의 셔플은 [02장](/post/extreme-optimization/simd-intrinsics-practical-usage/)에서 이어집니다.

## 흔한 오개념 교정

<strong>"룩업 테이블은 항상 계산보다 빠르다"</strong>는 사실이 아닙니다. 테이블이 캐시에 상주하지 못하면 메모리 접근 지연이 재계산 비용보다 커질 수 있고, 특히 여러 스레드가 같은 대형 테이블에 무작위로 접근하며 공유 캐시를 두고 경합할 때는 단일 스레드 벤치마크에서 보이지 않던 손해가 드러납니다.

<strong>"테이블은 클수록 정밀하고 좋다"</strong>는 정밀도와 속도를 혼동한 생각입니다. 테이블 크기를 늘리면 정밀도가 올라갈 수는 있지만 동시에 캐시 풋프린트가 커져, 같은 핫패스에서 함께 쓰이는 다른 데이터 구조를 캐시에서 밀어내는 캐시 오염(cache pollution)을 일으킬 수 있습니다. 목표는 "필요한 정밀도 안에서 가장 작은 테이블"입니다.

<strong>"룩업 테이블은 분기를 항상 대체할 수 있고 대체하는 것이 항상 이득이다"</strong>도 과장입니다. 이 판단은 추측이 아니라 측정으로 합니다. Linux에서는 `perf stat -e branches,branch-misses ./app`으로 분기 예측 실패율을 먼저 읽고, 실패율이 낮으면 LUT를 도입해도 줄어드는 비용이 거의 없습니다. 실패율이 높은 구간에서만 LUT가 이득을 낼 후보가 됩니다.

## 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 입력 도메인이 작고(바이트 등) 반복 접근이 많음 | LUT (테이블이 L1 상주 가능) | 매번 다단계 조건 분기 |
| 재계산 비용(나눗셈·삼각함수·복잡한 조건)이 메모리 접근보다 훨씬 큼 | LUT | 매번 산술 재계산 |
| 접근 패턴이 넓고 무작위라 캐시 히트율이 낮음 | 직접 계산 또는 SIMD 명령 | 크고 무작위 접근인 LUT |
| 여러 스레드가 같은 대형 테이블에 자주 접근 | 스레드-로컬 소형 테이블 또는 직접 계산 | 전역 대형 공유 테이블 |
| 프로파일링 결과 분기가 이미 예측이 잘 됨 | 분기 유지 | 불필요한 LUT 도입 |
| 인덱스가 비밀(암호 키 등)에 의존 | 상수시간 비트 연산 대안 | 비밀 의존 인덱스 LUT |

도입 전에는 `perf stat`이나 Intel VTune 같은 프로파일러로 캐시 미스율과 분기 예측 실패율을 먼저 측정하고, 도입 후 같은 지표로 회귀를 확인하는 것이 안전합니다.

## 비판적 시각: 한계와 트레이드오프

가장 심각한 한계는 보안입니다. Daniel J. Bernstein은 2005년 발표한 논문에서, 비밀 키에 의존하는 인덱스로 룩업 테이블에 접근하는 AES의 소프트웨어 구현이 캐시 접근 시간의 미세한 차이를 통해 키 정보를 노출할 수 있음을 실증했습니다. 테이블이 캐시 라인 경계에 걸쳐 있고 접근 인덱스가 비밀 값에서 유도된다면, 공격자는 히트·미스에 따른 타이밍 차이를 관측해 인덱스(즉 비밀의 일부)를 추론할 수 있습니다. 이 때문에 현대 암호 구현은 비밀 의존 인덱스로 테이블을 조회하는 방식을 피하고, 비트 연산만으로 상수 시간에 같은 결과를 내는 구현을 택합니다. 성능이 아니라 보안이 우선하는 코드 경로에서는 LUT 도입 전에 이 위험을 반드시 검토해야 합니다.

두 번째 한계는 멀티코어 환경의 캐시 경합입니다. 단일 스레드 벤치마크에서 이긴 LUT라도, 여러 코어가 같은 LLC를 공유하며 동시에 그 테이블에 접근하면 실제 프로덕션 부하에서는 캐시 라인 경합으로 이득이 줄거나 사라질 수 있습니다. 이런 경합은 단일 스레드 마이크로벤치마크로는 드러나지 않으므로, 실제 동시성 부하를 재현한 뒤 다시 측정해야 합니다.

세 번째는 유지보수성입니다. 매직 넘버로 채워진 테이블은 그 자체로는 왜 그 값인지 설명하지 못하고, 원본 알고리즘이 바뀌면 테이블 생성 로직도 함께 바뀌어야 합니다. `constexpr` 함수로 테이블을 생성하도록 코드에 남겨 두면(사례 1처럼) 테이블과 원본 알고리즘이 항상 일치한다는 것을 컴파일러가 보장해 주므로, 손으로 계산해 하드코딩한 배열보다 안전합니다. 극한 최적화와 유지보수성의 일반적인 균형 기준은 [11장: 극한 최적화와 유지보수성 균형](/post/extreme-optimization/extreme-optimization-maintainability-balance/)에서 다룹니다.

마지막으로, `constexpr`를 컴파일러가 알아서 테이블로 바꿔 준다는 뜻으로 오해하면 안 됩니다. [cppreference](https://en.cppreference.com/w/cpp/language/constexpr)에 따르면 `constexpr`는 값을 컴파일 타임에 평가하는 것이 가능하다고 선언할 뿐이어서, 상수가 아닌 인자로 부른 `constexpr` 함수는 런타임에 계산됩니다(같은 문서의 예제도 변수 인자의 `factorial(k)`를 런타임 계산이라고 주석합니다). 테이블이 컴파일 타임에 확정되려면 이 장의 `constexpr auto kCrc32Table = make_crc32_table();`처럼 상수 평가가 요구되는 자리에서 호출해야 합니다. 다만 컴파일러 최적화가 비슷한 일을 하는 경우는 따로 있습니다. 예를 들어 GCC의 [`-ftree-switch-conversion`](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)은 `switch` 안의 단순한 초기화를 스칼라 배열 초기화로 바꾸며 `-O2` 이상에서 기본으로 켜집니다. 그래서 값-대-값 매핑을 `switch`로 쓴 코드는 컴파일러가 이미 테이블로 만들었을 수 있으므로, 수동으로 테이블을 도입하기 전에 생성된 어셈블리를 확인하는 것이 먼저입니다. 벤치마크 없이 도입한 LUT는 코드 복잡도만 늘리는 헛수고가 될 수 있습니다.

## 마무리

이 장을 읽은 후 다음을 스스로 확인할 수 있어야 합니다.

- [ ] LUT가 "연산 → 메모리 접근" 치환이라는 원리와 그 비용의 성격을 설명할 수 있다.
- [ ] 테이블 크기와 캐시 적중률의 관계를 L1/L2/LLC 계층 관점에서 설명할 수 있다.
- [ ] CRC32 사례처럼 반복 연산을 테이블 조회로 치환하는 코드를 직접 작성하고 벤치마크로 검증할 수 있다.
- [ ] 분기를 LUT로 대체할지 판단할 때 분기 예측기의 실제 예측률을 먼저 확인해야 하는 이유를 설명할 수 있다.
- [ ] 비밀 의존 인덱스 LUT가 캐시 타이밍 부채널을 만들 수 있다는 것과 그 대안을 설명할 수 있다.

더 읽을 거리로는 [Agner Fog, Optimizing Software in C++](https://www.agner.org/optimize/optimizing_cpp.pdf)의 룩업 테이블 절, `std::array`의 표준 인터페이스를 다루는 [cppreference: std::array](https://en.cppreference.com/w/cpp/container/array), 그리고 캐시 타이밍 부채널의 원저인 [Bernstein, Cache-timing attacks on AES (2005)](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf)를 권합니다.

**이전 장**: [Hand-written 어셈블리 적용과 위험 관리](/post/extreme-optimization/hand-written-assembly-risk-management/) (07장)

**다음 장에서는** 비트 연산으로 같은 종류의 문제(분류, 개수 세기, 패리티 계산 등)를 테이블 없이 상수 공간에 푸는 기법을 다룹니다. LUT가 "공간을 써서 시간을 아끼는" 접근이라면, 비트 조작은 대체로 "산술·논리 연산만으로 같은 것을 더 빠르게" 얻으려는 접근이라, 두 기법을 나란히 비교하면 언제 어느 쪽을 선택할지에 대한 감각이 뚜렷해집니다.

→ [비트 조작 최적화 기법](/post/extreme-optimization/bit-manipulation-optimization-techniques/) (09장)
