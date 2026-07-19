---
collection_order: 7
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[RAG] 07. Cross-Encoder 파인튜닝 — InfoNCE로 재정렬 모델 학습하기"
slug: cross-encoder-fine-tuning
description: "02장에서 재정렬(re-ranking)용으로 소개한 Cross-Encoder를 직접 학습시키는 방법을 다룹니다. In-batch Negative와 Hard Negative 구성, InfoNCE Loss의 수식, 전체 학습 파이프라인을 원 논문과 함께 정리합니다. 시리즈 D의 마지막 챕터입니다."
tags:
  - Information-Retrieval(정보검색)
  - Retrieval-Augmented-Generation(RAG)
  - Fine-Tuning(파인튜닝)
  - BERT
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - PyTorch
  - NLP(Natural Language Processing)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Advanced
  - Reference(참고)
  - Implementation(구현)
  - Best-Practices
  - Vector-Database(벡터데이터베이스)
  - LLM(Large Language Model)
  - Data-Science(데이터사이언스)
  - Beginner
  - Case-Study
  - Comparison(비교)
  - Technology(기술)

image: "wordcloud.png"
---

02장에서 Cross-Encoder를 "정확하지만 느린" 재정렬기로 소개했습니다. 이 마지막 장은 그 Cross-Encoder를 실제로 어떻게 학습시키는지를 다룹니다. 핵심은 "정답 문서와 오답 문서를 어떻게 구성하는가"와 "그 구성으로 어떤 손실 함수를 최적화하는가" 두 가지입니다.

## Neural Scoring Function

Cross-Encoder는 질문 $q$와 문서 $d$를 함께 입력받아 관련도 점수를 출력하는 신경망 함수 $f(q,d)$입니다 — 02장에서 다룬 "Q와 D를 함께 넣으면 점수가 나오는" 구조를 실제로 학습 가능한 함수로 구현한 것입니다.

```python
import torch
import torch.nn as nn

class CrossEncoder(nn.Module):
    def __init__(self, bert_model: nn.Module, hidden_dim: int):
        super().__init__()
        self.bert = bert_model
        self.scorer = nn.Linear(hidden_dim, 1)

    def forward(self, query: str, document: str) -> torch.Tensor:
        # 질문과 문서를 [SEP]로 이어붙여 함께 인코딩 (02장의 방식 1)
        cls_output = self.bert.encode_pair(query, document)   # [CLS] 토큰의 최종 표현
        return self.scorer(cls_output)                          # 관련도 점수 하나
```

`encode_pair`가 질문과 문서를 하나의 시퀀스로 이어붙여 BERT에 함께 통과시키는 부분이 핵심입니다 — 이 덕분에 질문과 문서의 각 토큰이 LLM 시리즈 05장에서 다룬 Self-Attention을 통해 서로를 직접 참조할 수 있고, 이것이 Bi-encoder보다 Cross-Encoder가 더 정확한 이유입니다.

## In-Batch Negative — 배치 안의 나머지를 모두 오답으로

한 질문에 대해 명확히 관련 있는 문서(positive document)는 보통 하나만 두고 학습합니다 — 질문 하나에 여러 개의 정답 문서를 동시에 맞추도록 학습시키는 것은 훨씬 어렵기 때문입니다. 배치 안에서 정답 문서 이외의 모든 문서는 자동으로 negative(오답)로 간주해 학습에 사용합니다 — 이를 **In-batch Negative**라고 부릅니다.

```python
def build_in_batch_pairs(queries: list[str], positive_docs: list[str]) -> list[tuple[str, str, int]]:
    pairs = []
    for i, q in enumerate(queries):
        for j, d in enumerate(positive_docs):
            label = 1 if i == j else 0   # 같은 인덱스만 positive, 나머지는 전부 negative
            pairs.append((q, d, label))
    return pairs
```

배치 크기가 $N$이면, 이 방식으로 질문 하나당 $N-1$개의 negative를 별도 수집 없이 "공짜로" 얻을 수 있다는 것이 In-batch Negative의 실용적인 장점입니다.

무작위로 negative를 고르는 대신, 먼저 01장에서 다룬 BM25 같은 Sparse Retrieval을 돌려서 **상위에 랭크되었지만 실제 정답은 아닌 문서들**을 negative로 쓰면 더 정확한 모델을 얻을 수 있습니다 — 이렇게 고른 어려운 negative를 **Hard Negative**라고 부릅니다. 진짜 헷갈리는 오답(질문과 표면적으로는 관련 있어 보이지만 실제로는 정답이 아닌 문서)과 비교하며 학습해야, 모델이 단순히 "전혀 무관한 문서와 정답을 구분하는" 쉬운 패턴만 익히는 것을 피할 수 있습니다.

## InfoNCE — Positive는 밀어올리고 Negative는 밀어내기

학습 목표는 positive 쌍의 점수는 높이고, negative 쌍의 점수는 낮추는 것입니다. 이 손실 함수를 **InfoNCE**라 부릅니다.

> Aaron van den Oord, Yazhe Li, Oriol Vinyals, "Representation Learning with Contrastive Predictive Coding", *arXiv:1807.03748* (2018)

