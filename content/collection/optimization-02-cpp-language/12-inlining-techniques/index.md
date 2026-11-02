---
collection_order: 12
date: 2026-03-10
lastmod: 2026-07-10
draft: false
image: wordcloud.png
title: "[Optimization(C++) 12] 인라이닝 유도 기법"
slug: inlining-techniques
description: "코드 레벨에서 인라이닝을 유도하는 기법과 inline, __forceinline 등 활용을 다룹니다. 컴파일러 진단(Tr.03)과 연계해 인라이닝 실패 원인을 파악하고 핫패스 비용을 줄이는 방법을 정리하며, 코드 크기·디버깅 트레이드오프를 제시합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU
  - Cache
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Best-Practices
  - Clean-Code(클린코드)
  - Maintainability
  - Windows(윈도우)
  - Advanced
  - Deep-Dive
  - 실습
  - Guide(가이드)
  - Reference(참고)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Assembly(어셈블리)
  - Cache-Miss(캐시미스)
  - Inlining
  - LTO
  - Devirtualization
  - GCC
  - Clang
  - MSVC
  - ODR
---

**인라이닝 유도**란 호출 오버헤드를 없애고 상수 전파·최적화 기회를 늘리기 위해, 컴파일러가 함수를 호출부에 펼치도록 유도하는 것을 말합니다. 본 챕터에서는 **inline**·**__forceinline** 활용, 인라이닝을 유도하는 코드 패턴, 실패 원인 진단(Tr.03 연계)을 다루고 핫패스 비용을 줄이는 방법을 정리합니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 추상화 비용 분석](/post/cpp-optimization/abstraction-cost/)의 호출 오버헤드 개념을 전제로 합니다. 인라이닝이 "함수 호출을 호출부에 펼치는 것"이라는 정도만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **심화–전문가**를 포괄합니다. `inline`·`__forceinline`의 실제 의미부터 시작해, 전문가 구간에서는 인라이닝을 유도하는 코드 패턴, 컴파일러의 인라인 판단 방식, 실패 원인 진단, 코드 크기와의 트레이드오프를 다룹니다. **다루지 않는 것**: 컴파일러 인라이닝 리포트·LTO·진단 플래그의 깊은 사용법은 Tr.03 컴파일러 트랙에서 다루며, 이 장은 "코드 레벨에서 무엇을 할 수 있는가"에 집중합니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "inline 키워드와 컴파일러 최적화" | inline의 진짜 의미(ODR vs 인라이닝) 이해 |
| **중급자** | "인라이닝을 유도하는 코드 패턴" ~ "인라이닝 실패 원인과 진단 (Tr.03 연계)" | 인라인 유도·실패 진단 |
| **전문가** | "컴파일러는 무엇을 보고 인라인을 결정하는가" ~ "비판적 시각" | 코드 크기 대비 인라이닝 적용 판단 |

---

## inline 키워드와 컴파일러 최적화

**inline** 키워드의 원래 의도는 최적화기에게 "이 함수는 호출보다 본문 치환이 낫다"고 알려 주는 힌트였습니다. 그런데 컴파일러가 자체 비용 모델로 인라인 여부를 결정하게 되면서 이 힌트의 영향력은 약해졌고, 오늘날 `inline`의 실질적인 의미는 "같은 정의가 여러 번역 단위(TU)에 나와도 ODR(One Definition Rule) 위반이 아니다"라는 링크 규칙 쪽으로 옮겨 갔습니다. 헤더에 함수 정의를 둘 수 있는 것도 이 규칙 덕분입니다. 표준 문구도 힌트가 강제가 아님을 분명히 합니다.

> "The inline specifier indicates to the implementation that inline substitution of the function body at the point of call is to be preferred to the usual function call mechanism." — ISO C++ 작업 초안 [dcl.inline]/3

같은 조항은 이어서 구현이 이 치환을 반드시 수행할 필요는 없다고 덧붙입니다. 그래서 inline을 붙여도 인라인되지 않을 수 있고(재귀·크기 한도 초과), 반대로 inline 없이도 같은 TU에 정의가 보이는 작은 함수는 최적화 빌드에서 흔히 인라인됩니다.

**__forceinline**(MSVC), **__attribute__((always_inline))**(GCC/Clang)는 "가능하면 반드시 인라인해 달라"는 강한 힌트입니다. 그래도 컴파일러는 재귀 함수처럼 펼칠 수 없는 경우에는 인라인을 거부합니다. 무리하게 강제하면 코드 크기가 커지거나 컴파일이 실패할 수 있으므로, 정말 핫한 작은 함수에만 제한적으로 사용합니다.

