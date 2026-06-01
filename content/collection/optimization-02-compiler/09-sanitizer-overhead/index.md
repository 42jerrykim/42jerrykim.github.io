---
collection_order: 9
date: 2026-03-11
lastmod: 2026-06-01
draft: true
title: "[Compiler 02] Sanitizer 성능 오버헤드"
slug: sanitizer-overhead-performance
description: "AddressSanitizer, UBSan, TSan 등 동작 개요와 런타임 오버헤드, 디버그/CI vs 릴리즈 전략, 성능 측정 시 비활성화 필요성을 다룹니다."
tags:
  - C++
  - Performance
  - Optimization
  - Compiler
  - CPU
  - Cache
  - Memory
  - Benchmark
  - Profiling
  - CI-CD
  - Testing
  - 성능
  - 최적화
  - 컴파일러
  - 프로파일링
  - 테스트
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Linux
  - Windows
  - OS
  - 운영체제
  - Concurrency
  - 동시성
  - Latency
  - Throughput
  - Backend
  - 백엔드
  - Embedded
  - 임베디드
  - Debugging
  - 디버깅
  - Documentation
  - 문서화
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Best-Practices
  - Git
  - Automation
  - 자동화
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Data-Structures
  - 자료구조
  - Time-Complexity
  - 시간복잡도
  - Complexity-Analysis
  - 복잡도분석
  - Edge-Cases
  - 엣지케이스
  - Pitfalls
  - 함정
  - Error-Handling
  - 에러처리
  - Guide
  - 가이드
  - Reference
  - 참고
  - Technology
  - 기술
  - Tutorial
  - 튜토리얼
  - Advanced
  - Deep-Dive
  - 실습
  - Case-Study
  - Assembly
---

Sanitizer는 메모리·미정의 동작·데드락 검사에 유용하지만 런타임 비용이 큽니다. 이 챕터에서는 오버헤드와 사용 전략을 다룹니다.

## Sanitizer 종류와 동작 개요

Sanitizer는 공통적으로 **컴파일 시 검사 코드를 삽입(instrumentation)**해, 런타임에 잘못된 메모리 접근·미정의 동작·데이터 레이스를 그 즉시 잡아내는 도구입니다. 무엇을 잡는지에 따라 네 가지로 나뉘며, 검사 방식이 다른 만큼 오버헤드의 크기와 성격도 다릅니다. 아래에서 각 도구가 잡는 문제와 비용을 정리합니다.

- **AddressSanitizer(ASan)**: 힙 버퍼 오버플로우, use-after-free, 이중 해제 등을 검사합니다. 할당 시 주변에 "빨간 구역(redzone)"을 두고, 접근 시 해당 영역이 유효한지 검사합니다. 메모리 접근마다 체크가 들어가고, 할당 구조가 바뀌어 **메모리 사용량**이 크게 늘어납니다(보통 2~3배). **속도**도 2~5배 정도 느려지는 경우가 많습니다.
- **UndefinedBehaviorSanitizer(UBSan)**: 정수 오버플로우, null 역참조, 잘못된 캐스트 등 **미정의 동작**이 일어나는 순간을 잡습니다. 해당 연산이 실행될 때만 검사가 들어가므로, ASan보다는 오버헤드가 적지만, 핫 경로에 해당 연산이 많으면 눈에 띄게 느려질 수 있습니다.
- **ThreadSanitizer(TSan)**: 데이터 레이스(두 스레드가 동시에 같은 메모리를 접근하고 그중 하나는 쓸 때)를 검사합니다. 메모리 접근과 동기화 이벤트를 기록하므로 **메모리·속도** 모두 상당한 오버헤드가 듭니다(수 배 느려지고 메모리도 많이 씀).
- **MemorySanitizer(MSan)**: 초기화되지 않은 메모리 읽기를 찾습니다. 미초기화 비트맵을 유지해야 해서 오버헤드가 큽니다.

이들 도구는 **디버깅·CI**에서 버그를 찾는 데 매우 유용하지만, **릴리즈 빌드**나 **성능 측정용 빌드**에는 사용하지 않는 것이 원칙입니다.

