---
draft: true
title: "[Developer Tools] Cursor/VSCode 키보드 단축키 완전 가이드"
description: "Cursor와 VSCode의 모든 키보드 단축키를 카테고리별로 정리했습니다. 편집, 탐색, 디버깅, 터미널, 검색, 파일 관리 등 각 기능별 단축키와 실전 활용법을 초보자부터 고급 사용자까지 이해할 수 있도록 설명합니다."
date: 2025-10-30
lastmod: 2025-10-30
categories:
- Developer Tools
- Productivity
- Cursor
- VSCode
- IDE
tags:
- Cursor
- VSCode
- keyboard shortcuts
- 키보드 단축키
- productivity
- 생산성
- developer tools
- 개발자 도구
- IDE
- code editor
- 코드 에디터
- shortcuts
- 단축키
- hotkeys
- keybindings
- 키 바인딩
- editing
- 편집
- navigation
- 탐색
- debugging
- 디버깅
- terminal
- 터미널
- search
- 검색
- replace
- 교체
- file management
- 파일 관리
- window management
- 창 관리
- editor groups
- 에디터 그룹
- Git
- source control
- 소스 제어
- version control
- 버전 관리
- AI features
- AI 기능
- Composer
- Cmd+K
- code completion
- 코드 완성
- IntelliSense
- refactoring
- 리팩토링
- multi-cursor
- 멀티 커서
- selection
- 선택
- copy paste
- 복사 붙여넣기
- undo redo
- 실행 취소
- find
- 찾기
- goto
- 이동
- explorer
- 탐색기
- sidebar
- 사이드바
- panel
- 패널
- command palette
- 명령 팔레트
- quick open
- 빠른 열기
- extensions
- 확장 기능
- settings
- 설정
- workspace
- 작업 공간
- split editor
- 에디터 분할
- tab management
- 탭 관리
- code folding
- 코드 접기
- comment
- 주석
- formatting
- 포매팅
- snippets
- 스니펫
- bracket matching
- 괄호 매칭
- line manipulation
- 줄 조작
- text transformation
- 텍스트 변환
- cursor movement
- 커서 이동
- scroll
- 스크롤
- zoom
- 줌
- focus
- 포커스
- keyboard navigation
- 키보드 탐색
- efficiency
- 효율성
- workflow
- 워크플로우
- tips
- 팁
- tricks
- 트릭
- best practices
- 모범 사례
- customization
- 커스터마이징
- configuration
- 설정
- power user
- 파워 유저
- advanced
- 고급
- beginner
- 초보자
image: wordcloud.png
---

개발 생산성을 극대화하는 가장 확실한 방법 중 하나는 키보드 단축키를 마스터하는 것이다. 마우스로 메뉴를 탐색하는 시간을 줄이고 손을 키보드에서 떼지 않고도 원하는 작업을 빠르게 수행할 수 있다면, 코딩 흐름이 끊기지 않고 더 깊은 집중 상태를 유지할 수 있다. 이 가이드에서는 Cursor와 VSCode의 모든 주요 키보드 단축키를 카테고리별로 정리하여, 초보자부터 고급 사용자까지 모두가 활용할 수 있도록 포괄적으로 설명한다.

## 단축키 표기법 안내

이 가이드에서 사용하는 키 표기법은 다음과 같다:

- **Ctrl**: Control 키 (macOS에서는 Cmd)
- **Alt**: Alt 키 (macOS에서는 Option)
- **Shift**: Shift 키
- **+**: 키를 동시에 누름
- **Space**: 스페이스바
- **Enter**: 엔터 키
- **Backspace**: 백스페이스 키
- **Delete**: Delete 키

macOS 사용자는 대부분의 Ctrl을 Cmd로 읽으면 된다.

## 기본 편집 단축키

### 텍스트 선택

코드를 편집하기 전에 먼저 텍스트를 선택해야 하는 경우가 많다. 다음은 다양한 선택 방법이다.

