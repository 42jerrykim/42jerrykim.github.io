---
collection_order: 5
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[LLM 05] Self-Attention 완전분해 — Q, K, V부터 Multi-head까지"
slug: self-attention-explained
description: "Query, Key, Value로 나누는 이유부터 Scaled Dot-Product Attention, Causal Masking, Multi-head Attention까지 Self-Attention의 계산 과정을 수식과 PyTorch 코드로 분해합니다."
tags:
  - LLM(Large Language Model)
  - Transformer
  - Attention(어텐션)
  - Self-Attention
  - GPT(Generative Pre-trained Transformer)
  - BERT
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
  - Time-Complexity(시간복잡도)
---

같은 단어라도 문맥에 따라 뜻이 달라집니다. `an apple and orange`에서는 오렌지를 주목해 "사과(과일)"라는 뜻이 강해지고, `apple phone`에서는 phone을 주목해 "브랜드 애플"이라는 뜻이 강해집니다. **Attention**은 이렇게 "주변 단어로부터 몇 %씩 의미를 가져와 현재 단어의 진짜 의미를 결정하는" 계산입니다. 이 장은 04장에서 만든 입력 임베딩이 Attention을 거치며 어떤 계산을 통과하는지, Query·Key·Value 세 벡터로 쪼개는 이유부터 시작해 끝까지 분해합니다.

## 왜 Query, Key, Value로 나누는가

Self-Attention을 계산할 때는 입력 벡터를 그대로 쓰지 않고, 학습 가능한 세 개의 가중치 행렬을 곱해 **Query(Q)**, **Key(K)**, **Value(V)** 세 가지로 변환합니다. Query는 "내가 무엇을 알고 싶은가"를 나타내는 질문 벡터이고, Key는 "나는 어떤 정보를 갖고 있는가"를 나타내는 색인 벡터이며, Value는 실제로 전달할 내용물입니다.

이 세 가지를 굳이 나누는 이유는 두 가지 문제를 피하기 위해서입니다. 첫째, Q와 K를 나누지 않고 같은 벡터로 내적을 계산하면 항상 자기 자신과의 내적이 가장 크게 나옵니다(자기 자신이 자기 자신과 가장 유사하므로). 게다가 내적은 순서를 바꿔도 같은 값이 나오는 대칭 연산이라, `Tom ate the dog`과 `The dog ate Tom`처럼 방향이 다른 관계를 구별할 수 없습니다. Q와 K를 별도의 가중치 행렬로 분리하면 "A가 B에 얼마나 주목하는가"와 "B가 A에 얼마나 주목하는가"가 서로 다른 값을 가질 수 있게 됩니다. 둘째, K와 V를 나누지 않으면 "무엇을 기준으로 검색할지"와 "실제로 가져올 내용"의 역할이 뒤섞입니다. K와 V를 분리하면 검색 기준(K)과 전달 내용(V)을 독립적으로 학습할 수 있습니다.

## Scaled Dot-Product Attention

Attention Score는 Query와 Key를 내적해서 구합니다.

$$\text{score} = QK^T$$

이 값을 그대로 쓰면 벡터의 차원이 커질수록 내적값이 통계적으로 폭주하는 경향이 있어, Key 벡터의 차원 $d_k$의 제곱근으로 나눠 스케일을 조정합니다.

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

그 다음 01장에서 다룬 **Softmax**를 통과시켜 "각 단어로부터 몇 %씩 가져올지"를 확률 형태로 바꾸고, 이 확률로 Value를 가중합(weighted sum)하면 "문장 안에서 이 토큰이 실제로 어떤 의미를 갖는지"를 담은 벡터가 완성됩니다.

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    d_k = q.size(-1)
    scores = q @ k.transpose(-2, -1) / (d_k ** 0.5)   # (seq_len, seq_len)
    weights = F.softmax(scores, dim=-1)               # 각 행의 합이 1
    return weights @ v                                 # (seq_len, d_v)

seq_len, d_k = 4, 16
q = torch.randn(seq_len, d_k)
k = torch.randn(seq_len, d_k)
v = torch.randn(seq_len, d_k)

