---
draft: false
slug: net-user-command-manage-user-accounts-windows-cmd
title: "[CMD] 78. net user - 로컬·도메인 사용자 계정 관리"
description: "net user로 사용자 계정을 추가·수정·삭제·조회하는 법과 net 상위 명령군 안에서의 위치, 비밀번호 최소 길이가 net accounts /minpwlen을 따르는 규칙을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 780
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
- net-user
- 사용자계정
- Security(보안)
- Networking(네트워킹)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Administration
- Configuration(설정)
- Beginner
- Productivity(생산성)
- Workflow(워크플로우)
image: "wordcloud.png"
---

net user는 로컬 컴퓨터나 도메인의 사용자 계정을 추가·수정·삭제하고 상세 정보를 표시하는 명령이다. Part 8(네트워크와 원격 진단)의 마지막 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [77장: getmac](/post/cmd/getmac-command-mac-address-windows-cmd/)에서 MAC 주소를 다룬 뒤 이어지며, Part 8의 마지막 장이자 이 컬렉션 전체의 네트워크 파트를 마무리한다. 지금까지 네트워크 자체(주소, 경로, 연결, 이름)를 다뤘다면, 이 장은 그 네트워크에 접속하는 주체인 "사용자 계정"을 다룬다.

**이 장의 깊이**: 고급. **다루지 않는 것**: net user는 사실 `net`이라는 더 큰 명령군의 하위 명령 중 하나다 — `net use`(공유 연결), `net share`(공유 생성), `net view`(네트워크 리소스 조회) 같은 다른 `net` 하위 명령은 이 컬렉션에서 별도로 다루지 않는다.

## 사용법

```
net user [<사용자이름> {<비밀번호> | *} [<옵션>]] [/domain]
net user [<사용자이름> {<비밀번호> | *} /add [<옵션>] [/domain]]
net user [<사용자이름> [/delete] [/domain]]
net user <사용자이름> [/times:{<시간> | all}]
net user <사용자이름> [/active:{yes | no}]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<사용자이름>` | 계정 이름(최대 20자) |
| `<비밀번호>` \| `*` | 비밀번호 지정. `*`이면 대화형으로 입력 요청(화면에 표시되지 않음) |
| `/domain` | 도메인 컨트롤러에서 작업 수행 |
| `/add` | 새 계정 생성 |
| `/delete` | 지정 계정 삭제 |
| `/active:yes\|no` | 계정 활성화 여부(기본 yes) |
| `/times:<요일>,<시간>` | 로그인 허용 요일·시간. `all`이면 항상 허용 |

### 자주 쓰는 세부 옵션

| 옵션 | 설명 |
|---|---|
| `/fullname:"<이름>"` | 전체 이름 |
| `/expires:<날짜>\|never` | 계정 만료일(기본 never) |
| `/passwordreq:yes\|no` | 비밀번호 필수 여부(기본 yes) |
| `/passwordchg:yes\|no` | 사용자가 스스로 비밀번호를 바꿀 수 있는지(기본 yes) |
| `/comment:"<설명>"` | 계정 설명(최대 48자) |

## 예시

```
net user
net user tommyh
net user jays Cyk4^g3B /add /passwordreq:yes /times:monday-friday,8am-5pm /fullname:"Jay Jamison"
net user jays * /add
net user miked /time:M-F,08:00-17:00
net user anibals /time:M,4AM-12PM;T,12PM-8PM;W-F,8AM-5PM
```

## 주의사항·함정

**비밀번호 최소 길이는 별도 명령의 설정을 따른다**: net user 자체에는 비밀번호 길이를 강제하는 옵션이 없다. 대신 시스템 전체에 적용되는 값을 참조한다.

> "A password must satisfy the minimum password length value that is set with the **net accounts /minpwlen** command. A password can have as many as 127 characters." — Microsoft Learn, "net user"

즉 계정마다 다른 비밀번호 정책을 net user로 개별 지정할 수는 없고, `net accounts /minpwlen`으로 설정한 시스템 전역 정책 안에서만 비밀번호를 정할 수 있다.

