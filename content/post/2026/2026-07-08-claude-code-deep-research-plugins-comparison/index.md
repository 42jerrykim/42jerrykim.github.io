---
title: "[AI] Claude Code 딥리서치 플러그인 6종 비교: 실사용자 리뷰로 검증"
description: "insane-research·199-biotechnologies·Weizhena·hyperresearch·daymade·Defiect 6종을 API 키 요구·라이선스·GitHub 이슈 실사용자 리뷰로 비교하고, claim ledger 검증 게이트로 벤치마크 우위 주장을 교차검증했다."
date: 2026-07-08T13:00:00+09:00
lastmod: 2026-07-08
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Automation(자동화)
  - Open-Source(오픈소스)
  - GitHub
  - Productivity(생산성)
  - Workflow(워크플로우)
  - Comparison(비교)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Review(리뷰)
  - Tips
  - How-To
  - Case-Study
  - Deep-Dive
  - Best-Practices
  - Documentation(문서화)
  - Innovation(혁신)
  - Technology(기술)
  - Blog(블로그)
  - Web(웹)
  - API(Application Programming Interface)
  - Reference(참고)
  - Education(교육)
  - Configuration(설정)
  - Troubleshooting(트러블슈팅)
  - Software-Architecture(소프트웨어아키텍처)
  - Terminal
  - Benchmark
  - Security(보안)
image: wordcloud.png
draft: true
---

