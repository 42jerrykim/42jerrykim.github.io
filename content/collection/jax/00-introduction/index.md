---
collection_order: 0
date: 2026-08-30
lastmod: 2026-08-30
draft: false
title: "[JAX] 00. Introduction: JAX 실전 가이드"
slug: getting-started-jax
description: "NumPy 호환 배열에 자동미분과 XLA 컴파일을 결합한 JAX를 다루는 시리즈의 도입 챕터입니다. JAX가 존재하는 세 가지 이유부터 jit·grad·vmap·pmap을 아우르는 8개 챕터 커리큘럼, 학습 목표, PyTorch와의 관계까지 자세히 정리합니다."
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
  - Curriculum(커리큘럼)
  - Roadmap(로드맵)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Advanced
  - Case-Study

image: "wordcloud.png"
---

NumPy로 짠 함수 앞뒤에 딱 두 줄만 추가하면 — `jax.jit`으로 감싸고 `jax.grad`를 호출하면 — 같은 코드가 GPU·TPU에서 컴파일되어 실행되고, 별도의 역전파 코드 없이 기울기가 계산됩니다. Google DeepMind는 이 특성 위에서 <strong>AlphaFold 2</strong>의 추론 코드를 JAX와 Haiku로 공개했고, Google은 <strong>PaLM</strong>을 JAX와 Pathways 스택으로 TPU 포드에서 학습시켰다고 공식 논문에서 밝혔습니다(Chowdhery et al., "PaLM: Scaling Language Modeling with Pathways", 2022). 이후의 Gemini 계열 모델도 같은 JAX 기반 인프라 위에서 이어졌습니다. 이 시리즈는 "왜 PyTorch가 있는데 JAX가 필요한가"라는 질문에서 출발해, NumPy 호환 배열이 어떻게 자동미분·컴파일·병렬화까지 확장되는지를 실전 코드로 따라갑니다.

## JAX가 존재하는 세 가지 이유

JAX가 처음 등장한 논문은 스스로를 "고수준 트레이싱을 통해 머신러닝 프로그램을 컴파일하는 시스템"으로 소개합니다. 이 소개가 가리키는 존재 이유는 크게 세 가지입니다.

첫째, <strong>조합 가능한 함수 변환(Composable transforms)</strong>입니다. JAX는 `jit`(컴파일), `grad`(미분), `vmap`(벡터화), `pmap`(다중 디바이스 병렬화)을 서로 자유롭게 합성할 수 있는 순수 함수로 제공합니다. `jax.jit(jax.grad(jax.vmap(f)))`처럼 변환을 겹쳐 쓸 수 있다는 것은, "배치 처리된 함수의 기울기를 컴파일해서 실행"이라는 조합이 각 변환을 개별적으로 구현할 필요 없이 자동으로 성립한다는 뜻입니다. NumPy에는 애초에 자동미분이 없고, PyTorch의 즉시 실행(eager execution) 모델은 `torch.compile`이 나오기 전까지 이런 조합을 컴파일러 수준에서 최적화하지 못했습니다.

둘째, <strong>순수 함수형 프로그래밍 모델(Pure functional programming)</strong>입니다. JAX 배열은 불변(immutable)이고, JAX가 변환할 함수는 부작용(side effect)이 없는 순수 함수여야 합니다. 이 제약은 처음에는 불편하게 느껴지지만 — 전역 상태를 읽거나 쓰는 함수, 리스트에 값을 추가하는 함수는 `jit`이 다르게 동작합니다 — 그 대가로 컴파일러가 실행 순서를 재배치하고 여러 디바이스에 안전하게 분산시킬 수 있는 근거를 얻습니다. 함수형 모델이 왜 필요한지는 이 시리즈 전체를 관통하는 주제이며, 1장에서 본격적으로 다룹니다.

셋째, <strong>XLA를 통한 하드웨어 독립적 컴파일</strong>입니다. JAX 코드는 XLA(Accelerated Linear Algebra) 컴파일러가 이해하는 중간 표현으로 변환되고, 이 표현은 CPU·GPU·TPU 어디서든 같은 소스 코드로 실행됩니다. TPU는 원래 TensorFlow 전용에 가까웠지만, JAX는 TPU를 NumPy 문법 그대로 다룰 수 있는 통로를 열었습니다.

