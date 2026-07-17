---
collection_order: 4
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[RAG 04] 고차원 근사 검색 — LSH와 그래프 인덱스"
slug: approximate-nearest-neighbor-search
description: "차원의 저주 때문에 정확한 최근접 이웃 탐색이 고차원에서 왜 어려워지는지부터, 해시 기반 LSH와 HNSW 같은 그래프 인덱스로 근사 검색을 빠르게 만드는 방법, CLIP을 이용한 멀티모달 검색까지 다룹니다."
tags:
  - Information-Retrieval(정보검색)
  - Vector-Database(벡터데이터베이스)
  - Embedding(임베딩)
  - Retrieval-Augmented-Generation(RAG)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - Data-Structures(자료구조)
  - Algorithm(알고리즘)
  - Time-Complexity(시간복잡도)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Advanced
  - Reference(참고)
  - Implementation(구현)
  - Comparison(비교)
---

02장에서 다룬 Dense Retrieval은 질문과 문서를 수백 차원의 벡터로 인코딩합니다. 문서가 수백만 개라면, 매 질문마다 모든 문서 벡터와 유사도를 계산하는 것은 비현실적입니다. 이 장은 왜 고차원 공간에서는 정확한 탐색이 근본적으로 어려운지, 그리고 정확함을 조금 포기하는 대신 속도를 얻는 근사 탐색 기법들을 다룹니다.

## 왜 고차원 검색은 어려운가 — 차원의 저주

파인튜닝된 BERT의 임베딩은 보통 512, 1024, 2048차원 등 매우 고차원입니다. 검색은 본질적으로 탐색(search)과 같습니다. 문서 $n$개 중 정확한 매칭이라면 정렬된 데이터에서 이진 탐색으로 $O(\log n)$ 시간에 찾을 수 있지만, 고차원 공간에서는 이런 효율적인 탐색이 어려워지고 결국 선형 탐색에 가까운 비용이 듭니다. 이 현상을 **차원의 저주(Curse of Dimensionality)**라 부릅니다.

직관적인 이유는 이렇습니다 — 차원이 높아질수록 공간을 균등하게 나누기 위한 "변의 길이" 자체가 커져야 합니다. 예를 들어 1차원에서는 데이터의 절반을 담는 구간의 길이가 전체의 절반이면 충분하지만, 차원이 늘어날수록 같은 비율의 데이터를 담기 위한 초입방체(hypercube)의 한 변 길이는 1에 가까워집니다. 이 때문에 저차원에서 잘 동작하는 KD-tree 같은 트리 기반 탐색은, 고차원에서는 사실상 모든 데이터를 훑는 것과 큰 차이가 없어집니다.

## LSH — 비슷한 벡터를 같은 버킷에 담기

**LSH(Locality Sensitive Hashing)**는 KD-tree 같은 전통적인 트리 기반 탐색의 대안으로, 비슷한 벡터일수록 같은 해시 버킷(bucket)에 담기도록 설계된 해시 함수를 사용해 **근사 최근접 이웃(Approximate Nearest Neighbor, ANN)**을 빠르게 찾는 기법입니다.

```python
import numpy as np

class SimpleLSH:
    def __init__(self, dim: int, num_hashes: int = 8, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.hyperplanes = rng.standard_normal((num_hashes, dim))   # 무작위 초평면들

    def hash(self, vector: np.ndarray) -> str:
        projections = self.hyperplanes @ vector
        return "".join("1" if p > 0 else "0" for p in projections)   # 각 초평면 기준 부호로 버킷 ID 생성
```

`hash` 메서드는 벡터를 여러 개의 무작위 초평면에 투영해, 각 초평면 기준으로 어느 쪽에 있는지(부호)를 이어붙여 버킷 ID를 만듭니다. 비슷한 방향의 벡터는 대부분의 초평면에서 같은 쪽에 위치할 확률이 높으므로, 같은(또는 비슷한) 해시 값을 갖게 됩니다. 검색할 때는 전체 문서를 다 비교하는 대신, 질문 벡터와 같은 버킷에 속한 문서들만 후보로 좁혀 비교합니다 — 정확한 최근접 이웃을 놓칠 가능성이 있지만(근사), 탐색 범위를 극적으로 줄일 수 있습니다.

