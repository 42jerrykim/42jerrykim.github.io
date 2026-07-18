---
collection_order: 10
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[LLM] 10. RLHF와 DPO — 사람의 선호를 학습시키는 법"
slug: rlhf-and-dpo
description: "Reward Model로 응답 순위를 학습하고 강화학습으로 정책을 조정하는 RLHF 파이프라인과, Reward Model 없이 선호 데이터를 직접 손실함수로 바꾸는 DPO를 비교합니다. InstructGPT·DPO 원 논문을 인용합니다."
tags:
  - LLM(Large Language Model)
  - RLHF(Reinforcement Learning from Human Feedback)
  - DPO(Direct Preference Optimization)
  - Reinforcement-Learning(강화학습)
  - Fine-Tuning(파인튜닝)
  - Transformer
  - GPT(Generative Pre-trained Transformer)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - NLP(Natural Language Processing)
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
  - Prompt-Engineering(프롬프트엔지니어링)
  - ChatGPT
  - Hugging-Face
  - Attention(어텐션)

---

09장에서 다룬 지시 미세튜닝은 "정답 응답 하나"를 그대로 따라 하도록 학습시킵니다. 하지만 실제로 좋은 응답에는 여러 가지가 있고, 그중에서도 "더 도움이 되는 것"과 "덜 도움이 되는 것"의 미묘한 차이가 있습니다. 이 장은 이 차이를 사람의 판단으로부터 학습시키는 두 가지 방법 — Reward Model을 거치는 RLHF와, 그 과정을 생략하는 DPO — 을 다룹니다.

## Reward Model — 응답에 순위를 매기는 모델

**RLHF(Reinforcement Learning from Human Feedback)**의 첫 단계는 사람이 여러 응답 후보를 비교해 순위를 매긴 데이터를 모으는 것입니다. 예를 들어 같은 질문에 대해 모델이 생성한 응답 A, B, C 중 사람이 "A가 B보다 낫고, B가 C보다 낫다"고 평가한 데이터를 모읍니다. 이 순위 데이터로 **Reward Model(보상 모델)**을 학습시키는데, 이 모델은 응답 하나를 입력받아 "얼마나 좋은 응답인가"를 나타내는 스칼라 점수를 출력하도록 훈련됩니다.

> Long Ouyang, Jeff Wu, Xu Jiang 외, "Training language models to follow instructions with human feedback", *arXiv:2203.02155* (2022, InstructGPT)

Reward Model이 준비되면, 원래의 언어모델(정책, policy)이 생성한 응답에 Reward Model이 점수를 매기고, 이 점수를 보상 신호로 삼아 강화학습(주로 PPO 알고리즘)으로 정책을 업데이트합니다. 점수가 높은 방향으로 응답 경향을 조금씩 조정하는 것입니다. 이 과정에서 정책이 Reward Model을 "속이는" 방향으로 지나치게 치우치지 않도록, 원래 SFT 모델의 출력 분포에서 너무 멀어지지 않게 하는 페널티(KL penalty, 01장에서 다룬 KL Divergence)를 함께 사용합니다.

## DPO — Reward Model 없이 선호를 직접 학습하기

RLHF 파이프라인은 Reward Model 학습과 강화학습이라는 두 단계를 거쳐야 해서 구현이 복잡하고, 강화학습 특유의 불안정성(하이퍼파라미터 민감도, 학습 붕괴 위험)을 안고 있습니다. **DPO(Direct Preference Optimization)**는 이 두 단계를 하나의 지도학습(supervised learning) 손실함수로 대체하는 방법입니다.

> Rafael Rafailov, Archit Sharma, Eric Mitchell 외, "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", *arXiv:2305.18290* (2023)

DPO의 핵심 통찰은, RLHF가 최적화하려는 목적함수를 수학적으로 풀어보면 별도의 Reward Model 없이도 "선호되는 응답(chosen)의 확률은 높이고 덜 선호되는 응답(rejected)의 확률은 낮추는" 형태의 손실함수로 직접 표현할 수 있다는 것입니다.

