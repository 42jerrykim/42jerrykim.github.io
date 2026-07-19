---
collection_order: 4
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[On-Device AI] 04. LLM을 위한 Pruning — OBS와 SparseGPT"
slug: llm-pruning-fundamentals
description: "단순 절댓값 기준 Pruning이 LLM에서 왜 부족한지부터, 테일러 급수 기반 OBD·OBS, 이를 레이어 단위로 확장한 SparseGPT, Activation 크기까지 고려하는 Wanda까지 LLM 전용 Pruning 기법을 원 논문과 함께 정리합니다."
tags:
  - Pruning(가지치기)
  - LLM(Large Language Model)
  - Model-Compression(모델경량화)
  - On-Device-AI(온디바이스AI)
  - Transformer
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
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
  - Comparison(비교)
  - Hardware(하드웨어)
  - Mobile(모바일)
  - Embedded(임베디드)
  - Beginner
  - Case-Study
  - Technology(기술)
  - Best-Practices

image: "wordcloud.png"
---

01장에서 다룬 절댓값(magnitude) 기준 Pruning은 단순하고 빠르지만, LLM처럼 파라미터가 방대하고 서로 복잡하게 얽힌 모델에서는 정교함이 부족합니다. 이 장은 "이 가중치를 제거하면 손실이 얼마나 늘어나는가"를 더 정밀하게 근사하는 방법에서 출발해, 이를 LLM 규모에서 실제로 계산 가능하게 만든 SparseGPT까지 다룹니다.

## 왜 절댓값 기준으로는 부족한가

01장의 magnitude 기반 Pruning은 "가중치 하나하나의 절댓값이 작으면 그 가중치는 중요하지 않다"고 가정합니다. 하지만 이 가정은 가중치들 사이의 **상호작용**을 무시합니다. 어떤 가중치가 절댓값은 작아도 다른 가중치와 결합했을 때 손실에 큰 영향을 줄 수 있고, 반대로 절댓값이 커도 다른 가중치가 그 역할을 상당 부분 대신하고 있어 제거해도 손실 변화가 작을 수 있습니다. LLM처럼 파라미터 수가 많고 가중치 간 상호작용이 복잡한 모델에서는 이 단순 가정의 오차가 누적되어 성능 저하가 커집니다.

## 테일러 급수로 제거 오차 근사하기 — OBD와 OBS

이 문제를 개선하기 위해 **테일러 급수(Taylor Expansion)**로 "가중치를 제거했을 때 손실이 얼마나 늘어나는가"를 더 정밀하게 근사하는 방법들이 1990년대부터 제안되었습니다. **OBD(Optimal Brain Damage)**는 테일러 급수의 2차(second-order) 항까지 고려해 가중치 제거로 인한 오차를 근사하되, 계산을 단순화하기 위해 서로 다른 가중치 $i \ne j$ 사이의 상호작용 항은 무시합니다(가중치들이 서로 독립적이라는 가정). **OBS(Optimal Brain Surgeon)**는 OBD가 무시했던 이 $i \ne j$ 항(서로 다른 가중치 간의 상호작용)까지 고려해 OBD를 개선한 버전입니다. OBS는 계산이 더 정교한 만큼 연산 비용도 커서, 파라미터 수가 방대한 LLM에 그대로 적용하기에는 현실적인 제약이 있었습니다.

## SparseGPT — OBS를 LLM 규모로 확장하기

**SparseGPT**는 OBS 아이디어를 기반으로 하되, LLM 규모에서 실제로 계산 가능하도록 재구성한 LLM 전용 Pruning 기법입니다.

> Elias Frantar, Dan Alistarh, "SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot", *arXiv:2301.00774* (2023)

LLM은 워낙 크기 때문에, **레이어 단위로 독립적으로 분석**해 처리 가능하게 만드는 것이 핵심입니다. 기존 OBS 방식의 문제는, 가중치 하나를 제거(업데이트)하면 모델 전체가 바뀌므로 다음 가중치를 위한 계산(헤시안의 역행렬 $H^{-1}$)을 매번 새로 구해야 한다는 것이었습니다. SparseGPT는 **마스크(어떤 가중치를 제거할지)를 먼저 한 번에 결정**하고, 남은 가중치의 **재구성(reconstruction)** 과정을 분리해 이 문제를 해결합니다. 마스크를 정한 뒤 가중치 행렬을 열(column) 단위로 순차 처리하면서, 제거된 영역의 나머지 값들을 $H^{-1}$을 이용해 업데이트하고, $H^{-1}$ 자체도 제거된 영역을 반영해 갱신합니다. 이 방식으로 SparseGPT는 GPT 계열 모델을 재학습 없이 한 번에(one-shot) 50% 이상의 sparsity로 압축할 수 있음을 보였습니다.

