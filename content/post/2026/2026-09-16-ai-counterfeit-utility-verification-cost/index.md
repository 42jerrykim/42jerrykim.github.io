---
title: "[AI] AI가 썼다고 느끼는 순간, 독자 78%가 떠난다 — 위조 효용과 검증 비용의 경제학"
description: "MIT 경제학자 Christian Catalini의 '위조 효용' 개념과 668명 개발자 설문에서 나온 독자 이탈률 78%·71%를 통해, AI가 생성 비용은 낮췄지만 검증 비용은 그대로 남겨둔 소프트웨어 개발 현실을 짚는다."
date: 2026-09-16T07:00:00+09:00
lastmod: 2026-09-16
draft: false
image: "wordcloud.png"
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Software-Engineering(소프트웨어공학)
  - Code-Review(코드리뷰)
  - Code-Quality(코드품질)
  - Maintainability(유지보수성)
  - Case-Study
  - Deep-Dive
  - Governance
  - Compliance
  - Best-Practices
  - Productivity(생산성)
  - Automation(자동화)
  - Open-Source(오픈소스)
  - Prompt-Engineering(프롬프트엔지니어링)
  - Comparison(비교)
  - Reference(참고)
  - Anthropic
  - Claude
  - Martin-Fowler
  - Bryan-Cantrill
  - Christian-Catalini
  - Cynthia-Dunlop
  - Counterfeit-Utility
  - Hollow-Economy
  - Verification-Cost
  - AI-Generated-Content
  - Technical-Writing
  - Reader-Trust
  - AGI
---

2026년 9월 첫째 주, 서로 다른 세 사람이 서로 다른 매체에 쓴 글이 같은 결론으로 수렴했다. MIT 경제학자 Christian Catalini는 논문에서 "AI가 낮추는 건 생성 비용이지 검증 비용이 아니다"라고 썼고, Oxide Computer의 Bryan Cantrill은 자신의 블로그에 독자 668명을 설문한 수치를 인용하며 "AI가 쓴 것 같다고 느끼는 순간 독자의 78%가 즉시 떠난다"고 적었다. 그리고 Martin Fowler는 자신의 정기 코너 "Fragments"에서 이 둘을 나란히 소개하며 저작권 소송·에이전트 거버넌스 이슈까지 한데 묶었다. 이 글은 이 세 출처를 원문까지 추적해, "생성은 공짜에 가까워졌는데 검증은 왜 그대로인가"라는 질문이 코드 리뷰든 블로그 글이든 똑같은 모양으로 반복되는 이유를 짚는다.

## Catalini의 "위조 효용" — 측정 가능성이 새로운 자동화 경계선이 되다

Christian Catalini(MIT)는 Xiang Hui(워싱턴대), Jane Wu와 함께 쓴 논문 "Some Simple Economics of AGI"(arXiv:2602.20946)와 이를 정리한 에세이 "The Economics of AI: Verification as the New Scarcity"에서, 자동화의 경계선이 이동했다고 주장한다. 예전에는 "루틴 작업이냐 아니냐"가 무엇을 자동화할 수 있는지를 갈랐다면, 지금은 "결과를 측정할 수 있느냐 없느냐"가 그 자리를 대신한다는 것이다. 테스트를 통과하는지, 벤치마크 점수가 나오는지처럼 측정 가능한 작업은 AI가 만든 결과물을 곧바로 검증할 수 있지만, 코드의 장기 유지보수성이나 글의 논지가 실제로 타당한지처럼 측정하기 어려운 작업에서는 겉보기엔 그럴듯하지만 실질이 빈 결과물이 쌓인다.

Catalini는 이렇게 "눈에 보이는 지표는 만족시키지만 그 지표가 원래 대변해야 할 목적은 배신하는 산출물"을 <strong>위조 효용(counterfeit utility)</strong>이라 부른다. 예를 들어 교육용 AI 튜터가 학생의 참여 시간(측정 가능한 지표)은 늘리면서 실제 학습(측정하기 어려운 목적)은 방해하거나, 고객 응대 챗봇이 티켓 종결 건수는 늘리면서 정당한 불만은 조용히 눌러버리는 경우다. 이런 위조 효용이 조직·산업 전체로 누적되면 Catalini가 <strong>Hollow Economy(텅 빈 경제)</strong>라 부르는 상태에 이른다 — 겉으로 보이는 활동량과 대시보드 지표는 화려하게 상승하지만, 그 밑에서는 사람의 실질 역량이 약해지고, 숨은 기술부채와 서로 연관된 오류가 쌓이며, 정작 누구도 그 결과를 자신 있게 책임지지 못하는 상태다.

