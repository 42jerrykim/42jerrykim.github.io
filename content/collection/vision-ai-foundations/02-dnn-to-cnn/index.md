---
collection_order: 2
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[Vision AI 02] DNN에서 CNN으로 — 합성곱과 ResNet"
slug: dnn-to-cnn
description: "완전연결 신경망이 픽셀을 통계적 패턴으로만 처리한다는 한계 실험부터, Convolution·Padding·Stride·Pooling·Receptive Field, 그리고 ResNet의 Skip Connection까지 CNN 아키텍처의 핵심을 정리합니다."
tags:
  - Computer-Vision
  - CNN(Convolutional Neural Network)
  - ResNet
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - PyTorch
  - Data-Science(데이터사이언스)
  - History(역사)
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
  - Case-Study(케이스스터디)
---

이미지의 조각을 큼직하게 잘라 위치를 뒤섞어도 사람은 "자동차 범퍼, 하늘"처럼 대략적인 내용을 짐작합니다. 하지만 픽셀 단위로 완전히 뒤섞으면 사람 눈에는 노이즈로만 보입니다. 흥미로운 점은, 이렇게 픽셀 단위로 뒤섞은 이미지로 완전연결 신경망(DNN)을 학습시켜도 원본으로 학습했을 때와 비슷한 정확도가 나온다는 것입니다. 이 장은 이 실험이 드러내는 DNN의 한계에서 출발해, 그 한계를 보완하는 Convolution 구조와 ResNet의 Skip Connection까지 다룹니다.

## Perceptron에서 MLP까지 — 첫 번째 AI 겨울

**Perceptron(퍼셉트론)**은 사람 뉴런의 구조(입력을 받는 수상돌기, 가중합을 계산하는 세포체, 출력을 전달하는 축삭말단)를 본떠 만든 인공신경망의 가장 단순한 형태입니다. 입력 $X_1, ..., X_n$에 가중치 $W_1, ..., W_n$을 곱한 가중합에 Bias를 더한 뒤, 계단 함수(Step Function)를 통과시켜 결과를 이진 분류합니다.

퍼셉트론의 근본적인 한계는 **직선 하나로 데이터를 나누는 것(선형 분리)만 가능하다**는 것입니다. 두 입력값이 같으면 0, 다르면 1을 내야 하는 XOR 문제는 직선 하나로는 절대 올바르게 나눌 수 없습니다. 이 한계가 널리 알려지면서 신경망 연구는 오랜 침체기(1차 AI 겨울)에 들어갑니다. 1980년대 중반, 여러 층의 퍼셉트론을 쌓은 **MLP(Multi-Layer Perceptron)**를 역전파(Backpropagation)로 학습시키면 XOR 같은 비선형 문제도 풀 수 있음이 이론적으로 정립됩니다 — LLM 시리즈 01장에서 다룬 "선형함수만으로는 안 되고 활성화함수로 비선형성을 부여해야 한다"는 원리가 여기서도 그대로 적용됩니다. 다만 이론이 정립된 이후에도 당시 하드웨어 성능이 이 연산량을 감당하지 못해, 2000년대 GPU 성능이 비약적으로 발전하고 나서야 DNN 계열이 본격적으로 실용화됩니다.

## DNN의 한계 — 통계적 패턴 매칭

앞서 소개한 픽셀 셔플 실험이 말해주는 것은, DNN이 이미지를 처리하는 방식이 사람의 시각 시스템을 모방한 것이 아니라는 사실입니다. DNN/CNN 이전의 완전연결 신경망은 이미지를 "형태(의미론적 특징)"로 보는 게 아니라, **픽셀 사이의 통계적 상관관계 패턴**을 학습해서 분류합니다. 게다가 $100 \times 100$ 크기의 이미지를 완전연결 신경망에 그대로 넣으려면 10,000차원 벡터로 펼쳐야 하고, 이는 파라미터 수를 폭발적으로 늘립니다. 이 문제의식에서 "픽셀 하나하나가 아니라 주변 픽셀과의 지역적(local) 관계를 명시적으로 다루는 구조가 필요하지 않을까"라는 질문이 나오고, 그 답이 **Convolution(합성곱)**입니다.

## Convolution — 커널로 지역적 특징 뽑아내기

CNN은 커널(kernel) 크기만큼의 지역적 영역에만 집중해 특징을 뽑아냅니다. 커널의 크기(예: 3×3)는 사용자가 정하지만, 커널의 채널 개수는 항상 입력의 채널 개수와 같아야 합니다.

```python
import torch.nn as nn

conv = nn.Conv2d(
    in_channels=3,     # 입력 채널 수 (RGB)
    out_channels=64,    # 이 레이어가 학습할 커널(필터)의 개수
    kernel_size=3,
    stride=1,
    padding=1,
)
```

세 가지 하이퍼파라미터가 출력 크기를 결정합니다. **Padding(패딩)**은 입력 가장자리에 값을 덧대 입력과 출력의 공간 크기를 같게 유지하고, **Stride(스트라이드)**는 커널을 한 번에 몇 칸씩 이동시킬지를, **Pooling(풀링)**은 특징 맵을 다운샘플링(축소)하는 역할을 합니다. CNN 아키텍처 그림에서 흔히 보이는 것은 **Activation Map(활성화 맵)**이지만, 실제로 학습되는 대상은 그 활성화 맵을 만들어내는 **커널(필터)**이라는 점을 혼동하지 않아야 합니다. 레이어를 지날수록 Activation Map의 가로·세로 크기는 점점 작아지고 채널 수는 점점 늘어나는 것이 전형적인 CNN 구조입니다.

