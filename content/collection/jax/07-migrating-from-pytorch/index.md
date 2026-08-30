---
collection_order: 7
date: 2026-08-30
lastmod: 2026-08-30
draft: false
title: "[JAX] 07. PyTorch에서 마이그레이션"
slug: migrating-from-pytorch
description: "torch.Tensor·autograd·nn.Module·optimizer.step()을 JAX 개념으로 매핑하고, 순수성 위반·전역 PRNG·jit 재컴파일 함정 3가지와 eager 대 trace-and-compile 실행 모델 차이를 실전 코드로 다룹니다."
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
  - MLOps
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Advanced
  - Case-Study
  - JIT(JIT컴파일)
  - Numerical-Computing(수치계산)
  - Debugging(디버깅)
  - Migration(마이그레이션)
  - Array(배열)
  - Curriculum(커리큘럼)
  - Benchmark
image: "wordcloud.png"
---

PyTorch 코드베이스를 JAX로 옮기는 작업에서 가장 먼저 부딪히는 문제는 문법이 아니라 실행 모델이다. `torch.Tensor`는 있는 그대로 대응하는 `jax` 객체가 있지만, `nn.Module`의 `self.weight = ...`처럼 인스턴스가 자기 상태를 직접 들고 다니는 습관은 JAX의 순수 함수 제약과 정면으로 부딪힌다. [6장 Flax·Optax로 신경망 실전](/post/jax/neural-networks-with-flax-optax/)에서 이미 함수형 학습 루프를 직접 짜 봤다면, 이번 장은 그 코드가 "왜 그렇게 생겨야 했는지"를 PyTorch와의 차이로 역추적하는 자리다. API를 표로 매핑하는 데서 그치지 않고, PyTorch 습관을 그대로 옮겼을 때 실제로 터지는 함정 세 가지를 잘못된 코드부터 보여준다.

## 개념 매핑: PyTorch API를 JAX로 옮기기

PyTorch의 `nn.Module`은 객체가 자신의 파라미터·버퍼·옵티마이저 상태를 속성으로 들고 있는 <strong>객체지향(Object-Oriented)</strong> 모델이다. `model.weight`를 읽고 `loss.backward()`를 호출하면 프레임워크가 계산 그래프를 따라가며 `.grad` 속성을 채워 넣는다. JAX에는 이런 암묵적 상태 저장소가 없다. `jax.grad`는 순수 함수를 입력받아 또 다른 순수 함수(기울기 함수)를 반환하고, 파라미터는 함수 인자로 명시적으로 전달되는 값일 뿐이다. 이 차이 때문에 API를 1:1로 바꿔 끼우는 방식으로는 마이그레이션이 끝나지 않는다 — "상태를 어디에 보관하고 누가 갱신하는가"라는 설계 자체가 달라진다.

아래 표는 자주 마주치는 여섯 가지 대응 관계를 정리한 것이다. 각 행은 문법이 비슷해 보여도 내부 동작 방식이 다르므로, 표 아래에서 `device_put`과 `.at[].set()` 두 가지를 코드로 보충한다.

| PyTorch | JAX | 핵심 차이 |
|---|---|---|
| `torch.Tensor` | `jax.Array`(구 `jax.numpy.ndarray`) | JAX 배열은 불변(immutable)이다. 슬라이스 대입이 되지 않는다. |
| `tensor.requires_grad_()` + `loss.backward()` | `jax.grad(loss_fn)(params, ...)` | PyTorch는 텐서에 그래프를 암묵적으로 기록하고, JAX는 함수를 입력받아 새 함수(기울기 함수)를 만든다. |
| `class Model(nn.Module): ...` | Flax `nnx.Module` 또는 `linen.Module` (6장 참고) | Flax도 클래스 문법을 제공하지만, 파라미터는 트리 구조로 분리되어 `jit`·`grad`에 명시적으로 전달된다. |
| `optimizer.step()` | `optax.apply_updates(params, updates)` | PyTorch 옵티마이저는 파라미터를 제자리에서 수정한다. Optax는 새 파라미터 값을 반환할 뿐 아무것도 직접 바꾸지 않는다. |
| `tensor.to(device)` | `jax.device_put(x, device)` | PyTorch는 디바이스 간 이동이 항상 명시적이다. JAX 배열은 커밋되지 않은 상태로 기본 디바이스에 배치되며 필요 시 암묵적으로 옮겨질 수 있다. |
| `x[0] = 1` (in-place) | `x = x.at[0].set(1)` | JAX는 원본을 바꾸지 않고 갱신된 사본을 반환한다. `jit` 안에서 원본이 재사용되지 않으면 컴파일러가 실제로는 제자리 갱신으로 최적화한다. |

