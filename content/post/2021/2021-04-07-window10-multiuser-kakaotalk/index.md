---
title: "[How-To] Windows 10 다중 사용자 카카오톡 실행 권한 부여"
description: "Windows 10 한 PC 다중 사용자 환경에서 추가 계정의 카카오톡 실행 권한 문제를 해결하는 방법. 액세스 불가·0xc0000022 오류 대응, KakaoTalk.exe 보안 탭 권한 추가 절차, 재설치 시점 및 업데이트 후 주의 사항을 150자 분량으로 요약해 안내합니다."
categories:
  - KakaoTalk
date: "2021-04-07T00:00:00Z"
lastmod: "2026-03-16T00:00:00Z"
tags:
  - Windows
  - 윈도우
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - How-To
  - Tips
  - Troubleshooting
  - 트러블슈팅
  - Configuration
  - 설정
  - Technology
  - 기술
  - Blog
  - 블로그
  - Reference
  - 참고
  - Best-Practices
  - Documentation
  - 문서화
  - Productivity
  - 생산성
  - Education
  - 교육
  - Networking
  - 네트워킹
  - Mobile
  - 모바일
  - Workflow
  - 워크플로우
  - Migration
  - 마이그레이션
  - Hardware
  - 하드웨어
  - Cloud
  - 클라우드
  - Review
  - 리뷰
  - Comparison
  - 비교
  - Career
  - 커리어
  - Open-Source
  - 오픈소스
  - Innovation
  - 혁신
  - Markdown
  - 마크다운
  - Security
  - 보안
  - OS
  - 운영체제
  - Beginner
  - Case-Study
  - Error-Handling
  - 에러처리
  - 실습
  - Deep-Dive
  - Cheatsheet
  - 치트시트
  - Quick-Reference
  - DevOps
  - Automation
  - 자동화
  - IDE
  - Git
  - GitHub
  - Web
  - 웹
  - API
  - HTTP
  - JSON
  - YAML
  - Database
  - 데이터베이스
  - Caching
  - 캐싱
  - Performance
  - 성능
  - Debugging
  - 디버깅
  - Testing
  - 테스트
  - Implementation
  - 구현
  - Design-Pattern
  - 디자인패턴
  - Software-Architecture
  - 소프트웨어아키텍처
  - Clean-Code
  - 클린코드
  - Readability
  - Maintainability
  - Modularity
  - Code-Quality
  - 코드품질
  - Refactoring
  - 리팩토링
  - Pitfalls
  - 함정
  - Edge-Cases
  - 엣지케이스
  - Logging
  - 로깅
  - Profiling
  - 프로파일링
  - Benchmark
  - Deployment
  - 배포
  - Monitoring
  - 모니터링
  - Self-Hosted
  - 셀프호스팅
  - Privacy
  - 프라이버시
  - Gadget
  - 가젯
  - Android
  - iOS
  - Tablet
  - 태블릿
  - Keyboard
  - 키보드
  - Terminal
  - 터미널
  - Shell
  - 셸
  - Linux
  - 리눅스
  - macOS
  - Internet
  - 인터넷
  - Domain
  - 도메인
  - Agile
  - 애자일
  - Scrum
  - TDD
  - RDP
  - History
  - 역사
  - Culture
  - 문화
  - Science
  - 과학
  - Psychology
  - 심리학
  - Finance
  - 재무
  - Accounting
  - 회계
  - Vocabulary
  - English
  - 영단어
  - Conference
  - 컨퍼런스
  - Book-Review
  - 서평
  - Photography
  - 사진
  - Gaming
  - 게임
  - Cycling
  - 자전거
  - Watch
  - 시계
  - Speaker
  - 스피커
  - Samsung
  - Brand
  - 브랜드
  - ChatGPT
  - LLM
  - Prompt-Engineering
  - 프롬프트엔지니어링
  - Hugo
  - Jekyll
  - Tmux
  - Unzip
  - Compression
  - Advanced
image: "wordcloud.png"
draft: false
---

## 개요

이 포스트는 **한 대의 Windows 10 PC를 여러 사용자가 함께 사용할 때**, 새로 추가한 사용자 계정에서 **카카오톡(KakaoTalk) PC 버전이 실행되지 않는 현상**을 해결하는 방법을 정리한 가이드입니다. 설치한 사용자 외 다른 계정에서는 "지정한 장치, 경로 또는 파일에 액세스할 수 없습니다" 같은 권한 오류가 자주 발생하며, 여기에 **권한 추가 절차**, **0xc0000022 오류 시 재설치** 대응, **업데이트 후 재적용** 주의 사항까지 포함해 실무에서 바로 따라 할 수 있도록 구성했습니다.

