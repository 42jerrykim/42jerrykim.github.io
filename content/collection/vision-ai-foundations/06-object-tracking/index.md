---
collection_order: 6
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[Vision AI] 06. Tracking — ByteTrack과 TrackFormer"
slug: object-tracking-fundamentals
description: "여러 프레임에 걸쳐 같은 물체를 이어 붙이는 Multi-Object Tracking을, Tracking-by-Detection과 Tracking-by-Regression 두 접근으로 나눠 설명합니다. 저신뢰도 검출까지 활용하는 ByteTrack과 DETR 기반 TrackFormer를 다룹니다."
tags:
  - Computer-Vision
  - Object-Detection(객체탐지)
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
  - Attention(어텐션)
  - Beginner
  - Case-Study
  - Technology(기술)
  - Best-Practices
  - Implementation(구현)
  - Time-Complexity(시간복잡도)

image: "wordcloud.png"
---

05장에서 다룬 Object Detection은 프레임 하나에서 "무엇이 어디에 있는가"를 답합니다. <strong>Tracking(추적)</strong>은 여기서 한 걸음 더 나아가, 여러 프레임에 걸쳐 등장하는 물체가 "같은 개체인가"를 판단하는 문제입니다. 이 문제는 <strong>MOT(Multi-Object Tracking)</strong>라고 불리며, 이 장은 두 가지 접근 방식과 그중 최근 대세가 된 방식의 대표 기법 두 가지를 다룹니다.

## Tracking-by-Detection과 Tracking-by-Regression

**Tracking-by-Detection**은 이전 프레임과 현재 프레임 각각에서 Object Detector가 찾아낸 물체들을 놓고, "이전 프레임의 어느 박스가 현재 프레임의 어느 박스에 대응하는가"를 매칭(association)하는 작업만 풀면 Tracking이 됩니다. 이 방식은 Detector 성능에 크게 의존합니다 — 애초에 잘못 찾은 것끼리는 매칭해봐야 소용이 없기 때문입니다. 05장에서 다룬 것처럼 최근 Object Detector의 성능이 크게 좋아지면서, "검출은 Detector에게 맡기고 매칭 알고리즘만 잘 설계하면 된다"는 이 접근이 최근의 대세가 되었습니다.

**Tracking-by-Regression**은 이전 프레임들에서 물체가 이동해 온 궤적(속도·방향)을 바탕으로 현재 프레임에서의 위치를 직접 추정합니다. 한 프레임의 검출 결과만으로는 부족하고, 그 이전 프레임들과의 이동 이력이 필요합니다. Detector 성능이 아직 충분하지 않았던 시기에 더 많이 쓰였던 접근입니다.

| | Tracking-by-Detection | Tracking-by-Regression |
|---|---|---|
| 핵심 문제 | 프레임 간 박스 매칭(association) | 궤적 기반 위치 추정 |
| Detector 의존도 | 매우 높음(Detector가 정확해야 함) | 상대적으로 낮음 |
| 최근 추세 | 주류(Detector 성능 향상에 힘입어) | Detector가 부족했던 과거에 더 많이 사용 |

## ByteTrack — 저신뢰도 검출도 버리지 않는다

기존 Tracking-by-Detection 방식은 매칭을 신뢰도가 높은 검출 결과에만 의존하는 경우가 많아, 물체끼리 겹치는 상황에서 정확도가 떨어지는 문제가 있었습니다. **ByteTrack**의 핵심 아이디어는 신뢰도가 낮은 검출 결과도 버리지 않고 활용하는 것입니다.

> Yifu Zhang, Peize Sun, Yi Jiang 외, "ByteTrack: Multi-Object Tracking by Associating Every Detection Box", *arXiv:2110.06864* (2021)