`jax.device_put`은 텐서를 특정 디바이스로 옮기는 연산이지만, PyTorch의 `.to(device)`와 달리 인자를 생략하면 "커밋되지 않은(uncommitted)" 배열을 만들어 실행 시점에 필요한 디바이스로 자동 이동하게 둘 수도 있다.

```python
import jax
import jax.numpy as jnp

x = jnp.ones((4, 4))

# 특정 디바이스로 명시적으로 옮긴다 (torch.Tensor.to(device)에 대응).
cpu_devices = jax.devices("cpu")
x_cpu = jax.device_put(x, device=cpu_devices[0])
print(x_cpu.device)
```

`x[0] = 1`처럼 인덱스에 직접 대입하는 코드는 JAX에서 `TypeError`를 낸다. 대신 `.at[idx]` 접근자가 "이 위치를 이렇게 바꾼 새 배열을 만들라"는 의도를 표현한다.

```python
import jax.numpy as jnp

x = jnp.zeros((3, 3))
y = x.at[1, :].set(1.0)  # x는 그대로, y가 갱신된 새 배열이다.
print("x[1]:", x[1])     # [0. 0. 0.]
print("y[1]:", y[1])     # [1. 1. 1.]
```

`nn.Module`과 Flax Module의 매핑은 표만으로는 오해하기 쉽다. Flax `nnx.Module`은 PyTorch와 거의 동일하게 `self.linear = nnx.Linear(...)`처럼 속성으로 레이어를 등록할 수 있지만, 그 파라미터는 여전히 `jit`·`grad`가 순회할 수 있는 트리 구조(`nnx.Param`)로 분리되어 있다 — 이 분리를 실제로 코드로 다루는 방법은 6장에서 다뤘으므로 여기서는 반복하지 않는다.

## PyTorch 개발자가 자주 겪는 함정 3가지

앞의 표를 외운다고 해서 마이그레이션이 끝나지 않는 이유는, PyTorch에서 자연스러웠던 습관 세 가지가 JAX에서는 조용히 틀린 결과를 내거나 성능을 무너뜨리기 때문이다. 각 함정을 잘못된 코드 → 원인 → 올바른 코드 순서로 다룬다.

### 함정 1: 클래스 인스턴스 상태를 직접 수정하기

PyTorch에서는 `self.running_loss += loss`처럼 `forward()` 안에서 인스턴스 속성을 직접 갱신하는 코드가 흔하다. 객체가 가변(mutable)이기 때문에 이런 코드는 매번 호출될 때마다 값이 누적된다. JAX에서 같은 패턴을 `jit`으로 감싸면 어떻게 되는지 보자.

```python
import jax
import jax.numpy as jnp


class RunningLoss:
    """PyTorch식으로 self에 누적 상태를 직접 들고 다니는 클래스."""

    def __init__(self):
        self.total = jnp.array(0.0)

    def accumulate(self, loss):
        self.total = self.total + loss  # 부작용: self를 직접 수정한다.
        return self.total


tracker = RunningLoss()
jitted_accumulate = jax.jit(tracker.accumulate)

first = jitted_accumulate(jnp.array(1.0))
second = jitted_accumulate(jnp.array(1.0))
third = jitted_accumulate(jnp.array(1.0))
print(first, second, third)  # 세 번 호출했지만 세 값이 모두 같다.
```

