---
draft: true
title: "[Bash Shell] sed - 스트림 편집기"
description: "리눅스·유닉스에서 텍스트 스트림을 줄 단위로 변환하는 sed의 사용법, 치환(s), 삭제(d), 출력(p), 정규식과 플래그를 다룹니다."
date: 2026-03-15
lastmod: 2026-03-15
categories:
- Bash Shell
tags:
- Bash
- Shell
- Linux
- 리눅스
- Terminal
- 터미널
- Command
- 셸
- Guide
- 가이드
- Tutorial
- 튜토리얼
- Reference
- 참고
- Quick-Reference
- File-System
- String
- Process
- Automation
- 자동화
- Deployment
- 배포
- Error-Handling
- 에러처리
- Troubleshooting
- 트러블슈팅
- Workflow
- 워크플로우
- Best-Practices
- Documentation
- 문서화
- Configuration
- 설정
- Education
- 교육
- Technology
- 기술
- Productivity
- 생산성
- How-To
- Tips
- Beginner
- Advanced
- Comparison
- 비교
- Case-Study
- Deep-Dive
- 실습
- Review
- 리뷰
- Markdown
- 마크다운
- Open-Source
- 오픈소스
- History
- 역사
- sed
- 스트림편집
- 정규식
- 치환
- Regex
- 텍스트처리
image: "wordcloud.png"
---

`sed`(stream editor)는 **입력을 줄 단위**로 읽어 지정한 편집 명령을 적용한 뒤 출력한다. 치환·삭제·출력이 가장 많이 쓰인다.

## 사용법

```bash
sed [옵션] '스크립트' [파일...]
sed [옵션] -f 스크립트파일 [파일...]
```

## 주요 명령

| 명령 | 설명 |
|------|------|
| `s/패턴/대체/플래그` | 치환 (가장 많이 사용) |
| `d` | 해당 줄 삭제 |
| `p` | 해당 줄 출력 (보통 -n과 함께) |
| `q` | 여기서 종료 |

## 옵션

| 옵션 | 설명 |
|------|------|
| `-n`, `--quiet` | 패턴 공간을 자동 출력하지 않음 (p 등과 조합) |
| `-i[접미사]` | 파일 직접 수정 (백업 접미사 선택 가능) |
| `-E`, `-r` | 확장 정규식 사용 |

## 예시

```bash
# foo를 bar로 치환 (줄당 첫 번째만)
sed 's/foo/bar/' file.txt

# 모든 foo를 bar로 (g 플래그)
sed 's/foo/bar/g' file.txt

# 빈 줄 삭제
sed '/^$/d' file.txt

# 2번째 줄만 출력
sed -n '2p' file.txt

# 파일 직접 수정 (GNU sed)
sed -i 's/old/new/g' file.txt
```

## 참고

- [GNU sed manual](https://www.gnu.org/software/sed/manual/sed.html)