컴파일러마다 다른 강제 인라인 키워드는 매크로로 한 번 감싸 두어야 GCC·Clang·MSVC에서 모두 컴파일됩니다. `__forceinline`을 가드 없이 쓰면 GCC/Clang에서 컴파일 오류가 나므로 이식성을 위해 전처리기 분기를 둡니다. 아래 `hot.cpp`는 이 장의 진단·어셈블리 예시가 모두 사용하는 파일입니다.

```cpp
#include <cstdio>

#if defined(_MSC_VER)
  #define FORCE_INLINE __forceinline
#elif defined(__GNUC__) || defined(__clang__)
  #define FORCE_INLINE inline __attribute__((always_inline))
#else
  #define FORCE_INLINE inline
#endif

// 작은 함수: 인라인 후보에 잘 걸림
inline int add(int a, int b) { return a + b; }

// 강한 힌트: 컴파일러는 재귀 함수 등에서는 여전히 거부할 수 있다
FORCE_INLINE int hot_path(int x) { return add(x, 1); }

int main(int argc, char**) {
    std::printf("%d\n", hot_path(argc));   // 실행 인자 개수 + 1 출력
}
```

## 인라이닝을 유도하는 코드 패턴

인라이닝은 결국 "컴파일러가 호출부에서 피호출 함수의 본문을 볼 수 있고, 펼쳤을 때 이득이 크다고 판단하는가"의 문제입니다. 따라서 유도 패턴도 이 두 조건, 즉 **가시성**과 **비용**을 맞추는 쪽으로 정리됩니다.

비용 쪽에서 가장 효과가 큰 것은 함수를 **작게** 유지하는 것입니다. 한두 줄짜리, 분기가 적은 함수는 펼쳐도 코드가 거의 늘지 않으므로 컴파일러가 망설이지 않습니다. 복잡한 로직은 작은 함수로 쪼개되, 자주 실행되는 빠른 경로만 작게 남기고 드문 오류 처리 경로는 별도 함수로 빼 두면 빠른 경로가 인라인 한도 안에 들어옵니다. 호출처가 **한 곳뿐인 정적 함수**도 유리합니다. 펼친 뒤 원본 정의를 지울 수 있어 코드 크기가 거의 늘지 않으므로 컴파일러가 적극적으로 인라인합니다.

가시성 쪽에서는 **정의가 호출부와 같은 TU에 보여야** 합니다. 템플릿과 inline 함수를 헤더에 정의하는 관례가 바로 이 조건을 만족시키는 방법입니다. 핫패스가 여러 `.cpp`에 흩어져 있어 헤더로 옮기기 어렵다면 <strong>LTO(Link Time Optimization)</strong>를 켭니다. LTO는 컴파일 단계에서 중간 표현(IR)을 오브젝트에 함께 넣어 두고 링크 시점에 프로그램 전체를 다시 최적화하므로, 다른 TU에 정의된 함수도 인라인 후보가 됩니다.

## 컴파일러는 무엇을 보고 인라인을 결정하는가

GCC·Clang의 인라이너는 호출 하나하나에 대해 "펼쳤을 때 늘어나는 명령 수"와 "얻는 이득"을 추정해 비교하는 비용 모델을 씁니다. 이득에는 호출·반환 명령과 인자 전달이 사라지는 것뿐 아니라, 인자가 상수일 때 본문의 분기가 접히는 효과까지 포함됩니다. GCC는 이 판단을 크게 두 단계로 나눕니다. 먼저 각 함수를 최적화하는 도중 아주 작은 호출만 펼치는 **early inlining**을 하고, 이후 프로그램의 호출 그래프를 보고 나머지 후보를 고르는 **IPA(프로시저 간 분석) 인라이닝**을 합니다. 아래 진단 출력에 나오는 `--param early-inlining-insns`, `--param max-inline-recursive-depth`가 각 판단에 쓰이는 한도 파라미터입니다.

호출부가 "드물게 실행된다"고 추정되면 기준이 더 엄격해집니다. 예를 들어 `main`에서 한 번만 호출되는 함수는 코드 크기를 늘리면서까지 펼칠 가치가 없다고 보고 거부되며, 이것이 아래 `-Winline` 경고에 나오는 "call is unlikely and code size would grow"의 의미입니다. 반대로 PGO(프로파일 기반 최적화)로 실제 실행 빈도를 알려 주면 컴파일러가 뜨거운 호출부를 알게 되어 그곳의 인라인을 더 공격적으로 수행합니다.