세 번 호출했는데도 `first`, `second`, `third`가 모두 같은 값으로 나오는 이유는 `jit`의 캐싱 방식에 있다. 최초 호출에서 JAX는 `accumulate`의 파이썬 코드를 실제로 한 번 실행하며 트레이싱한다 — 이때 `self.total = self.total + loss`도 실행되어 계산 그래프에 구워지지만, 이후 같은 입력 형태(shape·dtype)로 다시 호출하면 JAX는 파이썬 함수를 다시 실행하지 않고 컴파일된 XLA 프로그램만 재사용한다. 즉 `self.total` 갱신 코드는 두 번째, 세 번째 호출에서 아예 실행되지 않는다. PyTorch의 즉시 실행 모델에서는 상상하기 어려운 이 동작은, JAX 공식 문서가 "부작용이 있는 함수(impure function)"의 대표 사례로 드는 전역 변수 캡처 문제와 근본적으로 같다.

올바른 방법은 상태를 인스턴스 속성이 아니라 함수의 입력과 출력으로 명시적으로 넘기는 것이다. 이는 5장에서 다룬 PRNG 키를 명시적으로 전달하는 원칙과 정확히 같은 이유에서 나온다 — JAX는 "무엇이 바뀌는가"를 함수 시그니처만 보고 알 수 있어야 컴파일러가 안전하게 최적화할 수 있다.

```python
import jax
import jax.numpy as jnp


@jax.jit
def accumulate(total, loss):
    return total + loss


total = jnp.array(0.0)
for loss in (jnp.array(1.0), jnp.array(1.0), jnp.array(1.0)):
    total = accumulate(total, loss)
print(total)  # 1.0 + 1.0 + 1.0 = 3.0으로 정상 누적된다.
```

### 함정 2: 난수 시드를 PyTorch·NumPy처럼 전역으로 취급하기

`torch.randn(3)`이나 `np.random.randn(3)`은 호출할 때마다 내부의 숨겨진 전역 생성기 상태를 바꾸며 서로 다른 값을 반환한다. JAX의 `jax.random.normal`은 순수 함수이므로, 같은 키를 두 번 넘기면 완전히 같은 결과가 나온다.

```python
import jax
import jax.numpy as jnp

key = jax.random.key(0)


def sample_batch(k):
    return jax.random.normal(k, shape=(3,))


print(sample_batch(key))
print(sample_batch(key))  # PyTorch/NumPy 감각으로는 다른 값을 기대하지만, 완전히 같다.
```

두 호출 결과가 같은 이유는 `jax.random.normal`이 키 값만으로 결과가 결정되는 순수 함수이기 때문이다. PyTorch·NumPy의 전역 생성기는 호출될 때마다 내부 상태를 자동으로 전진(advance)시키지만, JAX는 어떤 함수도 암묵적으로 키를 바꾸지 않는다 — 바꾸는 것은 항상 호출자의 몫이다. 이 성질을 모르고 같은 키를 여러 배치, 여러 드롭아웃 마스크에 재사용하면 서로 다른 샘플이어야 할 값들이 전부 동일해지는, 겉으로는 티가 잘 안 나는 재현성 버그가 생긴다.

올바른 방법은 `jax.random.split`으로 키를 매번 새로 나눠 쓰는 것이다.

```python
import jax
import jax.numpy as jnp

key = jax.random.key(0)


def sample_batch(k):
    return jax.random.normal(k, shape=(3,))


key, subkey1 = jax.random.split(key)
print(sample_batch(subkey1))

key, subkey2 = jax.random.split(key)
print(sample_batch(subkey2))  # 서로 다른 subkey를 썼으므로 값도 달라진다.
```

### 함정 3: jit 안에서 Python if를 그대로 써서 재컴파일이 폭증하기

`jit`으로 감싼 함수 안에서 인자 값에 따라 분기하는 Python `if`를 그대로 쓰면 어떻게 될까. 아래 코드는 `step`이 `jit`이 추적하는 값(트레이서)이라서 `TypeError`(`ConcretizationTypeError` 계열)를 낸다 — 트레이서는 구체적인 참/거짓 하나로 접힐 수 없기 때문이다.

```python
import jax
import jax.numpy as jnp


@jax.jit
def scaled_broken(step, x):
    if step % 2 == 0:  # step이 트레이서라서 파이썬 if가 진리값을 못 만든다.
        return x * 2.0
    return x + 1.0


# scaled_broken(jnp.array(0), jnp.ones(3))  # 실행하면 TracerBoolConversionError 계열 예외가 발생한다.
```

