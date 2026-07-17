---
collection_order: 2
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[RAG 02] Dense Retrieval — BERT로 의미를 검색하기"
slug: dense-retrieval-fundamentals
description: "희소 벡터 대신 신경망 임베딩으로 검색하는 Dense Retrieval을 다룹니다. Bi-encoder와 Cross-encoder의 정확도-속도 트레이드오프, DPR의 대조 학습, Re-ranking 2단계 구조를 원 논문과 함께 정리합니다."
tags:
  - Information-Retrieval(정보검색)
  - Retrieval-Augmented-Generation(RAG)
  - BERT
  - Embedding(임베딩)
  - Vector-Database(벡터데이터베이스)
  - Transformer
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - NLP(Natural Language Processing)
  - PyTorch
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Advanced
  - Reference(참고)
  - Comparison(비교)
  - Implementation(구현)
---

01장에서 다룬 BM25는 단어가 정확히 일치해야 검색이 됩니다. "자동차"로 검색하면 "차량"이라는 단어만 쓰인 문서는 찾지 못합니다. **Dense Retrieval**은 이 한계를 신경망 임베딩으로 넘어섭니다 — 단어의 표면형이 아니라 의미가 비슷한 문서를 찾습니다. 이 장은 Dense Retrieval을 학습하는 두 가지 구조와, 그 사이의 정확도-속도 트레이드오프를 다룹니다.

## Sparse에서 Dense로

01장의 방법들은 **Sparse Retrieval**이라 부릅니다(TF-IDF 벡터 자체가 대부분 0인 희소 벡터이기 때문입니다). **Dense Retrieval**은 질문과 문서를 각각 `dense_encoder(q)`, `dense_encoder(d)`로 인코딩해, 대부분의 값이 0이 아닌 조밀한(dense) 벡터를 만듭니다. 이 인코더는 파인튜닝된 BERT 같은 신경망입니다. 유사도는 LLM 시리즈 01장에서 다룬 내적 또는 코사인 유사도로 계산합니다 — 코사인 유사도는 벡터를 단위벡터로 정규화한 뒤 내적한 것과 같습니다.

BERT는 LLM 시리즈 03장에서 다룬 것처럼 인코더만 쓰는 구조로, **사전학습(Pre-training)**과 **파인튜닝(Fine-tuning)** 두 단계로 구성됩니다. 사전학습 단계는 NSP(Next Sentence Prediction)와 Masked LM(마스크 언어모델)의 손실을 최소화하는 것이 목표이며, 이 사전학습된 BERT를 검색 과제에 맞게 다시 파인튜닝한 것이 Dense Retrieval의 인코더입니다.

## 두 가지 학습 구조 — Cross-encoder와 Bi-encoder

Dense Retrieval을 학습하는 방법은 크게 두 갈래입니다.

1. `fine-tuned BERT(q, d) → similarity score`: 질문과 문서를 **함께** BERT에 넣어 유사도 점수를 직접 출력
2. `fine-tuned BERT(q) · fine-tuned BERT(d) → similarity score`: 질문과 문서를 **각각 따로** 인코딩한 뒤 내적으로 유사도 계산

정확도 측면에서는 첫 번째 방식이 더 좋습니다 — 질문과 문서가 서로를 직접 참조(attend)할 수 있기 때문입니다. 하지만 두 번째 방식은 문서 임베딩을 미리 계산해둘 수 있어 속도가 훨씬 빠릅니다.

| | Cross-encoder(방식 1) | Bi-encoder(방식 2) |
|---|---|---|
| 입력 | 질문·문서를 함께 인코딩 | 질문·문서를 각각 인코딩 |
| 정확도 | 높음(질문-문서 상호작용 반영) | 상대적으로 낮음 |
| 속도 | 느림(후보마다 매번 계산) | 빠름(문서 임베딩 사전 계산 가능) |
| 확장성 | 낮음(후보 $N$개면 $N$번 계산) | 높음(벡터 검색으로 대량 처리) |

**Cross-encoder**는 Q와 D를 함께 넣으면 점수 하나가 나오는 구조입니다(방식 1). 학습할 때는 질문과 관련된 문서(positive) 1개, 관련 없는 문서(negative) 여러 개를 함께 씁니다. 문제는 후보 문서가 $N$개 있으면 매번 $N$번을 모델에 통과시켜야 해서 매우 느리다는 것입니다 — 그래서 Cross-encoder는 보통 소수의 후보에 대해서만 적용하는 **Re-ranking** 단계에 쓰입니다.

## Re-ranking — 두 방식을 함께 쓰기

실전에서는 Bi-encoder와 Cross-encoder를 함께 씁니다. 먼저 빠른 Bi-encoder로 대량의 문서 중 후보를 빠르게 추린 뒤, 상위 후보들에 대해서만 느리지만 정확한 Cross-encoder로 다시 정밀하게 점수를 계산하는 2단계 구조입니다.

