---
collection_order: 4
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[Vision AI 04] ViT의 변형들 — DeiT, Swin, CLIP, DINO"
slug: vit-variants
description: "ViT의 데이터 효율성을 지식 증류로 보완한 DeiT, 연산량을 윈도우 기법으로 줄인 Swin, 자연어로 지도학습하는 CLIP, 레이블 없이 자기 증류로 학습하는 DINO까지 4가지 ViT 변형을 원 논문과 함께 다룹니다."
tags:
  - Vision-Transformer(ViT)
  - Computer-Vision
  - Transformer
  - Attention(어텐션)
  - Knowledge-Distillation(지식증류)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - PyTorch
  - Data-Science(데이터사이언스)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Advanced
  - Reference(참고)
  - Comparison(비교)
  - Case-Study(케이스스터디)
  - Beginner
  - Case-Study
  - Technology(기술)
  - Best-Practices
  - Implementation(구현)
  - Time-Complexity(시간복잡도)

---

03장에서 다룬 원조 ViT는 성능을 내려면 대량의 사전학습 데이터가 필요하고, 모든 패치 쌍 사이의 관계를 계산해야 해서 연산량이 이미지 크기의 제곱으로 늘어나며, 레이블링 비용도 여전히 큽니다. 이 장에서 다루는 네 가지 변형 — DeiT, Swin, CLIP, DINO — 은 각각 이 세 가지 제약 중 하나 이상을 겨냥해 등장했습니다.

## DeiT — 지식 증류로 데이터 효율 높이기

**DeiT(Data-efficient Image Transformer)**는 "작은 데이터셋에서도 CNN보다 좋은 성능을 내보자"는 목표로, 학습 전략 튜닝과 **지식 증류(Knowledge Distillation)**를 조합합니다.

> Hugo Touvron, Matthieu Cord, Matthijs Douze 외, "Training data-efficient image transformers & distillation through attention", *arXiv:2012.12877* (2020)

증류(Distillation)라는 이름은 불순물이 섞인 상태를 순수하게 정제하는 화학의 증류 공정에서 따온 것으로, 학습에는 **선생님(Teacher) 모델**과 **학생(Student) 모델**이 함께 필요합니다. DeiT는 원래 있던 CLS 토큰과 별개로 **Distillation Token**을 하나 더 추가해, 이 토큰이 선생님 모델의 출력을 따라가도록 학습시킵니다.

DeiT는 증류 방식을 두 가지로 실험합니다. **Soft Distillation**은 선생님의 출력 확률분포와 학생의 출력을 비교하는 KL Divergence 항과, 실제 정답과 비교하는 Cross Entropy 항을 가중합해 손실을 구성합니다. **Hard Distillation**은 선생님이 가장 확률 높다고 판단한 클래스(hard label)를 정답처럼 직접 반영합니다. 논문의 실험 결과는 Hard Distillation 쪽이 더 좋은 성능을 보였습니다 — 부드러운 확률분포를 흉내 내는 것보다, 선생님의 확신에 찬 판단을 명확한 신호로 주는 편이 오히려 더 잘 전달됐다는 뜻입니다.

## Swin Transformer — 윈도우로 연산량 줄이기

ViT의 Self-Attention은 모든 패치 쌍 사이의 관계를 계산하므로 연산량이 이미지 크기에 대해 제곱으로 늘어납니다. **Swin Transformer**는 패치들을 더 큰 단위인 **윈도우(Window)**로 묶고, 윈도우 내부의 패치들끼리만 Attention을 계산해 이 연산량을 줄입니다.

> Ze Liu, Yutong Lin, Yue Cao 외, "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows", *arXiv:2103.14030* (2021)

문제는 윈도우 내부로만 Attention을 제한하면 윈도우 경계를 넘어서는 관계를 놓친다는 것입니다. Swin은 **SW-MSA(Shifted Window Multi-head Self-Attention)**로 이를 보완합니다 — 레이어마다 윈도우의 경계를 이동(shift)시켜, 이전 레이어에서는 서로 다른 윈도우에 있던 패치들이 다음 레이어에서는 같은 윈도우에 속하도록 만듭니다. 윈도우를 이동시키면 이미지 경계에 크기가 맞지 않는 자투리 조각이 생기는데, 이를 처리하기 위해 반대편 끝을 이어붙이는 **Cyclic Shift** 기법을 쓰고, 이때 원래 이웃하지 않았던 영역끼리는 서로 학습되지 않도록 마스킹을 적용합니다.

또한 원조 ViT는 입출력 shape이 일정하게 유지되는 반면, Swin은 CNN처럼 레이어를 지날수록 공간 크기는 줄고 채널 수는 늘어나는 피라미드 구조를 갖습니다. 이는 CNN의 계층적 특징 추출이라는 장점과 Transformer의 유연함을 결합한 설계입니다.

| | ViT | Swin Transformer |
|---|---|---|
| Attention 범위 | 전체 패치(전역) | 윈도우 내부(지역) + Shift로 경계 보완 |
| 레이어별 shape | 입출력 동일하게 유지 | CNN처럼 공간 축소·채널 증가(피라미드) |
| 연산량 증가 | 이미지 크기의 제곱 | 윈도우 크기에 따라 선형에 가깝게 조절 |

## CLIP — 자연어의 지도 아래 이미지 학습하기

이미지를 사람이 일일이 라벨링하는 것은 비용이 크지만, 인터넷에는 이미지와 그에 딸린 텍스트(캡션) 쌍이 이미 방대하게 존재합니다. **CLIP**은 이런 (이미지, 텍스트) 쌍으로 레이블링 없이 자연어의 지도(supervision) 아래 이미지 표현을 학습합니다.