이 에러를 본 PyTorch 개발자가 흔히 시도하는 "해결책"은 `static_argnums`로 `step`을 정적 인자로 선언하는 것이다. 이렇게 하면 에러는 사라지지만, 다른 문제가 생긴다.

```python
from functools import partial

import jax
import jax.numpy as jnp


@partial(jax.jit, static_argnums=0)
def scaled_semi_fixed(step, x):
    print(f"tracing for step={step}")  # 실제로 트레이싱될 때만 실행된다.
    if step % 2 == 0:
        return x * 2.0
    return x + 1.0


for step in range(6):
    scaled_semi_fixed(step, jnp.ones(3))
```

`static_argnums=0`은 `step`을 "컴파일된 프로그램에 상수로 박아 넣을 값"으로 취급하라는 뜻이다. 그래서 `if step % 2 == 0:`은 정상 동작하지만, `step`이 서로 다른 값을 가질 때마다 JAX는 완전히 새로운 트레이싱·컴파일을 수행한다. 위 코드를 실행하면 `tracing for step=0`부터 `tracing for step=5`까지 여섯 번 모두 출력된다 — 반복문이 100단계, 1000단계로 늘어나면 그만큼 컴파일 캐시가 불어나는 것이 "재컴파일 폭증"이다. 학습 스텝 번호나 에폭 카운터처럼 매번 값이 바뀌는 변수를 `static_argnums`로 선언하는 것이 이 함정의 전형적인 진입 경로다.

올바른 해법은 `step`을 정적 인자로 만들지 말고, 값에 따른 분기를 `jax.lax.cond`처럼 트레이싱 가능한 제어 흐름 프리미티브로 표현하는 것이다.

```python
import jax
import jax.numpy as jnp


@jax.jit
def scaled_fixed(step, x):
    print("tracing scaled_fixed")  # 최초 한 번만 출력된다.
    return jax.lax.cond(step % 2 == 0, lambda v: v * 2.0, lambda v: v + 1.0, x)


for step in range(6):
    scaled_fixed(jnp.asarray(step), jnp.ones(3))
```

`step`이 이제 `x`와 마찬가지로 트레이싱되는 동적 인자이므로, `scaled_fixed`는 입력 형태가 바뀌지 않는 한 최초 한 번만 컴파일되고 나머지 다섯 번은 캐시된 프로그램을 그대로 재사용한다 — `print` 문이 첫 호출에서만 출력되는 것으로 직접 확인할 수 있다.

## 실행 모델: Eager execution 대 Trace-and-compile

세 함정이 반복해서 드러내는 근본 원인은 두 프레임워크의 실행 모델이 다르다는 사실이다. PyTorch는 <strong>즉시 실행(eager execution)</strong> 모델을 쓴다. `y = a + b`를 쓰면 그 줄이 실행되는 순간 실제 덧셈이 일어나고 결과가 즉시 파이썬 객체로 돌아온다. 디버거를 걸고 한 줄씩 따라가며 중간값을 찍어볼 수 있는 것은 이 모델 덕분이다. JAX는 `jit`으로 감싼 함수에 대해 <strong>트레이스-후-컴파일(trace-and-compile)</strong> 모델을 쓴다. 함수를 처음 호출할 때는 실제 값 대신 추상 트레이서로 한 번 실행해 계산 그래프(jaxpr)를 뽑아내고, 이를 XLA가 대상 하드웨어에 맞는 기계어로 컴파일한다. 이후 같은 입력 형태로 호출되는 모든 실행은 파이썬 인터프리터를 다시 거치지 않고 컴파일된 프로그램을 그대로 돌린다.

```mermaid
flowchart TD
    subgraph pytorch["PyTorch eager execution"]
        p1["연산 1 실행 결과 즉시 반환"] --> p2["연산 2 실행 결과 즉시 반환"]
        p2 --> p3["연산 3 실행 결과 즉시 반환"]
    end
    subgraph jaxFlow["JAX trace-and-compile"]
        j1["최초 호출 함수 트레이싱"] --> j2["XLA 컴파일"]
        j2 --> j3["컴파일된 프로그램 캐시"]
        j3 --> j4["이후 호출 캐시된 프로그램 실행"]
    end
```