## Receptive Field — 작은 커널을 여러 겹 쌓는 이유

하나의 출력값을 만드는 데 사용된 원본 이미지상의 범위를 **Receptive Field(수용 영역)**라고 합니다. 3×3 커널을 두 번 겹쳐 쌓으면 5×5 커널을 한 번 쓴 것과 같은 Receptive Field(5×5)를 얻으면서도, 학습해야 할 파라미터 수는 더 적습니다($3\times3\times2=18$개 vs. $5\times5=25$개, 채널 수를 고려하면 차이는 더 커집니다). 이 때문에 실제 CNN은 큰 커널 하나보다 작은 3×3 커널을 여러 겹 쌓는 방식을 선호합니다.

## Convolution의 변형들

| 종류 | 동작 | 목적 |
|---|---|---|
| 1×1 Convolution | 공간 크기는 유지, 채널 수만 변경 | 채널 차원 조정(사실상 픽셀 위치별 행렬 곱) |
| Group Convolution | 채널을 여러 그룹으로 나눠 그룹별 합성곱 | 연산량 절감 |
| Depthwise Convolution | 채널별로 독립적으로 합성곱 후 1×1로 채널 정보 재결합 | 연산량 절감 |
| Transposed Convolution | 특징 맵의 크기를 키움 | 업샘플링(복원) |

## Skip Connection과 ResNet

레이어가 학습해야 할 목표를 $H(x)$라 하면, 많은 경우 이 목표는 입력을 거의 그대로 보존하는 항등함수(identity)에 가깝습니다. 그런데 신경망이 항등함수 자체를 정확히 학습하는 것은 생각보다 어렵습니다. **Skip Connection**을 도입하면 레이어가 학습해야 할 대상이 $H(x)$가 아니라 **잔차(residual) $F(x) = H(x) - x$**로 바뀝니다.

> Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, "Deep Residual Learning for Image Recognition", *arXiv:1512.03385* (2015)

$F(x)$가 0에 가깝기만 하면 항등함수에 가까운 동작을 쉽게 재현할 수 있으므로 학습이 훨씬 쉬워집니다. 파라미터의 변화 폭 자체가 작아지면 손실 함수의 표면이 더 완만(smooth)해져, 지역 최저점에 덜 갇히고 전역 최저점까지 더 잘 흘러간다는 부수적인 장점도 있습니다.

ResNet-18처럼 비교적 얕은 모델은 3×3 Conv 두 번을 통과시킨 뒤 입력을 더하는 **Building Block**을 쓰지만, 채널 수가 큰 깊은 모델은 3×3 Conv를 그대로 쓰면 연산량이 매우 커지므로 **Bottleneck Block**을 씁니다 — 1×1 Conv로 채널을 먼저 줄이고(예: 256→64), 3×3 Conv로 특징을 추출한 뒤, 다시 1×1 Conv로 채널을 원래 크기(64→256)로 복원합니다. 레이어를 지나며 특징 맵의 크기나 채널 수가 바뀌면 입력 $x$와 출력 $F(x)$를 바로 더할 수 없으므로, Skip Connection 경로에도 1×1 Convolution(채널 조정)과 stride(공간 크기 조정)를 추가해 shape을 맞춘 뒤 더합니다.

```python
class BasicBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),  # 채널·크기 조정
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out = out + self.shortcut(x)      # Residual Connection
        return self.relu(out)
```

`self.shortcut`이 빈 `Sequential()`(항등함수)로 남아 있는 경우는 입력과 출력의 shape이 이미 같을 때이고, 그렇지 않을 때만 1×1 Conv로 shape을 맞춥니다. 최종적으로 마지막 Conv 블록을 통과한 $7\times7\times512$ 크기의 특징 맵은 **Global Average Pooling**($7\times7$ 영역 전체를 평균 내어 값 하나로 압축)으로 $1\times512$ 벡터가 된 뒤, 분류를 위한 완전연결 레이어를 거쳐 최종 클래스 확률이 됩니다.

## 흔한 오개념 — "Skip Connection은 그래디언트 소실을 막기 위한 것일 뿐이다"

Skip Connection의 효과를 "역전파 시 그래디언트가 잘 흐르게 해주는 통로"로만 이해하는 경우가 많은데, 이는 절반의 설명입니다. 그래디언트가 잘 흐르는 것은 결과이지 전부가 아닙니다. 더 근본적인 이유는 위에서 짚었듯, 레이어가 학습해야 할 목표를 "완전히 새로운 함수 $H(x)$"에서 "0에 가까운 잔차 $F(x)$"로 바꿔 **학습 문제 자체를 더 쉽게 만든다**는 데 있습니다. 항등함수에 가까운 목표를 학습하는 것이 왜 어려운지, 그리고 잔차를 학습하는 것이 왜 쉬운지를 설명할 수 있어야 Skip Connection을 제대로 이해했다고 할 수 있습니다.

다음 장에서는 CNN과는 다른 방식으로 이미지를 처리하는 Vision Transformer가, 이미지를 패치로 잘라 트랜스포머에 넣었을 때 실제로 무엇이 달라지는지를 다룹니다.
