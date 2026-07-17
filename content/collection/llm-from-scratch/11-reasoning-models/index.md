---
collection_order: 11
date: 2026-07-17
lastmod: 2026-07-17
draft: true
title: "[LLM(Series) 11] 추론 모델의 시대 — Chain-of-Thought와 GRPO"
slug: reasoning-models
description: "중간 추론 과정을 생성하면 왜 정답률이 올라가는지 Chain-of-Thought로 설명하고, 정답 채점의 어려움과 이를 해결하는 GRPO 강화학습 방식까지 최근 추론 모델의 학습 원리를 다룹니다."
tags:
  - LLM(Large Language Model)
  - Reinforcement-Learning(강화학습)
  - Fine-Tuning(파인튜닝)
  - Transformer
  - GPT(Generative Pre-trained Transformer)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - NLP(Natural Language Processing)
  - AI(인공지능)
  - Data-Science(데이터사이언스)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Advanced
  - Reference(참고)
  - Case-Study(케이스스터디)
  - Comparison(비교)
---

10장에서 다룬 RLHF·DPO는 "어떤 응답이 더 나은가"라는 선호를 학습시켰습니다. 이 장에서 다루는 **추론 모델(reasoning model)**은 한 걸음 더 나아가, 정답을 곧바로 내놓는 대신 중간 풀이 과정을 스스로 생성하도록 학습된 모델입니다. 이 장은 왜 중간 과정을 생성하는 것만으로 정답률이 오르는지, 그리고 정답이 있는 과제에서 이 능력을 강화학습으로 어떻게 강화하는지를 다룹니다.

## Chain-of-Thought — 왜 풀이 과정을 쓰면 정답률이 오르는가

**Chain-of-Thought(CoT, 사고의 연쇄)**는 모델에게 "단계별로 생각해서 풀어라"라는 식의 프롬프트를 주거나, 그런 형태의 데이터로 학습시켜 정답 이전에 중간 추론 과정을 먼저 생성하게 만드는 방법입니다.

> Jason Wei, Xuezhi Wang, Dale Schuurmans 외, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", *arXiv:2201.11903* (2022)

이 방법이 효과가 있는 이유는 06장에서 다룬 GPT의 생성 구조와 직접 연결됩니다. GPT는 이미 생성한 토큰들을 다시 입력으로 참고하며 다음 토큰을 예측하는 Causal 구조이므로, 중간 추론 과정을 먼저 텍스트로 뱉어내면 그 추론 결과가 이후 토큰을 예측할 때 추가적인 문맥(단서)으로 작용합니다. 반대로 곧바로 정답만 요구하면, 모델은 복잡한 다단계 추론을 단 한 번의 순전파 안에서 암묵적으로 끝내야 하는데, 이는 실제로 여러 단계를 거쳐야 풀리는 문제일수록 불리합니다. 즉 CoT는 "모델을 더 똑똑하게 만드는" 것이 아니라, **모델이 이미 가진 능력을 여러 스텝에 걸쳐 쓸 수 있도록 풀어주는** 효과에 가깝습니다.

## 정답 채점의 어려움과 GRPO

CoT로 생성된 추론 과정과 정답을 강화학습으로 더 강화하려면, "이 응답이 얼마나 좋은가"를 채점할 보상(reward) 신호가 필요합니다. 수학 문제처럼 정답이 명확한 과제는 최종 답이 맞았는지를 규칙 기반으로 채점할 수 있어 비교적 간단하지만, 10장에서 다룬 Reward Model 기반 RLHF처럼 별도의 채점 모델을 학습시키는 방식은 채점 모델 자체의 오차와 비용이 추가로 발생합니다.

**GRPO(Group Relative Policy Optimization)**는 이 문제를 별도의 가치 함수(value function, PPO에서 보상의 기준선을 추정하는 모델) 없이 해결하는 강화학습 방법입니다.

> Zhihong Shao, Peiyi Wang, Qihao Zhu 외, "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", *arXiv:2402.03300* (2024)

GRPO의 핵심 아이디어는, 같은 질문에 대해 여러 개의 응답을 한꺼번에 생성한 뒤, 그 그룹 안에서의 **상대적 순위**로 보상을 정규화하는 것입니다. 그룹 평균보다 좋은 응답은 양의 보상을, 평균보다 나쁜 응답은 음의 보상을 받는 식으로, 절대적인 보상 값을 추정하는 별도 모델 없이도 "이 그룹 안에서 상대적으로 어떤 응답이 나았는가"만으로 정책을 갱신할 수 있습니다. 이는 정답 유무를 규칙 기반으로 채점할 수 있는 수학·코딩 같은 과제에서 특히 계산 효율이 좋습니다.

| 방법 | 채점 기준 | 별도 가치 함수 필요 여부 |
|---|---|---|
| RLHF(PPO) | Reward Model이 부여한 절대 점수 | 필요 |
| GRPO | 같은 그룹 내 응답들의 상대적 순위 | 불필요 |

## 스케일링 법칙과 추론 시간 확장

기존 LLM의 성능 향상은 주로 모델 크기·데이터 양·학습 연산량을 늘리는 **학습 시간 스케일링(train-time scaling)**에 의존했습니다. 추론 모델은 여기에 더해, 답을 내기 전 얼마나 긴 추론 과정을 생성하도록 허용하느냐— **추론 시간 스케일링(inference-time scaling, 또는 test-time compute)** —도 성능을 좌우하는 별도의 축으로 취급합니다. 같은 모델이라도 더 긴 CoT를 생성하도록 허용하면(또는 학습 과정에서 더 긴 추론을 하도록 유도하면) 어려운 문제에서 정답률이 올라가는 경향이 관찰되며, 이는 "모델을 더 키우는 것"과는 별개로 "이미 학습된 모델에게 더 많이 생각할 시간을 주는 것"이 성능을 끌어올리는 또 다른 지렛대임을 보여줍니다.

## 흔한 오개념 — "추론 모델은 진짜로 논리적 추론을 한다"

CoT로 생성된 텍스트가 사람이 보기에 논리적인 풀이 과정처럼 보이기 때문에, 모델이 사람과 같은 방식으로 "생각"한다고 오해하기 쉽습니다. 하지만 07장에서 다룬 것처럼 GPT는 여전히 다음 토큰의 확률 분포를 예측하는 구조이고, CoT는 그 예측 과정에 중간 단계를 텍스트로 노출시켜 활용하는 기법입니다. 생성된 추론 과정이 실제로 최종 답을 도출하는 데 인과적으로 기여했는지, 아니면 그럴듯해 보이는 사후 설명(post-hoc rationalization)에 가까운지는 과제와 모델에 따라 다르며, 여전히 활발히 연구되는 주제입니다. "추론 과정이 텍스트로 보인다"는 것과 "그 과정이 사람의 논리적 추론과 동일한 방식으로 작동한다"는 것은 별개의 주장이라는 점을 구분해야 합니다.

이것으로 Phase 2(학습·정렬)가 끝났습니다. 다음 장에서는 Phase 3으로 넘어가, 이렇게 학습된 모델을 실제 서비스에서 빠르게 응답하도록 만드는 KV Cache와 서빙 효율화 기법을 다룹니다.
