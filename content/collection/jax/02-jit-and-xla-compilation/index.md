---
collection_order: 2
date: 2026-08-30
lastmod: 2026-08-30
draft: false
title: "[JAX] 02. jit과 XLA 컴파일"
slug: jit-and-xla-compilation
description: "jax.jit이 함수를 트레이싱해 jaxpr이라는 중간 표현을 만들고 이를 XLA 컴파일러로 넘겨 기계어로 바꾸는 과정과, 재컴파일이 일어나는 조건·static_argnums·if/for 제어흐름 함정을 코드와 함께 상세히 정리합니다."
tags:
  - JAX
  - NumPy
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
  - MLOps
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Advanced
  - JIT(JIT컴파일)
  - Numerical-Computing(수치계산)
  - Debugging(디버깅)
  - Profiling(프로파일링)
  - Benchmark
  - Closure(클로저)
  - Migration(마이그레이션)
  - type-hints
  - Array(배열)
  - Curriculum(커리큘럼)
image: "wordcloud.png"
---

[01장](/post/jax/numpy-and-functional-paradigm/)에서 `jax.jit`·`jax.grad`가 파이썬 함수를 직접 실행하지 않고 추상 값(트레이서)으로 한 번 실행해 본 뒤 그 실행 경로를 계산 그래프로 기록하는 **트레이싱(tracing)** 방식으로 동작한다고 설명했습니다. 이 장은 그 계산 그래프의 정체(jaxpr)와, `jit`이 그 그래프를 XLA 컴파일러에 넘겨 실제 기계어로 바꾸는 과정을 코드로 따라갑니다. `jit`을 "빠르게 만들어 주는 데코레이터" 정도로 알고 쓰면 재컴파일이 예상보다 자주 일어나거나, `if`/`for`가 들어간 함수가 뜬금없는 오류를 내는 상황을 마주하게 됩니다. 두 현상 모두 원인은 하나입니다 — `jit`은 함수를 매번 실행하는 것이 아니라, 특정 입력 형태에 대해 딱 한 번 트레이싱한 결과를 컴파일해 재생(replay)한다는 것입니다.

## 트레이싱과 jaxpr: 파이썬 함수가 계산 그래프가 되는 과정

`jit`으로 감싼 함수를 처음 호출하면 JAX는 실제 배열 값 대신 형태(shape)와 자료형(dtype)만 아는 추상 값인 <strong>트레이서(tracer)</strong>를 인자 자리에 채워 넣고, 파이썬 함수를 그 트레이서로 딱 한 번 실행합니다. 이 실행 과정에서 `jnp.sin`, `+`, `jnp.sum` 같은 JAX 연산이 호출될 때마다 트레이서는 "어떤 연산이 어떤 순서로 나를 거쳐 갔는지"를 기록하며, 실행이 끝나면 이 기록이 **jaxpr**(JAX expression)이라는 중간 표현(intermediate representation)으로 정리됩니다. jaxpr은 파이썬 문법이 전혀 남지 않은, 원시 연산(primitive)의 순서 있는 목록입니다. `jax.make_jaxpr`는 이 과정을 실제로 실행하지 않고 결과 jaxpr만 텍스트로 보여주는 디버깅 도구입니다.

```python
import jax
import jax.numpy as jnp

def f(x: jax.Array, y: jax.Array) -> jax.Array:
    return jnp.sum(x * y + jnp.sin(x))

x = jnp.ones(3)
y = jnp.ones(3) * 2

print(jax.make_jaxpr(f)(x, y))
```

이 코드를 실행하면 다음과 같은 jaxpr이 출력됩니다(JAX 0.11.1 기준, 버전에 따라 변수 이름·포맷은 달라질 수 있습니다).

```text
{ lambda ; a:f32[3] b:f32[3]. let
    c:f32[3] = mul a b
    d:f32[3] = sin a
    e:f32[3] = add c d
    f:f32[] = reduce_sum[axes=(0,) out_sharding=None] e
  in (f,) }
```