**추천 대상**

- 가정·사무실에서 한 PC에 Windows 사용자 계정을 여러 개 두고, 계정별로 카카오톡을 각각 쓰려는 분
- 카카오톡 실행 시 "액세스할 수 없습니다" 또는 "0xc0000022" 오류 메시지를 겪는 분
- Windows 파일·폴더 보안 탭에서 권한을 추가하는 기본 절차를 알고 싶은 분

---

## 배경: Windows 다중 사용자와 카카오톡

Windows 10에서는 **한 PC에 여러 로컬 또는 Microsoft 계정**을 만들 수 있습니다. 사용자마다 바탕 화면, 문서, 브라우저 프로필 등이 분리되어 있어, 가족이나 동료가 같은 기기를 써도 **개인 정보가 구분**됩니다. 대부분의 프로그램은 `C:\Program Files` 등 공통 경로에 설치되며, 모든 사용자가 실행 파일을 실행할 수 있도록 기본 권한이 부여되는 경우가 많습니다.

반면 **카카오톡 PC 버전**은 설치 시 특정 사용자 계정 기준으로 권한이 설정되거나, 실행 파일·설치 폴더에 대한 **명시적 권한이 다른 사용자에게 없을 수** 있어, 추가한 사용자 계정에서는 실행이 거부되는 현상이 자주 발생합니다. 이는 Windows의 보안·권한 모델과 카카오톡 설치 방식이 맞지 않는 경우에 해당합니다.

---

## 문제 상황

**증상**

- **한 사용자 계정**에서는 카카오톡이 정상 실행됨.
- **다른 사용자 계정**으로 로그인한 뒤 카카오톡을 실행하면:
  - "**지정한 장치, 경로 또는 파일에 액세스할 수 없습니다.**" (또는 "이 항목에서 액세스할 수 있는 권한이 없는 것 같습니다.") 메시지가 뜨며 실행되지 않음.
- 다른 프로그램(브라우저, 메모장 등)은 해당 계정에서 정상 실행되는 경우가 많아, **카카오톡만 권한 문제**로 보이는 것이 특징입니다.

원인은 **카카오톡 설치 폴더 및 실행 파일(`KakaoTalk.exe`)에 대한 NTFS 권한**이 "다른 사용자"에게 읽기·실행 권한이 없기 때문입니다. 따라서 해당 사용자 계정을 보안 주체로 추가하고, 필요한 권한을 허용해 주면 해결할 수 있습니다.

---

## 해결 방법

### 1. 카카오톡 설치 경로 및 실행 파일 확인

일반적인 설치 경로는 다음과 같습니다.

