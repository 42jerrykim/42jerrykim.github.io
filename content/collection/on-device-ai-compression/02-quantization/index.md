---
collection_order: 2
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[On-Device AI] 02. Quantization — 비트 수를 줄이는 법"
slug: model-quantization-fundamentals
description: "Linear Quantization의 Scale·Zero-point 계산부터 Symmetric·Asymmetric 방식, Static·Dynamic Quantization, PTQ와 QAT의 트레이드오프까지 모델을 저비트로 표현하는 Quantization의 핵심을 정리합니다."
tags:
  - Quantization(양자화)
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

01장의 Pruning이 "연결을 끊는" 방식이라면, <strong>Quantization(양자화)</strong>은 각 값을 표현하는 비트 수를 줄이는 방식입니다. 32비트 부동소수점으로 저장하던 가중치를 8비트나 4비트 정수로 바꾸면, 같은 모델도 저장 공간과 메모리 대역폭 사용량이 그만큼 줄어듭니다. 이 장은 값을 정수로 매핑하는 계산 과정부터, 언제 양자화 파라미터를 계산할지, 그리고 학습을 포함시킬지 여부에 따른 트레이드오프를 다룹니다.

## 왜 BF16 같은 포맷이 등장했는가

소수점을 얼마나 세밀하게 표현하느냐보다, 값의 범위를 얼마나 넓게 표현할 수 있느냐가 실전에서 더 중요한 경우가 많습니다. 일반적인 16비트 부동소수점(FP16)은 32비트(FP32)보다 지수(exponent) 비트를 줄여 표현 범위 자체가 좁아지는 반면, <strong>BF16(bfloat16)</strong>은 지수 비트를 FP32와 동일하게 유지하고 가수(mantissa) 비트만 줄입니다. 정밀도는 다소 떨어지더라도 오버플로우에 강한 넓은 범위를 유지할 수 있어, 최근 LLM 학습·추론에서 기본값처럼 쓰입니다.

## Quantization의 종류

값을 저비트로 매핑하는 방식은 크게 세 갈래로 나뉩니다. **Learned Quantization**은 데이터로부터 양자화 구간(레벨)을 학습하거나 결정합니다 — 예를 들어 K-means 클러스터링으로 비슷한 값끼리 묶어 조회 테이블(lookup table)로 구현합니다. **Uniform(균일) Quantization**은 정수와 실수 사이를 $r = S(q - Z)$ 형태의 아핀(affine) 변환으로 매핑하며, 양자화 구간 사이의 간격이 균일합니다. **Non-Uniform(비균일) Quantization**은 구간 간격이 데이터 분포에 따라 다르게 설정됩니다.

## Static과 Dynamic — 언제 양자화 파라미터를 정할 것인가

가중치(Weight)는 학습이 끝난 시점에 이미 고정된 값을 알고 있으므로, 추론 전에 미리(static) 양자화 파라미터를 계산해둘 수 있습니다. 반면 활성화값(Activation)은 입력에 따라 매번 달라지므로 미리 알 수 없습니다. 그럼에도 실무에서는 대표 입력 데이터로 미리 범위를 추정해두는 <strong>Static 방식(calibration)</strong>이 더 많이 사용됩니다 — 매 추론마다 범위를 다시 계산하는 Dynamic 방식보다 오버헤드가 적기 때문입니다.

## Linear Quantization의 계산

양자화는 실수 값 $r$을 정수 $q$로 바꾸는 과정입니다.

$$q = \mathrm{clamp}\big(\mathrm{round}(r/S) + Z\big), \qquad r = S(q - Z)$$

여기서 $S$(Scale)는 정수 구간과 실수 구간의 비율이고, $Z$(Zero-point)는 원래 값에서 "0"에 해당하는 정수 위치입니다. 양자화 파라미터는 실제 값의 범위로부터 계산합니다.

$$S = \frac{r_{max} - r_{min}}{q_{max} - q_{min}}, \qquad Z = \mathrm{round}\left(q_{min} - \frac{r_{min}}{S}\right)$$

```python
import torch

def linear_quantize(r: torch.Tensor, num_bits: int = 8):
    q_min, q_max = 0, 2**num_bits - 1
    r_min, r_max = r.min(), r.max()
    scale = (r_max - r_min) / (q_max - q_min)
    zero_point = torch.round(q_min - r_min / scale)
    q = torch.clamp(torch.round(r / scale) + zero_point, q_min, q_max)
    return q.to(torch.uint8), scale, zero_point

def dequantize(q: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor) -> torch.Tensor:
    return scale * (q.float() - zero_point)
```

