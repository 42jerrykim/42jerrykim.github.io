---
draft: false
collection_order: 40
slug: gitattributes-file-path-specific-behavior
title: "[Git] 40. .gitattributes"
date: 2026-09-04
lastmod: 2026-09-04
description: ".gitattributes가 파일 경로별로 Git의 동작(줄바꿈 정규화, diff 방식, 언어 통계 제외)을 세밀하게 지정하는 원리, 02장에서 다룬 core.autocrlf보다 이 파일이 우선되는 이유, linguist-generated로 자동 생성 코드를 리뷰에서 제외하는 법을 정리한 Git 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- Terminal
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- Workflow(워크플로우)
- DevOps
- Configuration(설정)
- File-System(파일시스템)
- Advanced
- Collaboration(협업)
- Cross-Platform
- Open-Source(오픈소스)
- Career(커리어)
image: "wordcloud.png"
---

02장에서 `core.autocrlf` 설정으로 줄바꿈 문자를 통일하는 법을 다뤘지만, 그 설정은 사용자별로 다르게 적용될 수 있어 팀 전체에 일관되게 강제하기 어렵다. `.gitattributes`는 이런 파일 경로별 동작을, 사용자 설정과 무관하게 저장소 자체에 고정해두는 파일이다.

## 개요

`.gitattributes`는 `.gitignore`(10장)와 비슷한 위치(저장소 루트 또는 하위 디렉터리)에 두는 텍스트 파일로, 각 줄에 파일 패턴과 그 파일에 적용할 속성(attribute)을 적는다.

```gitattributes
* text=auto
*.png binary
*.sh text eol=lf
*.bat text eol=crlf
docs/generated/* linguist-generated=true
```

`.gitignore`가 "이 파일을 추적할지 말지"를 결정한다면, `.gitattributes`는 "이미 추적하는 이 파일을 Git이 어떻게 다룰지"를 결정한다는 점이 근본적인 차이다.

## 기본 개념

가장 흔한 용도는 줄바꿈 정규화다. `text=auto`는 Git이 텍스트 파일로 판단되는 내용을 저장소에는 항상 LF로 저장하고, 체크아웃할 때만 운영체제 관례(Windows는 CRLF, macOS·Linux는 LF)로 변환하도록 지정한다. 이 설정은 02장의 `core.autocrlf`와 목적이 같지만, <strong>저장소에 커밋되어 모든 사용자에게 동일하게 적용된다</strong>는 점에서 사용자 개인 설정보다 우선한다. 팀에 새로 합류한 사람이 `core.autocrlf`를 설정하지 않았더라도, 저장소의 `.gitattributes`가 있다면 일관된 동작이 보장된다.

## 종류/세부

### 자주 쓰는 속성

| 속성 | 의미 |
|---|---|
| `text` / `-text` | 텍스트 파일로 취급(줄바꿈 정규화 대상) / 취급하지 않음 |
| `binary` | `-text -diff`의 축약형, 바이너리 파일로 취급(07장에서 다룬 diff 대상에서 제외) |
| `eol=lf` / `eol=crlf` | 체크아웃 시 항상 특정 줄바꿈 문자 강제(운영체제 무관하게 고정) |
| `diff=<드라이버>` | 특정 파일 형식에 맞는 커스텀 diff 도구 사용(예: 이미지 메타데이터 비교) |
| `linguist-generated=true` | GitHub의 언어 통계·diff 표시에서 자동 생성 파일 제외 |
| `export-ignore` | `git archive`로 배포판을 만들 때 해당 파일 제외 |

셸 스크립트(`.sh`)는 Unix 계열 도구가 실행하므로 항상 LF가 필요하고, 배치 파일(`.bat`)은 Windows에서 CRLF가 필요한 경우처럼, 파일 형식에 따라 줄바꿈이 <strong>운영체제가 아니라 그 파일의 용도</strong>로 결정돼야 하는 경우 `eol` 속성이 `core.autocrlf`보다 정확하다.

### 대용량 자동 생성 코드 제외하기

빌드 과정에서 자동 생성되는 코드(예: GraphQL 스키마에서 생성된 타입 정의)가 저장소에 커밋된다면, 이 코드가 Pull Request(21장)의 diff나 GitHub의 저장소 언어 통계에 노이즈로 잡히는 것을 막을 수 있다.

```gitattributes
src/generated/**/*.ts linguist-generated=true
```

이 설정은 GitHub 웹 UI가 해당 파일을 diff에서 기본적으로 접어서 보여주거나, 저장소가 실제로 어떤 언어로 작성됐는지 보여주는 통계에서 제외하는 데 쓰인다.

### 병합 전략 지정

특정 파일에 대해 13장에서 다룬 병합 방식과 다른 전략을 지정할 수도 있다. 예를 들어 자동 생성되는 잠금 파일(lock file)처럼 항상 한쪽 값을 그대로 유지하고 싶은 파일에는 `merge=ours` 같은 커스텀 병합 드라이버를 연결할 수 있다(드라이버 자체는 `.gitconfig`에 별도로 정의해야 한다).

## 주의사항·함정

**이미 저장소에 잘못된 줄바꿈으로 커밋된 파일은 `.gitattributes` 추가만으로 즉시 바뀌지 않는다**: 10장의 `.gitignore`와 비슷하게, 이 설정은 이후의 체크아웃·커밋 동작에만 적용된다. 이미 커밋된 파일의 줄바꿈을 일괄 정규화하려면 `git add --renormalize .` 명령으로 기존 파일들을 다시 스테이징해야 한다.

```bash
git add --renormalize .
git commit -m "gitattributes 규칙에 맞춰 줄바꿈 정규화"
```

**바이너리 파일을 텍스트로 잘못 취급하면 파일이 손상될 수 있다**: 이미지·압축 파일처럼 실제로는 바이너리인 파일에 실수로 `text` 속성이 적용되면, 체크아웃 과정의 줄바꿈 변환이 파일 내용을 깨뜨릴 수 있다. 확장자 기반 규칙을 작성할 때 대상 파일 형식이 실제로 텍스트인지 다시 확인하는 편이 안전하다.

**`.gitattributes`와 `.gitignore`를 혼동하기 쉽다**: 두 파일은 문법이 비슷하고 같은 위치에 두지만 목적이 다르다. 무시할 파일을 지정하려면 `.gitignore`(10장), 추적 중인 파일의 처리 방식을 지정하려면 `.gitattributes`라는 구분을 명확히 해야 한다.

## Reference

- [gitattributes Documentation](https://git-scm.com/docs/gitattributes)
