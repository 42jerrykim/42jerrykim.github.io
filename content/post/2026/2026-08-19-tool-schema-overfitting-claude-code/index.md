---
title: "[Claude Code] 도구 스키마 과적합: 최신 모델이 서드파티 도구에 약한 이유"
description: "Armin Ronacher가 CLI 에이전트 Pi에서 발견한 현상 — Claude Opus 4.8·Sonnet 5가 구형 모델보다 서드파티 도구 스키마에서 더 자주 실패하는 이유와, Claude Code 특화 학습의 대가, Anthropic의 공식 해법인 Strict Tool Use를 정리했다."
date: 2026-08-19T09:00:00+09:00
lastmod: 2026-08-19
draft: false
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Prompt-Engineering(프롬프트엔지니어링)
  - Fine-Tuning(파인튜닝)
  - Reinforcement-Learning(강화학습)
  - Automation(자동화)
  - Open-Source(오픈소스)
  - Case-Study
  - Deep-Dive
  - Comparison(비교)
  - Software-Architecture(소프트웨어아키텍처)
  - Best-Practices
  - Guide(가이드)
  - Troubleshooting(트러블슈팅)
  - Workflow(워크플로우)
  - Productivity(생산성)
  - Claude-Code
  - Claude
  - Anthropic
  - Tool-Use
  - Agentic-Coding
  - AI-Agent
  - Post-Training
  - Vendor-Lock-in
  - Grammar-Constrained-Decoding
  - Schema-Design
  - Third-Party-Tools
  - Simon-Willison
  - Armin-Ronacher
image: "wordcloud.png"
---

더 좋은 모델을 붙였는데 결과가 더 나빠졌다면, 보통은 프롬프트나 설정을 의심한다. 그런데 2026년 7월, 오픈소스 CLI 코딩 에이전트 Pi를 만든 Armin Ronacher는 정반대의 원인을 발견했다. 모델 자체가 최신으로 갈수록 자신이 정의한 도구 호출 스키마를 더 못 지켰던 것이다. 그는 이 현상을 블로그 글 [Better Models: Worse Tools](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/)에 정리했고, 같은 날 Simon Willison이 자신의 위클로그에서 이를 인용하며 더 넓은 논의로 번졌다. 이 글은 그 관찰이 왜 일어나는지, 그리고 지금(2026년 8월) 시점에 Anthropic이 내놓은 공식 해법이 무엇인지를 정리한다.

## 무슨 일이 있었나

Ronacher가 만든 Pi는 파일을 고칠 때 아래와 같은 중첩 배열 스키마를 도구 호출 파라미터로 기대한다.

```json
{
  "path": "some/file.py",
  "edits": [
    { "oldText": "text to replace", "newText": "replacement text" }
  ]
}
```

그런데 Claude Opus 4.8과 Claude Sonnet 5는 `oldText`·`newText` 값 자체는 정확히 채우면서도, 스키마에 없는 필드를 함께 만들어 넣었다. Ronacher가 실제로 관찰해 나열한 필드만 해도 `type`, `id`, `kind`, `unique`, `requireUnique`, `matchCase`, `in_file`, `forceMatchCount`, `children`, `notes`, `cost`, `oldText2`/`newText2`, `oldText_2`/`newText_2`, 심지어 `event.0.additionalProperties`처럼 그 자체로 스키마 문법을 흉내 낸 키까지 포함되어 있었다. Pi는 알 수 없는 필드가 섞인 호출을 거부하고 재시도를 요청하도록 만들어져 있었으므로, 모델은 값은 맞게 채워놓고도 형식 때문에 매번 한 번씩 더 왕복해야 했다. 더 이전 세대 모델에서는 이런 증상이 나타나지 않았다는 점이 이를 "성능 향상에 따라오는 부작용"이 아니라 **역행(regression)** 으로 보게 만든 근거였다.

## 왜 이런 일이 생기는가

원인은 무작위 노이즈가 아니라 특정 방향으로의 편향이라는 데 있다. Anthropic은 Claude Code 자체의 도구 호출 성공률을 높이기 위해 최신 모델을 Claude Code의 편집 도구 스키마(또는 그와 매우 유사한 학습 환경)에 맞춰 강화학습한 것으로 추정된다. 실제로 Claude Code의 표준 편집 도구는 Pi처럼 중첩된 `edits[]` 배열이 아니라, `file_path`·`old_string`·`new_string`과 선택적 플래그 `replace_all`로 이루어진 훨씬 평평한(flat) 구조를 쓴다. 게다가 Claude Code는 `old_str`처럼 구버전 파라미터명이나 `path`처럼 `file_path`의 별칭까지 받아주는 관대한 파서를 내장하고 있어서, 모델이 약간 다른 필드명을 만들어내도 문제없이 넘어간다. 이 조합이 학습 과정에서 "편집 도구 호출은 대략 이런 모양이고, 필드가 좀 달라도 받아준다"는 강한 사전 지식(prior)을 모델에 심어 놓았고, 그 prior가 Claude Code 바깥의 하네스에서는 정반대로 작동한 것이다.

