---
image: "wordcloud.png"
slug: registers-and-isa
collection_order: 60
draft: false
title: "[Computer Terms] 레지스터와 명령어 집합 구조 (Register, ISA)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "레지스터가 캐시·메인 메모리보다 빠른 이유를 CPU 내부의 물리적 위치와 접근 방식으로 설명하고, 명령어 집합 구조(ISA)가 소프트웨어와 하드웨어를 잇는 계약이라는 개념, RISC와 CISC의 설계 철학 차이를 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Computer-Architecture(컴퓨터구조)
- CPU
- Assembly(어셈블리)
- Performance(성능)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Memory(메모리)
- Operating-System(운영체제)
- Register(레지스터)
- ISA(명령어집합구조)
- RISC
- CISC
- Compiler(컴파일러)
- Hardware(하드웨어)
- Low-Level(로우레벨)
---

## 이 장을 읽기 전에

[CPU 구조와 파이프라이닝](/post/computerterms/cpu-and-pipelining/)에서 명령어가 인출·해독·실행·저장 단계를 거친다고 다뤘다. 이 챕터는 그 네 단계에서 실제로 값을 담아두는 가장 작고 빠른 저장 공간인 레지스터와, CPU가 이해할 수 있는 명령어의 형태를 정의하는 명령어 집합 구조(ISA)를 다룬다. 컴퓨터 구조 갈래의 새 하위 주제로, 이후 캐시 계층·SIMD·부동소수점·폰 노이만 구조로 이어진다.

## 레지스터가 캐시보다도 빠른 이유

**레지스터(Register)**는 CPU 코어 내부에 물리적으로 새겨진 저장 공간이다. L1 캐시조차 CPU 다이 위에 있지만 레지스터와는 별도의 회로 블록이며, 값을 꺼내려면 주소 디코딩과 캐시 태그 비교를 거쳐야 한다. 반면 레지스터는 실행 유닛(ALU)과 배선으로 직접 연결돼 있어 주소 계산이나 태그 비교 없이 한 사이클 안에 값을 읽고 쓸 수 있다. 이 물리적 근접성 때문에 레지스터는 메모리 계층에서 가장 빠르지만, 대신 개수가 극히 적다 — 일반적인 x86-64 범용 레지스터는 16개, ARM64는 31개 수준이다(정확한 개수는 아키텍처마다 다르다). 컴파일러는 자주 쓰는 변수를 이 좁은 레지스터 공간에 최대한 오래 붙잡아 두려고 하는데, 이를 **레지스터 할당(Register Allocation)**이라 부르며 컴파일러 최적화의 핵심 과제 중 하나다.

## 명령어 집합 구조: 소프트웨어와 하드웨어 사이의 계약

**명령어 집합 구조(ISA, Instruction Set Architecture)**는 CPU가 실행할 수 있는 명령어의 종류, 각 명령어가 사용하는 레지스터·주소 지정 방식, 데이터 타입을 정의한 규격이다. 소프트웨어를 만드는 쪽(컴파일러 개발자)과 하드웨어를 만드는 쪽(CPU 설계자)은 이 ISA 하나만 합의하면, 서로 상대방의 내부 구현을 몰라도 함께 동작하는 시스템을 만들 수 있다 — 인텔이 CPU 내부 파이프라인 구조를 완전히 바꿔도 x86-64 ISA만 그대로 유지하면 기존 컴파일된 바이너리가 계속 실행되는 이유가 여기에 있다. 이런 의미에서 ISA는 소프트웨어와 하드웨어 사이의 **계약(Contract)**이다: 계약 위의 세부 구현(파이프라인 깊이, 캐시 크기, 실제 회로 배선)은 세대마다 바뀌어도, 계약 자체(명령어 이름, 인코딩, 동작 의미)는 하위 호환을 위해 거의 바뀌지 않는다.

```text
고수준 언어 (C, Rust, ...)
        │  컴파일
        ▼
어셈블리 / ISA가 정의한 명령어 (mov, add, jmp, ...)
        │  이 경계가 ISA — 소프트웨어와 하드웨어의 계약
        ▼
마이크로아키텍처 (파이프라인, 캐시, 실행 유닛 — 세대마다 다름)
        │
        ▼
실제 트랜지스터 회로
```

같은 x86-64 ISA를 구현하는 인텔 CPU와 AMD CPU는 내부 마이크로아키텍처가 전혀 다르지만, 둘 다 같은 컴파일된 바이너리를 실행할 수 있다. 아래는 x86-64 어셈블리로, 레지스터 두 개(`eax`, `ebx`)를 더해 결과를 저장하는 명령어다. 이 코드는 ISA가 정의한 `add` 명령어의 의미를 그대로 보여준다.

```c
#include <stdio.h>

int add_two(int a, int b) {
    int result;
    /* 함수 인자 a, b 자체는 System V AMD64 ABI(표준 호출 규약)에 따라 컴파일러가 배치하지만,
       아래 인라인 asm은 그와 별개로 GCC 확장 제약조건 "a"/"b"로 a를 eax에, b를 ebx에
       직접 배치하도록 강제한다 — 이 예제가 보여주는 것은 호출 규약이 아니라 ISA 명령어 자체다 */
    __asm__ ("addl %%ebx, %%eax"
             : "=a" (result)
             : "a" (a), "b" (b));
    return result;
}

int main(void) {
    printf("%d\n", add_two(3, 4));   /* 7 */
    return 0;
}
```