`lambda` 다음에 나열된 `a:f32[3] b:f32[3]`가 함수 인자이고, `let` 아래 각 줄이 원시 연산 하나씩입니다. `mul`, `sin`, `add`, `reduce_sum`은 각각 파이썬 소스의 `x * y`, `jnp.sin(x)`, `+`, `jnp.sum`에 대응합니다. 이 목록에 파이썬 함수 이름이나 변수명 `f`, `x`, `y`는 남지 않고, 오직 형태·자료형이 붙은 값과 그 값들 사이의 연산만 남습니다. `jit`은 파이썬 함수 자체가 아니라 이 jaxpr을 XLA 컴파일러에 넘기고, XLA는 jaxpr을 HLO(High-Level Operations)라는 자신의 내부 표현으로 다시 낮춘 뒤 대상 하드웨어의 기계어로 컴파일합니다. 이후 같은 함수를 다시 호출할 때 트레이싱을 반복하지 않고 이 컴파일된 결과를 그대로 실행하는 것이 `jit`이 속도를 얻는 근본 메커니즘입니다.

트레이싱이 파이썬 실행을 완전히 대체하지는 않는다는 점도 중요합니다. 트레이서는 실제 값이 아니므로 `print(x)`는 구체적인 숫자 대신 트레이서 객체를 출력하고, 이 `print` 자체는 트레이싱이 일어나는 첫 호출에서만 실행됩니다 — 01장에서 다룬 전역 카운터·리스트 append가 캐시 재생 시 갱신되지 않는 현상과 같은 원인입니다.

## 캐시와 재컴파일: 언제 다시 트레이싱이 일어나는가

`jit`이 트레이싱 결과를 재사용하려면 "이전에 본 것과 같은 호출인가"를 판단할 기준이 필요합니다. 이 기준이 바로 인자의 <strong>형태(shape)</strong>와 <strong>자료형(dtype)</strong>, 그리고 pytree 구조(리스트·튜플·딕셔너리로 중첩된 인자라면 그 중첩 구조)입니다. 값 자체는 기준에 들어가지 않습니다 — 값이 달라도 형태·자료형이 같으면 캐시가 재사용되고, 형태나 자료형이 하나라도 달라지면 새로운 트레이싱과 컴파일이 다시 일어납니다. 함수 안에 `print`를 넣어 두면 이 재컴파일 시점을 직접 관찰할 수 있습니다.

```python
import jax
import jax.numpy as jnp

def f(x: jax.Array) -> jax.Array:
    print("tracing with", x)
    return x * 2

f_jit = jax.jit(f)
f_jit(jnp.array([1.0, 2.0, 3.0]))  # 첫 호출: 트레이싱 발생, "tracing with ..." 출력
f_jit(jnp.array([4.0, 5.0, 6.0]))  # 같은 shape(3,)·dtype float32 -> 캐시 재생, 출력 없음
f_jit(jnp.array([1.0, 2.0]))       # shape이 (2,)로 다름 -> 재트레이싱, 다시 출력
```

실제로 실행하면 `tracing with`가 첫 번째와 세 번째 호출에서만 출력되고, 두 번째 호출에서는 출력되지 않습니다. 세 번째 호출은 값이 아니라 배열 길이(shape)가 `(3,)`에서 `(2,)`로 바뀌었기 때문에 재컴파일됩니다. dtype도 같은 방식으로 캐시 키에 들어갑니다 — 같은 형태라도 `float32` 배열로 호출한 뒤 `int32` 배열로 호출하면 재트레이싱이 일어납니다. 이 캐싱 규칙은 실전에서 미묘한 성능 함정을 만듭니다. 배치 크기가 매 스텝 달라지는 학습 루프, 또는 가변 길이 시퀀스를 패딩 없이 그대로 넣는 코드는 호출할 때마다 새 shape을 만나 매번 재컴파일되고, 그 결과 `jit`을 쓰지 않은 것보다 오히려 느려질 수 있습니다.

