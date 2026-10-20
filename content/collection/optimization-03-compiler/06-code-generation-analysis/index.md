---
collection_order: 6
date: 2026-03-11
lastmod: 2026-10-20
draft: false
image: wordcloud.png
title: "[Compiler 03] 어셈블리 레벨 코드 생성 분석"
slug: code-generation-analysis-assembly
description: "-S·objdump·Compiler Explorer로 생성 코드를 확인하고, 호출 규약과 인라인 전후 차이, ps/ss 접미사·레지스터 폭으로 벡터화를 판별하는 규칙, GCC·Clang 벡터화 리포트와 언롤링 확인법을 GCC 14.2·Clang 19 실제 출력으로 다룹니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Assembly(어셈블리)
  - SIMD(단일명령다중데이터)
  - Vectorization(벡터화)
  - Floating-Point(부동소수점)
  - Low-Level(로우레벨)
  - Hardware(하드웨어)
  - Linux(리눅스)
  - Windows(윈도우)
  - Profiling(프로파일링)
  - Debugging(디버깅)
  - Comparison(비교)
  - Pitfalls(함정)
  - Best-Practices
  - Guide(가이드)
  - Reference(참고)
  - Tutorial(튜토리얼)
  - Advanced
  - Deep-Dive
  - 실습
  - GCC
  - Clang
  - LLVM
  - x86-64
---

