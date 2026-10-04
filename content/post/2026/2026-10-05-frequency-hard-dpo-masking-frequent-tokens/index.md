---
title: "[ML] DPO 손실의 절반을 차지하는 69개 토큰: Frequency-Hard DPO"
description: "DPO는 응답 토큰 전체의 로그확률 비율로 선호를 학습한다. 응답 토큰의 55.1%를 차지하는 69종의 고빈도 토큰을 손실에서 마스킹해 신호를 선명하게 만드는 Frequency-Hard DPO의 원리와 한계를 정리한다."
date: 2026-10-05T00:30:00+09:00
lastmod: 2026-10-05
draft: false
categories:
  - AI
tags:
  - DPO(Direct Preference Optimization)
  - RLHF(Reinforcement Learning from Human Feedback)
  - LLM(Large Language Model)
  - Fine-Tuning(파인튜닝)
  - Reinforcement-Learning(강화학습)
  - AI(인공지능)
  - Machine-Learning(머신러닝)
  - Deep-Learning(딥러닝)
  - NLP(Natural Language Processing)
  - Tokenization(토크나이징)
  - Transformer
  - PyTorch
  - Optimization(최적화)
  - Benchmark
  - Math(수학)
  - Deep-Dive
  - Case-Study
  - Best-Practices
  - Neural-Network
  - Open-Source(오픈소스)
  - Alignment
  - Preference-Learning
  - Frequency-Hard-DPO
  - Token-Masking
  - Gradient
  - Bradley-Terry
  - KL-Divergence
  - Reward-Model
  - GRPO
  - AlpacaEval
  - MT-Bench
  - Arena-Hard
  - Qwen
  - Llama
  - arXiv
  - 선호학습
  - 정렬
  - 고빈도토큰
  - 그래디언트
image: "wordcloud.png"
---

