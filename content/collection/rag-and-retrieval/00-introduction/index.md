---
collection_order: 0
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[RAG] 00. Introduction: RAG와 정보검색"
slug: getting-started-rag-and-retrieval
description: "검색과 LLM을 결합하는 시리즈의 도입 챕터입니다. LLM만으로는 부족한 세 가지 이유부터, 고전 IR에서 GraphRAG·MCP까지 이어지는 8개 챕터 커리큘럼과 학습 목표, 챕터별 우선순위 로드맵을 자세히 정리합니다."
tags:
  - Retrieval-Augmented-Generation(RAG)
  - Information-Retrieval(정보검색)
  - LLM(Large Language Model)
  - Vector-Database(벡터데이터베이스)
  - Embedding(임베딩)
  - BERT
  - Transformer
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - NLP(Natural Language Processing)
  - Knowledge-Graph(지식그래프)
  - MCP(Model Context Protocol)
  - Curriculum
  - 커리큘럼
  - Roadmap
  - 로드맵
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Data-Science(데이터사이언스)
  - PyTorch
  - Beginner
  - Advanced
  - Case-Study

image: "wordcloud.png"
---

LLM에게 인덱스에 없는 도시(예: 신장)에 대해 질문하면, 실제 지진 규모 7.1을 6.1이라고 답하는 것처럼 그럴듯하지만 틀린 답을 내놓습니다. 같은 질문을 인덱스에 포함된 도시에 대해 물으면 정확한 답이 나옵니다. 이 차이가 이 시리즈의 출발점입니다 — 아무리 큰 LLM도 검색이라는 외부 장치와 결합하지 않으면, "안다고 착각하는 것"과 "정말로 아는 것"을 스스로 구분하지 못합니다.

## LLM만으로는 부족한 세 가지 이유

검색이 필요한 이유는 크게 세 가지입니다. 첫째, <strong>지식의 시점 제한(Knowledge cutoffs)</strong>입니다 — 모델 파라미터는 특정 시점까지의 데이터로만 학습되어 최신 정보를 모릅니다. 둘째, <strong>비공개 데이터(Private data)</strong>입니다 — 회사 내부 문서처럼 애초에 모델 학습에 쓰이지 않은 데이터가 있습니다. 셋째, <strong>학습 실패(Learning failures)</strong>입니다 — LLM 시리즈 07장에서 다룬 것처럼, 설령 학습 데이터에 포함되었던 내용이라도 모델이 정확히 기억·재현하지 못할 수 있습니다. <strong>RAG(Retrieval-Augmented Generation)</strong>는 이 세 가지 한계를 "모델이 가진 지식의 범위를, 검색 대상 문서의 범위로 명시적으로 제한·보강"하는 방식으로 우회합니다.

## 이 시리즈가 다루는 범위

이 시리즈는 검색(Retrieval)의 고전 이론에서 시작해 LLM과 결합하는 지점까지를 다룹니다. 역색인·TF-IDF·BM25 같은 Sparse Retrieval, BERT 기반 Dense Retrieval, 검색과 생성을 잇는 RAG 파이프라인, 텍스트 대신 지식그래프를 검색하는 GraphRAG, 정형 데이터베이스를 자연어로 조회하는 MCP 기반 Text2SQL, 그리고 검색 품질을 끌어올리는 Cross-Encoder를 직접 학습시키는 방법까지가 범위입니다. LLM 자체의 아키텍처는 LLM 밑바닥부터 이해하기 시리즈를, 멀티모달 검색에 쓰이는 CLIP 같은 모델은 Vision AI 파운데이션 시리즈를 전제로 합니다.

## 커리큘럼

| 챕터 | 제목 | 핵심 질문 |
|---|---|---|
| 01 | Classical IR | 단어가 정확히 일치해야만 검색이 되는가 |
| 02 | Dense Retrieval | 의미가 비슷한 문서를 어떻게 신경망으로 찾는가 |
| 03 | RAG 파이프라인 구축 | 검색된 문서를 LLM에 어떻게 넘겨야 하는가 |
| 04 | 고차원 근사 검색 | 임베딩이 수백 차원일 때도 빠르게 검색할 수 있는가 |
| 05 | GraphRAG | 문서 대신 지식그래프를 검색하면 무엇이 달라지는가 |
| 06 | MCP 기반 Text2SQL | LLM이 정형 데이터베이스를 안전하게 조회하려면 |
| 07 | Cross-Encoder 파인튜닝 | 재정렬 모델은 무엇을 정답·오답으로 학습하는가 |

01–02장은 검색 자체의 두 갈래(Sparse·Dense)를, 03–04장은 그 검색을 LLM 생성과 실제로 결합하는 방법을, 05–07장은 텍스트 문서를 넘어선 확장(그래프, 정형 데이터, 재정렬 모델 직접 학습)을 다룹니다. 이 순서를 따르는 이유는 05–07장에서 다루는 응용이 모두 01–04장에서 다지는 검색·유사도 계산의 기본기를 전제하기 때문입니다. BM25·Dense Retrieval에 익숙하다면 01–02장을 건너뛰고 03장부터 시작해도 무리가 없습니다.

## 학습 결과

이 시리즈를 완주하면 "이 검색 문제에는 Sparse가 나은가 Dense가 나은가", "재정렬(re-ranking)이 필요한 상황인가", "텍스트 검색으로 충분한가 아니면 그래프·정형 데이터 결합이 필요한가"를 판단할 수 있게 됩니다. 이는 실무에서 RAG 시스템을 설계할 때 청킹 전략, 검색 트리거 시점, Bi-encoder와 Cross-encoder의 조합 같은 구체적인 설계 선택을 "왜 그렇게 해야 하는가"까지 설명하며 내리는 역량으로 이어집니다.

다음 장에서는 신경망 이전부터 검색 엔진의 근간이 되어 온 역색인·TF-IDF·BM25를 다룹니다.
