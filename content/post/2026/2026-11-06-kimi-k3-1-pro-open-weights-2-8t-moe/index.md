---
title: "[AI] Kimi K3.1 Pro 가중치 공개: 2.8T MoE 오픈 모델 정리"
description: "Moonshot AI가 Kimi K3.1 Pro 가중치를 Hugging Face에 공개했습니다. 2.8T MoE 구조, KDA·Gated DSA 어텐션, 가격·벤치마크, 커스텀 라이선스, 로컬 실행 현실성을 출처 기준으로 정리합니다."
date: 2026-11-06T09:00:00+09:00
lastmod: 2026-11-06
draft: false
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Open-Source(오픈소스)
  - Open-Weights
  - Hugging-Face
  - Benchmark(벤치마크)
  - Machine-Learning(머신러닝)
  - Deep-Learning(딥러닝)
  - Attention(어텐션)
  - Transformer
  - Quantization(양자화)
  - Model-Compression(모델경량화)
  - API
  - Optimization(최적화)
  - Moonshot-AI
  - Kimi
  - Kimi-K3
  - Kimi-K3.1-Pro
  - MoE
  - Mixture-of-Experts
  - Long-Context
  - Sparse-Attention
  - Linear-Attention
  - MXFP4
  - Terminal-Bench
  - GPQA
  - BrowseComp
  - OSWorld
  - Artificial-Analysis
  - OpenRouter
  - vLLM
  - SGLang
  - Unsloth
  - Frontier-Model
  - Chinese-AI
  - Model-License
  - Reasoning-Model
  - Coding-Agent
  - Inference
image: "wordcloud.png"
---

중국 Moonshot AI가 2026년 10월 23일 API로 먼저 내놓은 **Kimi K3.1 Pro**의 가중치를 11월 4일경 Hugging Face에 공개했습니다. 총 2.8조 파라미터 MoE 모델이라는 크기도 눈에 띄지만, 실무자가 더 눈여겨볼 부분은 세 가지입니다. 어텐션 층 구성이 바뀌었다는 점, API 가격이 Opus 5.5의 절반이라는 점, 라이선스가 표준 오픈소스가 아니라는 점입니다. 이 글은 모델 카드와 Moonshot 공지, Simon Willison의 정리를 바탕으로 확인된 사실과 아직 검증되지 않은 주장을 구분해 정리합니다.

---

## K3에서 K3.1 Pro까지의 흐름

Kimi K3는 2026년 7월 16일 공개됐고, 7월 27일 Modified MIT 라이선스로 가중치가 풀렸습니다. 이후 Moonshot은 K3를 추가 후학습한 K3.1 Pro를 10월 23일 API 등으로 먼저 공개하면서 가중치는 11월 4일까지 내놓겠다고 약속했고, 모델 카드가 올라오면서 그 약속이 지켜졌습니다.

| 시점 | 사건 |
|---|---|
| 2026-07-16 | Kimi K3 발표, 2.8T 파라미터·100만 토큰 컨텍스트 주장 |
| 2026-07-27 | K3 가중치 Hugging Face 공개 (Modified MIT) |
| 2026-10-23 | K3.1 Pro API 공개, 가중치는 11월 4일까지 공개 예고 |
| 2026-11-04경 | `moonshotai/Kimi-K3.1-Pro` 가중치 공개 |

## 모델 구조: 어텐션 층이 바뀌었다

모델 카드 기준 사양은 다음과 같습니다.

| 항목 | 값 |
|---|---|
| 총 파라미터 / 활성 파라미터 | 2.8T / 104B |
| 구조 | MoE, 전문가 896개 중 16개 선택 + 공유 전문가 2개 |
| 컨텍스트 길이 | 1,048,576 토큰 |
| 어텐션 | 93층 중 69층 KDA, 24층 Gated DSA |
| 비전 인코더 | MoonViT-V2 (401M) |
| 양자화 | MXFP4 가중치 / MXFP8 활성값, 양자화 인지 학습 |

<strong>MoE(Mixture of Experts, 전문가 혼합)</strong>는 토큰마다 일부 전문가 층만 활성화해 연산량을 줄이는 구조입니다. 2.8T라는 총 파라미터가 곧 토큰당 연산량은 아니고, 실제로 토큰 하나를 처리할 때 쓰는 파라미터는 104B입니다. 다만 메모리에는 전체 가중치가 올라가야 하므로 서빙 비용은 총 크기를 따라갑니다.

흥미로운 변경점은 어텐션입니다. 모델 카드는 K3의 전체 어텐션 층(Gated MLA)을 DeepSeek Sparse Attention 계열인 <strong>Gated DSA</strong>로 교체해 긴 컨텍스트 처리를 더 효율적으로 만들었다고 설명합니다. 93층 중 대부분(69층)은 KDA 층이고 전체 어텐션 성격의 층은 24층뿐입니다. 100만 토큰 컨텍스트에서 KV 캐시와 어텐션 연산이 병목이 되므로, 전체 어텐션 층의 비중을 줄이고 희소 어텐션으로 바꾸는 방향은 합리적인 선택으로 보입니다. 다만 이 변경이 실제 정확도와 지연에 얼마나 기여했는지는 모델 카드만으로 알 수 없고, 독립적인 ablation은 아직 확인하지 못했습니다.

## 가격과 벤치마크

Simon Willison의 정리에 따르면 K3.1 Pro API 가격은 입력 100만 토큰당 $2, 출력 $10으로 Opus 5.5의 절반입니다. Artificial Analysis 지수는 55점으로 Opus 5.5(58)보다 낮고 Fable 5.1·GPT-6 Astra·Gemini 4 Argon(각 53)보다 높습니다. 제3자 종합 지수 기준으로는 Opus 5.5 바로 아래, 나머지 프론티어 모델 위에 놓인 셈입니다.

