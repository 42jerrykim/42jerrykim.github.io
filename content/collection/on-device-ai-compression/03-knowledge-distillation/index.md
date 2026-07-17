---
collection_order: 3
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[On-Device AI(Series) 03] Knowledge Distillation — Teacher와 Student"
slug: knowledge-distillation-fundamentals
description: "작은 모델이 처음부터 학습되기 어려운 이유부터, Temperature로 만드는 Soft Label, Forward·Reverse KL Divergence의 차이, 중간 레이어를 비교하는 Feature-based KD까지 지식 증류의 핵심을 Hinton 원 논문과 함께 정리합니다."
tags:
  - Knowledge-Distillation(지식증류)
  - Model-Compression(모델경량화)
  - On-Device-AI(온디바이스AI)
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
  - Case-Study(케이스스터디)
---

01~02장에서 다룬 Pruning과 Quantization은 이미 학습된 모델에서 무언가를 "덜어내는" 접근이었습니다. **Knowledge Distillation(지식 증류)**은 방향이 다릅니다 — 작은 모델을 처음부터 잘 학습시키는 것 자체가 어렵다는 문제의식에서 출발해, 이미 잘 학습된 큰 모델의 지식을 작은 모델에 옮겨 담습니다. 이 장은 이 "옮겨 담는" 과정이 구체적으로 어떤 신호를 어떻게 전달하는지를 다룹니다.

## 작은 모델은 왜 학습이 어려운가

큰 모델은 학습 도중 어느 순간 갑자기 성능이 확 좋아지는 구간이 나타나는 경우가 있는 반면, 작은 모델은 그런 도약 없이 전반적으로 불안정한 학습 양상을 보이는 경향이 있습니다. 작은 모델을 정답 레이블만으로 처음부터 학습시키는 것보다, 이미 문제를 잘 푸는 큰 모델의 "풀이 과정에 대한 힌트"를 함께 주는 편이 훨씬 안정적인 학습으로 이어진다는 것이 Knowledge Distillation의 핵심 전제입니다.

## Teacher-Student 구조와 Temperature

복잡한 **선생님(Teacher)** 모델이 먼저 학습되어 있고, 간단한 **학생(Student)** 모델이 선생님의 지식을 전달받습니다. 가장 기본적인 방식은 Teacher와 Student 각각의 **로짓(logit, Softmax 통과 전 출력값)**을 비교해 손실을 구하는 것입니다.

> Geoffrey Hinton, Oriol Vinyals, Jeff Dean, "Distilling the Knowledge in a Neural Network", *arXiv:1503.02531* (2015)

핵심 아이디어는 "Teacher와 Student의 예측 확률분포를 서로 맞춘다"는 것입니다. 이때 LLM 시리즈 06장에서 다룬 **Temperature($T$)**가 다시 등장합니다 — Temperature를 높이면 Softmax 결과가 더 부드러워져, 뾰족한 1등 답 대신 다른 답들의 확률도 드러납니다. 이렇게 부드러워진 분포는 Student에게 "정답이 무엇인지"뿐 아니라 "오답들끼리는 서로 얼마나 비슷한지"에 대한 추가 정보(Hinton은 이를 **Dark Knowledge**라 부릅니다)까지 전달합니다. 예를 들어 숫자 이미지 분류에서 "이 이미지는 7이지만, 1과도 조금 닮았고 9와는 전혀 다르다"는 미묘한 관계 정보가 Soft Label에 담깁니다.

**Soft Label**은 Teacher가 만든 부드러운 확률분포 자체를 정답으로 쓰고, **Hard Label**은 원래의 실제 정답(one-hot)을 그대로 씁니다. 실전에서는 이 둘을 가중합해서 Student를 학습시킵니다.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

def distillation_loss(
    student_logits: torch.Tensor,
    teacher_logits: torch.Tensor,
    labels: torch.Tensor,
    temperature: float = 4.0,
    alpha: float = 0.5,
) -> torch.Tensor:
    soft_teacher = F.log_softmax(teacher_logits / temperature, dim=-1)
    soft_student = F.log_softmax(student_logits / temperature, dim=-1)
    soft_loss = F.kl_div(soft_student, soft_teacher, log_target=True, reduction="batchmean")
    soft_loss = soft_loss * (temperature ** 2)          # 스케일 보정

    hard_loss = F.cross_entropy(student_logits, labels)
    return alpha * soft_loss + (1 - alpha) * hard_loss