## Sanitizer 빌드·실행 명령

Sanitizer는 컴파일·링크 양쪽에 `-fsanitize=` 플래그를 주어 활성화합니다. 계측 코드가 삽입되므로 **빌드와 링크에 같은 플래그**를 넘겨야 하고, 디버깅을 위해 `-g`와 프레임 포인터 유지(`-fno-omit-frame-pointer`)를 함께 두는 것이 일반적입니다. GCC와 Clang의 플래그 이름은 거의 같습니다.

```bash
# AddressSanitizer + UndefinedBehaviorSanitizer (가장 흔한 조합)
clang++ -std=c++20 -g -O1 -fno-omit-frame-pointer \
        -fsanitize=address,undefined app.cpp -o app_asan

# ThreadSanitizer (데이터 레이스 검사; ASan과 동시 사용 불가)
clang++ -std=c++20 -g -O1 -fsanitize=thread app.cpp -o app_tsan

# 실행 시 옵션은 환경 변수로 제어 (예: 첫 오류에서 중단)
ASAN_OPTIONS=halt_on_error=1:detect_leaks=1 ./app_asan
```

ASan과 TSan은 런타임 구조가 충돌하므로 **한 바이너리에 함께 켤 수 없습니다**. UBSan은 ASan·TSan 어느 쪽과도 조합할 수 있습니다. 실행 시 동작은 `ASAN_OPTIONS`·`UBSAN_OPTIONS`·`TSAN_OPTIONS` 환경 변수로 조정합니다.

## 역사·배경

**AddressSanitizer(ASan)**는 2010년대 초 Google에서 개발되어 LLVM/Clang에 통합되었고, **UndefinedBehaviorSanitizer(UBSan)**·**ThreadSanitizer(TSan)**도 LLVM 생태계에서 표준화되었습니다. GCC도 비슷한 Sanitizer 옵션을 제공합니다. 이들은 메모리 오류·미정의 동작·데이터 레이스를 빌드 시 계측으로 잡아 주지만, 런타임 오버헤드가 크기 때문에 프로덕션에서는 사용하지 않고 디버그·CI에 한정해 사용합니다. LLVM 문서도 ASan을 "빠른 검출기"로 소개하면서 전형적 비용을 명시합니다.

