---
collection_order: 5
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[On-Device AI 05] LLM Quantization — SmoothQuant와 AWQ"
slug: llm-quantization-fundamentals
description: "LLM Activation의 Outlier가 왜 다루기 어려운지부터, 어려움을 Weight로 옮기는 SmoothQuant, 중요 채널만 보호하는 AWQ, OBS 계열의 GPTQ, QLoRA의 NF4·Double Quantization까지 LLM 전용 Quantization 기법을 정리합니다."
tags:
  - Quantization(양자화)
  - LLM(Large Language Model)
  - LoRA(Low-Rank Adaptation)
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

---

02장에서 다룬 Quantization을 LLM에 그대로 적용하면, CNN에서는 크게 문제 되지 않던 현상이 발목을 잡습니다 — Activation 값의 일부가 극단적으로 커지는 **outlier**입니다. 이 장은 이 outlier를 다루는 여러 접근을 살펴본 뒤, LLM에서는 왜 Weight만 양자화하는 방식이 더 널리 쓰이는지, 그리고 LoRA와 결합한 QLoRA가 어떻게 메모리를 더 아끼는지를 다룹니다.

## 필드에서는 Quantization이 더 많이 쓰인다

01·04장에서 다룬 Pruning과 이 장의 Quantization 중, 실무에서는 **Quantization이 더 널리 사용**됩니다. Pruning은 하드웨어의 지원 없이는 실질적인 속도 이득을 보기 어려운 반면, Quantization은 값을 표현하는 비트 수를 줄이는 것만으로도 메모리 사용량과 메모리 대역폭 사용량이 직접적으로 줄어들기 때문입니다. Weight만 양자화하는(weight-only) 방식에서는 실제 연산 시 Weight를 다시 역양자화(dequantization)해서 계산하는 경우가 많은데, 이는 연산 속도 자체보다는 **메모리를 읽어들이는 속도의 개선**에서 이득을 얻으려는 설계입니다 — LLM 시리즈 12장에서 다룬 Decode 단계의 메모리 바운드 특성을 생각하면, 이 이득이 왜 큰지 이해할 수 있습니다.

## Activation Outlier — LLM PTQ의 핵심 난제

LLM의 Activation을 양자화하는 과정에서 outlier가 많이 발생하는 것이 큰 난제입니다. **ZeroQuant**는 Activation은 값의 범위가 동적으로 크게 변하므로 Static 방식을 그대로 쓰면 정확도가 많이 떨어진다는 점에 착안해, Activation은 토큰(token) 단위로, Weight는 그룹(group) 단위로 양자화합니다. 양자화 과정에서 생기는 오차는 원본 모델을 Teacher로 삼은 지식 증류(03장 참고)로 보정합니다. **LLM.int8()**은 절댓값 최대치(Absolute Maximum) 방식으로 Scale을 결정하는 접근입니다.

## SmoothQuant — 어려움을 Weight 쪽으로 옮기기

**SmoothQuant**는 Activation의 outlier를 다루기 어려우니, 그 어려움을 **Weight 쪽으로 옮겨서** 완화하는 아이디어입니다.

> Guangxuan Xiao, Ji Lin, Mickael Seznec 외, "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models", *arXiv:2211.10438* (2022)

핵심은 간단한 항등식입니다. Activation $a$와 Weight $w$의 곱은 스케일 $s$를 도입해도 값이 변하지 않습니다.

$$w \cdot a = (w \cdot s) \cdot (a / s)$$

Activation은 스케일 $s$로 나누고 Weight는 $s$를 곱하면, 최종 계산 결과는 동일하게 유지되면서 Activation 쪽의 값 범위(range)만 완만하게 만들 수 있습니다. 스케일은 채널별로 다음과 같이 정합니다.

$$s = \frac{\max(|X|)^{\alpha}}{\max(|W|)^{1-\alpha}}$$

$\alpha$(migration strength)는 양자화 난이도를 Activation과 Weight 사이에 얼마나 옮길지 정하는 값으로, 보통 0.5를 씁니다. 이 스케일은 calibration 데이터로 미리 구해 앞단 LayerNorm·Linear의 가중치에 접어 넣을(fusion) 수 있어 추가 런타임 오버헤드가 없습니다.

**OmniQuant**는 SmoothQuant가 별도의 학습 없이 calibration 통계만으로 스케일을 정하는 것과 달리, Shift와 Scale 값을 학습 가능한 파라미터로 두고 **학습을 통해** 최적화합니다. **QuaRot**은 가중치와 Activation을 모두 4비트로 낮춘 W4A4 양자화를 최초로 성공시킨 접근으로(SmoothQuant는 8비트까지는 잘 동작하지만 4비트까지 내리면 무너집니다), 직교 행렬($RR^T = I$)의 성질을 이용해 $y = xW = (xR)(R^T W)$처럼 수식적으로 결과를 보존하면서 **회전(rotation)** 변환으로 특정 채널에 쏠린 outlier를 여러 채널로 고르게 분산시킵니다. **SpinQuant**는 QuaRot과 유사하지만 회전 행렬을 무작위로 두지 않고 학습으로 최적화합니다.

## AWQ — Activation을 기준으로 중요한 Weight 채널 보호하기

