---
collection_order: 1
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[LLM(Series) 01] AI 수학 기초 — 내적, Softmax, KL Divergence"
slug: ai-math-foundations
description: "Attention과 신경망 학습을 이해하는 데 필요한 최소한의 수학을 정리합니다. 벡터 내적과 코사인 유사도, 선형함수와 활성화함수, Softmax·Sigmoid, KL Divergence와 Cross Entropy를 코드와 함께 다룹니다."
tags:
  - LLM(Large Language Model)
  - Transformer
  - Attention(어텐션)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - GPT(Generative Pre-trained Transformer)
  - Embedding(임베딩)
  - PyTorch
  - Data-Science(데이터사이언스)
  - NLP(Natural Language Processing)
  - Self-Attention
  - Fine-Tuning(파인튜닝)
  - Reinforcement-Learning(강화학습)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Advanced
  - Reference(참고)
  - Time-Complexity(시간복잡도)
  - Implementation(구현)
---

Attention 메커니즘의 핵심 연산은 결국 벡터의 내적이고, 신경망 학습의 핵심 연산은 결국 미분과 확률분포 비교입니다. 이 장에서는 이후 챕터에서 반복적으로 등장할 다섯 가지 수학 도구 — 내적과 코사인 유사도, 행렬 곱셈, 선형함수와 활성화함수, 지수·로그함수와 Softmax·Sigmoid, KL Divergence와 Cross Entropy — 를 코드와 함께 최소한으로 정리합니다. 목표는 수학을 증명하는 것이 아니라, 03장 이후 Attention 수식을 봤을 때 "이 부분이 뭘 계산하는지" 막히지 않는 것입니다.

## 벡터의 내적과 코사인 유사도

**벡터(vector)**는 숫자를 순서대로 나열한 것이고, LLM에서는 단어·토큰 하나하나가 수백~수천 차원의 벡터(임베딩)로 표현됩니다. 두 벡터가 "얼마나 비슷한 방향을 가리키는가"를 재는 가장 기본적인 연산이 **내적(dot product)**입니다.

$$\vec{a} \cdot \vec{b} = \sum_i a_i b_i = |\vec{a}||\vec{b}|\cos\theta$$

내적값은 두 벡터의 크기(길이)와 사잇각(θ)에 동시에 영향을 받습니다. 크기 정보를 제거하고 순수하게 방향(의미)만 비교하고 싶다면, 두 벡터를 각각 길이 1인 **단위벡터**로 정규화한 뒤 내적을 계산합니다. 이렇게 정규화된 내적을 **코사인 유사도(cosine similarity)**라고 부르며, 값의 범위는 -1(정반대 방향)부터 1(같은 방향)까지입니다.

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    return dot / norm

king = np.array([0.9, 0.1, 0.4])
queen = np.array([0.85, 0.15, 0.5])
truck = np.array([-0.2, 0.9, -0.3])

