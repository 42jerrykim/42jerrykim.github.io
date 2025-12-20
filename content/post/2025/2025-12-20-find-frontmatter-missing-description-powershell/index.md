---
title: "[PowerShell] Frontmatter Description 누락 파일 찾기"
description: "Cursor/VSCode에서 멀티라인 frontmatter 검색의 한계를 극복하고, PowerShell만으로 description이 없는 마크다운 파일을 찾아내는 방법을 단계별로 안내합니다. draft:true 제외 로직과 정규식 설명 포함."
categories:
- PowerShell
- Hugo
tags:
- PowerShell
- Frontmatter
- Markdown
- Hugo
- VSCode
- Cursor
- 검색
- 정규식
- RegularExpression
- ContentManagement
- BlogManagement
- 블로그관리
- 마크다운
- 프론트매터
- Description
- SEO
- 콘텐츠관리
- 파일검색
- 텍스트처리
- 스크립팅
- 자동화
- Automation
- TechGuide
- DevTools
- 개발도구
- 기술가이드
- ITGuide
- Windows
- Draft
- 멀티라인
- Multiline
- 파싱
- Parsing
- YAML
- 메타데이터
- Metadata
- 콘텐츠검수
- QualityControl
- 품질관리
- StaticSite
- 정적사이트
- 웹개발
- WebDev
- 블로그운영
- 컨텐츠제작
- 워크플로우
- Workflow
- 생산성
- Productivity
- 스크립트
- Script
date: 2025-12-20
lastmod: 2025-12-20
image: wordcloud.png
---

## 개요

Hugo나 Jekyll 같은 정적 사이트 생성기를 사용하다 보면, 수백 개의 마크다운 파일 중 일부에서 frontmatter의 `description` 필드가 누락되는 경우가 있습니다. SEO와 콘텐츠 품질 관리를 위해 모든 글에 적절한 description이 있는지 확인해야 하지만, Cursor나 VSCode의 기본 검색 기능만으로는 "특정 필드가 없는" 파일을 찾기 어렵습니다.

이 포스트에서는 **PowerShell만으로** frontmatter 블록(`--- ... ---`) 안에 `description:` 필드가 없는 마크다운 파일을 찾아내는 방법을 소개합니다. 또한 `draft: true`로 표시된 작성 중인 글은 제외하는 로직도 함께 다룹니다.

## Cursor/VSCode Search 패널의 한계

Cursor(또는 VSCode)의 검색 패널(Ctrl+Shift+F)은 기본적으로 **줄 단위 정규식 매칭**을 수행합니다. Frontmatter는 여러 줄에 걸친 YAML 블록이기 때문에, "description 필드가 없는 경우"를 찾으려면 다음이 필요합니다:

1. **멀티라인 매칭**: 전체 frontmatter 블록을 하나의 텍스트로 처리
2. **부정 조건(Negative Lookahead)**: "특정 패턴이 없는" 경우를 찾기

VSCode 검색은 이러한 고급 멀티라인 정규식을 지원하지 않기 때문에, **터미널 도구**(ripgrep, PowerShell)를 활용해야 합니다.

## PowerShell 솔루션

### 기본 스크립트: Description 누락 파일 찾기

다음 PowerShell 스크립트는 `content` 디렉토리 하위의 모든 `.md` 파일을 검사해, frontmatter가 있지만 `description:` 필드가 없는 파일의 전체 경로를 출력합니다.

```powershell
Get-ChildItem -Recurse -File -Filter *.md content | Where-Object {
  $c = Get-Content $_.FullName -Raw
  if ($c -match '^\s*---\s*\r?\n(?<fm>[\s\S]*?)\r?\n---\s*(\r?\n|$)') {
    $fm = $Matches.fm
    -not ($fm -match '(?m)^\s*description\s*:\s*\S')
  } else {
    $false
  }
} | Select-Object -ExpandProperty FullName
```

**동작 원리:**
1. `Get-ChildItem -Recurse -File -Filter *.md content`: `content` 디렉토리 아래 모든 `.md` 파일 탐색
2. `Get-Content $_.FullName -Raw`: 파일 전체를 하나의 문자열로 읽기
3. 정규식 `^\s*---\s*\r?\n(?<fm>[\s\S]*?)\r?\n---\s*(\r?\n|$)`: 파일 맨 앞의 frontmatter 블록(`--- ... ---`) 추출
4. `(?<fm>...)`: frontmatter 내용을 `$Matches.fm`에 캡처
5. `(?m)^\s*description\s*:\s*\S`: 멀티라인 모드에서 `description:` 필드가 있는지 확인 (값이 비어있지 않은 경우)
6. `-not (...)`: description이 **없는** 경우만 필터링

### Draft 제외: 작성 중인 글 건너뛰기

블로그를 운영하다 보면 `draft: true`로 표시된 작성 중인 글이 많습니다. 이런 글들은 아직 완성되지 않았으므로 description이 없어도 괜찮습니다. 다음 스크립트는 `draft: true`인 파일을 제외합니다.

```powershell
Get-ChildItem -Recurse -File -Filter *.md content | Where-Object {
  $c = Get-Content $_.FullName -Raw

  if ($c -match '^\s*---\s*\r?\n(?<fm>[\s\S]*?)\r?\n---\s*(\r?\n|$)') {
    $fm = $Matches.fm

    $hasDescription = ($fm -match '(?m)^\s*description\s*:\s*\S')
    $isDraftTrue    = ($fm -match '(?m)^\s*draft\s*:\s*"?true"?\b')

    (-not $hasDescription) -and (-not $isDraftTrue)
  }
  else {
    $false
  }
} | Select-Object -ExpandProperty FullName
```

