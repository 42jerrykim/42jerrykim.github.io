---
collection_order: 1
date: 2026-08-30
lastmod: 2026-08-30
draft: false
title: "[JAX] 01. NumPy와 함수형 패러다임"
slug: numpy-and-functional-paradigm
description: "jax.numpy 배열이 NumPy와 API는 같지만 불변인 이유와 .at[idx].set() 사용법, 그리고 jit·grad 대상 함수가 순수해야 하는 이유를 전역 변수·리스트 append 오작동 예제와 lax.scan 수정 코드로 정리합니다."
tags:
  - JAX
  - NumPy
  - Autodiff(자동미분)
  - XLA
  - GPU(Graphics Processing Unit)
  - TPU(Tensor Processing Unit)
  - Python
  - PyTorch
  - Machine-Learning(머신러닝)
  - Deep-Learning(딥러닝)
  - Neural-Network
  - AI(인공지능)
  - Functional-Programming(함수형프로그래밍)
  - Vectorization(벡터화)
  - Parallel-Computing(병렬컴퓨팅)
  - Compiler(컴파일러)
  - Data-Science(데이터사이언스)
  - JIT(JIT컴파일)
  - Numerical-Computing(수치계산)
  - Debugging(디버깅)
  - Closure(클로저)
  - Array(배열)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
image: "wordcloud.png"
---

[00장](/post/jax/getting-started-jax/)에서 JAX가 존재하는 세 번째 이유로 꼽은 것이 순수 함수형 프로그래밍 모델이었습니다. 이 장은 그 약속을 코드 수준에서 구체화합니다. `jax.numpy`(관례상 `jnp`로 임포트)는 NumPy와 거의 동일한 함수·연산자 이름을 제공하지만, 배열을 다루는 규칙 하나가 근본적으로 다릅니다. 배열이 불변(immutable)이라는 점, 그리고 그 불변성이 `jax.jit`·`jax.grad` 같은 변환 대상 함수에 순수 함수(pure function)라는 조건을 강제한다는 점입니다. 이 두 규칙을 모르고 NumPy 코드를 그대로 옮기면, 에러 메시지가 명확한 경우도 있지만 에러 없이 조용히 틀린 값을 내는 경우도 있어서 더 위험합니다.

## JAX 배열은 왜 자리에서 바꿔 쓸 수 없는가

NumPy 배열은 C 배열과 마찬가지로 특정 메모리 주소를 가리키는 가변(mutable) 버퍼입니다. `x[0] = 1`은 그 주소의 내용을 덮어씁니다. JAX 배열(`jax.Array`)은 설계 자체가 다릅니다. 값이 한 번 만들어지면 내용이 절대 바뀌지 않는 불변 객체로 취급되며, "갱신"은 항상 원본은 그대로 두고 새 배열을 반환하는 형태로만 일어납니다. 이는 사소한 API 제약이 아니라, JAX가 함수 변환을 구현하는 방식의 전제 조건입니다 — 뒤에서 다루겠지만 `jit`이 연산 순서를 재배치하거나 `vmap`이 같은 연산을 배치 축으로 복제하려면, 어떤 연산도 "누가 먼저 이 메모리를 읽었는가"에 의존하지 않아야 합니다. 배열이 가변이면 이 순서 독립성을 컴파일러가 정적으로 증명할 방법이 없습니다.

이 제약은 인덱스 대입을 시도하는 순간 바로 드러납니다.

```python
import jax.numpy as jnp

x = jnp.arange(5)  # Array([0, 1, 2, 3, 4], dtype=int32)

try:
    x[0] = 100
except TypeError as e:
    print(type(e).__name__, "-", e)
```

이 코드를 실행하면 `TypeError`가 발생하며, 메시지는 JAX 배열이 불변이라 항목 단위 대입을 지원하지 않는다는 사실과 함께 `x = x.at[idx].set(y)` 형태의 대안을 안내합니다. 이 대안이 바로 JAX가 제공하는 **인덱스 갱신(indexed update)** API인 `.at[]`입니다.

```python
import jax.numpy as jnp

x = jnp.arange(5)
y = x.at[0].set(100)

print(x)  # [0 1 2 3 4] — 원본은 그대로
print(y)  # [100 1 2 3 4] — 새 배열
```