| 항목 | Claude Code 표준 편집 도구 | Pi의 편집 도구 |
|------|---------------------------|----------------|
| 구조 | 평평한 필드 (`file_path`, `old_string`, `new_string`, `replace_all`) | 중첩 배열 (`path`, `edits[]` 안에 `oldText`/`newText`) |
| 미지 필드 처리 | 별칭·타입 강제변환으로 관대하게 흡수 | 스키마 밖 필드가 섞이면 호출 자체를 거부 |
| 최신 모델의 경향 | 학습 환경과 일치 → 실패 적음 | prior와 불일치 → 허구 필드 생성 후 재시도 유발 |

## 시도된 대안과 왜 충분하지 않았는가

Ronacher가 검토했거나 실제로 적용해 본 완화책은 두 갈래였는데, 둘 다 증상을 줄일 뿐 원인을 없애지는 못했다.

| 대안 | 아이디어 | 한계 |
|------|----------|------|
| 하네스가 관대하게 파싱 | 알 수 없는 필드는 무시하고 넘어감 | Claude Code 자체가 이미 별칭·타입 강제변환·조용한 키 필터링으로 관대하게 대응 중이라는 점에서, 이는 증상을 감추는 것이지 모델의 prior 자체를 고치지 않는다 |
| 프롬프트로 스키마를 더 명확히 제시 | 시스템 프롬프트에 정확한 필드 목록을 강조 | 근본 원인이 post-training으로 굳어진 prior이므로, 프롬프트만으로는 간헐적으로 계속 재발한다 |

Ronacher가 실제로 효과를 본 것은 이 둘이 아니라 Anthropic API의 **strict 도구 호출 모드**였다. 그는 strict 모드를 켜면 문제가 사라지는 것을 관찰하고, 서버 쪽에서 JSON 스키마 구조가 허용하지 않는 키 자체를 샘플링하지 못하게 막고 있을 것이라고 추정했다.

## Anthropic의 공식 해법: Strict Tool Use

Ronacher가 추정만 했던 메커니즘은 이제 [Anthropic 공식 문서](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)에 **Structured Outputs**라는 이름의 정식 기능으로 문서화되어 있다. 도구 정의에 `strict: true`를 추가하면, 도구 이름 일치·필수 필드 포함·미지 필드 차단·타입 검증까지 네 가지를 모델이 아예 어길 수 없는 방식으로 보장한다. 이는 "제발 스키마를 지켜서 JSON을 만들어 달라"고 프롬프트로 부탁하는 것과는 층위가 다르다. Anthropic은 JSON 스키마를 문법(grammar)으로 컴파일해 추론 단계에서 토큰 생성 자체를 그 문법 안으로 제약한다 — 스키마를 위반하는 토큰은 모델이 물리적으로 뽑을 수 없게 만드는 방식이다(**grammar-constrained sampling**). 스키마 쪽에는 조건이 있는데, `additionalProperties`를 반드시 `false`로, `required` 배열을 명시해야 하며, 이를 지키지 않으면 요청 자체가 400 에러로 거부된다. Ronacher가 겪었던 "값은 맞는데 필드가 넘친다"는 증상은 정확히 `additionalProperties: false` 제약이 막는 종류의 문제다.

2026년 8월 기준 Strict Tool Use는 Claude Opus 5·Sonnet 5·Haiku 4.5를 포함한 최신 모델군과 Claude API·Amazon Bedrock·Google Cloud·Microsoft Foundry에서 지원되며, 헤더 방식의 구 베타(`structured-outputs-2025-11-13`)에서 `output_config` 파라미터 방식으로 넘어가는 과도기에 있다(구 방식도 당분간 계속 동작한다). 즉 7월에 Ronacher가 "우연히 효과가 있었다"고 관찰했던 대응책이, 한 달여 만에 정식 문서를 갖춘 안정적인 API 옵션으로 자리 잡은 셈이다.

## 더 큰 함의: 벤더 락인은 가중치 밖에서도 생긴다

