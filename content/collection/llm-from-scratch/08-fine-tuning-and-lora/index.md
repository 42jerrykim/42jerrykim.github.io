---
collection_order: 8
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[LLM] 08. 파인튜닝 실전 — Classification Fine-tuning과 LoRA"
slug: fine-tuning-and-lora
description: "사전학습된 GPT를 특정 과제에 맞추는 Classification Fine-tuning과, 전체 가중치 대신 저차원 행렬만 학습하는 LoRA·QLoRA를 다룹니다. 왜 파인튜닝마다 다른 전략이 필요한지 데이터 규모 관점에서 설명합니다."
tags:
  - LLM(Large Language Model)
  - Fine-Tuning(파인튜닝)
  - LoRA(Low-Rank Adaptation)
  - Transformer
  - GPT(Generative Pre-trained Transformer)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - NLP(Natural Language Processing)
  - AI(인공지능)
  - PyTorch
  - Hugging-Face
  - Data-Science(데이터사이언스)
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
  - Model-Compression(모델경량화)
  - Prompt-Engineering(프롬프트엔지니어링)
  - ChatGPT

image: "wordcloud.png"
---

07장까지 만든 GPT는 "다음 토큰을 예측"할 뿐, 스팸 메일을 분류하거나 특정 형식으로 답하는 등 구체적인 과제를 수행하도록 만들어지지는 않았습니다. <strong>파인튜닝(Fine-tuning)</strong>은 이렇게 사전학습된 베이스 모델을 특정 목적에 맞게 추가로 학습시키는 과정입니다. 이 장은 가장 단순한 형태인 Classification Fine-tuning에서 시작해, 전체 가중치를 건드리지 않고도 모델을 조정할 수 있는 LoRA로 넘어갑니다.

## Classification Fine-tuning — 출력층만 새로 붙이기

<strong>분류 미세튜닝(Classification Fine-tuning)</strong>의 핵심은 GPT의 마지막 출력층을 바꿔치기하는 것입니다. 원래 GPT의 출력층은 `Linear(emb_dim → vocab_size)`로 다음 토큰의 확률 분포를 만들지만, 분류 과제에서는 이 층을 `Linear(emb_dim → num_classes)`로 교체해 "스팸/정상"처럼 정해진 클래스 중 하나를 고르도록 만듭니다.

```python
import torch.nn as nn

class GPTForClassification(nn.Module):
    def __init__(self, gpt_backbone: nn.Module, emb_dim: int, num_classes: int):
        super().__init__()
        self.backbone = gpt_backbone          # 06장에서 만든 GPT 블록들 (사전학습된 가중치)
        self.classifier = nn.Linear(emb_dim, num_classes)

    def forward(self, x):
        hidden = self.backbone(x)              # (batch, seq_len, emb_dim)
        last_token_hidden = hidden[:, -1, :]    # 마지막 토큰의 표현만 사용
        return self.classifier(last_token_hidden)
```

`backbone`은 사전학습으로 언어의 구조와 상식을 이미 익힌 상태이므로, 새로 추가한 `classifier`만 (또는 backbone의 일부 상위 레이어까지 함께) 소량의 라벨링된 데이터로 학습시키면 됩니다. 이것이 "밑바닥부터 분류기를 학습하는 것"보다 훨씬 적은 데이터로 좋은 성능을 내는 이유입니다.

## LoRA — 전체 가중치 대신 저차원 행렬만 학습하기

모델이 커질수록 모든 가중치를 파인튜닝(Full Fine-tuning)하는 데 드는 메모리와 시간이 감당하기 어려워집니다. <strong>LoRA(Low-Rank Adaptation)</strong>는 기존 가중치 행렬 $W$를 얼려둔(freeze) 채, 그 옆에 훨씬 작은 두 행렬 $A$, $B$의 곱만 학습시켜 가중치 변화량을 근사하는 방법입니다.

$$W' = W + \Delta W = W + BA$$

> Edward J. Hu, Yelong Shen, Phillip Wallis 외, "LoRA: Low-Rank Adaptation of Large Language Models", *arXiv:2106.09685* (2021)

여기서 $W$가 $(d, d)$ 크기라면, $A$는 $(r, d)$, $B$는 $(d, r)$ 크기이고 $r$(rank)은 $d$보다 훨씬 작은 값(예: 4–64)입니다. 학습해야 할 파라미터 수가 $d^2$에서 $2rd$로 줄어들기 때문에, $r$이 작을수록 학습 비용은 급격히 줄어듭니다. 원 논문은 이 방식이 GPT-3 규모 모델에서도 Full Fine-tuning과 비슷한 성능을 내면서 학습 가능한 파라미터 수는 수천 분의 1로 줄일 수 있음을 보였습니다.

