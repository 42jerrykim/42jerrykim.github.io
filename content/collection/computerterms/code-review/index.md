---
image: "wordcloud.png"
slug: code-review
collection_order: 102
draft: false
title: "[Computer Terms] 코드 리뷰 (Code Review)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "코드 리뷰는 병합 전 마지막 검토 관문으로, 버그뿐 아니라 결합도·응집도 같은 설계 문제를 잡아낸다. 병목이 되지 않으려면 작은 단위로 자주 올려야 하는 이유와, PR을 언제 쪼개야 하는지 구체적인 판단 기준까지 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Code-Review(코드리뷰)
- Version-Control(버전관리)
- Software-Engineering(소프트웨어공학)
- Code-Quality(코드품질)
- Collaboration(협업)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Refactoring(리팩토링)
- Advanced
- Workflow(워크플로우)
- Maintainability(유지보수성)
- Readability
- Automation(자동화)
- Async(비동기)
- Reliability(신뢰성)
---

## 이 장을 읽기 전에

[버전 관리의 내부 구조](/post/computerterms/version-control-internals/)에서 다룬 브랜치·머지 개념과, [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)·[리팩토링과 코드 스멜](/post/computerterms/refactoring-and-code-smells/)에서 다룬 설계 품질 개념을 안다고 가정한다.

## 왜 머지 직전에 사람이 한 번 더 봐야 하는가

[버전 관리의 내부 구조](/post/computerterms/version-control-internals/)에서 다룬 것처럼 브랜치는 커밋을 가리키는 가벼운 포인터이므로, 기술적으로는 누구나 자기 브랜치를 곧바로 main에 머지할 수 있다. 그런데 대부분의 팀은 그 사이에 **풀 리퀘스트(Pull Request, PR)**라는 검토 단계를 끼워 넣는다. 이유는 단순하다 — 작성자 본인은 자기 코드의 문제를 발견하기 어렵다. 며칠 동안 한 가지 문제에만 몰두하면 "이 함수가 왜 이렇게 복잡해졌는지"를 당연하게 받아들이게 되고, 처음 코드를 보는 사람만 알아챌 수 있는 관점을 잃는다. **코드 리뷰(Code Review)**는 병합 전에 다른 사람의 눈으로 변경 사항을 한 번 더 검증하는 절차이며, PR은 그 검증이 이루어지는 장소다.

```mermaid
sequenceDiagram
    participant A as "작성자"
    participant P as "PR (워크플로)"
    participant R as "리뷰어"

    A->>P: "feature 브랜치에서 작업 후 PR을 연다"
    P->>R: "diff 알림"
    R->>P: "코멘트 남김 (버그, 설계, 스타일)"
    P->>A: "코멘트 알림"
    A->>P: "코멘트에 대응해 커밋 추가"
    R->>P: "승인(Approve)"
    P->>P: "main으로 머지"
```

이 워크플로는 리뷰어와 작성자가 서로 다른 시간대·일정에 있어도 문제없이 동작한다는 점에서 본질적으로 **비동기(Async)** 협업 방식이다 — 화상 회의처럼 두 사람이 동시에 시간을 맞출 필요 없이, 각자 여유가 될 때 diff를 읽고 코멘트를 남기면 된다. 많은 팀은 이 흐름의 일부(린터 검사, 테스트 실행, 코드 포맷팅 확인)를 자동화(Automation)해 CI가 먼저 처리하게 하고, 사람 리뷰어는 자동화가 다루기 어려운 설계 판단에만 집중하도록 한다.

## 리뷰가 잡아내는 문제의 종류

