---
title: "[Programming] S-expression 문법: dotted pair부터 quasiquote까지"
description: "S-expression은 Lisp 계열 언어의 데이터 표현이자 리더 문법입니다. atom·list·dotted pair부터 quote/quasiquote까지 핵심 문법을 예제로 정리하고 Scheme·Common Lisp·Clojure의 reader 차이를 비교합니다."
date: 2026-02-04
lastmod: 2026-02-04
categories:
  - Programming
  - Lisp
  - Language
tags:
  - S-expression
  - S-expr
  - sexp
  - symbolic expression
  - Symbolic Expressions
  - John McCarthy
  - McCarthy 1960
  - Lisp
  - Scheme
  - R5RS
  - Common Lisp
  - CLHS
  - Clojure
  - reader
  - Reader
  - reader macro
  - read syntax
  - datum syntax
  - external representation
  - code as data
  - homoiconicity
  - AST
  - parse
  - parser
  - token
  - whitespace
  - parentheses
  - list
  - proper list
  - improper list
  - dotted list
  - dotted pair
  - cons
  - car
  - cdr
  - nil
  - quote
  - quasiquote
  - unquote
  - unquote-splicing
  - backquote
  - macro
  - macros
  - metaprogramming
  - REPL
  - 함수 호출
  - 데이터 구조
  - 데이터 표현
  - 외부표현
  - S-표현식
  - 심볼릭 표현식
  - 리스프
  - 스킴
  - 커먼리스프
  - 클로저
  - 리더 문법
  - 리더 매크로
  - 점표기
  - 도트 페어
  - 컨스 셀
  - 카
  - 씨디알
  - 인용
  - 준인용
  - 언쿼트
  - 괄호
  - 공백
  - 구문
  - 문법
image: "wordcloud.png"
---

S-expression(S-표현식)은 “Lisp의 괄호 문법” 정도로 가볍게 소개되곤 하지만, 실제로는 **데이터의 외부 표현(external representation)** 이자, 많은 Lisp 계열 언어에서 **리더(reader)가 입력을 데이터 구조로 바꾸는 규칙**을 뜻합니다. 그래서 S-expression을 이해하면 다음이 한 번에 정리됩니다.

- 왜 `(f x y)` 형태가 함수 호출로 읽히는지
- 왜 `(a . b)` 같은 점표기(dotted pair)가 존재하는지
- 왜 `'x`가 단순한 “문법 설탕” 이상인지(코드=데이터의 관문)
- Scheme/Common Lisp/Clojure에서 “같아 보이지만 다른” reader 문법 차이가 무엇인지

## S-expression의 고전적 정의(원형)

John McCarthy의 1960년 논문에서 S-expression은 크게 두 가지로 정의됩니다.

- **atom**(원자): 원자 심볼은 S-expression이다.
- **ordered pair**(순서쌍): \(e_1\)과 \(e_2\)가 S-expression이면 \((e_1 \cdot e_2)\)도 S-expression이다.

여기서 오늘날 우리가 흔히 보는 리스트 표기는, 사실상 **순서쌍(cons cell)** 을 연쇄로 이어 붙인 약식입니다.

## 핵심 문법 치트시트

아래 예시는 “무엇이 S-expression(데이터)로 읽히는가”에 초점을 맞춥니다. (평가/실행 규칙은 언어별로 더 다양합니다.)

### 1) Atom

- **심볼**: `foo`, `+`, `map`, `my-namespace/foo` (언어별 허용 문자/네임스페이스 규칙은 다름)
- **숫자**: `42`, `3.14`
- **문자열**: `"hello"`

### 2) 리스트(list)

괄호로 둘러싼 형태는 대부분 “리스트”로 읽힙니다.

```lisp
(a b c)
```

### 3) Dotted pair / Improper list (점표기, 비정상 리스트)

S-expression을 “순서쌍”으로 본다면 가장 원형에 가까운 표기는 이것입니다.

```lisp
(a . b)
```

리스트는 사실상 cons의 연쇄이고, proper list는 마지막 cdr이 `nil`(혹은 언어의 empty list)인 형태입니다. (언어마다 빈 리스트/`nil`의 취급은 조금씩 다릅니다.)

```lisp
(a b c)      ; (a . (b . (c . nil))) 의 약식
(a b . c)    ; (a . (b . c)) : 마지막이 nil이 아니므로 improper list
```

이 점표기 규칙은 **데이터 구조를 정확히 표현**할 때(예: `(key . value)` 같은 연관쌍) 특히 중요합니다.

“약식이 어떻게 풀리는지”를 `cons`로 보면 직관이 생깁니다.

```lisp
; (a b c)
(cons 'a (cons 'b (cons 'c nil)))

; (a . b)
(cons 'a 'b)
```

### 4) Quote: `'x`는 무엇을 의미하나

대부분의 Lisp 계열에서 `'exp`는 아래의 약식입니다.

```lisp
'x        ; (quote x)
'(a b c)  ; (quote (a b c))
```

즉, 리더 단계에서 이미 `'`는 **리더 매크로(reader macro)** 로서 동작해, 입력을 `(quote ...)` 형태의 데이터로 바꿉니다.

### 5) Quasiquote / Backquote + Unquote(+Splicing)

quote가 “그대로 두기”라면, quasiquote/backquote는 “템플릿에 일부만 평가 값을 끼워 넣기”에 가깝습니다.

