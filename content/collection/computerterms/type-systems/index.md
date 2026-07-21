---
image: "wordcloud.png"
slug: type-systems
collection_order: 37
draft: false
title: "[Computer Terms] 타입 시스템: 정적/동적, 강/약 타입"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "타입 시스템은 정적/동적(검사 시점)과 강/약(암묵적 변환 허용 여부)이라는 서로 독립된 두 축으로 분류됩니다. 네 조합을 실제 언어 예시와 코드로 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Programming-Language(프로그래밍언어)
- Type-System(타입시스템)
- Static-Typing(정적타입)
- Dynamic-Typing(동적타입)
- Python
- TypeScript
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
- Debugging(디버깅)
- Code-Quality(코드품질)
---

## 이 장을 읽기 전에

[컴파일러와 인터프리터](/post/computerterms/compilers-and-interpreters/)에서 다룬 "오류를 언제 발견하는가"(컴파일 시점 vs 실행 시점) 논의를 이어받는다. 타입 시스템은 그 논의를 "이 값의 타입이 맞는지 언제, 얼마나 엄격하게 검사하는가"로 구체화한다.

## 두 개의 독립된 축: 검사 시점과 엄격함

타입 시스템을 이야기할 때 **정적/동적**과 **강/약**을 흔히 혼동하지만, 이 둘은 서로 다른 질문에 답하는 독립된 축이다. **정적(Static) vs 동적(Dynamic)**은 "타입 오류를 **언제** 검사하는가"를 묻는다 — 정적 타입은 [컴파일러와 인터프리터](/post/computerterms/compilers-and-interpreters/)에서 다룬 컴파일(또는 변환) 시점에, 동적 타입은 실제로 그 코드가 실행되는 순간에 검사한다. **강(Strong) vs 약(Weak)**은 "서로 다른 타입 사이의 **암묵적 변환**을 얼마나 허용하는가"를 묻는다.

## 정적 타입: 실행 전에 타입 오류를 잡는다

```typescript
// TypeScript: 정적 타입 — 컴파일(변환) 시점에 오류를 잡음
function add(a: number, b: number): number {
    return a + b;
}

add(1, "2");   // 컴파일 오류: Argument of type 'string' is not assignable to parameter of type 'number'
                // 이 코드는 실행조차 되지 않는다
```

## 동적 타입: 실행하는 순간에야 알 수 있다

```python
# Python: 동적 타입 — 실행 시점에야 타입이 결정되고 오류도 그때 발생
def add(a, b):
    return a + b

add(1, "2")   # 실행 시점에 TypeError: unsupported operand type(s) for +: 'int' and 'str'
              # 이 줄이 실제로 실행되기 전까지는 오류가 있는지 알 수 없다
```

같은 종류의 실수인데도, TypeScript는 코드를 실행하기 전에 오류를 알려주지만 Python은 그 함수가 실제로 문제의 인자로 호출될 때까지 오류를 발견하지 못한다 — 그 함수를 호출하는 코드 경로가 테스트에서 다뤄지지 않았다면, 이 버그는 운영 환경에서야 발견될 수도 있다.

## 강 타입 vs 약 타입: 암묵적 변환의 허용 정도

Python은 동적 타입이면서 동시에 비교적 **강 타입**이다 — `"2" + 1`처럼 문자열과 정수를 암묵적으로 섞으면 오류를 낸다. 반면 JavaScript는 동적 타입이면서 **약 타입**에 가깝다 — 서로 다른 타입끼리도 암묵적으로 변환해 연산을 시도한다.

```javascript
// JavaScript: 동적 + 약 타입 — 서로 다른 타입도 암묵적으로 변환해 연산
console.log("2" + 1);     // "21"  (숫자 1이 문자열로 변환되어 이어붙임)
console.log("2" - 1);     // 1     (이번엔 문자열 "2"가 숫자로 변환됨)
console.log([] + {});     // "[object Object]"  (둘 다 문자열로 변환)
```

```python
# Python: 동적이지만 강 타입 — 암묵적 변환을 허용하지 않고 명시적으로 오류를 냄
print("2" + 1)   # TypeError: can only concatenate str (not "int") to str
```

`"2" + 1`이 언어에 따라 `"21"`이 되거나, 오류가 나거나, 아예 컴파일이 안 되는 이 차이가 바로 강/약 타입 축이 정적/동적 축과 독립적이라는 것을 보여준다.

## 네 조합으로 보는 언어 분류

| | 정적 타입 | 동적 타입 |
|---|---|---|
| **강 타입** | Java, Rust, TypeScript(컴파일 후) | Python, Ruby |
| **약 타입** | C(포인터·정수 간 암묵적 변환 허용) | JavaScript, PHP |

이 네 칸 중 한 언어가 정확히 한 칸에만 속한다고 단정하기는 어렵다 — 예를 들어 C는 정적 타입이지만 `int`와 `char` 사이의 암묵적 변환을 폭넓게 허용해 약 타입에 가깝게 분류되며, TypeScript는 컴파일 단계에서는 강한 정적 검사를 하지만 결국 약 타입인 JavaScript로 변환돼 실행된다는 점에서 완전히 깔끔한 분류는 아니다.

## 흔한 오개념

**"정적 타입이 항상 더 안전하다"** — 정적 타입은 타입 불일치라는 **한 종류**의 오류를 실행 전에 잡아줄 뿐이다. 로직 오류(잘못된 계산식, 잘못된 조건문)는 타입이 아무리 정적이어도 컴파일러가 잡아주지 못한다. 동적 타입 언어도 [소프트웨어 설계 갈래](/post/computerterms/refactoring-and-code-smells/)에서 다룬 테스트로 충분히 안전하게 개발할 수 있다 — 정적 타입은 안전성을 얻는 **한 가지 방법**이지 유일한 방법이 아니다.

**"동적 타입 언어는 타입이 아예 없다"** — Python의 모든 값은 런타임에 명확한 타입(`int`, `str` 등)을 갖는다. "동적"은 "타입이 없다"가 아니라 "타입 검사가 실행 시점에 이뤄진다"는 뜻이다. `type(x)`로 언제든 실제 타입을 확인할 수 있다는 것이 이를 보여준다.

## 다른 개념과의 연결

정적 타입 검사가 [컴파일러와 인터프리터](/post/computerterms/compilers-and-interpreters/)에서 다룬 컴파일 단계의 일부로 이뤄진다는 점에서 두 챕터는 직접 이어진다. 프로그래밍 언어론 갈래는 이 챕터로 마무리되며, 다음은 코드가 어떻게 관리되고 배포되는지를 다루는 개발 프로세스 갈래로 이어간다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 정적/동적(검사 시점)과 강/약(암묵적 변환)이 서로 독립된 축임을 설명할 수 있다. 같은 코드가 언어에 따라 오류를 컴파일 시점에 내는지, 실행 시점에 내는지, 아니면 암묵적으로 변환해 실행되는지 구분할 수 있다. "정적 타입이 항상 더 안전하다"는 단순화가 왜 부정확한지 설명할 수 있다.

## 참고 자료

> Pierce, B. C. (2002). *Types and Programming Languages*, Chapter 1: Introduction. MIT Press.

- [TypeScript Handbook: Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) — 정적 타입 검사가 실제로 오류를 잡아내는 예시
- [MDN: Equality comparisons and sameness](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness) — JavaScript의 암묵적 타입 변환 규칙 상세