> "AddressSanitizer is a fast memory error detector. It consists of a compiler instrumentation module and a run-time library. ... Typical slowdown introduced by AddressSanitizer is 2x." — [Clang documentation: AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

## ASan 리포트 읽기

Sanitizer의 가치는 오류 발생 **시점과 위치**를 정확히 보여 주는 데 있습니다. 아래는 해제된 메모리를 다시 읽는 use-after-free를 ASan이 보고한 출력의 발췌입니다(실제 출력은 더 길며, 주소·오프셋은 실행마다 다릅니다).

```text
==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000050
READ of size 4 at 0x602000000050 thread T0
    #0 0x4a1c2d in process(int*) app.cpp:8:12
    #1 0x4a1d40 in main app.cpp:15:3
0x602000000050 is located 0 bytes inside of 4-byte region
freed by thread T0 here:
    #0 0x49e1a0 in operator delete(void*)
    #1 0x4a1d10 in main app.cpp:14:3
previously allocated by thread T0 here:
    #0 0x49d9a0 in operator new(unsigned long)
    #1 0x4a1cf0 in main app.cpp:13:18
```

리포트는 **무엇이**(heap-use-after-free), **어디서**(app.cpp:8), 그 메모리가 **언제 해제·할당되었는지**(app.cpp:14, app.cpp:13)를 스택 트레이스로 함께 보여 줍니다. 라인 번호가 나오려면 `-g`로 빌드해야 하므로, Sanitizer 빌드에는 디버그 정보를 함께 켜 둡니다.

## 런타임 오버헤드 정량

- **ASan**: 벤치마크에 따라 다르지만, 전형적으로 **2~3배 메모리**, **1.5~3배 실행 시간** 증가가 보고됩니다. I/O 위주 워크로드에서는 상대적으로 덜 느려질 수 있고, 메모리 접근이 많은 수치 코드에서는 크게 느려집니다.
- **UBSan**: 검사되는 연산이 적으면 1.1배 미만으로 끝나지만, 정수 연산·캐스트가 많은 경로에서는 1.5배 이상 나올 수 있습니다.
- **TSan**: 멀티스레드 벤치마크에서 **5~15배** 느려지고 메모리도 수 배 늘어나는 경우가 있습니다.

정확한 수치는 워크로드와 플랫폼에 따라 다르므로, 자신의 핵심 경로에서 Sanitizer on/off를 켜고 끄며 한 번 측정해 두면 기준이 됩니다.

오버헤드를 가늠하려면 **같은 소스를 san on/off로 빌드해 같은 입력으로 실행**하고 시간을 비교하면 됩니다. 아래는 동일 바이너리를 두 가지 빌드로 만들어 실행 시간을 재는 최소 스켈레톤입니다.

```bash
# 동일 소스를 baseline / asan 두 가지로 빌드
clang++ -std=c++20 -O2 bench.cpp -o bench_base
clang++ -std=c++20 -O2 -g -fno-omit-frame-pointer \
        -fsanitize=address,undefined bench.cpp -o bench_asan

# 각각 여러 번 실행해 비교 (실제로는 평균·표준편차를 봐야 함)
for b in bench_base bench_asan; do
  echo "== $b =="
  for i in 1 2 3; do /usr/bin/time -v ./$b 2>&1 | grep "wall clock"; done
done
```

아래 표의 배수는 **예시값**으로, 실제 수치는 CPU·컴파일러·플래그·워크로드에 따라 크게 달라집니다(메모리 접근이 많은 코드일수록 ASan 배수가 커지고, I/O 위주면 작아집니다).

| 빌드 | 실행 시간(예시 배수) | 메모리(예시 배수) | 비고 |
|------|------------------|-----------------|------|
| baseline (`-O2`) | 1.0× | 1.0× | 측정 기준 |
| ASan (`-fsanitize=address`) | 1.5~3× | 2~3× | 메모리 접근 많을수록 큼 |
| UBSan (`-fsanitize=undefined`) | 1.0~1.5× | ~1× | 검사 연산 수에 비례 |
| TSan (`-fsanitize=thread`) | 5~15× | 수 배 | 멀티스레드 동기화 기록 |

## 디버그/CI vs 릴리즈 전략

Sanitizer는 "어디서 켜고 어디서 끄느냐"가 핵심입니다. 큰 원칙은 **개발·CI 단계에서는 적극적으로 켜서 버그를 조기에 잡고, 릴리즈·성능 측정에서는 끈다**는 것입니다. 빌드 목적별로 정리하면 다음과 같습니다.

- **디버그 빌드·로컬 테스트**: ASan, UBSan을 켜서 메모리 오류·미정의 동작을 조기에 잡습니다. TSan은 동시성 버그가 의심될 때 사용합니다.
- **CI**: PR마다 또는 매일 ASan/UBSan(및 필요 시 TSan) 빌드를 돌려, 릴리즈 빌드에서는 드러나지 않는 버그를 자동으로 걸러냅니다. CI 시간이 길어지므로, 빠른 체크용 빌드와 Sanitizer 빌드를 단계로 나누는 경우가 많습니다.
- **릴리즈**: Sanitizer는 **끕니다**. 오버헤드와 호환성(일부 환경에서 Sanitizer 라이브러리 미지원) 때문에 프로덕션에서는 사용하지 않습니다.

## 성능 측정 시 Sanitizer 비활성화

**성능 벤치마크·프로파일링**을 할 때는 반드시 **Sanitizer가 꺼진** 빌드로 측정해야 합니다. 그렇지 않으면 측정 결과가 실제 릴리즈 성능을 전혀 반영하지 못합니다. 빌드 스크립트에서 "benchmark" 또는 "release" 설정은 Sanitizer 플래그를 넣지 않도록 하고, 실수로 Sanitizer가 켜진 상태로 벤치마크한 결과를 릴리즈 판단에 쓰지 않도록 합니다.

이를 강제하는 가장 안전한 방법은 **Sanitizer를 옵션으로 분리**해, 벤치/릴리즈 빌드에서는 끄는 것입니다. CMake에서는 옵션 플래그를 별도로 두고 디버그 검사 빌드에만 적용합니다.

```cmake
# Sanitizer는 옵션으로만 켠다 (기본 OFF -> 릴리즈·벤치는 san 없음)
option(ENABLE_SANITIZERS "Build with ASan+UBSan" OFF)

add_executable(app main.cpp)

if(ENABLE_SANITIZERS)
  target_compile_options(app PRIVATE
    -fsanitize=address,undefined -fno-omit-frame-pointer -g)
  target_link_options(app PRIVATE -fsanitize=address,undefined)
endif()
```

이렇게 두면 `cmake -DENABLE_SANITIZERS=ON`으로 검사용 빌드를, 기본 설정으로 벤치/릴리즈 빌드를 만들 수 있어 "san 켠 채로 벤치"하는 실수를 구조적으로 막습니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **redzone** | ASan이 할당 주변에 두는 "빨간 구역"; 접근 시 유효성 검사에 사용 |
| **instrumented 빌드** | Sanitizer 계측이 삽입된 빌드; 실행 시 검사·기록으로 오버헤드 발생 |

## 판단 기준: 언제 Sanitizer를 쓸지 / 피할지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 디버그·로컬 테스트 | ASan, UBSan(필요 시 TSan) | 릴리즈 빌드에 Sanitizer |
| CI | ASan/UBSan(및 TSan) 별도 타겟 | 성능 측정용 빌드에 Sanitizer |
| 릴리즈·벤치마크 | Sanitizer 끔 | Sanitizer 켠 상태로 성능 판단 |

## 자주 하는 실수

- **Sanitizer 켠 채로 벤치마크**: 성능 숫자는 Sanitizer가 꺼진 빌드에서만 의미 있다. 실수로 ASan/UBSan/TSan이 켜진 상태로 측정한 결과를 "릴리즈 성능"으로 보고하면 안 된다. 벤치 타겟에서는 Sanitizer 플래그를 넣지 않도록 빌드 스크립트를 분리한다.
- **릴리즈 빌드에 Sanitizer 포함**: 프로덕션 바이너리에 Sanitizer를 켜면 오버헤드(2~수 배 느려짐, 메모리 증가)와 호환성 문제(일부 환경 미지원)가 생긴다. 디버그·CI 전용으로만 사용한다.

## 학습 성과 목표

- **ASan·UBSan·TSan** 등 Sanitizer의 오버헤드(메모리·속도)를 설명할 수 있다.
- 디버그/CI에서는 Sanitizer를 켜고, 릴리즈·성능 측정에서는 끄는 전략을 적용할 수 있다.
- 성능 벤치마크 시 Sanitizer 비활성화가 필수임을 설명할 수 있다.

## 비판적 시각: 한계와 트레이드오프

Sanitizer는 **버그 찾기용 도구**이지, 성능 개선 도구가 아니다. 오버헤드가 크기 때문에 프로덕션에서는 쓰지 않고, 디버그·CI에서만 제한적으로 사용한다. "ASan을 켜두면 안전하다"는 식으로 릴리즈에 포함하면 안 되며, 성능 측정 시에는 반드시 Sanitizer를 끈 빌드로만 숫자를 본다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 오버헤드 | ASan 2~3배 메모리·1.5~3배 시간; TSan 수 배~수십 배 |
| 사용 | 디버그·CI에서 버그 검사; 릴리즈에서는 미사용 |
| 벤치마크 | Sanitizer 끈 빌드로만 측정 |

## 다음 장에서는

**디버그 정보와 성능**의 관계, 릴리즈 빌드에서 심볼 유지 전략을 다룹니다.

→ [디버그 정보와 성능](/post/compiler-optimization/debug-info-and-release-performance/) (챕터 10)
