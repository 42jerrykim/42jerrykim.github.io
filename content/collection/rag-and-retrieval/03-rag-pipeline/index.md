---
collection_order: 3
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[RAG] 03. RAG 파이프라인 구축 — Retriever-Reader"
slug: rag-pipeline-fundamentals
description: "검색과 생성을 잇는 Retriever-Reader 구조를 Lewis et al. 원 논문과 LlamaIndex 실습으로 다룹니다. Chunk Size 트레이드오프, 불확실성 기반 검색 트리거까지 RAG 파이프라인 설계의 실전 포인트를 정리합니다."
tags:
  - Retrieval-Augmented-Generation(RAG)
  - Information-Retrieval(정보검색)
  - LLM(Large Language Model)
  - Vector-Database(벡터데이터베이스)
  - Embedding(임베딩)
  - Transformer
  - Neural-Network
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
  - Implementation(구현)
  - Best-Practices
  - Case-Study(케이스스터디)
  - Data-Science(데이터사이언스)
  - Beginner
  - Case-Study
  - Comparison(비교)
  - Technology(기술)

image: "wordcloud.png"
---

01~02장에서 다룬 검색은 "관련 문서를 찾는" 절반의 문제였습니다. <strong>RAG(Retrieval-Augmented Generation)</strong>는 여기에 "찾은 문서를 읽고 답하는" 나머지 절반을 결합합니다. 이 장은 이 결합 구조가 수식으로 어떻게 표현되는지부터, 실제로 LlamaIndex로 구축했을 때 마주치는 청킹·프롬프트 설계 같은 실전 튜닝 포인트까지 다룹니다.

## Retriever-Reader 구조

RAG의 기본 구성은 **Retriever**(관련 문서를 효율적으로 검색)와 **Reader**(검색된 문서를 읽고 질문에 답하기) 두 역할로 나뉩니다.

> Patrick Lewis 외, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", *arXiv:2005.11401* (2020)

가장 단순한 형태는 기성품(out-of-the-box) Retriever와 Reader를 그대로 이어붙여, 검색된 문단(passage)들을 프롬프트 컨텍스트에 이어붙이는(concatenate) 방식입니다. Lewis et al.의 원 논문은 Retriever와 Generator를 처음부터 끝까지 함께 학습시키는 End-to-end 방식도 제안했지만, 이는 매우 많은 리소스가 필요해 실무에서 채택하기는 어렵습니다. 실무에서는 사전학습된 Retriever와 Reader(LLM)를 각각 독립적으로 가져와 연결하는 방식이 일반적입니다.

End-to-end 학습의 수식적 의미를 짚어보면, 입력 $x$에 대해 정답을 내야 할 때 어떤 문서 $z$를 뽑았을 때 정답 $y$가 잘 나오는지를 확률의 전체 법칙(law of total probability)으로 표현합니다.

$$P(y|x) = \sum_z P(z|x) \cdot P(y|x,z)$$

$P(z|x)$는 Retriever가 문서 $z$를 고를 확률이고, $P(y|x,z)$는 그 문서가 주어졌을 때 Reader가 정답 $y$를 낼 확률입니다. 실무에서 널리 쓰이는 "검색 후 이어붙이기" 방식은 이 식을 근사해, $z$ 중 가장 확률 높은 상위 $k$개만 뽑아 고정한 뒤 $P(y|x,z)$만 계산하는 것으로 볼 수 있습니다.

## Chunk Size — 가장 중요한 실전 튜닝 포인트

문서를 얼마나 잘게 잘라(chunking) 인덱싱하느냐가 검색 품질을 크게 좌우합니다. 너무 작게 자르면 원하는 정보가 청크 경계에서 잘려버려(질문에 필요한 문장이 청크 앞부분과 뒷부분으로 쪼개짐) 정보 손실이 발생합니다. 너무 크게 자르면 하나의 청크에 너무 많은 정보가 뒤섞여 들어가서, 정작 필요한 정보에 임베딩이 제대로 집중하지 못하고(dilution) 검색 정확도가 떨어집니다. 정답은 데이터의 성격에 달려 있어, 다루는 문서·질의 유형에 맞춰 청크 크기를 실험적으로 조정해야 합니다.

## LlamaIndex로 RAG 구축하기

LlamaIndex 같은 라이브러리는 Retriever-Reader 구조를 몇 줄의 코드로 조립할 수 있게 해줍니다.

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

documents = SimpleDirectoryReader("data").load_data()   # txt, csv, docx, pdf 등 다양한 형식 지원

splitter = SentenceSplitter(chunk_size=200, chunk_overlap=50)
index = VectorStoreIndex.from_documents(documents, transformations=[splitter])

