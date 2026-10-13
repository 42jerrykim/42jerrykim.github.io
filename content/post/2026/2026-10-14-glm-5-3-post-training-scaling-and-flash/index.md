---
title: "[AI] GLM-5.3: 사후학습만 늘린 모델과 새 베이스로 만든 Flash"
description: "Z.ai의 GLM-5.3은 베이스 모델을 재학습하지 않고 사후학습만 확장했고, GLM-5.3-Flash는 30T 토큰 멀티모달 코퍼스로 새로 학습한 320B-A18B MoE다. 두 모델의 차이, 공개 수치의 한계, 사이버 역량 평가가 주는 시사점을 정리한다."
date: 2026-10-14T01:30:00+09:00
lastmod: 2026-10-14
draft: false
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Machine-Learning(머신러닝)
  - Deep-Learning(딥러닝)
  - Reinforcement-Learning(강화학습)
  - Attention(어텐션)
  - Transformer
  - Benchmark
  - Performance(성능)
  - Open-Source(오픈소스)
  - Hugging-Face
  - Security(보안)
  - Software-Engineering(소프트웨어공학)
  - Case-Study
  - Best-Practices
  - Z.ai
  - GLM
  - GLM-5.3
  - GLM-5.3-Flash
  - Post-Training
  - MoE
  - Mixture-of-Experts
  - Multimodal
  - Open-Weight
  - Coding-Agent
  - Agentic-AI
  - Terminal-Bench
  - KV-Cache
  - Linear-Attention
  - Cyber-Capability
  - Binary-Exploitation
  - Anthropic
  - Frontier-Red-Team
  - Artificial-Analysis
  - Pricing
  - Model-Comparison
---

같은 "GLM-5.3"이라는 이름을 단 모델이 2주 간격으로 두 번 나왔다. 하나는 기존 베이스 모델에 사후학습(post-training)만 더 얹은 모델이고, 다른 하나는 30T 토큰 멀티모달 코퍼스로 처음부터 새로 학습한 별개의 모델이다. 이름이 같아서 둘을 같은 계열의 점진적 개선으로 읽기 쉽지만, 이 둘은 프론티어 랩이 쓰는 서로 다른 두 전략의 사례다. 이 글은 두 모델이 무엇이 다른지, 공개된 수치 중 어디까지 믿을 수 있는지, 그리고 Anthropic Frontier Red Team의 평가가 왜 별도로 주목받았는지를 정리한다.

## 두 개의 GLM-5.3

Z.ai는 2026-08-14에 GLM-5.3을 발표했다. MarkTechPost 보도의 제목이 "Z.ai Ships GLM-5.3 Without Retraining the Base Model"인 것처럼, 핵심은 GLM-5.2와 같은 베이스 위에서 사후학습만 확장했다는 점이다. 반면 2026-08-26에 공개된 GLM-5.3-Flash는 GLM-5 시리즈 최초의 네이티브 멀티모달 모델이며, MarkTechPost에 따르면 "30T 토큰 멀티모달 코퍼스로 새로 학습한 베이스 모델"에서 출발한다. 즉 Flash는 5.3의 경량판이 아니라, 가중치를 공유하지 않는 별도의 모델이다.

이 구분이 중요한 이유는 비교의 의미가 달라지기 때문이다. GLM-5.2에서 5.3으로의 향상은 "같은 베이스에서 사후학습이 얼마나 성능을 끌어올릴 수 있는가"를 보여 주는 실험이고, 5.3에서 Flash로의 변화는 "아키텍처와 사전학습 데이터를 바꾸면 무엇이 달라지는가"를 보여 주는 사례다. 두 전략이 같은 시기에 병행된다는 사실 자체가 Z.ai의 자원 배분을 읽는 단서가 된다.

| 구분 | GLM-5.3 | GLM-5.3-Flash |
|---|---|---|
| 공개일 | 2026-08-14 | 2026-08-26 |
| 베이스 모델 | GLM-5.2와 동일(재학습 없음) | 30T 토큰 멀티모달 코퍼스로 신규 학습 |
| 입력 | 텍스트 | 텍스트·이미지(·영상) |
| 규모 | MoE (본편 규모는 이 글에서 다루지 않음) | 총 320B, 토큰당 활성 18B |
| 라이선스 | 안전성 평가 후 가중치 공개 예정으로 보도 | MIT, Hugging Face 공개 |

## 사후학습 스케일링이 의미하는 것

사전학습 연산을 늘리지 않고도 코딩·에이전트 벤치마크가 크게 뛴다는 주장은 최근 업계 흐름과 맞닿아 있다. 새 베이스를 만드는 비용은 매우 크고 주기도 길다. 반면 강화학습 기반 사후학습은 검증 가능한 과제(코드 실행, 터미널 작업)를 보상 신호로 쓸 수 있어, 기존 베이스를 반복해서 다듬는 쪽이 투자 대비 효율이 높다는 판단이 가능하다. GLM-5.3이 그 판단의 한 사례다.

다만 여기서 한계를 짚어야 한다. 사후학습이 끌어올릴 수 있는 상한은 베이스가 가진 잠재 능력에 묶여 있다. 그래서 Z.ai도 얼마 뒤 아예 새 베이스를 학습한 Flash를 내놓았고, 이는 사후학습 스케일링이 만능이 아니라는 간접 증거로 읽을 수 있다. 이 해석은 필자의 추론이며 Z.ai가 이렇게 밝힌 것은 아니다.

## GLM-5.3-Flash의 구조

