---
collection_order: 5
date: 2026-03-11
lastmod: 2026-10-20
draft: false
image: wordcloud.png
title: "[Compiler 03] 인라이닝 실패 진단"
slug: inlining-diagnostics
description: "인라이닝이 실패하는 원인(가시성, 심볼 교체 가능성·옵션 불일치, 코드 크기 한도)을 GCC -fopt-info-inline-missed·Clang -Rpass-missed=inline의 실제 출력으로 진단하고, LTO·공유 라이브러리 빌드에서 확인하는 방법과 대처를 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Assembly(어셈블리)
  - Cache
  - Latency
  - Linux(리눅스)
  - Low-Level(로우레벨)
  - Debugging(디버깅)
  - Comparison(비교)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - Open-Source(오픈소스)
  - Standard(표준)
  - 실습
  - GCC
  - Clang
  - LLVM
  - LTO
  - Inlining
---

<strong>인라이닝(inlining)</strong>은 함수 호출을 호출부에 함수 본문을 펼쳐 넣는 최적화입니다. 핫 루프 안에 호출이 남으면 매 반복마다 인자 레지스터 준비, `call`/`ret`, 필요하면 스택 프레임 설정이라는 고정 비용이 붙고, 이 비용은 함수 본체가 작을수록 상대적으로 커집니다. 그러나 더 큰 손실은 호출 자체보다 **호출 경계가 다른 최적화를 막는다**는 데 있습니다. 본문이 펼쳐져야 상수 전파, 루프 불변식 이동, 벡터화가 호출자와 피호출자를 하나의 코드로 보고 동작할 수 있기 때문입니다.