생성된 어셈블리를 보면 인라이닝·벡터화·호출 비용을 추측이 아니라 사실로 확인할 수 있습니다. 이 챕터에서는 산출물을 뽑는 도구, 어셈블리에서 인라인 여부와 벡터화 여부를 판별하는 규칙, 그리고 컴파일러에게 벡터화 결과를 직접 묻는 리포트 옵션을 다룹니다. 본문의 어셈블리는 모두 2026년 10월 [Compiler Explorer](https://godbolt.org)에서 x86-64 gcc 14.2와 x86-64 clang 19.1.0으로 얻은 실제 출력이며, 읽기 쉽도록 Intel 문법으로 표시했습니다.

> "This is an optimization manual for advanced assembly language programmers and compiler makers." — Agner Fog, [Optimizing subroutines in assembly language](https://www.agner.org/optimize/)

## 산출물 확인 도구

컴파일 산출물을 보는 도구는 각기 다른 시점의 결과를 보여 주므로, 무엇을 확인하려는지에 따라 골라야 합니다.

`-S`는 컴파일러가 오브젝트 대신 어셈블리 파일(`.s`)을 쓰게 합니다. `g++ -S -O2 -masm=intel foo.cc`처럼 쓰면 소스 한 파일의 결과를 바로 얻을 수 있고, 같은 플래그로 빌드한 실제 코드와 동일한 최적화가 적용됩니다. GCC의 `-fverbose-asm`을 함께 주면 [GCC 문서](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html)의 설명대로 생성 코드에 주석 정보가 붙어, 어떤 명령이 어떤 변수·소스 줄에서 왔는지 따라가기 쉬워집니다. 다만 `-S`는 **번역 단위(TU) 하나**의 결과라서, 링크 시점에 일어나는 최적화는 보이지 않습니다.

[`objdump -d`](https://sourceware.org/binutils/docs/binutils/objdump.html)는 이미 만들어진 오브젝트나 실행 파일을 디스어셈블합니다. `-M intel`로 Intel 문법을 고를 수 있고, `-C`로 C++ 심볼 이름을 풀어 줍니다. 최종 바이너리를 보기 때문에 LTO처럼 링크 시점에 코드를 바꾸는 최적화의 결과를 확인할 수 있는 유일한 방법이기도 합니다. LTO를 켠 빌드에서 단일 `.cc`의 `-S` 출력만 보면 다른 TU 함수가 인라인되지 않은 것처럼 보이므로, 그때는 반드시 최종 바이너리를 봐야 합니다.

[Compiler Explorer](https://godbolt.org)는 브라우저에서 컴파일러와 플래그를 바꿔 가며 소스와 어셈블리를 나란히 보여 줍니다. 소스 줄을 클릭하면 그 줄이 만든 명령 구간이 강조되고, "Add new compiler"로 GCC와 Clang 창을 함께 띄워 같은 소스의 결과를 비교할 수 있습니다. 로컬 환경 없이 "이 패턴이 벡터화되는가"를 몇 초 안에 확인할 수 있어, 최소 재현 소스를 다듬는 단계에 특히 유용합니다.

## 인라인 전·후 비교

인라이닝이 어셈블리에 어떻게 나타나는지 가장 작은 예로 확인합니다.

```cpp
// inline_demo.cc
int add(int a, int b) {
    return a + b;
}

int compute(int x) {
    return add(x, 42) * 2;
}
```

`-O0`에서는 최적화를 하지 않으므로 인라이닝도 일어나지 않습니다. GCC 14.2 `-O0`의 `compute`는 인자를 스택 슬롯에 저장했다가 다시 읽고, `add`를 `call`로 부릅니다.

```text
compute(int):
        push    rbp
        mov     rbp, rsp
        sub     rsp, 8
        mov     DWORD PTR [rbp-4], edi
        mov     eax, DWORD PTR [rbp-4]
        mov     esi, 42
        mov     edi, eax
        call    add(int, int)
        add     eax, eax
        leave
        ret
```

`call add(int, int)`가 함수 경계가 남아 있다는 신호입니다. Compiler Explorer는 이름을 풀어서 보여 주지만, `objdump -d`를 `-C` 없이 쓰면 같은 자리에 맹글링된 이름 `_Z3addii`가 나옵니다. `-O2`에서는 결과가 완전히 달라집니다.

```text
compute(int):
        lea     eax, [rdi+84+rdi]
        ret
```

`add`가 인라인되자 컴파일러는 `(x + 42) * 2`를 `2x + 84`로 다시 쓰고, 주소 계산 명령 `lea` 하나로 계산했습니다. 이 예가 보여 주는 핵심은 인라이닝으로 `call`/`ret` 비용이 사라진 것보다, **함수 경계가 사라져야 상수 접기와 식 재구성이 가능해졌다는 점**입니다. 핫 경로의 어셈블리에서 기대한 계산이 보이지 않고 `call`이 남아 있다면, 인라이닝 실패가 다른 최적화까지 막고 있을 가능성이 큽니다. 인라이닝 실패의 원인을 진단하는 방법은 [챕터 05](/post/compiler-optimization/inlining-diagnostics/)에서 다룹니다.

## 함수 경계와 호출 규약

<strong>호출 규약(calling convention)</strong>은 인자를 어느 레지스터나 스택 위치로 넘기는지, 어떤 레지스터를 호출된 쪽이 보존해야 하는지, 스택을 어떻게 정렬하는지를 정합니다. Linux 등이 쓰는 [System V x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI)는 정수·포인터 인자를 `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9` 순으로, 부동소수점 인자를 `xmm0`부터 넘깁니다. 아래 `scale` 함수의 실제 출력에서 `dst`가 `rdi`, `src`가 `rsi`, `factor`가 `xmm0`, `n`이 `edx`로 들어오는 것이 바로 이 규칙입니다. Windows x64는 [MS Learn의 x64 호출 규약](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention)대로 앞의 정수 인자 네 개를 `RCX`, `RDX`, `R8`, `R9`로 넘기고, 호출자가 레지스터 인자 네 개를 저장할 shadow store를 항상 스택에 확보해야 합니다.

이 규칙을 알면 어셈블리를 읽을 때 "어느 레지스터가 어느 변수인가"를 바로 짝지을 수 있고, 호출 경계의 비용도 구체적으로 보입니다. 호출 전후로 caller-saved 레지스터를 스택에 저장했다가 복원하는 `push`/`pop`이나 `mov [rsp+...]`가 많이 보이면, 레지스터 압박이나 호출 경계가 비용을 만들고 있다는 뜻입니다. 인라인되면 이 저장·복원이 줄거나 사라지고, 위의 `compute`처럼 호출자와 피호출자가 하나의 식으로 합쳐질 수 있습니다. 반대로 `call`이 있어도 그 함수가 프로파일상 핫하지 않다면 비용은 무시할 수준이므로, 어셈블리는 항상 프로파일로 찾은 핫 경로에 대해 읽어야 합니다.

## 벡터화 판별: 접미사와 레지스터 폭

루프가 벡터화됐는지 확인할 때 가장 흔한 오해는 "`v`로 시작하는 명령이면 SIMD"라는 생각입니다. AVX가 켜지면 스칼라 부동소수점 연산도 VEX 인코딩을 쓰므로 `vmulss`처럼 `v`가 붙고, x86-64의 스칼라 float·double 연산은 항상 `xmm` 레지스터를 씁니다. 따라서 `v` 접두사나 `xmm` 레지스터만으로는 아무것도 판단할 수 없습니다. 판별 기준은 두 가지입니다.

첫째는 **명령 접미사**입니다. `ps`(packed single)·`pd`(packed double)는 레지스터의 모든 레인을 처리하는 벡터 연산이고, `ss`(scalar single)·`sd`(scalar double)는 최하위 레인 하나만 처리하는 스칼라 연산입니다. 정수 SIMD는 `vpaddd`, `vpmulld`처럼 `p` 접두가 붙은 형태로 나옵니다. 둘째는 **레지스터 폭과 주소 증가량**입니다. packed 연산이 `ymm`(256비트, float 8개)이나 `zmm`(512비트, float 16개)을 쓰고 루프 인덱스가 32바이트·64바이트씩 증가하면 넓은 벡터로 처리하고 있다는 뜻입니다. packed 연산이 `xmm`을 쓰면 128비트(float 4개) 벡터입니다.

다음 루프로 확인해 보겠습니다.

```cpp
// vectorize_demo.cc: 벡터화 여부를 관찰하기 위한 루프
void scale(float* dst, const float* src, float factor, int n) {
    for (int i = 0; i < n; ++i)
        dst[i] = src[i] * factor;
}
```

GCC 14.2 `-O2 -mavx2`의 출력은 **스칼라 루프**입니다. `vmulss`로 float 하나를 곱하고 `vmovss`로 하나를 저장하며, 주소는 4바이트씩 증가합니다.

```text
.L3:
        vmulss  xmm1, xmm0, DWORD PTR [rsi+rax]
        vmovss  DWORD PTR [rdi+rax], xmm1
        add     rax, 4
        cmp     rax, rdx
        jne     .L3
```

같은 소스를 GCC 14.2 `-O3 -mavx2`로 컴파일하면 벡터 본체가 생깁니다. `vbroadcastss`로 `factor`를 8개 레인에 복사한 뒤 `vmulps ymm`으로 8개를 한 번에 곱하고, 주소는 32바이트씩 증가합니다.

```text
        vbroadcastss    ymm2, xmm0
        ...
.L5:
        vmulps  ymm1, ymm2, YMMWORD PTR [rsi+rax]
        vmovups YMMWORD PTR [rcx+rax], ymm1
        add     rax, 32
        cmp     rdi, rax
        jne     .L5
```

Clang 19.1.0은 `-O2 -mavx2`에서 이미 이 루프를 벡터화하며, 한 반복에 `vmulps ymm` 네 개를 펼쳐 32개 float를 처리합니다. 두 컴파일러가 `-O2`에서 다르게 동작하는 이유는 GCC가 `-O2`에서 벡터화 비용 모델을 `very-cheap`으로 두기 때문입니다. [GCC Optimize Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)에 따르면 이 모델은 데이터 의존성이나 정렬에 대한 런타임 검사가 필요하면 벡터화하지 않는데, `dst`와 `src`가 겹칠 수 있는 이 루프는 바로 그런 검사가 필요합니다. 컴파일러 간 기본값 차이는 [챕터 04](/post/compiler-optimization/compiler-comparison-gcc-clang-msvc/)에서 자세히 비교합니다.

## 컴파일러 리포트로 벡터화 확인하기

어셈블리 판독은 결과를 보여 주지만, 왜 그렇게 됐는지는 컴파일러 리포트가 알려 줍니다. GCC는 `-fopt-info-vec`(성공), `-fopt-info-vec-missed`(실패), Clang은 [LLVM Vectorizers 문서](https://llvm.org/docs/Vectorizers.html)가 설명하는 `-Rpass=loop-vectorize`(성공), `-Rpass-missed=loop-vectorize`(실패), `-Rpass-analysis=loop-vectorize`(실패 원인 문장)를 씁니다.

```bash
g++     -O3 -mavx2 -c vectorize_demo.cc -fopt-info-vec
clang++ -O2 -mavx2 -c vectorize_demo.cc -Rpass=loop-vectorize
```

위 `scale` 루프에 대한 실제 출력은 다음과 같습니다. GCC는 32바이트 벡터 본체를 만들고, 포인터가 겹칠 가능성 때문에 런타임 검사로 분기하는 "loop versioning"을 했으며, 남은 원소를 16바이트 벡터로 한 번 더 처리했다고 알려 줍니다. Clang은 벡터 폭 8과 4배 인터리브를 보고합니다.

```text
<source>:2:23: optimized: loop vectorized using 32 byte vectors
<source>:2:23: optimized:  loop versioned for vectorization because of possible aliasing
<source>:2:23: optimized: loop vectorized using 16 byte vectors

<source>:2:5: remark: vectorized loop (vectorization width: 8, interleaved count: 4) [-Rpass=loop-vectorize]
```

리포트의 "possible aliasing"은 그대로 개선 방향이 됩니다. 두 포인터가 겹치지 않는다는 것을 호출자가 보장할 수 있다면 `dst`와 `src`에 `__restrict`를 붙여 런타임 검사를 없앨 수 있습니다. 실제로 그렇게 바꾸면 GCC 14.2 `-O3` 리포트에서 "loop versioned" 줄이 사라집니다. 다만 같은 수정을 해도 GCC `-O2`에서는 이 루프가 여전히 벡터화되지 않았는데, 반복 횟수 `n`을 몰라 필요한 에필로그 루프를 very-cheap 모델이 허용하지 않기 때문입니다. GCC의 실패 메시지는 내부 분석 단계를 그대로 드러내는 경우가 많아, `-O2`에서 이 루프에 `-fopt-info-vec-missed`를 걸면 "couldn't vectorize loop" 다음에 직관적이지 않은 이유가 나오기도 합니다. 그럴 때는 Clang의 `-Rpass-analysis` 문장을 함께 보면 원인을 좁히기 쉽습니다.

## 루프 언롤링 확인

언롤링은 루프 본체를 여러 번 복사해 반복 횟수와 분기를 줄이는 최적화이며, 어셈블리에서는 같은 명령 패턴이 주소 오프셋만 바뀌며 연달아 나타나는 모습으로 보입니다. 흔히 "`-O3`가 더 많이 언롤링한다"고 생각하지만, GCC 문서의 `-O3` 목록에는 `-funroll-loops`가 없고 이 옵션은 `-fprofile-use`·`-fauto-profile`에서 켜집니다. `-O3` 출력이 `-O2`보다 길어지는 주된 이유는 벡터 본체와 남은 원소를 처리하는 에필로그가 추가되기 때문이므로, 파일 길이로 언롤링을 추정해서는 안 됩니다.

언롤링을 직접 확인하려면 옵션을 명시해 비교합니다. GCC 14.2 `-O2 -mavx2 -funroll-loops`로 위 `scale`을 컴파일하면 스칼라 루프 본체가 8회 복사되어, 주소 오프셋이 0, 4, 8, …, 28로 바뀌는 `vmulss`/`vmovss` 쌍이 나열되고 루프 인덱스는 32바이트씩 증가합니다.

```text
.L3:
        vmulss  xmm8, xmm0, DWORD PTR [rsi+rax]
        vmovss  DWORD PTR [rcx+rax], xmm8
        vmulss  xmm9, xmm0, DWORD PTR [rsi+4+rax]
        vmovss  DWORD PTR [rcx+4+rax], xmm9
        ...                                    # 같은 쌍이 오프셋 28까지 반복
        add     rax, 32
        cmp     rax, rdx
        jne     .L3
```

이 출력은 벡터화와 언롤링이 별개라는 점도 보여 줍니다. 32바이트씩 진행하는 것은 `-O3` 벡터 루프와 같지만, 접미사가 `ss`이므로 여전히 스칼라 연산입니다. 반복 횟수가 컴파일 시점에 정해진 작은 루프는 아예 루프가 사라지기도 합니다. 예를 들어 정수 8개를 더하는 고정 길이 루프는 GCC 14.2 `-O2`에서 분기 없이 `paddd`(packed 정수 덧셈) 몇 개와 셔플로 바뀝니다.

## 실전 진단 절차

어셈블리를 볼 대상은 프로파일러(perf, VTune 등)로 찾은 핫 함수입니다. 그 함수만 담은 최소 소스를 만들어 Compiler Explorer나 `-S -O2 -masm=intel`로 어셈블리를 뽑고, 핫 루프 안에 `call`이 남았는지로 인라이닝을, `ps`/`pd` 접미사와 레지스터 폭으로 벡터화를 확인합니다. 기대한 최적화가 일어나지 않았다면 `-fopt-info-vec-missed`나 `-Rpass-missed=loop-vectorize`로 이유를 묻고, 별칭·비용 모델·플래그 중 무엇이 막았는지에 따라 `__restrict`, 최적화 수준, 소스 구조를 조정합니다. LTO 빌드라면 마지막 확인은 반드시 `objdump -d -C -M intel ./app`으로 최종 바이너리에서 합니다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **호출 규약(calling convention)** | 인자 전달 레지스터·스택, 보존 레지스터, 스택 정렬 규칙. System V(rdi, rsi, …)와 Windows x64(RCX, RDX, R8, R9 + shadow store)가 다르다 |
| **packed / scalar** | `ps`/`pd`는 레지스터 전체 레인을, `ss`/`sd`는 최하위 레인 하나만 처리 |
| **vbroadcastss** | 스칼라 float 하나를 벡터 레지스터의 모든 레인에 복사하는 AVX 명령 |
| **loop versioning** | 런타임 조건(예: 포인터 겹침)에 따라 벡터 버전과 스칼라 버전 중 하나를 고르도록 루프를 복제하는 기법 |
| **lea** | Load Effective Address. 주소 계산 회로로 덧셈·스케일 곱을 한 명령에 처리 |

## 판단 기준: 언제 어셈블리를 볼지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 인라이닝 여부 확인 | 핫 루프의 `call` 유무를 `-S`·Compiler Explorer로 확인 | 소스만 보고 인라인됐다고 가정 |
| 벡터화 여부 확인 | `ps`/`pd` 접미사·레지스터 폭과 벡터화 리포트를 함께 확인 | `v` 접두사나 `xmm` 사용만으로 판단 |
| LTO 빌드 | 최종 바이너리를 `objdump -d`로 확인 | 단일 TU `-S`만 보고 판단 |

## 자주 하는 실수

- **`v` 접두사를 SIMD의 증거로 보기**: AVX 빌드에서는 스칼라 연산도 `vmulss`, `vaddsd`처럼 `v`로 시작한다. 접미사와 레지스터 폭을 본다.
- **어셈블리 파일 길이로 언롤링을 추정하기**: GCC `-O3`는 `-funroll-loops`를 켜지 않으며, 길이 차이는 주로 벡터 본체와 에필로그에서 온다. 반복되는 명령 패턴과 인덱스 증가량을 본다.
- **`-O0` 출력으로 성능을 논하기**: `-O0`은 인라이닝도 레지스터 할당도 하지 않아 모든 변수가 스택을 오간다. 성능 분석에는 실제 배포 플래그로 만든 출력을 쓴다.

## 학습 성과 목표

- `-S`, `-fverbose-asm`, `objdump -d`, Compiler Explorer가 각각 어느 시점의 산출물을 보여 주는지 구분해 쓸 수 있다.
- System V와 Windows x64 호출 규약을 근거로 어셈블리의 레지스터와 변수를 짝짓고, 인라인 전후의 차이를 설명할 수 있다.
- 접미사·레지스터 폭과 GCC·Clang 벡터화 리포트로 벡터화 성공·실패와 원인을 판별할 수 있다.

## 비판적 시각: 한계와 트레이드오프

어셈블리 읽기는 진단 도구이지 그 자체가 최적화는 아닙니다. 명령 수가 적다고 빠른 것은 아니며, 벡터화된 루프도 데이터가 캐시에 없으면 메모리 대역폭에 묶여 스칼라 루프와 비슷한 속도를 낼 수 있습니다. 또 이 챕터의 판별 규칙은 x86-64에 한정됩니다. AArch64의 NEON·SVE는 명령 이름과 레지스터 체계가 달라서(`fmul v0.4s` 같은 형식) 같은 원리를 다른 표기로 읽어야 합니다. 마지막으로 컴파일러 출력은 버전마다 바뀌므로, 이 글의 GCC 14.2·Clang 19.1.0 출력도 참고 사례일 뿐입니다. 자신의 툴체인 버전에서 같은 절차로 다시 확인하는 습관이 결론보다 중요합니다.

## 다음 장에서는

**함수 멀티버저닝**(CPU 기능별 다중 버전), GCC/Clang target 속성, 디스패치 비용을 다룹니다.

→ [함수 멀티버저닝](/post/compiler-optimization/function-multiversioning-cpu/) (챕터 07)
