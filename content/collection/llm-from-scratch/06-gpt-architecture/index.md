---
collection_order: 6
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[LLM 06] GPT 아키텍처 해부 — 정규화, FFN, Residual, 샘플링"
slug: gpt-architecture-anatomy
description: "Multi-head Attention을 감싸는 GPT 블록의 나머지 구성요소인 LayerNorm, Feed Forward Network, Residual Connection, Dropout을 조립하고, Temperature·Top-K 샘플링으로 다음 토큰을 생성하는 과정을 다룹니다."
tags:
  - LLM(Large Language Model)
  - Transformer
  - GPT(Generative Pre-trained Transformer)
  - Attention(어텐션)
  - Self-Attention
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - NLP(Natural Language Processing)
  - AI(인공지능)
  - PyTorch
  - Embedding(임베딩)
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
  - Prompt-Engineering(프롬프트엔지니어링)
  - ChatGPT
  - Hugging-Face

---

05장에서 만든 Multi-head Attention 하나만으로는 GPT가 되지 않습니다. 실제 GPT 블록은 Attention 앞뒤로 정규화를 두르고, Attention 뒤에 Feed Forward Network를 이어붙이고, 각 서브층의 입력을 출력에 그대로 더하는 Residual Connection으로 감싼 구조입니다. 이 장은 이 나머지 부품들을 하나씩 조립해 완전한 GPT 블록을 완성하고, 마지막으로 이 블록이 만든 확률 분포에서 실제로 다음 토큰을 어떻게 골라내는지까지 다룹니다.

## 정규화 — 학습을 안정시키는 전처리

레이어를 거칠 때마다 값의 분포가 크게 흔들리면 학습이 불안정해집니다. **정규화(Normalization)**는 평균을 0, 분산을 1로 맞춰 이 흔들림을 줄이는 연산으로, Attention과 Feed Forward를 통과하기 전에 각각 적용합니다.

$$\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}, \quad y = \gamma \hat{x} + \beta$$

여기서 $\epsilon$은 분모가 0이 되는 것을 막는 아주 작은 값이고, $\gamma$(스케일)와 $\beta$(시프트)는 정규화를 얼마나 반영할지를 학습 가능한 파라미터로 조정합니다 — 정규화가 항상 옳은 방향은 아니므로, 필요한 만큼만 적용되도록 학습됩니다.

| 방식 | 정규화 기준 | 주로 쓰이는 곳 |
|---|---|---|
| Layer Normalization | 샘플 하나 안에서 피처 전체 | LLM |
| Batch Normalization | 배치 안에서 같은 위치의 피처들 | Vision 모델 |
| RMS Normalization | 평균을 빼는 계산을 생략하고 제곱평균제곱근으로만 나눔 | 최근 LLM(계산량이 적어 선호) |

$$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{n}\sum x_i^2 + \epsilon}} \cdot \gamma$$

## Feed Forward Network와 활성화함수

Feed Forward는 "선형함수 → 활성화함수 → 선형함수"의 단순한 구조입니다. 앞의 선형함수가 차원을 부풀리고(GPT-2 기준 임베딩 차원의 4배로 확장), 활성화함수를 거친 뒤 뒤의 선형함수가 다시 원래 차원으로 축소합니다.

```python
import torch.nn as nn

class FeedForward(nn.Module):
    def __init__(self, emb_dim: int, expansion: int = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(emb_dim, emb_dim * expansion),
            nn.GELU(),
            nn.Linear(emb_dim * expansion, emb_dim),
        )

    def forward(self, x):
        return self.net(x)
```

01장에서 다룬 활성화함수 중 **ReLU**($f(x) = \max(0, x)$)는 단순하고 0보다 큰 구간에서 기울기가 그대로 1이라 레이어를 깊게 쌓기 유리하지만, 0 이하의 입력을 모두 죽여버려 해당 뉴런이 영구히 비활성화되는 "Dying ReLU" 문제가 있습니다. **GELU**는 0 근처에서 완만하게 음수 쪽으로 살짝 내려갔다가 다시 올라오는 부드러운 곡선으로 이 단점을 보완해, 최근 LLM에서 널리 쓰입니다.

## Residual Connection — 입력을 출력에 그대로 더하기

ResNet에서 처음 도입된 이 아이디어는 입력값에 레이어의 출력을 그대로 더해 다음 레이어로 전달합니다.

$$y = x + f(x)$$

레이어를 깊게 쌓았을 때 앞부분의 값이 뒤로 갈수록 흐려지는 문제를 막아주고, 레이어가 "정답을 완전히 새로 만드는" 대신 "입력에서 조금만 바뀌면 되는 값(잔차)"만 학습하면 되므로 학습이 훨씬 쉬워집니다.

## Dropout — 과적합을 막는 무작위 마스킹