print(cosine_similarity(king, queen))  # king·queen: 방향이 비슷 -> 1에 가까움
print(cosine_similarity(king, truck))  # king·truck: 방향이 다름 -> 0에 가까움
```

이 코드에서 `king`과 `queen`의 코사인 유사도가 `king`과 `truck`보다 훨씬 높게 나오는 이유는, 임베딩 공간에서 의미가 가까운 단어일수록 비슷한 방향의 벡터를 갖도록 학습되기 때문입니다. 05장에서 다룰 Self-Attention의 Attention Score도 결국 이 내적 연산을 Query·Key 벡터 사이에 적용한 것입니다.

## 행렬 곱셈과 Transpose

여러 벡터를 한꺼번에 다룰 때는 벡터를 행(row) 또는 열(column)로 쌓은 **행렬(matrix)**을 사용합니다. 행렬 곱셈 $C = AB$는 $A$의 각 행 벡터와 $B$의 각 열 벡터를 내적한 결과로 $C$의 각 원소를 채우는 연산입니다. 이 정의 때문에 $A$가 $(m, k)$ 크기이고 $B$가 $(k, n)$ 크기일 때만 곱셈이 성립하며, 두 행렬의 안쪽 차원($k$)이 일치해야 합니다.

**Transpose(전치, $A^T$)**는 행렬의 행과 열을 서로 바꾸는 연산입니다. 두 행렬을 곱하려는데 안쪽 차원이 맞지 않을 때, 한쪽을 전치해서 차원을 맞추는 용도로 자주 쓰입니다. 05장에서 Attention Score를 계산할 때 $QK^T$처럼 Key 행렬에 전치가 붙는 이유도, Query 행렬 $(n, d_k)$와 Key 행렬 $(n, d_k)$를 그대로 곱할 수 없어서 Key를 $(d_k, n)$으로 전치해 안쪽 차원을 맞추기 때문입니다.

## 선형함수와 활성화함수 — 왜 비선형성이 필요한가

신경망의 한 뉴런이 계산하는 기본 단위는 **선형함수(linear function)**입니다.

$$z = w_1 x_1 + w_2 x_2 + \cdots + b$$

문제는 선형함수만 아무리 깊게 쌓아도 여전히 하나의 선형함수로 축약된다는 것입니다(선형함수의 합성은 선형함수입니다). 즉 선형함수만으로는 직선(또는 평면)으로 나눌 수 없는 복잡한 데이터 분포를 학습할 수 없습니다. 이 한계는 1969년 민스키(Marvin Minsky)와 페퍼트(Seymour Papert)가 단층 퍼셉트론이 XOR 같은 선형 분리 불가능한 문제를 풀 수 없음을 지적하면서 처음 AI 겨울의 원인 중 하나가 되었습니다. 해법은 선형함수 뒤에 비선형 **활성화함수(activation function)**를 붙이는 것입니다 — 이렇게 하면 선형 계산을 아무리 쌓아도 붕괴하지 않고 점점 더 복잡한 함수를 표현할 수 있습니다. 이 때문에 신경망에서는 "선형함수 → 활성화함수"가 항상 한 쌍으로 등장합니다.

## 지수함수·로그함수·Softmax·Sigmoid

지수함수 $e^x$는 신경망에서 두 가지 역할을 합니다. 첫째, 작은 차이를 극적으로 확대합니다 — 점수 10, 8, 1의 차이는 크지 않지만 $e^{10}, e^{8}, e^{1}$로 보내면 차이가 극명하게 벌어집니다. 둘째, 모든 수를 양수로 바꿔줍니다 — 확률처럼 다뤄야 하는 값에서 음수가 나오면 곤란하기 때문입니다. 로그함수는 지수함수의 역연산으로, 곱셈을 덧셈으로 바꿔주어 계산을 안정시키고(언더플로우 방지), 손실(loss) 계산에 널리 쓰입니다.

**Softmax**는 여러 실수 값을 합이 1인 확률 분포로 바꿉니다.

$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

**Sigmoid**는 Softmax를 두 개의 클래스(참/거짓)로 단순화한 특수한 경우로, 값 하나를 0~1 사이의 확률로 변환합니다.

$$\sigma(z) = \frac{1}{1+e^{-z}}$$

| 함수 | 출력 형태 | 용도 |
|---|---|---|
| Softmax | 합이 1인 확률 벡터 | 다음 토큰 예측처럼 여러 후보 중 하나를 고르는 다중 분류 |
| Sigmoid | 0~1 사이 스칼라 | 참/거짓을 판단하는 이진 분류, 게이트(gate) 값 |

## 두 확률분포의 거리 — KL Divergence와 Cross Entropy

모델이 예측한 확률분포 $Q$가 실제 정답 분포 $P$와 얼마나 다른지를 재는 지표가 **KL Divergence(Kullback-Leibler Divergence)**입니다.

$$D_{KL}(P\|Q) = \sum_i P(i) \log\frac{P(i)}{Q(i)} = \underbrace{\sum_i P(i)\log\frac{1}{Q(i)}}_{\text{Cross Entropy}} - \underbrace{\sum_i P(i)\log\frac{1}{P(i)}}_{\text{Entropy}}$$

KL Divergence는 Cross Entropy에서 Entropy(분포 $P$ 자신의 불확실성)를 뺀 값입니다. 정답 분포 $P$는 학습 중 고정되어 있으므로 Entropy 항도 고정되고, 결국 KL Divergence를 줄이는 것과 Cross Entropy를 줄이는 것은 같은 방향의 최적화가 됩니다 — 이것이 분류·언어모델 학습에서 **Cross Entropy Loss**를 손실함수로 쓰는 이유입니다. $-\log(p)$는 "얼마나 놀라운 사건인가"라는 정보량을 의미하기도 합니다 — 일어날 확률이 낮은 사건일수록 $-\log(p)$ 값이 커지므로, 모델이 정답에 낮은 확률을 부여할수록 큰 페널티를 받습니다.

```python
import numpy as np