## 인라이닝 실패 원인과 진단 (Tr.03 연계)

인라인이 실패하는 원인은 크게 셋입니다. 첫째, **함수 크기·복잡도**가 한도를 넘거나 재귀라서 비용 모델이 거부하는 경우입니다. 둘째, **호출 시점에 타깃을 모르는 경우**입니다. 가상 함수 호출, 함수 포인터·`std::function`을 통한 호출은 컴파일러가 실제 대상을 증명하지 못하면 인라인할 수 없습니다. 다만 `final` 클래스, 같은 TU 안에서 상수로 전파된 함수 포인터, LTO로 클래스 계층 전체가 보이는 경우에는 컴파일러가 **devirtualization**(간접 호출을 직접 호출로 바꾸기)을 먼저 수행한 뒤 인라인할 수 있습니다([03장](/post/cpp-optimization/abstraction-cost/) 참고). 셋째, **정의가 보이지 않는 경우**입니다. 다른 TU에 있는 함수를 LTO 없이 호출하면 컴파일러는 본문이 없어 펼칠 수 없습니다.

GCC에서는 `-fopt-info-inline-optimized`로 인라인된 호출을, `-fopt-info-inline-missed`와 `-Winline`으로 인라인되지 못한 호출과 그 이유를 볼 수 있습니다. 아래는 위 `hot.cpp`를 GCC 14.2(x86-64, Compiler Explorer)로 컴파일한 실제 출력입니다. `add`가 `hot_path`로, `hot_path`가 `always_inline` 때문에 `main`으로 펼쳐졌음을 보여 줍니다.

```text
$ g++ -O2 -fopt-info-inline-optimized hot.cpp
hot.cpp:15:46: optimized:  Inlining int add(int, int)/15 into int hot_path(int)/16.
hot.cpp:18:16: optimized:   Inlining int hot_path(int)/16 into int main(int, char**)/17 (always_inline).
```

실패 쪽을 보려면 inline을 붙였지만 펼칠 수 없는 함수가 필요합니다. 아래 `big.cpp`의 `fib`는 재귀이고 `main`에서 한 번만 호출됩니다.

```cpp
#include <cstdio>

// inline을 붙였지만 재귀라 호출부에 완전히 펼칠 수 없다
inline unsigned long fib(unsigned n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main(int argc, char**) {
    std::printf("%lu\n", fib(static_cast<unsigned>(argc) + 30));
}
```

같은 GCC 14.2에서 `-Winline`과 `-fopt-info-inline-missed`를 함께 주면 다음 출력이 나옵니다(일부 발췌, 경고 아래의 소스 표시 줄은 생략). 재귀 호출은 재귀 깊이 한도 때문에, `main`의 호출은 "드문 호출인데 코드가 커진다"는 비용 판단 때문에 거부됐음을 이유까지 확인할 수 있습니다.

```text
$ g++ -O2 -Winline -fopt-info-inline-missed big.cpp
big.cpp:5:40: missed:   Not inlining: recursive call.
big.cpp:9:16: missed:   will not early inline: int main(int, char**)/16->long unsigned int fib(unsigned int)/15, growth 6 exceeds --param early-inlining-insns divided by number of calls
big.cpp:9:16: missed:   not inlinable: int main(int, char**)/16 -> long unsigned int fib(unsigned int)/15, call is unlikely and code size would grow
big.cpp:5:27: missed:    not inlining recursively: --param max-inline-recursive-depth exceeded.
big.cpp:4:22: warning: inlining failed in call to 'long unsigned int fib(unsigned int)': call is unlikely and code size would grow [-Winline]
```

인라인 성공은 생성된 어셈블리에서도 드러납니다. 아래 첫 블록은 `add`에 `__attribute__((noinline))`을 붙여 인라인을 막은 버전, 두 번째 블록은 원래 `hot.cpp`이며 둘 다 GCC 14.2 `-O2`가 만든 `main`의 발췌입니다(Intel 문법). 인라인을 막으면 `add`를 위한 인자 세팅과 `call`이 남지만, 인라인되면 `argc + 1` 계산이 `lea esi, [rdi+1]` 한 명령으로 접혀 `printf`의 인자로 바로 들어갑니다.