**AWQ(Activation-aware Weight Quantization)**는 전체 채널 중 약 1% 내외의 "중요한(salient) 채널"만 원래 정밀도로 유지하고 나머지만 양자화하면 정확도를 잘 지킬 수 있다는 발견에 기반합니다.

> Ji Lin, Jiaming Tang, Haotian Tang 외, "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration", *arXiv:2306.00978* (2023)

어떤 채널이 중요한지는 **Weight 자체의 크기가 아니라 Activation의 분포**를 보고 결정합니다 — Weight 크기로 고르면 무작위 선택과 별 차이가 없다는 것이 논문의 관찰입니다(Activation 쪽 정보를 활용한다는 것이 이름의 유래). 다만 1%만 원래 정밀도로 남기는 혼합 정밀도(mixed precision)는 하드웨어 구현이 까다롭기 때문에, 실제 AWQ는 중요한 채널을 그대로 보존하는 대신 **양자화 전에 스케일 $s$를 곱해 키우고 양자화 후 다시 $s$로 나누는** 방식으로 보호합니다.

```python
import torch

def awq_protect_channel(weight: torch.Tensor, channel_idx: int, s: float, quantize_fn):
    weight = weight.clone()
    weight[:, channel_idx] *= s              # 중요 채널을 양자화 전에 확대
    weight = quantize_fn(weight)              # 양자화 (그룹 내 다른 값들 영향은 미미)
    weight[:, channel_idx] /= s              # 양자화 후 원래 스케일로 복원
    return weight
```

그룹 크기가 충분히 크면(예: 128) $s$를 곱해도 그룹 내 최댓값(양자화 간격 $\Delta$)이 거의 변하지 않으므로, 해당 채널의 양자화 오차는 대략 $1/s$배로 줄어듭니다 — SmoothQuant와 같은 원리를 weight-only 양자화에 적용한 것입니다. 최적의 스케일은 Activation 크기의 거듭제곱 $s = s_X^{\alpha}$ 형태로 두고, $\alpha$를 grid search로 찾습니다.

## Weight-Only Quantization의 다른 계열 — GPTQ, SpQR

**GPTQ**는 04장에서 다룬 SparseGPT와 유사한 방식(OBS 계열)을 Pruning이 아니라 Quantization에 적용한 기법입니다.

> Elias Frantar, Saleh Ashkboos, Torsten Hoefler, Dan Alistarh, "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers", *arXiv:2210.17323* (2022)

**SpQR**은 Weight 중에서 outlier(=중요한 weight)에 집중하는 방식으로, GPTQ와 유사한 방법으로 outlier를 찾아냅니다. 흥미롭게도 outlier는 무작위로 흩어져 있는 것이 아니라 특정 채널이나 행(row)에 몰려있는 경향이 있습니다 — 이는 AWQ가 "중요한 채널"이라는 개념으로 접근한 것과 같은 관찰입니다.

## QLoRA — Quantization과 LoRA의 결합

LLM 시리즈 08장에서 다룬 QLoRA를 이 장의 관점에서 다시 보면, 원본 모델을 4비트로 양자화해 메모리를 아끼고 그 위에 LoRA를 얹어 학습하는 조합입니다.

> Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer, "QLoRA: Efficient Finetuning of Quantized LLMs", *arXiv:2305.14314* (2023)

QLoRA가 쓰는 **NF4(NormalFloat4)**는 모델 가중치가 정규분포를 따른다는 가정 아래, 값이 몰린 구간은 촘촘하게 값이 드문 구간은 성글게 양자화 레벨을 배치합니다 — 각 구간을 적분한 넓이가 같아지도록 설계되어, 균일 양자화보다 실제 가중치 분포에 더 잘 들어맞습니다. **Double Quantization(이중 양자화)**은 한 걸음 더 나아가, 64개의 파라미터가 공유하는 32비트 스케일 값 자체를 다시 한 번 양자화합니다(256개를 그룹으로 묶어) — 다만 그만큼 연산 속도에는 약간의 손해가 있습니다.

## 흔한 오개념 — "LLM은 CNN보다 Quantization에 더 강하다"

LLM이 방대한 파라미터를 가진 만큼 몇 개의 값을 거칠게 양자화해도 잘 버틸 것이라 생각하기 쉽지만, 이 장에서 다룬 SmoothQuant·AWQ·QuaRot 같은 기법들이 등장한 이유 자체가 **LLM이 CNN보다 오히려 Quantization에 더 취약한 지점(Activation Outlier)을 갖고 있기 때문**입니다. CNN 시절에는 outlier를 그냥 잘라내도(clipping) 큰 문제가 없었지만, LLM에서는 특정 채널에 몰린 outlier가 실제로 중요한 정보를 담고 있어 그냥 잘라내면 성능이 크게 떨어집니다. 이 장에서 다룬 기법들이 하나같이 "outlier를 제거하지 않고 다른 곳으로 옮기거나(SmoothQuant, QuaRot) 별도로 보호하는(AWQ, SpQR)" 전략을 취하는 이유가 바로 이것입니다 — LLM 양자화의 어려움은 파라미터 수가 아니라 값의 분포 특성에서 온다는 것이 핵심입니다.

다음 장에서는 압축이 아닌 다른 축으로 넘어가, Attention 연산과 Decode 단계 자체를 빠르게 만드는 Speculative Decoding·FlashAttention 같은 추론 가속 기법을 다룹니다.