> Alec Radford, Jong Wook Kim, Chris Hallacy 외, "Learning Transferable Visual Models From Natural Language Supervision", *arXiv:2103.00020* (2021)

CLIP은 이미지 인코더와 텍스트 인코더를 각각 통과시켜 임베딩을 얻은 뒤, **대조 학습(Contrastive Learning)**으로 학습합니다. 배치 안에서 짝이 맞는 (이미지, 텍스트) 쌍은 임베딩이 서로 비슷한 방향을 향하도록, 짝이 맞지 않는 쌍은 방향이 다르도록 학습합니다. 이를 행렬로 표현하면 대각선(정답 쌍)의 유사도는 크게, 나머지(오답 쌍)의 유사도는 작게 만드는 것이 목표입니다.

```python
import torch
import torch.nn.functional as F

def clip_contrastive_loss(image_emb: torch.Tensor, text_emb: torch.Tensor, temperature: float = 0.07) -> torch.Tensor:
    image_emb = F.normalize(image_emb, dim=-1)
    text_emb = F.normalize(text_emb, dim=-1)
    logits = image_emb @ text_emb.T / temperature   # (batch, batch) 유사도 행렬
    labels = torch.arange(logits.size(0))            # 대각선이 정답 쌍
    loss_i2t = F.cross_entropy(logits, labels)
    loss_t2i = F.cross_entropy(logits.T, labels)
    return (loss_i2t + loss_t2i) / 2
```

`logits`의 대각선 원소가 정답 쌍(같은 인덱스의 이미지-텍스트)의 유사도이므로, `labels`를 `[0, 1, 2, ...]`로 두고 Cross Entropy를 적용하면 대각선의 유사도를 높이고 나머지를 낮추는 방향으로 학습됩니다. CLIP은 학습 시 자연어 "문장"으로 학습했기 때문에, 추론 시에도 단어 하나만 넣기보다 문장 형태로 넣어야 성능이 잘 나옵니다. 인터넷에서 흔히 볼 수 있는 유형의 이미지에는 별도 학습 없이도(Zero-shot) 잘 동작했다는 것이 논문의 핵심 결과 중 하나입니다.

## DINO — 레이블 없는 자기 증류

**DINO(Self-DIstillation with NO labels)**는 레이블 없이 이미지를 분할(segmentation)하는 데 유용한 표현을 학습하는 자기 지도(Self-supervised) 방법입니다.

> Mathilde Caron, Hugo Touvron, Ishan Misra 외, "Emerging Properties in Self-Supervised Vision Transformers", *arXiv:2104.14294* (2021)

DINO도 Teacher-Student 구조를 쓰지만, DeiT와 달리 Teacher를 별도로 미리 학습시키지 않습니다. 대신 Student의 파라미터를 **EMA(지수이동평균, Exponential Moving Average)**로 서서히 반영해 Teacher를 갱신합니다. 학습 데이터는 **Multi-crop 전략**으로 만드는데, 원본 이미지에서 50% 이상을 잘라낸 것을 Global view, 그보다 작게 잘라낸 것을 Local view라 부르고, Teacher에게는 Global view만, Student에게는 Global view와 Local view를 섞어(Local view 비중을 높여) 보여줍니다. 즉 "선생님은 이미지 전체를 넓게 보고, 학생은 일부만 보고도 선생님과 같은 결론에 도달하도록" 강제하는 구조입니다.

Softmax를 적용할 때 Student에는 상대적으로 큰 Temperature를, Teacher에는 훨씬 작은 Temperature를 사용하는 비대칭 구조도 특징입니다 — Temperature가 작을수록 분포가 뾰족해지므로(LLM 시리즈 06장 참고), "선생님은 확신에 찬 답을 제시하고 학생은 그 답을 부드럽게 따라간다"는 비유가 성립합니다. 특정 클래스로 출력이 쏠려버리는 붕괴(collapse) 현상을 막기 위해, Teacher 출력에서 노드별 이동평균값을 빼는 **Centering**도 함께 적용됩니다. Teacher는 역전파로 갱신되지 않고(stop-gradient) 오직 EMA로만 갱신됩니다.

DINO로 학습된 모델의 Attention map을 시각화하면, 레이블을 전혀 준 적이 없는데도 이미지 속 전경 객체 부분에서만 활성화가 크게 나타납니다. 원 논문은 이 현상의 정확한 원인이 완전히 규명된 것은 아니라고 밝히면서도, Global view와 Local view가 같은 결론에 도달해야 하는 제약이 반복되면서 결과적으로 전경 객체에 반응이 몰리게 된 것으로 추정합니다.

## 흔한 오개념 — "네 모델 모두 같은 문제를 다른 방법으로 푼 것이다"

DeiT·Swin·CLIP·DINO를 "ViT를 개선한 모델들"로 뭉뚱그리기 쉽지만, 이들은 서로 다른 병목을 겨냥합니다. DeiT는 **데이터 효율성**(적은 데이터로도 잘 학습되는가), Swin은 **연산 효율성**(큰 이미지에서도 감당할 수 있는가), CLIP은 **레이블 비용**(사람이 일일이 라벨링하지 않아도 되는가), DINO는 **표현의 자기조직화**(레이블 없이도 의미 있는 구조가 드러나는가)를 다룹니다. 실무에서 이 네 모델 중 하나를 고를 때는 "지금 가진 자원의 병목이 데이터인지, 연산인지, 레이블인지"를 먼저 진단하는 것이 모델 선택의 출발점입니다.

다음 장에서는 지금까지 다룬 CNN·ViT 아키텍처가 실제로 "물체의 위치와 클래스를 동시에 맞추는" Object Detection 문제에 어떻게 적용되는지, R-CNN 계열부터 DETR까지 다룹니다.
