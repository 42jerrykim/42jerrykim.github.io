---
collection_order: 1
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[On-Device AI] 01. Pruning — 가지치기로 모델 슬림화하기"
slug: model-pruning-fundamentals
description: "신경망이 과잉 설계되는 이유부터, Fine-grained와 Coarse-grained Pruning의 정확도-가속 트레이드오프, Magnitude 기반 선택, N:M Sparsity, 희소 행렬 저장 방식까지 Pruning의 핵심을 정리합니다."
tags:
  - Pruning(가지치기)
  - Model-Compression(모델경량화)
  - On-Device-AI(온디바이스AI)
  - CNN(Convolutional Neural Network)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - PyTorch
  - Hardware(하드웨어)
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
  - Best-Practices
  - Mobile(모바일)
  - Embedded(임베디드)
  - LLM(Large Language Model)
  - Case-Study
  - Comparison(비교)

image: "wordcloud.png"
---

완전연결 레이어는 원래 모든 노드가 서로 연결되어 있지만, 이 연결 전부가 추론 시점에 똑같이 중요하게 쓰이지는 않습니다. <strong>Pruning(가지치기)</strong>은 중요도가 낮은 연결을 끊어(0으로 만들어) 모델을 경량화하는 기법입니다. 이 장은 왜 이런 가지치기가 가능한지, 그리고 어떤 단위로 얼마나 잘라낼지가 왜 정확도와 하드웨어 가속 사이의 트레이드오프를 만드는지를 다룹니다.

## 왜 가지치기가 가능한가 — Over-parameterization

신경망은 학습이 잘 되기 위해 필요 이상으로 크게(**over-parameterized**) 설계되는 경향이 있습니다. 학습 과정에서는 이 여분의 파라미터가 다양한 경로로 손실을 줄이는 시도를 가능하게 해주지만, 학습이 끝난 뒤 추론 시점에는 모든 가중치가 똑같이 기여하지 않습니다. 모델이 잘 압축된다는 것은 뒤집어 보면 원래 그만큼 <strong>중복성(redundancy)</strong>이 높았다는 뜻이기도 합니다. Convolution 레이어는 완전연결 레이어보다 Pruning에 상대적으로 민감한 편인데, 이는 채널 하나하나가 이미 특정 패턴을 담당하도록 구조화되어 있어 중복이 상대적으로 적기 때문입니다.

## Pruning의 단위 — 세밀할수록 정확하지만 가속은 어렵다

Pruning은 얼마나 세밀한 단위로 잘라내느냐에 따라 성격이 완전히 달라집니다. **Fine-grained(세밀한 단위)** Pruning은 개별 가중치 하나하나를 판단해 제거하므로 정확도 손실이 적지만, 그 결과로 남는 스파스(0이 많은) 패턴이 불규칙해서 일반적인 GPU 하드웨어로 가속하기 어렵습니다. **Coarse-grained(굵은 단위)** Pruning은 채널이나 레이어 전체를 통째로 제거하므로 정확도 손실은 크지만, 규칙적인 형태라 하드웨어 가속이 훨씬 쉽습니다.

이 스펙트럼은 보통 네 단계로 나눠 다룹니다.

| 단위 | 판단 기준 | 정확도 | 가속 용이성 |
|---|---|---|---|
| Fine-grained | 개별 가중치 $\|W\|$ | 높음 | 낮음 |
| Vector-level | 커널 안 행 벡터의 절댓값 합 | 중상 | 중 |
| Kernel-level | 2D 컨볼루션 커널 단위 | 중 | 중상 |
| Channel-level | 입력 채널 전체 | 낮음 | 높음 |

네 방법 모두 "중요도(절댓값 또는 절댓값 합)를 계산 → 임계값(threshold)을 구함 → 임계값 이하를 0으로 만드는 마스크 적용"이라는 동일한 절차를 따르며, 단위가 굵어질수록 같은 sparsity(희소 비율)에서 제거되는 중요도의 총합과 재구성 오차($\|WX-\hat{W}X\|_2^2$)가 커집니다.

## Magnitude 기반 선택 — 절댓값이 작은 것부터 제거

가장 단순하면서도 널리 쓰이는 접근은 **가중치의 절댓값(magnitude)이 작은 것부터 제거**하는 것입니다. 절댓값이 작다는 것은 그 가중치가 출력에 미치는 영향이 작다는 의미로 해석할 수 있기 때문입니다.

```python
import torch

def magnitude_prune(weight: torch.Tensor, sparsity: float) -> torch.Tensor:
    num_prune = int(weight.numel() * sparsity)
    threshold = torch.kthvalue(weight.abs().flatten(), num_prune).values
    mask = weight.abs() > threshold
    return weight * mask

pruned = magnitude_prune(torch.randn(1024, 1024), sparsity=0.5)   # 50%를 0으로
```

`torch.kthvalue`로 절댓값 기준 하위 `sparsity` 비율에 해당하는 임계값을 구한 뒤, 그보다 작은 가중치를 0으로 만드는 마스크를 곱합니다. Element-wise(개별 가중치) 대신 행(row) 전체를 L1-norm이나 L2-norm 기준으로 판단해 통째로 제거하는 Vector 단위 방식도 널리 쓰입니다.

