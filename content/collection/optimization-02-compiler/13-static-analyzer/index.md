---
collection_order: 13
date: 2026-03-11
lastmod: 2026-06-01
draft: true
title: "[Compiler 02] 성능 관련 정적 분석"
slug: static-analyzer-performance
description: "성능 관련 컴파일러·정적 분석 경고(미사용 결과·불필요한 복사·비효율 루프), Clang Static Analyzer·GCC -fanalyzer, CI에 경고 통합하고 벤치마크와 분리해 성능 회귀와 연계하는 방법을 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU
  - Cache
  - Memory(메모리)
  - Benchmark
  - Profiling(프로파일링)
  - CI-CD
  - Testing(테스트)
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Linux(리눅스)
  - Windows(윈도우)
  - OS(운영체제)
  - Concurrency(동시성)
  - Latency
  - Throughput
  - Backend(백엔드)
  - Embedded(임베디드)
  - Debugging(디버깅)
  - Documentation(문서화)
  - Refactoring(리팩토링)
  - Clean-Code(클린코드)
  - Best-Practices
  - Git
  - Automation(자동화)
  - Software-Architecture(소프트웨어아키텍처)
  - Design-Pattern(디자인패턴)
  - Data-Structures(자료구조)
  - Time-Complexity(시간복잡도)
  - Complexity-Analysis(복잡도분석)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Error-Handling(에러처리)
  - Guide(가이드)
  - Reference(참고)
  - Technology(기술)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Case-Study
  - Assembly
---

컴파일러와 정적 분석기는 미사용 결과, 비효율 루프 등 성능 관련 경고를 낼 수 있습니다. 이 챕터에서는 도구와 CI 연계를 다룹니다.

## 성능 관련 컴파일러·정적 분석 경고

컴파일러와 정적 분석 도구는 **성능과 직간접적으로 연관된** 경고를 내놓을 수 있습니다. 대표적인 것만 정리하면 다음과 같습니다.

- **미사용 결과 / 불필요한 복사**: 함수 반환값을 쓰지 않거나, 값으로 받을 때 복사가 불필요하게 일어나는 경우. `-Wunused-result`, `-Wunused-value` 또는 분석기별 "무시된 반환값", "복사 대신 이동 가능" 같은 메시지가 나올 수 있습니다. 불필요한 복사는 Tr.01(객체 수명, 파라미터 전달)과도 연결됩니다.
- **비효율적인 루프/알고리즘**: 루프 안에서 매 반복마다 불변 식을 계산하거나, 더 적합한 자료 구조가 있는데 비효율적인 연산을 쓰는 패턴. 일부 분석기는 "이 루프는 O(n²)이고, 정렬된 구조를 쓰면 개선될 수 있다" 수준의 힌트를 주기도 합니다.
- **분기·비교**: 항상 참/거짓인 조건, 죽은 분기 등은 최적화 단계에서 제거되지만, 정적 분석기는 "이 조건은 불필요하다"는 식의 경고를 낼 수 있어, 코드 단순화·성능에 도움이 됩니다.

이런 경고는 **버그**가 아니라 **개선 여지**를 알려 주는 것이므로, 가능하면 켜 두고 중요한 항목부터 수정하는 것이 좋습니다.

## Clang Static Analyzer / GCC -fanalyzer

두 도구 모두 **성능 전용**이 아니라 정확성·안전성 위주이지만, 출력되는 경고 중에는 "이렇게 바꾸면 더 빠르거나 더 단순해진다"에 해당하는 것이 섞여 있으므로, 성능 트랙에서는 그런 항목을 골라 개선 포인트로 활용할 수 있습니다.