```python
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, base_layer: nn.Linear, rank: int = 8, alpha: float = 16.0):
        super().__init__()
        self.base_layer = base_layer
        for param in self.base_layer.parameters():
            param.requires_grad = False        # 원래 가중치는 얼려둔다

        in_dim, out_dim = base_layer.in_features, base_layer.out_features
        self.lora_A = nn.Parameter(torch.randn(rank, in_dim) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_dim, rank))
        self.scale = alpha / rank

    def forward(self, x):
        base_out = self.base_layer(x)
        lora_out = x @ self.lora_A.T @ self.lora_B.T
        return base_out + self.scale * lora_out
```

`lora_B`를 0으로 초기화하는 이유는, 학습을 시작하는 시점에는 `lora_A @ lora_B`가 0이 되어 원래 모델의 동작을 그대로 유지한 채 학습이 진행되도록 하기 위해서입니다. `self.scale`(alpha/rank)은 LoRA로 추가된 변화량이 원래 출력에 얼마나 강하게 반영될지를 조정하는 계수입니다.

## QLoRA와 BF16 — 메모리를 더 아끼기

**QLoRA**는 LoRA의 아이디어에 양자화(Quantization)를 결합해, 얼려둔 원본 가중치 $W$를 4비트 같은 저정밀도로 저장하고 학습 가능한 $A$, $B$ 행렬만 16비트로 유지하는 방식입니다. 이렇게 하면 원본 모델을 GPU 메모리에 올리는 비용 자체가 크게 줄어들어, 소비자용 GPU 한 장으로도 수십억 파라미터 모델을 파인튜닝할 수 있게 됩니다. 이 시리즈의 양자화 원리 자체는 별도의 On-Device AI 경량화 시리즈에서 더 깊이 다루므로, 여기서는 LoRA와 결합되는 지점만 짚습니다. <strong>BF16(bfloat16)</strong>은 일반적인 16비트 부동소수점(FP16)과 달리 지수(exponent) 비트를 32비트 부동소수점과 동일하게 유지해, 정밀도는 다소 낮아지더라도 값의 범위(overflow에 강한 정도)는 유지하는 절충안으로, 최근 LLM 학습에서 기본값처럼 쓰입니다.

## 언제 Full Fine-tuning, 언제 LoRA를 쓰는가

| 상황 | 권장 방식 | 이유 |
|---|---|---|
| 라벨 데이터가 매우 많고, 모델을 근본적으로 다른 도메인에 적응시켜야 함 | Full Fine-tuning | 모든 가중치를 조정할 여지가 필요 |
| 라벨 데이터가 제한적이고, 특정 스타일·형식만 조정하면 됨 | LoRA | 적은 데이터로도 과적합 없이 조정 가능 |
| GPU 메모리가 제한적(개인 GPU, 다중 모델 서빙) | QLoRA | 원본 가중치를 저정밀도로 유지해 메모리 절약 |
| 여러 과제를 하나의 베이스 모델로 서빙해야 함 | LoRA(어댑터 교체) | 과제별로 작은 $A$, $B$ 행렬만 교체하면 됨 |

## 흔한 오개념 — "LoRA는 성능을 어느 정도 포기하는 대신 속도를 얻는 기법이다"

LoRA를 "가벼운 대신 성능이 떨어지는 타협안"으로 오해하기 쉽지만, 원 논문의 실험 결과는 적절한 rank를 선택했을 때 여러 벤치마크에서 Full Fine-tuning과 동등하거나 오히려 더 나은 성능을 보였습니다. 그 이유는 파인튜닝 과정에서 실제로 필요한 가중치 변화량 $\Delta W$가 원래 가중치 행렬의 차원보다 훨씬 낮은 랭크(low-rank) 구조를 갖는 경향이 있기 때문입니다 — 즉 대부분의 파인튜닝 과제는 애초에 전체 파라미터 공간을 다 쓸 필요가 없다는 것이 LoRA가 성립하는 근거입니다. 다만 이는 "적은 데이터로 기존 능력을 조금 조정하는" 상황에 해당하는 것이고, 모델에게 완전히 새로운 지식 체계를 통째로 주입해야 하는 극단적인 경우에는 Full Fine-tuning이 여전히 필요할 수 있습니다.

다음 장에서는 분류가 아니라 "지시를 따르는" 능력 자체를 학습시키는 지시 미세튜닝을, 프롬프트 포맷과 손실 계산에서 정답이 아닌 부분을 제외하는 마스킹 기법 중심으로 다룹니다.