**만료일을 `never`로 지정해도 완전히 영구적이지는 않다**: 기본값인 `never`는 관리자가 수동으로 비활성화하거나 삭제하기 전까지는 만료일 자체가 없다는 뜻일 뿐, 계정이 다른 정책(비활성 계정 자동 정리 등)의 영향을 받지 않는다는 보장은 아니다.

**`/times`에 공백을 넣으면 안 된다**: 요일과 시간을 지정하는 형식(`M,4AM-12PM;T,12PM-8PM`)은 쉼표·세미콜론으로 구분자를 엄격히 지키고, 공백을 넣으면 파싱이 깨진다. 08장(cd)이나 44장(diskpart)의 문법과 달리, 이 옵션은 공백에 특히 민감하다.

**`net`은 훨씬 큰 명령군의 일부다**: 이 장에서 다룬 `net user`는 `net`이라는 상위 명령 아래 있는 수십 개 하위 명령 중 하나일 뿐이다. `net use`(네트워크 드라이브 연결), `net share`(폴더 공유), `net view`(네트워크의 다른 컴퓨터 조회), `net accounts`(계정 정책) 같은 형제 명령들이 있다 — 이 컬렉션은 사용자 계정 관리라는 한 갈래만 다루지만, 필요하다면 `net /?`로 전체 하위 명령 목록을 확인할 수 있다.

**비밀번호를 명령줄에 그대로 적으면 화면·이력·로그에 노출된다**: 위 예시의 `net user jays Cyk4^g3B /add`처럼 비밀번호를 명령줄에 평문으로 적으면, 그 값이 화면에 그대로 보이고 셸 명령 이력에 남으며, 옆에서 화면을 보는 사람이나 프로세스 생성 감사(Process Creation auditing) 같은 로깅 도구로 명령줄 인자를 수집하는 프로세스에도 실시간으로 노출된다. 더 안전한 패턴은 비밀번호 자리에 `*`을 쓰는 것이다 — 예시의 `net user jays * /add`처럼 쓰면 화면에 표시되지 않고 이력에도 남지 않는 대화형 입력으로 비밀번호를 받는다.

**PowerShell에서는 `New-LocalUser`·`Set-LocalUser`를 쓴다**: PowerShell의 대응 명령은 `New-LocalUser`와 `Set-LocalUser`이며, 비밀번호를 `-Password` 매개변수로 받되 평문 문자열이 아니라 `SecureString` 타입만 받는다. `net user`의 명령줄 평문 비밀번호 인자보다 기본적으로 더 안전한 설계다 — 다만 `SecureString`도 메모리 내 보호 수준이 제한적이므로 완전한 비밀 보호 수단으로 과신해서는 안 된다.

## 흔한 오개념

<strong>"도메인에 가입된 컴퓨터에서는 net user가 도메인 계정에 영향을 줄 수도 있다"</strong>는 오해가 흔하다. `/domain` 스위치를 붙이지 않은 `net user`는 그 컴퓨터가 도메인에 가입되어 있든 아니든 항상 로컬 컴퓨터의 계정 데이터베이스(SAM)만 대상으로 한다. 실제 Active Directory 도메인 계정을 다루려면 반드시 `/domain`을 명시해야 하며, 이를 빠뜨리면 의도한 도메인 계정이 아니라 완전히 별개인 로컬 전용 계정을 생성·수정하게 되는데도 아무런 오류나 경고 없이 조용히 그렇게 처리된다.

## 다음 장에서는

다음은 79장 — 시동 구성 데이터를 관리하는 `bcdboot` 명령으로 Part 9(부팅 구성과 기타 유틸리티)가 시작된다.

## 평가 기준

- net user로 사용자 계정을 조회·추가·수정·삭제할 수 있다.
- 비밀번호 최소 길이가 net user가 아니라 `net accounts /minpwlen`을 따른다는 것을 안다.
- `/times` 옵션의 엄격한 구분자 규칙(공백 금지)을 지켜 로그인 허용 시간을 지정할 수 있다.
- net user가 더 큰 `net` 명령군의 한 하위 명령일 뿐이라는 것을 안다.

## 참고

- [net user | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