DPO(Direct Preference Optimization)는 보상 모델과 강화학습 루프를 없애고, chosen·rejected 응답 쌍에 대한 분류 손실 하나로 언어모델을 정렬하는 기법이다. 단순함 덕에 사후학습의 기본 도구가 됐지만, 그 손실이 응답의 모든 토큰을 똑같이 취급한다는 점은 오랫동안 당연하게 받아들여졌다. 2026년 9월 26일 제출된 논문 「Masking Frequent Tokens Sharpens Direct Preference Optimization」은 이 가정에 의문을 던진다. 저자들(Saini, Jha, Tang, Liu)은 응답 토큰의 55.1%가 단 69종의 토큰으로 채워져 있고, 이 토큰들이 선호 응답과 비선호 응답 양쪽에 비슷하게 나타나 학습 신호를 희석한다고 보고했다(출처: [arXiv:2609.32445](https://arxiv.org/abs/2609.32445)). 이 글은 DPO 손실이 어떻게 토큰 단위로 분해되는지부터 시작해, 이 마스킹 기법이 왜 말이 되는지와 어디까지 믿을 수 있는지를 정리한다.

## 먼저 DPO 손실을 토큰 단위로 풀어 보기

DPO는 최적 정책이 보상의 닫힌 형태 함수라는 사실을 이용해 보상을 `r(x, y) = β·log(π_θ(y|x) / π_ref(y|x))` 꼴의 정책 로그확률 비율로 재매개변수화한다(출처: [Rafailov et al., NeurIPS 2023](https://papers.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html), [arXiv:2305.18290](https://arxiv.org/abs/2305.18290)). 여기에 Bradley-Terry 선호 모델을 얹으면 손실은 chosen·rejected 각각의 로그확률 비율 차이를 시그모이드에 통과시킨 `-log σ(β · logits)`가 된다.

핵심은 응답 `y`의 로그확률이 토큰별 로그확률의 합이라는 점이다. 자기회귀 모델에서 `log π(y|x) = Σ_t log π(y_t | x, y_<t)`이므로, 응답 하나의 암묵적 보상은 토큰마다 하나씩 기여분을 가진 합으로 쓸 수 있다. 즉 DPO는 "chosen 응답의 토큰 기여분 합"과 "rejected 응답의 토큰 기여분 합"의 차이를 키우도록 학습하며, 길이가 같은 응답에서는 모든 위치가 같은 가중치 1로 들어간다. 이 구조가 이 글의 출발점이다. 토큰이 합산되는 순간, 어떤 토큰이 신호를 담고 어떤 토큰이 잡음인지는 손실 함수가 구분해 주지 않는다.

## 왜 고빈도 토큰이 문제인가

자연어 응답에서 쉼표, 마침표, 관사, 조사, "the"·"is" 같은 기능어는 응답의 어느 쪽이 좋은지와 거의 무관하게 거의 모든 응답에 등장한다. 논문이 측정한 바로는 이런 69종의 토큰이 응답 토큰의 55.1%를 차지한다. 이 토큰들은 chosen과 rejected 양쪽에 대칭적으로 나타나므로, 로그확률 비율 차이를 계산할 때 서로 상쇄되어야 이상적이다. 하지만 상쇄는 평균적으로만 일어난다. 개별 샘플에서는 이 토큰들의 로그비율이 서로 다른 값을 가지고, 학습 중 그래디언트는 그 우연한 차이를 따라 흔들린다. 선호를 가르는 정보는 대개 응답의 소수 위치(사실 오류, 구체적 표현, 거절 여부 등)에 몰려 있는데, 절반이 넘는 토큰이 정보 없이 그래디언트에 끼어들면 정작 중요한 위치의 신호 대 잡음비가 낮아진다.

여기서 구분해야 할 것은 논문이 실제로 주장한 범위다. 논문 초록이 말하는 것은 (1) 고빈도 토큰이 응답 토큰의 과반을 차지하고, (2) 선호·비선호 응답에 비슷하게 나타나며, (3) 그 결과 학습 신호가 희석된다는 점이다. "그래디언트의 절반 이상이 낭비된다"처럼 그래디언트 크기의 비율로 환산한 수치는 이 글에서 확인한 초록에 없으므로, 토큰 비율 55.1%를 그래디언트 비율로 읽지 않는 편이 안전하다.

## Frequency-Hard DPO: 마스킹이 하는 일

제안된 방법은 이름 그대로 "hard" 마스킹이다. 논문은 이 방법이 고빈도 응답 토큰의 암묵적 보상 기여를 0으로 만들고, 정보가 있는 위치에는 단위 가중치(1)를 준다고 설명한다. 위의 토큰 합 표현으로 말하면 토큰마다 가중치 `w_t ∈ {0, 1}`를 곱해 `Σ_t w_t · (토큰별 로그비율)`을 쓰는 것이다. 고빈도 집합에 속한 토큰은 `w_t = 0`, 나머지는 `w_t = 1`이다.

이 설계에서 눈여겨볼 점은 세 가지다. 첫째, 학습되는 파라미터가 없다. 가중치는 학습이 아니라 토큰 빈도 통계에서 결정되므로 모델에 모듈을 추가하지 않는다. 둘째, 선호 데이터를 다시 만들지 않는다. 같은 chosen·rejected 쌍을 그대로 쓰고 손실 계산만 바꾼다. 셋째, 연산 오버헤드가 사실상 없다. 마스크 곱셈 한 번이 전부다. 논문은 이를 "추가 비용 없는 개선"으로 제시한다. 아래는 이 아이디어를 PyTorch로 옮긴 설명용 스케치이며, 논문 공식 구현이 아니다. 고빈도 토큰 집합을 어떻게 고르는지(임계값, 코퍼스 기준)는 이 글에서 확인하지 못했으므로 `frequent_ids`는 호출자가 주는 입력으로만 둔다.

```python
import torch
import torch.nn.functional as F

def masked_dpo_loss(policy_logp, ref_logp, chosen_ids, rejected_ids,
                    frequent_ids, beta=0.1):
    # policy_logp / ref_logp: dict {"chosen": [B, T], "rejected": [B, T]} 토큰별 로그확률
    # chosen_ids / rejected_ids: [B, T] 토큰 id, frequent_ids: 마스킹할 고빈도 토큰 id 텐서
    def seq_logratio(side, ids):
        keep = ~torch.isin(ids, frequent_ids)           # 고빈도 토큰은 0, 나머지는 1
        per_token = policy_logp[side] - ref_logp[side]  # 토큰별 로그비율
        return (per_token * keep).sum(dim=-1)

    margin = seq_logratio("chosen", chosen_ids) - seq_logratio("rejected", rejected_ids)
    return -F.logsigmoid(beta * margin).mean()
```

패딩 토큰 처리와 길이 정규화는 생략했다. 표준 DPO와의 차이는 `keep` 한 줄뿐이라는 점이 요점이다.

## 어떤 결과가 보고됐나

논문은 Qwen-2.5-7B-Instruct와 Llama-3-8B-Instruct 두 모델에서 AlpacaEval, MT-Bench, Arena-Hard를 평가했고, 표준 DPO 대비 일관된 개선이 있었다고 보고한다(출처: [arXiv:2609.32445](https://arxiv.org/abs/2609.32445)). 이 글은 초록 수준의 정보만 확인했으므로 구체적인 점수 향상 폭은 적지 않는다. 수치가 필요하면 논문 본문의 표를 직접 확인해야 한다. 같은 이유로 7–8B 규모의 두 모델 결과를 더 큰 모델이나 다른 선호 데이터셋으로 일반화할 수 있다는 근거도 아직 없다.

## 이 접근을 어떻게 읽어야 하나

이 연구가 흥미로운 이유는 개선의 방향에 있다. 이전의 DPO 개선들은 손실의 수학적 형태를 바꾸는 쪽이 많았다. GRPO처럼 크리틱을 없애고 그룹 상대 이점으로 갈아타는 식이다(출처: [DeepSeekMath, arXiv:2402.03300](https://arxiv.org/abs/2402.03300)). 반면 이 논문은 손실의 형태는 그대로 두고 "어떤 토큰이 그 손실에 들어가는가"를 진단한다. 진단에는 토큰 빈도 집계라는 값싼 도구만 필요하다. 그래서 같은 질문을 자기 데이터에 적용해 볼 수 있다. 자기 선호 데이터에서 응답 토큰 분포를 세어 보고, 상위 몇십 종이 전체의 몇 퍼센트를 차지하는지만 확인해도 이 문제가 본인의 설정에서 얼마나 큰지 가늠할 수 있다.

반대로 조심할 지점도 있다. 첫째, 고빈도 토큰이 항상 무정보인 것은 아니다. "not" 같은 부정어나 "sorry" 같은 거절 표현은 흔하면서도 선호를 가르는 신호일 수 있고, 빈도만으로 자르는 hard 마스킹은 이런 토큰도 함께 지울 위험이 있다. 이것은 논문이 직접 보고한 결과가 아니라 방법의 구조에서 나오는 추론이며, 실제로 얼마나 문제가 되는지는 논문의 분석을 확인해야 한다. 둘째, 한국어처럼 조사와 어미가 토큰화에 따라 쪼개지는 언어에서는 "69종 55.1%"라는 수치 자체가 달라질 수 있다. 이 수치는 논문이 사용한 데이터와 토크나이저에 대한 측정값이다. 셋째, DPO가 오프라인 선호 데이터에 고정된다는 근본적 한계는 그대로다. 토큰 마스킹은 그 한계를 건드리지 않는다.

## 정리

- DPO 손실은 응답 토큰의 로그비율을 모든 위치에 같은 가중치로 합산하기 때문에, 선호와 무관한 기능어 토큰도 그래디언트에 섞여 들어간다.
- 논문은 69종의 토큰이 응답 토큰의 55.1%를 차지하며 선호·비선호 응답 양쪽에 비슷하게 나타난다고 보고하고, 이를 손실에서 마스킹하는 Frequency-Hard DPO를 제안한다.
- 파라미터 추가·데이터 재구성 없이 Qwen-2.5-7B-Instruct와 Llama-3-8B-Instruct에서 AlpacaEval·MT-Bench·Arena-Hard 전반의 개선이 보고됐다. 개선 폭은 본문 표에서 확인해야 한다.
- 적용 전에는 자기 데이터의 토큰 빈도 분포를 먼저 세어 보고, 빈도 기반 마스킹이 부정어·거절 표현 같은 신호 토큰을 지우지 않는지 점검하는 것이 좋다.

## 참고 자료

- Saini, Jha, Tang, Liu. "Masking Frequent Tokens Sharpens Direct Preference Optimization." 2026-09-26 제출. [arXiv:2609.32445](https://arxiv.org/abs/2609.32445)
- Rafailov et al. "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." NeurIPS 2023. [논문 페이지](https://papers.nips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html), [arXiv:2305.18290](https://arxiv.org/abs/2305.18290)
- Shao et al. "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." 2024. [arXiv:2402.03300](https://arxiv.org/abs/2402.03300)
