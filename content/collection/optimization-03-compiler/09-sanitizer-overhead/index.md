---
collection_order: 9
date: 2026-03-11
lastmod: 2026-10-20
draft: false
image: wordcloud.png
title: "[Compiler 03] Sanitizer 성능 오버헤드"
slug: sanitizer-overhead-performance
description: "ASan·UBSan·TSan·MSan의 계측 코드가 어디서 비용을 만드는지 실제 어셈블리로 확인하고, Clang 공식 문서의 오버헤드 수치와 직접 측정법, 디버그·CI·릴리즈 빌드별 sanitizer 배치 전략과 대안을 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - Memory(메모리)
  - Debugging(디버깅)
  - Testing(테스트)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Security(보안)
  - Reliability
  - Concurrency(동시성)
  - Thread(스레드)
  - Benchmark
  - Profiling(프로파일링)
  - Linux(리눅스)
  - Assembly(어셈블리)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Clang
  - GCC
  - LLVM
  - Sanitizer
  - AddressSanitizer
  - CMake
---

Sanitizer는 메모리 오류·미정의 동작·데이터 레이스를 발생 지점에서 바로 잡아 주는 강력한 도구지만, 그 대가로 실행 시간과 메모리를 크게 씁니다. 이 챕터에서는 그 비용이 **어디서** 생기는지를 계측 코드 수준에서 확인하고, 공식 문서가 밝히는 전형적인 오버헤드 수치, 직접 측정하는 방법, 그리고 디버그·CI·릴리즈 빌드에서 sanitizer를 배치하는 전략을 다룹니다. 본문의 어셈블리와 리포트는 2026년 10월 [Compiler Explorer](https://godbolt.org)의 x86-64 clang 19.1.0에서 얻은 실제 출력입니다.

## Sanitizer 종류

Sanitizer는 공통적으로 컴파일러가 프로그램에 <strong>검사 코드를 삽입(instrumentation)</strong>하고, 함께 링크되는 런타임 라이브러리가 그 검사를 수행하는 구조입니다. 무엇을 잡느냐에 따라 검사 대상과 비용 구조가 달라집니다.

<strong>AddressSanitizer(ASan)</strong>는 힙·스택·전역 버퍼 오버플로, use-after-free, 이중 해제 같은 메모리 접근 오류를 잡습니다. 모든 메모리 읽기·쓰기 앞에 "이 주소에 접근해도 되는가"를 묻는 검사가 들어가므로 비용이 메모리 접근 횟수에 비례합니다. <strong>UndefinedBehaviorSanitizer(UBSan)</strong>는 부호 있는 정수 오버플로, 잘못된 시프트, 정렬되지 않은 포인터, 범위를 벗어난 배열 인덱스 같은 미정의 동작을 잡습니다. 검사는 해당 연산이 있는 자리에만 들어가므로 비용이 코드 성격에 따라 크게 달라집니다. <strong>ThreadSanitizer(TSan)</strong>는 두 스레드가 동기화 없이 같은 메모리에 접근하고 그중 하나가 쓰는 데이터 레이스를 잡으며, 모든 메모리 접근과 동기화 이벤트를 기록합니다. <strong>MemorySanitizer(MSan)</strong>는 초기화되지 않은 메모리를 읽어 분기나 주소 계산에 쓰는 경우를 잡고, 모든 값의 초기화 여부를 비트 단위로 추적합니다.

## 빌드·실행 명령

Sanitizer는 컴파일과 링크 양쪽에 `-fsanitize=`를 주어 켭니다. 링크에도 같은 플래그가 있어야 런타임 라이브러리가 함께 링크됩니다. 리포트에 소스 줄 번호가 나오도록 `-g`를, 스택 추적이 정확하도록 `-fno-omit-frame-pointer`를 함께 주는 것이 일반적이며, Clang 문서는 ASan의 합리적인 성능을 위해 `-O1` 이상을 권합니다.

```bash
# AddressSanitizer + UndefinedBehaviorSanitizer (가장 흔한 조합)
clang++ -std=c++20 -g -O1 -fno-omit-frame-pointer \
        -fsanitize=address,undefined app.cc -o app_asan

# ThreadSanitizer (ASan과 함께 켤 수 없음)
clang++ -std=c++20 -g -O1 -fsanitize=thread app.cc -o app_tsan

# 실행 시 동작은 환경 변수로 조정 (예: 누수 검사 켜기)
ASAN_OPTIONS=detect_leaks=1 ./app_asan
```

ASan과 TSan은 런타임 구조가 서로 충돌해 한 바이너리에 함께 켤 수 없고, UBSan은 둘 중 어느 쪽과도 조합할 수 있습니다. MSan 역시 ASan·TSan과 함께 쓸 수 없습니다. 따라서 CI에서는 보통 "ASan+UBSan" 빌드와 "TSan" 빌드를 따로 둡니다.

## 리포트 읽기: use-after-free

Sanitizer의 가치는 오류가 **일어난 순간**과 원인이 된 할당·해제 위치를 함께 보여 주는 데 있습니다. 아래 프로그램은 해제한 메모리를 다시 읽습니다.

```cpp
// app.cc: use-after-free를 일부러 만드는 예제
#include <cstdio>

int process(const int* p) {
    return *p + 1;              // 해제된 메모리 읽기
}

int main() {
    int* p = new int(41);
    delete p;
    std::printf("%d\n", process(p));
}
```

Clang 19.1.0에서 `-g -O1 -fno-omit-frame-pointer -fsanitize=address`로 빌드해 실행한 출력의 앞부분입니다(주소와 libc 프레임은 실행 환경마다 다르며, 일부 줄을 생략했습니다).

```text
==2==ERROR: AddressSanitizer: heap-use-after-free on address 0x502000000010 at pc 0x603aecf4cd77 bp 0x7ffc7749e530 sp 0x7ffc7749e528
READ of size 4 at 0x502000000010 thread T0
    #0 0x603aecf4cd76 in process(int const*) /app/example.cpp:5:12
    #1 0x603aecf4cd76 in main /app/example.cpp:11:25
    ...
0x502000000010 is located 0 bytes inside of 4-byte region [0x502000000010,0x502000000014)
freed by thread T0 here:
    #0 0x603aecf4b522 in operator delete(void*, unsigned long) .../asan_new_delete.cpp:155:3
    #1 0x603aecf4cd29 in main /app/example.cpp:10:5
    ...
previously allocated by thread T0 here:
    #0 0x603aecf4a8bd in operator new(unsigned long) .../asan_new_delete.cpp:86:3
    #1 0x603aecf4cd00 in main /app/example.cpp:9:14
    ...
SUMMARY: AddressSanitizer: heap-use-after-free /app/example.cpp:5:12 in process(int const*)
```

리포트는 무엇이 잘못됐는지(heap-use-after-free, 4바이트 읽기), 어디서 일어났는지(5행 `process`), 그 메모리가 언제 해제되고(10행) 언제 할당됐는지(9행)를 각각의 스택 추적으로 보여 줍니다. `-O1`에서 `process`가 `main`에 인라인됐지만, 디버그 정보 덕분에 두 프레임이 모두 복원되어 있습니다. 출력 뒤쪽에는 문제 주소 주변의 "shadow bytes"가 이어지는데, 다음 절에서 볼 ASan의 메커니즘이 바로 이 shadow 메모리입니다.

## 오버헤드는 어디서 오나

ASan의 비용을 이해하려면 검사 코드가 어떻게 생겼는지 보면 됩니다. [AddressSanitizer 알고리즘 문서](https://github.com/google/sanitizers/wiki/AddressSanitizerAlgorithm)에 따르면 ASan은 애플리케이션 메모리 8바이트마다 shadow 메모리 1바이트를 두고, x86-64 Linux에서는 `Shadow = (Mem >> 3) + 0x7fff8000`으로 주소를 대응시킵니다. shadow 바이트가 0이면 8바이트 전체에 접근할 수 있고, 다른 값이면 일부만 접근 가능하거나 해제·redzone 영역이라는 뜻입니다. 할당할 때 객체 앞뒤에 접근 금지 구역(redzone)을 붙이고, 해제한 메모리는 바로 재사용하지 않고 격리(quarantine)해 두므로 오버플로와 use-after-free가 shadow 검사에 걸립니다.

포인터 하나를 읽는 함수에 이 검사가 어떻게 들어가는지 Clang 19.1.0 `-O1`의 실제 출력으로 비교합니다.

```cpp
long load(const long* p) { return *p; }
```

```text
# -O1
load(long const*):
        mov     rax, qword ptr [rdi]
        ret

# -O1 -fsanitize=address
load(long const*):
        push    rax
        mov     rax, rdi
        shr     rax, 3                          # Mem >> 3
        cmp     byte ptr [rax + 2147450880], 0  # + 0x7fff8000 위치의 shadow 바이트 검사
        jne     .LBB0_2
        mov     rax, qword ptr [rdi]
        pop     rcx
        ret
.LBB0_2:
        call    __asan_report_load8@PLT
```

`2147450880`은 `0x7fff8000`이므로, 문서의 대응식이 그대로 기계어가 된 것입니다. 원래 명령 하나였던 읽기가 시프트·shadow 읽기·비교·분기를 거치게 되고, shadow 메모리 접근이 캐시를 함께 차지합니다. 이것이 ASan 비용이 메모리 접근 밀도에 비례하는 이유입니다.

TSan은 구조가 다릅니다. 같은 함수를 `-O1 -fsanitize=thread`로 컴파일하면 읽기 앞에 `call __tsan_read8`이, 함수 입구와 출구에 `__tsan_func_entry`/`__tsan_func_exit` 호출이 들어갑니다. 인라인 검사가 아니라 **매 접근마다 런타임 함수 호출**이 일어나고, 런타임은 접근한 스레드와 시점을 shadow 셀에 기록해 다른 스레드의 접근과 happens-before 관계를 비교합니다. 메모리 접근 하나가 함수 호출 하나로 바뀌므로 ASan보다 비용이 한 단계 큽니다.

## 공식 문서가 밝히는 오버헤드

LLVM 프로젝트의 각 sanitizer 문서는 전형적인 비용을 다음과 같이 밝힙니다. [AddressSanitizer 문서](https://clang.llvm.org/docs/AddressSanitizer.html)는 전형적인 속도 저하를 2배로 적고, 메모리 사용량은 할당 크기에 따라 달라 작은 할당이 많을수록 오버헤드가 커지며, 스택 메모리는 최대 3배까지 늘어나는 것을 관찰했다고 설명합니다. [ThreadSanitizer 문서](https://clang.llvm.org/docs/ThreadSanitizer.html)는 속도 저하를 약 5–15배, 메모리 오버헤드를 약 5–10배로 적습니다. [MemorySanitizer 문서](https://clang.llvm.org/docs/MemorySanitizer.html)는 전형적인 속도 저하를 3배로 적습니다. [UndefinedBehaviorSanitizer 문서](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)는 수치 대신 검사의 런타임 비용이 작고 주소 공간 배치나 ABI에 영향을 주지 않는다고만 설명합니다.

| Sanitizer | 전형적 속도 저하 | 메모리 | 출처 |
|-----------|----------------|--------|------|
| ASan | 2× | 할당 크기에 따라 다름, 스택 최대 3× | Clang AddressSanitizer 문서 |
| TSan | 약 5–15× | 약 5–10× | Clang ThreadSanitizer 문서 |
| MSan | 3× | – | Clang MemorySanitizer 문서 |
| UBSan | 작음(수치 없음) | 배치·ABI 영향 없음 | Clang UBSan 문서 |

이 수치는 "전형적" 값이며, 자신의 코드에서의 배수는 메모리 접근 밀도, 할당 패턴, 스레드 수에 따라 달라집니다. 그래서 핵심 경로에 대해서는 한 번 직접 측정해 두는 것이 좋습니다.

## 직접 측정하기

오버헤드를 재는 방법은 단순합니다. 같은 소스를 sanitizer 없이, 그리고 sanitizer를 켜고 각각 빌드한 뒤 같은 입력으로 여러 번 실행해 비교합니다. 아래는 메모리 읽기가 대부분인 루프의 시간을 재는 최소 벤치입니다.

```cpp
// bench.cc: 메모리 접근이 많은 루프로 sanitizer 오버헤드를 재는 최소 벤치
#include <chrono>
#include <cstdio>
#include <vector>

int main() {
    std::vector<int> v(1 << 22);                    // 16 MiB
    for (std::size_t i = 0; i < v.size(); ++i) v[i] = static_cast<int>(i);

    auto t0 = std::chrono::steady_clock::now();
    long long sum = 0;
    for (int rep = 0; rep < 50; ++rep)
        for (std::size_t i = 0; i < v.size(); i += 7)   // 메모리 읽기가 대부분
            sum += v[i] ^ rep;
    auto t1 = std::chrono::steady_clock::now();

    std::printf("sum=%lld time=%.1f ms\n", sum,
                std::chrono::duration<double, std::milli>(t1 - t0).count());
}
```

```bash
clang++ -std=c++20 -O2 bench.cc -o bench_base
clang++ -std=c++20 -O2 -g -fno-omit-frame-pointer \
        -fsanitize=address,undefined bench.cc -o bench_asan

# 각각 여러 번 실행해 중앙값과 분산을 비교, 최대 메모리도 함께 기록
for b in bench_base bench_asan; do
  for i in 1 2 3 4 5; do
    /usr/bin/time -v ./$b 2>&1 | grep -E "time=|Maximum resident"
  done
done
```

참고로 Compiler Explorer의 공유 실행 환경에서 두 빌드를 한 번씩 돌렸을 때는 25.9 ms와 37.2 ms로 약 1.4배 차이였습니다. 공식 문서의 전형값 2배보다 작은 것은 이 루프가 큰 배열을 띄엄띄엄 읽어 원래부터 메모리 대기에 묶여 있고, 검사 명령의 비용이 그 대기 시간에 일부 가려지기 때문으로 보입니다. 공유 환경의 단일 측정이라 잡음이 크므로 이 숫자 자체를 일반화하면 안 되며, 이 예가 보여 주는 것은 "배수는 워크로드마다 다르다"는 사실입니다. 자신의 핵심 벤치에 대해 같은 절차로 중앙값을 구해 두면, CI에서 sanitizer 빌드의 테스트 시간 한도를 정할 때도 근거가 됩니다.

## 디버그·CI·릴리즈 전략

Sanitizer를 배치하는 원칙은 "개발과 CI에서는 적극적으로 켜고, 성능 측정과 릴리즈에서는 끈다"입니다. 로컬 개발과 단위 테스트에서는 ASan+UBSan 빌드를 기본으로 두면 메모리 오류와 미정의 동작이 테스트를 작성하는 순간 드러납니다. CI에서는 같은 테스트 스위트를 ASan+UBSan 빌드와 TSan 빌드로 각각 돌리되, 실행 시간이 일반 빌드의 몇 배가 되므로 빠른 기본 검사 단계와 sanitizer 단계를 분리하거나 sanitizer 빌드를 야간 작업으로 돌리는 구성이 흔합니다.

릴리즈 바이너리에는 표준 sanitizer 런타임을 넣지 않습니다. 성능 비용만이 이유가 아닙니다. AddressSanitizer 문서는 런타임이 프로덕션 실행 파일에 링크되도록 만들어지지 않았고 보안을 고려해 개발되지 않아 결과 실행 파일의 보안을 해칠 수 있다고 경고합니다. 다만 UBSan 문서는 공격 표면이 작은 최소 런타임(minimal runtime)을 프로덕션용으로 제공하며, 그 경우에도 보안 측면을 신중히 검토하라고 덧붙입니다.

성능 측정 빌드는 반드시 sanitizer가 꺼진 상태여야 합니다. 이를 사람의 주의에 맡기지 않으려면 빌드 시스템에서 sanitizer를 기본값이 꺼진 옵션으로 분리합니다.

```cmake
cmake_minimum_required(VERSION 3.13)   # target_link_options 사용
project(app CXX)

# Sanitizer는 옵션으로만 켠다 (기본 OFF -> 릴리즈·벤치는 sanitizer 없음)
option(ENABLE_SANITIZERS "Build with ASan+UBSan" OFF)

add_executable(app main.cpp)

if(ENABLE_SANITIZERS)
  target_compile_options(app PRIVATE
    -fsanitize=address,undefined -fno-omit-frame-pointer -g)
  target_link_options(app PRIVATE -fsanitize=address,undefined)
endif()
```

`cmake -DENABLE_SANITIZERS=ON`으로 검사용 빌드를 만들고, 기본 설정으로 벤치·릴리즈 빌드를 만들면 "sanitizer를 켠 채 벤치마크"하는 실수가 구조적으로 막힙니다.

## 판단 기준: 어떤 빌드에 무엇을 켤지

| 빌드 | 권장 | 비권장 |
|------|------|--------|
| 로컬 개발·단위 테스트 | ASan+UBSan 기본, 동시성 의심 시 TSan | 경고가 없다는 이유로 sanitizer 생략 |
| CI | ASan+UBSan, TSan을 별도 잡으로 | 한 바이너리에 ASan과 TSan 동시 지정 |
| 벤치마크·릴리즈 | sanitizer 끔(필요하면 UBSan 최소 런타임 검토) | 표준 ASan 런타임을 프로덕션에 링크 |

## 자주 하는 실수

- **UBSan은 비용이 0이라고 생각하기**: 문서의 표현은 "작다"이지 "없다"가 아니다. 예를 들어 `int` 배열을 더하는 루프는 Clang 19.1.0 `-O2 -mavx2`에서 `vpaddd`로 벡터화되지만, `-fsanitize=signed-integer-overflow`를 더하면 덧셈마다 오버플로 검사가 붙어 벡터 명령이 모두 사라졌다. 핫 루프라면 UBSan도 측정 대상이다.
- **ASan이 모든 메모리 오류를 잡는다고 생각하기**: ASan은 실행된 경로에서, redzone이나 격리 영역에 걸린 접근만 잡는다. 실행되지 않은 코드의 버그는 보이지 않고, redzone을 건너뛰어 다른 유효한 객체에 닿는 오버플로나 오래전에 해제되어 재사용된 메모리 접근은 놓칠 수 있다.
- **sanitizer 경고가 없으면 안전하다고 보기**: 경고가 없다는 것은 테스트가 실행한 경로에서 해당 도구가 감지할 수 있는 오류가 없었다는 뜻일 뿐이다. 테스트 커버리지와 퍼징을 함께 늘려야 의미가 커진다.

## 학습 성과 목표

- ASan의 shadow 메모리 검사와 TSan의 런타임 호출이 계측 코드로 어떻게 나타나는지 설명하고, 이것이 오버헤드의 크기 차이로 이어지는 이유를 말할 수 있다.
- Clang 공식 문서의 전형적 오버헤드(ASan 2배, TSan 5–15배, MSan 3배)를 출처와 함께 인용하고, 자신의 워크로드에서 직접 측정할 수 있다.
- 디버그·CI·릴리즈 빌드별로 sanitizer를 배치하고, 빌드 시스템으로 벤치마크 빌드에서 sanitizer를 배제할 수 있다.

## 비판적 시각: 한계와 트레이드오프

Sanitizer는 동적 분석 도구라서 테스트가 실행한 경로만 검사합니다. 커버리지가 낮은 코드베이스에서 "ASan CI가 통과했다"는 사실은 생각보다 약한 보증입니다. 또 sanitizer로 계측하지 않은 서드파티 라이브러리 내부의 오류는 보이지 않거나, MSan처럼 모든 의존성을 계측해야 정확해지는 도구는 도입 비용이 큽니다. 프로덕션에서 메모리 오류를 잡고 싶다면 다른 설계의 도구를 봐야 합니다. [GWP-ASan](https://llvm.org/docs/GwpAsan.html)은 할당 일부만 표본으로 골라 guard page를 붙이는 방식으로 프로덕션 환경에서 use-after-free와 힙 오버플로를 찾도록 설계됐고, [HWASan](https://clang.llvm.org/docs/HardwareAssistedAddressSanitizerDesign.html)은 AArch64의 포인터 상위 바이트 태그를 이용해 ASan보다 적은 메모리로 비슷한 오류를 잡습니다. 두 도구 모두 검출 범위나 하드웨어 지원에서 ASan과 다른 절충을 하므로, 개발 단계의 ASan을 대체하기보다 보완하는 도구로 보는 것이 맞습니다.

## 다음 장에서는

**디버그 정보와 성능**의 관계, 릴리즈 빌드에서 심볼 유지 전략을 다룹니다.

→ [디버그 정보와 성능](/post/compiler-optimization/debug-info-and-release-performance/) (챕터 10)