## Wanda — Activation까지 함께 보는 휴리스틱

**Wanda**(Weights **and** Activations)는 SparseGPT보다 훨씬 단순한 계산으로, magnitude 방식보다 좋은 성능을 내는 휴리스틱 방법입니다.

> Mingjie Sun, Zhuang Liu, Anna Bair, J. Zico Kolter, "A Simple and Effective Pruning Approach for Large Language Models", *arXiv:2306.11695* (2023)

가중치의 절댓값만 보는 magnitude 방식과 달리, Wanda는 그 가중치에 실제로 곱해지는 입력(Activation)의 크기까지 함께 고려합니다. 중요도는 다음과 같이 계산됩니다.

$$\text{importance}(w_{ij}) = |w_{ij}| \times \|X_j\|_2$$

여기서 $\|X_j\|_2$는 calibration 데이터를 흘려보내며 수집한 해당 입력 채널 activation의 L2 norm입니다. LLM에서는 특정 채널에 항상 큰 값이 곱해지는 패턴이 존재하기 때문에, 가중치 크기만 보지 않고 그 채널의 activation 크기까지 반영하면 훨씬 정확한 중요도 추정이 가능합니다.

```python
import torch

def wanda_importance(weight: torch.Tensor, activation_norm: torch.Tensor) -> torch.Tensor:
    # weight: (out_features, in_features), activation_norm: (in_features,)
    return weight.abs() * activation_norm.unsqueeze(0)   # 채널별 activation 크기를 반영

def wanda_prune(weight: torch.Tensor, activation_norm: torch.Tensor, sparsity: float) -> torch.Tensor:
    importance = wanda_importance(weight, activation_norm)
    num_prune = int(weight.shape[1] * sparsity)                        # 행(row)별로 동일 비율 적용
    threshold = torch.kthvalue(importance, num_prune, dim=1, keepdim=True).values
    mask = importance > threshold
    return weight * mask
```

`activation_norm`은 실제 모델을 calibration 데이터로 한 번 실행해 각 입력 채널의 activation L2 norm을 미리 수집해 둔 값입니다. `wanda_prune`은 행(출력 뉴런)별로 동일한 비율로 Pruning을 적용하며, 가중치 업데이트나 재학습 없이도 단순 magnitude 방식보다 훨씬 좋은 성능(perplexity)을 보였다고 보고됩니다. 다만 계산이 간단한 대신, Pruning 비율이 50%를 넘어가면 오차가 급격히 커지는 한계가 있습니다.

## LLM Pruning 기법 비교

| 기법 | 고려하는 정보 | 재학습 필요 여부 | 계산 비용 |
|---|---|---|---|
| Magnitude(01장) | 가중치 절댓값만 | 불필요 | 매우 낮음 |
| OBS | 가중치 간 2차 상호작용(헤시안) | 불필요 | 매우 높음(LLM 규모에 비현실적) |
| SparseGPT | OBS를 레이어 단위로 근사 | 불필요(One-shot) | 중간 |
| Wanda | 가중치 절댓값 × Activation 크기 | 불필요 | 낮음 |

## 흔한 오개념 — "더 정교한 근사(OBS)일수록 실무에 항상 더 유리하다"

OBS가 OBD보다, SparseGPT가 magnitude 방식보다 이론적으로 더 정확한 근사를 쓰니 실무에서도 항상 우월할 것이라 생각하기 쉽지만, 실제 선택은 **정확도와 계산 비용의 트레이드오프**로 결정됩니다. Wanda가 SparseGPT보다 훨씬 단순한 계산으로도 준수한 성능을 내는 것은, LLM 가중치 Pruning에서 "가중치 간의 정교한 2차 상호작용"보다 "그 가중치에 실제로 곱해지는 activation의 크기"라는 상대적으로 값싼 정보만으로도 상당 부분의 이득을 얻을 수 있다는 것을 보여줍니다. 다만 Wanda는 50% 이상의 높은 sparsity에서 성능이 급격히 나빠지는 한계가 있으므로, 목표 압축률이 낮다면 Wanda의 간편함이, 목표 압축률이 매우 높다면 SparseGPT의 정교함이 유리한 식으로 목표 sparsity에 따라 선택이 달라져야 합니다.

다음 장에서는 같은 논리를 Quantization에 적용해, LLM에서 유독 다루기 어려운 Activation의 Outlier 문제를 SmoothQuant와 AWQ가 각각 어떻게 우회하는지를 다룹니다.
