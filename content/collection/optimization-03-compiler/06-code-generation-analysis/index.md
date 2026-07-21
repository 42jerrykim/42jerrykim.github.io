---
collection_order: 6
date: 2026-03-11
lastmod: 2026-07-12
draft: false
image: wordcloud.png
title: "[Compiler 03] 어셈블리 레벨 코드 생성 분석"
slug: code-generation-analysis-assembly
description: "컴파일 산출물 확인(-S, objdump, Godbolt), 함수 경계·호출 규약과 성능, hot 함수 형태·벡터화/루프가 어셈블리에서 드러나는 방식을 다룹니다. LTO 사용 시 최종 바이너리 확인 필요성과 인라인·SIMD·루프 언롤링 해석 방법을 제시합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Compiler(컴파일러)
  - CPU(Central Processing Unit)
  - Cache
  - Memory(메모리)
  - Benchmark
  - Profiling(프로파일링)
  - CI-CD(Continuous Integration/Continuous Deployment)
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

생성된 어셈블리를 보면 인라이닝·벡터화·호출 비용을 직접 확인할 수 있습니다. 이 챕터에서는 도구 사용법과 해석 포인트를 구체적인 어셈블리 예시와 함께 다룹니다. 생성 코드를 읽는 일은 고급 최적화의 기본기로, 컴파일러가 실제로 무엇을 만들었는지 확인하지 않으면 추측에 의존하게 됩니다.

