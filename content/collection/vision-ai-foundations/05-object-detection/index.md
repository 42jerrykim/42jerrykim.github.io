---
collection_order: 5
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[Vision AI] 05. Object Detection — R-CNN에서 DETR까지"
slug: object-detection-fundamentals
description: "IoU와 mAP 같은 평가지표부터, Two-stage인 R-CNN·Faster R-CNN과 Transformer 기반 DETR까지 Object Detection의 핵심 개념과 발전 과정을 다룹니다. Recall-Precision 트레이드오프를 실무 사례로 설명합니다."
tags:
  - Object-Detection(객체탐지)
  - Computer-Vision
  - Transformer
  - CNN(Convolutional Neural Network)
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
  - Best-Practices
  - Attention(어텐션)
  - Beginner
  - Case-Study
  - Technology(기술)
  - Implementation(구현)
  - Time-Complexity(시간복잡도)

image: "wordcloud.png"
---

이미지 분류가 "이 사진에 무엇이 있는가"를 답한다면, **Object Detection**은 "무엇이, 어디에" 있는가를 동시에 답하는 문제입니다. 즉 물체의 <strong>클래스(class)</strong>와 <strong>경계 상자(bounding box)</strong>를 함께 맞춰야 합니다. 이 장은 이 문제를 어떻게 평가하는지부터 시작해, 후보 영역을 먼저 제안하는 전통적인 방식에서 그 과정 자체를 없애버린 DETR까지의 흐름을 다룹니다.

## 왜 Object Detection이 어려운가

같은 클래스의 물체라도 크기(스케일)가 다르고, 다른 물체에 부분적으로 가려질 수 있고(occlusion), 자세가 변하고, 배경이 복잡하고, 조명 조건이 다양합니다. 이런 변동성 아래에서도 일관되게 위치와 클래스를 맞춰야 한다는 점이 순수 분류 문제와 다른 어려움을 만듭니다.

## 평가 지표 — IoU에서 mAP까지

예측한 박스와 정답 박스(Ground Truth)가 얼마나 겹치는지는 <strong>IoU(Intersection over Union)</strong>로 잽니다.

$$\text{IoU} = \frac{\text{교집합 영역}}{\text{합집합 영역}}$$

완벽히 일치하면 1, 전혀 안 겹치면 0입니다. 탐지가 "성공"했다고 인정하려면 두 가지 임계값을 모두 통과해야 합니다 — Confidence Score가 일정 기준(예: 0.5) 이상이어야 "물체가 있다"고 인정하고, IoU가 일정 기준(예: 0.5) 이상이어야 "제대로 찾았다"고 인정합니다. 이를 모두 만족해야 <strong>TP(True Positive)</strong>로 집계됩니다. Object Detection에서는 물체가 없는데 없다고 판단한 경우(TN)는 의미가 없어 다루지 않고, TP·**FN(놓침)**·**FP(잘못 찾음)** 세 가지만 계산합니다.

$$\text{Recall} = \frac{TP}{\text{전체 정답 개수}}, \qquad \text{Precision} = \frac{TP}{\text{내가 찾았다고 한 개수}}$$

Recall은 "실제 정답 중 몇 개를 찾아냈는가", Precision은 "내가 찾았다고 한 것 중 몇 개가 진짜였는가"를 묻는 지표입니다. 이 둘은 서로 반비례하는 경향이 있습니다 — Confidence Score 임계값을 낮춰 더 많이 "있다"고 판단하면 Recall은 오르지만 엉뚱한 것까지 잡아내며 Precision은 떨어지고, 임계값을 높여 확실한 것만 골라내면 Precision은 오르지만 Recall은 떨어집니다.

어느 지표를 우선할지는 도메인에 따라 달라집니다. 암 진단처럼 실제 양성을 놓치는 대가(FN)가 매우 큰 도메인에서는 Precision이 다소 낮아지더라도 Recall을 최대한 높이는 방향을 선호합니다. 반대로 스팸 메일 필터처럼 정상 메일을 스팸으로 잘못 거르면 안 되는 상황에서는 Precision이 더 중요합니다. 임계값을 바꿔가며 Recall-Precision 쌍을 그래프로 그린 것이 **PR Curve**이고, 이 곡선 아래 면적이 <strong>AP(Average Precision)</strong>입니다. 이를 모든 클래스에 대해 계산해 평균 낸 것이 <strong>mAP(mean Average Precision)</strong>로, Object Detection의 대표 평가지표입니다.

## Two-stage Detector — 후보를 먼저 제안하고 다듬기

**Object Proposal**은 물체가 있을 법한 후보 영역을 먼저 뽑는 과정입니다. **Two-stage Detector**는 이 후보 제안(1단계)과, 각 후보에 대한 클래스·박스 예측(2단계)을 나눠 처리합니다.

**R-CNN**은 Selective Search로 후보 영역을 뽑고, 각 영역을 CNN에 통과시켜 특징을 뽑은 뒤 SVM으로 분류합니다. 문제는 물체가 아닌 배경 후보도 많이 섞여 들어간다는 점, 그리고 후보 영역마다 CNN을 반복 실행해야 해서 매우 느리다는 점이었습니다. **Fast R-CNN**은 이미지 전체를 한 번만 CNN에 통과시킨 뒤 그 특징 맵에서 후보 영역만 잘라내는 방식으로 이 비효율을 개선했지만, 여전히 CPU 연산인 Selective Search가 병목이었습니다.