| 구분 | 기존 자동화 경계 | Catalini가 말하는 새 경계 |
|---|---|---|
| 판단 기준 | 루틴 작업 여부 | 결과의 측정 가능 여부 |
| AI가 잘하는 영역 | 반복적·정형적 업무 | 생성(generation) 전반 |
| 여전히 사람이 필요한 영역 | 비정형·창의적 업무 | 검증(verification) 전반 |
| 방치했을 때의 위험 | 자동화 실패로 업무 지연 | 위조 효용이 누적된 Hollow Economy |

## 독자는 어떻게 "이거 AI가 썼네"를 알아채는가 — 668명 설문이 보여준 이탈률

Cantrill이 2026년 9월 5일 자신의 블로그(bcantrill.dtrace.org)에 올린 글 "The Revolt of the Reader"는 기술 블로그 뉴스레터 "Write That Blog"를 운영하는 Cynthia Dunlop이 그해 6월 16일 발표한 설문 결과를 인용한다. Dunlop은 X·Bluesky·LinkedIn에 설문을 공유해 개발자·기술 블로그 독자 668명의 응답을 모았다(익명 자발 참여 설문이라 표본이 전체 개발자 인구를 대표한다고 보장할 수는 없다는 점은 Dunlop 본인도 밝히고 있다). 그 결과는 다음과 같다.

- 글이 LLM이 쓴 것 같다고 느끼는 순간, 응답자의 <strong>78%가 즉시 읽기를 중단</strong>한다.
- 그중 <strong>71%는 이후로도 그 저자의 글을 계속 피한다</strong>.
- <strong>98%는 다소 거칠어도 저자 본인이 직접 쓴 글을 AI가 다듬은 글보다 선호</strong>한다고 답했다.

Cantrill은 이 수치를 자신의 에세이에서 인용하며 확산시켰고, Fowler는 다시 이를 자신의 Fragments 코너에 소개하며 "78% of readers stop immediately once they sense something is the work of a stochastic parrot, and 71% go on to blacklist the writer"라는 문장으로 요약했다. 즉 지금 이 통계가 퍼지는 경로는 Dunlop(1차 설문)→Cantrill(자신의 관찰과 결합해 재해석)→Fowler(더 넓은 독자층에 요약 전파)라는 3단 인용 구조를 거친 것이다. 표본이 자기선택적이라는 한계는 있지만, 세 명의 서로 다른 필자가 같은 주간에 같은 수치를 각자의 논지로 재인용했다는 사실 자체가 "독자가 AI 글쓰기를 감지하는 것에 매우 민감하게 반응한다"는 정성적 신호로는 충분히 강하다.

## 같은 비대칭이 코드 리뷰에서도 이미 벌어지고 있다

이 글쓰기 검증 비용 문제는 낯설지 않다. [AI 코딩 에이전트 시대의 품질 청구서](/post/2026-09-01-ai-coding-agent-velocity-quality-tradeoff/)에서 다룬 Faros AI의 22,000명 텔레메트리 조사가 정확히 같은 구조를 코드에서 보여줬다 — AI 에이전트 덕분에 PR 생산량은 5배로 늘었지만, 그 코드를 사람이 검증하는 데 걸리는 시간은 4배로 늘었고 사고율은 3배 넘게 증가했다. 코드는 컴파일되고 테스트도 통과하니 "측정 가능한" 지표는 다 초록불이지만, 그 코드가 장기적으로 유지보수 가능한 설계인지, 숨은 논리적 결함은 없는지는 "측정하기 어려운" 영역에 남아 사람의 리뷰를 여전히 요구한다. Catalini의 표현을 빌리면, 테스트 통과율이라는 눈에 보이는 지표 위에서 위조 효용이 쌓이고 있었던 셈이다.

블로그 글쓰기와 코드 작성은 언뜻 다른 활동처럼 보이지만, 둘 다 "그럴듯해 보이는 산출물을 만드는 비용"과 "그 산출물이 실제로 맞는지 확인하는 비용" 사이의 간극이라는 같은 문제를 공유한다. 그리고 그 간극은 AI가 생성 속도를 올릴수록 좁혀지는 게 아니라 오히려 벌어진다 — 생성량이 늘어난 만큼 검증해야 할 대상도 함께 늘어나기 때문이다.

