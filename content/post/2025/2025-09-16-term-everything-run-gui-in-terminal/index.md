---
title: "[Linux] term.everything - 터미널에서 GUI 앱 실행하기"
description: "term.everything은 자체 제작 Wayland 컴포지터로, 리눅스에서 GUI 창을 모니터 대신 터미널로 렌더링한다. 로컬과 SSH 환경 모두에서 터미널 안에서 데스크톱 앱을 실행·조작할 수 있게 해 주며, kitty·iTerm2 같은 이미지 지원 터미널에선 더 높은 해상도를 활용할 수 있다."
date: 2025-09-16
lastmod: 2025-09-16
categories:
- "Linux"
- "Terminal"
- "Wayland"
tags:
- "term.everything"
- "Wayland"
- "Wayland compositor"
- "terminal GUI"
- "terminal"
- "CLI"
- "Linux"
- "x11"
- "Wayland host"
- "kitty"
- "iTerm2"
- "alacritty"
- "ssh"
- "remote desktop"
- "image protocol"
- "full resolution"
- "resolution scaling"
- "FPS"
- "performance"
- "TypeScript"
- "Bun"
- "C++"
- "AGPL-3.0"
- "FOSS"
- "open source"
- "GUI in terminal"
- "Firefox"
- "file manager"
- "Doom"
- "beta"
- "roadmap"
- "usage"
- "how it works"
- "HowIDidIt"
- "Linux desktop"
- "Compositor"
- "graphics"
- "rendering"
- "framebuffer"
- "SSH over terminal"
- "iterm2 inline images"
- "kitty graphics"
- "터미널"
- "리눅스"
- "웨일랜드"
- "컴포지터"
- "원격 접속"
- "이미지 터미널"
- "성능"
- "사용법"
- "오픈소스"
- "라이선스"
- "개발자 도구"
- "실험적 기능"
- "프로젝트 소개"
- "설치"
- "빌드"
image: "wordcloud.png"
---

## 한눈에 보기

- **무엇**: `term.everything`은 GUI 앱의 창을 모니터 대신 터미널에 그려주는, 순수 CLI 기반의 Wayland 컴포지터다. 터미널만으로도 데스크톱 앱을 실행·조작할 수 있다.
- **어디서**: 리눅스에서 동작하며, x11·Wayland 호스트 모두 지원. SSH로도 전송 가능하다.
- **어떻게**: 터미널의 행·열 해상도에 맞춰 창을 렌더링하며, kitty·iTerm2 같은 이미지 지원 터미널에선 고해상도 렌더링이 가능하다.
- **상태**: 베타 단계로 일부 앱은 실행이 실패하거나 크래시할 수 있다. 프로젝트와 예시는 저장소에서 확인 가능하다.

> 프로젝트 페이지: [mmulet/term.everything](https://github.com/mmulet/term.everything)

## 왜 흥미로운가

리눅스 서버나 원격 환경에서 “GUI가 꼭 필요하지만 X 포워딩이나 VNC 설정은 번거롭다”는 상황이 있다. `term.everything`은 터미널이 있는 어디서든 GUI를 가져올 수 있게 하고, SSH를 통해 시演·데모·간단 조작을 빠르게 공유하도록 돕는다. 또한 “터미널용 파일 뷰어를 또 만들지 말고, 이미 있는 파일 매니저를 터미널에서 그대로 쓰자”는 재치 있는 문제의식도 담고 있다.

## 동작 원리 요약

- **Wayland 컴포지터 내장**: 프로젝트 자체가 Wayland 컴포지터로, 외부 디스플레이 서버 없이 앱 창 버퍼를 직접 수신·합성한다.
- **터미널로 출력**: 합성된 결과를 터미널의 문자 격자 또는 이미지 프로토콜(kitty/iterm2 등)을 이용해 렌더링한다.
- **해상도/성능 트레이드오프**: 터미널 행·열을 늘리면 화질은 좋아지지만 프레임 레이트가 낮아질 수 있다. 이미지 지원 터미널에선 고해상도 출력이 가능하나 성능 비용이 커질 수 있다.

자세한 구현 내막은 저장소의 기술 기록을 참고하자: [HowIDidIt.md](https://github.com/mmulet/term.everything/blob/main/resources/HowIDidIt.md).

## 설치와 실행(개요)

- 가장 간단한 방법은 저장소의 릴리스를 내려받아 실행하는 것이다: [Releases](https://github.com/mmulet/term.everything/releases)
- 소스 코드는 **TypeScript(Bun)**와 **C++**가 혼합되어 있으며, 개발 친화적으로 구성되어 있다.
- 터미널이 kitty/iterm2처럼 이미지 렌더링을 지원하면 더 높은 품질을 기대할 수 있다.

## 호환성과 제약

- **플랫폼**: Linux. 호스트가 x11이든 Wayland든 동작하도록 설계됨.
- **전송**: SSH 상에서도 동작 가능. 네트워크·터미널 성능에 따라 지연/프레임이 달라질 수 있음.
- **앱 호환성(베타)**: 일부 앱이 실행에 실패하거나 충돌할 수 있다. 문제 시 이슈 리포트를 권장.

## 대표 활용 시나리오

- 원격 서버에서 브라우저·파일 매니저·도구 UI를 터미널만으로 잠깐 띄워 확인
- 라이브 데모/강의에서 설정 부담 없이 GUI를 터미널 스트림으로 공유
- 최소 권한 SSH 세션에서 가벼운 UI 상호작용 수행

## 라이선스와 기여

- **라이선스**: AGPL-3.0
- **기여**: 이슈/PR 환영. 코드베이스는 TypeScript(Bun) 위주에 C++ 일부가 포함됨.

## 로드맵(저장소 기준)

1) Term some things — 현재 단계  
2) Term most things  
3) Term everything❗

## 마무리

`term.everything`은 “터미널만 있어도 GUI를 쓸 수 있는가?”라는 오래된 질문에 신선한 답을 제시한다. 아직 베타이지만, SSH·원격 운영·시연 문맥에서 실용적 가능성을 충분히 보여주고 있다. 관심 있다면 저장소의 예제와 도움말을 먼저 확인해보자.

## 참고

- 저장소: [https://github.com/mmulet/term.everything](https://github.com/mmulet/term.everything)
- 구현 기록: [HowIDidIt.md](https://github.com/mmulet/term.everything/blob/main/resources/HowIDidIt.md)
- 릴리스: [Releases](https://github.com/mmulet/term.everything/releases)