output = scaled_dot_product_attention(q, k, v)
print(output.shape)  # torch.Size([4, 16])
```

`scores`의 각 행은 "이 토큰이 다른 모든 토큰에 얼마나 주목하는가"를 나타내는 원시 점수이고, `Softmax`를 거친 `weights`의 각 행은 합이 1인 확률 분포가 됩니다. 이 확률로 `v`를 가중합한 결과가 출력이므로, 출력 벡터의 shape은 입력 시퀀스 길이와 Value의 차원을 그대로 유지합니다.

## Causal Masking — 미래를 보지 않기

GPT처럼 다음 토큰을 순서대로 생성하는 **Causal Language Model**은 학습 시점에 아직 등장하지 않은 미래 토큰을 미리 봐서는 안 됩니다. 그래서 Attention Score 행렬에서 대각선 위쪽(미래 토큰에 해당하는 위치)을 $-\infty$로 마스킹한 뒤 Softmax를 적용합니다. $e^{-\infty} \approx 0$이므로 Softmax를 거치면 해당 위치의 확률이 정확히 0이 됩니다.

```python
def causal_mask(seq_len: int) -> torch.Tensor:
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
    return mask.masked_fill(mask == 1, float("-inf"))

mask = causal_mask(4)
scores = q @ k.transpose(-2, -1) / (d_k ** 0.5)
masked_scores = scores + mask     # 대각선 위쪽에 -inf를 더해 미래 토큰을 가림
weights = F.softmax(masked_scores, dim=-1)
```

`torch.triu(..., diagonal=1)`은 대각선 바로 위쪽부터 시작하는 상삼각 행렬을 만들고, 그 위치의 값을 $-\infty$로 채워 `scores`에 더합니다. 반면 BERT 같은 **Masked Language Model**은 양쪽 문맥을 모두 볼 수 있어 문맥 파악에는 유리하지만, 문장 중간에 새 토큰이 추가될 때마다 앞부분 전체를 다시 계산해야 한다는 구조적 차이가 있습니다(12장에서 다룰 KV 캐싱은 이 Causal 구조를 전제로 합니다).

## Multi-head Attention — 여러 관점에서 동시에 보기

Attention을 한 번만 계산하면 한 가지 관점에서만 문맥을 파악하게 됩니다. **Multi-head Attention**은 Q, K, V를 여러 개의 "헤드(head)"로 나눠 각기 다른 관점에서 병렬로 Attention을 계산한 뒤 결과를 이어붙입니다(concat). 구현 측면에서는 헤드마다 별도로 계산하지 않고, Q/K/V 각각에 대해 하나의 큰 행렬을 만든 뒤 `view`로 헤드 수만큼 나눠서 병렬 계산하는 것이 효율적입니다.

```python
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, emb_dim: int, n_heads: int):
        super().__init__()
        assert emb_dim % n_heads == 0
        self.n_heads = n_heads
        self.head_dim = emb_dim // n_heads
        self.qkv_proj = nn.Linear(emb_dim, emb_dim * 3)
        self.out_proj = nn.Linear(emb_dim, emb_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, seq_len, emb_dim = x.shape
        qkv = self.qkv_proj(x).view(batch, seq_len, 3, self.n_heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)                        # 각 (batch, seq_len, n_heads, head_dim)
        q, k, v = (t.transpose(1, 2) for t in (q, k, v))    # (batch, n_heads, seq_len, head_dim)
        scores = q @ k.transpose(-2, -1) / (self.head_dim ** 0.5)
        weights = F.softmax(scores, dim=-1)
        out = (weights @ v).transpose(1, 2).reshape(batch, seq_len, emb_dim)
        return self.out_proj(out)
```

GPT-2는 12개의 헤드를 사용했지만, 최근 대형 모델은 128개에 이르는 헤드를 사용하는 경우도 있어 그만큼 더 다양한 관점에서 문맥을 파악합니다. 여러 트랜스포머 블록이 쌓이면 앞쪽 블록은 입력 값에서 관계를 파악하는 데 집중하고, 뒤쪽 블록은 그 관계를 바탕으로 출력을 준비하는 경향이 관찰됩니다.

## 흔한 오개념 — "헤드가 많을수록 무조건 성능이 좋아진다"

헤드 수를 늘리면 더 다양한 관점을 볼 수 있을 것 같지만, 임베딩 차원(`emb_dim`)이 고정된 상태에서 헤드 수만 늘리면 헤드 하나가 담당하는 차원(`head_dim = emb_dim / n_heads`)이 줄어듭니다. 헤드 하나의 표현력이 지나치게 작아지면 오히려 각 헤드가 의미 있는 패턴을 학습하기 어려워집니다. 실제로는 헤드 수와 `head_dim`의 균형, 그리고 전체 모델 크기(레이어 수·임베딩 차원)에 맞춰 헤드 수를 함께 조정합니다 — "헤드가 많을수록 좋다"가 아니라 "모델 규모에 맞는 헤드 수가 따로 있다"가 정확한 이해입니다.

다음 장에서는 이 Multi-head Attention을 감싸는 나머지 구성요소 — 정규화, Feed Forward, Residual Connection, Dropout — 을 조립해 하나의 완전한 GPT 블록을 만듭니다.
