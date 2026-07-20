---
collection_order: 1
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[Vision AI] 01. 비전을 위한 배경지식 — 카메라와 확률통계"
slug: vision-background-knowledge
description: "카메라 센서가 이미지를 만드는 ISP 파이프라인부터, 행렬-벡터 곱의 가중합 해석, Likelihood와 Bayes' Rule, MLE·MAP, Entropy까지 컴퓨터 비전에 필요한 배경지식을 코드와 함께 정리합니다."
tags:
  - Computer-Vision
  - Machine-Learning(머신러닝)
  - Deep-Learning(딥러닝)
  - Neural-Network
  - AI(인공지능)
  - PyTorch
  - Data-Science(데이터사이언스)
  - CNN(Convolutional Neural Network)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Reference(참고)
  - Implementation(구현)
  - Hardware(하드웨어)
  - Camera
  - Image-Processing
  - Comparison(비교)
  - Time-Complexity(시간복잡도)
  - Transformer
  - Attention(어텐션)
  - Advanced
  - Case-Study
  - Technology(기술)

image: "wordcloud.png"
---

LLM 시리즈에서는 텍스트가 토큰 ID로 바뀐 뒤 임베딩되는 과정을 다뤘습니다. 비전 모델의 입력은 그 이전 단계, 즉 빛이 카메라 센서를 거쳐 픽셀값의 배열이 되는 과정에서 이미 여러 가공을 거칩니다. 이 장은 그 가공 과정을 간단히 짚은 뒤, CNN·ViT를 이해하는 데 필요한 벡터·확률통계의 직관을 정리합니다.

## 카메라와 이미지 신호 처리 파이프라인

카메라의 **이미지 센서**는 빛을 전기 신호로 변환합니다. 이 원본 신호는 그대로 쓸 수 있는 형태가 아니라서, **ISP(Image Signal Processing)** 파이프라인을 거쳐 사람이 보기 좋은 이미지로 가공됩니다 — 예를 들어 일정 값 이하의 신호는 검은색으로 간주하거나, 비어있는 색상 값을 주변 픽셀값으로 채우는 보간 처리를 거칩니다.

이렇게 만들어진 RGB 이미지를 모델에 넣으려면 몇 가지 변환이 더 필요합니다. 이미지는 보통 `(Height, Width, Channel)` 순서(HWC)로 저장되지만, 딥러닝 프레임워크는 채널을 앞으로 보낸 `(Channel, Height, Width)`(CHW) 순서를 기대합니다. 여기에 픽셀값을 0~1 범위로 바꾸고 채널별 평균·표준편차로 정규화하는 과정이 더해집니다.

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),      # 데이터 증강: 무작위로 잘라내기
    transforms.RandomHorizontalFlip(),          # 데이터 증강: 좌우 반전
    transforms.ToTensor(),                       # PIL 이미지 -> 0~1 범위의 CHW 텐서
    transforms.Normalize(mean=(0.4914, 0.4822, 0.4465), std=(0.2470, 0.2435, 0.2616)),
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.4914, 0.4822, 0.4465), std=(0.2470, 0.2435, 0.2616)),
])
```

학습용 파이프라인에만 `RandomCrop`·`RandomHorizontalFlip` 같은 <strong>데이터 증강(augmentation)</strong>을 넣는 이유는, 모델이 같은 물체를 위치·방향이 조금씩 다른 형태로도 인식하도록 강제해 과적합을 줄이기 위해서입니다. 평가(test) 시에는 이런 무작위성이 결과를 흔들면 안 되므로 `ToTensor`와 `Normalize`만 적용합니다.

## 행렬-벡터 곱은 결국 가중합이다

벡터의 스칼라 곱은 방향은 그대로 두고 크기만 바꿉니다. 두 벡터 $A$, $B$에 대해 $\alpha A + (1-\alpha)B$($0 \le \alpha \le 1$)를 계산하면, $\alpha$ 값에 따라 $A$와 $B$를 잇는 직선 위의 한 점을 표현할 수 있습니다 — 이를 <strong>가중합(weighted sum)</strong>이라 부릅니다.

이 가중합 개념은 행렬-벡터 곱셈을 이해하는 열쇠입니다. 행렬 $C$와 벡터 $\vec{a}$의 곱 $C\vec{a}$는 "행과 열을 하나씩 내적한다"는 기계적 계산으로도 볼 수 있지만, **$C$의 각 열(column)을 $\vec{a}$의 각 원소로 가중합한 것**이라는 관점으로 보면 더 직관적입니다.

```python
import numpy as np

C = np.array([[1, 0, 2],
              [0, 1, 3]])
a = np.array([2, 1, 0.5])

result_matmul = C @ a                                    # 기계적 계산
result_weighted_sum = a[0]*C[:, 0] + a[1]*C[:, 1] + a[2]*C[:, 2]  # 열벡터의 가중합