이 사례가 흥미로운 지점은 단순한 버그 리포트를 넘어선다는 데 있다. 모델 제공사가 자사 공식 하네스(Claude Code)의 사용성을 극대화하는 방향으로 모델을 특화 학습시킬수록, 그 모델을 가져다 쓰는 서드파티 에이전트 생태계는 구조적으로 "우리 하네스에 맞는 도구 스키마 변형을 따로 구현해야 하는가"라는 선택에 몰린다. Anthropic 입장에서 Claude Code 자체의 도구 호출 성공률은 post-training의 최우선 순위이고, 서드파티 하네스와의 호환성은 그다음이다. 반대로 Pi 같은 서드파티는 Anthropic의 학습 데이터·환경을 통제할 수 없으므로 원인이 아니라 증상에만 대응할 수 있다. Willison이 지적했듯, 결국 남는 질문은 "Pi 같은 도구들이 모델마다 최적화된 여러 개의 편집 도구 변형을 구현해야 하는가"이다. 벤더 락인이 모델 가중치 자체가 아니라 **도구 호출 관례(convention)** 층위에서도 발생할 수 있다는 뜻이다.

## 판단 기준: 언제 신경 써야 하는가

- Claude Code만 쓰고 자체 하네스를 만들 계획이 없다면, 이 문제는 사실상 남의 일이다. 표준 편집 도구 자체가 이미 학습 환경과 일치한다.
- Pi처럼 **자체 도구 스키마를 직접 정의하는** 서드파티 코딩 에이전트를 만들거나, 여러 모델 제공사의 API를 한 하네스로 스위칭해 쓰고 있다면, 도구 스키마를 설계할 때 `strict: true`(또는 각 제공사의 동등 기능)를 기본값으로 켜 두는 편이 낫다. 관대한 파싱으로 증상만 감추면 모델 세대가 바뀔 때마다 같은 문제가 다른 필드 이름으로 재발한다. (참고로 [cmux](https://github.com/manaflow-ai/cmux)처럼 Claude Code·Codex 등 기존 에이전트를 그대로 실행만 하는 터미널 래퍼는 자체 편집 도구 스키마가 없으므로 이 문제와 무관하다.)
- 자체 하네스의 도구 스키마가 이미 Claude Code처럼 평평한 구조(예측 가능한 소수의 최상위 필드)라면, 애초에 최신 모델의 prior와 충돌할 여지가 적다. 중첩 배열·다중 선택적 필드처럼 구조가 복잡할수록 이 현상에 더 취약하다.

## 한계와 남은 트레이드오프

Strict Tool Use가 "허구 필드가 섞여 들어오는" 증상은 없애지만, 모델이 애초에 그 스키마가 요구하는 의미(semantic)를 잘못 이해해서 틀린 값을 정확한 형식으로 채워 넣는 문제까지 막아주지는 않는다. 스키마 자체를 문법으로 강제하는 것과, 모델이 그 문법 안에서 올바른 내용을 채우는 것은 별개의 보장이다. 또한 이 기능은 현재 Anthropic 최신 모델·특정 플랫폼 조합에 한정되므로, 여러 모델 제공사를 동시에 지원해야 하는 하네스라면 제공사마다 다른 강제 방식(OpenAI의 Structured Outputs, 오픈소스 문법 제약 디코딩 라이브러리 등)을 각각 통합해야 하는 부담은 여전히 남는다.

## 평가 기준: 이 글로 무엇을 판단할 수 있어야 하는가

- 서드파티 하네스를 직접 만들 때 `strict: true`(또는 제공사별 동등 기능)를 켜야 하는 조건과, 켜지 않아도 되는 조건(Claude Code처럼 이미 학습 환경과 스키마가 일치하는 경우)을 구분해서 설명할 수 있다.
- `additionalProperties: false`와 `required` 배열이 왜 strict 모드의 필수 조건인지, 그리고 이것이 왜 "값은 맞는데 필드가 넘치는" 증상을 원천 차단하는지 설명할 수 있다.
- 이 현상이 모델의 무작위 오류가 아니라 Claude Code 특화 post-training이 만든 prior 때문이라는 인과관계를, "시도된 대안이 왜 증상만 가리고 원인을 없애지 못했는가"와 함께 설명할 수 있다.
- 벤더 락인이 모델 가중치뿐 아니라 도구 호출 관례(스키마 형태) 층위에서도 발생할 수 있다는 것이 자신이 다루는 하네스·워크플로에 어떤 의미인지 판단할 수 있다.

## 참고 자료

- [Armin Ronacher, "Better Models: Worse Tools" (2026-07-04)](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/)
- [Simon Willison, "Better Models: Worse Tools" 인용·논평 (2026-07-04)](https://simonwillison.net/2026/Jul/4/better-models-worse-tools/)
- [Anthropic, "Structured outputs" 공식 문서](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