- **Ctrl+A**: 모든 텍스트 선택
- **Ctrl+L**: 현재 줄 전체 선택
- **Shift+방향키**: 문자/줄 단위로 선택 확장
- **Ctrl+Shift+방향키**: 단어/블록 단위로 선택 확장
- **Alt+Shift+방향키**: 열(Column) 선택 모드
- **Ctrl+Shift+L**: 선택한 텍스트의 모든 일치 항목 선택 (멀티 커서)
- **Ctrl+D**: 현재 단어 선택 / 다음 일치 항목 추가
- **Ctrl+U**: 마지막 커서 위치 취소

### 복사, 잘라내기, 붙여넣기

- **Ctrl+C**: 복사
- **Ctrl+X**: 잘라내기
- **Ctrl+V**: 붙여넣기
- **Ctrl+Shift+V**: 서식 없이 붙여넣기
- **Ctrl+K Ctrl+V**: 클립보드 히스토리 열기

### 실행 취소 및 재실행

- **Ctrl+Z**: 실행 취소 (Undo)
- **Ctrl+Y** 또는 **Ctrl+Shift+Z**: 재실행 (Redo)

### 줄 조작

- **Ctrl+Enter**: 아래에 새 줄 삽입
- **Ctrl+Shift+Enter**: 위에 새 줄 삽입
- **Alt+방향키 위/아래**: 현재 줄을 위/아래로 이동
- **Shift+Alt+방향키 위/아래**: 현재 줄 복사하여 위/아래에 붙여넣기
- **Ctrl+Shift+K**: 현재 줄 삭제
- **Ctrl+J**: 다음 줄과 합치기

### 들여쓰기

