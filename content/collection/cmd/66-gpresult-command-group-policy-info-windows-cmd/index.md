---
draft: false
slug: gpresult-command-group-policy-info-windows-cmd
title: "[CMD] 66. gpresult - 그룹 정책 적용 결과(RSoP) 조회"
description: "gpresult로 사용자·컴퓨터에 적용된 그룹 정책 결과(RSoP)를 조회하는 법과 /r·/v·/z·/x·/h 중 반드시 하나를 지정해야 하는 규칙, /x·/h가 다른 옵션과 함께 쓰일 수 없는 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 660
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
- Advanced
- gpresult
- 그룹정책
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Security(보안)
- Networking(네트워킹)
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Beginner
image: "wordcloud.png"
---

gpresult는 원격 사용자와 컴퓨터에 적용된 정책의 결과 집합(Resultant Set of Policy, RSoP)을 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [65장: driverquery](/post/cmd/driverquery-command-device-driver-status-windows-cmd/)에서 드라이버 상태를 다룬 뒤 이어진다. 도메인 환경에서 "왜 이 컴퓨터·사용자에는 이 설정이 적용되는가"를 진단할 때 쓰는 명령이다.

**이 장의 깊이**: 고급. 도메인·그룹 정책 환경을 전제로 한다.

## 사용법

```
gpresult [/s <시스템> [/u <사용자> [/p [<비밀번호>]]]] [/user [<대상도메인>\]<대상사용자>] [/scope {user | computer}] {/r | /v | /z | [/x | /h] <파일이름> [/f] | /?}
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/r` | RSoP 요약 데이터 표시 |
| `/v` | 상세 정책 정보(우선순위 1로 적용된 세부 설정 포함) |
| `/z` | 사용 가능한 모든 정보(우선순위 1 이상 세부 설정까지) |
| `[/x \| /h] <파일이름>` | XML(`/x`) 또는 HTML(`/h`) 형식으로 저장. `/u`·`/p`·`/r`·`/v`·`/z`와 함께 쓸 수 없음 |
| `/f` | `/x`·`/h`로 지정한 파일이 이미 있어도 덮어씀 |
| `/scope user\|computer` | 사용자 또는 컴퓨터 정책만 표시(생략 시 둘 다) |
| `/user <대상사용자>` | RSoP를 확인할 대상 사용자 지정 |
| `/s <시스템>` | 원격 컴퓨터 지정 |

## 예시

```
gpresult /r
gpresult /v
gpresult /h report.html
gpresult /s srvmain /user maindom\targetuser /scope user /r
gpresult /s srvmain /user maindom\targetuser /z > policy.txt
gpresult /s srvmain /u maindom\hiropln /p p@ssW23 /r
```

## 주의사항·함정

**출력 옵션 중 반드시 하나를 지정해야 한다**: `/?`를 제외하면, `/r`·`/v`·`/z`·`/x`·`/h` 중 하나는 반드시 있어야 한다.

> "Except when using **/?**, you must include an output option, **/r**, **/v**, **/z**, **/x**, or **/h**." — Microsoft Learn, "gpresult"

옵션 없이 그냥 `gpresult`만 실행하면 원하는 결과를 얻지 못한다 — 최소한 `/r`(요약)을 붙여야 한다.

**`/x`·`/h`는 다른 대부분의 옵션과 함께 쓸 수 없다**: 파일로 저장하는 두 옵션은 `/u`, `/p`, `/r`, `/v`, `/z`와 동시에 지정할 수 없다. 파일로 저장하면서 동시에 화면에 요약을 보고 싶다면 두 번 실행해야 한다.

**`/v`·`/z`는 출력이 매우 길어 리다이렉션이 권장된다**: Microsoft Learn 스스로도 결과를 파일로 리다이렉션하는 것이 유용하다고 안내한다(`gpresult /z >policy.txt`). 63장(systeminfo)에서 이미 익힌 습관을 그대로 적용하면 된다.

**ARM64에서는 `/h`가 SysWow64 버전에서만 동작한다**: 흔히 마주치지 않는 함정이지만, ARM64 기반 Windows에서 HTML 보고서를 생성하려는데 원인 모를 오류가 난다면 이 아키텍처 제약을 의심해볼 수 있다.

**원격 방화벽 규칙이 열려 있어야 한다**: 원격 컴퓨터의 RSoP 데이터를 가져오려면 인바운드 네트워크 트래픽을 허용하는 방화벽 규칙이 미리 구성되어 있어야 한다.

**PowerShell 대안은 `Get-GPResultantSetOfPolicy`다**: GroupPolicy 모듈에 포함된 cmdlet으로 RSoP 데이터를 조회할 수 있다. 다만 이 모듈은 기본 PowerShell에 내장되어 있지 않고, 도메인에 가입된 컴퓨터에서 RSAT(원격 서버 관리 도구)의 그룹 정책 관리 기능을 설치해야 쓸 수 있는 경우가 많다 — gpresult처럼 별도 설치 없이 어디서나 바로 실행할 수 있는 것은 아니라는 점이 다르다.

## 흔한 오개념

<strong>"gpresult /s로 아무 원격 컴퓨터나 방화벽 설정 걱정 없이 조회할 수 있다"</strong>는 오해가 있다. 실제로는 원격 컴퓨터의 인바운드 방화벽 규칙이 미리 열려 있어야 하며, 기본 방화벽 설정 그대로인 컴퓨터를 대상으로 하면 원격 조회 자체가 실패한다.

## 다음 장에서는

다음은 67장 — 콘솔·직렬·병렬 포트 등 시스템 장치를 구성하는 `mode` 명령을 다룬다.

## 평가 기준

- gpresult로 사용자·컴퓨터에 적용된 그룹 정책 결과를 조회할 수 있다.
- `/r`·`/v`·`/z`·`/x`·`/h` 중 하나가 반드시 필요하다는 규칙을 안다.
- `/x`·`/h`가 다른 옵션과 함께 쓰일 수 없다는 제약을 설명할 수 있다.
- 원격 조회에 방화벽 인바운드 규칙이 필요하다는 것을 안다.

## 참고

- [gpresult | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
