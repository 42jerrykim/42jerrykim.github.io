---
image: "wordcloud.png"
slug: memory-safety-and-ownership
collection_order: 101
draft: false
title: "[Computer Terms] 메모리 안전성과 소유권 (Memory Safety, Ownership)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "수동 메모리 관리는 use-after-free, 이중 해제 같은 버그를 낳습니다. Rust의 소유권·빌림 규칙이 이런 버그를 컴파일 시점에 원천 차단하는 원리를 가비지 컬렉션과 대비해 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Programming-Language(프로그래밍언어)
- Memory-Management(메모리관리)
- Rust
- Garbage-Collection(가비지컬렉션)
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
- Performance(성능)
- Debugging(디버깅)
- Concurrency(동시성)
- Optimization(최적화)
- Clean-Code(클린코드)
- Data-Structures(자료구조)
- Security(보안)
---

## 이 장을 읽기 전에

[메모리 관리와 가상 메모리](/post/computerterms/memory-management/)에서 다룬 `malloc`/`free`의 수동 메모리 관리와, [가비지 컬렉션](/post/computerterms/garbage-collection/)에서 다룬 자동 회수 방식을 안다고 가정한다. 이 챕터는 이 두 접근과 다른 제3의 방식, 즉 컴파일러가 메모리 규칙을 강제해 버그 자체를 없애는 방법을 다룬다.

## 수동 메모리 관리가 낳는 버그들

[메모리 관리와 가상 메모리](/post/computerterms/memory-management/)에서 다룬 `malloc`/`free`(또는 C++의 `new`/`delete`)는 프로그래머에게 큰 자유를 주지만, 그만큼 실수할 여지도 크다. 대표적인 두 가지 버그가 있다. **use-after-free**는 이미 `free`로 해제한 메모리 영역을 그 뒤에도 계속 가리키는 포인터(**댕글링 포인터, Dangling Pointer**)를 통해 접근하는 버그다. 해제된 영역은 이후 다른 용도로 재할당될 수 있으므로, 이를 읽거나 쓰면 전혀 다른 데이터를 덮어쓰거나 예측 불가능한 값을 읽게 된다. **이중 해제(Double Free)**는 같은 메모리 영역을 `free`로 두 번 해제하는 버그로, 메모리 할당기의 내부 자료구조를 손상시켜 프로그램이 무작위로 충돌하거나, 공격자가 이를 악용해 임의 코드를 실행하는 보안 취약점으로 이어질 수 있다.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int));
    *p = 42;
    free(p);           // p가 가리키던 메모리를 해제

    printf("%d\n", *p);  // use-after-free: 이미 해제된 메모리를 읽음(정의되지 않은 동작)
    free(p);              // 이중 해제: 같은 포인터를 다시 해제(정의되지 않은 동작)

    return 0;
}
```

이 코드는 C 컴파일러가 문법적으로는 허용하지만, 실행 결과는 플랫폼과 할당기 구현에 따라 달라지는 **정의되지 않은 동작(Undefined Behavior)**이다 — 아무 문제 없이 도는 것처럼 보이다가 나중에야 충돌할 수도 있어 디버깅이 특히 어렵다.

## 가비지 컬렉션이 막아주는 것과 못 막아주는 것

[가비지 컬렉션](/post/computerterms/garbage-collection/)은 "아무도 참조하지 않을 때만 회수한다"는 규칙으로 이중 해제와 use-after-free를 원천적으로 막는다 — 참조가 하나라도 남아 있으면 GC가 절대 회수하지 않으므로, 이미 회수된 메모리를 실수로 다시 가리키는 상황 자체가 생기지 않는다. 하지만 이 안전성에는 대가가 있다. GC는 언제 정확히 메모리를 회수할지 프로그래머가 통제하기 어렵고, mark-and-sweep 방식은 회수 시점에 실행을 일시 정지시킬 수 있어 짧은 지연에도 민감한 시스템(운영체제 커널, 실시간 오디오 처리, 브라우저 엔진)에는 부담이 된다.

## 소유권: 컴파일 시점에 규칙을 강제한다

Rust는 GC 없이도 메모리 안전성을 보장하는 세 번째 접근을 택한다. **소유권(Ownership)** 모델은 모든 값에 정확히 하나의 **소유자(Owner)** 변수만 있을 수 있다는 규칙을 컴파일러가 강제한다. 소유자가 스코프를 벗어나면 그 값은 자동으로 해제되며, 값을 다른 변수에 대입하면 소유권이 그 변수로 **이동(Move)**하고 원래 변수는 더 이상 그 값을 쓸 수 없게 된다.

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;              // 소유권이 s1에서 s2로 이동(move)

    println!("{}", s2);       // 정상: s2가 현재 소유자
    // println!("{}", s1);    // 컴파일 오류: s1은 더 이상 유효한 값을 가리키지 않음
}
```