`x.at[0].set(100)`은 `x`를 수정하지 않고, `x`의 인덱스 0만 100으로 바꾼 **새 배열**을 반환합니다. `.at[]`는 `set` 외에도 `add`, `subtract`, `multiply`, `divide`, `power`, `min`, `max` 같은 인덱스 단위 연산과, 인덱스 범위를 벗어났을 때의 처리 방식을 고르는 `get`을 함께 제공합니다. 예를 들어 `x.at[2].add(10)`은 인덱스 2의 값에 10을 더한 새 배열을 반환하며, NumPy였다면 `x[2] += 10`으로 썼을 연산을 대체합니다. 함수형 갱신이라는 이름과 달리 실행 비용이 항상 배열 전체 복사인 것은 아닙니다 — `jit`으로 컴파일된 코드 안에서 `x.at[idx].set(y)`의 입력 `x`가 이후 다시 쓰이지 않는다고 컴파일러가 판단하면, XLA는 실제로는 제자리 갱신(in-place update)으로 최적화합니다. 즉 "불변"은 프로그래밍 모델 수준의 의미론이지, 매 호출이 항상 전체 배열을 복사한다는 실행 보장은 아닙니다.

인덱스 범위를 벗어난 경우의 기본 동작도 NumPy와 다릅니다. NumPy는 범위를 벗어난 인덱스에 `IndexError`를 던지지만, JAX는 GPU·TPU에서 실행되는 컴파일된 코드가 조건부로 예외를 던지기 어렵다는 제약 때문에 기본값이 다릅니다. 조회(`.at[idx].get()`)는 기본적으로 인덱스를 배열 범위 안으로 클리핑(clip)해 마지막 유효 인덱스의 값을 반환하고, 갱신(`.at[idx].set()`, `.at[idx].add()` 등)은 기본 모드 `promise_in_bounds`에서 범위를 벗어난 인덱스의 갱신을 조용히 버립니다(drop). 두 동작 모두 `mode` 인자로 `"clip"`, `"drop"`, `"fill"` 등을 명시해 바꿀 수 있습니다. 디버깅 중에는 이 기본값이 오히려 버그를 감추므로, 인덱스가 항상 범위 안이라고 확신할 수 없는 코드라면 `mode` 인자를 명시적으로 지정하는 편이 안전합니다.

## jit·grad가 순수 함수를 요구하는 이유

<strong>순수 함수(pure function)</strong>란 같은 입력에 대해 항상 같은 출력을 내고, 함수 바깥의 상태를 읽거나 쓰지 않는 함수입니다. `jax.jit`, `jax.grad`, `jax.vmap`, `jax.pmap`은 모두 파이썬 함수를 직접 실행하지 않고, 함수에 추상적인 자리표시자 값(트레이서, tracer)을 넣어 한 번 실행시켜 본 뒤 그 실행 경로를 계산 그래프로 기록하는 **트레이싱(tracing)** 방식으로 동작합니다. 이후 같은 입력 형태(shape)·자료형(dtype)으로 다시 호출되면, 파이썬 함수를 다시 실행하지 않고 트레이싱 시점에 기록해 둔 컴파일된 실행 파일을 그대로 재생(replay)합니다. 이 캐싱 구조 때문에, 함수 안에서 일어나는 파이썬 수준의 부작용(전역 변수 수정, 리스트 append, 파일 입출력 등)은 **트레이싱이 실제로 일어나는 첫 호출에서 딱 한 번만** 실행되고, 이후의 호출에서는 실행되지 않습니다.

전역 카운터를 증가시키는 함수로 이 문제를 직접 확인할 수 있습니다.

```python
import jax
import jax.numpy as jnp

counter = 0

def impure_counter(x):
    global counter
    counter += 1
    return x + counter

f = jax.jit(impure_counter)

print(f(jnp.array(1.0)))  # 2.0  (첫 호출: 트레이싱 중 counter가 0 -> 1)
print(f(jnp.array(1.0)))  # 2.0  (같은 shape/dtype -> 캐시된 실행 파일 재생, counter 갱신 안 됨)
print(f(jnp.array(5.0)))  # 6.0  (여전히 캐시 재생, counter는 계속 1)
print("counter:", counter)  # 1
```

세 번째 호출은 인자 값만 다를 뿐 형태와 자료형이 동일하므로 캐시가 재사용됩니다. `impure_counter`를 순수 함수라고 착각하면 매 호출마다 `counter`가 증가해 `f(x)`가 `x+1`, `x+2`, `x+3`을 차례로 반환하리라 기대하지만, 실제로는 `counter`가 트레이싱 시점의 값 1에 영구히 고정된 채 `x+1`만 반복됩니다. 파이썬 리스트에 값을 추가하는 함수도 같은 방식으로 어긋납니다.

```python
import jax
import jax.numpy as jnp

trace_log = []

def bad_append(x):
    trace_log.append(x)  # 트레이싱 중이라 x는 실제 값이 아니라 Tracer 객체
    return x * 2

g = jax.jit(bad_append)
g(jnp.array(3.0))
g(jnp.array(4.0))  # 같은 shape -> 캐시 재생, append 재실행 안 됨

print(len(trace_log))       # 1
print(type(trace_log[0]))   # <class 'jaxlib...Tracer'> 계열 — 3.0도 4.0도 아님
```