> "The Clang Static Analyzer is a source code analysis tool that finds bugs in C, C++, and Objective-C programs." — [Clang Static Analyzer](https://clang-analyzer.llvm.org/)

### Clang Static Analyzer (scan-build) 사용법

```bash
# CMake 프로젝트에서 scan-build 사용
scan-build cmake -DCMAKE_BUILD_TYPE=Debug ..
scan-build make -j$(nproc)

# 결과를 HTML 보고서로 저장 (기본: /tmp/scan-build-*)
scan-build -o ./analysis_report make -j$(nproc)

# 특정 체커만 활성화 (성능 관련 체커 예시)
scan-build --enable-checker alpha.performance.Padding make
```

출력 예시:
```text
scan-build: 3 bugs found.
scan-build: Run 'scan-view /tmp/scan-build-2026-06-01-123456-1234-1' to examine bug reports.

foo.cc:15:5: warning: Value stored to 'result' is never read [deadcode.DeadStores]
bar.cc:42:12: warning: Potential null pointer dereference [core.NullDereference]
baz.cc:78:8: warning: Function call argument is an uninitialized value [core.CallAndMessage]
```

위 `deadcode.DeadStores`처럼 "저장했지만 읽지 않는 값"은 죽은 계산을 알려 주므로, 핫 경로에 있다면 불필요한 연산을 줄이는 단서가 됩니다.

### GCC -fanalyzer 사용법

```bash
# 단일 파일 분석
g++ -O2 -fanalyzer foo.cc -c 2>&1 | grep "warning:"

# CMake 프로젝트: 분석 빌드용 플래그 추가
cmake -DCMAKE_CXX_FLAGS="-fanalyzer" -DCMAKE_BUILD_TYPE=Debug ..
make -j$(nproc) 2>&1 | grep -E "warning:|note:"
```

`-fanalyzer`는 컴파일 시간이 늘어나므로 CI의 별도 "static analysis" 단계에서만 켜는 것이 좋습니다. GCC 12 이상에서 지원 수준이 더 좋습니다.

**Clang Static Analyzer**는 Clang 기반의 정적 분석기로, 메모리 누수·null 역참조·데이터 플로우 이상 등과 함께, 일부 성능 관련 이슈(불필요한 연산, 개선 가능한 패턴)를 보고할 수 있습니다. **GCC -fanalyzer**는 GCC 10부터 포함된 정적 분석 패스입니다.

### clang-tidy의 성능 체크

**clang-tidy**는 `performance-*` 계열 체크를 따로 제공해, 불필요한 복사·값 전달·범위 기반 루프의 복사 등을 직접 짚어 줍니다. `compile_commands.json`(CMake가 `CMAKE_EXPORT_COMPILE_COMMANDS=ON`으로 생성)을 읽어 프로젝트 전체에 적용할 수 있습니다.

```bash
# compile_commands.json 생성 후 performance 체크만 실행
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
clang-tidy -p build --checks='-*,performance-*' src/*.cpp
```

예를 들어 `performance-unnecessary-value-param`은 "복사 대신 const 참조로 받으라"는 식으로, 핫 경로의 불필요한 복사를 줄이는 데 직접 쓰입니다.

## CI에 경고 통합하고 성능 회귀와 연계

정적 분석을 실효성 있게 쓰려면 경고를 사람이 가끔 보는 것이 아니라 **CI에서 자동으로 관리**해야 합니다. 다만 정적 분석은 성능을 직접 측정하지 않으므로, "경고 관리"와 "벤치마크 기반 회귀 측정"을 별개의 단계로 두고 함께 운영하는 것이 핵심입니다.

- **경고를 CI에 넣기**: 컴파일 시 `-Wall -Wextra` 및 분석기 플래그를 켜고, **새로 발생하는 경고**를 실패로 두거나, 기존 경고 목록을 baseline으로 두고 **증가분만** 실패로 두는 방식을 씁니다. 성능 관련 경고만 필터링해 실패로 두는 것도 가능합니다.
- **성능 회귀와 연계**: 정적 분석 경고 자체는 "성능 회귀"를 직접 측정하지는 않습니다. 다만 "미사용 결과", "불필요한 복사" 등을 줄이면 실제 벤치마크에서 회귀가 나올 가능성을 낮출 수 있습니다. CI 파이프라인에서는 (1) 정적 분석으로 경고를 관리하고, (2) 별도 단계에서 **벤치마크**를 돌려 수치적 회귀를 잡는 두 단계를 함께 두는 구성을 권장합니다. 경고 제거가 곧 성능 개선은 아니지만, 코드 품질과 잠재적 성능 이슈를 한 번에 다루는 데 도움이 됩니다.

GitHub Actions에서는 빌드와 분리된 "static-analysis" job을 두어 분석만 돌립니다. 분석은 컴파일 시간이 늘어나므로 일반 빌드·테스트와 병렬 job으로 분리하는 것이 좋습니다.

```yaml
static-analysis:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Configure (export compile_commands.json)
      run: cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    - name: clang-tidy (performance checks)
      run: clang-tidy -p build --checks='-*,performance-*' src/*.cpp
```

## 용어 정리

| 용어 | 설명 |
|------|------|
| **scan-build** | Clang Static Analyzer를 빌드와 함께 실행하게 하는 래퍼 스크립트 |
| **-fanalyzer** | GCC 10부터 제공되는 정적 분석 패스; 컴파일 시 함께 수행, 메모리·리소스 이슈 등 보고 |

## 판단 기준: 언제 정적 분석을 쓸지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| CI | Clang Static Analyzer·GCC -fanalyzer 별도 단계 | 분석 없이 릴리즈만 |
| 성능 경고 | 미사용 결과·불필요한 복사 등 개선 포인트로 활용 | 경고 무시·비활성화 |
| 회귀 | 정적 분석 + 벤치마크 단계 분리 | 경고만으로 성능 보장 가정 |

## 자주 하는 실수

- **경고 제거 = 성능 개선으로 오해**: 정적 분석 경고(미사용 결과, 불필요한 복사 등)를 고치면 코드 품질이 나아지고 잠재적 이슈가 줄어들지만, **경고를 없앴다고 해서 실제 벤치마크 수치가 개선된다는 보장은 없다**. 성능 회귀는 별도 벤치마크 단계로 측정해야 한다.
- **분석 없이 릴리즈만**: 정적 분석을 CI에 넣지 않고 빌드·릴리즈만 하면, 개선 가능한 패턴과 잠재적 버그를 놓친다. Clang Static Analyzer·GCC -fanalyzer를 별도 단계로 돌리고, 중요한 경고를 실패로 두는 정책을 두는 것이 좋다.

## 학습 성과 목표

- **성능 관련** 컴파일러·정적 분석 경고(미사용 결과·복사·루프 등)를 설명할 수 있다.
- **Clang Static Analyzer·GCC -fanalyzer**를 CI에 통합하고, 성능 경고를 골라 활용할 수 있다.
- 정적 분석과 **벤치마크 기반 회귀 측정**을 구분해 둘 다 적용할 수 있다.

## 비판적 시각: 한계와 트레이드오프

정적 분석기는 **성능 전용 도구가 아니다**. 주된 목적은 정확성·안전성(메모리, 리소스, 데이터 플로우)이고, 성능 관련 경고는 그중 일부일 뿐이다. "경고를 다 없애면 성능이 보장된다"는 잘못된 생각을 피하고, 경고는 코드 품질·개선 포인트로 활용하고, 실제 성능은 **벤치마크**로 따로 측정하는 것이 전문가다운 구분이다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 경고 | 미사용 결과·불필요한 복사·비효율 루프 등 |
| 도구 | scan-build(Clang), -fanalyzer(GCC) |
| CI | 경고 관리 + 별도 벤치마크로 회귀 측정 |

## 다음 장에서는

**BOLT·후링크(post-link) 최적화** 개념, PGO·LTO와의 순서 감각, 프로파일 대표성과 CI 재현성, 적용 판단 기준을 다룹니다.

→ [BOLT·후링크 최적화](/post/compiler-optimization/bolt-post-link-binary-layout-optimization/) (챕터 14)