```python
import torch
import torch.nn.functional as F

def dpo_loss(
    policy_chosen_logprob: torch.Tensor,
    policy_rejected_logprob: torch.Tensor,
    ref_chosen_logprob: torch.Tensor,
    ref_rejected_logprob: torch.Tensor,
    beta: float = 0.1,
) -> torch.Tensor:
    policy_diff = policy_chosen_logprob - policy_rejected_logprob
    ref_diff = ref_chosen_logprob - ref_rejected_logprob
    logits = beta * (policy_diff - ref_diff)
    return -F.logsigmoid(logits).mean()
```

`policy_*_logprob`은 현재 학습 중인 모델이 chosen/rejected 응답에 부여하는 로그 확률이고, `ref_*_logprob`은 학습을 시작하기 전(또는 SFT 직후) 고정해 둔 참조 모델의 로그 확률입니다. `beta`는 참조 모델에서 얼마나 벗어나도 되는지를 조절하는 계수로, RLHF에서 KL 페널티가 하던 역할을 대신합니다. Reward Model도, 강화학습 루프도 없이 일반적인 지도학습 파인튜닝과 같은 방식으로 최적화할 수 있다는 점이 DPO의 실무적 장점입니다.

## RLHF와 DPO 비교

| | RLHF | DPO |
|---|---|---|
| Reward Model | 별도로 학습 필요 | 불필요 |
| 최적화 방식 | 강화학습(PPO) | 지도학습(분류 손실과 유사) |
| 구현 복잡도 | 높음(두 단계 파이프라인, 강화학습 불안정성) | 낮음(일반 파인튜닝과 유사한 학습 루프) |
| 필요 데이터 | 순위/비교 데이터 | 순위/비교 데이터(RLHF와 동일한 형태 활용 가능) |
| 실무 활용 | 초기 정렬 연구(InstructGPT 등)의 표준 | 최근 오픈소스 모델 상당수가 채택 |

두 방법 모두 "사람이 더 선호하는 응답이 무엇인가"라는 같은 종류의 데이터를 요구한다는 공통점이 있고, 차이는 그 데이터를 최적화 신호로 바꾸는 경로에 있습니다. RLHF는 Reward Model이라는 중간 표현을 거쳐 강화학습으로, DPO는 수학적 등가 변환을 통해 곧바로 지도학습 손실로 이어집니다.

## 흔한 오개념 — "DPO는 RLHF보다 약한(부정확한) 근사다"

DPO를 "복잡한 RLHF를 간단하게 흉내 낸 근사 기법"으로 오해하기 쉽지만, 원 논문의 핵심 주장은 근사가 아니라 **동일한 최적화 문제의 수학적으로 등가인 해**를 더 단순한 형태로 유도했다는 것입니다. RLHF가 Bradley-Terry 선호 모델을 가정해 Reward Model을 학습하고 그 Reward를 강화학습으로 최대화한다면, DPO는 같은 가정 아래에서 그 최적화 문제의 닫힌 형태 해를 정책 자체의 손실함수로 직접 표현합니다. 다만 두 방법이 완전히 동일한 실무 성능을 낸다고 단정할 수는 없습니다 — Reward Model을 별도로 학습하는 RLHF는 그 Reward Model을 다른 용도(예: 응답 필터링)로 재사용할 수 있다는 실무적 이점이 있고, 어떤 방법이 특정 데이터셋·모델 크기에서 더 안정적인지는 여전히 활발한 연구 주제입니다.

다음 장에서는 정렬(alignment)을 마친 모델이 어떻게 더 깊은 추론 능력을 갖추게 되는지, Chain-of-Thought와 최근 추론 모델들이 사용하는 강화학습 기반 학습법을 다룹니다.