def cross_entropy(p_true: np.ndarray, q_pred: np.ndarray, eps: float = 1e-12) -> float:
    q_pred = np.clip(q_pred, eps, 1.0)
    return -np.sum(p_true * np.log(q_pred))

target = np.array([0, 1, 0])          # 정답: 2번째 클래스
good_pred = np.array([0.05, 0.9, 0.05])  # 정답에 높은 확률을 준 예측
bad_pred = np.array([0.4, 0.2, 0.4])     # 정답에 낮은 확률을 준 예측

print(cross_entropy(target, good_pred))  # 작은 손실
print(cross_entropy(target, bad_pred))   # 큰 손실
```

`good_pred`처럼 정답 클래스에 높은 확률을 준 예측은 손실이 작고, `bad_pred`처럼 정답을 낮게 평가한 예측은 손실이 큽니다. 이 손실을 줄이는 방향으로 가중치를 갱신하는 과정이 02장에서 다룰 역전파와 경사하강법입니다.

## 흔한 오개념 — "Softmax는 그냥 정규화(normalize)다"

Softmax를 "값들의 합이 1이 되게 나눠주는 정규화"로 이해하는 경우가 많지만, 이는 절반만 맞는 설명입니다. 단순 정규화($z_i / \sum_j z_j$)는 원래 값들의 상대적 비율을 그대로 유지한 채 합만 1로 맞춥니다. 반면 Softmax는 먼저 지수함수를 거치기 때문에, 원래 값들 사이의 작은 차이를 확률 공간에서 훨씬 크게 벌립니다. 예를 들어 점수 `[2, 1, 0]`을 단순 정규화하면 `[0.67, 0.33, 0]`이 되지만, Softmax를 적용하면 `[0.67, 0.24, 0.09]`로 1등과 2등의 격차가 더 크게 벌어집니다. 이 차이 때문에 Softmax는 "가장 그럴듯한 답을 더 확신 있게 고르는" 방향으로 작동하며, 단순 정규화는 이런 성질이 없습니다.

## 언제 내적을, 언제 코사인 유사도를 쓰는가

임베딩 벡터가 이미 단위벡터로 정규화되어 있다면 내적과 코사인 유사도는 같은 값을 냅니다 — 이 경우 정규화 과정을 매번 반복하지 않고 내적만 계산하는 편이 더 빠릅니다. 반대로 벡터의 크기(길이)가 서로 다르고 그 크기 차이가 의미 있는 정보(예: 문서 길이, 등장 빈도)를 담고 있다면, 내적은 그 크기 차이에 영향을 받으므로 방향만 비교하려는 목적에는 코사인 유사도가 더 적합합니다. 05장에서 다룰 Attention Score 계산은 정규화하지 않은 내적($QK^T$)을 그대로 쓰고, 대신 $\sqrt{d_k}$로 나누는 스케일링으로 크기 폭주 문제를 다룹니다.

## 참고 자료

이 장에서 다룬 확률과 정보이론, 수치 계산의 형식적 정의는 다음 자료에서 더 엄밀하게 다룹니다.

> Ian Goodfellow, Yoshua Bengio, Aaron Courville, *Deep Learning*, MIT Press (2016). 3장(확률과 정보이론), 4장(수치 계산)이 이 장의 내용과 대응합니다. 전문은 https://www.deeplearningbook.org/ 에서 무료로 볼 수 있습니다.

다음 장에서는 이 수학 도구들이 실제로 어떻게 쓰이는지, 순전파·역전파·경사하강법으로 이어지는 신경망 학습 과정을 다룹니다.