## 검증되지 않은 위조 효용은 결국 청구서로 돌아온다

Fowler는 같은 호에서 Sony Music Publishing과 Warner Chappell Music이 2026년 8월 말 Anthropic을 상대로 제기한 저작권 소송도 짧게 다룬다. 두 음악 퍼블리셔는 Anthropic이 Claude를 학습시키는 과정에서 "수만 건" 규모의 저작물을 라이브러리 제네시스 등 불법 경로로 취득해 사용했다고 주장하며, 곡당 최대 15만 달러의 법정 손해배상을 청구했다. Anthropic은 혐의를 부인하며 모델 학습이 저작권법상 변형적 공정 이용(fair use)에 해당한다고 맞서고 있어, 이 소송의 결론이 어느 쪽으로 날지는 아직 열려 있다.

이 소송을 이 글의 맥락에 놓고 보면, 학습 데이터의 출처가 적법한지는 그 자체로 Catalini가 말한 "측정하기 어려운" 영역에 가깝다 — 모델의 벤치마크 점수나 응답 품질은 쉽게 측정되지만, 그 모델을 만드는 데 쓰인 데이터 전체가 라이선스를 지켰는지는 사후에 소송을 통해서야 드러나는 경우가 많다. 검증되지 않은 채 쌓인 위조 효용이 몇 년 뒤 수십억 달러 규모의 소송이라는 청구서로 돌아올 수 있다는 걸 보여주는 사례다.

## 그래서 무엇을 확인해야 하는가

이 흐름에서 끌어낼 수 있는 실무 판단 기준은 세 가지로 정리된다.

1. **"측정 가능"과 "검증 완료"를 혼동하지 않는다.** 테스트 통과, 벤치마크 점수, PR 생산량처럼 자동으로 집계되는 지표가 좋아 보인다고 해서 그 이면의 목적(유지보수성, 사실관계, 저작권 준수)까지 검증됐다고 넘겨짚지 않는다. 지표가 측정하지 못하는 영역이 무엇인지 먼저 목록화하는 게 첫 단계다.
2. **생성량이 늘면 검증 예산도 함께 늘려야 한다.** Faros AI 사례처럼 리뷰 시간·리뷰어 수를 생산량 증가에 비례해 늘리지 않으면 그 격차만큼 결함이 검증되지 않은 채로 누적된다. 이는 코드뿐 아니라 문서·마케팅 카피 등 AI로 대량 생성하는 모든 산출물에 적용된다.
3. **독자·동료에게 AI 관여 사실을 숨기지 않는다.** Dunlop의 설문이 보여주듯, 사람들은 AI가 썼다는 사실 자체보다 그것을 숨기려 한 시도에 더 강하게 반응하는 경향이 있다. 이 글도 예외가 아니다 — 이 문단을 포함해 이 포스트 전체는 사람이 고른 주제를 Claude가 리서치하고 초안을 쓴 뒤 사람의 검토 없이 자동 게시되는 파이프라인의 결과물이다. 그 사실을 밝히는 것과, 본문에 인용한 모든 수치를 원 출처까지 추적해 검증하는 것이 이 격차를 조금이라도 좁히는 유일한 방법이라고 판단했다.

## 참고 자료

- Martin Fowler, "Fragments: September 8" (2026-09-08): <https://martinfowler.com/fragments/2026-09-08.html>
- Christian Catalini, Xiang Hui, Jane Wu, "Some Simple Economics of AGI" (arXiv:2602.20946): <https://arxiv.org/abs/2602.20946>
- Christian Catalini, "The Economics of AI: Verification as the New Scarcity": <https://catalini.com/ideas/economics-of-ai/>
- Bryan Cantrill, "The Revolt of the Reader" (2026-09-05): <https://bcantrill.dtrace.org/2026/09/05/the-revolt-of-the-reader/>
- Cynthia Dunlop, "Write That Blog" — 668명 개발자 설문 (2026-06-16): <https://writethatblog.substack.com/p/dev-reaction-to-ai-blog-posts>
- TechCrunch, "Sony Music, Warner sue Anthropic, alleging a 'brazen campaign' of intellectual property theft" (2026-08-29): <https://techcrunch.com/2026/08/29/sony-music-warner-sue-anthropic-alleging-a-brazen-campaign-of-intellectual-property-theft/>
- [AI 코딩 에이전트 시대의 품질 청구서](/post/2026-09-01-ai-coding-agent-velocity-quality-tradeoff/)
