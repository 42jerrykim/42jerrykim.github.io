---
title: "[AI] 하네스 택스: 코딩 에이전트 정확도는 그대로인데 비용만 최대 5배 벌어지는 이유"
description: "UC 버클리·Arena 소속 연구팀과 별개의 논문 저자들이 2026년 9월 중순 같은 주에, 코딩 에이전트 하네스 선택이 정확도는 거의 못 바꾸면서 비용만 최대 5배 벌어지게 만드는 구조를 21개·176개 실험 조합으로 각각 실측하고 분해했다."
date: 2026-09-22T02:10:00+09:00
lastmod: 2026-09-22
draft: false
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Benchmark(벤치마크)
  - Automation(자동화)
  - Productivity(생산성)
  - Software-Engineering(소프트웨어공학)
  - Prompt-Engineering(프롬프트엔지니어링)
  - MCP(Model Context Protocol)
  - Open-Source(오픈소스)
  - DevOps(데브옵스)
  - Technology(기술)
  - GPT(Generative Pre-trained Transformer)
  - ChatGPT
  - Cloud(클라우드)
  - IDE(Integrated Development Environment)
  - Coding-Agent
  - Claude-Code
  - Codex-CLI
  - SWE-bench
  - Terminal-Bench
  - HarnessTax
  - Agent-Harness
  - Context-Management
  - Cost-Optimization
  - arXiv
  - Pareto-Frontier
  - Token-Cost
  - UC-Berkeley
  - Model-Evaluation
  - Agentic-AI
image: "wordcloud.png"
---

같은 모델에 Claude Code를 얹으나 Pi를 얹으나 문제 해결률은 거의 같은데, 청구서는 두 배가 나온다면 그 차액은 어디서 온 걸까. 2026년 9월 셋째 주, 서로 모르고 작업한 두 연구팀이 이 질문에 답을 냈다. UC 버클리 Sky Lab과 Arena가 함께 쓴 HarnessTax(2026-09-16 공개)는 7개 모델과 3개 하네스를 21가지 조합으로 붙여 "하네스가 정확도보다 비용에 훨씬 더 크게 관여한다"는 걸 실측으로 보였고, 같은 주 arXiv에 올라온 "An Empirical Study of Harness Design for Coding Agents"(arXiv:2609.20804, 2026-09-17 제출)는 그 비용 차이를 만드는 내부 부품(컨텍스트 관리·플래닝·액션 스페이스)을 176개 실험 설정으로 쪼개 분해했다. 두 논문을 겹쳐 읽으면 "하네스를 고를 때 뭘 걱정해야 하는가"에 대한 꽤 구체적인 답이 나온다.

## HarnessTax — 21개 모델×하네스 조합의 실측

Melissa Z. Pan, Shuo Yang, Negar Arabzadeh, Wei-Lin Chiang, Ion Stoica, Matei Zaharia가 쓴 이 연구는 Claude Fable 5, Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-5.6 Sol/Luna, Kimi K3까지 7개 모델을 Claude Code·Codex CLI·Pi 세 하네스에 얹어 SWE-bench Lite와 Terminal-Bench 2.0에서 21개 모델–하네스 조합을 평가했다. 각 조합마다 30개 과제를 3회씩 반복해 비용(토큰·달러)과 성공률을 함께 쟀다.

가장 선명한 사례가 Claude Fable 5다. 이 모델은 Claude Code에서 97.8%, Codex에서 96.7%, Pi에서 96.7%를 풀어 세 하네스 간 성공률 차이가 1%포인트 남짓이었다. 그런데 비용은 Claude Code가 시도당 평균 1.33달러, Pi가 0.67달러로 정확히 두 배 차이였다. 이 패턴은 Fable 5만의 예외가 아니라, 공유 모델 전체에서 기하평균 기준 Claude Code가 Pi 대비 SWE-bench Lite에서 약 2.0배, Codex 대비 약 1.6배, Terminal-Bench 2.0에서 Pi 대비 약 1.5배 비쌌다. 반면 하네스가 성공률에 미치는 평균 영향은 SWE-bench Lite에서 ±2%, Terminal-Bench 2.0에서 ±5% 안쪽에 머물렀다. 연구팀은 이 비대칭을 "하네스 택스(harness tax)"라고 이름 붙였다 — 다른 하네스와 비교해보지 않고 기본값을 그대로 받아들이면, 품질 차이 없이 조용히 더 내고 있는 비용이라는 뜻이다.

두 번째 발견은 최소 구성 하네스의 경쟁력이다. Pi는 read·write·edit·bash 단 4개 도구만 제공하는 오픈소스 하네스인데도 두 벤치마크 모두에서 비용–성공률 파레토 프런티어에 올라섰다. Fable 5 기준 Pi와 Claude Code는 시도당 평균 턴 수가 15.4회 대 15.3회로 거의 같았는데도, Claude Code 쪽 비용이 약 두 배였다. 원인의 일부는 첫 호출 시점부터 드러난다 — 7개 모델 전체 평균으로 Claude Code의 초기 컨텍스트(지시문 + 도구 스키마)가 Pi보다 10배 이상 길었다. 세 번째 발견은 공급사 최적화가 곧 최적 조합을 보장하지 않는다는 것이다. Anthropic·OpenAI 여섯 개 모델과 두 벤치마크를 합친 열두 개 비교 중 아홉 개에서, 모델을 만든 회사가 아닌 다른 하네스가 더 높은 성공률을 냈다. Sonnet 4.6은 SWE-bench Lite에서 Claude Code(66.7%)보다 Codex(68.9%)에서, GPT-5.6 Sol은 Terminal-Bench 2.0에서 Codex(78.9%, 0.76달러)보다 Pi(83.3%, 0.42달러)에서 더 낫고 더 쌌다.