**Faster R-CNN**은 Selective Search를 GPU에서 처리 가능한 <strong>RPN(Region Proposal Network)</strong>으로 대체합니다.

> Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun, "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks", *arXiv:1506.01497* (2015)

RPN은 미리 정의된 여러 크기·비율의 기준 박스인 **Anchor Box**를 기준으로, 각 위치에서 "여기에 물체가 있는가/없는가"를 이진 분류합니다. 손실 함수는 분류(Cross Entropy)와 박스 위치 회귀(01장에서 다룬 1-노름 기반 L1 Loss)를 함께 사용합니다. 여러 후보 박스가 같은 물체를 중복으로 가리킬 때는, 신뢰도가 가장 높은 박스만 남기고 나머지를 제거하는 **NMS(Non-Maximum Suppression)** 후처리를 거칩니다.

## One-stage Detector — 후보 제안 없이 곧바로

**One-stage Detector**는 후보 제안 단계 없이 특징 맵에서 곧바로 클래스와 바운딩 박스를 출력합니다. **CenterNet**처럼 박스 대신 물체의 중심점(keypoint)을 예측하는 방식으로 접근하는 계열도 있습니다. 두 계열 모두 결국 "클래스가 무엇인지(classification)"와 "박스 좌표 4개(x, y, w, h)를 얼마나 정확히 맞추는지(regression)"라는 공통 목표를 갖지만, One-stage는 속도, Two-stage는 정확도 쪽에 상대적으로 유리한 경향이 있습니다.

## DETR — Transformer로 재해석한 Object Detection

<strong>DETR(DEtection TRansformer)</strong>은 기존 Detector들의 복잡한 후처리(Anchor 설계, NMS)를 없애고, Object Detection을 **집합(Set) 예측 문제**로 재정의합니다.

> Nicolas Carion, Francisco Massa, Gabriel Synnaeve 외, "End-to-End Object Detection with Transformers", *arXiv:2005.12872* (2020)

CNN으로 특징 맵을 뽑은 뒤 인코더-디코더 트랜스포머를 통과시키고, 디코더의 각 쿼리(query)는 이미지 내에 있을 수 있는 물체 하나에 대응합니다(실제 구현에서는 보통 100개의 쿼리를 씁니다). 모델의 출력은 `pred_logits`(클래스 확률, 물체가 없는 경우를 위한 "no-object" 클래스 포함)와 `pred_boxes`(0–1로 정규화된 중심좌표·폭·높이)입니다.

학습 시에는 예측과 정답(GT) 박스들을 헝가리안 알고리즘으로 **일대일 매칭**한 뒤, 매칭된 쌍에 대해서만 분류·박스 손실을 계산하고 짝이 없는 쿼리는 "no-object"로 학습시킵니다. 이 **이분 매칭(Bipartite Matching)** 덕분에 같은 물체를 여러 쿼리가 중복 예측하지 않아, 기존 Detector에 필수였던 NMS 후처리가 필요 없어집니다. 두 박스가 전혀 겹치지 않을 때 항상 0이 되는 일반 IoU의 한계를 보완하기 위해, 겹치지 않는 경우에도 두 박스가 얼마나 가까운지를 반영하는 <strong>GIoU(Generalized IoU)</strong>를 손실 함수에 함께 씁니다.

| | Two-stage(Faster R-CNN) | One-stage | DETR |
|---|---|---|---|
| 후보 제안 단계 | RPN으로 명시적 제안 | 없음(특징 맵에서 직접 예측) | 없음(쿼리가 후보 역할) |
| 중복 제거 | NMS 필요 | NMS 필요 | 이분 매칭으로 불필요 |
| Anchor 설계 | 필요 | 대개 필요 | 불필요 |
| 상대적 강점 | 정확도 | 속도 | 후처리 단순화, 전역 문맥 |

## 흔한 오개념 — "mAP가 높은 모델이 항상 더 나은 선택이다"

mAP는 모든 클래스·모든 Confidence 임계값을 종합한 하나의 숫자이지만, 실제 배포 환경의 요구사항은 이 숫자 하나로 환원되지 않습니다. 위에서 다룬 것처럼 암 진단과 스팸 필터가 Recall과 Precision 중 서로 다른 것을 우선하듯, 같은 mAP를 가진 두 모델도 PR Curve의 모양(어느 Recall 구간에서 Precision이 급격히 떨어지는가)이 다르면 실무에서의 적합도가 달라집니다. 모델을 비교할 때는 mAP 하나만 볼 것이 아니라, 실제 배포 시 사용할 Confidence 임계값 부근에서의 Recall·Precision을 함께 확인해야 합니다.

다음 장에서는 한 프레임에서의 Detection을 넘어, 여러 프레임에 걸쳐 같은 물체를 추적하는 Tracking 문제를 다룹니다.