인라이닝은 컴파일러가 자동으로 결정하는 것이 원칙이지만, 조건이 맞지 않으면 호출이 그대로 남습니다. 이 챕터에서는 인라인되지 않는 원인을 컴파일러 관점에서 분류하고, GCC·Clang의 리포트와 어셈블리로 그 결정을 직접 확인하는 방법을 다룹니다. 본문의 리포트 출력은 모두 아래 예제를 2026년 10월 [Compiler Explorer](https://godbolt.org)에서 x86-64 gcc 14.2, x86-64 clang 19.1.0으로 컴파일해 얻은 실제 출력입니다.

## 인라이닝 실패의 주요 원인

컴파일러가 호출을 인라인하지 않는 이유는 크게 세 가지로 나눌 수 있고, 리포트 메시지도 대체로 이 셋 중 하나로 읽힙니다.

### 가시성(다른 번역 단위)

일반 컴파일 모델에서는 **각 TU가 독립적으로 컴파일**됩니다. 호출하는 TU에 함수의 선언만 있고 본문이 없으면, 컴파일러는 다른 오브젝트 파일에 있을 구현을 볼 수 없으므로 인라인할 수 없습니다. GCC 리포트는 이 경우를 "function body not available"로 표시합니다. 헤더에 정의된 `inline` 함수나 템플릿은 호출하는 TU에서 본문이 보이므로 인라인 후보가 됩니다. 따라서 핫 경로의 작은 함수는 헤더에 두거나 같은 `.cc`에 두거나, 링크 시점에 모든 TU를 함께 보는 LTO를 켜야 크로스-TU 인라이닝이 가능해집니다.

### 심볼 교체 가능성과 ABI 경계

본문이 보여도 인라인이 금지되는 경우가 있습니다. ELF 공유 라이브러리에서는 export된 심볼을 동적 링커가 다른 구현으로 바꿔 끼울 수 있는데(symbol interposition), [GCC Optimize Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)의 `-fsemantic-interposition` 설명대로 이런 심볼에 대해서는 컴파일러가 인라이닝과 프로시저 간 전파를 하지 못합니다. 그래서 `-fPIC`로 빌드한 라이브러리 안에서는 같은 파일에 정의된 함수끼리도 호출이 남을 수 있습니다. 해결책은 해당 심볼을 export하지 않거나(`-fvisibility=hidden`, `static`, 익명 네임스페이스), 교체가 일어나도 의미가 같다고 컴파일러에 약속하는 `-fno-semantic-interposition`을 쓰는 것입니다.

다른 하나는 컴파일 옵션 불일치입니다. 호출자와 피호출자의 `target` 속성(예: AVX2 사용 여부)이 다르면, 피호출자의 명령어를 호출자가 실행할 수 있다고 보장할 수 없으므로 GCC·Clang 모두 인라인을 거부합니다. 이 불일치는 [함수 멀티버저닝](/post/compiler-optimization/function-multiversioning-cpu/)이나 intrinsic을 쓸 때 자주 만나며, `always_inline` 함수에서 일어나면 컴파일 오류가 됩니다.

### 코드 크기 한도

인라이닝을 무한히 하면 코드 크기가 커져 I-cache 압박과 컴파일 시간이 늘어나므로, 컴파일러는 함수 크기·호출 빈도·루프 안 여부 같은 요소로 비용을 추정하고 한도를 넘는 호출은 남겨 둡니다. 한도는 컴파일러마다 다르게 정의됩니다. GCC는 [GCC 14.2 매뉴얼](https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Optimize-Options.html)의 `--param` 설명대로 `inline`으로 선언한 함수와 클래스 안에 정의한 메서드에는 `max-inline-insns-single`, 그 밖의 함수에는 더 제한적인 `max-inline-insns-auto`라는 명령어 수 한도를 쓰고, Clang은 호출 지점마다 비용(cost)을 계산해 임계값(threshold)과 비교합니다. 같은 함수가 한 컴파일러에서는 인라인되고 다른 컴파일러에서는 호출로 남는 일이 흔한 이유가 여기에 있습니다.

## 진단용 예제

아래 파일 하나에 세 가지 경우를 모두 넣었습니다. `add`는 작아서 인라인될 것으로 기대되는 함수, `big_func`은 루프 네 개가 들어 있어 크기 한도에 걸릴 수 있는 함수, `external`은 선언만 있고 본문이 다른 TU에 있는 함수입니다. `-S`나 리포트 확인은 이 파일 하나로 되고, 실행 파일을 만들려면 `external`의 정의를 담은 두 번째 파일을 함께 링크합니다.

```cpp
// foo.cc: 인라이닝 성공·실패를 한 파일에서 관찰하는 예제
#include <cstdio>

int external(int x);                  // 다른 TU(ext.cc)에 정의: 본문이 안 보임

static int add(int a, int b) { return a + b; }   // 작은 함수

int big_func(int x) {                 // 루프가 여러 개인 큰 함수
    int s = 0;
    for (int i = 0; i < x; ++i) s += (i * i) ^ (s >> 3);
    for (int i = 0; i < x; ++i) s -= (i * 7) | (s << 2);
    for (int i = 0; i < x; ++i) s += (s % 13) * i;
    for (int i = 0; i < x; ++i) s ^= (s / 7) + i;
    return s;
}

int compute(int n) {
    int r = 0;
    for (int i = 0; i < n; ++i) {
        r = add(r, i);                // 인라인 기대
        r += big_func(i) + big_func(r & 15);  // 크기 때문에 호출로 남을 수 있음
        r += external(i);             // 본문이 없어 인라인 불가
    }
    return r;
}

int main() { std::printf("%d\n", compute(100)); }
```

```cpp
// ext.cc
int external(int x) { return x * 3 + 1; }
```

```bash
g++ -O2 foo.cc ext.cc -o foo && ./foo
```

## 인라이닝 리포트 확인 방법

### GCC: -fopt-info-inline-missed / -all

GCC의 `-fopt-info`는 옵션 이름 뒤에 메시지 종류와 최적화 그룹을 붙여 범위를 정합니다. 주의할 점은 메시지 종류를 생략했을 때의 기본값입니다. [GCC Developer Options](https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html) 문서는 생략 시 기본값이 `optimized-optall`, 즉 **성공한 최적화만** 출력한다고 설명합니다. 따라서 `-fopt-info-inline`만 주면 "무엇이 인라인됐는지"만 나오고, "왜 안 됐는지"를 보려면 `-fopt-info-inline-missed`(실패만)나 `-fopt-info-inline-all`(성공·실패·검토 과정 전부)을 써야 합니다.

```bash
# 실패한 인라이닝과 이유만 (stderr로 출력)
g++ -O2 -c foo.cc -fopt-info-inline-missed
# 성공한 인라이닝만
g++ -O2 -c foo.cc -fopt-info-inline-optimized
```

`foo.cc`에 `-fopt-info-inline-missed`를 적용한 실제 출력 중 `compute` 관련 줄은 다음과 같습니다(`main`에 대한 줄은 생략).

```text
<source>:21:36: missed:   will not early inline: int compute(int)/17->int big_func(int)/16, call is cold and code would grow at least by 23
<source>:22:22: missed:   not inlinable: int compute(int)/17 -> int external(int)/19, function body not available
<source>:21:36: missed:   not inlinable: int compute(int)/17 -> int big_func(int)/16, --param max-inline-insns-auto limit reached
```

세 원인이 그대로 드러납니다. `external`은 "function body not available"(가시성), `big_func`은 "max-inline-insns-auto limit reached"(크기 한도)로 거부됐습니다. "will not early inline"은 GCC가 최적화 초반에 수행하는 early inliner의 판단이고, 최종 결정은 뒤의 "not inlinable" 줄입니다. `-fopt-info-inline-optimized`로 바꾸면 성공한 한 줄만 나옵니다.

```text
<source>:20:16: optimized:  Inlining int add(int, int)/15 into int compute(int)/17.
```

GCC 14.2의 메시지는 `optimized:`/`missed:`/`note:` 접두사로 종류를 구분하므로, 출력을 걸러 낼 때는 `grep -E "optimized:|missed:"`처럼 접두사로 거르는 편이 정확합니다.

### Clang: -Rpass=inline / -Rpass-missed=inline

Clang은 최적화 remark를 pass 이름으로 고릅니다. [Clang User's Manual](https://clang.llvm.org/docs/UsersManual.html)의 최적화 리포트 절대로 `-Rpass=inline`은 **성공한** 인라이닝만, `-Rpass-missed=inline`은 인라인하지 않기로 한 호출만, `-Rpass-analysis=inline`은 결정의 근거를 출력합니다. 성공과 실패를 함께 보려면 두 옵션을 같이 줍니다.

```bash
clang++ -O2 -c foo.cc -Rpass=inline -Rpass-missed=inline
```

같은 `foo.cc`에 대한 Clang 19.1.0의 실제 출력입니다.

```text
<source>:20:13: remark: '_ZL3addii' inlined into '_Z7computei' with (cost=-15035, threshold=337) at callsite _Z7computei:3:13; [-Rpass=inline]
<source>:21:14: remark: '_Z8big_funci' inlined into '_Z7computei' with (cost=120, threshold=225) at callsite _Z7computei:4:14; [-Rpass=inline]
<source>:21:28: remark: '_Z8big_funci' inlined into '_Z7computei' with (cost=120, threshold=225) at callsite _Z7computei:4:28; [-Rpass=inline]
<source>:27:34: remark: '_Z7computei' not inlined into 'main' because too costly to inline (cost=320, threshold=225) [-Rpass-missed=inline]
```

여기서 두 컴파일러의 판단이 갈립니다. GCC는 `big_func`을 크기 한도로 거부했지만, Clang은 비용 120이 임계값 225보다 작다고 보고 두 호출 모두 인라인했습니다. 반대로 `compute`를 `main`에 넣는 것은 Clang도 비용 320으로 거부했습니다. `add`의 비용이 크게 음수인 것은 인라인하면 호출 오버헤드가 사라지고 연산이 단순해져 오히려 코드가 줄어든다고 평가했다는 뜻입니다. `external`에 대해서는 본문이 없어 인라인 후보 자체가 되지 않으므로 remark가 나오지 않습니다.

### 어셈블리로 최종 확인

리포트는 결정 과정을 보여 주고, 최종 결과는 어셈블리가 보여 줍니다. [챕터 06](/post/compiler-optimization/code-generation-analysis-assembly/)의 방법대로 `-S`로 어셈블리를 뽑아 호출 지점에 `call`이 남았는지 확인합니다. GCC 14.2 `-O2`로 컴파일한 `compute`에는 리포트와 일치하게 다음 호출이 남아 있고, `add`에 대한 호출은 없습니다.

```text
compute(int):
        ...
        call    big_func(int)
        call    big_func(int)
        call    external(int)
```

## 공유 라이브러리 경계를 리포트로 확인하기

앞에서 설명한 심볼 교체 가능성도 리포트로 직접 볼 수 있습니다. 아래 두 함수는 같은 파일에 있으므로 일반 빌드에서는 `sq`가 `use`에 인라인됩니다.

```cpp
// interp.cc
int sq(int x) { return x * x; }       // 공유 라이브러리에서 export되는 함수
int use(int y) { return sq(y) + 1; }
```

GCC 14.2에서 `-O2 -fPIC -fopt-info-inline-missed`로 컴파일하면 `use` 안에 `call sq(int)@PLT`가 남고, 리포트는 이유를 다음과 같이 밝힙니다.

```text
<source>:2:27: missed:   not inlinable: int use(int)/1 -> int sq(int)/0, function body can be overwritten at link time
```

같은 명령에 `-fno-semantic-interposition`이나 `-fvisibility=hidden`을 더하면 호출이 사라지고 인라인됩니다. 같은 조건에서 Clang 19.1.0은 `-fPIC`만으로도 `sq`를 인라인했습니다. 두 컴파일러의 기본 가정이 다르다는 점을 알아 두면, 같은 라이브러리를 GCC와 Clang으로 빌드했을 때의 성능 차이 하나를 설명할 수 있습니다.

## LTO 빌드에서 확인하기

LTO를 켜면 인라이닝 결정 일부가 링크 시점으로 옮겨집니다. 그래서 단일 TU의 `-S` 출력에서는 `external` 호출이 남아 있어도, 최종 바이너리에서는 인라인되어 있을 수 있습니다. 이 경우 확인 대상은 컴파일 단계가 아니라 링크 단계입니다. GCC에서는 `-flto`로 빌드할 때 링크 명령에도 `-O2 -flto`와 `-fopt-info-inline-missed`를 함께 넘겨 링크 시점 최적화 단계의 리포트를 받고, Clang에서는 최종 실행 파일을 `objdump -d`로 디스어셈블해 `call` 유무를 확인하는 방법이 가장 확실합니다. 이름이 비슷한 GCC `-flto-report`는 Developer Options 문서에 따르면 링크 타임 옵티마이저 내부 동작을 GCC 개발자용으로 출력하는 옵션이라, 인라이닝 결정을 읽는 용도로는 맞지 않습니다.

## inline, always_inline, LTO가 결정에 미치는 영향

C++의 `inline` 키워드는 "반드시 펼쳐라"라는 명령이 아니라, 여러 TU에 같은 정의가 있어도 된다는 링크 규칙(ODR 예외)에 가깝습니다. 그래도 헤더에 정의를 둘 수 있게 해 주므로 결과적으로 모든 TU에서 본문이 보이고, 가시성 문제를 푸는 가장 흔한 수단이 됩니다. 앞서 본 것처럼 GCC는 `inline` 선언 여부에 따라 다른 크기 한도를 적용하므로, 키워드가 휴리스틱에도 영향을 줍니다.

`__attribute__((always_inline))`은 힌트가 아니라 요구입니다. [GCC 함수 속성 문서](https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html)는 이 속성이 붙은 `inline` 함수를 다른 제약과 무관하게 인라인하며, 인라인하지 못하면 오류로 진단한다고 설명합니다. 따라서 `target` 옵션이 다른 함수에 `always_inline` 함수를 부르면 경고가 아니라 "inlining failed in call to 'always_inline'" 같은 컴파일 오류를 만납니다. 크기 휴리스틱도 무시하므로, 측정으로 이득이 확인된 작은 함수에만 쓰는 것이 안전합니다.

LTO는 링크 시점에 모든 TU의 중간 표현을 함께 보므로 가시성 제약을 없앱니다. 다른 `.cc`에만 정의된 작은 함수가 LTO에서 비로소 인라인되는 경우가 많습니다. 다만 LTO도 크기 한도, 심볼 교체 가능성, `target` 불일치는 그대로 적용하므로 "LTO를 켰으니 인라인될 것"이라는 가정은 리포트로 확인해야 합니다.

## 점검 순서

인라이닝이 기대대로 되지 않을 때는 원인을 좁히는 순서가 중요합니다. 먼저 호출 지점에서 피호출 함수의 본문이 보이는지 확인합니다. 선언만 보인다면 다른 원인을 찾을 필요 없이 헤더나 같은 TU로 옮기거나 LTO를 켜는 것이 답입니다. 본문이 보이는데도 호출이 남는다면 GCC `-fopt-info-inline-missed`나 Clang `-Rpass-missed=inline`으로 거부 이유를 읽습니다. 이유가 크기 한도라면 함수를 핫 경로와 콜드 경로로 쪼개 핫 부분만 작게 만들고, 심볼 교체 가능성이라면 visibility를 조정하고, `target` 불일치라면 옵션을 맞춥니다. 마지막으로 `-S` 또는 최종 바이너리 디스어셈블리에서 `call`이 사라졌는지 보고, 실제 실행 시간이 줄었는지 측정합니다.

이 챕터는 "왜 인라인되지 않았는지"를 진단하는 쪽에 초점을 둡니다. 작은 함수를 헤더에 두기, 템플릿으로 구현을 노출하기, `final`로 devirtualization을 유도하기처럼 인라이닝을 끌어내는 코드 구조는 Low-latency C++ 언어 최적화 트랙(Tr.02)에서 다루므로, 구조를 바꾼 뒤 이 챕터의 리포트로 결과를 확인하는 식으로 두 트랙을 함께 쓰면 됩니다.

## 한눈에 보기: 인라이닝 실패 원인과 진단

| 원인 | GCC 리포트 표현 | 대처 |
|------|----------------|------|
| **가시성** | function body not available | 헤더·같은 TU 배치, LTO |
| **심볼 교체 가능성** | function body can be overwritten at link time | `-fvisibility=hidden`, `static`, `-fno-semantic-interposition` |
| **옵션 불일치** | target specific option mismatch | 호출자·피호출자의 `target` 옵션 통일 |
| **코드 크기** | `--param max-inline-insns-auto`/`-single` limit reached | 핫·콜드 분리, 측정 후 제한적 `always_inline` |

## 판단 기준: 언제 진단할지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 핫 경로에 호출 비용 의심 | `-fopt-info-inline-missed`/`-Rpass-missed=inline`과 어셈블리 확인 | 추측만으로 코드 구조 변경 |
| LTO를 켠 뒤에도 느림 | 링크 단계 리포트·최종 바이너리 디스어셈블리 확인 | 컴파일 단계 `-S`만 보고 판단 |
| 공유 라이브러리 내부 호출 | visibility 설정과 interposition 리포트 확인 | 모든 심볼을 기본 visibility로 export |

## 자주 하는 실수

- **`-fopt-info-inline`만으로 실패 이유를 찾으려 하기**: 메시지 종류를 생략하면 성공한 최적화만 출력된다. 실패 이유는 `-missed`나 `-all`을 붙여야 나온다.
- **`-Rpass=inline`이 실패도 보여 준다고 생각하기**: `-Rpass`는 성공한 변환만 보고한다. 거부된 호출은 `-Rpass-missed=inline`으로 따로 요청해야 한다.
- **`always_inline`을 여러 함수에 거는 것**: 크기 휴리스틱을 무시하므로 코드가 불어나고, 옵션이 다른 호출자에서는 컴파일 오류가 된다. 측정으로 이득이 확인된 작은 함수에만 쓴다.

## 학습 성과 목표

- 인라이닝 실패를 가시성, 심볼 교체 가능성·옵션 불일치, 코드 크기 한도로 분류하고 각각의 대처를 설명할 수 있다.
- GCC `-fopt-info-inline-missed`/`-all`과 Clang `-Rpass=inline`/`-Rpass-missed=inline`의 출력을 읽고, 어셈블리의 `call`로 최종 결과를 확인할 수 있다.
- LTO와 공유 라이브러리 빌드에서 인라이닝을 어느 단계에서 확인해야 하는지 판단할 수 있다.

## 비판적 시각: 한계와 트레이드오프

인라이닝은 많을수록 좋은 것이 아닙니다. 과도한 인라이닝은 코드 크기와 컴파일 시간을 늘리고 I-cache를 압박하며, 위 예제처럼 GCC와 Clang이 같은 함수를 다르게 판단한다는 것은 "정답 임계값"이 존재하지 않는다는 뜻이기도 합니다. 리포트는 컴파일러가 왜 그렇게 결정했는지를 알려 줄 뿐, 그 결정이 실행 시간에 이득인지는 알려 주지 않습니다. 따라서 `always_inline`이나 `--param` 조정으로 결정을 뒤집기 전에, 해당 호출이 프로파일상 실제로 핫한지와 바꾼 뒤 실행 시간이 줄었는지를 측정으로 확인해야 합니다. 리포트 메시지의 문구 또한 컴파일러 버전마다 바뀌므로, 문자열 매칭에 의존하는 자동화는 버전을 고정해 두어야 합니다.

## 다음 장에서는

**어셈블리 레벨** 코드 생성 분석, -S·objdump·Godbolt 사용, 함수 경계·호출 규약·hot 함수 형태 해석을 다룹니다.

→ [코드 생성 분석](/post/compiler-optimization/code-generation-analysis-assembly/) (챕터 06)