ByteTrack의 매칭 절차는 두 단계로 나뉩니다. 먼저 검출 결과를 신뢰도(score) 기준으로 높은 그룹과 낮은 그룹으로 나눕니다. 신뢰도 높은 박스들로 기존 트랙과 먼저 매칭(First Association)한 뒤, **Second Association**에서 신뢰도가 낮았던 박스들을 별도로 보관해두었다가 매칭을 한 번 더 시도합니다. 이 두 번째 단계가 ByteTrack의 핵심 기여입니다 — 물체가 일시적으로 다른 물체에 가려져 신뢰도가 낮게 나온 검출이라도, 놓치지 않고 기존 트랙과 이어 붙일 기회를 한 번 더 얻습니다.

```python
def bytetrack_association(high_conf_boxes, low_conf_boxes, existing_tracks, iou_fn, iou_threshold=0.3):
    # 1단계: 신뢰도 높은 검출로 먼저 매칭
    matched_1, unmatched_tracks_1, unmatched_high = match_by_iou(
        existing_tracks, high_conf_boxes, iou_fn, iou_threshold
    )
    # 2단계: 남은 트랙을 신뢰도 낮은 검출과 다시 매칭 (ByteTrack의 핵심)
    matched_2, unmatched_tracks_2, _ = match_by_iou(
        unmatched_tracks_1, low_conf_boxes, iou_fn, iou_threshold
    )
    return matched_1 + matched_2, unmatched_tracks_2, unmatched_high
```

`unmatched_tracks_1`(1단계에서 짝을 찾지 못한 기존 트랙)을 곧바로 "추적 실패"로 처리하지 않고, `low_conf_boxes`(신뢰도가 낮아 보통 버려지는 검출)와 다시 한번 매칭을 시도하는 것이 이 함수의 핵심입니다. 이 두 번째 기회 덕분에 가려짐(occlusion)으로 일시적으로 신뢰도가 낮아진 검출도 추적이 끊기지 않고 이어질 수 있습니다.

## TrackFormer — DETR을 추적에 확장하기

05장에서 다룬 DETR은 이미지 하나에서 물체를 쿼리(query) 단위로 예측했습니다. **TrackFormer**는 이 쿼리 개념을 시간축으로 확장합니다.

> Tim Meinhardt, Alexander Kirillov, Laura Leal-Taixé, Christoph Feichtenhofer, "TrackFormer: Multi-Object Tracking with Transformers", *arXiv:2101.02702* (2021)

이전 프레임에서 특정 물체를 추적하던 쿼리를 다음 프레임에도 그대로 이어서 입력하면, 그 쿼리는 자연스럽게 "같은 물체를 계속 따라가는" 역할을 하게 됩니다. 새로 나타난 물체는 새로운 쿼리로 처리하고, 더 이상 보이지 않는 물체의 쿼리는 종료합니다. 이 방식은 DETR이 이분 매칭으로 프레임 내 중복 예측 문제를 해결한 것과 같은 원리로, 별도의 매칭 알고리즘(ByteTrack의 IoU 기반 매칭 같은) 없이 트랜스포머의 쿼리 메커니즘 자체가 추적 대응 관계를 담당하도록 설계되었습니다.

## 흔한 오개념 — "Tracking은 Detection을 여러 번 반복하면 되는 문제다"

Detection 성능이 충분히 좋아지면 Tracking도 자동으로 해결된다고 생각하기 쉽지만, ByteTrack이 다루는 문제(가려짐으로 인한 일시적 저신뢰도 검출)가 보여주듯, "각 프레임에서 정확히 검출하는 것"과 "프레임 간에 같은 개체임을 정확히 판단하는 것"은 별개의 문제입니다. 두 사람이 스쳐 지나가며 잠시 겹치는 장면을 생각해 보면, 각 프레임에서 두 사람을 정확히 검출했더라도 겹치는 순간 전후로 어느 박스가 어느 사람인지 매칭이 틀리면 추적 궤적 자체가 뒤바뀔 수 있습니다. Tracking은 Detection의 정확도에 크게 의존하지만, 그 위에 "매칭(association)"이라는 별도의 문제를 풀어야 하는 독립적인 과제입니다.

다음 장에서는 박스 단위가 아니라 픽셀 단위로 물체를 분류하는 Segmentation을, FCN부터 범용 파운데이션 모델인 SAM까지 다룹니다.