> Roy Frostig, Matthew James Johnson, Chris Leary, "Compiling machine learning programs via high-level tracing", *SysML 2018* — JAX를 처음 공개한 논문으로, 이 논문에서 다룬 자동미분·XLA 컴파일 기능이 2018년 12월 [google/jax](https://github.com/jax-ml/jax) 오픈소스 공개로 이어졌습니다. 프로젝트 README는 스스로를 "Autograd와 XLA를 하나로 합친 것(Autograd and XLA, brought together)"이라고 요약합니다.

## 이 시리즈가 다루는 범위

이 시리즈는 JAX의 핵심 변환 함수(`jit`, `grad`, `vmap`, `pmap`)를 순서대로 익히고, 이를 실제 신경망 학습 코드로 연결한 뒤, 기존 PyTorch 코드베이스를 옮기는 실전 가이드로 마무리합니다. XLA 컴파일러 내부의 HLO(High-Level Operations) 최적화 패스나, PaLM급 모델 학습에 쓰이는 Pathways 분산 인프라처럼 JAX 바깥의 시스템은 범위 밖입니다 — 이는 최적화(Optimization) 시리즈의 컴파일러·동시성 챕터, 그리고 LLM 밑바닥부터 이해하기 시리즈와 맞닿아 있는 별개의 주제입니다. NumPy 배열 연산 자체에 익숙하지 않다면 Python 컬렉션을 먼저 참고하는 것을 권장합니다.

시작하기 전에 두 가지 흔한 오해를 짚고 넘어갈 필요가 있습니다. 하나는 "JAX는 GPU·TPU에서 더 빠르게 도는 NumPy일 뿐"이라는 생각인데, 실제로는 `jit`이 함수를 XLA 그래프로 컴파일해 연산 융합·메모리 재사용까지 최적화하므로 속도 차이는 하드웨어가 아니라 컴파일러가 만듭니다 — 02장에서 이 컴파일 과정 자체를 다룹니다. 다른 하나는 "PyTorch 코드를 거의 그대로 옮기면 JAX에서도 동작할 것"이라는 기대인데, PyTorch의 `nn.Module`은 파라미터를 객체 내부 상태로 들고 있는 반면 JAX가 변환할 함수는 부작용 없는 순수 함수여야 하므로 이 가정은 마이그레이션 초기 단계에서 대부분 깨집니다 — 07장이 이 간극을 메우는 구체적인 절차를 다룹니다.

## 커리큘럼

| 챕터 | 제목 | 핵심 질문 |
|---|---|---|
| 01 | NumPy와 함수형 패러다임 | 왜 배열을 제자리에서 바꿔 쓸 수 없는가 |
| 02 | jit과 XLA 컴파일 | 파이썬 함수가 어떻게 하드웨어 독립적 기계어로 바뀌는가 |
| 03 | grad: 자동미분 | 코드를 실행하지 않고도 기울기를 어떻게 계산하는가 |
| 04 | vmap과 pmap: 벡터화·병렬화 | 반복문 없이 배치 처리와 다중 디바이스를 어떻게 다루는가 |
| 05 | PRNG와 상태 관리 | 전역 난수 상태 없이 재현 가능한 무작위성을 어떻게 얻는가 |
| 06 | Flax·Optax로 신경망 실전 | 함수형 원칙 위에서 실제 모델을 어떻게 학습시키는가 |
| 07 | PyTorch에서 마이그레이션 | 기존 PyTorch 코드베이스를 옮길 때 무엇부터 바꿔야 하는가 |

01–03장은 JAX의 세 가지 핵심 변환(NumPy 호환, 컴파일, 미분)을 하나씩 익히고, 04–05장은 그 변환을 배치·다중 디바이스·무작위성이라는 실전 요구사항에 적용합니다. 06장은 여기까지 쌓은 개념으로 실제 신경망을 학습시키고, 07장은 PyTorch 경험자가 이 모든 개념을 기존 지식에 매핑하도록 돕습니다. 이 순서를 따르는 이유는 06장의 Flax·Optax 학습 루프가 01–05장에서 다지는 불변성·컴파일·미분·PRNG 처리 방식을 그대로 전제하기 때문입니다. NumPy와 자동미분 개념에 이미 익숙하다면 01장을 건너뛰고 02장부터 시작해도 무리가 없습니다.

```mermaid
flowchart LR
    ch01["01 NumPy·함수형"] --> ch02["02 jit·XLA"]
    ch02 --> ch03["03 grad 자동미분"]
    ch03 --> ch04["04 vmap·pmap"]
    ch04 --> ch05["05 PRNG·상태"]
    ch05 --> ch06["06 Flax·Optax"]
    ch06 --> ch07["07 PyTorch 마이그레이션"]
```

## 학습 결과

이 시리즈를 완주하면 "이 함수가 왜 예상보다 자주 재컴파일되는가", "이 함수에 `grad`가 통하지 않는 이유가 부작용 때문인가", "배치 차원을 직접 다룰지 `vmap`에 맡길지", "PyTorch 코드를 JAX로 옮길 때 `nn.Module`과 `optimizer.step()`을 무엇으로 바꿔야 하는가"를 스스로 판단할 수 있게 됩니다. 이는 실무에서 JAX 기반 연구 코드를 읽거나, 대규모 학습 파이프라인의 컴파일 병목을 진단하거나, 기존 PyTorch 프로젝트의 일부를 JAX로 이전할지 결정하는 구체적인 역량으로 이어집니다.

다음 장에서는 JAX 배열이 NumPy 배열과 어떻게 다른지, 그리고 왜 JAX가 변환 대상 함수에 순수성을 요구하는지를 다룹니다.
