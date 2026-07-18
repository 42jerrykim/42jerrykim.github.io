---
collection_order: 2
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[LLM] 02. 신경망은 어떻게 학습하는가 — 역전파와 Adam"
slug: neural-network-training
description: "순전파·손실 계산·역전파로 이어지는 신경망 학습 과정을 Chain Rule과 경사하강법 관점에서 정리합니다. Local Minimum 문제를 보완하는 Adam Optimizer, Batch Size·Epoch·Step 개념을 코드와 함께 다룹니다."
tags:
  - LLM(Large Language Model)
  - Transformer
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - GPT(Generative Pre-trained Transformer)
  - PyTorch
  - Data-Science(데이터사이언스)
  - NLP(Natural Language Processing)
  - Fine-Tuning(파인튜닝)
  - Reinforcement-Learning(강화학습)
  - Attention(어텐션)
  - Embedding(임베딩)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Advanced
  - Reference(참고)
  - Implementation(구현)
  - Best-Practices
  - Time-Complexity(시간복잡도)
  - Prompt-Engineering(프롬프트엔지니어링)

---

01장에서 정리한 Softmax와 Cross Entropy는 "모델의 예측이 정답과 얼마나 다른가"를 숫자 하나로 표현하는 도구였습니다. 이 장은 그 숫자(손실, loss)를 어떻게 줄여나가는지, 즉 신경망이 실제로 "학습"한다는 것이 계산 단계에서 무엇을 의미하는지를 다룹니다. 이 과정을 이해하면 이후 08~11장에서 다루는 파인튜닝·RLHF·DPO가 결국 "손실함수를 무엇으로 정의하고 어떤 데이터로 최적화하는가"의 변형이라는 것이 보입니다.

## 학습의 세 단계 — 순전파, 손실 계산, 역전파

신경망 학습은 하나의 배치(batch) 데이터에 대해 다음 세 단계를 반복합니다. 첫째, **순전파(forward pass)**로 입력에서 출력까지 계산을 진행합니다 — 예를 들어 $z_1 = x_1 w_1 + x_2 w_2 + b$, $h_1 = \sigma(z_1)$처럼 레이어를 하나씩 통과합니다. 둘째, 출력과 정답을 비교해 **손실(loss)**을 계산합니다. 셋째, 손실을 줄이는 방향으로 각 가중치를 얼마나 바꿔야 하는지를 **역전파(backpropagation)**로 계산합니다. 이 세 단계가 데이터셋을 여러 번 훑으며 반복되는 것이 학습입니다.

손실 함수는 과제에 따라 다르게 선택됩니다. 회귀(연속값 예측)에는 평균제곱오차(MSE)를 흔히 쓰고,

$$L_{MSE} = \frac{1}{n}\sum (y_{pred} - y_{true})^2$$

분류(다음 토큰 예측 포함)에는 01장에서 다룬 Cross Entropy를 씁니다. 언어모델의 사전학습(Pretraining)은 "다음 토큰이 무엇인가"를 맞히는 다중 분류 문제이므로, GPT류 모델은 거의 예외 없이 Cross Entropy Loss로 학습됩니다.

## Backpropagation과 Chain Rule

역전파의 핵심은 **연쇄법칙(Chain Rule)**입니다. 어떤 가중치 $w_5$가 손실 $L$에 미치는 영향을 알고 싶다면, $w_5$에서 $L$까지 이어지는 계산 경로의 각 단계별 미분값을 모두 곱하면 됩니다.

$$\frac{\partial L}{\partial w_5} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z_3} \cdot \frac{\partial z_3}{\partial w_5}$$

이는 "치타가 사자보다 2배 빠르고, 사자가 공보다 2배 빠르고, 공이 사람보다 1.5배 빠르면 치타는 사람보다 몇 배 빠른가?"라는 질문과 같은 구조입니다 — 답은 각 비율을 그대로 곱한 $2 \times 2 \times 1.5 = 6$입니다. 신경망도 출력에서 입력 방향으로 층을 거슬러 올라가며 각 층의 미분값을 곱해 나가고, 이렇게 계산한 기울기(gradient)로 가중치를 갱신하는 것이 **경사하강법(Gradient Descent)**입니다.

$$w \leftarrow w - \alpha \frac{\partial L}{\partial w}$$

여기서 학습률 $\alpha$(learning rate)는 보통 $10^{-4} \sim 10^{-5}$처럼 작은 값을 씁니다. 한 걸음씩 내려가면서 방향(기울기의 부호)을 계속 확인해야 하므로, 너무 큰 걸음은 손실이 줄어드는 지점을 지나쳐버릴 위험이 있습니다.

## Local Minimum과 Adam Optimizer

