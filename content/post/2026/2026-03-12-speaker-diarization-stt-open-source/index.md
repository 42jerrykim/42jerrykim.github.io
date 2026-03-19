---
title: "[AI] 녹음 음성 화자 인식·STT 오픈소스 정리 (Reverb, WhisperX, pyannote)"
description: "녹음된 음성에서 누가 언제 말했는지(화자 다이어리제이션)와 음성을 글자로 바꾸는(STT) 오픈소스 도구를 정리한다. Reverb, WhisperX, pyannote-audio의 특징, 요구사항, 라이선스와 선택 가이드를 담았으며 로컬 실행 가능한 프로젝트 위주로 소개한다."
date: 2026-03-12
lastmod: 2026-03-19
categories:
  - AI
  - OpenSource
tags:
  - AI
  - 인공지능
  - Machine-Learning
  - 머신러닝
  - Deep-Learning
  - 딥러닝
  - NLP
  - Open-Source
  - 오픈소스
  - Python
  - 파이썬
  - Docker
  - Blog
  - 블로그
  - Technology
  - 기술
  - Tutorial
  - 가이드
  - Guide
  - Review
  - 리뷰
  - Documentation
  - 문서화
  - Best-Practices
  - Reference
  - 참고
  - Comparison
  - 비교
  - How-To
  - Tips
  - Productivity
  - 생산성
  - Education
  - 교육
  - Innovation
  - 혁신
  - Troubleshooting
  - 트러블슈팅
  - Configuration
  - 설정
  - GitHub
  - Implementation
  - 구현
  - Web
  - 웹
  - API
  - Performance
  - 성능
  - Optimization
  - 최적화
  - Git
  - Linux
  - 리눅스
  - Automation
  - 자동화
  - Deployment
  - 배포
  - Backend
  - 백엔드
  - Data-Science
  - 데이터사이언스
  - Software-Architecture
  - Design-Pattern
  - Clean-Code
  - Refactoring
  - 리팩토링
  - Markdown
  - 마크다운
  - Workflow
  - 워크플로우
  - Migration
  - 마이그레이션
  - Privacy
  - 프라이버시
  - Self-Hosted
  - 셀프호스팅
  - Beginner
  - Case-Study
  - Terminal
  - 터미널
  - Hugo
  - Neural-Network
  - Security
  - 보안
  - Testing
  - 테스트
  - Code-Quality
  - 코드품질
  - Caching
  - 캐싱
  - Async
  - 비동기
  - Concurrency
  - 동시성
  - Monitoring
  - 모니터링
  - DevOps
  - CI-CD
  - Debugging
  - 디버깅
  - Error-Handling
  - 에러처리
  - Modularity
  - Interface
  - 인터페이스
  - Type-Safety
  - Maintainability
  - Scalability
  - 확장성
image: "wordcloud.png"
---

회의나 인터뷰 녹음처럼 **녹음된 음성**을 다룰 때, “누가 언제 말했는지(화자 인식·다이어리제이션)”와 “무슨 말을 했는지(음성 인식·STT)”를 함께 처리하고 싶을 때가 많다. 이 글에서는 **녹음 음성에 대한 화자 인식과 STT를 지원하는 오픈소스**를 웹 검색과 문서를 바탕으로 정리한다.

## 왜 화자 인식 + STT인가?

- **화자 다이어리제이션(Speaker diarization)**: 오디오 구간별로 “화자 A”, “화자 B”처럼 **누가 말한 구간인지** 구분하는 기술.
- **STT(Speech-to-Text)**: 음성을 **텍스트로 변환**하는 기술.

둘을 함께 쓰면 “화자 1: …”, “화자 2: …” 형태로 **발화자별 전사 결과**를 만들 수 있어 회의록, 인터뷰 정리, 자막 생성 등에 유용하다. 아래 도구들은 모두 **녹음 파일을 입력**으로 받을 수 있고, **로컬/오프라인 실행**이 가능한 오픈소스다.

---

## Reverb (Rev, 2024) — ASR + 다이어리제이션 통합

