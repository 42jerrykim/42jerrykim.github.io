---
name: shell-command-post-writing
description: >-
  셸/터미널 명령어 글 작성 가이드 — Bash Shell(content/collection/bashshell/)과 CMD(content/collection/cmd/)
  공통. 플랫폼별 접두어([Bash Shell]/[CMD])·경로·태그 풀, 70자 이하 title, 150자 description, 50개 이상 tags,
  본문 구조(명령어 참조형·개념/가이드형), 정신 모델·이식성 주의, Mermaid 준수, 작성 체크리스트를 포함한다.
  bashshell·cmd 컬렉션 포스트 작성·보강 시 사용한다. (구 bashshell-post-writing·cmd-post-writing 통합)
---

# 셸 명령어 포스트 작성 가이드 (Bash Shell + CMD 공통)

`content/collection/bashshell/`(Bash/Linux)과 `content/collection/cmd/`(Windows 명령 프롬프트)의 명령어·개념 포스트를 작성할 때 따르는 단일 가이드다. 두 컬렉션은 글 성격이 동일하므로 규칙을 공유하고, 플랫폼별 차이는 §1 표로만 분기한다. [`blog-post-writing`](../blog-post-writing/SKILL.md), [`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md)과 함께 적용하며, 교육 글 내용 완결성은 [`educational-content-writing`](../educational-content-writing/SKILL.md) §7.2(명령어·도구)를 따른다.

---

## 1. 플랫폼별 분기 (이것만 다르다)

| 항목 | Bash Shell | CMD |
|------|-----------|-----|
| 경로 | `content/collection/bashshell/<slug>/index.md` | `content/collection/cmd/<slug>/index.md` |
| 제목 접두어 | `[Bash Shell]` | `[CMD]` |
| title 예 | `[Bash Shell] grep - 패턴 검색` | `[CMD] rmdir - 빈 폴더 삭제` |
| categories | `- Bash Shell` | `- CMD` (기존 컬렉션 관례 확인) |
| 핵심 태그 풀 | Bash, Shell, Linux, 리눅스, Terminal, File-System, Process, Automation | Windows, 윈도우, Shell, 셸, Terminal, Batch, Automation, 자동화 |
| 1차 출처 | man 페이지·GNU/POSIX 문서 | Microsoft Learn 명령 참조 |
| 이식성 주의 | GNU vs BSD/POSIX 옵션 차이 | CMD vs PowerShell 차이, (선택) 유닉스 대응 명령 비교 |

## 2. 공통 메타 규칙 (필수)

- **title**: 접두어 + `명령어 - 핵심 역할` 형식, 70자 이내.
- **description**: 150자 내외. 명령어 역할·주요 옵션·활용 맥락(또는 대상 독자)을 2~3문장으로.
- **tags**: 최소 50개 이상(한글·영어 혼합), `data/tags.yaml` 승인 태그 우선. **명령어·기능·도메인과 실제 관련 있는 태그만** 사용한다 — Markdown, Deployment처럼 본문과 무관한 보일러플레이트로 개수를 채우지 않는다([`educational-content-writing`](../educational-content-writing/SKILL.md) §7.3 태그=본문 일치).
- **date / lastmod**: 작성·수정 당일(로컬 타임존, `Get-Date -Format "yyyy-MM-dd"`). 폴더명에 날짜를 쓰면 `date`와 동일 유지. 의미 있는 개정 시 `lastmod` 갱신.
- **draft**: 신규 글은 `draft: true`. 배포 전 검토 후 사람이 `draft: false`로 변경.
- **categories**: 리스트 형식(문자열 금지).
- **image**: 워드클라우드 사용 시 `wordcloud.png`, 없으면 `tmp_wordcloud.png` 등 고정 이미지 명시.
- **폴더명(slug)**: 소문자·하이픈, 명령어명 또는 개념명 (예: `grep`, `xcopy`, `io-redirection`, `setlocal-endlocal`).

## 3. 본문 구조

### 3.0 정신 모델 우선 (공통 원칙)

옵션 나열 전에 **이 도구가 세상을 보는 방식**을 한 단락으로 먼저 서술한다 (예: awk=레코드/필드 스트림, `find`=트리 순회+술어 평가, `xcopy`=원본→대상 트리 복제). 독자가 옵션을 외우는 대신 모델로부터 유추할 수 있게 한다.

### 3.1 명령어 참조형 (예: grep, find, ps / dir, xcopy, rmdir)

1. **개요**: 명령어 역할, 지원 환경(Bash/POSIX 셸 또는 CMD/PowerShell) + 정신 모델
2. **사용법**: `명령 [옵션] [인자...]` 기본 문법 (그대로 실행 가능한 형태)
3. **옵션/매개변수**: 그룹별 표 또는 리스트. 짧은 설명 + 필요 시 예시
4. **예시**: 실전 명령 5~10개 (파이프/리다이렉션 조합, 자주 쓰는 옵션 조합, 배치 활용)
5. **주의사항·함정**: 와일드카드·인용/이스케이프·공백 처리·권한·복구 불가 동작, **이식성 차이**(§1 표의 해당 항목)
6. **Reference**: 1차 출처(man / Microsoft Learn) 1~2개 링크 (접근 확인 필수)

### 3.2 개념/가이드형 (예: redirection, pipe, 환경변수)

1. **개요**: 정의·중요성·활용 사례
2. **기본 개념**: 작동 원리, 관련 용어(파일 디스크립터 등)
3. **종류/세부**: 하위 유형별 설명 (입력/출력 리디렉션, Here Document 등)
4. **예제·다이어그램**: Mermaid로 흐름 시각화
5. **(선택)** FAQ, 관련 기술, 결론
6. **Reference**: 공식 문서·참고 링크

## 4. Mermaid 규칙

[`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md)의 문법(노드 ID 공백 없이, 특수문자 라벨은 `""` 감싸기, 줄바꿈 `</br>`)을 따른다. 파이프라인·리디렉션 흐름 다이어그램에서 특히 자주 위반되므로 꼼꼼히 확인한다.

## 5. 작성 체크리스트

- [ ] 경로·접두어·categories가 §1 표의 해당 플랫폼과 일치하는가?
- [ ] title 70자 이내, description 150자 내외인가?
- [ ] tags 50개 이상이고, 본문과 무관한 보일러플레이트 태그가 없는가?
- [ ] 신규 글에 `draft: true`가 있는가? date/lastmod가 정확한가?
- [ ] 옵션 나열 전에 **정신 모델** 단락이 있는가?
- [ ] 본문이 참조형(§3.1) 또는 개념형(§3.2) 구조를 따랐는가?
- [ ] **이식성 주의**(GNU/BSD 또는 CMD/PowerShell 차이)를 다뤘는가?
- [ ] Mermaid 노드 ID·라벨 규칙을 지켰는가?
- [ ] 1차 출처(man/Microsoft Learn) Reference가 있고 링크가 접근 가능한가?
