---
collection_order: 12
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[LLM] 12. LLM 서빙 효율화 — KV Cache, GQA, MLA"
slug: llm-serving-efficiency
description: "이미 계산한 Key·Value를 재사용하는 KV Cache부터, 메모리 사용량을 줄이는 GQA와 MLA, Sliding Window Attention까지 LLM 추론을 빠르게 만드는 서빙 효율화 기법을 다룹니다. 시리즈 A의 마지막 챕터입니다."
tags:
  - LLM(Large Language Model)
  - Transformer
  - Attention(어텐션)
  - GPT(Generative Pre-trained Transformer)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - NLP(Natural Language Processing)
  - AI(인공지능)
  - PyTorch
  - Data-Science(데이터사이언스)
  - On-Device-AI(온디바이스AI)
  - Model-Compression(모델경량화)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Advanced
  - Reference(참고)
  - Implementation(구현)
  - Time-Complexity(시간복잡도)
  - Best-Practices
  - Prompt-Engineering(프롬프트엔지니어링)
  - ChatGPT
  - Hugging-Face

image: "wordcloud.png"
---

지금까지 다룬 모든 기법은 "모델을 어떻게 만들고 조정하는가"에 관한 것이었습니다. 이 마지막 장은 관점을 바꿔, 이미 학습이 끝난 모델을 실제 서비스에서 **얼마나 빠르게 응답하게 만들 것인가**를 다룹니다. 05장에서 구현한 Self-Attention을 그대로 서비스에 쓰면 사용자가 메시지를 한 글자씩 더 보낼 때마다 이전 전체 문장에 대한 Attention을 처음부터 다시 계산하게 되는데, 이 장은 그 낭비를 없애는 KV Cache에서 출발해 최근 대형 모델들이 채택하는 메모리 절약 기법으로 이어집니다.

## KV Cache — 이미 계산한 결과를 재사용하기

GPT 같은 Causal 모델은 토큰을 한 번에 하나씩 생성합니다. $n$번째 토큰을 생성할 때, 05장의 Attention 계산식 $\text{softmax}(QK^T/\sqrt{d_k})V$을 보면 $K$와 $V$는 이전에 생성된 모든 토큰(1번째부터 $n-1$번째까지)에 대해 매번 새로 계산되고 있습니다. 하지만 이전 토큰들의 Key·Value 벡터는 새 토큰이 추가된다고 해서 값이 바뀌지 않습니다 — 오직 새로 추가된 토큰의 Key·Value만 새로 계산하면 됩니다.

**KV Cache**는 이 사실을 이용해, 한 번 계산한 Key·Value 벡터를 GPU 메모리에 저장해 두고 다음 토큰을 생성할 때 재사용하는 기법입니다.

```python
class KVCache:
    def __init__(self):
        self.k_cache: torch.Tensor | None = None
        self.v_cache: torch.Tensor | None = None

    def update(self, new_k: torch.Tensor, new_v: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if self.k_cache is None:
            self.k_cache, self.v_cache = new_k, new_v
        else:
            self.k_cache = torch.cat([self.k_cache, new_k], dim=1)   # 시퀀스 길이 축으로 이어붙임
            self.v_cache = torch.cat([self.v_cache, new_v], dim=1)
        return self.k_cache, self.v_cache
```

`update`가 호출될 때마다 새로 생성된 토큰 하나 분량의 Key·Value(`new_k`, `new_v`)만 계산해 캐시에 이어붙이고, Attention 계산에는 누적된 전체 캐시를 사용합니다. 이 덕분에 매 토큰 생성 시점의 연산량이 시퀀스 길이에 비례해 매번 새로 계산할 때보다 훨씬 줄어듭니다. 다만 이 캐시 자체가 시퀀스가 길어질수록, 그리고 배치(동시 사용자 수)가 늘어날수록 GPU 메모리를 크게 차지한다는 새로운 병목을 만듭니다 — 뒤에서 다룰 GQA·MLA는 바로 이 메모리 병목을 줄이기 위한 기법입니다.

## Prefill과 Decode — 두 단계의 서로 다른 연산 특성

LLM의 추론은 크게 두 단계로 나뉩니다. **Prefill**은 사용자가 입력한 프롬프트 전체를 한 번에 병렬로 처리해 첫 출력 토큰을 만들기까지의 단계이고, **Decode**는 이후 토큰을 KV Cache를 활용해 하나씩 순차적으로 생성하는 단계입니다. Prefill은 프롬프트 길이만큼의 토큰을 한꺼번에 행렬 연산으로 처리하므로 연산량(compute) 중심이고, Decode는 토큰을 하나씩만 계산하는 대신 캐시 전체를 메모리에서 읽어와야 하므로 메모리 대역폭(memory bandwidth) 중심이라는 서로 다른 병목을 가집니다. 이 특성 차이는 On-Device AI 경량화 시리즈에서 다룰 하드웨어별 최적화 전략과 직결됩니다.

## GQA — Key/Value 헤드 수를 줄이기

05장에서 다룬 Multi-head Attention은 Query, Key, Value 모두 헤드 수만큼 독립적으로 존재합니다. 헤드 수가 많을수록 KV Cache에 저장해야 할 Key·Value의 양도 그만큼 늘어납니다. <strong>GQA(Grouped Query Attention)</strong>는 Query는 기존처럼 헤드마다 독립적으로 유지하되, 여러 Query 헤드가 하나의 Key·Value 헤드를 공유하도록 그룹을 묶습니다.

