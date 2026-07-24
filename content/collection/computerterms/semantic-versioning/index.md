---
image: "wordcloud.png"
slug: semantic-versioning
collection_order: 103
draft: false
title: "[Computer Terms] 시맨틱 버저닝 (Semantic Versioning, SemVer)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "MAJOR.MINOR.PATCH 형식은 하위 호환 깨짐·기능 추가·버그 수정을 숫자로 약속하는 신뢰의 계약입니다. 이 규칙을 어긴 배포가 실무에서 어떤 문제를 일으키는지, npm의 caret·tilde 범위 규칙과 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Version-Control(버전관리)
- Software-Engineering(소프트웨어공학)
- Deployment(배포)
- Best-Practices
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Comparison(비교)
- Deep-Dive
- Case-Study
- Collaboration(협업)
- Reliability(신뢰성)
- CI-CD(Continuous Integration/Continuous Deployment)
- Advanced
- JSON(JavaScript Object Notation)
- API-Design(API설계)
- Standard(표준)
- How-To
- Tips
---

## 이 장을 읽기 전에

[버전 관리의 내부 구조](/post/computerterms/version-control-internals/)에서 다룬 커밋·태그 개념과, 패키지 매니저(npm, pip 등)로 외부 라이브러리를 설치해 본 경험을 안다고 가정한다.

## 버전 번호는 왜 임의로 매기면 안 되는가

프로젝트가 라이브러리 하나에 의존하면, 그 라이브러리의 새 버전이 나올 때마다 "업데이트해도 내 코드가 안 깨질까"를 매번 고민해야 한다. 라이브러리 저자가 버전 번호를 "그냥 배포할 때마다 1씩 올리는 숫자"로 쓴다면, 이 질문에 답할 방법이 없다 — 버전만 봐서는 이번 업데이트가 사소한 버그 수정인지, 기존 코드를 깨뜨리는 큰 변경인지 알 수 없기 때문이다. **시맨틱 버저닝(Semantic Versioning, SemVer)**은 이 문제를 semver.org가 공개한 표준(Standard) 명세로 해결한다 — 버전 번호 자체에 의미를 부여해 — `MAJOR.MINOR.PATCH` 세 자리 숫자 각각에 정해진 규칙을 부여해, 버전 번호만 보고도 이번 변경이 안전한지 예측할 수 있게 만든다.

```text
1.4.2
│ │ └── PATCH: 하위 호환되는 버그 수정
│ └──── MINOR: 하위 호환되는 기능 추가
└────── MAJOR: 하위 호환을 깨는 변경
```

**MAJOR**는 기존 API를 사용하는 코드가 그대로는 동작하지 않을 수 있는 변경(함수 시그니처 변경, 동작 방식 자체가 달라짐)이 있을 때 올린다. **MINOR**는 기존 코드는 그대로 두고 새 기능만 추가했을 때 올린다 — 기존에 이 라이브러리를 쓰던 코드는 아무것도 바꾸지 않아도 계속 동작해야 한다. **PATCH**는 외부에서 보이는 동작(API)은 그대로 두고 내부 버그만 고쳤을 때 올린다. 셋 중 하나를 올리면 그 오른쪽 숫자는 0으로 초기화한다(예: MINOR를 올리면 `1.4.2` → `1.5.0`).

## 신뢰의 계약으로 작동하는 이유

한 프로젝트가 수십–수백 개의 패키지에 의존하는 것이 흔한 오늘날, 사람이 매 업데이트마다 changelog를 일일이 읽고 호환성을 확인하는 것은 현실적이지 않다. 그래서 npm, pip 같은 패키지 매니저는 `package.json`이나 `requirements.txt`에 **버전 범위**를 지정하고, SemVer 규칙을 신뢰해 자동으로 업데이트를 적용한다.

```json
{
  "dependencies": {
    "left-pad": "^1.4.2"
  }
}
```

`^1.4.2`는 "MAJOR 버전 1을 유지하는 한(즉 `1.x.x` 범위 내에서) 자동으로 최신 버전을 써도 좋다"는 뜻이다. 이 지정이 안전하려면 라이브러리 저자가 SemVer 규칙을 정확히 지킨다는 전제가 필요하다 — MINOR나 PATCH 업데이트에서 기존 API를 몰래 깨뜨리지 않는다는 약속이다. 이 약속이 지켜지는 한, 개발자는 매번 업데이트 내용을 검토하지 않고도 최신 버그 수정과 기능을 자동으로 받을 수 있다. 즉 SemVer는 기술 규격이기 이전에, 라이브러리 저자와 그것을 소비하는 수많은 프로젝트 사이의 **신뢰 계약**이다.

## 계약을 어긴 배포가 일으키는 문제

