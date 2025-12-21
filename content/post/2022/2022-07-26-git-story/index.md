---
image: "tmp_wordcloud.png"
description: "git-story는 Git 저장소의 커밋 히스토리를 바탕으로 애니메이션 비디오(.mp4)를 자동 생성하여 프로젝트 흐름을 쉽게 시각화하고, 팀원들과 개발 과정을 효과적으로 공유할 수 있도록 도와주는 무료 오픈소스 도구입니다."
date: "2022-07-26T00:00:00Z"
header:
  teaser: /assets/images/undefined/git-story.png
tag:
- Git
- git-story
- Commit
- History
- Animation
- 애니메이션
- 히스토리
title: '[Git] git-story - 커밋 히스토리를 애니메이션으로 만들어 설명하기'
---

Git 프로젝트의 커밋 히스토리를 기반으로 비디오 애미메이션(.mp4)를 생성하여 Git 프로젝트를 설명하는 방법에 대해서 알아 본다.

## 특징

* Git 프로젝트를 시각화, 워크플로우를 팀과 공유 하는 등의 목적으로 사용
* Repo 에서 커맨드 한번으로 .mp4 애니메이션 생성
  * 시작 커밋 ID/Ref 지정 (기본값은 HEAD)
  * 포함할 커밋 갯수 지정 (기본값은 8)
  * HEAD, 브랜치명, Tag의 Ref Label을 기본 표시
* 커스텀 인트로/아웃트로 추가 가능
* 다크모드/라이트모드

## 예시

![/assets/images/undefined/git-story.png](/assets/images/undefined/git-story.png)

## 사이트

[https://initialcommit.com/tools/git-story](https://initialcommit.com/tools/git-story)