트레이싱·컴파일에 드는 비용과 컴파일된 결과를 재생하는 비용이 얼마나 차이 나는지는 직접 시간을 재보면 드러납니다. 아래 코드는 같은 함수를 처음 호출할 때와, 이미 컴파일된 상태로 다시 호출할 때의 벽시계 시간을 비교합니다.

```python
import time
import jax
import jax.numpy as jnp

def f(x: jax.Array) -> jax.Array:
    y = x
    for _ in range(200):
        y = jnp.sin(y) + y * 0.5
    return y

f_jit = jax.jit(f)
x = jnp.array(1.0)

t0 = time.perf_counter()
f_jit(x).block_until_ready()
t1 = time.perf_counter()
for _ in range(5):
    f_jit(x).block_until_ready()
t2 = time.perf_counter()

print(f"첫 호출(트레이싱+컴파일+실행): {t1 - t0:.4f}s")
print(f"캐시 재생 5회 평균:            {(t2 - t1) / 5:.6f}s")
```

CPU 전용 환경(2026-08, JAX 0.11.1)에서 실제로 측정하면 첫 호출은 약 0.14초, 이후 캐시 재생은 평균 0.000019초(약 19마이크로초) 정도로 나옵니다 — 약 7000배 차이입니다. 이 수치 자체는 하드웨어·JAX 버전·함수 복잡도에 따라 크게 달라지므로 그대로 인용할 절대값은 아니지만, "컴파일 비용은 트레이싱이 일어나는 순간에만 지불되고 그 이후 호출은 훨씬 저렴하다"는 정성적 사실은 이 격차의 크기에서 항상 확인됩니다. 반대로 말하면, 형태가 계속 바뀌어 매번 재트레이싱되는 코드는 이 첫 호출 비용을 매번 새로 지불하는 셈이라 `jit`의 이점을 거의 얻지 못합니다.

### static_argnums·static_argnames로 파이썬 값을 캐시 키에 포함시키기

캐시 키가 형태·자료형만 본다는 규칙은 함수 안에서 `for _ in range(n):`처럼 파이썬 정수 `n`으로 반복 횟수를 정하는 코드와 충돌합니다. `n`이 트레이서라면 반복 횟수를 트레이싱 시점에 알 수 없어 `range(n)` 자체가 오류를 냅니다. `jax.jit`의 `static_argnums`(위치 인자 인덱스)·`static_argnames`(키워드 인자 이름)는 지정한 인자를 트레이서로 바꾸지 않고 파이썬 값 그대로 유지하면서, 그 값 자체를 캐시 키에 추가하라고 지시하는 옵션입니다.

```python
import jax
import jax.numpy as jnp
from functools import partial

@partial(jax.jit, static_argnames=["n"])
def power_iter(x: jax.Array, n: int) -> jax.Array:
    for _ in range(n):
        x = x * x
    return x

print(power_iter(jnp.array(2.0), 3))  # 256.0  (n=3 -> 새로 트레이싱·컴파일)
print(power_iter(jnp.array(2.0), 4))  # 65536.0 (n=4 -> n이 바뀌었으므로 다시 트레이싱·컴파일)
print(power_iter(jnp.array(3.0), 3))  # n=3은 이미 컴파일된 적 있음 -> x 값만 다르면 캐시 재생
```

`n`을 `static_argnames`로 지정하면 `range(n)`이 파이썬 정수 `range`로 정상 동작하고, `n`이 3에서 4로 바뀔 때마다 새로운 jaxpr이 만들어져 재컴파일됩니다. 여기서 흔히 하는 오해가 하나 있습니다 — "static이면 배열도 상수 취급되니 괜찮겠지"라는 생각으로 배열 인자를 `static_argnums`에 넣는 경우입니다. static 인자는 캐시 키로 쓰이기 위해 해시 가능(hashable)해야 하는데, `jax.Array`는 해시를 지원하지 않으므로 이렇게 쓰면 `ValueError: Non-hashable static arguments are not supported`가 발생합니다. static 인자는 반복 횟수·문자열 플래그·설정값처럼 호출마다 소수의 값만 가지는 파이썬 객체에만 씁니다 — 값의 가짓수가 많으면 그만큼 재컴파일도 잦아지기 때문입니다.