```python
def two_stage_retrieval(query: str, documents: list[str], bi_encoder, cross_encoder, top_k: int = 100, rerank_k: int = 10):
    query_emb = bi_encoder.encode(query)
    doc_embs = bi_encoder.encode_batch(documents)          # 미리 계산해둘 수 있음
    scores = query_emb @ doc_embs.T
    candidates = [documents[i] for i in scores.argsort()[-top_k:]]   # 1단계: 빠른 후보 추리기

    reranked = sorted(candidates, key=lambda d: cross_encoder.score(query, d), reverse=True)
    return reranked[:rerank_k]                              # 2단계: 정밀한 재정렬
```

`bi_encoder.encode_batch(documents)`는 문서가 바뀌지 않는 한 미리 계산해 벡터 DB에 저장해둘 수 있는 반면, `cross_encoder.score(query, d)`는 질문이 들어올 때마다 후보 각각에 대해 새로 계산해야 합니다. `top_k`(1단계에서 추릴 후보 수)를 `rerank_k`(최종 반환 수)보다 훨씬 크게 잡는 이유는, Bi-encoder가 놓칠 수 있는 진짜 정답을 재정렬 단계에서 구제할 여지를 남기기 위해서입니다.

## DPR — 문서 인코딩을 오프라인으로 미리 끝내기

**DPR(Dense Passage Retrieval)**은 Bi-encoder 구조를 실제로 대규모 오픈 도메인 질의응답에 적용한 대표적인 연구입니다.

> Vladimir Karpukhin, Barlas Oğuz, Sewon Min 외, "Dense Passage Retrieval for Open-Domain Question Answering", *arXiv:2004.04906* (2020)

DPR은 학습할 때는 질문 인코더와 문서 인코더 두 개를 함께(paired) 학습시키지만, 학습이 끝나면 문서 인코딩은 오프라인 전처리로 미리 끝내둘 수 있습니다 — 모든 문서를 `BERT(d)`로 미리 인코딩해서 벡터 DB에 저장해두면, 추론 시점에는 질문이 들어올 때마다 질문 인코더 `BERT(q)`만 계산해서 빠르게 조회할 수 있습니다.

$$\text{Sim}(q, doc) = \text{EncQ}(q)^\top \text{EncD}(doc), \quad \mathcal{L} = -\log\frac{\exp(\text{Sim}(q_i, doc_i^+))}{\exp(\text{Sim}(q_i, doc_i^+)) + \sum_j \exp(\text{Sim}(q_i, doc_{i,j}^-))}$$

손실은 정답 문서(positive)와의 유사도는 높이고, 나머지(negative) 문서와의 유사도는 낮추는 방향으로 학습됩니다 — LLM 시리즈 02장에서 다룬 Cross Entropy, Vision AI 시리즈 04장에서 다룬 CLIP의 대조 학습(Contrastive Learning)과 같은 구조입니다. DPR 논문은 이 방식을 "확장성은 뛰어나지만 질문-문서 간 상호작용은 제한적"이라고 요약하는데, 이는 앞서 다룬 Bi-encoder의 정확도-속도 트레이드오프와 같은 맥락입니다.

정보검색 연구에서 널리 쓰이는 벤치마크로는 TREC(Text REtrieval Conference 데이터셋 모음)과 MS MARCO(마이크로소프트가 공개한 대규모 질의응답/검색 데이터셋)가 있습니다.

## 흔한 오개념 — "Dense Retrieval이 Sparse Retrieval을 완전히 대체한다"

신경망 기반 Dense Retrieval이 의미적 유사도까지 포착할 수 있으니 01장의 Sparse Retrieval(BM25 등)을 완전히 대체했을 것이라 생각하기 쉽지만, 실무에서는 두 방식을 **함께** 쓰는 경우가 많습니다. Dense Retrieval은 의미가 비슷하지만 표현이 다른 문서를 잘 찾는 대신, 고유명사·제품 코드·정확한 숫자처럼 "정확히 일치해야 의미가 있는" 검색에서는 오히려 BM25 같은 Sparse 방식이 더 안정적인 경우가 있습니다. 두 방식의 점수를 결합하는 **Hybrid Search**가 실무에서 흔히 쓰이는 이유가 여기에 있습니다 — 의미적 유사도와 어휘적 정확성이라는 서로 다른 신호를 상호 보완적으로 활용하는 것입니다.

다음 장에서는 이렇게 검색된 문서를 실제로 LLM의 답변 생성과 연결하는 RAG 파이프라인을, 청킹 전략과 LlamaIndex 실습 중심으로 다룹니다.