$$\mathcal{L}_{\text{InfoNCE}} = -\log\frac{\exp(f(q, d^+))}{\exp(f(q, d^+)) + \sum_{d^- \in \text{negatives}}\exp(f(q, d^-))}$$

이 형태는 LLM 시리즈 01장에서 다룬 Cross Entropy, 02장에서 다룬 DPR의 대조 학습 손실과 본질적으로 동일한 구조입니다 — 정답 항의 값은 분자에, 전체 후보(정답 포함)의 합은 분모에 두는 형태로, 정답 항이 전체에서 차지하는 비중을 최대화하는 방향으로 학습이 진행됩니다.

```python
import torch.nn.functional as F

def info_nce_loss(scores: torch.Tensor, positive_idx: torch.Tensor) -> torch.Tensor:
    # scores: (batch, num_candidates) - 질문마다 여러 후보 문서에 대한 점수
    return F.cross_entropy(scores, positive_idx)
```

`F.cross_entropy`가 내부적으로 Softmax와 Negative Log-Likelihood를 함께 계산하므로, InfoNCE Loss는 사실상 "후보 문서들 중 정답을 고르는 다중 분류 문제"의 Cross Entropy와 같은 코드로 구현됩니다. `scores`의 각 행이 한 질문에 대한 여러 후보(positive 1개 + negative 여러 개)의 점수이고, `positive_idx`는 그중 정답의 위치입니다.

## 전체 학습 파이프라인

Cross-Encoder를 학습하는 파이프라인은 세 단계로 정리됩니다. 먼저 질문-문서 쌍(In-batch negative 및 필요시 Hard negative 포함)을 구성합니다. 그다음 각 쌍에 대해 신경망으로 점수를 계산합니다. 마지막으로 InfoNCE Loss로 positive를 밀어올리고 negative를 밀어내는 방향으로 학습합니다.

```python
def train_step(cross_encoder, optimizer, queries, pos_docs, neg_docs):
    optimizer.zero_grad()
    all_scores = []
    for q, pos, negs in zip(queries, pos_docs, neg_docs):
        candidates = [pos] + negs
        scores = torch.stack([cross_encoder(q, d) for d in candidates])
        all_scores.append(scores)
    scores_batch = torch.stack(all_scores)               # (batch, 1 + num_negatives)
    positive_idx = torch.zeros(len(queries), dtype=torch.long)   # positive는 항상 0번째
    loss = info_nce_loss(scores_batch.squeeze(-1), positive_idx)
    loss.backward()
    optimizer.step()
    return loss.item()
```

이렇게 학습된 Cross-Encoder는 02장에서 다룬 2단계 Re-ranking 구조의 2단계(정밀 재정렬)에 배치되어, Bi-encoder가 빠르게 추린 후보들의 최종 순위를 정교하게 다시 매기는 역할을 합니다.

## 흔한 오개념 — "Hard Negative를 많이 쓸수록 항상 더 좋은 모델이 나온다"

Hard Negative가 무작위 negative보다 학습에 더 유용한 신호를 준다는 것은 맞지만, "많을수록 좋다"는 결론으로 바로 이어지지는 않습니다. Hard Negative의 비중이 지나치게 높아지면, 모델이 "실제로는 미묘하게 다른 두 문서를 구분하는" 데는 능숙해지는 대신, 명백히 무관한 문서와 정답을 구분하는 기본적인 능력이 오히려 불안정해질 수 있습니다 — 학습 신호가 지나치게 어려운 사례에만 집중되면서 쉬운 사례에 대한 일반화가 흔들리는 현상입니다. 실무에서는 In-batch Negative(무작위에 가까운 negative)와 Hard Negative를 적절히 섞어 쓰는 것이 일반적이며, 그 비율 자체가 데이터셋과 과제에 따라 실험적으로 조정해야 하는 하이퍼파라미터입니다.

## 시리즈 D를 마치며

00장에서 시작해, 역색인·TF-IDF·BM25 같은 고전 Sparse Retrieval(01장)에서 BERT 기반 Dense Retrieval(02장)로 넘어가, 검색과 생성을 잇는 RAG 파이프라인(03장)과 고차원 근사 검색(04장)을 다진 뒤, 텍스트를 넘어선 확장으로 GraphRAG(05장)와 MCP 기반 Text2SQL(06장), 그리고 재정렬 모델을 직접 학습시키는 방법(07장)까지 다뤘습니다. 이 시리즈 전체에서 반복해서 등장한 축은 "정확도와 속도(또는 비용)의 트레이드오프"였습니다 — Sparse와 Dense, Bi-encoder와 Cross-encoder, Once Retrieval과 Iterative Retrieval, 고정된 결정 트리와 에이전틱 워크플로우 사이의 선택이 모두 이 축 위에 있었습니다. 이 트레이드오프를 인식하고 상황에 맞게 조정하는 능력이, LLM 밑바닥부터 이해하기·Vision AI 파운데이션·On-Device AI 경량화 세 시리즈에서 다진 기초와 만나 실제 RAG 시스템을 설계하는 역량으로 이어집니다.