```text
; add를 noinline으로 막은 경우 (main 발췌)
        mov     esi, 1
        call    add(int, int)       ; 호출/반환 + 결과 레지스터 이동
        mov     edi, OFFSET FLAT:.LC0
        mov     esi, eax
        xor     eax, eax
        call    printf

; 인라인된 경우 (main 발췌)
        lea     esi, [rdi+1]        ; add(argc, 1)이 한 명령으로 접힘
        xor     eax, eax
        mov     edi, OFFSET FLAT:.LC0
        call    printf
```

이렇게 원인(크기·재귀·가상성·가시성)을 확인한 뒤에야 함수를 쪼갤지, 정의를 헤더로 옮길지, LTO를 켤지를 결정할 수 있습니다.

**구조화 진단 출력**: GCC 15(2025-04 릴리스)부터는 `-fdiagnostics-add-output=sarif`로 기존 텍스트 진단을 stderr에 유지하면서 **SARIF**(정적 분석 결과를 위한 표준 JSON 포맷) 출력을 파일로 함께 뽑을 수 있습니다. 이 출력에 담기는 것은 `-Winline` 같은 경고 진단이며, `-fopt-info` 계열 최적화 리포트는 별도의 덤프 출력이라 여기에 해당하지 않습니다. Clang 쪽은 `-Rpass=inline`·`-Rpass-missed=inline`과 `-fsave-optimization-record`(YAML/bitstream)가 최적화 리포트를 구조화된 형태로 내보내는 역할을 하며, 둘 다 CI 대시보드처럼 **자동화 파이프라인에 물릴 때** 텍스트 로그를 보완하는 용도로 씁니다.

## 실무 가이드

핫패스는 가능하면 작고 단순한 함수로 유지하고, 설계 단계에서부터 인라인 경계를 의식합니다. 다른 TU의 함수, 가상 호출, 함수 포인터는 모두 인라인을 막을 수 있는 경계이므로, 매우 자주 실행되는 루프 안에 이런 경계가 있다면 정의를 헤더로 옮기거나, 템플릿 매개변수로 호출 대상을 넘기거나, LTO를 켜는 것을 검토합니다.

인라인이 실제로 이득인지는 측정으로 확인합니다. 인라인 후에는 호출 오버헤드가 사라지고 상수 전파 같은 후속 최적화가 일어날 수 있지만, 반대로 펼친 코드가 명령어 캐시(I-cache)를 더 차지해 주변 코드의 캐시 미스가 늘 수도 있습니다. 그래서 인라인 전후로 마이크로벤치마크와 함께 바이너리 크기(`size` 명령)를 비교하고, 핫한 경로만 인라인하고 나머지는 호출로 두는 균형을 잡습니다. 드문 오류 경로에 GCC/Clang의 `__attribute__((noinline, cold))`를 붙여 빠른 경로 밖으로 밀어내는 것도 같은 균형을 맞추는 방법입니다.

## 판단 기준 (언제 쓰고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 핫한 작은 함수 | inline, 필요 시 always_inline | 큰 함수에 강제 인라인 |
| 여러 TU에서 호출 | 헤더 정의, LTO | TU 경계 넘어 인라인 기대만 |
| 인라인 실패 원인 | `-fopt-info-inline-missed` 등으로 확인 | 추측만 하고 변경 |

## 비판적 시각: 한계와 트레이드오프

인라인 힌트는 어디까지나 비용 모델에 들어가는 입력 하나일 뿐입니다. `inline`은 표준상 강제력이 없고, `always_inline`·`__forceinline`도 재귀처럼 펼칠 수 없는 경우를 바꾸지 못합니다. 더 큰 문제는 강제 인라인이 컴파일러의 판단을 덮어쓴다는 점입니다. 컴파일러가 "드문 호출이라 펼칠 가치가 없다"고 본 곳에 강제 인라인을 걸면, 거의 실행되지 않는 코드가 핫 루프 사이에 끼어들어 오히려 느려질 수 있습니다.

"많이 인라인할수록 빠르다"는 직관도 틀립니다. 인라인은 호출 비용을 없애는 대신 코드 크기를 키우고, 코드 크기는 I-cache와 분기 예측기 자원을 소비합니다. 핫 루프가 I-cache에 들어가던 상태에서 과도한 인라인으로 넘치게 되면 호출 몇 개를 없앤 이득보다 캐시 미스 비용이 커집니다. 핫 경로와 차가운 경로를 구분해 핫 경로만 펼치는 것이 기본 원칙이며, 그 구분은 프로파일러가 알려 줍니다.

