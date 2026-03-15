# Cursor CLI로 비드래프트 MD 본문 개선 명령어 정리

draft가 아닌 content MD 파일을 Cursor CLI로 **한 건씩** 개선할 때 사용하는 명령 형식, 재사용 프롬프트, 비드래프트 목록 생성 방법을 정리한 문서입니다.

**위치**: `script/md-improve/` — 사용법, 스크립트, 생성된 명령어 파일을 한 폴더에서 관리합니다.

---

## 1. Cursor CLI 명령 형식

- 에이전트 실행: `agent "프롬프트"` (또는 `cursor agent` 등 터미널 설정에 따라 다를 수 있음)
- **컨텍스트에 파일 포함**: `@` 로 파일/폴더 지정
- **비대화형**: `-p` 또는 `--print`, 파일 수정 허용: `--force`
- **경로**: 워크스페이스 루트 기준 **상대 경로** 사용 (슬래시 `/` 권장)

### 한 개 파일에 대해 개선할 때 (한 줄 예시)

**목표**: 최신 규칙에 맞게 **대폭** 개선(살짝 다듬기가 아니라 구조·분량·품질을 규칙 수준까지 끌어올림).

```powershell
agent -p --force "@content/collection/Algorithm/2025/2025-12-03-boj-27533-walk-separately-lindstrom-cpp-solution/index.md" "이 포스트를 최신 규칙에 맞게 대폭 개선해줘. ... (아래 재사용 프롬프트 전체 사용)"
```

**선별 실행**: `@` 뒤의 경로만 바꿔가며 복사·실행하면 됩니다.

**영화 리뷰(Movies)**: `content/collection/Movies/.cursor/rules/movie-review-writing-rules.mdc`를 반드시 준수하도록 프롬프트에 명시되어 있습니다.

---

## 2. 재사용 프롬프트 (복사용)

아래 블록을 그대로 복사해 `"..."` 안에 넣어 사용할 수 있습니다. **대폭 개선**을 요구하며, **영화 리뷰는 movie-review-writing-rules.mdc 준수**를 명시한 프롬프트입니다.

```
이 포스트를 최신 규칙에 맞게 대폭 개선해줘. 살짝 고치는 수준이 아니라, 규칙을 완전히 반영해서 내용과 구조를 크게 보강해줘. 1) 규칙 확인: .cursor/rules의 rules-that-must-be-followed.mdc, hugo-content-bundle-naming.mdc를 반드시 읽고, 이 포스트가 속한 컬렉션에 해당하는 규칙 파일도 반드시 읽어줘. 특히 content/collection/Movies/ 아래 영화 리뷰인 경우 content/collection/Movies/.cursor/rules/movie-review-writing-rules.mdc를 반드시 읽고 전 항목을 준수해줘. 2) Front matter: tags 50개 이상(영어·한글, data/tags.yaml 참고), description 150자 분량, title 70자 이하, 제목 형식·날짜·lastmod 등 규칙에 맞게 전부 수정해줘. 3) Mermaid: 노드 ID(camelCase/PascalCase, 예약어 금지), 라벨에 특수문자·등호 등 있으면 반드시 큰따옴표로 감싸기, 줄바꿈은 </br> 사용 등 규칙대로 모두 수정해줘. 4) 본문: 컬렉션 규칙에서 요구하는 섹션 구조를 반드시 반영해줘. 영화 리뷰(Movies)인 경우 movie-review-writing-rules.mdc에 따라 개요(영화 정보·추천 대상), 구조 분석(Act 5 도식), 영화 전체 내용(Act 1~5, 장면 비트 [S01][S02]... 연속·미드포인트·클라이맥스 표시), 캐릭터 분석(3명 이상), 영상미와 음악, 종합 평가(장단점·한 줄 평·참고 문헌 3개 이상) 등이 빠지지 않도록 추가·보강하고, 작성 체크리스트를 모두 충족해줘. 문장만 다듬는 수준이 아니라 구조와 분량·품질을 규칙과 우수 포스트 수준까지 끌어올려줘.
```

---

## 3. 비드래프트 목록 생성

**비드래프트** = frontmatter에 `draft: true`가 **없는** content 내 `.md` 파일입니다.

### 스크립트 사용 (권장)

**프로젝트 루트**에서 실행:

```powershell
.\script\md-improve\list-non-draft-md.ps1
```