모델 카드가 제시하는 수치(최대 추론 수준)는 아래와 같습니다.

| 벤치마크 | 점수 |
|---|---|
| Terminal-Bench 4.0 | 65.7 (Moonshot 공지 기준 Opus 5.5 66.4, GPT-6 Astra 58.2) |
| BrowseComp | 92.1 |
| GPQA-Diamond | 94.2 |
| OSWorld V2.1 | 79.6 |

모두 Moonshot이 직접 보고한 수치이고, 독립 재현은 확인되지 않았습니다. Terminal-Bench 4.0은 Claude Code 하네스로 평가했다고 모델 카드에 적혀 있어, 하네스 선택에 따라 점수가 달라질 수 있다는 점도 감안해야 합니다. 공지에는 환각률(Kimi Hallu Bench Hard, 도구 사용)이 23.4%에서 8.3%로 줄었다는 주장도 있지만 같은 한계가 적용됩니다.

## 사이버 위험을 줄인 오픈 웨이트

이번 공개에서 특이한 대목은 안전 처리 방식입니다. Moonshot은 오픈 웨이트로 공개하기 위해 사이버 관련 데이터를 중간 학습과 RL 단계에서 제거했다고 밝혔습니다. 공지에 따르면 사이버 위험 저감을 적용한 모델의 xdev-bench-hard pass@3은 81.0%로, 미적용 모델의 90.5%보다 낮습니다. 즉 공격 능력 지표를 약 9.5%p 낮춘 상태로 가중치를 푼 것입니다. 가중치가 공개되면 파인튜닝으로 안전 처리를 되돌릴 수 있다는 한계가 있으므로, 이 수치는 "기본 모델의 능력 수준"으로만 읽는 편이 안전합니다.

## 라이선스는 표준 오픈소스가 아니다

K3가 Modified MIT였던 것과 달리 K3.1 Pro는 모델 카드에 "Kimi K3.1 Pro License"라는 커스텀 라이선스로 표기돼 있습니다. 조항의 세부 내용은 이 글에서 직접 검증하지 못했습니다. 커뮤니티 댓글에는 연매출 2,000만 달러를 넘으면 별도 계약이 필요하다는 해석이 있었지만, 댓글 작성자의 주장일 뿐이므로 상용 도입을 검토한다면 라이선스 원문을 직접 확인해야 합니다. "가중치가 공개됐다"와 "자유롭게 쓸 수 있다"는 다른 문제입니다.

## 직접 돌릴 수 있는가

모델 카드가 권장하는 추론 엔진은 vLLM, SGLang, TokenSpeed입니다. 멀티턴·도구 호출 때는 `reasoning_content`와 `tool_calls`를 포함한 assistant 메시지 전체를 다음 요청에 되돌려 보내야 하므로, 대화 이력을 가공하는 클라이언트 코드에서 이 필드를 누락하면 동작이 달라질 수 있습니다.

하드웨어 요구량은 K3의 선례로 가늠할 수 있습니다. K3의 MXFP4 배포본이 약 594GB였고, Unsloth 가이드는 동적 1비트 양자화(UD-IQ1_S, 594GB)로도 top-1 정확도 78.9%, 더 보수적인 UD-Q2_K_XL(861GB)은 90.4%를 유지한다고 소개했습니다. 같은 총 파라미터 규모인 K3.1 Pro도 비슷한 수백 GB 단위 메모리가 필요하다고 추정되지만, K3.1 Pro 전용 양자화 수치는 확인하지 못했습니다. 결국 개인용 PC에서 돌리는 모델이라기보다 다중 GPU 서버나 대용량 통합 메모리 장비가 있어야 하는 모델이고, 대부분의 사용자에게 현실적인 경로는 OpenRouter나 Together 같은 호스팅 제공자입니다.

## 정리

| 판단 항목 | 근거 |
|---|---|
| 가격 대비 성능 | API $2/$10, 종합 지수 55로 Opus 5.5(58) 근접 |
| 구조적 특징 | 2.8T MoE·활성 104B, 69층 KDA + 24층 Gated DSA, 100만 토큰 |
| 도입 전 확인 | 커스텀 라이선스 원문, 벤치마크 독립 재현, 도구 호출 시 메시지 필드 처리 |
| 자체 호스팅 | 수백 GB 메모리 필요, 호스팅 제공자 이용이 현실적 |

벤더 수치는 모두 독립 검증 전이므로, 도입을 고민한다면 자신의 코딩·에이전트 작업 몇 가지를 직접 돌려 보고 비용과 품질을 비교하는 것이 가장 확실합니다.

## 참고 및 출처

- [Kimi-K3.1-Pro 모델 카드 — Hugging Face](https://huggingface.co/moonshotai/Kimi-K3.1-Pro)
- [Introducing Kimi K3.1 Pro — Moonshot AI](https://www.kimi.ai/blog/kimi-k3-1-pro)
- [Kimi K3.1 Pro — Simon Willison's Weblog, 2026-10-23](https://simonwillison.net/2026/Oct/23/kimi-k31-pro/)
- [Kimi K3, and what we can still learn from the pelican benchmark — Simon Willison's Weblog, 2026-07-16](https://simonwillison.net/2026/Jul/16/kimi-k3/)
- [Run Kimi K3 Locally — Unsloth Docs](https://unsloth.ai/docs/models/kimi-k3)
