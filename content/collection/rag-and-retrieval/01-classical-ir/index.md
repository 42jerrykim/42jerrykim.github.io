---
collection_order: 1
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[RAG] 01. Classical IR — 역색인, TF-IDF, BM25"
slug: classical-information-retrieval
description: "역색인 자료구조부터 단어 빈도의 한계를 보정하는 TF-IDF, 오랫동안 사실상 표준이었던 BM25, 그리고 MRR·Precision·Recall 같은 검색 평가 지표까지 신경망 이전 정보검색의 핵심을 자세히 정리합니다."
tags:
  - Information-Retrieval(정보검색)
  - Retrieval-Augmented-Generation(RAG)
  - NLP(Natural Language Processing)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - Data-Science(데이터사이언스)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Reference(참고)
  - Implementation(구현)
  - Time-Complexity(시간복잡도)
  - History(역사)
  - Algorithm(알고리즘)
  - Data-Structures(자료구조)
  - Comparison(비교)
  - Best-Practices
  - Vector-Database(벡터데이터베이스)
  - LLM(Large Language Model)
  - PyTorch
  - Neural-Network
  - Advanced
  - Case-Study

image: "wordcloud.png"
---

검색엔진이 등장한 지 수십 년이 지났지만, 그 근간이 되는 아이디어는 지금도 RAG 시스템의 일부로 살아 있습니다. 이 장은 신경망이 등장하기 전, "쿼리가 주어지면 관련 문서를 어떻게 빠르게 찾을 것인가"라는 문제를 검색엔진이 어떻게 풀어왔는지를 다룹니다.

## 역색인 — 검색 엔진의 근간 자료구조

전통적인 정보검색은 두 단계로 이루어집니다. 쿼리(Query)에서 term(키워드)을 추출하고, 그 term으로 문서를 검색합니다. 이때 핵심 자료구조가 **역색인(Inverted Index)**입니다 — `{단어: 문서 목록(posting list)}` 형태로, 각 단어가 등장하는 문서 목록을 미리 만들어둡니다.

```python
from collections import defaultdict

def build_inverted_index(documents: list[str]) -> dict[str, list[int]]:
    index = defaultdict(list)
    for doc_id, text in enumerate(documents):
        for term in set(text.lower().split()):
            index[term].append(doc_id)
    return index

docs = ["stanford university campus", "berkeley university research"]
index = build_inverted_index(docs)
common_docs = set(index["university"]) & set(index["stanford"])   # 두 단어가 모두 등장하는 문서
```

`index["university"]`와 `index["stanford"]`의 교집합을 구하면 두 단어가 모두 등장하는 문서를 빠르게 찾을 수 있습니다. 문서 전체를 순회하며 매번 단어를 검사하는 대신, 미리 만들어둔 색인을 조회하는 것만으로 검색이 끝나는 것이 이 자료구조의 핵심입니다. 검색의 결과물은 **순위가 매겨진 문서 목록(ranked list of documents)**이며, 대표적인 랭킹 알고리즘으로 PageRank, TF-IDF, BM25가 있습니다.

## Term-Document Matrix와 희소 표현

문서 집합(corpus) 전체는 **Term-Document Matrix**로 표현할 수 있습니다. 모든 term을 모은 것을 **vocabulary(어휘집)**라 하고, 각 문서는 이 vocabulary 크기만큼의 열벡터로 표현됩니다. 문서 하나에는 전체 단어 중 극히 일부만 등장하므로, 이 벡터는 대부분의 값이 0인 **희소 벡터(sparse vector)**가 됩니다. 역색인은 이 행렬을 "행(row) 기준으로 조밀하게(dense)" 표현한 것으로도 볼 수 있습니다 — 즉 역색인과 Term-Document Matrix는 같은 정보를 다른 방향으로 압축한 것입니다.

단순히 단어가 몇 번 등장했는지(word frequency)만으로 문서를 비교하면 문제가 생깁니다. 직관적으로 더 관련 있어 보이는 문서보다, 특정 단어가 단순 반복된 문서가 먼저 나오는 왜곡이 발생할 수 있습니다.

## TF-IDF — 흔한 단어의 가중치를 낮추기

**TF-IDF**는 단어 빈도(TF)에 **IDF(Inverse Document Frequency)**로 보정을 가합니다.

$$\text{IDF}(w) = \log\frac{|D|}{\text{df}(w)}$$

$\text{df}(w)$는 단어 $w$가 등장하는 문서의 개수이고, 전체 문서 수 $|D|$가 훨씬 크기 때문에 로그를 취합니다. TF-IDF의 핵심은 **여러 문서에 흔하게 등장하지 않는(희귀한) 단어일수록, 그 단어가 매칭될 때 더 큰 가중치를 준다**는 것입니다 — "the"나 "a" 같은 단어는 거의 모든 문서에 등장해 IDF가 낮고, 전문 용어는 소수의 문서에만 등장해 IDF가 높습니다.