> "This is an optimization manual for advanced assembly language programmers and compiler makers." — Agner Fog, [Optimizing subroutines in assembly language](https://www.agner.org/optimize/)

## 산출물 확인 도구

컴파일 산출물을 보는 도구들은 각기 다른 시점의 결과를 보여 줍니다. 어떤 단계에서 무엇을 보는지 먼저 이해하는 것이 중요합니다.

- **-S**: 컴파일러가 어셈블리 파일(.s)을 생성하도록 합니다. `g++ -S -O2 foo.cc` 또는 `clang++ -S -O2 foo.cc`로 소스에서 곧바로 .s를 얻을 수 있습니다. 이것은 **단일 TU**의 결과이므로, 다른 .cc에 있는 함수의 크로스-TU 인라이닝은 반영되지 않습니다.
- **-fverbose-asm** (GCC): 어셈블리 안에 변수명·소스 라인 등 주석을 넣어 읽기 쉽게 합니다. `-S`와 함께 `g++ -S -O2 -fverbose-asm foo.cc` 형태로 사용합니다.
- **objdump -d**: 이미 만들어진 오브젝트·실행 파일을 디스어셈블합니다. `objdump -d a.out` 또는 `objdump -d -M intel a.out`(인텔 문법)으로 기계어와 어셈블리 니모닉을 볼 수 있습니다.
- **Godbolt (Compiler Explorer)**: 웹에서 컴파일러·플래그를 바꿔 가며 소스 → 어셈블리를 비교할 수 있습니다. 여러 컴파일러·버전을 한 화면에서 비교할 때 유용하며, 소스 라인과 어셈블리 라인을 색상으로 매핑해 줍니다.

LTO를 켠 경우에는 단일 .cc만 -S로 뽑으면 크로스-TU 인라이닝이 반영되지 않습니다. 최종 링크된 바이너리를 objdump하거나, LTO 단계에서 나오는 합쳐진 IR/어셈블리를 보는 것이 전체 그림을 보는 데 필요합니다.

## 구체적인 어셈블리 예시: 인라인 전/후 비교

인라이닝이 어셈블리에 어떻게 나타나는지 구체적으로 살펴봅니다. 다음 소스를 기준으로 합니다.

```cpp
// inline_demo.cc
int add(int a, int b) {
    return a + b;
}

int compute(int x) {
    return add(x, 42) * 2;
}
```

**-O0(최적화 없음)으로 컴파일 시** `compute`의 어셈블리 (개념적):

```asm
compute:
    push   rbp
    mov    rbp, rsp
    sub    rsp, 16
    mov    DWORD PTR [rbp-4], edi     ; x를 스택에 저장
    mov    eax, DWORD PTR [rbp-4]
    mov    esi, 42
    mov    edi, eax
    call   _Z3addii                   ; add 함수 호출(call 명령)
    add    eax, eax                   ; *2
    leave
    ret
```

`call _Z3addii` — 이 줄이 **함수 호출이 남아 있다는 신호**입니다. push/pop 오버헤드가 발생합니다.

**-O2로 컴파일 시** `compute`의 어셈블리:

```asm
compute:
    lea    eax, [rdi+42]              ; add(x, 42)를 인라인: lea 하나로
    add    eax, eax                   ; *2
    ret
```

`call`이 사라지고 `lea + add + ret` 세 명령으로 압축됩니다. 이것이 **인라이닝된 상태**입니다. 함수 경계가 없어지면서 컴파일러가 전체를 한 번에 최적화할 수 있습니다.

## 구체적인 어셈블리 예시: 벡터화 확인

루프가 벡터화되었는지 어셈블리에서 확인하는 방법입니다.

```cpp
// vectorize_demo.cc: 벡터화 여부를 관찰하기 위한 루프
void scale(float* dst, const float* src, float factor, int n) {
    for (int i = 0; i < n; ++i)
        dst[i] = src[i] * factor;
}
```

**-O2 -march=native로 컴파일 시** (AVX2 지원 머신에서 GCC/Clang):

```asm
; 벡터화된 루프 본체 (개념적 — 실제 출력은 컴파일러·버전마다 다름)
vbroadcastss ymm0, xmm0        ; factor를 8개 레인에 복사 (256비트)
.Lvectorized_loop:
  vmovups     ymm1, [rsi+rax]  ; src 8개 float 로드
  vmulps      ymm1, ymm1, ymm0 ; 8개 동시 곱셈
  vmovups     [rdi+rax], ymm1  ; dst에 8개 저장
  add         rax, 32          ; 32 bytes = 8 floats 진행
  cmp         rax, rdx
  jl          .Lvectorized_loop
; 나머지 처리(tail loop)...
```

`vmovups`, `vmulps` — **v** 접두사가 붙은 명령이 SIMD 벡터 연산의 신호입니다. `ymm*` 레지스터는 256비트(8 × float), `xmm*`은 128비트(4 × float), `zmm*`은 512비트(16 × float)입니다.

**벡터화가 안 된 경우** (`-O0` 또는 루프 패턴이 벡터화를 막는 경우):

```asm
; 스칼라 루프 — SIMD 명령 없음
.Lscalar_loop:
  movss   xmm0, DWORD PTR [rsi+rax*4]  ; 하나씩 로드 (32비트만)
  mulss   xmm0, xmm1                    ; 하나씩 곱
  movss   DWORD PTR [rdi+rax*4], xmm0  ; 하나씩 저장
  inc     eax
  cmp     eax, ecx
  jl      .Lscalar_loop
```

`movss`, `mulss` — **ss**(single scalar)가 붙은 명령은 한 번에 하나의 float만 처리합니다.

## Godbolt 활용 워크플로우

**단계별 사용법**:
1. godbolt.org에 소스를 붙여 넣습니다.
2. 우측 컴파일러 탭에서 `x86-64 gcc 13.2` 또는 `x86-64 clang 17.0` 등을 선택합니다.
3. 컴파일러 옵션에 `-O2 -march=native` (또는 `-O2 -mavx2`)를 입력합니다.
4. 소스 라인을 클릭하면 해당 라인이 생성한 어셈블리 구간이 강조됩니다.
5. "Add new compiler" 버튼으로 GCC와 Clang을 나란히 두고 비교합니다.
6. `-O2`와 `-O3`를 번갈아 입력해 레벨 차이도 확인합니다.

Godbolt에서는 로컬 환경 없이 빠르게 실험할 수 있어, "이 패턴이 벡터화되는지", "인라인이 됐는지"를 즉시 확인하기에 유용합니다.

## 함수 경계와 호출 규약

<strong>호출 규약(calling convention)</strong>은 인자 전달(레지스터 vs 스택), callee-saved vs caller-saved 레지스터, 스택 정렬 등을 정의합니다. x86-64에서는 보통 첫 몇 개 인자는 레지스터로 넘기고, 나머지는 스택에 넣습니다. 함수가 **호출될 때마다** 반환 주소 저장·레지스터 저장·스택 프레임 설정·복귀 시 복원이 일어나므로, 작은 함수가 자주 호출되면 이 비용이 누적됩니다. **인라인**되면 이 경계가 사라져 호출/반환 오버헤드가 없어지고, 컴파일러가 호출부와 함께 추가 최적화를 할 수 있습니다. 어셈블리에서 `call`이 보이면 "함수 경계가 있다"고 보면 되고, 핫 루프 안에 `call`이 많으면 인라이닝 또는 함수 합치기를 검토할 만합니다.

## hot 함수 형태 해석

- **인라인 여부**: 해당 호출 지점에 `call`이 없고, 그 함수의 본문에 해당하는 명령들이 그 자리에 펼쳐져 있으면 인라인된 것입니다. `call _Z...`가 반복되면 인라인되지 않은 호출이 남아 있는 것입니다.
- **불필요한 저장/복원**: 호출 전후로 많은 `push`/`pop` 또는 스택에 대한 저장이 보이면, 레지스터 압박이나 호출 규약으로 인한 비용이 큽니다. 인라인되면 이런 저장이 줄어들거나 사라질 수 있습니다.
- **분기**: 조건문·루프가 복잡하게 나뉘어 있으면 분기 예측 실패 비용이 클 수 있습니다. 프로파일과 함께 "실제로 자주 타는 경로"가 짧고 단순한지 확인하면 도움이 됩니다.

## 벡터화/루프 형태

- **SIMD 명령**: x86에서는 `vmulps`, `vaddpd`, `vpaddd` 등 **벡터 연산**이 보이면 해당 루프가 벡터화된 것입니다. 레지스터 이름이 `xmm*`, `ymm*`, `zmm*`이면 128/256/512비트 SIMD를 쓰는 것입니다.
- **루프 언롤링**: 같은 연산이 여러 번 반복되어 한 번에 처리되는 형태로 펼쳐져 있으면 언롤링된 것입니다. 루프 백엣지(분기)가 줄어든 대신 코드가 길어집니다.
- **루프가 사라짐**: 상수 횟수 작은 루프는 완전히 펼쳐져서 루프 제어 분기가 없어질 수 있습니다.

벡터화가 안 된 루프는 스칼라 연산(`add`, `mul` 등)만 나열되고, 인덱스 증가·조건 점검 분기가 반복됩니다. 벡터화·언롤링이 성능에 중요하다면 이 챕터와 챕터 01(최적화 플래그), 04(컴파일러 비교)를 함께 참고해 플래그·컴파일러를 조정하면 됩니다.

## 루프 언롤링 확인

루프 언롤링은 루프 바디를 여러 번 복사해 반복 횟수를 줄이는 최적화입니다. 어셈블리에서 같은 명령 패턴이 연속해서 나타나면 언롤링된 것입니다.

```bash
# -O3는 -O2보다 더 공격적인 언롤링을 하는 경우가 많음
g++ -O3 -march=native -S loop_demo.cc -o loop_o3.s
g++ -O2 -march=native -S loop_demo.cc -o loop_o2.s
wc -l loop_o2.s loop_o3.s    # -O3 쪽이 더 길면 언롤링이 많다는 신호
```

## 실전 진단 절차

1. 핫 함수를 profiler(perf, VTune)로 찾는다.
2. 해당 함수만 포함한 최소 소스를 만든다.
3. `-S -O2 -fverbose-asm` 또는 Godbolt로 어셈블리를 뽑는다.
4. `call` 유무로 인라이닝 여부, `vmov/vadd` 유무로 벡터화 여부를 확인한다.
5. 원하는 최적화가 안 됐다면 이유(가시성, 루프 패턴, 플래그)를 확인하고 수정한다.
6. LTO 환경에서는 `objdump -d ./app | grep -A 30 "<func_name>"` 으로 최종 바이너리를 확인한다.

## 용어 정리

| 용어 | 설명 |
|------|------|
| **호출 규약(calling convention)** | 인자 전달(레지스터/스택), callee/caller 저장 레지스터, 스택 정렬 등; 플랫폼별로 정의됨 |
| **SIMD** | Single Instruction Multiple Data; 벡터 연산. x86에서는 xmm/ymm/zmm 레지스터 사용 |
| **vmovups** | AVX/AVX2 비정렬 벡터 로드/스토어 명령; v=벡터, mov=이동, u=unaligned, ps=packed single |
| **vmulps** | AVX/AVX2 벡터 곱셈; 8개 float를 동시에 곱 |
| **lea** | Load Effective Address; 주소 계산을 덧셈·곱셈에 활용하는 명령 |

## 판단 기준: 언제 어셈블리를 볼지

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 인라이닝·벡터화 확인 | -S·objdump·Godbolt로 호출·SIMD 확인 | 추측만으로 결론 |
| LTO 사용 시 | 최종 바이너리 또는 LTO 단계 산출물 확인 | 단일 TU -S만 보고 판단 |
| hot 함수 형태 | call·push/pop·분기 밀도 확인 | 소스만 보고 최적화 |

## 자주 하는 실수

- **LTO 켠 상태에서 단일 TU -S만 보고 판단**: LTO를 쓰면 인라이닝이 링크 시점에 일어나므로, 한 .cc만 -S로 뽑으면 크로스-TU 인라인이 반영되지 않는다. 최종 바이너리를 objdump하거나 LTO 단계 산출물을 봐야 전체 그림이 맞다.
- **어셈블리 해석 없이 추측**: "인라인됐을 것이다", "벡터화됐을 것이다"라고 가정하지 말고, call 유무·SIMD 명령·루프 형태를 실제로 확인한 뒤 최적화 전략을 세운다.

## 학습 성과 목표

- **-S**, **objdump -d**, **Godbolt**로 컴파일 산출물을 확인할 수 있다.
- 함수 경계·호출 규약이 성능에 미치는 영향과, 인라인 시 사라지는 비용을 설명할 수 있다.
- 어셈블리에서 **인라인 여부·SIMD·루프 언롤링**을 해석할 수 있다.

## 비판적 시각: 한계와 트레이드오프

어셈블리를 보는 것은 **진단 도구**이지, 그 자체가 최적화는 아니다. "어셈블리가 짧으면 빠르다" 같은 단순 규칙은 없고, 호출이 많아도 그 함수가 핫하지 않으면 영향이 작을 수 있다. 프로파일로 실제 병목을 확인한 뒤, 해당 경로의 어셈블리를 보고 인라인·벡터화·분기 배치를 판단하는 순서를 지키는 것이 효율적이다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 도구 | -S, -fverbose-asm, objdump -d, Godbolt |
| 확인 포인트 | call 유무(인라인), SIMD 명령(벡터화), 루프 형태 |
| LTO | 단일 TU -S는 불완전; 최종 바이너리 또는 LTO 산출물 확인 |

## 다음 장에서는

**함수 멀티버저닝**(CPU 기능별 다중 버전), GCC/Clang target 속성, 디스패치 비용을 다룹니다.

→ [함수 멀티버저닝](/post/compiler-optimization/function-multiversioning-cpu/) (챕터 07)
