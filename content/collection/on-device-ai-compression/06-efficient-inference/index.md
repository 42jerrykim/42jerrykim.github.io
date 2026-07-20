---
collection_order: 6
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[On-Device AI] 06. 추론 가속 — Speculative Decoding, FlashAttention"
slug: efficient-transformer-inference
description: "압축이 아니라 연산·메모리 접근 패턴을 최적화하는 추론 가속 기법을 다룹니다. Speculative Decoding, FlashAttention, 중요 토큰만 남기는 H2O를 원 논문과 함께 정리하는 시리즈의 마지막 챕터입니다."
tags:
  - On-Device-AI(온디바이스AI)
  - LLM(Large Language Model)
  - Model-Compression(모델경량화)
  - Attention(어텐션)
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
  - Time-Complexity(시간복잡도)
  - Case-Study(케이스스터디)
  - Hardware(하드웨어)
  - Mobile(모바일)
  - Embedded(임베디드)
  - Beginner
  - Case-Study
  - Comparison(비교)

image: "wordcloud.png"
---

01~05장은 모델 자체를 작게 만드는 압축 기법을 다뤘습니다. 이 장은 관점을 바꿔, 모델 크기는 그대로 두고 **연산 순서와 메모리 접근 패턴**을 최적화해 추론을 빠르게 만드는 기법들을 다룹니다. 00장에서 짚은 Decode 단계의 메모리 바운드 병목을 직접 겨냥한 기법들이라는 공통점이 있습니다.

## Sparse Attention — 모든 토큰을 다 볼 필요는 없다

LLM 시리즈 05장에서 다룬 Attention은 Q와 K를 전체 토큰에 대해 계산합니다. 하지만 관사·전치사처럼 문맥적으로 중요도가 낮은 토큰까지 매번 전체 연산에 포함시킬 필요는 없다는 관찰에서 **Sparse Attention**이 출발합니다. 가까운 토큰(Local)과 중요도가 높은 소수의 토큰(Global)은 항상 계산하고, 나머지 영역은 듬성듬성(sparse) 계산합니다. <strong>Dynamic Sparsity(SpAtten)</strong>는 덜 중요한 토큰을 줄이는 것뿐 아니라 Attention 헤드 자체도 동적으로 줄이며, **Deja Vu**는 비슷한 아이디어를 LLM 추론에 적용합니다. LLM 시리즈 07장에서 다룬 "LLM 파라미터의 대부분이 FFN에 있다"는 사실에 착안해, 조건에 따라 FFN의 필요한 부분만 계산하는 **Conditional Computation**도 같은 계열의 아이디어입니다.

## Speculative Decoding — 작은 모델이 추측하고 큰 모델이 검증하기

00장에서 다룬 것처럼 Decode 단계는 GEMV 연산이라 GPU 병렬성을 충분히 활용하지 못합니다. **Speculative Decoding**은 이 문제를 정면으로 우회합니다.

> Yaniv Leviathan, Matan Kalman, Yossi Matias, "Fast Inference from Transformers via Speculative Decoding", *arXiv:2211.17192* (2022)

핵심 아이디어는 작고 빠른 모델(draft model)이 먼저 $\gamma$개의 토큰을 추측해서 생성하고(빠른 GEMV 연산), 크고 정확한 모델(target model)이 이 추측들을 한꺼번에 검사(GEMM 연산, 병렬 처리 가능)하는 것입니다. Draft 모델이 만든 $\gamma$개의 토큰을 Target 모델에게 한 번에 넣어 검사시키면, Target 모델 입장에서는 Prefill과 동일한 형태의 병렬 연산이 됩니다. 검사 결과 맞은 토큰은 그대로 채택하고, 어느 지점에서 처음 틀렸다면 그 지점부터는 Target 모델이 직접 토큰 하나를 새로 생성해 이어갑니다(이 부분은 일반 Decode와 같습니다).

```python
def speculative_decode_step(draft_model, target_model, context, gamma: int = 4):
    draft_tokens = draft_model.generate(context, num_tokens=gamma)   # 빠른 GEMV 연산 * gamma
    target_logits = target_model.forward(context + draft_tokens)      # 한 번의 GEMM 연산
    accepted = []
    for i, token in enumerate(draft_tokens):
        if target_model.accepts(target_logits[i], token):             # 검증 통과
            accepted.append(token)
        else:
            new_token = target_model.sample(target_logits[i])          # 처음 틀린 지점부터 재생성
            accepted.append(new_token)
            break
    return accepted
```

$\gamma$개 전체를 검사하는 시간과 토큰 1개를 생성하는 시간이 GEMM/GEMV 특성상 큰 차이가 없기 때문에, 한 번에 여러 토큰을 "공짜로" 채택할 수 있다면 그만큼 이득입니다. 다만 $\gamma$를 무작정 크게 잡는다고 좋은 것은 아닙니다 — 예를 들어 7개를 추측시켰는데 2번째 토큰부터 틀렸다면 뒤의 5개는 전부 버려지는 낭비가 됩니다. Draft 모델의 예측 정확도와 $\gamma$ 값 사이의 균형을 실험적으로 맞춰야 하며, 조건에 따라 대체로 2~3배의 속도 향상이 보고됩니다. 서버에서 먼저 널리 채택된 기법이지만, 온디바이스 환경에도 그대로 적용해 유사한 수준의 가속을 얻을 수 있다는 실증 사례들이 이어지고 있습니다.

## 토큰/KV 프루닝 — H2O