**추가된 로직:**
- `$isDraftTrue = ($fm -match '(?m)^\s*draft\s*:\s*"?true"?\b')`: frontmatter 내에 `draft: true` 또는 `draft: "true"` 패턴이 있는지 확인
- `(-not $hasDescription) -and (-not $isDraftTrue)`: description도 없고, draft도 아닌 경우만 출력

### 정규식 상세 설명

#### `(?m)` - Multiline 모드
PowerShell의 정규식에서 `(?m)` 플래그를 사용하면 `^`와 `$`가 전체 문자열의 시작/끝이 아니라 **각 줄의 시작/끝**을 의미합니다. Frontmatter는 여러 줄로 구성되므로, 각 필드명을 줄 단위로 찾기 위해 필수입니다.

```powershell
# (?m) 없으면: ^ = 전체 문자열 시작만 매칭
# (?m) 있으면: ^ = 각 줄의 시작 매칭
$fm -match '(?m)^\s*description\s*:\s*\S'
```

#### `\b` - 단어 경계
`"?true"?\b`에서 `\b`는 단어 경계를 나타냅니다. `draft: true123` 같은 잘못된 값을 매칭하지 않도록 보장합니다.

#### `[\s\S]*?` - 최소 매칭
`[\s\S]`는 "모든 문자(공백 포함)"를 의미하고, `*?`는 **최소 매칭**(non-greedy)을 의미합니다. 이를 통해 첫 번째 `---`부터 두 번째 `---`까지만 frontmatter로 인식합니다.

## 결과 저장 옵션

검색 결과를 텍스트 파일로 저장하면, 나중에 참고하거나 다른 도구로 후처리할 수 있습니다.

```powershell
$results = Get-ChildItem -Recurse -File -Filter *.md content | Where-Object {
  $c = Get-Content $_.FullName -Raw
  if ($c -match '^\s*---\s*\r?\n(?<fm>[\s\S]*?)\r?\n---\s*(\r?\n|$)') {
    $fm = $Matches.fm
    $hasDescription = ($fm -match '(?m)^\s*description\s*:\s*\S')
    $isDraftTrue    = ($fm -match '(?m)^\s*draft\s*:\s*"?true"?\b')
    (-not $hasDescription) -and (-not $isDraftTrue)
  } else { $false }
} | Select-Object -ExpandProperty FullName

# 결과를 파일로 저장
$results | Set-Content .\missing-description.txt

# 총 개수 출력
Write-Host "Description 누락 파일: $($results.Count)개"
```

이제 `missing-description.txt` 파일에 description이 없는 파일 목록이 저장되며, Cursor에서 해당 경로를 클릭하면 바로 파일을 열 수 있습니다.

## 실무 팁

### 1. 특정 디렉토리만 검사
전체 `content` 대신 특정 하위 디렉토리만 검사하려면 경로를 변경하세요.

```powershell
Get-ChildItem -Recurse -File -Filter *.md content/post | Where-Object { ... }
```

### 2. 파일명만 간단히 출력
전체 경로가 아닌 파일명만 보고 싶다면:

```powershell
... | Select-Object -ExpandProperty Name
```

### 3. CSV로 내보내기
파일 경로, 수정 날짜 등을 함께 저장하려면:

```powershell
... | Select-Object FullName, LastWriteTime | Export-Csv .\missing-description.csv -NoTypeInformation
```

### 4. Cursor Task로 등록
자주 사용하는 경우 `.vscode/tasks.json`에 등록하면 `Tasks: Run Task` 메뉴에서 바로 실행할 수 있습니다.

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Find Missing Descriptions",
      "type": "shell",
      "command": "pwsh",
      "args": [
        "-NoProfile",
        "-Command",
        "Get-ChildItem -Recurse -File -Filter *.md content | Where-Object { $c = Get-Content $_.FullName -Raw; if ($c -match '^\\s*---\\s*\\r?\\n(?<fm>[\\s\\S]*?)\\r?\\n---\\s*(\\r?\\n|$)') { $fm = $Matches.fm; $hasDescription = ($fm -match '(?m)^\\s*description\\s*:\\s*\\S'); $isDraftTrue = ($fm -match '(?m)^\\s*draft\\s*:\\s*\"?true\"?\\b'); (-not $hasDescription) -and (-not $isDraftTrue) } else { $false } } | Select-Object -ExpandProperty FullName"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

## 대안: ripgrep 사용

시스템에 [ripgrep](https://github.com/BurntSushi/ripgrep)이 설치되어 있다면, PCRE2 정규식으로 더 빠르게 검색할 수 있습니다.

```bash
rg --pcre2 -U -l --glob "*.md" '(?ms)\A---\R(?!(?:(?!\R---\R).)*^\s*description\s*:)(?:(?!\R---\R).)*\R---' content
```

단, ripgrep은 별도 설치가 필요하고, "draft:true 제외" 로직을 추가하려면 더 복잡한 정규식이 필요합니다. PowerShell 방식이 가독성과 유지보수 측면에서 더 유리합니다.

## 마치며

정적 사이트를 운영하다 보면 콘텐츠 품질 관리가 중요합니다. Frontmatter의 description 필드는 검색 엔진 최적화(SEO)와 소셜 미디어 공유 시 표시되는 요약문으로 활용되므로, 모든 글에 적절한 description을 작성하는 것이 좋습니다.

이 포스트에서 소개한 PowerShell 스크립트를 활용하면, 수백 개의 마크다운 파일 중 description이 누락된 글을 빠르게 찾아낼 수 있습니다. 정기적으로 실행해 콘텐츠 품질을 유지하세요!