학습 중 무작위로 일부 뉴런을 꺼버려서, 모델이 특정 뉴런에 과의존하지 않고 다양한 경로로 학습하게 만드는 기법입니다. 베이스 모델을 사전학습할 때는 데이터가 워낙 방대해 과적합 위험이 낮아 Dropout을 잘 쓰지 않는 경우가 많지만, 08장에서 다룰 것처럼 상대적으로 적은 데이터로 파인튜닝할 때는 과적합 위험이 커지므로 Dropout이 유리해집니다.

## GPT 블록 조립

지금까지의 부품을 하나로 합치면 다음과 같은 GPT 블록이 됩니다.

```python
class GPTBlock(nn.Module):
    def __init__(self, emb_dim: int, n_heads: int, drop_rate: float = 0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(emb_dim)
        self.attn = MultiHeadAttention(emb_dim, n_heads)   # 05장에서 구현
        self.norm2 = nn.LayerNorm(emb_dim)
        self.ffn = FeedForward(emb_dim)
        self.dropout = nn.Dropout(drop_rate)

    def forward(self, x):
        x = x + self.dropout(self.attn(self.norm1(x)))    # Attention + Residual
        x = x + self.dropout(self.ffn(self.norm2(x)))     # FFN + Residual
        return x
```

GPT-2 124M 기준 설정값은 `vocab_size=50257`, `context_length=1024`, `emb_dim=768`, `n_heads=12`, `n_layers=12`입니다. 전체 흐름은 토큰 임베딩 + 위치 임베딩 → Dropout → `GPTBlock` 12개 반복 → 최종 LayerNorm → 출력층 `Linear(768 → 50257)` 순서입니다. 잔차 연결이 있는 구간은 입력과 출력의 차원이 반드시 같아야 하고, **마지막 출력층에서만** 임베딩 차원이 어휘 사전 크기로 바뀝니다.

## 다음 토큰 생성 — Temperature와 Top-K

마지막 선형층을 통과한 값(logits)을 Softmax에 넣으면 다음 토큰의 확률 분포가 나옵니다. 매번 가장 확률이 높은 토큰만 뽑으면 같은 입력에 항상 같은 출력이 나와 다양성이 사라지므로, 두 파라미터로 확률 분포의 모양을 조절합니다.

**Temperature**는 Softmax 계산 전에 logit을 온도값 $T$로 나눕니다.

$$\text{softmax}(z_i / T) = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}}$$

$T$를 낮추면 분포가 뾰족해져 결정적인 출력에 가까워지고, $T$를 높이면 분포가 평평해져 다양한 표현이 나올 확률이 높아집니다. **Top-K 샘플링**은 확률이 높은 순서로 K개만 남기고 나머지를 $-\infty$로 마스킹한 뒤 Softmax를 적용합니다. **Top-P(nucleus) 샘플링**은 확률 누적 합이 특정 비율(예: 90%)을 넘을 때까지만 후보로 남기는 방식입니다.

```python
def sample_next_token(logits: torch.Tensor, temperature: float = 1.0, top_k: int = 50) -> torch.Tensor:
    logits = logits / temperature
    top_values, top_indices = torch.topk(logits, top_k)
    probs = F.softmax(top_values, dim=-1)
    chosen = torch.multinomial(probs, num_samples=1)
    return top_indices.gather(-1, chosen)
```

Hugging Face에 공개된 모델은 제작자가 권장하는 Temperature·Top-K·Top-P 값을 함께 공개하는 경우가 많고, 추론(reasoning)이 중요한 작업과 일반 대화 작업에 서로 다른 권장값이 제시되기도 합니다.

## 흔한 오개념 — "Temperature를 0으로 두면 가장 똑똑한 답이 나온다"

Temperature를 0에 가깝게 낮추면 모델이 항상 가장 확률 높은 토큰만 결정적으로 선택하게 되지만, 이것이 "가장 똑똑한 답"을 보장하지는 않습니다. 언어모델의 확률 분포는 한 토큰씩 순차적으로 결정되므로, 매 순간 가장 그럴듯한 토큰만 고르는 탐욕적(greedy) 선택이 문장 전체로 보면 반복적이거나 지역적으로 최적인 답에 갇히는 경우가 많습니다. 창의적 생성에는 적당히 높은 Temperature나 Top-P가, 사실 기반 응답이나 코드 생성처럼 일관성이 중요한 작업에는 낮은 Temperature가 유리하다는 식으로 **과제 성격에 맞춰 선택하는 것**이 정확한 접근입니다.

다음 장에서는 이렇게 완성된 GPT 블록 안에서, 특히 파라미터의 약 3분의 2를 차지하는 Feed Forward Network가 실제로 어떻게 지식을 저장하는지를 다룹니다.
