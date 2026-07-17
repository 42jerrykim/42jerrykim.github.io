---
collection_order: 7
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[Vision AI 07] Segmentation — FCN에서 SAM까지"
slug: image-segmentation-fundamentals
description: "픽셀 단위로 분류하는 Segmentation을 FCN의 Skip Fusion부터 Mask R-CNN, U-Net의 Encoder-Decoder 구조, Transformer 기반 SegFormer, 범용 파운데이션 모델 SAM까지 원 논문과 함께 정리합니다. 시리즈 B의 마지막 챕터입니다."
tags:
  - Image-Segmentation(이미지분할)
  - Computer-Vision
  - CNN(Convolutional Neural Network)
  - Transformer
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
  - Implementation(구현)
---

Object Detection이 박스 단위로 물체 위치를 찾는다면, **Segmentation**은 **픽셀 단위**로 어느 물체에 속하는지를 분류합니다. 이 장은 이 문제를 처음으로 완전한 CNN 구조로 푼 FCN에서 시작해, Detection과 결합한 Mask R-CNN, 의료 영상에서 출발해 지금도 널리 쓰이는 U-Net, Transformer 기반 SegFormer, 그리고 프롬프트 하나로 무엇이든 분할하는 SAM까지 다룹니다.

## FCN — 완전 합성곱으로 픽셀 단위 예측하기

**FCN(Fully Convolutional Network)**은 완전연결 레이어 없이 오직 합성곱 레이어만으로 입력 전체를 픽셀 단위 예측으로 바꾼 첫 구조입니다.

> Jonathan Long, Evan Shelhamer, Trevor Darrell, "Fully Convolutional Networks for Semantic Segmentation", *arXiv:1411.4038* (2014)

Pooling을 거치며 이미지는 여러 단계에 걸쳐 축소되는데(예: $2^5=32$배), 이를 다시 32배로 키워 원본 해상도로 복원해야 합니다. 문제는 이렇게 한 번에 32배를 복원하면 세밀한 경계 정보가 크게 손실된다는 것입니다. FCN은 **Skip Fusion**으로 이를 보완합니다 — 중간 레이어(아직 많이 축소되지 않아 세밀한 정보를 더 많이 가진 레이어)의 특징을 복원 과정에 함께 합쳐, 점진적으로 더 정확한 경계를 그려냅니다.

## Mask R-CNN — Detection에 픽셀 마스크를 더하기

**Mask R-CNN**은 05장에서 다룬 Faster R-CNN(Object Detection)에 Segmentation 기능을 추가로 결합한 모델입니다.

> Kaiming He, Georgia Gkioxari, Piotr Dollár, Ross Girshick, "Mask R-CNN", *arXiv:1703.06870* (2017)

동작 순서는 먼저 Object Detection으로 박스를 찾은 뒤, 각 박스 내부에서 픽셀 단위 마스크를 예측하는 두 단계입니다. 여기서 중요한 설계 선택이 있습니다 — Mask Head가 풀어야 할 문제는 이미 박스 단계에서 "어떤 물체인지"가 결정된 뒤이므로, 다중 클래스 분류가 아니라 "이 픽셀이 물체인가 아닌가"라는 **이진 분류**로 단순화됩니다. 그래서 Mask Head의 출력층은 여러 클래스를 겨루는 Softmax 대신, 각 클래스별로 독립적인 확률을 내는 **Sigmoid**를 씁니다. 클래스가 이미 정해진 상태에서 그 클래스에 해당하는 마스크 채널 하나만 사용하면 되므로, 클래스 간 경쟁 없이 각 픽셀의 전경/배경 여부만 판단하면 됩니다.

## U-Net — Encoder의 정보를 Decoder로 그대로 이어붙이기

**U-Net**은 2015년 의료 영상(세포 분할) 문제를 겨냥해 발표된 오래된 논문이지만, 지금도 Diffusion 같은 생성 모델의 백본으로 널리 쓰이는 구조입니다.

> Olaf Ronneberger, Philipp Fischer, Thomas Brox, "U-Net: Convolutional Networks for Biomedical Image Segmentation", *arXiv:1505.04597* (2015)

U-Net의 핵심은 Encoder에서 압축한 특징을 Decoder에서 복원할 때, 같은 해상도의 Encoder 특징을 **직접 이어붙이는(concatenate)** 것입니다. FCN의 Skip Fusion과 목적은 비슷하지만(세밀한 정보 보존), 값을 더하는(add) 대신 채널 방향으로 이어붙인다는 점이 다릅니다.

```python
import torch
import torch.nn as nn

class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1), nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1), nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.net(x)

class Up(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
        self.conv = DoubleConv(in_channels, out_channels)   # concat 이후 채널이 2배가 됨

    def forward(self, x_decoder: torch.Tensor, x_encoder: torch.Tensor) -> torch.Tensor:
        x_decoder = self.up(x_decoder)                        # 해상도를 2배로 키움
        x = torch.cat([x_encoder, x_decoder], dim=1)          # 같은 해상도의 Encoder 특징과 결합
        return self.conv(x)
```

Encoder는 `MaxPool2d`로 해상도를 절반씩 줄이며 `DoubleConv`로 채널을 늘리는 `Down` 블록의 반복이고(예: 64→128→256→512→1024), Decoder는 `ConvTranspose2d`로 해상도를 2배씩 키운 뒤 같은 해상도의 Encoder 특징 맵을 채널 방향으로 이어붙이고(이 지점에서 채널이 일시적으로 2배가 됨) 다시 `DoubleConv`로 채널을 줄이는 `Up` 블록의 반복입니다. 마지막 1×1 Convolution으로 채널 수를 클래스 수에 맞춥니다 — 이진 분할이면 로짓 1채널을 출력해 `BCEWithLogitsLoss`(Sigmoid + Binary Cross Entropy)로 학습하고, 예측 시에는 Sigmoid를 취한 뒤 0.5 임계값으로 마스크를 만듭니다.