이 차이가 성능에 미치는 영향은 두 방향으로 갈린다. 즉시 실행은 연산 하나하나마다 파이썬-C++ 경계를 넘나드는 디스패치 비용을 반복해서 치르지만, 사용자는 매 줄의 결과를 바로 볼 수 있다. 트레이스-후-컴파일은 여러 연산을 하나의 컴파일된 프로그램으로 융합(fusion)해 디스패치 횟수를 줄이고 커널 간 중간 결과를 메모리에 왕복시키지 않을 여지를 컴파일러에 주지만, 그 대가로 최초 호출의 트레이싱·컴파일 비용과 — 함정 3에서 본 것처럼 — 입력 형태가 바뀔 때마다 재컴파일되는 위험을 진다. 어느 쪽이 더 빠른가는 연산의 개수·크기, 반복 횟수, 하드웨어에 따라 달라지므로 이 글에서 구체적인 배수를 단정하지 않는다. 대신 직접 측정할 수 있는 골격 코드를 아래에 둔다.

```python
# benchmark_pytorch.py
import timeit

import torch


def elementwise_chain(x: torch.Tensor) -> torch.Tensor:
    for _ in range(50):
        x = x * 1.0001 + 0.0001
    return x


x = torch.randn(1024, 1024)

eager_time = timeit.timeit(lambda: elementwise_chain(x), number=100)
print(f"PyTorch eager: {eager_time:.4f}s / 100 runs")
# 실제 수치는 CPU/GPU, PyTorch 버전, 텐서 크기에 따라 달라진다.
# 이 코드는 측정 방법의 골격만 제공하며, 특정 배수를 보장하지 않는다.
```

```python
# benchmark_jax.py
import timeit

import jax
import jax.numpy as jnp


def elementwise_chain(x: jax.Array) -> jax.Array:
    for _ in range(50):
        x = x * 1.0001 + 0.0001
    return x


jitted_chain = jax.jit(elementwise_chain)
x = jax.random.normal(jax.random.key(0), (1024, 1024))

# 컴파일 1회를 미리 실행해, 트레이싱·컴파일 비용이 벤치마크 루프에 섞이지 않게 한다.
jitted_chain(x).block_until_ready()

no_jit_time = timeit.timeit(lambda: elementwise_chain(x).block_until_ready(), number=100)
jit_time = timeit.timeit(lambda: jitted_chain(x).block_until_ready(), number=100)

print(f"JAX no-jit: {no_jit_time:.4f}s / JAX jit: {jit_time:.4f}s / 100 runs each")
# 실제 결과는 하드웨어(CPU/GPU/TPU)·JAX 버전·워크로드 크기에 따라 다르다.
```

JAX 벤치마크에서 `.block_until_ready()`를 호출하는 이유는 JAX가 연산을 비동기로 디스패치하기 때문이다 — 이 호출이 없으면 실제 계산이 끝나기 전에 파이썬이 다음 줄로 넘어가 버려, `timeit`이 계산 시간이 아니라 디스패치 시간만 잰다.

## 마이그레이션 판단 기준

두 프레임워크 중 어느 쪽을 택할지는 "더 빠른 쪽"이 아니라 팀의 워크플로와 인프라에 달려 있다. 아래 표는 실무에서 자주 마주치는 상황별 판단 기준이다.

| 상황 | 권장 방향 | 이유 |
|---|---|---|
| 커스텀 미분·배치 벡터화·다중 디바이스 병렬화를 자주 조합해야 하는 연구 코드 | JAX 검토 | `jit`·`grad`·`vmap`·`pmap`이 서로 자유롭게 합성되는 표준 API로 제공된다(00장 참고). |
| TorchServe·ONNX 내보내기 등 PyTorch 전용 배포 파이프라인에 깊이 의존 | PyTorch 유지 또는 학습만 JAX로 분리 | 서빙 생태계 전체를 옮기는 비용이 성능 이득보다 클 수 있다. |
| `torch.autograd.Function`으로 작성한 커스텀 CUDA 커널이 많음 | 단계적 마이그레이션 | XLA 쪽 동등한 커스텀 연산을 새로 작성해야 하므로 전체 재작성보다 점진적 이전이 안전하다. |
| TPU 클러스터에서 대규모 데이터·모델 병렬 학습이 핵심 | JAX 검토 | `pmap`과 TPU 친화적 컴파일 스택이 PyTorch보다 먼저 이 워크로드를 겨냥해 설계됐다. |
| `pdb`·즉석 `print`로 중간값을 자주 찍어보는 빠른 반복 실험 단계 | PyTorch eager 유지 또는 JAX `jit` 없이 프로토타이핑 | 즉시 실행은 매 줄 결과를 바로 보여준다. JAX도 `jit` 없이 실행하거나 `jax.debug.print`로 대응할 수 있지만 기본값은 아니다. |