```

`soft_loss`에 `temperature ** 2`를 곱하는 이유는, 로짓을 $T$로 나눈 뒤 Softmax를 취하면 손실과 기울기의 크기가 대략 $1/T^2$배로 작아지기 때문입니다. `hard_loss`(Temperature 없는 일반 Cross Entropy)와 균형을 맞추려면 다시 $T^2$을 곱해 스케일을 보정해야 한다는 것이 Hinton 원 논문의 제안입니다.

## Forward KL과 Reverse KL — CNN과 LLM의 차이

Teacher와 Student의 최종 출력(response)만 비교하는 가장 단순한 형태를 **Response-based KD**라 부릅니다. CNN 시절에는 주로 **Forward KL Divergence**($D_{KL}(P_{teacher} \| Q_{student})$)를 사용했지만, LLM에서는 Forward와 **Reverse KL**($D_{KL}(Q_{student} \| P_{teacher})$)을 함께 쓰는 경우가 많습니다.

이 차이는 Teacher의 확률분포가 두 개의 봉우리(쌍봉, bimodal)를 갖고 Student는 봉우리 하나만 표현할 수 있는 상황을 생각하면 이해하기 쉽습니다. Forward KL로 학습하면 Student는 두 봉우리를 동시에 흉내 내려다 오히려 그 중간 지점에 봉우리 하나가 생기는, 어느 쪽도 아닌 애매한 형태로 수렴합니다. Reverse KL로 학습하면 Student는 Teacher의 두 봉우리 중 더 높은 쪽 하나만 선택하고 낮은 봉우리는 과감히 포기하는 형태로 수렴합니다. 다양한 표현이 뒤섞인 LLM의 출력 분포를 다룰 때는, 애매한 중간값보다 뚜렷한 선택을 하는 편이 유리한 경우가 많아 두 방식을 함께 씁니다(둘을 절충한 대칭적 지표로 JS Divergence를 쓰기도 합니다).

## Feature-based KD — 중간 레이어 비교하기

최종 출력이 아니라 **중간 레이어의 출력값(feature map)**을 비교해 손실을 계산하는 방식입니다. 문제는 Teacher와 Student의 feature map 차원이 서로 다르다는 것인데, 이를 해결하는 접근이 여러 갈래로 갈립니다. **FitNet 계열(hint 기반)**은 Student에 회귀(regression) 레이어를 붙여 채널 수를 Teacher와 맞춘 뒤 두 중간 feature map을 MSE Loss로 정렬합니다. **NST(Neuron Selectivity Transfer)**는 정확한 값을 그대로 흉내 내는 대신 비슷한 **분포**를 갖도록 학습하며, 분포 간 차이를 재는 데 MMD(Maximum Mean Discrepancy)를 씁니다. **Factor Transfer**는 feature에서 핵심 요인(factor)만 추출해 전달하는데, 이때 쓰는 Paraphraser는 오토인코더와 비슷하게 차원을 줄였다가 복원하는 과정에서 정말 중요한 정보만 남깁니다.

```python
class FitNetLoss(nn.Module):
    def __init__(self, student_channels: int, teacher_channels: int):
        super().__init__()
        self.regressor = nn.Conv2d(student_channels, teacher_channels, kernel_size=1)

    def forward(self, student_feature: torch.Tensor, teacher_feature: torch.Tensor) -> torch.Tensor:
        aligned = self.regressor(student_feature)   # 채널 수를 Teacher에 맞춤
        return F.mse_loss(aligned, teacher_feature.detach())
```

`teacher_feature.detach()`로 Teacher 쪽 기울기 계산을 차단하는 이유는, Teacher는 이미 학습이 끝난 고정된 모델이고 오직 Student(와 `regressor`)만 학습 대상이기 때문입니다.

## Structural/Functional KD — 값이 아니라 관계를 전달하기

앞선 방법들이 "Teacher의 feature 값 자체"를 흉내 내려 했다면, 이 계열은 **feature들 사이의 관계**를 전달하는 데 초점을 맞춥니다. 레이어를 하나씩 지날 때 값이 어떻게 변화하는지, 또는 ReLU를 통과한 결과의 경계선(activation boundary)이 어떤 모양인지를 흉내 냅니다. **Matching Sparsity Patterns**는 어떤 뉴런이 활성화되고 어떤 뉴런이 죽는지(sparsity 패턴) 자체가 비슷하도록 학습합니다 — feature의 실제 값을 그대로 전달하면 경계 근처의 미세한 값들은 Student가 학습하기 어렵기 때문에, 그 경계 정보 자체를 전달하는 편이 더 안정적입니다. **Matching Relational Information**은 Teacher와 Student의 레이어 개수가 다를 수 있다는 점을 고려해, Residual 모듈을 통과하기 전후로 feature가 어떻게 변화하는지(관계의 변화)를 전달합니다.

## Transformer에 KD 적용하기

Transformer 구조에 KD를 적용할 때는 앞서 다룬 FitNet(Feature-based KD)과 유사한 방식을 씁니다 — Student와 Teacher의 차원이 다르므로 Linear 레이어로 차원을 맞춰가며 학습하고, 학습이 끝난 뒤에는 이 Linear 레이어를 제거하고 사용합니다. 학습 시에만 필요한 "발판" 역할을 하는 것입니다. Vision AI 시리즈 04장에서 다룬 DeiT의 Distillation Token도 이 Response-based KD를 ViT 구조에 적용한 사례입니다.

## 흔한 오개념 — "Soft Label은 Hard Label보다 항상 더 많은 정보를 준다"

Soft Label이 확률분포 전체를 담고 있으니 Hard Label(one-hot)보다 항상 더 유용한 신호를 준다고 생각하기 쉽지만, Vision AI 시리즈 04장에서 다룬 DeiT의 실험 결과는 이 직관과 어긋납니다. DeiT는 Soft Distillation(Teacher의 확률분포를 KL Divergence로 흉내)과 Hard Distillation(Teacher가 가장 확신한 클래스를 명확한 정답처럼 사용)을 비교했을 때, **Hard Distillation 쪽이 더 좋은 성능**을 보였습니다. 부드러운 확률분포가 담은 미묘한 관계 정보가 항상 학습에 도움이 되는 것은 아니며, 오히려 선생님의 확신에 찬 판단을 명확한 신호로 주는 편이 특정 상황(ViT처럼 대량의 데이터·큰 모델)에서는 더 잘 전달될 수 있다는 것을 보여주는 사례입니다.

이것으로 Phase 1(CNN 기초)이 끝났습니다. 다음 장부터는 지금까지 다룬 세 기법이 LLM 규모에서는 왜 더 정교해져야 하는지를, 먼저 LLM Pruning부터 다룹니다.