레이어마다 Pruning에 대한 민감도는 다릅니다. 다른 레이어는 고정한 채 한 레이어의 sparsity만 올려가며 정확도 변화를 측정하는 **Sensitivity Scan**으로 민감한 레이어와 둔감한 레이어를 파악해 레이어별로 차등 적용하면, 모든 레이어에 같은 비율을 적용하는 것보다 같은 압축률에서 정확도가 더 잘 유지됩니다. 모델 전체 가중치를 하나의 집합으로 보고 전역 임계값 하나로 자르는 **Global Magnitude Pruning**은 레이어별 차등 효과를 자동으로 얻는 간편한 방법입니다. 목표 sparsity를 한 번에 적용하는 One-shot Pruning보다, 여러 epoch에 걸쳐 비율을 점진적으로 올리는 **Iterative Pruning**이 성능 회복에 유리하며, 초반에는 빠르게 후반에는 천천히 비율을 올리는 Cubic 스케줄이 일반적으로 더 좋은 성능을 보입니다.

## N:M Sparsity — 실전에서 가장 널리 쓰이는 절충안

**N:M Sparsity**는 연속된 $M$개의 값 중 $N$개를 제거하는 방식으로, 실무에서 가장 많이 쓰이는 조합은 4개 중 2개를 제거하는 **2:4 Sparsity**(50% 희소성)입니다. NVIDIA는 Ampere 아키텍처부터 GPU 하드웨어 차원에서 2:4 Sparsity 연산을 직접 지원합니다. 4개 값마다 항상 정확히 2개씩만 남기 때문에 압축 결과가 규칙적인 크기를 가지고, 인덱스도 "4개 중 몇 번째 위치인지"만 표현하면 되므로 2비트로 충분합니다. 이런 규칙성 덕분에 일반적인 비정형(irregular) sparsity와 달리 GPU에서 실질적인 가속(곱셈 연산 수를 절반으로 절감)을 얻을 수 있고, CNN·BERT 등 다양한 모델에서 정확도 손실이 거의 없었다고 보고됩니다.

<strong>Channel Permutation(채널 재배열)</strong>은 Vector-wise Pruning의 정확도를 높이기 위해, Pruning 전에 값이 작은 채널끼리·큰 채널끼리 모이도록 채널 순서를 미리 바꾸는 기법입니다. 다만 한 레이어의 채널 순서를 바꾸면 그 출력이 다음 레이어의 입력이 되므로, 다음 레이어의 입력 채널 순서도 함께 맞춰 수정해야 계산 결과가 원래와 같아집니다.

## 희소 행렬을 저장하는 방법

Pruning으로 많은 값이 0이 된 행렬을 그대로 저장하면 메모리 낭비가 크므로, 0이 아닌 값만 효율적으로 저장하는 압축 포맷이 필요합니다. **CSR(Compressed Sparse Row)**·<strong>CSC(Compressed Sparse Column)</strong>는 0이 아닌 값과 그 위치(행/열 인덱스)만 저장하는 대표적인 포맷입니다. 다만 이런 비정형 포맷은 입력값이 0일 때 연산을 건너뛰도록 지원하는 전용 하드웨어가 있어야 실질적인 속도 이득을 얻을 수 있습니다.

## 실전 활용 — Pruning의 한계와 대안

Unstructured(Element-wise) Pruning은 정확도는 잘 보존되지만 가속을 위해 전용 하드웨어가 필요하고, Structured Pruning(채널·레이어 단위)은 하드웨어 지원이 없어도 바로 속도 이득을 볼 수 있지만 정확도 손실이 큽니다. 이론적으로는 매력적이지만 하드웨어의 지원 없이는 실제로 속도 이득을 보기 어렵기 때문에, 현업에서는 비교적 활용도가 낮은 기법으로 평가받습니다. 그래서 실무에서 가장 널리 쓰이는 조합은 **Structured Pruning으로 모델을 먼저 작게 만든 뒤, Knowledge Distillation(03장)으로 성능을 다시 복원하는** 방식입니다 — Pruning으로 작아진 모델은 처음부터 다시 학습(Fine-tuning)하기가 어렵기 때문에, 원래의 큰 모델을 Teacher로 삼아 지식을 증류받는 편이 훨씬 실용적입니다.

## 흔한 오개념 — "Pruning 비율이 높을수록 무조건 더 좋은 경량화다"

Sparsity 비율(예: 90% Pruning)이 높을수록 모델이 더 가벼워지니 항상 유리하다고 생각하기 쉽지만, 이 절에서 다룬 것처럼 **하드웨어가 그 패턴을 가속할 수 있는지**가 실질적인 이득을 결정합니다. 90% Fine-grained Pruning으로 파라미터 수는 크게 줄었어도, 일반 GPU가 그 비정형 패턴을 가속하지 못하면 실제 추론 속도는 거의 개선되지 않을 수 있습니다. 반대로 50% 2:4 Sparsity는 절대적인 압축률은 더 낮아도, 하드웨어가 직접 지원하는 규칙적인 패턴이라 실질적인 속도 이득으로 이어집니다. "몇 %를 잘라냈는가"보다 "그 패턴을 내 하드웨어가 가속할 수 있는가"가 Pruning 전략을 판단하는 더 정확한 기준입니다.

다음 장에서는 연결을 끊는 대신 각 값을 표현하는 비트 수 자체를 줄이는 Quantization을, Linear Quantization의 계산 과정과 PTQ·QAT의 트레이드오프 중심으로 다룹니다.