- **Tab**: 들여쓰기
- **Shift+Tab**: 내어쓰기
- **Ctrl+]**: 선택 영역 들여쓰기
- **Ctrl+[**: 선택 영역 내어쓰기

### 주석

- **Ctrl+/**: 줄 주석 토글
- **Shift+Alt+A**: 블록 주석 토글
- **Ctrl+K Ctrl+C**: 선택 영역 주석 처리
- **Ctrl+K Ctrl+U**: 선택 영역 주석 해제

### 코드 접기 (Folding)

- **Ctrl+Shift+[**: 현재 영역 접기
- **Ctrl+Shift+]**: 현재 영역 펼치기
- **Ctrl+K Ctrl+0**: 모든 영역 접기
- **Ctrl+K Ctrl+J**: 모든 영역 펼치기
- **Ctrl+K Ctrl+1~9**: 레벨별 접기

### 코드 포매팅

- **Shift+Alt+F**: 문서 전체 포매팅
- **Ctrl+K Ctrl+F**: 선택 영역 포매팅
- **Shift+Alt+O**: Import 구문 정리

## 커서 이동 및 탐색

### 기본 커서 이동

- **방향키**: 한 글자/줄씩 이동
- **Ctrl+방향키 좌/우**: 단어 단위로 이동
- **Home**: 줄의 처음으로 이동
- **End**: 줄의 끝으로 이동
- **Ctrl+Home**: 파일의 처음으로 이동
- **Ctrl+End**: 파일의 끝으로 이동
- **Ctrl+G**: 특정 줄로 이동 (줄 번호 입력)
- **Ctrl+U**: 마지막 커서 위치로 돌아가기

### 스크롤

- **Ctrl+방향키 위/아래**: 커서 위치는 유지하고 화면만 스크롤
- **Ctrl+PageUp/PageDown**: 이전/다음 에디터 탭으로 이동
- **Alt+PageUp/PageDown**: 한 화면씩 스크롤

### 심볼 및 정의로 이동

- **F12**: 정의로 이동 (Go to Definition)
- **Ctrl+F12**: 구현으로 이동 (Go to Implementation)
- **Shift+F12**: 참조 찾기 (Find All References)
- **Alt+F12**: 정의 미리보기 (Peek Definition)
- **Ctrl+Shift+O**: 파일 내 심볼로 이동
- **Ctrl+T**: 작업 공간 내 심볼로 이동

### 브래킷/괄호 이동

- **Ctrl+Shift+\\**: 짝이 맞는 브래킷으로 이동

### 멀티 커서

- **Alt+클릭**: 커서 추가
- **Ctrl+Alt+방향키 위/아래**: 위/아래에 커서 추가
- **Ctrl+D**: 현재 선택과 일치하는 다음 항목에 커서 추가
- **Ctrl+Shift+L**: 현재 선택과 일치하는 모든 항목에 커서 추가
- **Esc**: 멀티 커서 모드 종료

## 검색 및 교체

### 기본 검색

- **Ctrl+F**: 현재 파일에서 찾기
- **Ctrl+H**: 현재 파일에서 찾기 및 바꾸기
- **F3** 또는 **Enter**: 다음 찾기
- **Shift+F3** 또는 **Shift+Enter**: 이전 찾기
- **Alt+Enter**: 일치하는 모든 항목 선택
- **Esc**: 검색 상자 닫기

### 전역 검색

- **Ctrl+Shift+F**: 작업 공간 전체에서 검색
- **Ctrl+Shift+H**: 작업 공간 전체에서 찾기 및 바꾸기
- **F4**: 검색 결과에서 다음으로 이동
- **Shift+F4**: 검색 결과에서 이전으로 이동

### 검색 옵션

검색 상자에서 다음 버튼을 사용할 수 있다:
- **대소문자 구분** (Alt+C)
- **단어 단위로 찾기** (Alt+W)
- **정규식 사용** (Alt+R)

## 파일 및 폴더 관리

### 파일 열기 및 저장

- **Ctrl+O**: 파일 열기
- **Ctrl+S**: 파일 저장
- **Ctrl+Shift+S**: 다른 이름으로 저장
- **Ctrl+K S**: 모든 파일 저장
- **Ctrl+W**: 현재 에디터 닫기
- **Ctrl+K Ctrl+W**: 모든 에디터 닫기
- **Ctrl+Shift+T**: 최근에 닫은 에디터 다시 열기

### 빠른 열기

- **Ctrl+P**: 파일로 이동 (Quick Open)
- **Ctrl+Tab**: 열린 파일 간 전환
- **Ctrl+Shift+Tab**: 열린 파일 간 역방향 전환
- **Ctrl+K P**: 현재 파일의 경로 복사
- **Ctrl+K R**: 현재 파일을 탐색기에서 열기

### 탐색기

- **Ctrl+Shift+E**: 탐색기로 포커스 이동
- **Ctrl+K E**: 탐색기에서 현재 파일로 이동
- **Enter**: 파일 열기
- **Ctrl+Enter**: 옆에 열기
- **Space**: 미리보기

### 새 파일/폴더

탐색기에서:
- **Ctrl+N**: 새 파일
- **Ctrl+Shift+N**: 새 폴더

## 에디터 그룹 및 창 관리

### 에디터 분할

- **Ctrl+\\**: 에디터 분할 (Split)
- **Ctrl+1, 2, 3**: 첫 번째, 두 번째, 세 번째 에디터 그룹으로 포커스 이동
- **Ctrl+K Ctrl+방향키**: 에디터 그룹 간 포커스 이동
- **Ctrl+K Shift+방향키**: 에디터를 다른 그룹으로 이동

### 에디터 레이아웃

- **Ctrl+K 방향키**: 에디터 그룹 크기 조정
- **Ctrl+K Ctrl+Shift+방향키**: 에디터 그룹 이동
- **Ctrl+K V**: Markdown 미리보기를 옆에 열기

### 전체 화면 및 줌

- **F11**: 전체 화면 토글
- **Ctrl+=**: 확대
- **Ctrl+-**: 축소
- **Ctrl+0**: 확대/축소 초기화

### 사이드바 및 패널

- **Ctrl+B**: 사이드바 토글
- **Ctrl+J**: 패널 토글 (터미널, 문제, 출력 등)
- **Ctrl+Shift+U**: 출력 패널 표시
- **Ctrl+Shift+M**: 문제 패널 표시
- **Ctrl+Shift+Y**: 디버그 콘솔 표시

## 디버깅

### 기본 디버깅

- **F5**: 디버깅 시작/계속
- **Shift+F5**: 디버깅 중지
- **Ctrl+Shift+F5**: 재시작
- **F9**: 중단점(Breakpoint) 토글
- **F10**: 한 단계씩 실행 (Step Over)
- **F11**: 한 단계씩 코드 안으로 들어가기 (Step Into)
- **Shift+F11**: 한 단계씩 코드 밖으로 나가기 (Step Out)
- **Ctrl+K Ctrl+I**: 호버 정보 표시

### 디버그 뷰

- **Ctrl+Shift+D**: 디버그 뷰 열기
- **Ctrl+F8**: 활성화/비활성화 중단점

### 콘솔 및 REPL

- **Ctrl+Shift+Y**: 디버그 콘솔 토글

## 터미널

### 기본 터미널 작업

- **Ctrl+`**: 터미널 토글
- **Ctrl+Shift+`**: 새 터미널 생성
- **Ctrl+Shift+5**: 터미널 분할
- **Alt+방향키**: 터미널 간 포커스 이동
- **Ctrl+PageUp/PageDown**: 터미널 간 전환
- **Ctrl+Home/End**: 터미널 맨 위/아래로 스크롤

### 터미널 관리

- **Ctrl+C**: 실행 중인 명령 중지 (터미널 내부)
- **Ctrl+Shift+K**: 터미널 닫기

## Git 및 소스 제어

### 소스 제어 뷰

- **Ctrl+Shift+G**: 소스 제어 뷰 열기
- **Ctrl+Shift+G G**: Git: Commit 명령 실행
- **Ctrl+Shift+G P**: Git: Push 명령 실행

### 변경사항 보기

- **Ctrl+Shift+G D**: 변경사항 비교 (Diff)
- **F7**: 다음 변경사항으로 이동
- **Shift+F7**: 이전 변경사항으로 이동

### Gutter 액션

- 줄 번호 왼쪽의 Gutter를 클릭하여 Git blame 정보 확인

## AI 기능 (Cursor 전용)

Cursor는 VSCode를 기반으로 하지만 강력한 AI 기능을 추가로 제공한다.

### Composer

- **Ctrl+I** (또는 **Cmd+I** on macOS): Composer 열기
  - Composer는 Cursor의 AI 에이전트로, 여러 파일을 한 번에 편집하고 복잡한 코딩 작업을 수행할 수 있다.
  - 자연어로 요청을 입력하면 AI가 코드를 생성하거나 수정한다.
  - 파일 탐색, 검색, 편집을 자동으로 수행한다.

### 인라인 편집 (Cmd+K)

- **Ctrl+K** (또는 **Cmd+K** on macOS): 인라인 AI 편집 시작
  - 현재 커서 위치에서 AI에게 코드 수정을 요청할 수 있다.
  - 선택한 코드 블록을 수정하거나 새로운 코드를 생성한다.
  - 자연어 지시로 리팩토링, 주석 추가, 버그 수정 등을 수행한다.

### AI 채팅

- **Ctrl+L**: AI 채팅 열기
  - 코드에 대해 질문하거나 설명을 요청할 수 있다.
  - 현재 파일이나 선택한 코드를 컨텍스트로 제공한다.

### 코드 제안

- **Tab**: AI 제안 수락
- **Esc**: AI 제안 거부

## 명령 팔레트 및 설정

### 명령 팔레트

- **Ctrl+Shift+P** 또는 **F1**: 명령 팔레트 열기
  - 모든 명령을 검색하고 실행할 수 있는 가장 강력한 도구다.
  - 명령 이름의 일부만 입력해도 자동 완성된다.
  - `>` 접두사로 명령 실행, `@` 접두사로 심볼 검색, `:` 접두사로 줄 번호 이동 등을 할 수 있다.

### 설정

- **Ctrl+,**: 설정 열기
- **Ctrl+K Ctrl+S**: 키보드 단축키 설정 열기
- **Ctrl+Shift+P > "settings.json"**: JSON 형식으로 설정 편집

### 사용자 스니펫

- **Ctrl+Shift+P > "Configure User Snippets"**: 사용자 정의 스니펫 설정

## 확장 기능

### 확장 기능 관리

- **Ctrl+Shift+X**: 확장 기능 뷰 열기
- **Ctrl+Shift+P > "Extensions: Install Extensions"**: 확장 기능 설치
- **Ctrl+Shift+P > "Extensions: Show Installed Extensions"**: 설치된 확장 기능 보기

## 유용한 기타 기능

### IntelliSense

- **Ctrl+Space**: IntelliSense 트리거 (자동 완성)
- **Ctrl+Shift+Space**: 매개변수 힌트 표시
- **Ctrl+.**: 빠른 수정 (Quick Fix) 제안 표시

### 리팩토링

- **F2**: 심볼 이름 바꾸기 (Rename Symbol)
- **Ctrl+Shift+R**: 리팩토링 옵션 표시

### 문제 탐색

- **F8**: 다음 문제(오류/경고)로 이동
- **Shift+F8**: 이전 문제로 이동
- **Ctrl+Shift+M**: 문제 패널 열기

### 작업 (Tasks)

- **Ctrl+Shift+B**: 빌드 작업 실행
- **Ctrl+Shift+P > "Tasks: Run Task"**: 작업 실행

### Breadcrumbs

- **Ctrl+Shift+.**: Breadcrumbs로 포커스 이동
- **Ctrl+Shift+;**: Breadcrumbs의 마지막 요소로 포커스

### Markdown

- **Ctrl+Shift+V**: Markdown 미리보기
- **Ctrl+K V**: Markdown 미리보기를 옆에 열기

### Emmet

- **Tab**: Emmet 약어 확장 (HTML/CSS)
- **Ctrl+Shift+P > "Emmet: Wrap with Abbreviation"**: 선택 영역을 Emmet 약어로 감싸기

## 커스텀 키바인딩 설정하기

기본 단축키가 마음에 들지 않거나 자주 사용하는 명령에 단축키를 추가하고 싶다면 직접 커스터마이징할 수 있다.

### 키바인딩 편집기 사용

1. **Ctrl+K Ctrl+S**를 눌러 키보드 단축키 설정 열기
2. 변경하고 싶은 명령을 검색
3. 명령 옆의 연필 아이콘 클릭
4. 원하는 키 조합 입력
5. Enter를 눌러 저장

### keybindings.json 직접 편집

더 세밀한 제어를 원한다면 `keybindings.json` 파일을 직접 편집할 수 있다.

1. **Ctrl+Shift+P**를 눌러 명령 팔레트 열기
2. "Preferences: Open Keyboard Shortcuts (JSON)" 검색
3. JSON 형식으로 키바인딩 정의

예시:
```json
[
  {
    "key": "ctrl+shift+c",
    "command": "editor.action.commentLine",
    "when": "editorTextFocus"
  }
]
```

### 조건부 키바인딩

`when` 절을 사용하여 특정 조건에서만 단축키가 작동하도록 설정할 수 있다.

예를 들어:
- `"when": "editorTextFocus"`: 에디터에 포커스가 있을 때만
- `"when": "editorLangId == 'python'"`: Python 파일에서만
- `"when": "terminalFocus"`: 터미널에 포커스가 있을 때만

## 실전 활용 팁

### 초보자를 위한 시작 단축키 5개

처음부터 모든 단축키를 외울 필요는 없다. 다음 5개만 먼저 익혀도 생산성이 크게 향상된다:

1. **Ctrl+P**: 파일 빠르게 열기
2. **Ctrl+Shift+P**: 명령 팔레트 (모든 기능 검색)
3. **Ctrl+D**: 다음 일치 항목 선택 (멀티 커서)
4. **Ctrl+/**: 주석 토글
5. **Alt+방향키 위/아래**: 줄 이동

### 중급 사용자를 위한 생산성 향상 팁

- **멀티 커서 활용**: Ctrl+D와 Alt+클릭을 조합하여 반복 작업을 빠르게 처리
- **스니펫 만들기**: 자주 사용하는 코드 패턴을 스니펫으로 등록
- **Emmet 활용**: HTML/CSS 작성 시 Emmet 약어로 빠르게 마크업 생성
- **정규식 검색**: Ctrl+F에서 정규식 모드를 활용하여 복잡한 패턴 검색

### 고급 사용자를 위한 워크플로우 최적화

- **작업 자동화**: tasks.json으로 빌드, 테스트, 배포 작업 자동화
- **멀티 커서 고급 기법**: Column selection(Alt+Shift+드래그)과 Ctrl+Shift+L 조합
- **Vim 키바인딩**: Vim 확장 설치 후 모달 편집으로 마우스 없이 작업
- **커스텀 스니펫과 키바인딩**: 팀 전체에서 사용할 공통 설정 공유

### 단축키 학습 전략

1. **단계적 학습**: 한 번에 5-10개씩 익히고 익숙해지면 다음으로 진행
2. **매일 사용**: 의식적으로 마우스 대신 키보드 사용 연습
3. **치트시트 활용**: 자주 보이는 곳에 단축키 목록 붙여두기
4. **명령 팔레트 활용**: 단축키가 기억나지 않으면 Ctrl+Shift+P로 검색

## 플랫폼별 차이점

### Windows/Linux vs macOS

- Windows/Linux의 **Ctrl**은 대부분 macOS에서 **Cmd**에 대응
- Windows/Linux의 **Alt**는 대부분 macOS에서 **Option**에 대응
- 일부 단축키는 플랫폼에 따라 다를 수 있으므로 설정에서 확인 필요

### macOS 전용 단축키

- **Cmd+,**: 설정 열기
- **Cmd+W**: 탭 닫기
- **Cmd+Q**: 애플리케이션 종료
- **Cmd+H**: 애플리케이션 숨기기

## 자주 발생하는 문제와 해결

### 단축키가 작동하지 않을 때

- 확장 프로그램이 단축키를 오버라이드하고 있는지 확인
- 시스템 단축키와 충돌하는지 확인 (특히 Windows의 Ctrl+Alt 조합)
- 키보드 레이아웃 설정 확인

### 단축키 충돌 해결

- **Ctrl+K Ctrl+S**로 키바인딩 설정 열기
- 충돌하는 단축키 검색
- 우선순위가 높은 것을 남기고 나머지 제거하거나 변경

## 결론

키보드 단축키는 처음에는 배우기 어려워 보이지만, 일단 익숙해지면 개발 속도와 효율성이 비약적으로 향상된다. 이 가이드에서 소개한 단축키를 모두 한 번에 외울 필요는 없다. 자신의 작업 패턴에 맞는 단축키부터 하나씩 익혀가며, 점차 마우스에 손을 뻗는 횟수를 줄여나가면 된다.

특히 Cursor의 AI 기능(Composer, Cmd+K)을 단축키로 빠르게 호출할 수 있다면, 코딩 흐름을 유지하면서도 AI의 도움을 효과적으로 받을 수 있다. 명령 팔레트(Ctrl+Shift+P)는 모든 단축키를 외우지 못하더라도 필요한 기능을 빠르게 찾을 수 있는 강력한 도구이니, 이것만큼은 꼭 기억하자.

매일 조금씩 새로운 단축키를 시도하고, 자신만의 워크플로우를 최적화해 나가면, 어느새 키보드만으로 거의 모든 작업을 처리하는 파워 유저가 되어 있을 것이다. 행복한 코딩 되시길!