`addl %ebx, %eax`는 ISA가 "eax 레지스터 값에 ebx 레지스터 값을 더해 eax에 저장한다"고 정의한 명령어를 그대로 부른 것이다. 이 코드가 실제로 어떤 회로로 실행되는지(연산 유닛 배치, 파이프라인 단계 수)는 CPU 세대와 제조사에 따라 달라도, `addl`이 의미하는 바는 ISA 문서에 고정돼 있어 바뀌지 않는다.

## RISC와 CISC

ISA는 설계 철학에 따라 크게 두 갈래로 나뉜다. **CISC(Complex Instruction Set Computer)**는 x86처럼 한 명령어가 메모리 접근과 연산을 함께 수행하는 등 복잡한 동작을 하나로 묶어, 적은 명령어로 많은 일을 하도록 설계됐다. **RISC(Reduced Instruction Set Computer)**는 ARM처럼 각 명령어를 단순하게 유지하는 대신(대부분 레지스터끼리만 연산하고 메모리 접근은 별도 load/store 명령어로 분리) 명령어 하나의 실행 시간을 예측하기 쉽게 만들어 파이프라이닝 효율을 높인다. 두 철학은 절대적 우열이 아니라 트레이드오프다 — 최신 x86 CPU도 내부적으로는 복잡한 CISC 명령어를 더 작은 RISC 스타일 마이크로 연산(micro-op)으로 쪼개 실행하는 것으로 알려져 있다(내부 구현은 제조사가 공개하지 않아 구현 정의로 남는다).

## 비교: RISC vs CISC

| 특성 | RISC (예: ARM) | CISC (예: x86) |
|---|---|---|
| 명령어당 동작 | 단순, 1개 동작 위주 | 복잡, 여러 동작 결합 가능 |
| 명령어 길이 | 대부분 고정 길이 | 가변 길이 |
| 메모리 접근 | load/store 명령어로 분리 | 대부분 명령어가 메모리 접근 가능 |
| 파이프라이닝 | 예측이 쉬워 효율적 | 디코딩이 복잡해 상대적으로 어려움 |
| 대표 사례 | ARM, RISC-V | x86-64 |

이 표에서 실무 판단의 기준은 **레거시 호환성과 전력 효율 중 무엇이 더 중요한가**다. 새로 설계하는 시스템이고 예측 가능한 파이프라인·낮은 전력 소비가 중요하다면(모바일 기기, 임베디드, 최근의 서버·데스크톱 CPU까지) RISC 철학(ARM, RISC-V)이 유리하다. 실제로 스마트폰·태블릿은 거의 전량 ARM을 쓰고, Apple Silicon처럼 데스크톱·서버로도 RISC 철학이 확장되는 추세다. 반면 수십 년간 x86 바이너리로 축적된 소프트웨어 생태계(윈도우 애플리케이션, 특정 산업용 소프트웨어)를 그대로 돌려야 한다면, CISC 명령어 집합인 x86-64를 벗어나기 어렵다 — ISA를 바꾸면 그 위에서 동작하던 모든 실행 파일을 다시 컴파일하거나 에뮬레이션해야 하므로, 순수 설계상의 우열과 별개로 기존 생태계의 전환 비용이 실무 선택을 좌우하는 경우가 많다.

## 흔한 오개념

**"레지스터가 빠른 건 캐시보다 용량이 작기 때문이다"** — 용량 차이는 결과일 뿐 원인이 아니다. 레지스터가 빠른 근본 이유는 CPU 실행 유닛과 직결된 물리적 위치와 주소 디코딩이 없는 접근 방식이다. 용량이 작은 이유도 사실은 거꾸로다: 접근 회로를 실행 유닛에 최대한 가깝게 두려다 보니 물리적으로 많이 둘 수 없는 것이다.

**"RISC는 명령어 수가 적어서 항상 CISC보다 코드 크기가 작다"** — 오히려 반대인 경우가 많다. RISC는 복잡한 동작을 여러 단순 명령어로 쪼개기 때문에 같은 작업을 하는 데 더 많은 명령어(더 큰 바이너리)가 필요할 수 있다. RISC의 이점은 코드 크기가 아니라 각 명령어의 실행 시간을 예측하기 쉬워 파이프라이닝·클럭 속도 최적화가 유리하다는 데 있다.

## 다른 개념과의 연결

레지스터가 CPU 파이프라인의 인출·해독·실행·저장 각 단계에서 실제로 값을 주고받는 통로라는 점은 [CPU 구조와 파이프라이닝](/post/computerterms/cpu-and-pipelining/)에서 다룬 네 단계와 직접 이어진다. 레지스터 다음으로 빠른 저장 공간인 캐시가 어떻게 계층을 이루는지는 다음 챕터인 캐시 계층에서 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 레지스터가 캐시·메모리보다 빠른 이유를 물리적 위치와 접근 방식으로 설명할 수 있다. ISA가 왜 소프트웨어와 하드웨어 사이의 계약인지, 마이크로아키텍처와 무엇이 다른지 구분할 수 있다. RISC와 CISC의 설계 철학 차이와 각각의 트레이드오프를 설명할 수 있다.

## 참고 자료

> Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach* (6th ed.), Chapter 1: Fundamentals of Quantitative Design and Analysis (Instruction Set Principles). Morgan Kaufmann.

- [Wikipedia: Instruction Set Architecture](https://en.wikipedia.org/wiki/Instruction_set_architecture) — ISA의 정의와 구성 요소 개요
- [Wikipedia: X86-64](https://en.wikipedia.org/wiki/X86-64) — x86-64 ISA의 레지스터 구성과 CISC 설계 특징 개요