`s1`이 가리키던 문자열의 소유권이 `s2`로 넘어가는 순간, Rust 컴파일러는 `s1`을 더 이상 유효하지 않은 것으로 취급한다. 그래서 주석 처리된 줄의 주석을 풀면 컴파일 자체가 되지 않는다 — 실행 전에, 잠재적인 use-after-free를 컴파일러가 원천 차단하는 것이다. 값을 소유하지 않고 잠시 참조만 하고 싶을 때는 **빌림(Borrowing)**을 쓴다.

```rust
fn calculate_length(s: &String) -> usize {  // &String: 소유권을 가져오지 않고 빌리기만 함
    s.len()
}

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);  // s1을 빌려줌(소유권은 그대로 s1에 남음)

    println!("{} 의 길이는 {}", s1, len);  // s1을 계속 쓸 수 있다
}
```

빌림에는 규칙이 있다 — 같은 시점에 **읽기 전용 빌림은 여러 개** 존재할 수 있지만, **쓰기 가능한 빌림은 단 하나만** 허용되며, 쓰기 가능한 빌림이 존재하는 동안에는 다른 어떤 빌림도 허용되지 않는다. 이 규칙을 컴파일러가 정적으로 검사하는 것을 **빌림 검사기(Borrow Checker)**라고 부르며, 이 검사를 통과한 코드는 실행 시점에 별도의 런타임 검사나 GC 없이도 use-after-free와 이중 해제가 발생하지 않음이 보장된다.

## 비교: 수동 관리 vs 가비지 컬렉션 vs 소유권

| 특성 | 수동 관리(C) | 가비지 컬렉션(Java, Python) | 소유권(Rust) |
|---|---|---|---|
| 안전성 보장 시점 | 없음(전적으로 프로그래머 책임) | 실행 시점(런타임 검사) | 컴파일 시점(빌림 검사기) |
| use-after-free | 발생 가능 | 발생하지 않음 | 컴파일 오류로 차단 |
| 런타임 오버헤드 | 없음 | 있음(GC 실행 비용) | 없음(컴파일 시점에 해소) |
| 프로그래머 부담 | 해제 시점을 직접 관리 | 낮음(회수는 자동) | 소유권·빌림 규칙 학습 필요 |

## 흔한 오개념

**"Rust는 가비지 컬렉션이 있는 언어다"** — Rust는 GC를 쓰지 않는다. 값의 소유자가 스코프를 벗어나는 순간 컴파일러가 삽입한 해제 코드가 실행되며, 이 해제 시점은 실행 중에 동적으로 결정되는 것이 아니라 컴파일 시점에 소유권 규칙만으로 이미 정해져 있다. "자동으로 메모리가 관리된다"는 결과만 보면 GC와 비슷해 보이지만, 그 방식(런타임 추적 vs 컴파일 시점 규칙)은 근본적으로 다르다.

**"소유권 모델은 항상 GC보다 우월하다"** — 소유권 모델은 런타임 오버헤드가 없는 대신, 빌림 검사기의 규칙을 프로그래머가 배우고 지켜야 하는 학습 비용과, 규칙을 만족시키기 위해 코드 구조를 더 신경 써서 짜야 하는 개발 비용이 따른다. GC 언어는 이런 규칙 없이 자유롭게 자료구조를 공유할 수 있어 개발 속도가 빠른 경우가 많다. 어느 쪽이 더 나은지는 지연 시간 요구사항과 팀의 숙련도에 따라 달라지는 트레이드오프다.

## 다른 개념과의 연결

소유권 모델은 [메모리 관리와 가상 메모리](/post/computerterms/memory-management/)의 수동 관리가 낳는 버그를, [가비지 컬렉션](/post/computerterms/garbage-collection/)과는 다른 방식(런타임 추적 대신 컴파일 시점 규칙)으로 해결하는 접근이다. 이 챕터로 프로그래밍 언어론 갈래의 심화 내용을 마무리하며, 언어가 메모리를 다루는 세 가지 철학(수동·자동·컴파일 시점 검증)을 모두 짚었다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. use-after-free와 이중 해제가 왜 위험한지 예시 코드로 설명할 수 있다. 소유권과 빌림 규칙이 이 버그들을 컴파일 시점에 차단하는 원리를 설명할 수 있다. 수동 관리·가비지 컬렉션·소유권 세 접근의 안전성 보장 시점과 런타임 오버헤드 차이를 비교할 수 있다.

## 참고 자료

> Matsakis, N. D., & Klock, F. S. (2014). "The Rust Language." *ACM SIGAda Ada Letters*, 34(3), 103–104.

- [The Rust Programming Language: Understanding Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) — 소유권·빌림·라이프타임에 대한 공식 문서
- [OWASP: Using Freed Memory (CWE-416)](https://owasp.org/www-community/vulnerabilities/Using_freed_memory) — use-after-free가 실제 보안 취약점으로 이어지는 사례