## Empirical Study — 비용 차이를 만드는 부품 분해

HarnessTax가 "얼마나 차이 나는가"를 바깥에서 쟀다면, Run-Ze Fan 등 9명이 쓴 이 arXiv 논문은 "왜 차이가 나는가"를 하네스 내부에서 뜯었다. 하나의 실행 루프를 고정한 채 컨텍스트 관리 전략 5종, 컨텍스트 윈도 예산, 플래닝 유무, 액션 스페이스(사전정의 도구 대 bash 전용)라는 독립 축을 각각 갈아 끼워 4개 모델 × SWE-Bench Verified/Terminal-Bench 2.1에서 176개 조합을 평가했다.

핵심 발견은 넷이다. 첫째, 컨텍스트 관리는 컨텍스트 윈도 예산이 빠듯할 때만 값어치가 커진다 — 효과의 대부분이 "요약을 잘해서"가 아니라 "컨텍스트 오버플로로 실행이 중간에 끊기는 실패를 막아서" 나온다. 둘째, 5가지 컨텍스트 관리 전략 중 규칙 기반으로 불필요한 단계를 먼저 걷어낸(elision) 뒤 LLM으로 요약하는 방식이 전체 효율에서 가장 강력했다. 셋째, 플래닝의 역할은 모델 크기에 따라 뒤집힌다 — 약한 모델에는 정확도를 지탱하는 스캐폴딩이지만, 강한 모델에서는 같은 정확도를 더 적은 비용으로 얻는 절약 장치로 기능이 바뀐다. 넷째, 사전정의된 도구는 bash에 서툰 모델의 성능을 끌어올리지만, bash에 능숙한 모델은 bash 전용 인터페이스만으로도 충분했다 — 도구를 더 얹는 게 항상 이득은 아니라는 뜻이다.

## 두 연구를 겹쳐 읽으면

HarnessTax의 "10배 긴 초기 컨텍스트"와 Empirical Study의 "컨텍스트 관리는 예산이 빠듯할 때 가치가 커진다"는 발견은 같은 그림의 양면이다. 하네스가 지시문과 도구 스키마를 두툼하게 들고 시작할수록 컨텍스트 예산은 더 빨리 빠듯해지고, 그 순간부터 컨텍스트 관리 전략의 효과가 커지기 시작한다. 반대로 Pi처럼 도구 4개로 시작하는 하네스는 애초에 예산 압박이 덜하니 정교한 컨텍스트 관리가 없어도 파레토 프런티어에 오를 수 있다. 즉 "무거운 하네스 + 정교한 컨텍스트 관리"와 "가벼운 하네스 + 단순한 관리"는 비슷한 결과에 도달하는 두 가지 다른 경로이고, 그 중간 지점 — 무거운 하네스인데 컨텍스트 관리는 기본값 — 이 하네스 택스가 가장 크게 발생하는 지점이라는 결론이 나온다.

## 실무 판단 기준

두 연구 모두 "이 하네스가 무조건 낫다"는 결론을 내지 않는다는 점이 오히려 실무적으로 중요하다. 판단은 이렇게 나뉜다.

- **같은 모델을 여러 워크플로에 반복 투입하는 경우**: 기본 하네스를 그대로 쓰기 전에 최소 하나의 대안(오픈소스 최소 하네스 등)과 비용·성공률을 나란히 재보는 것이 이득이다. 반복 횟수가 많을수록 2–5배 비용 차이가 누적된다.
- **컨텍스트 윈도 예산이 넉넉한 조직**: Empirical Study의 결론대로 컨텍스트 관리 최적화의 효과가 작으므로, 이 축에 시간을 쓰기보다 다른 병목(도구 설계, 플래닝 여부)을 먼저 본다.
- **약한 모델을 쓰는 경우**: 사전정의 도구와 플래닝을 갖춘 무거운 하네스가 여전히 정확도에 실질적으로 기여하므로, 비용만 보고 최소 하네스로 바꾸면 성공률이 떨어질 수 있다.
- **강한 모델 + bash 능숙**: 도구를 더 얹기보다 bash 전용 인터페이스로 단순화하는 쪽이 비용 대비 이득이 크다.
- **일회성 작업이거나 작업량이 적은 경우**: 하네스 택스가 누적될 표본이 적으므로 굳이 비교 실험을 벌일 필요는 없다.

## 한계

두 연구 모두 SWE-bench 계열과 Terminal-Bench라는 코딩 작업 벤치마크에 한정돼 있어, 리서치나 글쓰기 같은 다른 도메인 에이전트 작업에 그대로 일반화되는지는 검증되지 않았다. HarnessTax 저자들도 이 결과가 "모델이 훈련 중 접했을 수 있는 두 오픈소스 벤치마크"에 한정된 것일 수 있다고 명시했다. 또한 Empirical Study의 발견은 컨텍스트 예산과 모델 강도라는 두 변수가 서로 얽혀 있어("예산이 빠듯할 때만", "강한 모델일수록") 조건부 결론이지, 하나의 절대적인 최적 하네스 설계를 제시하지는 않는다.

## 참고 자료

- [HarnessTax: How Much Does the Harness Matter for Coding Agents? (2026-09-16)](https://harnesstax.github.io/)
- [An Empirical Study of Harness Design for Coding Agents (arXiv:2609.20804, 2026-09-17)](https://arxiv.org/abs/2609.20804)
