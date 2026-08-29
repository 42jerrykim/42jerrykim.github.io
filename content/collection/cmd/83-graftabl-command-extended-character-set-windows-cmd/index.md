---
draft: false
slug: graftabl-command-extended-character-set-windows-cmd
title: "[CMD] 83. graftabl - 그래픽 모드 확장 문자 세트"
description: "graftabl로 그래픽 모드에서 코드 페이지별 확장 문자를 표시하도록 설정하는 법과 최신 Windows에서는 대부분 설치되지 않는 레거시 명령이라는 점, chcp·mode로 대체해야 하는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 830
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Beginner
- graftabl
- 코드페이지
- Legacy(레거시)
- Encoding(인코딩)
- Comparison(비교)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Administration
- Education(교육)
- CLI
- Configuration(설정)
- History(역사)
- DOS
- Fundamentals(기초)
image: "wordcloud.png"
---

graftabl은 그래픽 모드에서 코드 페이지별 확장 문자 세트를 표시할 수 있게 설정하는 DOS 시절의 레거시 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [82장: ftype](/post/cmd/ftype-command-file-type-open-command-windows-cmd/)에서 파일 형식 연결을 다룬 뒤 이어진다. 앞 두 장(assoc, ftype)이 여전히 실무에서 쓰이는 명령이었다면, graftabl은 이 컬렉션 전체에서 가장 오래되고 가장 니치한 명령이다 — 이미 최신 Windows에는 기본 설치되지 않는 경우가 많다.

**이 장의 깊이**: 입문(역사적 맥락 이해 목적). **다루지 않는 것**: 코드 페이지 자체를 활성화·전환하는 것은 70장(chcp)이 담당한다; graftabl은 그래픽 모드에서의 표시 방식만 다룬다.

## 개요 + 정신 모델

graftabl은 "콘솔 입력 코드 페이지"가 아니라 <strong>그래픽 모드에서 확장 문자가 화면에 어떻게 그려지는지</strong>만 다룬다.

> "Enables Windows operating systems to display an extended character set in graphics mode. If used without parameters, **graftabl** displays the previous and the current code page." — Microsoft Learn, "graftabl"

이 명령은 DOS 시절, 그래픽 어댑터가 코드 페이지별 확장 ASCII 문자(악센트 부호, 키릴 문자 등)를 올바르게 그리도록 문자 세트를 메모리에 로드하는 용도로 만들어졌다. 오늘날 TrueType 폰트와 유니코드를 쓰는 콘솔에서는 이 문제 자체가 발생하지 않는다.

## 사용법

```
graftabl <코드페이지>
graftabl /status
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<코드페이지>` | 확장 문자 표시에 쓸 코드 페이지 번호 |
| `/status` | 현재 로드된 코드 페이지 표시 |

### 지원 코드 페이지

| 번호 | 지역 |
|---|---|
| 437 | 미국 |
| 850 | 다국어(라틴 I) |
| 852 | 슬라브(라틴 II) |
| 855 | 키릴(러시아어) |
| 857 | 터키어 |
| 860 | 포르투갈어 |
| 861 | 아이슬란드어 |
| 863 | 캐나다 프랑스어 |
| 865 | 노르딕 |
| 866 | 러시아어 |
| 869 | 현대 그리스어 |

## 예시

```
graftabl /status
graftabl 437
graftabl 850
graftabl 852
graftabl 866
```

## 주의사항·함정

**최신 Windows에는 이 명령 자체가 없는 경우가 많다**: Microsoft Learn이 명시적으로 경고한다.

> "The **graftabl** command is a legacy command, and therefore outdated. It is normally not installed in modern Windows versions. Please see the [chcp](/post/cmd/chcp-command-active-code-page-windows-cmd/) page for codepage handling." — Microsoft Learn, "graftabl"

즉 이 명령을 실행했을 때 "명령을 찾을 수 없다"는 오류가 나오더라도 시스템이 고장 난 것이 아니라 정상이다. 코드 페이지를 다뤄야 한다면 70장(chcp)이나 67장(mode)을 대신 써야 한다.

**콘솔 입력 코드 페이지는 바꾸지 않는다**: graftabl은 화면에 그려지는 방식만 바꿀 뿐, 콘솔이 입력을 해석하는 코드 페이지 자체는 바꾸지 못한다.

> "The **graftabl** command affects only the monitor display of extended characters of the code page that you specify. It doesn't change the actual console input code page. To change the console input code page, use the [mode](/post/cmd/mode-command-configure-system-devices-windows-cmd/) or [chcp](/post/cmd/chcp-command-active-code-page-windows-cmd/) command." — Microsoft Learn, "graftabl"

이 구분을 모르고 graftabl로 입력 인코딩 문제를 해결하려 하면 아무 효과가 없다 — 표시 문제와 입력 해석 문제는 서로 다른 계층이며, 후자는 반드시 mode·chcp로 다뤄야 한다.

**배치 스크립트에서 ERRORLEVEL로 결과를 확인할 수 있다**: graftabl은 종료 코드를 반환한다(0=성공, 1=잘못된 매개변수, 2=파일 오류). 30장대(배치 스크립팅)에서 다룬 `%ERRORLEVEL%` 패턴을 이 레거시 명령에도 그대로 적용할 수 있지만, 실무에서 이 명령 자체를 스크립트에 넣을 일은 거의 없다.

**PowerShell에는 대응하는 cmdlet이 없다 — 옮길 필요 자체가 없기 때문이다**: graftabl이 풀던 문제는 그래픽 모드에서 확장 문자를 렌더링하는 표시 계층의 문제였는데, 이 문제 자체가 Windows Terminal이나 PowerShell 콘솔 환경에는 존재하지 않는다. 현대 콘솔은 TrueType 폰트와 유니코드를 기본으로 사용해 확장·악센트 문자를 처음부터 올바르게 그리므로, 이 기능을 "이식"할 대상이 애초에 없다.

## 흔한 오개념

<strong>"graftabl이 최신 Windows에 없다는 것은 확장·악센트 문자를 콘솔에서 제대로 표시할 방법이 아예 없다는 뜻이다"</strong>는 오해가 흔하다. 실제로는 정반대다 — 최신 Windows 콘솔은 TrueType 폰트와 유니코드·UTF-8 지원(70장, chcp)을 통해 확장 문자를 처리하며, 이는 graftabl이 다루던 그래픽 모드 문자 세트 로딩과는 완전히 다른, 훨씬 더 강력한 방식이다. 즉 graftabl이 풀던 문제 자체가 오늘날에는 더 나은 방식으로 대체되어 사라진 것이지, 문제가 여전히 존재하는데 해결되지 않은 채로 방치된 것이 아니다.

## 다음 장에서는

다음은 84장 — 이 컬렉션의 마지막 장으로, 텍스트 파일을 프린터로 보내는 `print` 명령을 다룬다.

## 평가 기준

- graftabl이 그래픽 모드의 확장 문자 표시만 다루고 콘솔 입력 인코딩은 다루지 않는다는 것을 구분할 수 있다.
- 최신 Windows에서 이 명령이 기본 설치되지 않을 수 있고, 그 경우 chcp·mode로 대체해야 한다는 것을 안다.
- graftabl이 등장한 DOS 시절의 기술적 배경(그래픽 어댑터의 확장 ASCII 렌더링)을 이해한다.

## 참고

- [graftabl | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/graftabl)
- [chcp | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chcp)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