## SegFormer — Transformer를 CNN처럼 쓰기

**SegFormer**는 패치를 겹치게(overlap) 잘라 사용하고, 패치를 병합(merging)하며 레이어가 깊어질수록 크기가 줄어드는 CNN과 유사한 구조를 Transformer로 구현합니다.

> Enze Xie, Wenhai Wang, Zhiding Yu 외, "SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers", *arXiv:2105.15203* (2021)

03장에서 다룬 원조 ViT의 Self-Attention은 시퀀스 길이가 길어질수록 연산량이 제곱으로 늘어나는데, SegFormer는 **Efficient Self-Attention**으로 이를 줄입니다 — Key의 시퀀스 길이 $N$을 $N/R$로 줄이는 대신 채널 $C$를 $C \times R$로 늘렸다가, Linear 층을 거치며 다시 $C$로 복원합니다. 이렇게 하면 시퀀스 길이가 줄어든 상태를 유지하면서도 연산량을 절약할 수 있습니다. **Mix-FFN**은 Residual Connection을 적용하면서 02장에서 다룬 Depthwise Convolution을 함께 사용해 연산량을 더 줄입니다. 별도의 Position Embedding 없이도, 논문은 Zero Padding 자체가 암묵적으로 위치 정보를 제공한다고 설명합니다.

## SAM — 프롬프트 하나로 무엇이든 분할하기

**SAM(Segment Anything Model)**은 포인트·박스·마스크·텍스트 등 다양한 프롬프트를 받아 "무엇이든" 분할할 수 있도록 설계된 범용 Segmentation 모델입니다.

> Alexander Kirillov 외, "Segment Anything", *arXiv:2304.02643* (2023)

CLIP·DINO와 마찬가지로 **파운데이션 모델**을 지향하며, 텍스트 프롬프트 인코더는 CLIP의 텍스트 인코더를 재사용하고, 이미지 인코더는 이미지 일부를 가리고 나머지로 복원하도록 학습하는 자기지도 방식(MAE, Masked Autoencoder)으로 사전학습된 인코더를 가져다 씁니다. 이미지는 Image Encoder를, 프롬프트는 Prompt Encoder를 거친 뒤, 두 인코딩 결과가 합쳐져 Mask Decoder에서 최종 마스크를 만듭니다.

점 하나만 찍어 프롬프트를 주면, 그 점이 "사람 전체"를 가리키는지 "팔만"을 가리키는지 모호할 수 있습니다. SAM은 이 **Ambiguity(모호성)**를 마스크 하나로 억지로 답하는 대신, 서로 다른 크기의 후보 마스크 여러 개와 각각의 신뢰도(confidence score)를 함께 출력해 사용자가 원하는 수준을 고를 수 있게 합니다. SAM 학습에 쓰인 SA-1B 데이터셋은 기존 Segmentation 데이터셋보다 이미지 수는 약 11배, 마스크 수는 약 400배(11억 개)에 달하는데, 이는 사람이 처음부터 다 라벨링한 것이 아니라 **Data Engine**이라는 반복적 자동화 과정으로 만들어졌습니다 — 먼저 기존 데이터로 SAM을 학습시키고, 그 모델로 새 이미지에 자동 라벨링을 시도한 뒤 사람이 잘못된 부분만 교정하고, 교정된 데이터로 다시 학습시키는 과정을 반복하면 점점 사람 개입이 줄어들다가 결국 완전 자동으로 대량의 라벨을 생성할 수 있게 됩니다.

## 흔한 오개념 — "Segmentation은 Detection보다 항상 더 어려운 상위 문제다"

Segmentation이 픽셀 단위로 더 세밀한 정보를 요구하니 Detection보다 무조건 어렵다고 생각하기 쉽지만, Mask R-CNN의 설계가 보여주듯 실제로는 문제를 어떻게 쪼개느냐에 따라 난이도가 달라집니다. Mask R-CNN은 "어떤 물체인지"를 Detection 단계에서 먼저 확정하고, Segmentation 단계는 "이 픽셀이 그 물체에 속하는가"라는 훨씬 단순한 이진 분류로 축소합니다. 즉 Segmentation이 어려운 것이 아니라, **박스 안에서 픽셀을 분류하는 것**과 **이미지 전체에서 모든 클래스의 픽셀을 한 번에 분류하는 것(Semantic Segmentation)**은 난이도가 다른 문제입니다. 두 방식 중 어느 쪽이 적합한지는 "물체 각각을 개별 인스턴스로 구분해야 하는가(Instance Segmentation)"와 "클래스별로만 구분하면 되는가(Semantic Segmentation)"라는 요구사항에 달려 있습니다.

## 시리즈 B를 마치며

00장에서 시작해 여기까지, 손으로 설계한 특징에서 CNN(01~02장), Transformer 기반 ViT(03~04장), 그리고 Detection·Tracking·Segmentation이라는 세 가지 실전 응용(05~07장)까지 컴퓨터 비전의 전체 지형을 훑었습니다. 이 시리즈에서 반복적으로 등장한 세 가지 아이디어 — Teacher-Student 구조로 지식을 압축·전달하기(DeiT, DINO), Transformer의 유연한 입출력을 활용해 CNN의 장점을 재현하기(Swin, SegFormer), 어려운 문제를 더 단순한 하위 문제로 쪼개기(Mask R-CNN, DETR) — 는 LLM 밑바닥부터 이해하기 시리즈와 On-Device AI 경량화 시리즈에서도 다른 이름으로 계속 등장합니다.