IDF에는 두 가지 문제가 있습니다. $\text{df}(w)=0$일 때(단어가 전혀 등장하지 않을 때) 정의되지 않는 문제, 그리고 문서의 길이 차이를 고려하지 못하는 문제입니다 — 백과사전처럼 긴 문서와 짧은 메시지를 그대로 비교하면 불공정합니다.

## BM25 — TF-IDF의 개선판

**BM25**는 TF-IDF의 두 문제를 보정한 형태로, 오랫동안 정보검색의 사실상 표준으로 쓰였습니다.

$$\text{BM25}(w, doc, D) = \underbrace{\frac{\text{TF}(w,doc)\cdot(k+1)}{\text{TF}(w,doc) + k\cdot\left(1-b+b\cdot\frac{|doc|}{\text{avgdoclen}}\right)}}_{\text{Score}} \times \text{IDF}_{BM25}(w,D)$$

$k$(보통 1.2 부근)는 단어 빈도가 계속 늘어나도 점수가 무한정 커지지 않도록 **평탄화(flatten)**하는 역할을 합니다 — 어떤 단어가 10번 등장한 문서가 1번 등장한 문서보다 10배 더 관련 있다고 보지 않고, 그 증가폭을 완만하게 만듭니다. $b$(보통 0.75 부근)는 문서 길이에 대한 패널티를 조절합니다 — `avgdoclen`(평균 문서 길이)보다 긴 문서에는 페널티를 줘서, 단순히 길다는 이유만으로 더 많은 단어를 포함해 유리해지는 것을 막습니다. $k$, $b$ 값에 따라 점수 곡선의 기울기가 달라지므로, 실전에서는 도메인에 맞게 조정 가능한 튜닝 포인트입니다.

```python
import math

def bm25_score(term_freq: int, doc_len: int, avg_doc_len: int, doc_freq: int, num_docs: int, k: float = 1.2, b: float = 0.75) -> float:
    idf = math.log(num_docs / doc_freq)
    numerator = term_freq * (k + 1)
    denominator = term_freq + k * (1 - b + b * doc_len / avg_doc_len)
    return idf * (numerator / denominator)
```

## 검색 결과를 평가하는 지표

검색 결과의 품질은 두 가지 관점으로 평가합니다. 하나는 "**첫 번째** 관련 문서가 얼마나 앞쪽에 있는가"이고, 다른 하나는 "**전체** 결과가 얼마나 정답을 많이 포함하는가"입니다.

**Reciprocal Rank(RR)**은 정답 문서가 결과 목록에서 몇 번째에 위치했는지(Rank)의 역수입니다 — 정답이 1등이면 1, 2등이면 0.5, 10등이면 0.1처럼, 첫 번째로 등장한 정답 문서의 위치 품질을 나타냅니다. 여러 쿼리에 대한 평균을 내면 **MRR(Mean Reciprocal Rank)**이 됩니다.

**Precision(정밀도)**과 **Recall(재현율)**은 Vision AI 시리즈 05장에서 다룬 Object Detection의 평가지표와 같은 개념입니다 — Precision은 검색 시스템이 보여준 결과물 중 실제 정답이 얼마나 포함되어 있는지를, Recall은 세상에 존재하는 전체 정답 중 시스템이 얼마나 많은 정답을 놓치지 않고 찾아냈는지를 측정합니다.

| 지표 | 초점 | 질문 |
|---|---|---|
| MRR(RR의 평균) | 첫 번째 관련 문서의 위치 | 정답이 얼마나 위쪽에 나오는가 |
| Precision | 결과의 정확성 | 보여준 것 중 몇 %가 진짜 정답인가 |
| Recall | 결과의 적중률 | 존재하는 정답 중 몇 %를 찾았는가 |

## 흔한 오개념 — "BM25는 TF-IDF보다 항상 더 정확하다"

BM25가 TF-IDF의 두 가지 결함(정의되지 않는 경우, 문서 길이 미고려)을 보정한 개선판이라는 사실 때문에 "BM25가 TF-IDF의 상위 호환"이라고 단정하기 쉽지만, 정확히는 BM25가 **더 많은 조정 가능한 파라미터($k$, $b$)를 통해 더 넓은 상황에 적응할 수 있는 프레임워크**를 제공한다고 이해하는 것이 정확합니다. $k$, $b$를 적절히 튜닝하지 않으면 BM25도 특정 도메인(예: 문서 길이 편차가 매우 큰 코퍼스)에서는 기대만큼 성능이 나오지 않을 수 있습니다. "BM25가 TF-IDF보다 낫다"는 일반적인 관찰은 맞지만, 그 우위는 자동으로 보장되는 것이 아니라 파라미터가 데이터에 맞게 조정되었을 때 실현됩니다.

다음 장에서는 단어의 정확한 일치에 의존하는 Sparse Retrieval의 한계를 넘어, 신경망으로 의미가 비슷한 문서를 찾는 Dense Retrieval을 다룹니다.