01·04장에서 다룬 Pruning이 가중치를 대상으로 했다면, <strong>H2O(Heavy-Hitter Oracle)</strong>는 KV Cache에 쌓인 **토큰**을 대상으로 합니다.

> Zhenyu Zhang, Ying Sheng, Tianyi Zhou 외, "H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models", *arXiv:2306.14048* (2023)

모든 토큰의 KV를 캐싱하는 대신, 중요도가 높은 소수의 "Heavy Hitter" 토큰만 남기고 나머지는 캐시에서 제거합니다. 어떤 토큰을 지울지는 Attention Score를 기준으로 판단합니다 — Prefill 과정에서 각 토큰이 다른 토큰들로부터 받은 Attention 값이 누적되는데, 이 값이 작은(다른 토큰들의 주목을 별로 못 받는) 토큰부터 제거합니다. 단순히 "직전 몇 개의 최근 토큰"만 캐싱하는 Local Attention 방식은 최근 토큰 외의 정보를 모두 잃어버려 성능 저하가 크지만, H2O는 여기에 더해 과거 토큰 중 Attention Score가 높았던 소수의 Heavy Hitter를 추가로 함께 유지한다는 점이 핵심 차별점입니다. 실험 결과 KV Cache를 전체의 약 5%만 유지해도 원래 성능과 거의 동일한 결과를 냈다고 보고되며, 대체로 약 20%까지 압축해도 성능 저하가 거의 없다는 결과가 함께 제시됩니다(그 이하로 더 압축하면 성능이 눈에 띄게 떨어지기 시작합니다). **SnapKV**, **Quest**도 비슷한 목적(중요한 KV만 선별적으로 유지)의 후속 기법들입니다.

## FlashAttention — 메모리 접근 자체를 줄이기

**FlashAttention**은 Attention 행렬 전체를 한 번에 느린 메모리(HBM)에 올리는 대신, <strong>타일링(tiling)</strong>해서 일부만 빠른 메모리(SRAM)에 올려 처리하는 **Operator Fusion**의 대표 사례입니다.

> Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré, "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness", *arXiv:2205.14135* (2022)

문제는 Softmax가 전체 값에 대한 정규화(모든 값의 합으로 나누는 연산)를 필요로 한다는 점인데, 타일 단위로 쪼개 처리하면 아직 전체 값을 다 보지 못한 상태입니다. FlashAttention은 **타일별로 로컬(local) Softmax를 먼저 계산**하고, 이후 타일들을 병합(merge)할 때 그 값을 보정하는 방식으로 이를 해결합니다. 이 접근의 중요한 특징은 근사가 아니라 **수학적으로 정확히 같은 결과**를 내면서(논문 제목의 "Exact Attention"), 순전히 메모리 접근 패턴만 최적화해 속도를 높인다는 것입니다 — 압축 기법들이 정확도와 속도를 맞바꾸는 것과 달리, FlashAttention은 맞바꿈 없이 순수하게 I/O 효율만 개선합니다.

## Patch-based Inference — 메모리가 극도로 제한된 환경

메모리가 SRAM 정도밖에 없는 매우 제한된 기기에서 모델을 돌리기 위한 방법으로, 이미지를 패치 단위로 나눠 처리해 **최대(peak) 메모리 사용량 자체를 줄이는** 접근입니다. 전체 이미지를 한 번에 처리하려면 중간 activation을 모두 메모리에 올려야 하지만, 패치 단위로 나눠 처리하면 한 시점에 필요한 메모리가 패치 크기에 비례해 크게 줄어듭니다.

## 흔한 오개념 — "이 장의 기법들은 압축 기법의 대체재다"

Speculative Decoding·FlashAttention·H2O를 01~05장의 Pruning·Quantization과 "경쟁하는" 대안으로 이해하기 쉽지만, 실제로는 서로 다른 축을 최적화하는 **보완재**에 가깝습니다. Quantization으로 모델 크기를 줄여도 Decode 단계의 GEMV 병목 자체는 사라지지 않고, Speculative Decoding으로 Decode를 가속해도 모델이 메모리에 올라가지 않으면 애초에 실행할 수 없습니다. 실무에서는 이 장에서 다룬 기법들과 01~05장의 압축 기법을 함께 조합해 쓰는 것이 일반적입니다 — 예를 들어 AWQ로 모델을 4비트로 압축한 뒤, 그 위에 FlashAttention과 Speculative Decoding을 함께 적용하는 식입니다.

## 시리즈 C를 마치며

00장에서 시작해, Prefill과 Decode라는 서로 다른 병목을 축으로 Pruning(01, 04장)·Quantization(02, 05장)·Knowledge Distillation(03장)이라는 압축 3대 기법을 CNN 기초부터 LLM 특화 기법까지 다뤘고, 이 장에서는 압축이 아닌 연산·메모리 접근 최적화로 관점을 넓혔습니다. 이 시리즈 전체에서 반복해서 등장한 두 가지 패턴은 "어려운 문제(outlier, 느린 Decode)를 다른 곳으로 옮기거나 분리해서 우회한다"(SmoothQuant, Speculative Decoding)는 것과 "정확한 계산 대신 근사로 충분한 부분을 찾아낸다"(테일러 근사, 로컬 Softmax)는 것입니다. 이 두 패턴은 LLM 밑바닥부터 이해하기 시리즈와 Vision AI 파운데이션 시리즈에서 다룬 여러 설계 선택에서도 다른 이름으로 계속 등장했던 것과 같은 종류의 통찰입니다.