## Python 제어흐름의 함정: if/for가 트레이싱 시점에 고정된다

`jit` 안에서 가장 자주 마주치는 오류는 트레이서 값으로 파이썬 `if`를 분기하려는 코드입니다. 트레이서는 형태·자료형만 아는 추상 값이라 `bool(tracer)`로 참·거짓을 확정할 방법이 없는데, 파이썬 `if 조건:`은 내부적으로 `조건`을 `bool()`로 변환해야 분기를 결정할 수 있기 때문입니다. 다음은 이 문제를 그대로 재현하는 깨진 ReLU 구현입니다.

```python
import jax
import jax.numpy as jnp

@jax.jit
def relu_broken(x: jax.Array) -> jax.Array:
    if x > 0:
        return x
    else:
        return 0.0 * x

relu_broken(jnp.array(3.0))
```

이 코드는 실행 즉시 `TracerBoolConversionError`를 던집니다. 실제 오류 메시지는 다음과 같습니다.

```text
TracerBoolConversionError: Attempted boolean conversion of traced array with shape bool[].
The error occurred while tracing the function relu_broken ... This concrete value was
not available in Python because it depends on the value of the argument x.
```

원인은 `x > 0`이 만든 `bool[]` 트레이서를 `if`가 곧바로 `bool()`로 변환하려 했다는 데 있습니다. 트레이싱은 "입력 형태에 대해 한 번만 실행해 그래프를 뽑는" 절차이므로, `x`의 구체적인 부호에 따라 다른 코드 경로를 타는 `if`는 애초에 트레이싱 모델과 맞지 않습니다. 이 함정은 `for i in range(n)`에서 `n`이 트레이서인 경우, `while` 조건이 트레이서인 경우에도 동일하게 나타납니다. 반대로 `for _ in range(n)`처럼 `n`이 파이썬 정수(위 `static_argnames` 예제)라면, 이 반복문은 트레이싱 시점에 실제로 `n`번 펼쳐져(loop unrolling) jaxpr에 그만큼의 연산이 나열됩니다 — 반복 횟수가 커질수록 jaxpr과 컴파일 시간도 함께 커진다는 뜻입니다.

고치는 방법은 분기 여부를 파이썬 `if`가 아니라 XLA가 이해하는 연산으로 표현하는 것입니다. 가장 간단한 방법은 두 분기를 모두 계산해 두고 조건에 따라 원소 단위로 선택하는 `jnp.where`입니다.

```python
import jax
import jax.numpy as jnp

@jax.jit
def relu_where(x: jax.Array) -> jax.Array:
    return jnp.where(x > 0, x, 0.0 * x)

print(relu_where(jnp.array(3.0)))   # 3.0
print(relu_where(jnp.array(-2.0)))  # -0.0
```

`jnp.where(조건, a, b)`는 파이썬 분기가 아니라 XLA의 `select` 연산으로 컴파일됩니다. `jax.make_jaxpr(relu_where)(jnp.array(3.0))`으로 확인하면 `gt`(초과 비교)와 `select_n` 연산만 남고 파이썬 `if`의 흔적은 전혀 없습니다. 다만 `jnp.where`는 이름 그대로 두 분기 `a`, `b`를 조건과 무관하게 **항상 둘 다 계산**한 뒤 결과만 고르므로, 두 분기 중 하나가 매우 무겁거나(비용이 큰 행렬 연산 등) 다른 하나가 정의되지 않은 입력에서 예외를 낼 수 있는 연산(0으로 나누기 등)이라면 부적합합니다. 이런 경우에는 실제로 조건에 맞는 한쪽 분기만 실행하도록 컴파일되는 `jax.lax.cond`를 씁니다.