코드 리뷰를 "오탈자나 버그를 찾는 절차"로만 이해하면 절반만 이해한 것이다. 리뷰가 실제로 걸러내는 문제는 크게 세 층위로 나뉜다. 첫째는 **동작 오류**다 — 널 체크 누락, 경계 조건 실수, 테스트가 놓친 예외 상황처럼 코드를 실행하기 전에는 드러나지 않는 결함을 사람의 눈으로 먼저 잡는다. 둘째는 **설계 문제**다 — [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬, 한 모듈이 지나치게 많은 다른 모듈을 알아야 동작하는 구조나, 서로 관련 없는 책임이 한 클래스에 뒤섞인 구조는 코드가 "일단 동작"하기 때문에 테스트를 통과하고도 남아 있을 수 있다. 이런 문제는 자동화된 테스트로는 걸러지지 않고, 오직 사람이 diff를 읽으며 "이 함수가 왜 이 모듈의 내부 사정까지 알아야 하지"라고 질문할 때만 드러난다. 셋째는 **코드 스멜**이다 — [리팩토링과 코드 스멜](/post/computerterms/refactoring-and-code-smells/)에서 다룬 긴 메서드, 중복 로직, 데이터 뭉치 같은 징후를 리뷰어가 지적하면, 문제가 아직 작을 때 리팩토링할 기회가 생긴다.

```text
# 리뷰 코멘트 예시 (동작 오류 vs 설계 문제)

# 동작 오류
"이 배열이 비어 있으면 items[0]에서 예외가 발생합니다"

# 설계 문제
"이 PaymentService가 UserRepository와 EmailSender를 동시에
직접 호출하고 있습니다 — 책임을 분리하는 게 어떨까요?"
```

두 코멘트는 성격이 다르다. 앞의 것은 정적 분석 도구나 테스트가 나중에라도 잡아낼 수 있는 문제지만, 뒤의 것은 코드가 "지금 당장은" 잘 동작하기 때문에 도구로는 걸러지지 않는다. 설계 문제를 걸러내는 능력이야말로 코드 리뷰가 자동화된 검사와 구별되는 지점이다.

## 리뷰가 병목이 되는 이유와 작은 단위의 원칙

리뷰는 공짜가 아니다 — 리뷰어의 시간과 집중력을 쓰는 작업이고, PR이 열려서 승인되기까지의 시간(Cycle Time)만큼 병합이 늦어진다. 여기서 흔한 실패 패턴이 나온다. 한 PR에 수백–수천 줄이 몰리면, 리뷰어는 변경 전체를 이해할 인지적 여력이 없어 표면적인 스타일 문제만 짚거나, 반대로 지쳐서 대충 승인(Rubber-stamp)해 버린다. 두 경우 모두 리뷰의 본래 목적인 설계 검증이 실질적으로 작동하지 않는다.

이 문제를 완화하는 원칙이 **작은 단위로 자주 올리기**다. 하나의 논리적 변경(기능 하나, 버그 수정 하나)을 수백 줄 이하로 쪼개 PR을 자주 열면, 리뷰어가 diff 전체를 실제로 읽고 맥락을 유지한 채 판단할 수 있다. 이는 [CI/CD와 테스트 유형](/post/computerterms/ci-cd-and-testing-types/)에서 다룬 "자주, 작게 통합해 문제를 일찍 발견한다"는 지속적 통합의 원칙을 리뷰 단계에도 그대로 적용한 것이다 — 통합이 커밋 단위로 자주 일어나야 충돌이 작듯, 리뷰도 변경 단위가 작아야 검토가 실질적이다.

| 구분 | 작은 PR | 큰 PR |
|------|---------|-------|
| 리뷰어 이해도 | diff 전체를 실제로 읽음 | 표면만 훑고 넘어가기 쉬움 |
| 리뷰 대기 시간 | 짧음 (빠른 판단 가능) | 김 (부담이 커 미루기 쉬움) |
| 설계 문제 발견율 | 높음 (맥락 유지) | 낮음 (인지 부하로 놓침) |
| 충돌 가능성 | 낮음 | 높음 (오래 열려 있을수록 다른 변경과 충돌) |

## 언제 PR을 쪼개야 하는가

절대적인 줄 수 기준은 없지만, 실무에서 흔히 참고하는 신호는 두 가지다. 첫째, 변경이 **하나의 논리적 목적**을 벗어나는가다 — "버그 수정 + 리팩토링 + 새 기능"이 한 PR에 섞여 있다면, 그 각각을 별도 PR로 쪼개는 것이 원칙이다. 리뷰어가 "이 줄이 버그 수정 때문인지 리팩토링 때문인지" 구분해야 한다면 이미 PR이 너무 크다는 신호다. 둘째, **리뷰어가 diff를 한 번에 다 읽고 맥락을 유지할 수 있는가**다 — 정확한 줄 수는 팀·도메인마다 다르지만, 일부 팀은 수백 줄 안팎을 경험적 상한으로 삼아 그 이상이면 PR을 쪼개도록 관행을 정해 둔다. 자동 생성된 코드(락파일, 마이그레이션 스크립트)처럼 사람이 실제로 읽을 필요가 없는 변경은 이 기준에서 제외하고 판단한다. 이 두 신호 중 하나라도 걸리면, 커밋을 논리적 단위로 나눠 별도 PR로 순차 제출하는 편이 리뷰의 가독성(Readability)과 코드베이스의 유지보수성(Maintainability)을 함께 지킨다.

## 흔한 오개념

**"리뷰는 버그를 찾는 절차다"** — 버그 발견은 코드 리뷰의 부수 효과 중 하나일 뿐이다. 정적 분석 도구·타입 체커·테스트가 이미 상당수의 동작 오류를 걸러낼 수 있다. 사람이 개입해야만 발견되는 것은 오히려 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/) 위반이나 [리팩토링과 코드 스멜](/post/computerterms/refactoring-and-code-smells/)에서 다룬 설계 냄새처럼, "지금은 동작하지만 나중에 변경하기 어려워지는" 문제다. 이런 문제를 놓치는 팀은 리뷰를 자동 린터의 대체물 정도로만 쓰고 있을 가능성이 크다.