print(np.allclose(result_matmul, result_weighted_sum))   # True
```

이 관점은 LLM 시리즈 05장에서 다룬 Attention의 $\text{weights} \cdot V$ 계산과 정확히 같은 구조입니다 — Attention Score(가중치)로 Value 벡터들을 얼마씩 섞을지 정하는 것도 결국 가중합입니다.

## Norm — 벡터의 크기를 재는 여러 방법

벡터의 크기를 재는 방법은 하나가 아닙니다.

| Norm | 정의 | 별칭 |
|---|---|---|
| 1-노름 | 각 성분 절댓값의 합 | 직각보행(Manhattan) 거리 |
| 2-노름 | $\sqrt{\sum x_i^2}$ (유클리드 거리) | 그냥 "노름"이라 하면 보통 이것 |
| 무한대 노름 | 성분 중 절댓값이 가장 큰 값 | — |

05장에서 다룰 Faster R-CNN의 바운딩 박스 회귀 손실이 1-노름(L1 Loss)을 쓰는 이유도, 좌표 차이를 "직각으로만 이동하는 거리"로 다루는 것이 이상치(outlier)에 덜 민감하기 때문입니다.

## Gradient(기울기) — 가장 가파르게 증가하는 방향

$\nabla$(나블라)가 붙은 표기는 함수를 각 변수에 대해 편미분한 값들을 모아놓은 벡터를 의미합니다. **Gradient는 벡터**이며, 그 함수가 가장 가파르게 증가하는 방향을 가리킵니다. LLM 시리즈 02장에서 다룬 경사하강법이 "$-$Gradient 방향으로 이동"하는 이유도, Gradient의 반대 방향이 손실을 가장 빠르게 줄이는 방향이기 때문입니다.

## Likelihood와 Bayes' Rule — 학습이란 무엇을 찾는 과정인가

**Likelihood(가능도)는 확률이 아닙니다.** "관측된 데이터가 분포 A에서 나왔을 가능성이 높은가, 분포 B에서 나왔을 가능성이 높은가"를 비교하는 지표이지, 그 자체로 확률값은 아닙니다. 이 개념은 <strong>베이즈 정리(Bayes' Rule)</strong>로 학습 문제를 표현할 때 등장합니다.

$$\underbrace{P(\theta|D)}_{\text{Posterior}} = \frac{\overbrace{P(D|\theta)}^{\text{Likelihood}} \cdot \overbrace{P(\theta)}^{\text{Prior}}}{\underbrace{P(D)}_{\text{Evidence}}}$$

여기서 $D$는 학습 데이터(이미지와 정답 레이블의 쌍들), $\theta$는 모델 파라미터입니다. "학습 데이터 $D$가 주어졌을 때 파라미터 $\theta$가 어떤 값을 가질 확률분포인가"를 구하는 것이 Posterior를 구하는 일이지만, 딥러닝 모델의 파라미터는 보통 수백만~수십억 개에 달해 이 분포를 직접 계산하는 것은 현실적으로 불가능합니다.

<strong>MLE(Maximum Likelihood Estimation)</strong>는 이 문제를 우회해, Posterior 전체 대신 **Likelihood를 가장 크게 만드는 파라미터 $\theta$ 하나**만 찾습니다. 여러 후보 $\theta$ 값 각각에 대해 "이 $\theta$였다면 관측된 데이터 $D$가 나올 가능성"을 비교해서, 그 가능성이 가장 큰 $\theta$를 선택하는 것 — 이것이 바로 우리가 실제로 하는 "모델 학습"의 정체입니다. <strong>MAP(Maximum A Posteriori)</strong>는 여기에 Prior(사전 확률)를 곱해, "파라미터 값은 너무 크지 않은 게 낫다"처럼 데이터를 보기 전부터 가진 선험적 믿음까지 반영합니다.

## Entropy — 얼마나 예측 불가능한가

**Entropy**는 "어떤 결과를 인코딩할 때 필요한 평균 최소 비트 수"로 정의됩니다. 직관적으로는, 자주 일어나는 사건은 짧은 코드로, 드문 사건은 긴 코드로 표현하는 것이 평균적으로 가장 효율적인 전송 방법이라는 통찰에서 나옵니다.

$$H(X) = \sum_x P(x) \cdot \left(-\log P(x)\right)$$

$-\log P(x)$는 확률이 1(항상 일어남)에 가까울수록 0에 가깝고, 확률이 0에 가까울수록(드문 사건) 커지는 값으로, 그 사건에 필요한 "코드 길이"에 해당합니다. 이 코드 길이를 확률로 가중평균한 것이 Entropy이며, **Entropy가 높다는 것은 결과를 예측하기 어렵다(불확실성이 크다)는 뜻**입니다. LLM 시리즈 01장에서 다룬 KL Divergence와 Cross Entropy도 이 Entropy 개념 위에, "정답 분포와 예측 분포가 얼마나 다른가"를 얹은 것입니다.

## 흔한 오개념 — "Likelihood와 확률은 같은 말이다"

두 용어를 같은 의미로 섞어 쓰는 경우가 많지만, 수학적으로는 "무엇을 고정하고 무엇을 변수로 보는가"가 다릅니다. 확률 $P(D|\theta)$는 파라미터 $\theta$를 고정한 채 데이터 $D$가 변할 때의 함수이고(데이터 공간에서 적분하면 1이 됨), Likelihood는 반대로 관측된 데이터 $D$를 고정한 채 파라미터 $\theta$를 변화시키며 보는 같은 수식입니다(파라미터 공간에서 적분해도 1이 되지 않습니다). 이 차이 때문에 "이 데이터가 나올 확률이 0.7이다"는 말은 성립해도, "이 파라미터의 Likelihood가 0.7이다"를 "이 파라미터가 맞을 확률이 70%다"로 해석하는 것은 오류입니다 — 정확한 해석은 "다른 파라미터 후보들과 비교했을 때 상대적으로 더 그럴듯하다"는 것입니다.

다음 장에서는 이 배경지식을 바탕으로, 완전연결 신경망(DNN)이 왜 이미지 처리에 한계를 갖고, Convolution이 그 한계를 어떻게 풀어내는지를 다룹니다.