## 참고 및 출처

- [JAX for PyTorch users — JAX AI Stack](https://docs.jaxstack.ai/en/latest/JAX_for_PyTorch_users.html): `torch.Tensor`/`jax.Array`, `backward()`/`grad`, `device_put` 등 PyTorch↔JAX 대응 관계를 공식적으로 정리한 문서.
- [🔪 JAX - The Sharp Bits 🔪](https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html): `.at[].set()` in-place 갱신, 순수 함수 위반 시 전역 상태가 캡처되는 사례, `jit` 재트레이싱 조건을 다루는 JAX 공식 가이드.
- [Control flow and logical operators with JIT](https://docs.jax.dev/en/latest/control-flow.html): `static_argnums`와 `lax.cond`/`lax.switch`의 트레이드오프를 다루는 공식 문서.
- [jax.random.key — JAX documentation](https://docs.jax.dev/en/latest/_autosummary/jax.random.key.html): 현재 권장되는 타입 키(typed key) API 문서.

## 평가 기준

- `torch.Tensor`·`nn.Module`·`optimizer.step()`이 이번 장의 표 없이도 JAX의 어떤 개념에 대응하는지 설명할 수 있다.
- 클래스 인스턴스 상태를 `jit` 함수 안에서 직접 수정하면 두 번째 호출부터 어떤 값이 반환되는지, 왜 그런지 예측할 수 있다.
- 전역 PRNG 키를 재사용했을 때 어떤 문제가 생기는지, `jax.random.split`으로 어떻게 고치는지 설명할 수 있다.
- `jit` 함수 안에서 트레이서에 Python `if`를 직접 쓰면 왜 에러가 나고, `static_argnums`로 우회했을 때 왜 재컴파일이 늘어나는지 설명할 수 있다.
- eager execution과 trace-and-compile의 차이를 하드웨어 디스패치 관점에서 설명하고, 실제 비교가 필요할 때 `timeit`과 `block_until_ready()`로 어떻게 측정하는지 안다.
- 주어진 PyTorch 프로젝트를 두고 "JAX로 옮길지, 부분만 옮길지, 유지할지"를 팀 인프라·워크플로 기준으로 판단할 수 있다.

## 마무리

이 시리즈는 00장에서 JAX가 조합 가능한 함수 변환·순수 함수형 모델·XLA 컴파일이라는 세 가지 이유로 존재한다는 주장에서 출발했다. 01장의 불변 배열과 함수형 패러다임은 왜 `x[0] = 1`이 아니라 `x.at[0].set(1)`을 써야 하는지의 근거였고, 02장의 `jit`·XLA 컴파일은 이번 장에서 다룬 재컴파일 폭증 함정과 eager 대 trace-and-compile 비교의 토대였다. 03장의 `grad` 자동미분은 `loss.backward()`가 왜 `jax.grad(loss_fn)`이라는 함수 변환으로 바뀌는지를, 04장의 `vmap`·`pmap`은 배치·다중 디바이스 처리를 반복문 없이 표현하는 방법을 보여줬다. 05장의 PRNG 상태 관리는 이번 장 함정 2의 전역 시드 문제를 직접 예고했고, 06장의 Flax·Optax 학습 루프는 이번 장 개념 매핑 표의 `nn.Module`·`optimizer.step()` 행이 실제로 어떤 코드로 구현되는지 보여준 실전 사례였다. 결국 PyTorch에서 JAX로 옮기는 결정은 API 대응표를 외우는 문제가 아니라, 00–06장에서 쌓은 "상태를 명시적으로 넘기고, 컴파일러가 재배치할 여지를 주는" 함수형 사고방식을 실제 코드베이스와 팀의 인프라 제약 위에 놓고 저울질하는 문제다.