**"승인 수를 늘리면 품질이 올라간다"** — 리뷰어를 3명, 5명으로 늘려도 각자가 대충 훑고 넘어가면 품질은 오르지 않는다. 오히려 "누군가는 자세히 보겠지"라는 책임 분산 심리(Bystander Effect와 유사한 현상)로 아무도 꼼꼼히 보지 않는 역설이 생길 수 있다. 리뷰 품질은 리뷰어 수가 아니라 PR 크기와 리뷰어가 그 도메인을 실제로 이해하는지에 달려 있다 — 결국 시스템의 신뢰성(Reliability)은 승인 절차의 형식적 개수가 아니라 리뷰가 실제로 문제를 걸러내는지에 좌우된다.

## 다른 개념과의 연결

코드 리뷰는 [버전 관리의 내부 구조](/post/computerterms/version-control-internals/)의 브랜치·머지 흐름 위에서 동작하는 인간 검증 단계이고, [CI/CD와 테스트 유형](/post/computerterms/ci-cd-and-testing-types/)의 자동화된 테스트와 상호 보완 관계에 있다 — 테스트가 "동작이 맞는가"를 자동으로 확인한다면, 리뷰는 "이 설계가 앞으로도 유지보수 가능한가"를 사람이 판단한다. 리뷰가 지적한 [결합도와 응집도](/post/computerterms/coupling-and-cohesion/) 문제나 [리팩토링과 코드 스멜](/post/computerterms/refactoring-and-code-smells/)의 처방을 실제로 적용하는 것이 다음 커밋의 몫이 된다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 코드 리뷰가 자동화된 테스트·정적 분석과 어떻게 역할이 다른지 설명할 수 있다. 리뷰가 잡아내는 문제를 동작 오류와 설계 문제(결합도·응집도, 코드 스멜)로 구분해 예를 들 수 있다. PR 크기가 리뷰 품질에 미치는 영향을 설명하고, 작은 단위로 자주 올려야 하는 이유를 CI/CD의 지속적 통합 원칙과 연결해 설명할 수 있다.

## 참고 자료

> Google Engineering Practices Documentation. "What to look for in a code review". google.github.io.

- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) — 구글 엔지니어링 팀이 공개한 리뷰어 가이드라인, 설계 문제 우선순위를 명시
- [GitHub Docs: About Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) — PR 워크플로의 공식 문서