가중치는 분포가 0을 중심으로 거의 대칭이므로, Zero-point를 항상 0으로 고정하고 $S = |W|_{max} / q_{max}$만 구하는 **Symmetric(대칭)** 방식을 주로 씁니다. Symmetric 방식은 Zero-point 계산·저장이 필요 없어 연산이 단순해지는 장점이 있지만, 실제 분포가 대칭이 아닐 경우 **Asymmetric(비대칭)** 방식보다 오차가 커질 수 있습니다.

Weight와 Activation을 각각 저비트로 양자화했다면, 매번 역양자화(dequantization)해서 계산하는 대신 **저비트 상태 그대로 연산**하고, 값이 누적(accumulate)되는 부분에서만 더 높은 정밀도(예: 32비트)로 처리해 오차 누적을 방지하는 방식이 실무에서 널리 쓰입니다.

## Outlier(이상치) 처리 — CNN과 LLM의 차이

값의 분포에서 극단적으로 크거나 작은 outlier를 어떻게 다루느냐도 중요한 설계 지점입니다. CNN 시절에는 outlier를 제거(clipping)하는 방식이 일반적이었습니다. 하지만 LLM에서는 outlier를 단순히 제거하지 않고 <strong>보정(compensate)</strong>해서 사용하는 방식이 선호됩니다 — LLM에서는 특정 채널에 몰린 outlier가 실제로 중요한 정보를 담고 있는 경우가 많기 때문입니다. 이 통찰은 05장에서 다룰 AWQ에서 더 발전된 형태로 다시 등장합니다.

## PTQ와 QAT — 언제 양자화할 것인가

<strong>PTQ(Post-Training Quantization)</strong>는 이미 학습이 끝난 모델에 대해, 추가 학습 없이 소량의 데이터만 사용해 양자화 파라미터만 뽑아냅니다. 작업량(overhead)이 적은 대신 정확도가 다소 떨어질 수 있으며, **AdaRound** 같은 보정 기법으로 정확도를 끌어올릴 수 있습니다. **Per-Channel Weight Quantization**은 텐서 전체에 하나의 Scale을 쓰는 Per-Tensor 방식이 채널마다 값의 범위가 크게 다른 작은 모델에서 문제가 될 수 있어, 채널별로 Scale을 따로 두는 방식입니다(다만 Scale 저장 비용이 채널 수만큼 늘어납니다). **Weight Equalization**은 Per-Channel의 메모리 부담과 Per-Tensor의 낮은 정확도 사이의 절충안으로, 채널 간 값의 범위를 사전에 맞춰주는 기법입니다(활성화 함수가 선형이어야 정확하게 적용 가능합니다).

<strong>QAT(Quantization-Aware Training)</strong>는 가중치를 32비트로 유지하면서, 순전파 과정에서는 저비트로 양자화된 것처럼 계산하고 그 결과로 발생하는 오차를 학습 과정에 반영합니다. 문제는 양자화 함수가 계단(step) 형태라 미분이 불가능하다는 것입니다(기울기가 대부분 0). 그래서 순전파에서는 실제 계단형 양자화 함수를 쓰지만, 역전파에서는 **선형 함수인 것처럼 근사**해 기울기를 흘려보냅니다(Straight-Through Estimator와 유사한 아이디어).

| | PTQ | QAT |
|---|---|---|
| 추가 학습 | 불필요(소량의 calibration 데이터만) | 필요 |
| 비용 | 낮음 | 높음 |
| 정확도 | 상대적으로 낮음(AdaRound 등으로 보정 가능) | 상대적으로 높음 |

## 흔한 오개념 — "양자화 함수는 미분이 안 되니 QAT는 불가능하다"

양자화 함수가 계단 형태라 기울기가 거의 항상 0이라는 사실만 보면, "손실을 역전파로 최소화하는" 일반적인 학습 방식이 QAT에는 적용될 수 없을 것처럼 보입니다. 하지만 QAT는 이 문제를 "정확한 미분"이 아니라 "학습에 유용한 근사"로 우회합니다 — Straight-Through Estimator는 순전파에서는 실제 계단 함수를 쓰되, 역전파에서는 그 계단 함수가 마치 항등함수(기울기 1)인 것처럼 취급해 기울기를 그대로 통과시킵니다. 이는 수학적으로 엄밀한 미분이 아니라 실용적인 근사이지만, 실제로는 이 근사만으로도 양자화로 인한 오차를 학습 과정에 충분히 반영할 수 있다는 것이 QAT가 실무에서 동작하는 이유입니다.

다음 장에서는 Pruning·Quantization과는 다른 세 번째 축인 Knowledge Distillation을, Teacher-Student 구조와 Temperature를 이용한 Soft Label 전달 방식 중심으로 다룹니다.