- **출력**: 한 줄에 하나씩 상대 경로 (예: `content/collection/Algorithm/2025/.../index.md`)
- **파일로 저장** (같은 폴더에 저장):

```powershell
.\script\md-improve\list-non-draft-md.ps1 | Out-File -FilePath script\md-improve\non-draft-paths.txt -Encoding utf8
```

---

## 4. 명령어 나열 방식

대상이 수백~천 개이므로, **명령어 전체**는 스크립트로 생성하고, 문서에는 예시만 적어 둡니다.

### 명령어 생성 스크립트

경로 목록에서 `agent -p --force "@경로" "프롬프트"` 한 줄씩 생성. **프로젝트 루트**에서 실행:

```powershell
# 경로 목록 파일이 있을 때 (이 폴더의 non-draft-paths.txt 사용)
.\script\md-improve\generate-improve-commands.ps1 -PathListFile script\md-improve\non-draft-paths.txt -OutputFile script\md-improve\improve-commands.txt

# 파이프로 경로 전달
.\script\md-improve\list-non-draft-md.ps1 | .\script\md-improve\generate-improve-commands.ps1 -OutputFile script\md-improve\improve-commands.txt
```

생성된 `script\md-improve\improve-commands.txt`에서 **원하는 줄만 복사**해 터미널에 붙여 넣어 실행하면 됩니다.

### 생성된 명령어 예시 (형식만 참고)

```powershell
agent -p --force "@content/collection/Algorithm/2025/2025-12-03-boj-27533-walk-separately-lindstrom-cpp-solution/index.md" "이 포스트를 최신 규칙에 맞게 대폭 개선해줘. ..."
```

나머지 파일에 대해서는 `.\script\md-improve\list-non-draft-md.ps1`와 `.\script\md-improve\generate-improve-commands.ps1`를 실행해 `improve-commands.txt`를 만든 뒤, 필요한 줄만 복사해 실행하면 됩니다. **프롬프트를 바꾼 뒤에는 명령어를 다시 생성**해야 새 프롬프트가 반영됩니다.

---

## 5. 규칙 준수 범위 (프롬프트에 반영된 내용)

- **공통**: `.cursor/rules/rules-that-must-be-followed.mdc` — frontmatter(tags 50개 이상, description 150자, title 70자 이하), Mermaid 문법(노드 ID, 라벨 따옴표, `</br>` 등)
- **공통**: `.cursor/rules/hugo-content-bundle-naming.mdc` — 제목 형식, 날짜/lastmod
- **컬렉션별**: Algorithm, Movies, TV-Show, Vocabulary, CMD, Bash Shell 등 해당 경로의 규칙에 맞게 본문·메타 보완
- **영화 리뷰(Movies)**: `content/collection/Movies/.cursor/rules/movie-review-writing-rules.mdc` — 개요(영화 정보·추천 대상), Act 5 구조 분석, 영화 전체 내용(장면 비트 [S01]~ 연속·미드포인트·클라이맥스), 캐릭터 분석 3명 이상, 영상미와 음악, 종합 평가·참고 문헌 3개 이상, 작성 체크리스트 충족

---

## 6. 흐름 요약

1. `.\script\md-improve\list-non-draft-md.ps1` 실행 → 비드래프트 경로 목록 (필요 시 `script\md-improve\non-draft-paths.txt`로 저장)
2. `.\script\md-improve\generate-improve-commands.ps1` 실행 → `script\md-improve\improve-commands.txt` 생성
3. `improve-commands.txt`에서 **원하는 줄만 복사** → 터미널에서 `agent` 명령 실행
4. 한 번에 **하나의 md 파일**만 개선되므로, 선별 실행에 적합합니다.

---

## 이 폴더 구성

| 파일 | 설명 |
|------|------|
| `README.md` | 이 사용법 문서 |
| `list-non-draft-md.ps1` | 비드래프트 .md 경로 목록 출력 |
| `generate-improve-commands.ps1` | 경로 목록 → agent 명령 한 줄씩 생성 |
| `improve-commands.txt` | 생성된 명령어 목록 (스크립트 실행으로 갱신) |
| `non-draft-paths.txt` | 비드래프트 경로 저장 시 생성 (선택) |

규칙 파일은 워크스페이스 루트의 `.cursor/rules/rules-that-must-be-followed.mdc` 등을 참조합니다.
