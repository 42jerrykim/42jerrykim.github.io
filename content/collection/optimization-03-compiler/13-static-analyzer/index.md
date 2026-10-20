---
collection_order: 13
date: 2026-03-11
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Compiler 03] 성능 관련 정적 분석"
slug: static-analyzer-performance
description: "Clang Static Analyzer·GCC -fanalyzer·clang-tidy의 분석 원리와 비용, 패딩·불필요한 복사·죽은 저장 같은 성능 관련 경고의 실제 출력과 대처, CI에서 정적 분석과 벤치마크를 분리 운영하는 방법을 다룹니다."
tags:
  - C++
  - C
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - Memory(메모리)
  - Cache
  - Code-Quality(코드품질)
  - Debugging(디버깅)
  - Testing(테스트)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Reliability
  - Linux(리눅스)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - Comparison(비교)
  - Open-Source(오픈소스)
  - Clang
  - GCC
  - LLVM
  - Static-Analysis
  - clang-tidy
  - GitHub-Actions
---

정적 분석기는 프로그램을 실행하지 않고 소스만 보고 결함을 찾는 도구입니다. 대부분은 메모리 안전성과 정확성을 위한 도구지만, 그중 일부 체크는 불필요한 복사, 낭비되는 구조체 패딩, 읽히지 않는 계산처럼 성능과 직결된 패턴을 짚어 줍니다. 이 챕터에서는 Clang Static Analyzer, GCC `-fanalyzer`, clang-tidy가 어떤 원리로 동작하고 성능 관점에서 무엇을 잡아 주는지, 실제 경고가 어떻게 생겼는지, 그리고 CI에서 경고 관리와 벤치마크를 어떻게 나눠 운영하는지를 다룹니다. 본문의 경고 메시지는 2026년 10월 [Compiler Explorer](https://godbolt.org)의 x86-64 clang 19.1.0과 clang-tidy(trunk)에서 얻은 실제 출력입니다.

## 세 도구의 동작 원리와 비용

세 도구는 이름이 비슷하게 묶이지만 분석 방식이 달라서, 잡는 문제와 드는 비용이 다릅니다.

[Clang Static Analyzer](https://clang-analyzer.llvm.org/)(CSA)는 공식 사이트의 설명대로 심볼릭 실행에 기반한 경로 민감·프로시저 간 분석을 합니다. 함수 안의 분기를 따라가며 "이 경로에서 이 변수는 null일 수 있다" 같은 상태를 추적하므로, 특정 경로에서만 일어나는 null 역참조나 해제 후 사용을 찾을 수 있습니다. 같은 사이트는 이런 깊은 분석 때문에 정적 분석이 컴파일보다 훨씬 느릴 수 있고, 거짓 양성(false positive)이 체커마다 크게 다르다고 밝힙니다.

GCC의 `-fanalyzer`도 비슷한 방식입니다. [GCC Static Analyzer Options 문서](https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html)는 이를 커버리지 유도 심볼릭 실행으로 설명하고, 건전하지도 완전하지도 않아 거짓 양성과 거짓 음성이 모두 있을 수 있는 버그 찾기 도구라고 명시합니다. 중요한 제약도 같은 문서에 있습니다. 최신 매뉴얼과 GCC 14.2 매뉴얼 모두 "The analyzer is only suitable for use on C code in this release."라고 적고 있으므로, C++ 프로젝트에 `-fanalyzer`를 그대로 켜는 것은 현재 공식적으로 권장되는 사용법이 아닙니다. C++ 코드에는 CSA와 clang-tidy를 쓰는 편이 맞습니다.

[clang-tidy](https://clang.llvm.org/extra/clang-tidy/)는 경로를 추적하지 않고 AST(추상 구문 트리)의 패턴을 매칭하는 린터입니다. 분석이 가볍고 결정론적이라 거짓 양성이 상대적으로 적은 대신, "이 경로에서만 생기는 문제"는 찾지 못합니다. 성능 관점에서 가장 직접적으로 쓸모 있는 도구는 이쪽으로, `performance-` 접두사가 붙은 체크 묶음이 불필요한 복사와 비효율적인 표준 라이브러리 사용을 짚어 줍니다.

## 실제 경고로 보는 성능 관련 체크

### CSA: 죽은 저장과 구조체 패딩

아래 파일에는 성능과 정확성 문제가 섞여 있습니다. `Packet`은 필드 순서 때문에 패딩이 많이 생기는 구조체이고, `compute`는 계산해 놓고 쓰지 않는 값을, `deref`는 특정 분기에서만 null을 역참조하는 경로를 갖고 있습니다.

```cpp
// sa.cc
#include <cstdlib>

struct Packet {          // 필드 순서 때문에 패딩이 생기는 구조체
    char  flag;
    double value;
    char  kind;
    double weight;
    char  tag;
};

int compute(int x) {
    int result = x * 2;  // 저장했지만 읽지 않는 값
    result = x + 1;
    return result;
}

int deref(int* p, bool cond) {
    if (cond) p = nullptr;
    return *p;           // cond가 참이면 null 역참조
}

double use(const Packet& pk) { return pk.value + pk.weight; }
```

`clang++ --analyze sa.cc`로 기본 체커를 돌리면 두 개의 경고가 나옵니다. 성능 체커인 `optin.performance.Padding`은 이름의 `optin` 패키지가 뜻하듯 기본으로 꺼져 있어 명시적으로 켜야 합니다. [CSA 체커 문서](https://clang.llvm.org/docs/analyzer/checkers.html)에 따르면 이 체커는 기본 허용 패딩이 24바이트라서, 아래 예에서는 임계값(`AllowedPad`)을 낮춰 실행했습니다.

```bash
clang++ --analyze \
  -Xclang -analyzer-checker=optin.performance.Padding \
  -Xclang -analyzer-config -Xclang optin.performance.Padding:AllowedPad=2 \
  sa.cc
```

```text
<source>:3:8: warning: Excessive padding in 'struct Packet' (21 padding bytes, where 5 is optimal). Optimal fields order: value, weight, flag, kind, tag, consider reordering the fields or adding explicit padding members [optin.performance.Padding]
<source>:12:9: warning: Value stored to 'result' during its initialization is never read [deadcode.DeadStores]
<source>:19:12: warning: Dereference of null pointer (loaded from variable 'p') [core.NullDereference]
3 warnings generated.
```

패딩 경고는 성능에 직접 연결됩니다. 체커 문서는 과도한 패딩이 메모리를 낭비하고 프로세서 캐시의 효율을 떨어뜨린다고 설명하는데, 이 구조체를 배열로 대량 처리한다면 크기가 줄어든 만큼 캐시 라인 하나에 더 많은 원소가 들어갑니다. 경고가 제시한 순서(`value, weight, flag, kind, tag`)로 바꾸면 패딩이 21바이트에서 5바이트로 줄어듭니다. `deadcode.DeadStores`는 그 자체로 성능 문제라기보다 의도와 다른 코드의 신호입니다. 최적화 컴파일러는 이런 죽은 저장을 어차피 제거하므로 실행 속도에는 보통 영향이 없지만, 핫 경로에서 이 경고가 나왔다면 개발자가 의도한 계산이 실제로는 쓰이지 않고 있다는 뜻일 수 있습니다. `core.NullDereference`는 경로 민감 분석의 전형적인 결과로, `cond`가 참인 경로에서만 일어나는 문제를 찾아냈습니다.

프로젝트 전체에 적용할 때는 빌드 명령을 감싸는 `scan-build`를 씁니다. `scan-build cmake ..`로 구성한 뒤 `scan-build -o ./analysis_report make`처럼 빌드하면, 컴파일러 호출마다 분석을 끼워 넣고 결과를 HTML 보고서로 모아 줍니다. 체커는 `--enable-checker optin.performance.Padding`처럼 켭니다.

### clang-tidy: 불필요한 복사

clang-tidy의 성능 체크는 C++ 코드에서 가장 흔한 성능 실수인 불필요한 복사를 정확히 짚습니다.

```cpp
// tidy.cc
#include <string>
#include <vector>

std::size_t total_length(std::vector<std::string> names) {   // 값으로 받아 매번 복사
    std::size_t n = 0;
    for (auto s : names) n += s.size();                      // 원소마다 string 복사
    return n;
}
```

```bash
clang-tidy tidy.cc -checks='-*,performance-*' -- -std=c++20
```

```text
<source>:4:51: warning: the parameter 'names' of type 'std::vector<std::string>' (aka 'std::vector<basic_string<char>>') is copied for each invocation but only used as a const reference; consider making it a const reference [performance-unnecessary-value-param]
<source>:6:15: warning: loop variable is copied but only used as const reference; consider making it a const reference [performance-for-range-copy]
2 warnings generated.
```

두 경고는 각각 함수 호출마다 벡터 전체를 복사하는 비용과, 루프 반복마다 문자열을 복사하는 비용을 가리킵니다. [performance-unnecessary-value-param 문서](https://clang.llvm.org/extra/clang-tidy/checks/performance/unnecessary-value-param.html)의 설명대로 이 체크는 복사 비용이 큰 타입의 값 매개변수가 const 참조로 충분할 때만 경고하므로, 기계적으로 고쳐도 의미가 바뀌지 않는 경우가 대부분입니다. 같은 `performance-*` 묶음에는 `performance-inefficient-string-concatenation`(루프 안의 문자열 `+` 누적), `performance-move-const-arg`(효과 없는 `std::move`), `performance-inefficient-vector-operation`(`reserve` 없이 반복 `push_back`) 등이 있으며, 전체 목록은 [clang-tidy 체크 목록](https://clang.llvm.org/extra/clang-tidy/checks/list.html)에서 확인할 수 있습니다. 프로젝트 전체에 적용하려면 CMake에 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`을 주어 `compile_commands.json`을 만들고 `clang-tidy -p build`로 그 파일을 읽게 합니다.

## CI에서 경고 관리와 성능 측정을 나누기

정적 분석 경고는 사람이 가끔 들여다보면 쌓이기만 하므로 CI에서 자동으로 관리해야 합니다. 이미 경고가 많은 코드베이스에서 처음부터 "경고 0"을 강제하면 도입 자체가 막히므로, 현재 경고 목록을 기준선으로 저장해 두고 **새로 생긴 경고만** 실패로 처리하는 방식이 현실적입니다. 정적 분석은 컴파일보다 느리므로 일반 빌드·테스트와 다른 job으로 분리해 병렬로 돌립니다.

```yaml
name: static-analysis
on: [pull_request]

jobs:
  clang-tidy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure (export compile_commands.json)
        run: cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
      - name: clang-tidy (performance checks as errors)
        run: |
          clang-tidy -p build --checks='-*,performance-*' \
                     --warnings-as-errors='performance-*' src/*.cpp
```

여기서 구분해야 할 것은 정적 분석이 성능을 **측정하지 않는다**는 점입니다. 위 job은 "값으로 받은 벡터" 같은 패턴을 막아 줄 뿐, 어떤 변경이 핫 경로를 10% 느리게 만들었는지는 알려 주지 않습니다. 그래서 성능 회귀는 별도의 벤치마크 job이 고정된 러너에서 기준 결과와 비교해 잡아야 하고, 정적 분석 job은 그 회귀가 생길 가능성을 줄이는 예방 장치로 둡니다. 두 job을 같은 PR 검사에 나란히 두면, 패턴 수준의 실수는 리뷰 전에 걸러지고 실제 수치 변화는 벤치마크가 보고합니다.

## 판단 기준: 어떤 도구를 어디에 쓸지

| 목적 | 권장 | 비권장 |
|------|------|--------|
| C++ 코드의 불필요한 복사·비효율 패턴 | clang-tidy `performance-*`를 PR마다 실행 | 리뷰어의 눈에만 의존 |
| 경로 의존 버그(null, 해제 후 사용) | CSA(`scan-build`)를 야간 또는 별도 job으로 | 컴파일 경고만으로 대체 |
| 구조체 레이아웃 낭비 | `optin.performance.Padding`을 명시적으로 켜고 `AllowedPad` 조정 | 기본 체커만 켜고 패딩이 잡힐 것으로 기대 |
| C 코드 분석 | GCC `-fanalyzer` | C++ 프로젝트에 `-fanalyzer`를 그대로 적용 |

## 자주 하는 실수

- **CSA가 성능 체커를 기본으로 켠다고 생각하기**: 성능 체커는 `optin.performance` 패키지에 있어 명시적으로 켜야 하고, 패딩 체커는 기본 임계값이 24바이트라 작은 구조체에서는 경고가 나오지 않는다.
- **`-fanalyzer`를 C++ 분석기로 쓰기**: GCC 공식 문서는 현재 릴리스의 분석기가 C 코드에만 적합하다고 명시한다. C++에는 CSA와 clang-tidy를 쓴다.
- **경고 0이면 성능도 괜찮다고 생각하기**: 정적 분석은 알려진 패턴만 찾고 실행 시간을 재지 않는다. 성능 회귀는 벤치마크로만 확인할 수 있다.

## 학습 성과 목표

이 챕터를 마치면 정적 분석을 "경고를 없애는 일"이 아니라 성능 실수를 조기에 거르는 예방 장치로 배치할 수 있어야 합니다.

- CSA·GCC `-fanalyzer`(심볼릭 실행)와 clang-tidy(AST 패턴 매칭)의 원리 차이와 그에 따른 비용·거짓 양성 특성을 설명할 수 있다.
- `optin.performance.Padding`, `performance-unnecessary-value-param`, `performance-for-range-copy` 경고를 읽고 의미가 바뀌지 않는 수정으로 연결할 수 있다.
- CI에서 정적 분석 job과 벤치마크 job을 분리하고, 기준선 이후의 새 경고만 실패로 처리하는 정책을 설계할 수 있다.

## 비판적 시각: 한계와 트레이드오프

정적 분석의 가장 큰 비용은 시간과 신뢰입니다. 경로 민감 분석은 컴파일보다 훨씬 느려서 모든 PR에 돌리기 어렵고, 거짓 양성이 쌓이면 개발자가 경고를 무시하는 습관이 생겨 진짜 문제까지 묻힙니다. 그래서 체커를 많이 켜는 것보다, 팀이 반드시 고칠 소수의 체커를 고르고 나머지는 정기 점검으로 돌리는 편이 실효성이 큽니다. 성능 관점에서도 한계는 분명합니다. 패딩 체커는 구조체가 실제로 핫 경로에서 대량으로 쓰이는지 모르고, 복사 체크는 그 함수가 1초에 한 번 불리는지 백만 번 불리는지 모릅니다. 정적 분석이 가리킨 후보는 프로파일러로 핫스팟인지 확인한 뒤 우선순위를 정해야, 효과 없는 수정에 리뷰 시간을 쓰지 않게 됩니다.

## 다음 장에서는

**BOLT·후링크(post-link) 최적화** 개념, PGO·LTO와의 순서 감각, 프로파일 대표성과 CI 재현성, 적용 판단 기준을 다룹니다.

→ [BOLT·후링크 최적화](/post/compiler-optimization/bolt-post-link-binary-layout-optimization/) (챕터 14)