```python
import jax
import jax.numpy as jnp
from jax import lax

@jax.jit
def relu_cond(x: jax.Array) -> jax.Array:
    return lax.cond(x > 0, lambda v: v, lambda v: 0.0 * v, x)

print(relu_cond(jnp.array(3.0)))   # 3.0
print(relu_cond(jnp.array(-2.0)))  # -0.0
```

`lax.cond(조건, true_fn, false_fn, 피연산자)`는 `true_fn`과 `false_fn`을 각각 별도로 트레이싱해 XLA의 조건부(conditional) 연산으로 컴파일하고, 실행 시점에는 조건에 맞는 쪽 하나만 실행합니다. 두 방식 모두 위 `relu_broken`과 같은 수학적 결과를 내지만, 선택 기준은 분기 비용입니다 — 분기가 값싼 원소 단위 연산이면 `jnp.where`가 코드도 짧고 벡터화하기도 쉽고, 분기 중 하나가 비싸거나 다른 쪽 입력에서 위험하다면 `lax.cond`로 실행 자체를 건너뛰어야 합니다.

### 클로저로 캡처한 파이썬 값도 트레이싱 시점에 고정된다

`if`/`for`만큼 자주 놓치는 함정이 하나 더 있습니다. `jit`으로 감쌀 함수가 자신의 인자가 아니라 바깥 스코프의 파이썬 변수를 클로저(closure)로 캡처해 쓰는 경우, 그 변수의 값은 트레이싱이 일어난 순간의 값으로 jaxpr에 상수로 박제됩니다. 이후 바깥 변수를 바꾸고 같은 `jit` 함수를 다시 불러도, 형태·자료형이 그대로라면 캐시가 재생될 뿐 새 값은 반영되지 않습니다. 하이퍼파라미터처럼 호출 사이에 절대 바뀌지 않는 상수를 캡처하는 것은 안전하지만, 학습률처럼 스텝마다 바뀌어야 하는 값이라면 클로저가 아니라 함수 인자로 명시해야 합니다 — 이는 01장에서 다룬 "전역 카운터가 갱신되지 않는" 문제와 원인이 같습니다. 트레이싱은 함수의 인자만 추적하고, 인자 바깥에서 읽어 온 값은 무엇이든 트레이싱 시점의 스냅샷으로 고정한다는 원칙 하나로 두 현상이 모두 설명됩니다.

## 하드웨어 독립성: 같은 jaxpr이 CPU·GPU·TPU에서 컴파일되는 이유

jaxpr에는 "이 연산을 CPU에서 실행하라"거나 "이 배열을 GPU 메모리에 올려라" 같은 하드웨어 종속적인 지시가 전혀 없습니다. 잡히는 것은 오직 원시 연산과 그 데이터 흐름뿐입니다. `jit`은 이 하드웨어 독립적인 jaxpr을 XLA에 넘기고, 실제 기계어로 낮추는 작업은 XLA의 백엔드가 담당합니다. XLA는 원래 TensorFlow 프로젝트 내부에서 만들어진 컴파일러였고, 이후 Google·Meta·Amazon·Apple 등이 함께 관리하는 OpenXLA 프로젝트로 독립해 지금은 TensorFlow·PyTorch·JAX가 공통으로 쓰는 백엔드가 되었습니다. 같은 jaxpr이라도 실행 대상이 CPU면 XLA는 벡터 레지스터를 채우는 SIMD 명령으로, GPU면 워프(warp) 단위 병렬 커널로, TPU면 행렬 곱셈 전용 유닛(MXU)을 겨냥한 명령으로 각각 다른 기계어를 만들어 냅니다. 개발자가 직접 손대는 부분은 `jax.jit(f)`라는 한 줄뿐이고, 어떤 백엔드를 쓸지는 `jax.devices()`가 보여 주는 실행 환경(로컬 CPU, CUDA GPU, TPU 파드 등)에 따라 XLA가 알아서 고릅니다. 이 사실이 뜻하는 것은 "속도가 항상 같다"가 아니라 "같은 소스 코드가 재작성 없이 여러 하드웨어에 컴파일된다"는 이식성입니다 — PyTorch 코드를 CPU에서 GPU로 옮기려면 최소한 `.to(device)` 같은 텐서 이동 코드가 필요한 것과 달리, JAX·XLA 조합에서는 배열이 어느 디바이스에 있는지에 따라 같은 `jit` 함수가 그 디바이스에 맞게 컴파일됩니다.