> Joshua Ainslie, James Lee-Thorp, Michiel de Jong 외, "GQA: Training Generalized Multi-Head Transformer Models from Multi-Head Checkpoints", *arXiv:2305.13245* (2023)

예를 들어 Query 헤드가 32개이고 이를 4개씩 묶어 8개의 그룹으로 만들면, Key·Value 헤드는 32개가 아니라 8개만 있으면 됩니다. 극단적으로 모든 Query 헤드가 Key·Value 헤드 하나를 공유하면 <strong>Multi-Query Attention(MQA)</strong>이 되는데, GQA는 이 MQA(캐시는 가장 작지만 품질 손실이 큼)와 기존 Multi-head Attention(품질은 좋지만 캐시가 큼) 사이의 절충안입니다.

## MLA — Key/Value를 저차원으로 압축하기

<strong>MLA(Multi-head Latent Attention)</strong>는 헤드 수를 줄이는 GQA와 다른 접근을 씁니다. 각 토큰의 Key·Value를 그대로 캐싱하는 대신, 07장에서 다룬 잠재 공간(Latent Space) 개념처럼 훨씬 작은 차원의 잠재 벡터로 압축해 저장하고, 실제 Attention을 계산할 때만 원래 차원으로 복원합니다.

> DeepSeek-AI, "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model", *arXiv:2405.04434* (2024)

캐시에 저장되는 벡터의 차원 자체를 줄이기 때문에, 헤드 수는 그대로 유지하면서도 GQA보다 더 적극적으로 KV Cache 메모리를 절약할 수 있다고 보고되어 있습니다. 다만 압축·복원 연산이 추가되는 만큼 구현 복잡도는 GQA보다 높습니다.

| 기법 | 메모리 절약 방식 | 품질 손실 위험 |
|---|---|---|
| Multi-head Attention(기본) | 없음(모든 헤드 독립) | 없음(기준선) |
| GQA | Query 헤드를 그룹으로 묶어 Key/Value 헤드 수 축소 | 그룹 크기에 비례 |
| MQA | 모든 Query가 Key/Value 헤드 1개 공유 | GQA보다 큼 |
| MLA | Key/Value를 저차원 잠재 벡터로 압축 | 압축률에 비례 |

## Sliding Window Attention — 먼 과거를 아예 보지 않기

또 다른 접근은 캐시를 압축하는 대신, 애초에 참고하는 범위를 제한하는 것입니다. **Sliding Window Attention**은 각 토큰이 전체 시퀀스가 아니라 자신으로부터 일정 거리(윈도우) 안의 토큰에만 Attention을 계산하도록 제한합니다. 아주 먼 과거의 토큰까지 매번 참고할 필요가 없는 과제(예: 최근 대화 맥락이 중요한 챗봇)에서는 이 제한이 성능 손실 없이 캐시와 연산량을 크게 줄여줍니다. 다만 윈도우 밖의 정보가 실제로 필요한 과제(예: 긴 문서 전체를 요약해야 하는 경우)에서는 정보 손실이 발생할 수 있어, 일부 레이어만 Sliding Window를 쓰고 나머지 레이어는 전체 시퀀스를 보게 하는 절충 구조도 흔히 쓰입니다.

## 흔한 오개념 — "GQA·MLA 같은 효율화 기법은 모델 품질을 반드시 희생시킨다"

Key·Value를 줄이거나 압축하면 정보 손실이 발생해 품질이 떨어질 것이라는 직관은 자연스럽지만, 실제로는 "얼마나 줄이는가"와 "사전학습 단계부터 그 구조로 학습했는가"에 따라 결과가 크게 달라집니다. GQA 원 논문은 소수의 추가 학습 스텝(원래 사전학습 연산량의 5% 수준)만으로 기존 Multi-head Attention 모델을 GQA 구조로 업트레이닝해도 품질 저하가 크지 않다는 결과를 보고합니다. MLA를 채택한 DeepSeek-V2 역시 처음부터 그 구조로 사전학습을 진행해 품질과 효율 양쪽을 모두 노렸습니다. 즉 이런 기법들은 "품질을 깎아 속도를 얻는 타협"이라기보다, 애초에 Key·Value가 담아야 하는 정보의 실제 중복도를 줄이는 구조적 설계에 가깝습니다 — 08장에서 LoRA를 다룰 때 짚은 "실제로 필요한 자유도는 원래 차원보다 작다"는 통찰과 같은 계열의 아이디어입니다.

## 시리즈 A를 마치며

00장에서 시작해 여기까지 오면서, Transformer의 수학적 기반(01~02장)부터 아키텍처(03~07장), 학습과 정렬(08~11장), 그리고 서빙 효율화(12장)까지 GPT류 모델의 전체 생애주기를 훑었습니다. 이 시리즈에서 다진 아키텍처 이해는 Vision AI 파운데이션 시리즈(같은 Transformer 구조를 이미지에 적용), On-Device AI 경량화 시리즈(이 장에서 다룬 KV Cache·메모리 문제를 Quantization·Pruning으로 더 깊이 다룸), RAG와 정보검색 시리즈(외부 지식을 검색해 LLM에 제공하는 방법)의 공통 전제가 됩니다.