Claude Code 플러그인 마켓플레이스에는 2026년 7월 기준 "딥리서치"를 표방하는 프로젝트가 최소 6종 있다. 저마다 "타사 대비 압도적"이라고 홍보하지만, 정작 API 키 요구 여부·라이선스·실사용 중 파이프라인이 멈추는지 같은 실무 질문에는 대답이 별로 없다. 이 글은 [insane-research](https://github.com/fivetaku/insane-research), [claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill)(199-biotechnologies), [Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills)(Weizhena), [hyperresearch](https://github.com/jordan-gibbs/hyperresearch)(Jordan Gibbs), [deep-research](https://github.com/daymade/claude-code-skills/blob/main/deep-research/SKILL.md)(daymade), [deep-research-plugin](https://github.com/Defiect/deep-research-plugin)(Defiect) 6종을 GitHub API 통계·이슈 트래커·Hacker News·X/Threads에서 직접 조사하고, insane-research의 claim ledger 검증 게이트로 "타사 대비 우위" 주장 자체를 검증해봤다.

## 개요: 6개 프로젝트와 추천 대상

여섯 프로젝트는 접근 방식이 뚜렷이 갈린다. **검증 파이프라인 정교화**에 집중하는 계열(199-biotechnologies, Defiect, daymade), **검색 접근성(사이트 우회) 자체**를 강점으로 삼는 계열(insane-research/insane-search), **조사 결과를 영속적 지식창고로 축적**하는 계열(hyperresearch), **사람이 단계마다 개입**하는 human-in-the-loop 계열(Weizhena)로 나눌 수 있다. 이 글은 Claude Code CLI로 리서치를 자동화하려는 개발자, 이미 하나를 쓰고 있지만 다른 대안과 실제 차이를 알고 싶은 사용자, "벤치마크에서 이겼다"는 문구를 그대로 믿어도 되는지 궁금한 독자를 대상으로 한다.

## 아키텍처/구조: 파이프라인 길이와 검증 방식의 차이

여섯 프로젝트 모두 "질문 분해 → 병렬 검색 → 교차검증 → 종합"이라는 큰 틀은 같지만, 파이프라인 길이와 검증을 강제하는 방식이 다르다. insane-research는 7단계 파이프라인에 `claim_ledger.jsonl` + `validate_ledger.py`라는 **결정론적 검증 게이트**를 붙여, 고위험 주장이 반증 검색을 거치지 않으면 코드 레벨에서 최종 보고서에 실리지 못하게 막는다. 199-biotechnologies는 8단계(Scope→Plan→Retrieve→Triangulate→Outline→Synthesize→Critique→Package)로 5~10개 동시 검색과 서브에이전트를 병렬 운용한다. hyperresearch는 16단계로 가장 길며, 조사 결과를 Obsidian과 비슷한 영속 지식 위키(vault)에 누적하는 점이 다른 5종과 구분된다. Weizhena는 outline 생성 → deep investigation의 2단계로 가장 단순하지만, 매 단계 사람이 확인하는 human-in-the-loop이 핵심이다. daymade는 7단계(P0-P7)로 원본 검색 결과를 폐기하고 정제된 노트만 남겨 컨텍스트를 60~70% 절감한다고 명시한다. Defiect는 dr-lead(Opus)·dr-scout(Sonnet)·dr-analyst(Opus)·dr-writer(Opus) 4-agent로 역할을 분리한 설계이지만, 실제 커밋은 1개뿐이다.

## 주요 기능 상세

### insane-research (GPTaku)

자매 플러그인 [insane-search](https://github.com/fivetaku/insane-search)와 결합하면 로그인·CAPTCHA가 없는 한 네이버 블로그·레딧·X 등 대부분의 사이트를 **API 키 없이** 우회 접근할 수 있다는 점이 다른 5종과 가장 뚜렷이 구분되는 차별점이다. 실사용자가 Threads에 남긴 후기("네이버는 insane search가 잘 뚫립니다, API 발행도 필요 없쥬")로도 이 차별점이 교차 확인된다. 이 글 자체도 insane-research로 조사했다. 마켓플레이스는 717★, 자매 플러그인 insane-search는 1,847★다(2026-07 기준, GitHub API 직접 조회).

### claude-deep-research-skill (199-biotechnologies)

"엔터프라이즈급"을 표방하며 819★를 확보했고, Markdown/HTML/PDF 다중 포맷 출력을 지원한다. 주요 주장에 10개 이상 출처·3개 이상 인용을 요구하는 명시적 품질 기준이 강점이다. 다만 저장소에 **명시적 LICENSE 파일이 없어** 실사용자가 이슈로 직접 지적했고("팀 내부 마켓플레이스에 벤더링하고 싶은데 라이선스가 없어 조건이 불명확하다", [이슈 #2](https://github.com/199-biotechnologies/claude-deep-research-skill/issues/2)), "Opus 4.8 auto mode의 안전 분류기가 서브에이전트의 search-cli 사용을 차단한다"는 실사용 문제도 보고돼 있다([이슈 #9](https://github.com/199-biotechnologies/claude-deep-research-skill/issues/9)).

### Deep-Research-skills (Weizhena)

Claude Code뿐 아니라 OpenCode·Codex에도 이식돼 크로스플랫폼으로 쓸 수 있고, 1,547★로 조사 대상 중 가장 큰 커뮤니티를 보유한다. 포크 프로젝트(hermes-deep-research)의 실측 데이터에 따르면 Opus 모델을 전체 파이프라인(수집+작성)에 그대로 쓰면 11항목×43필드 규모 조사에서 비용이 급격히 커져 "수집 모델과 작성 모델을 분리하라"는 실사용자 제안이 이슈로 올라와 있다([이슈 #6](https://github.com/Weizhena/Deep-Research-skills/issues/6)).

### hyperresearch (Jordan Gibbs)

조사 결과를 세션 간에 누적되는 검색 가능한 지식 위키로 만든다는 점이 독특하다. 490★로 규모는 작지만 이슈 트래커가 활발하다. 저자는 자신의 [Medium 글](https://medium.com/@jordan_gibbs/i-built-the-most-intelligent-deep-research-agent-13c3de5ebc8d)에서 "RACE DeepResearchBench에서 OpenAI·Google·NVIDIA의 딥리서치 솔루션을 능가한다"고 주장하지만, 수치가 이미지로만 제시돼 텍스트로 검증할 수 없었고 [DeepResearchBench 공식 리더보드(Epoch AI)](https://epoch.ai/benchmarks/deepresearchbench)에도 hyperresearch 항목이 없다 — 이번 조사에서는 **미확정(판단 보류)** 으로 처리했다. 실사용자 이슈로는 "10단계(초안 작성)에서 무한 루프에 걸린다"([이슈 #30](https://github.com/jordan-gibbs/hyperresearch/issues/30)), "동기화 시 노트 ID가 충돌해 데이터가 조용히 유실된다"([이슈 #25](https://github.com/jordan-gibbs/hyperresearch/issues/25)) 등이 보고됐다.

### deep-research (daymade/claude-code-skills)

리드 에이전트+서브에이전트 구조로 원본 검색 결과를 폐기하고 정제된 노트만 유지해 컨텍스트를 60~70% 절감한다고 명시한다. 시간 민감 주장에 독립 소스 2개 이상을 요구하고 신뢰도 표시(High/Medium/Low)를 노출하는 등 실무형 안전장치가 촘촘하다. 다만 대형 스킬 모음집(1,252★)의 일부라 이 스킬만의 독립적 커뮤니티 신호를 분리해 확인하긴 어렵다.

### deep-research-plugin (Defiect)

evidence graph와 품질 게이트를 앞세운 설계 자체는 흥미롭지만, 총 커밋 1개·스타 2개·이슈와 PR 0개로 **활성도가 사실상 없다**. 실사용 검증 사례를 전혀 찾을 수 없었다는 것 자체가 이번 조사의 결론 중 하나다.

## 왜 사용해야 할까 — 실제 이점

여섯 프로젝트를 나란히 놓고 보면 "딥리서치 플러그인"이라는 카테고리가 실제로 해결하는 문제가 뚜렷해진다. 웹 UI 기반 서비스(Perplexity, ChatGPT, Gemini)와 달리 CLI 안에서 세션이 로컬 파일로 남아 재개할 수 있고, 오픈소스라 파이프라인을 그대로 읽고 커스터마이징할 수 있으며, 출처 등급이나 claim ledger 같은 장치로 "어디까지 믿을 근거가 있는지"를 결과물에 드러낸다. 다만 이 이점은 프로젝트마다 구현 완성도가 다르다는 게 이번 조사의 핵심 발견이다.

## 적용 시나리오와 판단 기준

| 상황 | 추천 |
|---|---|
| API 키 없이 바로 쓰고 싶다 / 한국어·차단된 사이트 접근이 중요하다 | insane-research(+insane-search) |
| 라이선스가 명확해야 하고 다중 출력 포맷(PDF)이 필요한 대규모 조직 | 199-biotechnologies(단, LICENSE 이슈는 직접 확인) |
| Claude Code 외에 OpenCode·Codex에서도 같은 워크플로우가 필요하다 | Weizhena/Deep-Research-skills |
| 조사 결과를 세션 간 지식으로 누적하고 싶다 | hyperresearch |
| 컨텍스트/토큰 효율이 최우선이고 이미 daymade 마켓플레이스를 쓴다 | daymade deep-research |

**부적합하거나 주의할 경우**: 활성도가 사실상 없는 Defiect의 `deep-research-plugin`은 설계만 보고 프로덕션에 바로 투입하기엔 위험 부담이 크다. 8~16단계급 다단계 파이프라인은 정교한 만큼 중간에 멈추거나 데이터가 유실될 지점도 많으므로, 짧고 단순한 사실 확인에는 과할 수 있다.

## 장단점과 종합 평가

세 프로젝트(199-biotechnologies, Weizhena, hyperresearch) 모두 GitHub 이슈에서 **LICENSE 파일 부재로 인한 사용 조건 불명확**과 **다단계 파이프라인 중간 지점에서의 정체·데이터 유실**이 공통으로 지적됐다. "8~16단계의 정교한 파이프라인"이라는 설계상 장점이 동시에 "중간에 꼬일 지점이 많다"는 리스크로 이어질 수 있다는 뜻이다. 또한 hyperresearch와 199-biotechnologies가 저장소 설명에 명시한 "타사 대비 압도적 우위" 벤치마크 주장은 둘 다 제작자 자기평가이며, 이번 조사의 반증 검색에서 독립적인 제3자 벤치마크 재현 결과를 찾지 못했다. 실제 선택 기준은 벤치마크 수치보다 API 키 요구 여부·라이선스 명시 여부·이슈 트래커의 실사용 리포트 밀도로 판단하는 편이 안전하다.

## 시작하기

insane-research를 API 키 없이 바로 써보려면 아래 두 명령이면 충분하다.

```bash
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
/plugin install insane-research@gptaku-plugins
```

199-biotechnologies나 Weizhena 계열처럼 검색 API 프로바이더가 필요한 스킬은 클론 후 스킬 디렉터리에 배치한다.

```bash
git clone https://github.com/199-biotechnologies/claude-deep-research-skill.git ~/.claude/skills/deep-research
# Brave/Serper/Exa/Jina/Firecrawl 중 최소 하나의 API 키를 환경변수로 설정
```

## 참고 문헌

1. [insane-research — GitHub](https://github.com/fivetaku/insane-research): 파이프라인·A~E 출처 등급·claim ledger 검증 게이트 원출처.
2. [gptaku_plugins — GitHub](https://github.com/fivetaku/gptaku_plugins): insane-research가 속한 마켓플레이스.
3. [insane-search — GitHub](https://github.com/fivetaku/insane-search): API 키 없는 우회 접근 자매 플러그인.
4. [claude-deep-research-skill — GitHub](https://github.com/199-biotechnologies/claude-deep-research-skill): 8단계 엔터프라이즈급 파이프라인.
5. [199-biotechnologies 이슈 #2 — LICENSE 요청](https://github.com/199-biotechnologies/claude-deep-research-skill/issues/2)
6. [199-biotechnologies 이슈 #9 — search-cli 차단](https://github.com/199-biotechnologies/claude-deep-research-skill/issues/9)
7. [Deep-Research-skills — GitHub](https://github.com/Weizhena/Deep-Research-skills): human-in-the-loop 2단계 구조.
8. [Weizhena 이슈 #6 — 실측 비용 데이터](https://github.com/Weizhena/Deep-Research-skills/issues/6)
9. [hyperresearch — GitHub](https://github.com/jordan-gibbs/hyperresearch): 16단계 영속 지식 위키.
10. [I Built the Most Intelligent Deep Research Agent — Medium](https://medium.com/@jordan_gibbs/i-built-the-most-intelligent-deep-research-agent-13c3de5ebc8d): 저자 본인의 벤치마크 우위 주장(제3자 검증 없음).
11. [hyperresearch 이슈 #25 — 동기화 데이터 유실](https://github.com/jordan-gibbs/hyperresearch/issues/25)
12. [hyperresearch 이슈 #30 — 10단계 무한루프](https://github.com/jordan-gibbs/hyperresearch/issues/30)
13. [DeepResearchBench 리더보드 — Epoch AI](https://epoch.ai/benchmarks/deepresearchbench): hyperresearch 항목 부재 확인.
14. [daymade/claude-code-skills — deep-research SKILL.md](https://github.com/daymade/claude-code-skills/blob/main/deep-research/SKILL.md)
15. [deep-research-plugin — GitHub](https://github.com/Defiect/deep-research-plugin): 4-agent 설계, 활성도 사실상 없음.
16. [실사용자 Threads 후기 — insane-search API 키 불필요 확인](https://www.threads.com/@yeon.gyu.kim/post/DZ6O0MZktpv/)
