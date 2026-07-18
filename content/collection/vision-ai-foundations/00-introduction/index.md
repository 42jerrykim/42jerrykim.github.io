---
collection_order: 0
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[Vision AI] 00. Introduction: Vision AI 파운데이션"
slug: getting-started-vision-ai-foundations
description: "손으로 설계한 특징에서 CNN, Vision Transformer로 이어지는 컴퓨터 비전의 진화를 정리하는 시리즈의 도입 챕터입니다. 8개 챕터의 커리큘럼과 학습 목표, LLM 시리즈와의 연결점까지 상세히 다룹니다."
tags:
  - Computer-Vision
  - CNN(Convolutional Neural Network)
  - Vision-Transformer(ViT)
  - Transformer
  - Attention(어텐션)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - Object-Detection(객체탐지)
  - Image-Segmentation(이미지분할)
  - PyTorch
  - Data-Science(데이터사이언스)
  - ResNet
  - Curriculum
  - 커리큘럼
  - Roadmap
  - 로드맵
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - History(역사)
  - Beginner
  - Advanced
  - Case-Study
  - Reference(참고)

---

사람은 조각난 이미지를 뒤섞어도 "자동차 범퍼가 보이고 하늘이 보인다"는 식으로 대략적인 내용을 짐작할 수 있습니다. 그런데 같은 방식으로 뒤섞은 이미지로 신경망을 학습시켜 보면, 원본으로 학습했을 때와 비슷한 정확도가 나옵니다. 이 실험이 말해주는 것은 신경망이 이미지를 "형태(사람이 보는 방식)"가 아니라 "픽셀 사이의 통계적 패턴"으로 처리한다는 사실입니다. 이 시리즈는 이 발견에서 출발해, 사람의 시각 처리에 조금이라도 더 가까운 구조(Convolution의 지역성, Attention의 전역성)를 찾아가는 컴퓨터 비전의 발전 과정을 다룹니다.

## 왜 지금 컴퓨터 비전의 기초를 다시 짚어야 하는가

컴퓨터 비전은 크게 세 시기를 거쳐 발전했습니다. 1960~2010년의 초기 시대에는 SIFT·HOG 같은 손으로 설계한 특징(hand-crafted feature)을 SVM·AdaBoost 같은 분류기에 넣는 방식이 주류였습니다. 2011~2020년의 딥러닝 혁명기에는 "입력과 정답만 주면 중간 과정은 알아서 학습한다"는 End-to-End 학습으로 패러다임이 바뀌며 AlexNet·ResNet 같은 CNN이 이 자리를 대체했습니다. 2021년 이후로는 언어모델에서 검증된 Transformer 구조가 비전에도 들어와, Vision Transformer(ViT)를 시작으로 Detection·Segmentation을 포함한 거의 모든 비전 응용이 Transformer 기반으로 재구성되는 흐름이 이어지고 있습니다.

이 흐름을 알아야 하는 이유는 단순한 역사 지식이 아니라, 지금도 두 계열(CNN과 Transformer)이 공존하며 각자의 강점을 살려 쓰이고 있기 때문입니다. CNN은 커널 크기만큼의 지역적(local) 영역에서 시작해 레이어가 깊어지며 점차 넓은 영역을 보는 반면, ViT는 처음부터 Attention으로 이미지 전체의 전역적(global) 관계를 봅니다. 어떤 문제에 어떤 계열이 유리한지 판단하려면 두 구조의 차이를 구조 수준에서 이해하고 있어야 합니다.

## 이 시리즈가 다루는 범위

이 시리즈는 CNN과 Vision Transformer의 아키텍처, 그리고 Object Detection·Tracking·Segmentation이라는 세 가지 실전 응용을 다룹니다. LLM 밑바닥부터 이해하기 시리즈에서 정리한 Transformer/Attention의 기본 구조를 전제로 하며, 그 구조가 이미지 도메인에서 어떻게 재사용·변형되는지에 집중합니다. 모델을 가볍게 만드는 Pruning·Quantization은 On-Device AI 경량화 시리즈에서, 외부 지식을 검색해 활용하는 RAG는 RAG와 정보검색 시리즈에서 별도로 다룹니다.

## 커리큘럼

| 챕터 | 제목 | 핵심 질문 |
|---|---|---|
| 01 | 비전을 위한 배경지식 | 카메라는 어떻게 이미지를 만들고, 어떤 수학이 필요한가 |
| 02 | DNN에서 CNN으로 | 왜 완전연결 신경망이 아니라 합성곱이 필요한가 |
| 03 | Vision Transformer | 이미지를 패치로 잘라 트랜스포머에 넣으면 무엇이 달라지는가 |
| 04 | ViT의 변형들 | DeiT·Swin·CLIP·DINO는 ViT의 어떤 한계를 보완했는가 |
| 05 | Object Detection | 물체의 위치와 클래스를 동시에 맞추는 문제는 어떻게 풀리는가 |
| 06 | Tracking | 여러 프레임에 걸친 같은 물체를 어떻게 이어 붙이는가 |
| 07 | Segmentation | 박스가 아니라 픽셀 단위로 분류하려면 무엇이 달라지는가 |

01~02장은 CNN 계열의 기초를, 03~04장은 Transformer 계열의 기초와 그 개선판을, 05~07장은 두 계열의 구조를 실제 응용 문제에 적용하는 방법을 다룹니다. 이 순서를 따르는 이유는 05~07장에서 다루는 실전 모델(DETR, Mask R-CNN, SegFormer 등)이 모두 02장과 03~04장에서 다지는 CNN·Transformer 기초를 조합해서 만들어지기 때문입니다. 이미 CNN 기초에 익숙하다면 02장을 건너뛰고 03장부터 시작해도 무리가 없습니다.

## 학습 결과

이 시리즈를 완주하면 CNN과 ViT 각각이 어떤 원리로 이미지의 특징을 뽑아내는지 구조 수준에서 설명할 수 있게 되고, Object Detection·Segmentation 모델을 접했을 때 그 모델이 One-stage인지 Two-stage인지, 박스 기반인지 픽셀 기반인지, CNN 백본을 쓰는지 Transformer 백본을 쓰는지를 스스로 분류하고 그 선택의 트레이드오프를 판단할 수 있게 됩니다. 이는 실무에서 새로운 비전 모델의 논문이나 문서를 읽을 때, 낯선 이름의 구조라도 이 시리즈에서 다지는 기본 패턴(Convolution·Attention·Encoder-Decoder·Teacher-Student)의 조합으로 빠르게 분해해 이해하는 역량으로 이어집니다.

다음 장에서는 CNN을 다루기 전에 필요한 배경지식으로, 카메라가 이미지를 만드는 파이프라인과 벡터·확률통계의 기하학적 직관을 정리합니다.