## 그래프 기반 인덱스 — 최근의 추세

최근에는 **그래프 인덱스(Graph Index)**를 사용하는 추세가 늘고 있습니다. 대표적인 방식이 **HNSW(Hierarchical Navigable Small World)**입니다.

> Yu. A. Malkov, D. A. Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs", *arXiv:1603.09320* (2016)

그래프는 정점(vertex, 여기서는 문서에 해당)과 간선(edge)만 기억하면 됩니다. 검색 시에는 임의의 정점에서 출발해, 후보 이웃 정점들 중 질문 벡터에 가장 가까운 노드로 반복적으로 이동합니다 — 그리디 탐색에 가까운 방식입니다. HNSW는 이 그래프를 여러 층(layer)으로 쌓아, 상위 층에서는 성긴 연결로 빠르게 대략적인 위치까지 이동하고 하위 층으로 내려갈수록 촘촘한 연결로 정밀하게 탐색 범위를 좁혀 나갑니다.

| | LSH | 그래프 인덱스(HNSW) |
|---|---|---|
| 핵심 자료구조 | 해시 버킷 | 다층 근접 그래프 |
| 탐색 방식 | 같은 버킷 내에서만 비교 | 그리디하게 이웃 노드로 이동 |
| 정확도-속도 조절 | 해시 함수·버킷 수 | 그래프 연결 밀도(층수, 이웃 수) |

## 실전 활용 — 멀티모달 검색

Vision AI 시리즈 04장에서 다룬 CLIP을 사용해 이미지를 벡터화하면, 텍스트로 이미지를 검색하는 등 **멀티모달 검색(multimodal search)**도 같은 Dense Retrieval의 틀 안에서 구현할 수 있습니다. CLIP의 이미지 인코더와 텍스트 인코더는 같은 벡터 공간에 임베딩을 만들도록 학습되어 있으므로, "노을이 지는 해변" 같은 텍스트 쿼리를 임베딩한 뒤 이 장에서 다룬 LSH나 그래프 인덱스로 가장 가까운 이미지 벡터를 찾으면 텍스트-이미지 검색이 됩니다. 검색 대상의 모달리티(텍스트, 이미지, 오디오)가 달라져도 "벡터 공간에서 가까운 것을 빠르게 찾는다"는 이 장의 원리는 그대로 재사용됩니다.

## 흔한 오개념 — "근사 검색은 항상 정확도를 희생하는 타협이다"

LSH나 그래프 인덱스가 "근사(Approximate)"라는 이름 때문에 정확도를 상당히 희생하는 것처럼 들리지만, 실무에서 적절히 튜닝된 ANN 인덱스는 정확한(exact) 탐색 대비 리콜(정답을 놓치지 않는 비율)이 95% 이상으로 유지되면서도 탐색 속도는 수십~수백 배 빨라지는 경우가 흔합니다. "근사"가 의미하는 것은 "이론적으로 100% 정확함을 보장하지 않는다"는 것이지, "실무에서 눈에 띄게 부정확하다"는 뜻이 아닙니다. 벡터 DB(Milvus, Pinecone, FAISS 등)를 선택할 때 중요한 것은 "근사냐 정확이냐"가 아니라, 주어진 리콜 목표를 만족하면서 얼마나 빠른 인덱스를 구성할 수 있는가입니다.

이것으로 검색 자체의 기본기(Phase 1)가 끝났습니다. 다음 장부터는 텍스트 문서를 넘어선 확장으로, 먼저 지식그래프를 검색 대상으로 삼는 GraphRAG를 다룹니다.