query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("드레스덴과 자매결연한 한국 도시는?")
```

문서는 **노드(Node)** 단위로 쪼개지고, 각 노드는 임베딩 벡터로 변환되어 저장됩니다(외부 벡터 DB를 연결하지 않으면 로컬 메모리에 저장). `SentenceSplitter`의 `chunk_size`는 글자 수가 아니라 **토큰 수** 기준이며, 문장 중간에서 끊기지 않게 분할하므로 실제 토큰 수는 설정값보다 약간 작을 수 있습니다. `chunk_overlap`은 이웃 노드끼리 겹치는 토큰 수로, 정보가 청크 경계에서 잘리는 문제를 완화합니다.

`index.as_query_engine()`은 내부적으로 두 요소의 조합입니다 — 질문 임베딩과 가까운 top-k 노드를 검색하는 **리트리버**(`similarity_top_k`로 개수 조절)와, 검색된 컨텍스트를 프롬프트에 넣어 LLM이 답을 합성하는 **Response Synthesizer**입니다. 합성 프롬프트가 흔히 "주어진 컨텍스트 정보만으로, 사전 지식을 쓰지 말고 답하라(not prior knowledge)"고 명시적으로 지시하기 때문에, LLM이 원래 알고 있는 사실이라도 검색된 문서에 근거가 없으면 답하지 않도록 유도합니다 — 다만 이 강제가 완벽하지는 않아서, 모델의 파라미터 지식이 답에 섞여 나오는 경우도 실무에서 관찰됩니다.

인덱스는 정적이지 않습니다. `index.insert(document)`로 새 문서를 추가하고, `index.update_ref_doc()`이나 `index.refresh_ref_docs()`로 같은 문서 ID의 내용을 갱신하며, `index.delete_ref_doc()`으로 삭제합니다. 실무 RAG 시스템은 이런 증분 업데이트를 통해 인덱스를 계속 최신 상태로 유지합니다.

## 언제 검색해야 하는가 — 불확실성 기반 트리거

모든 질문에 검색이 필요한 것은 아닙니다. "1+1은 얼마인가"처럼 모델이 이미 확실히 아는 질문에도 매번 검색을 트리거하면 지연 시간과 비용만 늘어납니다. 언제 검색을 트리거할지 결정하는 접근은 크게 두 가지입니다 — 모델이 스스로 검색이 필요하다고 판단해 특수 토큰을 생성하게 하는 방식, 그리고 모델이 **불확실할 때**만 검색하는 방식입니다.

불확실성을 정량화하는 방법은 확률분포와 밀접하게 연관됩니다. LLM 시리즈 01장에서 다룬 Softmax가 확률분포를 만드는 방법이라는 것을 상기하면, 그 분포의 <strong>분산(variance)</strong>이나 <strong>엔트로피(entropy)</strong>로 불확실성을 측정할 수 있습니다. 이 값이 크면(모델이 다음 토큰을 확신하지 못하면) 검색을 트리거하는 식입니다. 검색을 한 번 더 해야 한다면, 문장 전체가 아니라 **불확실한 토큰 부분만 마스킹하고 그 부분만 다시 쿼리**하는 접근도 있습니다 — 이미 확신하는 부분까지 다시 검색해 시간을 낭비하지 않도록 하는 최적화입니다.

## 흔한 오개념 — "검색된 문서를 많이 넣을수록 답변 품질이 좋아진다"

Retriever가 찾은 문서를 가능한 한 많이 컨텍스트에 넣으면 Reader가 더 풍부한 정보를 활용해 좋은 답을 낼 것이라 생각하기 쉽지만, 위에서 다룬 Chunk Size 트레이드오프와 같은 원리로 오히려 역효과가 날 수 있습니다. 관련 없는 정보가 컨텍스트에 많이 섞여 들어가면, LLM이 정말 중요한 정보에 제대로 집중하지 못하고 응답 품질이 떨어지는 현상이 실무에서 흔히 관찰됩니다. 이 문제는 05장에서 다룰 GraphRAG 실습에서 "고정된 질의 생성이 불필요하게 넓은 범위의 정보를 끌어와 컨텍스트 과잉과 할루시네이션을 유발한" 사례로 다시 등장합니다 — "많이 검색하는 것"이 아니라 "정확히 필요한 만큼만 검색하는 것"이 RAG 설계의 핵심 목표입니다.

다음 장에서는 이런 검색을 실제로 대규모 벡터 공간에서 빠르게 수행하기 위한 고차원 근사 검색 기법, LSH와 그래프 인덱스를 다룹니다.