## 평가 기준 (학습 성과 목표)

이 장을 마치면 인라이닝을 "키워드를 붙이는 일"이 아니라 "컴파일러의 비용 모델에 맞는 코드를 쓰고 결과를 진단하는 일"로 다룰 수 있어야 합니다.

- **inline**과 **__forceinline**/always_inline의 차이(힌트 vs 강한 힌트), inline의 ODR 의미, 컴파일러가 인라인을 거부하는 경우를 설명할 수 있다.
- **작은 함수·단일 호출·헤더 정의·LTO**가 인라이닝에 유리한 이유를 가시성과 비용 두 축으로 설명하고, 핫패스 설계에 적용할 수 있다.
- 인라이닝 실패 원인(크기·재귀·가상·함수 포인터·TU 경계)을 `-Winline`·`-fopt-info-inline-missed` 출력에서 읽어 내고, devirtualization이 가능한 경우를 구분할 수 있다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| inline | 표준상 힌트 + ODR 예외; always_inline은 강한 힌트 |
| 유도 패턴 | 작은 함수, 헤더 정의, LTO |
| 실패 원인 | 크기·재귀·가상·함수 포인터·TU 경계 → Tr.03 진단 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **ODR** | One Definition Rule; inline 함수는 여러 TU에 정의 가능, 하나로 합쳐짐 |
| **LTO** | Link Time Optimization; 링크 시점에 인라인 등 최적화 |
| **always_inline** | GCC/Clang의 강한 인라인 힌트; MSVC의 __forceinline에 대응 |
| **devirtualization** | 간접(가상·함수 포인터) 호출의 대상을 증명해 직접 호출로 바꾸는 최적화 |

### 자주 묻는 질문 (FAQ)

**Q: LTO를 켰는데도 다른 TU의 함수가 인라인되지 않습니다. 왜 그런가요?**  
A: LTO는 가시성 문제만 해결합니다. 비용 모델의 판단은 그대로이므로 함수가 크거나 호출부가 드물다고 추정되면 여전히 거부됩니다. 또 공유 라이브러리에서 기본 가시성으로 내보낸 함수는 런타임에 다른 정의로 대체될 수 있어(semantic interposition) 인라인이 막힐 수 있습니다. 이 경계는 [18장](/post/cpp-optimization/abi-link-boundaries-extreme-cpp-performance/)에서 다룹니다.

### 적용 체크리스트 (실무용)

- [ ] 핫패스는 작고 단순한 함수로 유지했는가? — 크기 한도 안에 들어야 비용 모델이 펼친다.
- [ ] 인라인 전/후 벤치마크와 바이너리 크기를 함께 비교했는가? — I-cache 손해가 호출 비용 절감보다 클 수 있다.
- [ ] 인라인 실패 원인을 `-fopt-info-inline-missed`·`-Winline`으로 확인했는가? — 원인에 따라 처방(쪼개기·헤더 이동·LTO)이 다르다.

### 추가 읽기 및 관련 챕터

- **챕터 11 (예외)**: noexcept가 인라이닝에 미치는 영향.
- **챕터 13 (variant/optional/expected)**: visit 디스패치와 인라인.
- **Tr.03**: -Winline, -fopt-info-inline, 최적화 리포트.
- [cppreference: inline specifier](https://en.cppreference.com/w/cpp/language/inline) — inline이 ODR과 인라인 힌트 두 역할을 동시에 갖는 정확한 의미를 다루는 1차 출처.
- [C++ 작업 초안 [dcl.inline]](https://eel.is/c++draft/dcl.inline) — 위 인용문의 출처인 표준 조항.
- [GCC 15 Release Series Changes](https://gcc.gnu.org/gcc-15/changes.html) — `-fdiagnostics-add-output=sarif` 등 GCC 15의 진단 출력 변경 사항 1차 문서.
- [LLVM Remarks (Optimization Remarks)](https://llvm.org/docs/Remarks.html) — Clang/LLVM의 `-Rpass`·`-fsave-optimization-record` 구조화 진단 문서.

---

## 다음 장에서는

**이전 장**: [예외 처리 심화](/post/cpp-optimization/exception-deep-dive/) (챕터 11)

**std::variant/optional/expected**를 다룹니다. 타입 안전 유니온·옵셔널·에러 전달 타입의 성능 특성과 오버헤드, 예외 대안으로서의 expected를 정리합니다. → [std::variant/optional/expected](/post/cpp-optimization/variant-optional-expected/) (챕터 13)