Scheme/Common Lisp 계열(표기: `` ` ``, `,`, `,@`) 예시:

```lisp
`(a b ,x)     ; x를 평가해서 그 값이 들어감
`(a ,@xs b)   ; xs(리스트/시퀀스)를 풀어서(splice) 여러 원소로 삽입
```

Clojure는 동일한 컨셉을 다른 기호로 씁니다(표기: `` ` ``, `~`, `~@`).

## 언어별 reader 문법 차이(“비슷해 보이지만 다르다”)

S-expression 자체는 개념이지만, 실제 사용자는 특정 언어의 “reader”를 만나게 됩니다.

### Scheme(R5RS): datum/read syntax 관점

Scheme 표준 문서에서는 “입력 문자열을 datum으로 읽는 규칙”을 문법으로 정의합니다. 리스트, dotted pair, quote/quasiquote의 동작이 **읽기 단계**에서 어떻게 해석되는지 확인하기 좋습니다.

- dotted pair: `(a . b)`
- quote: `'x`
- quasiquote: `` `(...) `` + `,`/`,@`

예를 들어 quasiquote 템플릿은 이런 감각입니다.

```scheme
`(a ,x ,@xs)
```

### Common Lisp: reader macro characters(강력한 리더)

Common Lisp의 reader는 표준 macro character들이 풍부합니다. 특히 `.`(점표기), `'`(quote), `` ` ``(backquote), `,`/`,@`(unquote/splicing)은 “입력→데이터” 변환을 규정하는 핵심입니다.

또한 CL의 backquote는 구현이 내부적으로 `append`, `list`, `cons` 조합으로 변환되는 식으로 설명되곤 하지만, 중요한 건 “리더가 특정한 데이터(코드)를 만들어 준다”는 점입니다.

덧붙여 Common Lisp은 `readtable`을 통해 “어떤 문자들이 어떤 방식으로 읽히는지”를 커스터마이즈할 수 있어서, 언어/DSL 제작에서 reader 단계가 특히 강력해집니다.

### Clojure: S-expression + 추가 리터럴(벡터/맵/키워드)

Clojure는 리스트 기반 표현을 사용하지만, reader 레벨에서 다음 리터럴을 기본 제공합니다.

- **vector**: `[1 2 3]`
- **map**: `{:a 1 :b 2}`
- **keyword**: `:user/id`

그리고 Clojure의 syntax-quote(백틱)는 단순 quote보다 강력해서, 네임스페이스를 자동으로 수식(qualification)하는 등 “매크로 작성에 유리한” 추가 규칙이 있습니다. 즉 “S-expression을 읽는다”는 동일한 출발점 위에, 언어가 의도적으로 리더 규칙을 더 얹은 사례입니다.

```clojure
'(a b c)      ; (quote (a b c))
`(a ~x ~@xs)  ; syntax-quote + unquote/unquote-splicing
```

## 같은 표기, 다른 의미가 생기는 지점: 빈 리스트와 nil/false

reader 문법이 비슷해도, “빈 리스트/거짓/없음”의 의미론은 언어마다 다릅니다.

- **Common Lisp**: `NIL`은 빈 리스트이면서 거짓
- **Scheme**: `'()`(빈 리스트)와 `#f`(거짓)가 분리
- **Clojure**: `nil`과 `false`가 분리(빈 컬렉션은 truthy)

## 실전 팁: 자주 하는 실수 6가지

1. **리더 vs 평가 혼동**: `(1 2 3)`은 “리스트로 읽히지만”, 평가하면(언어에 따라) 함수 호출 규칙으로 해석될 수 있습니다.
2. **dotted list는 구조를 바꾼다**: `(a b . c)`는 `(a b c)`와 완전히 다른 자료구조입니다.
3. **공백은 토큰 경계**: `foo-bar`는 심볼 1개지만 `foo - bar`는 토큰 3개입니다.
4. **quote가 없으면 심볼은 ‘값’으로 해석될 수 있다**: `(a b)`에서 `a`가 함수/연산자로 평가되는 계열이 많습니다.
5. **quasiquote 중첩 깊이**: quasiquote 내부에서 unquote가 언제 해석되는지는 중첩 규칙이 있습니다(특히 매크로 작성 시).
6. **언어별 literal 확장**: Clojure의 벡터/맵/키워드처럼, “괄호만이 전부”가 아닌 언어도 많습니다.

## S-expression을 “문법”으로 볼 때 가장 중요한 구분: read vs eval

S-expression을 이해할 때 헷갈림의 80%는 “읽기(read)”와 “평가(eval)”를 섞어서 생각하는 데서 옵니다.

- **read**: 텍스트 → 데이터 구조 (리스트/심볼/숫자/문자열/…)
- **eval**: 데이터 구조 → 실행/값 (언어의 평가 규칙에 따름)

즉, `(f x y)`는 *read 단계*에서는 그저 “리스트”이고, *eval 단계*에서 “첫 원소를 연산자로 보고 나머지를 인자로 평가”하는 규칙이 흔할 뿐입니다(언어별 예외와 확장이 존재).

## 참고 자료

- McCarthy(1960) 원문(HTML): [Recursive Functions of Symbolic Expressions…](https://www-formal.stanford.edu/jmc/recursive/node3.html)
- Scheme R5RS Syntax: [Revised(5) Scheme - Syntax](https://people.csail.mit.edu/jaffer/r5rs/Syntax.html)
- Common Lisp HyperSpec(Reader): [2.4.6 Reader Syntax](https://www.lispworks.com/documentation/HyperSpec/Body/02_df.htm)
- Clojure 공식 문서: [The Reader](https://clojure.org/reference/reader)