단순 경사하강법은 손실 함수의 표면이 울퉁불퉁할 때 진짜 최저점(global minimum)이 아닌 **지역 최저점(local minimum)**에 갇히거나, 평평한 구간(plateau)에서 학습이 멈춘 것처럼 느려지는 문제가 있습니다. 이를 보완하기 위해 실무에서는 단순 경사하강법 대신 **Adam(Adaptive Moment Estimation)** 옵티마이저를 기본값으로 씁니다.

> Diederik P. Kingma, Jimmy Ba, "Adam: A Method for Stochastic Optimization", *arXiv:1412.6980* (2014, ICLR 2015 발표)

Adam은 과거 기울기의 방향을 누적한 **모멘텀(momentum)**과, 파라미터마다 학습률을 다르게 조정하는 **적응적 학습률(adaptive learning rate)**을 결합합니다. 모멘텀은 공이 언덕을 굴러 내려가듯 이전 방향의 관성을 유지해 평평한 구간을 더 빠르게 통과하게 하고, 적응적 학습률은 자주 갱신되는 파라미터는 걸음을 줄이고 드물게 갱신되는 파라미터는 걸음을 키워 균형을 맞춥니다. 대부분의 LLM 사전학습·파인튜닝은 Adam 또는 그 변형인 AdamW를 기본 옵티마이저로 사용합니다.

```python
import torch
import torch.nn as nn

model = nn.Linear(768, 768)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
loss_fn = nn.CrossEntropyLoss()

x = torch.randn(8, 768)          # 배치 크기 8
target = torch.randint(0, 768, (8,))

optimizer.zero_grad()             # 이전 스텝의 기울기 초기화
output = model(x)                 # 순전파
loss = loss_fn(output, target)    # 손실 계산
loss.backward()                   # 역전파 - 각 파라미터의 기울기 계산
optimizer.step()                  # Adam 규칙으로 가중치 갱신
```

`optimizer.zero_grad()`를 빼먹으면 이전 스텝에서 계산된 기울기가 누적되어 엉뚱한 방향으로 갱신되는 흔한 실수가 발생합니다. `loss.backward()`가 Chain Rule을 자동으로 적용해 모든 파라미터의 기울기를 계산하고, `optimizer.step()`이 그 기울기를 Adam 규칙에 따라 가중치에 반영합니다.

## Batch Size, Epoch, Step

전체 학습 데이터를 한 번에 모델에 넣지 않는 이유는 메모리 제약과 학습 안정성 때문입니다. 대신 데이터를 작은 묶음으로 나눠 순차적으로 학습하며, 이때 쓰이는 세 용어를 구분해야 합니다.

| 용어 | 의미 |
|---|---|
| Batch Size | 한 번의 순전파·역전파에 사용하는 데이터 샘플 개수 |
| Step(Iteration) | 배치 하나를 처리하고 가중치를 한 번 갱신하는 단위 |
| Epoch | 전체 데이터셋을 한 번 다 훑는 단위 (= 데이터 수 ÷ Batch Size 번의 Step) |

Batch Size가 클수록 기울기 추정이 안정적이지만 GPU 메모리를 많이 쓰고, 작을수록 메모리는 절약되지만 기울기 추정이 노이즈에 더 민감해집니다. 이 트레이드오프는 07장 이후 파인튜닝을 실습할 때 "왜 배치 크기를 줄이면 학습률도 함께 조정해야 하는가"라는 질문으로 다시 등장합니다.

## 흔한 오개념 — "학습률을 낮추면 항상 더 정확한 모델이 나온다"

학습률을 낮추면 한 걸음의 보폭이 작아지므로 더 정밀하게 최저점에 다가갈 것 같지만, 실제로는 지역 최저점이나 평평한 구간에 갇혀 학습이 사실상 멈추는 위험이 커집니다. 반대로 학습률이 너무 크면 손실이 줄어드는 지점을 계속 지나쳐 진동하거나 발산합니다. 그래서 실무에서는 학습률을 고정하지 않고, 초반에는 크게 시작했다가 점차 줄이는 **학습률 스케줄링(learning rate scheduling)**이나, Adam처럼 파라미터별로 학습률을 자동 조정하는 옵티마이저를 함께 사용합니다. "낮을수록 좋다"가 아니라 "학습 단계와 데이터 규모에 맞는 값이 따로 있다"가 정확한 이해입니다.

## 참고 자료

Chain Rule과 경사하강법의 수학적 배경은 01장에서 인용한 자료의 연장선에 있습니다.

> Ian Goodfellow, Yoshua Bengio, Aaron Courville, *Deep Learning*, MIT Press (2016), 6장(Deep Feedforward Networks)·8장(Optimization for Training Deep Models). https://www.deeplearningbook.org/

다음 장에서는 이렇게 학습되는 신경망이 왜 RNN 구조에서 Transformer 구조로 옮겨가야 했는지, 언어모델 아키텍처의 진화 과정을 다룹니다.