**저장소**: [revdotcom/reverb](https://github.com/revdotcom/reverb)

Reverb는 Rev에서 2024년 공개한 오픈소스로, **STT(ASR)와 화자 다이어리제이션을 한 번에** 제공한다.

### 특징

- **ASR**: WeNet 기반 STT. 장문 음성 인식 벤치마크에서 Whisper Large-v3, Canary-1B 대비 더 낮은 WER을 보고한다.
- **화자 다이어리제이션**: Pyannote 기반. 발화 구간별 화자 라벨을 붙인다.
- **입출력**: 녹음 오디오 파일 입력, CLI·Python API·Docker 지원.

### 요구사항

- Python 3.10+
- Hugging Face 액세스 토큰
- Git LFS

### 라이선스

- 코드: Apache-2.0. 모델은 Hugging Face에서 별도 확인 필요.

**정리**: 장문 녹음, 회의·인터뷰처럼 **STT와 화자 구분을 한 번에** 쓰고 싶을 때, 그리고 **최신 성능**을 중시할 때 적합하다.

---

## WhisperX — STT + 단어 단위 타임스탬프 + 다이어리제이션

**저장소**: [m-bain/whisperX](https://github.com/m-bain/whisperX)

WhisperX는 OpenAI **Whisper** 위에 **단어 단위 타임스탬프**와 **화자 다이어리제이션**을 붙인 오픈소스 파이프라인이다.

### 특징

- **STT**: Whisper 기반. 여러 언어·장문 녹음 지원.
- **단어 단위 타임스탬프**: 구간별·단어별 시간 정보 제공 → 자막·편집에 유리.
- **화자 다이어리제이션**: pyannote 연동으로 “누가 언제 말했는지” 라벨링.

### 장점

- 스타 수 2만 개 이상으로 커뮤니티가 크고, Whisper 생태계와 호환된다.
- 로컬 실행 가능, 녹음 파일 직접 입력 지원.

**정리**: **Whisper를 이미 쓰고 있거나**, **단어 단위 타임스탬프**가 필요할 때, 그리고 STT와 화자 구분을 함께 쓰고 싶을 때 고려할 만하다.

---

## pyannote-audio — 화자 다이어리제이션 전문

**저장소**: [pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio)

pyannote-audio는 **화자 다이어리제이션 전용** 툴킷이다. STT는 포함하지 않는다.

### 특징

- **화자 다이어리제이션**: 발화 활동 검출(SAD), 화자 전환 검출, 겹침 발화 검출, 화자 임베딩 등.
- **STT 없음**: 텍스트 전사는 하지 않으므로, Whisper·Reverb 등 **다른 STT와 조합**해서 사용한다.
- v4 기준 **Community-1** 파이프라인으로 로컬에서 무료 사용 가능( Hugging Face 토큰 필요).

### 활용

- “누가 언제 말했는지”만 필요할 때.
- Reverb·WhisperX의 **다이어리제이션 엔진**으로도 쓰인다.

**정리**: **화자 구분만** 필요하거나, 원하는 STT와 **직접 파이프라인을 짜고 싶을 때** 선택한다.

---

## 선택 가이드 (녹음 음성 기준)

| 목적 | 추천 |
|------|------|
| **STT + 화자 인식 한 번에** | **Reverb** 또는 **WhisperX** |
| **최신 성능·장문 녹음** | **Reverb** (2024, 벤치마크 상 우수) |
| **Whisper 기반 + 단어 단위 타임스탬프** | **WhisperX** |
| **화자 구분만** (STT는 따로) | **pyannote-audio** + 원하는 STT |

---

## 기타 참고

- **TranscriptionSuite** 등 “완전 로컬·오픈소스 음성 전사” 도구도 커뮤니티에서 소개된다. 요구사항·라이선스는 각 프로젝트를 확인하는 것이 좋다.
- **Whisper + pyannote**를 직접 묶어서 “Whisper로 STT → pyannote로 화자 구분 → 구간 매칭” 파이프라인을 만드는 방식도 가능하다.
- **IBM**의 `build-custom-stt-model-with-diarization` 등 커스텀 STT·다이어리제이션 구축 가이드도 있다.

Reverb·pyannote는 **Hugging Face 토큰**과 **모델 라이선스** 확인이 필요하다. 사용 목적(상업/비상업, 재배포 등)에 맞게 각 저장소와 Hugging Face 페이지를 꼭 확인하자.