## 이 장이 다루지 않는 것

`jit`이 만든 jaxpr을 XLA가 내부적으로 어떻게 융합(fusion)·재배치하는지, HLO 최적화 패스가 구체적으로 무엇을 하는지는 이 장의 범위 밖입니다 — 이는 컴파일러 내부 구현이며 XLA 자체의 문서 영역입니다. `donate_argnums`(입력 버퍼 재사용), `in_shardings`/`out_shardings`(다중 디바이스 분산 배치), AOT(ahead-of-time) 컴파일(`jax.jit(f).lower(...).compile()`)도 다루지 않습니다 — 분산·병렬 실행은 4장(`vmap`·`pmap`)에서 이어집니다.

## 이 장을 읽은 후 확인할 것

`jax.make_jaxpr`로 뽑은 jaxpr을 보고 어떤 원시 연산이 몇 개 있는지 읽을 수 있어야 합니다. 같은 `jit` 함수를 두 번째로 호출했을 때 재컴파일이 일어나는지 여부를, "형태·자료형이 같은가"라는 기준만으로 예측할 수 있어야 합니다. `static_argnums`/`static_argnames`를 언제 써야 하고, 왜 배열 인자에는 쓸 수 없는지 설명할 수 있어야 합니다. 마지막으로, 트레이서 값으로 파이썬 `if`를 쓰다가 `TracerBoolConversionError`를 만났을 때 `jnp.where`와 `lax.cond` 중 어느 쪽으로 고칠지, 그 판단 기준(분기 비용)을 근거로 선택할 수 있어야 합니다. 이 네 가지는 3장에서 다룰 `grad`의 자동미분이 같은 트레이싱 메커니즘 위에서 동작한다는 사실을 이해하는 전제가 됩니다.

## 참고 및 출처

- [JAX 공식 문서, "Just-in-time compilation"](https://docs.jax.dev/en/latest/jit-compilation.html) — 트레이싱·jaxpr·`jit` 캐싱 모델을 설명하는 1차 출처입니다.
- [JAX 공식 문서, "Control flow"](https://docs.jax.dev/en/latest/control-flow.html) — `static_argnums`, `lax.cond`, `lax.while_loop` 등 제어흐름 대안을 정리한 공식 문서입니다.
- [JAX 공식 문서, `jax.jit` API 레퍼런스](https://docs.jax.dev/en/latest/_autosummary/jax.jit.html) — `static_argnums`·`static_argnames`·`donate_argnums` 등 전체 파라미터 목록입니다.
- [JAX 공식 문서, 에러 레퍼런스](https://docs.jax.dev/en/latest/errors.html) — `TracerBoolConversionError`를 포함한 JAX 특유 예외의 원인과 해결법을 정리합니다.
- [OpenXLA 프로젝트, "XLA"](https://openxla.org/xla) — XLA가 TensorFlow·PyTorch·JAX가 공유하는 컴파일러로 재편된 배경을 설명하는 프로젝트 공식 문서입니다.

다음 장에서는 `grad`가 `jit`과 같은 트레이싱 메커니즘 위에서 어떻게 코드를 한 번도 수치적으로 미분하지 않고 기울기를 계산하는지를 다룹니다. [03장: grad 자동미분](/post/jax/autodiff-with-grad/)에서 이어집니다.