`trace_log`에는 두 번의 호출에도 불구하고 원소가 하나만 들어 있고, 그마저도 실제 실행 시점의 구체적인 값이 아니라 트레이싱 중에만 존재하는 추상 트레이서 객체입니다. 이 객체를 `jit` 바깥에서 NumPy 연산에 쓰려고 하면 `jit` 컨텍스트를 벗어났다는 오류가 나거나, 최악의 경우 조용히 의미 없는 값으로 취급됩니다.

이 두 예제를 올바르게 고치는 방법은 상태를 전역 변수나 클로저에 숨기지 않고 함수의 입력과 출력으로 명시적으로 통과시키는 것입니다. 카운터는 인자로 받아 갱신된 값을 반환값에 포함시킵니다.

```python
import jax
import jax.numpy as jnp

def pure_counter(x, counter):
    counter = counter + 1
    return x + counter, counter

f = jax.jit(pure_counter)

result, counter = f(jnp.array(1.0), jnp.array(0))
print(result, counter)  # 2.0 1

result, counter = f(result, counter)
print(result, counter)  # 4.0 2
```

`counter`가 더 이상 함수 바깥의 전역 상태가 아니라 매 호출마다 명시적으로 주고받는 값이므로, 몇 번을 호출하든 트레이싱은 처음 한 번만 일어나고 이후 호출은 매번 올바른 갱신 결과를 돌려줍니다. 리스트에 값을 누적하는 패턴은 `jax.lax.scan`으로 대체합니다. `scan`은 반복마다 상태(carry)를 다음 반복으로 넘기고 각 반복의 출력을 자동으로 쌓아 배열로 반환하는, JAX의 트레이싱 모델과 호환되는 반복 원시 함수(primitive)입니다.

```python
import jax
import jax.numpy as jnp

def step(carry, x):
    carry = carry + x
    return carry, carry  # (다음 carry, 이번 반복의 출력)

@jax.jit
def running_sum(xs):
    init = jnp.array(0.0)
    _, outputs = jax.lax.scan(step, init, xs)
    return outputs

xs = jnp.arange(5.0)
print(running_sum(xs))  # [ 0.  1.  3.  6. 10.]
```

`jnp.arange(5.0)`은 `[0, 1, 2, 3, 4]`이고, `step`이 누적합을 계산하므로 출력은 `[0, 1, 3, 6, 10]`입니다 — 파이썬 리스트에 손으로 append했다면 트레이싱 아래서 깨졌을 로직이, `scan`을 쓰면 `outputs`이라는 배열로 안전하게 쌓입니다. 두 수정 모두 "함수 밖의 무언가를 바꾸지 않는다"는 같은 원칙을 따릅니다: 이 원칙이 지켜지는지 확인하는 방법은 별도의 정적 분석 도구가 아니라, 같은 함수를 여러 번 호출해 보고 매번 순수 파이썬으로 계산한 기대값과 일치하는지 대조하는 것입니다 — 위 `pure_counter` 예제에서 두 번째 호출 결과가 4.0이 아니라 다른 값이 나온다면 상태가 함수 바깥으로 새고 있다는 신호입니다.

## 이 제약이 컴파일 최적화·병렬화의 전제가 되는 이유

이 절은 [00장](/post/jax/getting-started-jax/)에서 "함수형 모델이 왜 필요한지는 이 시리즈 전체를 관통하는 주제"라고 예고했던 부분을 구체화합니다. `jit`이 트레이싱한 계산 그래프를 XLA에 넘기면, XLA는 그 그래프를 하드웨어에 맞게 재배치·융합(fusion)·병렬화합니다. 예를 들어 서로 데이터 의존성이 없는 두 연산은 순서를 바꾸거나 동시에 실행해도 결과가 같아야 하고, 여러 개의 작은 연산을 커널 하나로 묶어도(fusion) 원래 순서대로 실행한 것과 같은 결과가 나와야 합니다. 이 재배치·융합이 안전하려면 그래프에 기록된 데이터 흐름이 함수의 실행 결과를 완전히 결정해야 합니다. 함수가 전역 변수를 읽거나 쓰는 부작용을 가지고 있으면, 그 부작용이 "몇 번째 호출인가"라는 그래프 바깥의 숨은 상태에 의존하게 되어 컴파일러가 재배치의 안전성을 증명할 근거를 잃습니다. 순수성 제약은 이 증명 부담을 원천적으로 없애, 트레이싱된 그래프만 보고도 최적화가 안전하다는 것을 보장합니다.