이 신뢰가 깨지는 가장 흔한 실무 사고는 **하위 호환성을 깨는 변경을 MINOR나 PATCH로 배포하는 경우**다. 저자 입장에서는 "작은 개선"이라고 생각한 변경(기본값 변경, 에러 메시지 형식 변경, 내부적으로만 쓰던 함수 제거)이 실제로는 누군가의 코드를 깨뜨릴 수 있다. `^1.4.2`로 의존하던 수많은 프로젝트는 이 변경을 MAJOR 업데이트로 인식하지 못하기 때문에 자동으로 새 버전을 받아버리고, 아무것도 바꾸지 않은 자신의 코드가 갑자기 빌드나 런타임에서 깨지는 것을 목격하게 된다. 이런 사고가 반복되면 팀은 결국 버전 범위를 `^1.4.2` 대신 `1.4.2`(정확히 고정)로 바꾸게 되는데, 이는 SemVer가 약속하는 "안전한 자동 업데이트"라는 이점 자체를 포기하는 것이다.

| 상황 | 올바른 버전 증가 | 어긴 경우 실무 영향 |
|------|------------------|----------------------|
| 버그만 수정, API 동일 | PATCH | 정상 — 자동 업데이트 안전 |
| 새 함수 추가, 기존 함수 그대로 | MINOR | 정상 — 자동 업데이트 안전 |
| 기존 함수의 기본 동작 변경 | MAJOR | MINOR로 배포 시 `^`로 의존한 프로젝트가 예고 없이 깨짐 |
| 지원 중단(Deprecated) 함수 제거 | MAJOR | PATCH로 배포 시 빌드 자체가 실패할 수 있음 |

## 흔한 오개념

**"1.0.0 이전(0.x.x)에도 같은 규칙이 적용된다"** — SemVer 명세는 `0.y.z`를 초기 개발 단계로 규정하며, 이 구간에서는 API가 언제든 바뀔 수 있다고 명시한다. 즉 `0.1.0`에서 `0.2.0`으로 올라갈 때도 MAJOR 수준의 파괴적 변경이 있을 수 있다 — MINOR 자리가 올라가도 하위 호환을 보장하지 않는다. 이 때문에 `0.x` 버전의 패키지를 프로덕션에 의존할 때는 `^0.1.0` 같은 범위 지정을 더 보수적으로 다뤄야 한다.

**"버전 번호가 크면 더 성숙하거나 안정적인 소프트웨어다"** — MAJOR 번호는 하위 호환을 깨는 변경이 몇 번 있었는지를 셀 뿐, 소프트웨어의 성숙도나 품질과는 무관하다. 어떤 프로젝트는 API를 신중하게 설계해 수년간 `1.x.x`에 머무르고, 어떤 프로젝트는 초기 설계를 자주 뒤엎어 `9.x.x`에 도달한다. 버전 숫자의 크기가 아니라 MAJOR가 오른 **횟수와 이유**를 changelog로 확인하는 것이 더 신뢰할 수 있는 판단 기준이다.

## 다른 개념과의 연결

시맨틱 버저닝은 [버전 관리의 내부 구조](/post/computerterms/version-control-internals/)에서 다룬 Git 태그로 릴리스 시점을 표시하는 관행과 자연스럽게 맞물리고(예: `v1.4.2` 태그), [CI/CD와 테스트 유형](/post/computerterms/ci-cd-and-testing-types/)의 자동 배포 파이프라인은 흔히 커밋 메시지나 PR 라벨을 분석해 다음 버전 번호(MAJOR/MINOR/PATCH)를 자동으로 결정하는 도구(semantic-release 등)와 결합해 쓰인다. 다음 챕터에서는 코드는 이미 배포됐지만 사용자에게 노출하는 시점을 별도로 제어하는 피처 플래그를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. `MAJOR.MINOR.PATCH` 각 자리가 어떤 종류의 변경을 의미하는지 구분해 설명할 수 있다. 패키지 매니저의 버전 범위 지정(`^1.4.2` 등)이 왜 SemVer 준수를 전제로 하는 신뢰 계약인지 설명할 수 있다. 하위 호환을 깨는 변경이 MINOR나 PATCH로 잘못 배포됐을 때 의존 프로젝트에 어떤 문제가 생기는지, 그리고 `0.x.x` 버전대의 예외 규칙을 설명할 수 있다.

## 참고 자료

> Preston-Werner, T. (2013). "Semantic Versioning 2.0.0". semver.org.

- [Semantic Versioning 2.0.0 (공식 명세)](https://semver.org/) — SemVer 규칙 원문, MAJOR/MINOR/PATCH와 0.x.x 예외 조항 포함
- [npm Docs: About semantic versioning](https://docs.npmjs.com/about-semantic-versioning) — npm이 버전 범위(`^`, `~`)를 실제로 해석하는 방식
