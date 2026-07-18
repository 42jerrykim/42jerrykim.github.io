---
collection_order: 0
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[On-Device AI 00] Introduction: On-Device AI 경량화"
slug: getting-started-on-device-ai-compression
description: "모델을 자원이 제한된 기기에서 빠르게 돌리는 경량화 시리즈의 도입 챕터입니다. Prefill/Decode의 서로 다른 병목, Pruning·Quantization·Distillation 3대 기법의 관계, 7개 챕터 커리큘럼을 정리합니다."
tags:
  - On-Device-AI(온디바이스AI)
  - Model-Compression(모델경량화)
  - Quantization(양자화)
  - Pruning(가지치기)
  - Knowledge-Distillation(지식증류)
  - LLM(Large Language Model)
  - Transformer
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - AI(인공지능)
  - PyTorch
  - Hardware(하드웨어)
  - Embedded(임베디드)
  - Curriculum
  - 커리큘럼
  - Roadmap
  - 로드맵
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Mobile(모바일)
  - Beginner
  - Advanced
  - Case-Study
  - Reference(참고)

---

같은 트랜스포머 연산인데도, LLM이 프롬프트를 읽을 때(Prefill)와 답을 한 글자씩 뱉을 때(Decode)는 병목의 성격이 완전히 다릅니다. Prefill은 GPU 연산 능력이 부족해서 느리고, Decode는 GPU가 놀고 있는데도 메모리에서 가중치를 읽어오는 속도 때문에 느립니다. 이 시리즈는 "모델을 어떻게 만들고 학습시키는가"를 다룬 LLM·Vision 시리즈에서 관점을 바꿔, "이미 만든 모델을 자원이 제한된 환경에서 어떻게 빠르고 가볍게 돌릴 것인가"를 다룹니다.

## 왜 지금 경량화를 다뤄야 하는가

GPU 하드웨어 성능은 꾸준히 발전해 왔지만, 모델 크기가 커지는 속도가 이를 앞지르고 있습니다. LLM 시리즈 12장에서 다룬 KV Cache의 크기는

$$\text{KV Cache 크기} = 2 \times B \times S \times L \times D \times P$$

($B$=배치 크기, $S$=시퀀스 길이, $L$=레이어 수, $D$=Hidden Dimension, $P$=정밀도)로 계산되는데, 모델 자체의 크기에 비해 이 값이 차지하는 비중이 상당히 큽니다. 서버에서는 여러 사용자의 요청을 배치로 묶어 GPU 활용도를 어느 정도 끌어올릴 수 있지만, 온디바이스 환경에서는 보통 요청이 하나씩만 들어와 배치로 묶기 어렵고, 이 비효율이 그대로 체감 속도 저하로 이어집니다. 이런 제약 아래에서 모델을 실제로 쓸 수 있게 만드는 것이 이 시리즈가 다루는 문제입니다.

## Prefill과 Decode — 두 단계의 서로 다른 병목

LLM 추론은 성격이 다른 두 단계로 나뉩니다. **Prefill 단계**는 사용자가 입력한 프롬프트 전체를 한꺼번에 처리하는 단계로, 행렬×행렬 연산(GEMM)이 여러 토큰에 대해 병렬로 일어나 GPU 활용도가 높습니다. **Decode 단계**는 모델이 만든 토큰이 다시 입력으로 들어가는 자기순환(autoregressive) 구조라 한 번에 토큰 하나씩만 계산해야 하고, 이때는 행렬×벡터 연산(GEMV)이 되어 GPU 병렬성을 충분히 활용하지 못한 채 메모리 접근이 병목이 됩니다. 이 둘을 구분하는 것이 이 시리즈 전체를 관통하는 뼈대입니다 — Pruning·Quantization은 주로 메모리(모델 크기) 병목을, Speculative Decoding 같은 기법은 주로 Decode 단계의 GEMV 비효율을 겨냥합니다.

## 경량화의 3대 기법과 이 시리즈의 범위

모델을 가볍게 만드는 방법은 크게 세 갈래입니다. **Pruning(가지치기)**은 중요도가 낮은 연결을 끊어 파라미터 자체를 줄이고, **Quantization(양자화)**은 각 값을 표현하는 비트 수를 줄이며, **Knowledge Distillation(지식 증류)**은 큰 모델(Teacher)의 지식을 작은 모델(Student)에 옮겨 담습니다. 이 시리즈는 이 세 기법을 CNN 수준의 기초부터 시작해 LLM에 특화된 형태(SparseGPT, AWQ 등)로 확장하고, 마지막으로 Attention 연산 자체를 빠르게 만드는 추론 가속 기법까지 다룹니다. 모델 아키텍처 자체(Transformer/GPT의 구조)는 LLM 밑바닥부터 이해하기 시리즈를, CNN·ViT 아키텍처는 Vision AI 파운데이션 시리즈를 전제로 합니다.

## 커리큘럼

| 챕터 | 제목 | 핵심 질문 |
|---|---|---|
| 01 | Pruning | 어떤 가중치를 끊어도 성능이 유지되는가 |
| 02 | Quantization | 몇 비트까지 줄여도 정확도를 지킬 수 있는가 |
| 03 | Knowledge Distillation | 작은 모델은 큰 모델의 무엇을 배워야 하는가 |
| 04 | LLM을 위한 Pruning | 왜 단순 절댓값 기준으로는 부족한가 |
| 05 | LLM Quantization | Activation의 Outlier는 왜 다루기 어려운가 |
| 06 | Efficient Transformer 추론 | Attention과 Decode 자체를 어떻게 빠르게 만드는가 |

01~03장은 CNN을 예시로 세 기법의 원리를 다지고, 04~05장은 같은 기법이 LLM 규모에서 왜 더 정교해져야 하는지를 다룹니다. 06장은 관점을 바꿔, 압축이 아니라 연산·메모리 접근 패턴 자체를 최적화하는 기법(Speculative Decoding, FlashAttention)을 다룹니다. CNN 경량화 실무 경험이 있다면 01~02장을 건너뛰고 03장부터 시작해도 무리가 없습니다.

## 학습 결과

이 시리즈를 완주하면 "이 모델을 얼마나 가볍게 만들 수 있는가"라는 질문에 Pruning·Quantization·Distillation 중 어떤 조합이 적합한지, 그리고 그 선택이 정확도·하드웨어 가속·구현 복잡도 사이에서 어떤 트레이드오프를 만드는지 판단할 수 있게 됩니다. 이는 실무에서 On-Device 배포를 검토할 때 "이 논문(GPTQ, AWQ, SmoothQuant 등)이 정확히 무엇을 어디로 옮겨서 문제를 우회하는지"를 구조적으로 읽어내는 역량, 그리고 서버 배포와 온디바이스 배포 각각에 어떤 최적화가 더 유효한지를 구분하는 판단 기준으로 이어집니다.

다음 장에서는 가장 단순한 경량화 아이디어인 Pruning을, "왜 신경망은 잘라내도 괜찮을 만큼 크게 설계되는가"라는 질문에서 시작해 다룹니다.