- `C:\Program Files\Kakao\KakaoTalk\`
- 실행 파일: `KakaoTalk.exe`

위 경로가 아니라면, 바탕 화면 또는 시작 메뉴의 카카오톡 바로 가기에서 **우클릭 → 속성 → "파일 위치 열기"** 등으로 실제 설치 폴더를 확인한 뒤, 해당 폴더의 `KakaoTalk.exe`를 기준으로 아래 단계를 진행하면 됩니다.

### 2. 실행 파일에 사용자 권한 추가

1. **`KakaoTalk.exe`** 위치로 이동한 뒤, **`KakaoTalk.exe`**를 **우클릭** → **속성** 선택.
2. **보안** 탭 → **편집** 버튼 클릭.
3. **추가** 버튼 클릭 후, **실행이 안 되는 사용자 계정 이름**을 입력.
   - Microsoft 계정(이메일)을 쓰는 경우, Windows가 짧은 이름(예: `DESKTOP-XXXXX\abcde`)으로 할당한 경우가 있으므로, `C:\Users` 아래 폴더 이름을 참고하거나, "이름 확인"으로 검색해 선택.
4. 해당 계정을 선택한 상태에서 **모든 권한에 "허용"** 체크(또는 최소한 **읽기 및 실행**, **읽기**, **쓰기** 등 필요한 권한 허용) 후 **확인**.
5. 속성 창에서 **확인**을 눌러 저장.

이후 **해당 사용자 계정으로 로그인**한 뒤 카카오톡을 다시 실행해 봅니다.

### 3. "0xc0000022" 오류가 나는 경우

권한을 추가한 뒤에도 **"응용 프로그램이 올바로 시작될 수 없습니다(0xc0000022). 확인을 클릭하여 응용 프로그램을 닫습니다."** 라는 팝업이 뜨는 경우가 있습니다. 이는 실행 파일의 **무결성·서명·권한**이 꼬였을 때 자주 나타납니다.

**대응 절차**

1. **카카오톡 완전 제거** 후, **재부팅** 권장.
2. **다시 카카오톡 설치** (필요 시 모든 사용자용으로 설치하는 옵션이 있으면 선택).
3. 설치가 끝난 뒤, **실행이 안 되던 사용자 계정**에 대해 위 **2번 단계(권한 추가)** 를 다시 수행.
4. 해당 계정으로 로그인한 뒤 카카오톡 실행 확인.

아래 플로우는 위 과정을 요약한 것입니다.

```mermaid
flowchart LR
  subgraph problemGroup["문제 구간"]
    nodeA[다른 사용자로 로그인]
    nodeB["카카오톡 실행 시도"]
    nodeC["액세스할 수 없음"]
    nodeA --> nodeB
    nodeB --> nodeC
  end
  subgraph fixGroup["해결 구간"]
    nodeD["KakaoTalk.exe 보안 탭"]
    nodeE["사용자 계정 추가 및 권한 허용"]
    nodeF["해당 계정으로 실행 확인"]
    nodeD --> nodeE
    nodeE --> nodeF
  end
  subgraph extraGroup["0xc0000022 시"]
    nodeG["카카오톡 제거 후 재설치"]
    nodeH["다시 권한 추가"]
    nodeG --> nodeH
    nodeH --> nodeF
  end
  nodeC --> nodeD
  nodeF -->|"실패 시"| nodeG
```

---

## 주의 사항

- **카카오톡이 업데이트될 때마다** 실행 파일이나 설치 경로가 바뀌거나 권한이 초기화될 수 있습니다. 그럴 경우 **다시 해당 사용자 계정에 대해 권한 추가**를 해 주어야 할 수 있습니다.
- **관리자 권한**이 있는 계정으로 위 설정을 진행하는 것이 안전합니다. 권한을 과도하게 "Everyone" 등으로 열어 두면 보안 위험이 커지므로, **실행이 필요한 사용자 계정만** 추가하는 것을 권장합니다.
- 회사·기관 PC는 **그룹 정책·도메인 정책**으로 권한이 제한되어 있을 수 있으므로, 필요 시 관리자에게 문의한 뒤 진행하는 것이 좋습니다.

---

## 참고 문헌

- 노랗IT월드, 「[지정한 장치 경로 또는 파일에 액세스할 수 없습니다 오류 원인과 해결 방법 (윈도우7·10·11 공통)](https://yellowit.co.kr/it-review/%EC%A7%80%EC%A0%95%ED%95%9C-%EC%9E%A5%EC%B9%98-%EA%B2%BD%EB%A1%9C-%EB%98%90%EB%8A%94-%ED%8C%8C%EC%9D%BC%EC%97%90-%EC%95%A1%EC%84%B8%EC%8A%A4%ED%95%A0-%EC%88%98-%EC%97%86%EC%8A%B5%EB%8B%88%EB%8B%A4-2/)」, 2026년 3월 링크 확인.
- yuyu100, 「[윈도우10에서 카카오톡 실행 안될 때 권한주는 법](https://yuyu100.tistory.com/790)」, 2026년 3월 링크 확인.
- 노랗IT월드, 「[지정한 장치 경로 또는 파일에 액세스할 수 없습니다 – 윈도우10](https://yellowit.co.kr/it-review/%ec%a7%80%ec%a0%95%ed%95%9c-%ec%9e%a5%ec%b9%98-%ea%b2%bd%eb%a1%9c-%eb%98%90%eb%8a%94-%ed%8c%8c%ec%9d%bc%ec%97%90-%ec%95%a1%ec%84%b8%ec%8a%a4%ed%95%a0-%ec%88%98-%ec%97%86%ec%8a%b5%eb%8b%88%eb%8b%a4/)」, 2026년 3월 링크 확인.

---

문제 발생 시 팝업창 예시는 아래와 같습니다.

| ![문제 발생](/assets/images/2021/2021-04-07-122050.png) |
| :----------------------------------------------------------------: |
| *권한 부족 또는 0xc0000022 오류 시 나타날 수 있는 팝업 예시* |