`grad`도 같은 트레이싱 메커니즘 위에서 동작합니다. 역방향 자동미분(reverse-mode automatic differentiation)은 순전파 계산 그래프를 기록한 뒤 그래프를 거꾸로 훑으며 각 연산의 국소 미분을 연쇄 법칙으로 곱해 나가는데, 이 과정이 성립하려면 순전파 그래프가 함수의 전체 동작을 빠짐없이 기술해야 합니다. 함수 바깥의 부작용으로 계산된 값이 결과에 섞여 있으면 그 값이 어떤 입력의 함수인지 그래프가 알 수 없으므로 미분 자체가 정의되지 않습니다. `vmap`과 `pmap`(4장에서 다룹니다)은 한 번 트레이싱된 순수 계산을 배치 축이나 디바이스 축으로 그대로 복제해 병렬 실행하는 변환입니다. 복제되는 계산이 전역 상태를 공유해 쓰기 경쟁을 일으키면 배치 원소마다, 또는 디바이스마다 실행 순서에 따라 결과가 달라질 수 있는데, 순수 함수는 애초에 공유할 외부 상태가 없으므로 이 경쟁 자체가 존재하지 않습니다. 정리하면 배열 불변성과 함수 순수성은 각각 독립된 제약이 아니라, "트레이싱된 그래프가 곧 함수의 전체 의미"라는 하나의 전제를 실행 가능하게 만드는 두 축입니다.

## 언제 이 제약을 의식해야 하는가

일반 파이썬 함수를 짤 때는 부작용이 자연스럽고 편리하지만, `jit`·`grad`·`vmap`·`pmap`으로 감쌀 함수를 작성할 때는 판단 기준이 달라집니다. 함수 안에서 인자로 받지 않은 값을 읽는다면(전역 변수, 클로저로 캡처한 가변 객체, 클래스 인스턴스 속성 등) 그 값이 트레이싱 시점에 고정되어도 괜찮은 상수인지 먼저 확인해야 합니다. 하이퍼파라미터처럼 호출 사이에 절대 바뀌지 않는 값이라면 문제가 없지만, 학습 스텝마다 바뀌는 값이라면 인자로 명시해야 합니다. 함수 안에서 리스트나 딕셔너리 같은 파이썬 컨테이너에 값을 축적한다면, 그 컨테이너가 함수 지역 변수로 선언되고 함수가 끝나기 전에 소비되는지(허용) 아니면 함수 바깥으로 노출되거나 여러 호출에 걸쳐 누적되는지(금지, `scan`으로 교체)를 구분합니다. `print` 같은 디버깅 출력은 트레이싱 시점에만 실행된다는 점을 받아들이고 임시 디버깅 용도로만 쓰거나, 매 호출마다 값을 보고 싶다면 트레이싱을 우회해 실행 시점에 출력하는 `jax.debug.print`류의 도구를 대신 씁니다. 배열을 갱신해야 하는 코드에서는 인덱스 대입 대신 처음부터 `.at[idx].set()` 계열을 습관화하면, 뒤늦게 `TypeError`를 만나 코드를 다시 고치는 시행착오를 줄일 수 있습니다.

## 이 장을 읽은 후 확인할 것

`x[0] = 1`이 왜 안 되는지, `.at[idx].set()`이 원본과 반환값 중 무엇을 바꾸는지 코드 없이 설명할 수 있어야 합니다. 전역 변수를 수정하는 함수를 `jit`으로 감쌌을 때 두 번째 호출부터 어떤 값이 나오는지, 그 이유가 무엇인지(트레이싱은 형태·자료형이 같으면 재실행되지 않는다는 캐싱 규칙) 설명할 수 있어야 합니다. 마지막으로, 리스트 append 대신 상태를 함수 인자·반환값으로 명시하거나 `lax.scan`으로 옮기는 수정을 실제 코드에 적용할 수 있어야 합니다. 이 세 가지가 이후 장에서 다룰 `jit`의 내부 동작(2장)과 `grad`의 자동미분(3장)을 이해하는 전제가 됩니다.

## 참고 및 출처

- [JAX 공식 문서, "🔪 JAX - The Sharp Bits 🔪 (Common Gotchas)"](https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html) — 배열 불변성, `.at[]` 인덱스 갱신, 순수 함수 요구사항을 다루는 1차 출처입니다.
- [JAX 공식 문서, "Quickstart: How to think in JAX"](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html) — 트레이싱·컴파일 캐싱 모델을 소개하는 공식 입문 문서입니다.
- [JAX 공식 문서, `jax.numpy.ndarray.at`](https://docs.jax.dev/en/latest/_autosummary/jax.numpy.ndarray.at.html) — `.at[]`가 지원하는 연산과 범위 초과 시 기본 동작(`mode` 인자)을 정리한 API 레퍼런스입니다.

다음 장에서는 `jit`이 트레이싱한 계산 그래프를 XLA가 실제로 어떻게 컴파일하는지, 그리고 왜 입력 형태가 바뀔 때마다 재컴파일이 일어나는지를 다룹니다. [02장: jit과 XLA 컴파일](/post/jax/jit-and-xla-compilation/)에서 이어집니다.