MarkTechPost와 vLLM 레시피에 따르면 Flash는 320B 총 파라미터 중 토큰당 18B만 활성화하는 MoE 모델이다. 45개 레이어에 KDA 선형 어텐션 층과 NoPE 스파스 MLA 층을 교차 배치하고, 토큰마다 288개 전문가 중 8개로 라우팅한다. 컨텍스트 길이는 1,048,576토큰이다. 선형 어텐션은 국소 의존성을 싸게 처리하고, 스파스 어텐션은 전역적으로 관련 있는 문맥을 가져오는 역할로 설명된다.

100만 토큰 수준에서는 어텐션 연산 자체보다 "어떤 키를 볼지 고르는 인덱서"가 병목이 된다. Z.ai는 이를 위해 IndexPool이라는 방식으로 인덱서 키 벡터 묶음을 가중 풀링해 지연과 메모리를 억제한다고 밝혔고, GLM-5.3 대비 어텐션 연산 약 3분의 1, KV 캐시 4.4분의 1이라고 보고했다. 이 수치는 Z.ai가 보고한 값이며 독립 검증은 확인하지 못했다.

## 벤치마크 수치를 읽는 법

Flash의 보고 수치는 Terminal-Bench 2.1에서 84.3(Claude Opus 4.8 85.0, GPT-5.6 Terra 87.4), DeepSWE v1.1에서 63.4(GLM-5.2 46.2), AutomationBench에서 48.8(GLM-5.2 26.2)이다. 독립 평가 기관인 Artificial Analysis는 Intelligence Index v4.1.1에서 57점을 매겼다. MarkTechPost 스스로도 표의 대부분이 Z.ai가 보고한 값이며 벤치마크마다 하네스가 달라 교차 비교는 설정에 좌우된다고 단서를 단다.

가격도 같은 방식으로 읽어야 한다. API 표준 가격은 입력 100만 토큰당 $0.15(캐시 입력 $0.03), 출력 $0.50이다. 태스크당 비용은 MarkTechPost가 할인 티어 기준 $0.045라고 적었는데, Artificial Analysis 모델 페이지는 다른 집계 값을 보여 줄 수 있다. 티어와 집계 방식이 다르면 단일 숫자로 단정하기 어렵다. 같은 보도는 Flash가 "강한 지능 대비 비용이지만 느리고 장황하다"고 평가한다. 시각 능력도 약점으로 지목되어, BabyVision과 MVBench에서는 Gemini 3.7 Flash에 뒤진다.

## 사이버 역량: 임계선을 넘었다는 평가

가장 눈여겨볼 대목은 성능표가 아니라 안전성 평가다. Anthropic Frontier Red Team은 내부 Binary Exploitation 벤치마크에서 무작위로 고른 100개 과제로 모델을 평가했다. Simon Willison이 인용한 내용에 따르면 GLM-5.3은 4%, Claude Mythos Preview는 6%에서 완전한 제어 흐름 하이재킹에 성공했고, 이전 세대인 Claude Opus 4.6과 GLM-5.2는 하나도 성공하지 못했다. 리포트는 GLM-5.3이 Mythos Preview보다 낮은 성능이라 해도 의미 있는 임계선을 분명히 넘었다고 평가한다.

여기서 읽어야 할 점은 두 가지다. 첫째, 4%라는 절대 수치는 작지만 0%에서의 도약이라는 점이 핵심이다. 둘째, 같은 베이스에 사후학습만 더한 모델에서 이런 도약이 나타났다는 것은, 오픈웨이트 모델의 공격적 사이버 역량이 새 사전학습 없이도 빠르게 따라올 수 있음을 뜻한다. 가중치를 공개하는 모델이라면 안전성 평가와 하드닝 이후에 공개하겠다는 Z.ai의 방침이 실제로 무엇을 막는지 계속 지켜볼 일이다.

## 어떻게 판단할 것인가

모델을 고를 때는 다음 기준이 현실적이다.

- 코딩 에이전트에 비용 대비 성능이 필요하고 API로 쓸 수 있다면 Flash는 후보에 올릴 만하다. 다만 자체 호스팅은 FP8 체크포인트만 약 306GiB이고 Hopper 이상 GPU가 필요해, 8-GPU 노드 이상이 있는 조직이 아니면 현실적이지 않다.
- 이미지·화면 이해가 핵심이라면 약점으로 지목된 벤치마크를 직접 확인한다.
- 벤더 보고 수치만으로 결정하지 말고, 자신의 과제와 하네스로 소규모 평가를 돌린다. 하네스 설정에 따라 순위가 바뀔 수 있다.
- 보안 민감 환경에서는 오픈웨이트 모델의 공격 역량 상승을 위협 모델에 반영한다.

## 정리

GLM-5.3과 GLM-5.3-Flash는 이름은 같지만 "기존 베이스를 다듬는 전략"과 "새 베이스를 처음부터 학습하는 전략"이라는 서로 다른 선택이다. 공개 수치의 상당수는 벤더 보고값이므로 독립 평가와 직접 검증이 필요하다. 그리고 사후학습만으로 사이버 역량이 0%에서 4%로 넘어갔다는 외부 평가는 성능 경쟁과 별개로 오래 기억해 둘 신호다. 이 글의 수치는 2026-10-14 기준 확인 가능한 보도에 근거하며, 일부 원문(GLM-5.3 본편 보도)은 접근 제한으로 직접 확인하지 못해 본문에서 세부 수치를 인용하지 않았다.

## 참고 자료

- [MarkTechPost, Z.ai Releases GLM-5.3-Flash (2026-08-26)](https://www.marktechpost.com/2026/08/26/z-ai-releases-glm-5-3-flash-a-320b-a18b-natively-multimodal-moe-with-a-1m-token-context/)
- [Artificial Analysis, GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash)
- [Simon Willison, Anthropic Frontier Red Team (2026-09-29)](https://simonwillison.net/2026/Sep/29/anthropic-frontier-red-team/)
