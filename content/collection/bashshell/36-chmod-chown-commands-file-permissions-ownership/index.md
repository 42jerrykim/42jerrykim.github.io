---
draft: false
slug: chmod-chown-commands-file-permissions-ownership
title: "[Bash Shell] 36. chmod, chown - 권한과 소유권"
description: "리눅스·유닉스에서 파일 권한을 바꾸는 chmod와 소유자·그룹을 바꾸는 chown을 서로 다른 두 축으로 구분해 정리한다. 8진수·기호 모드, 재귀 옵션의 심볼릭 링크 처리, setuid/setgid/sticky bit, umask까지 실무 예제로 다룬다."
date: 2026-03-15
lastmod: 2026-08-24
collection_order: 360
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Automation(자동화)
- Security(보안)
- Permission
- System-Administration(시스템관리)
- chmod
- chown
- chgrp
- umask
- setuid
- setgid
- sticky-bit
- 8진수권한
- 기호모드
- 소유자
- 소유권
- 그룹
- rwx
- root
- 재귀적용
- 심볼릭링크
- 접근제어
- 파일권한
- privilege-escalation
image: "wordcloud.png"
---

`chmod`는 <strong>권한(퍼미션)</strong>을, `chown`은 <strong>소유자·그룹</strong>을 바꾼다. 이름은 비슷해 보여도 커널 안에서 완전히 다른 메타데이터를 건드리는 별개의 명령어다.

## 이 장을 읽기 전에

직전 챕터인 [35장: alias](/post/bashshell/alias-command-shell-command-shortcuts/)까지가 Part 5(셸 스크립팅)였다. 조건문·반복문·함수·종료 코드로 스크립트를 작성하고 제어하는 법을 다뤘다면, 이 장부터는 <strong>Part 6(파일 시스템과 권한)</strong>이 시작된다. 지금까지 배운 스크립팅 도구로 파일을 다루려면 그 전에 "누가 이 파일을 읽고 쓰고 실행할 수 있는가"와 "이 파일은 누구 소유인가"를 정확히 알아야 한다 — 이 장은 그 두 질문에 각각 답하는 `chmod`와 `chown`을 다룬다.

이 장이 전제하는 지식은 [07장: cp, mv, rm](/post/bashshell/cp-mv-rm-commands-copy-move-delete-files/)에서 다룬 기본적인 파일·디렉터리 조작 정도이며, 별도의 셸 스크립팅 지식은 필요 없다. 난이도는 입문–중급이다. 기본 권한 변경부터 8진수·기호 모드, 재귀 적용 시 심볼릭 링크 처리, setuid/setgid/sticky bit 같은 특수 권한 비트까지 다룬다. **다루지 않는 것**: 조건에 맞는 파일을 찾아 `chmod`/`chown`과 함께 실행하는 법(`find ... -exec chmod ...`)은 [37장: find](/post/bashshell/find-command-search-files-conditions-linux/)에서 다룬다. rwx 9비트 모델을 넘어서는 세분화된 ACL(Access Control List)은 이 컬렉션의 범위 밖이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| Permission denied를 당장 해결해야 하는 사람 | 개요+정신 모델, 사용법·옵션, 예시 | 8진수·기호 모드로 원하는 권한을 정확히 설정하고, 소유자·그룹을 바꿔 흔한 권한 에러를 해결한다 |
| 배포·시스템 관리 스크립트를 짜려는 사람 | 주의사항·함정, 흔한 오개념 | 재귀 적용 시 심볼릭 링크 함정, root 권한 제약, setuid/setgid 자동 해제 같은 안전장치를 이해하고 스크립트에 반영한다 |

## 개요 + 정신 모델

리눅스에서 모든 파일은 세 그룹(소유자·그룹·기타)에 대해 읽기·쓰기·실행(rwx) 세 비트씩, 총 9비트의 <strong>권한(permission)</strong> 정보를 갖는다. `chmod`("change mode")는 이 "누가 무엇을 할 수 있는가"라는 권한 비트만 바꾼다. 반면 파일은 그와 완전히 별개로 "이 파일은 누구 소유이고 어느 그룹에 속하는가"라는 <strong>소유권(ownership)</strong> 정보(UID·GID)도 갖고 있으며, `chown`("change owner")은 이 소유권만 바꾼다. 두 명령을 같은 대상을 다루는 옵션 차이 정도로 착각하기 쉽지만, 실제로는 커널 시스템 호출 수준에서부터 `chmod(2)`와 `chown(2)`로 완전히 분리되어 있다 — 권한과 소유권은 서로 독립적인 두 축이라, 파일을 소유하지 않아도 실행 권한이 있으면 실행할 수 있고, 소유자라도 자신에게 읽기 권한을 주지 않으면 자기 파일을 못 읽을 수도 있다.

권한을 표기하는 방식도 두 갈래로 나뉜다. <strong>8진수 모드</strong>(`755`)는 rwx 9비트를 3비트씩 묶어 8진수 숫자 세 개(소유자·그룹·기타)로 표현한 것이고, <strong>기호 모드</strong>(`u+x`)는 "누구(u/g/o/a)에게 무엇(r/w/x)을 어떻게(+/-/=)"라는 문장 구조로 표현한 것이다. 둘은 표기 방식만 다를 뿐 최종적으로 바꾸는 대상(같은 9비트)은 동일하다 — `chmod 755 file`과 `chmod u=rwx,g=rx,o=rx file`은 결과가 완전히 같다. 8진수는 전체 권한을 한 번에 지정할 때 빠르고, 기호 모드는 기존 권한 중 일부만 바꿀 때(`u+x`처럼 나머지는 그대로 두고 실행 권한만 추가) 더 안전하다.

## 사용법 · 옵션

```bash
chmod [옵션] 8진수 파일...
chmod [옵션] 기호모드 파일...
chown [옵션] 사용자[:그룹] 파일...
chown [옵션] :그룹 파일...
```

### chmod — 8진수 모드

세 자리 숫자는 순서대로 소유자·그룹·기타의 권한이며, 각 자리는 r(4)+w(2)+x(1)를 더한 값이다.

| 값 | 의미 | 값 | 의미 |
|----|------|----|------|
| 7 | rwx (4+2+1) | 3 | -wx (2+1) |
| 6 | rw- (4+2) | 2 | -w- |
| 5 | r-x (4+1) | 1 | --x |
| 4 | r-- | 0 | --- |

네 자리로 쓰면 맨 앞자리가 setuid(4)·setgid(2)·sticky(1) 같은 특수 권한 비트를 지정한다(아래 "특수 권한 비트" 참고). 예를 들어 `4755`는 setuid + `rwxr-xr-x`다.

### chmod — 기호 모드

| 기호 | 의미 |
|------|------|
| `u`, `g`, `o`, `a` | 소유자(user), 그룹(group), 기타(other), 전체(all) |
| `+`, `-`, `=` | 권한 추가, 제거, 정확히 지정(나머지는 제거) |
| `r`, `w`, `x` | 읽기, 쓰기, 실행 |
| `s` | setuid(`u`에 적용 시) 또는 setgid(`g`에 적용 시) |
| `t` | sticky bit(`a` 또는 생략 시 디렉터리에 적용) |
| `X` | 디렉터리이거나 이미 누군가에게 실행 권한이 있을 때만 실행 권한 부여(대량 재귀 적용 시 유용) |

### chmod — 재귀·심볼릭 링크 옵션

| 옵션 | 설명 |
|------|------|
| `-R`, `--recursive` | 디렉터리 안까지 재귀적으로 적용 |
| `-H` | 명령줄에 직접 지정한 인자가 디렉터리를 가리키는 심볼릭 링크면 그 안까지 순회 |
| `-L` | 순회 도중 만나는 모든 디렉터리 심볼릭 링크를 따라 들어감 |
| `-P` | 심볼릭 링크를 절대 따라가지 않음(GNU chmod의 기본값) |

### chown — 소유자·그룹 변경

| 형식 | 의미 |
|------|------|
| `chown user file` | 소유자만 변경 |
| `chown user:group file` | 소유자와 그룹을 함께 변경 |
| `chown :group file` (또는 `chgrp group file`) | 그룹만 변경 |
| `chown -R user:group dir/` | 디렉터리와 하위 항목 전체의 소유자·그룹 변경 |

`chown`도 `-R`/`-H`/`-L`/`-P`를 chmod와 동일한 의미로 지원하며, 추가로 심볼릭 링크 자체의 소유권(링크를 따라가지 않고)을 바꾸는 `-h`, `--no-dereference` 옵션이 있다.

## 예시

### chmod 기본

```bash
# 소유자·그룹·기타 모두에게 읽기+실행, 소유자만 쓰기까지 (rwxr-xr-x)
chmod 755 script.sh

# 기존 권한은 유지한 채 소유자에게 실행 권한만 추가
chmod u+x deploy.sh

# 그룹과 기타 사용자의 쓰기 권한을 제거
chmod go-w config.yml

# 디렉터리 하위 파일 전체를 읽기 전용으로 (재귀)
chmod -R 644 dist/
```

### chmod 특수 권한 비트

```bash
# setuid 설정: 이 실행 파일은 항상 소유자 권한으로 실행된다 (예: passwd)
chmod u+s /usr/local/bin/tool
chmod 4755 /usr/local/bin/tool

# setgid 설정: 디렉터리 안에 새로 생성되는 파일이 부모 디렉터리 그룹을 상속
chmod g+s shared_dir/
chmod 2775 shared_dir/

# sticky bit 설정: /tmp처럼 누구나 쓸 수 있어도 자기 파일만 삭제 가능
chmod +t /shared/tmp
chmod 1777 /shared/tmp
```

### chown 기본

```bash
# 소유자만 변경
chown deploy app.log

# 소유자와 그룹을 함께 변경
chown www-data:www-data /var/www/html

# 그룹만 변경 (chown과 chgrp 두 방법)
chown :developers project/
chgrp developers project/

# 배포 디렉터리 전체를 서비스 계정 소유로 재귀 변경
chown -R deploy:deploy /var/app
```

### 조합

```bash
# 권한과 소유권을 함께 정리해 배포 스크립트 실행 준비
chown deploy:deploy deploy.sh && chmod u+x deploy.sh

# 심볼릭 링크는 그대로 두고 링크가 가리키는 실제 파일 소유자만 변경(기본 동작)
chown deploy target_file

# 심볼릭 링크 자체의 소유권만 변경(-h)
chown -h deploy symlink_to_file
```

## 주의사항·함정

**소유자 변경은 보통 root만 할 수 있다.** POSIX는 `_POSIX_CHOWN_RESTRICTED`라는 옵션으로 이를 규정하는데, 리눅스를 포함한 대부분의 시스템이 이를 적용해 일반 사용자는 자기가 소유한 파일이라도 다른 사용자에게 소유권을 넘길 수 없다. 만약 아무나 자기 파일을 남에게 chown할 수 있다면, 디스크 사용량 할당량(quota)을 다른 사용자 명의로 떠넘기거나, 파일을 root 소유로 바꾼 뒤 setuid 비트를 노려 권한 상승을 시도하는 경로가 열리기 때문이다. 반면 그룹 변경은 상대적으로 완화되어 있어, 소유자는 자신이 이미 속한 그룹으로는 `chown :group`(또는 `chgrp`)을 root 없이도 실행할 수 있다.

**재귀 적용 시 심볼릭 링크를 따라갈지는 옵션으로 명시해야 한다.** `chmod -R`과 `chown -R`은 기본적으로(`-P`) 심볼릭 링크를 따라가지 않는다. 디렉터리 트리 안에 다른 위치를 가리키는 심볼릭 링크가 섞여 있을 때 `-L`(모든 디렉터리 심볼릭 링크를 따라 들어감)을 무심코 켜면, 의도치 않게 트리 바깥의 디렉터리까지 권한·소유권이 바뀔 수 있다. `-H`는 명령줄에 직접 지정한 인자가 심볼릭 링크일 때만 따라가고 순회 중 만나는 링크는 따라가지 않는다는 점에서 `-L`과 다르다. `chown`에는 추가로 `-h`(`--no-dereference`) 옵션이 있어, 순회 방식과 별개로 "심볼릭 링크 자체"의 소유권을 바꿀지 "링크가 가리키는 대상"의 소유권을 바꿀지도 따로 지정할 수 있다.

**setuid/setgid 비트는 안전을 위해 자동으로 해제될 수 있다.** 실행 파일의 소유자나 그룹을 일반 사용자 권한으로 `chown`/`chmod`하면, 커널이 그 파일의 setuid·setgid 비트를 자동으로 지운다(`chown(2)` 매뉴얼에 명시된 동작). 이는 이미 setuid가 걸린 실행 파일의 소유권이 바뀌는 틈을 타 권한 상승 공격이 성립하는 것을 막기 위한 안전장치다. 그래서 setuid를 다시 켜려면 소유권 변경 뒤에 `chmod u+s`를 별도로 다시 실행해야 하는 경우가 많다.

**setuid·setgid·sticky bit는 강력한 만큼 남용하면 보안 위험이 된다.** setuid가 걸린 실행 파일은 실행한 사용자가 누구든 파일 소유자(흔히 root) 권한으로 동작하므로, 검증되지 않은 바이너리에 함부로 걸어두면 그 자체가 권한 상승 통로가 된다. 시스템에 이미 setuid/setgid가 걸린 실행 파일이 있는지 점검할 때는 `find / -perm -4000 -o -perm -2000` 같은 조합을 쓴다(자세한 `find` 조건 검색은 다음 장에서 다룬다).

**`umask`는 새로 생성되는 파일의 기본 권한을 결정한다.** `chmod`가 이미 존재하는 파일의 권한을 바꾸는 명령이라면, `umask`는 "앞으로 새로 만들어질 파일·디렉터리의 기본 권한에서 어떤 비트를 빼고 시작할지"를 정하는 셸 설정값이다. 파일은 기본 666(rw-rw-rw-), 디렉터리는 기본 777(rwxrwxrwx)에서 `umask` 값만큼 비트를 뺀 권한으로 생성된다 — 흔한 `umask 022`는 그룹·기타의 쓰기 권한(0-2=... 022의 각 자리를 666/777에서 빼는 방식)을 빼서, 새 파일이 644(rw-r--r--), 새 디렉터리가 755(rwxr-xr-x)로 만들어지게 한다. `umask` 자체를 바꾸는 것은 이 장의 범위를 넘지만, "왜 새로 만든 파일마다 매번 `chmod`를 실행하고 있다면 `umask` 설정을 먼저 의심하라"는 점은 기억해 둘 만하다.

## 흔한 오개념

**"디렉터리 권한에서 실행(x) 비트는 파일 실행과 같은 의미다"는 착각이다.** 디렉터리에서 x는 "이 디렉터리 안으로 들어가 이름을 알고 있는 항목에 접근할 수 있는가"(탐색 권한)를 뜻하고, r은 "`ls`로 디렉터리 안의 항목 목록을 볼 수 있는가"를 뜻한다. 이 둘은 독립적이라, x만 있고 r이 없는 디렉터리는 정확한 파일명을 알면 `cat dir/secret.txt`로 접근할 수 있지만 `ls dir/`로 목록은 볼 수 없다 — 반대로 r만 있고 x가 없으면 파일 이름은 보이지만 그 안으로 들어가거나 파일을 열 수는 없다.

**"권한 문제가 생기면 일단 777로 풀고 본다"는 임시방편은 문제를 진단하는 대신 숨긴다.** `chmod 777`은 소유자·그룹·기타 모두에게 읽기·쓰기·실행 권한을 전부 열어주므로, 웹 서버 프로세스가 파일을 못 읽는 문제든 배포 스크립트가 디렉터리에 못 쓰는 문제든 일단 에러는 사라지지만, 그 파일이 왜 원래 권한으로 접근이 안 됐는지(소유자가 다른가, 그룹 멤버십이 빠졌는가)는 그대로 남는다. 실무에서는 "누가 실제로 이 파일에 접근해야 하는가"를 먼저 확인해 필요한 최소 권한만 열고, 소유자·그룹이 잘못됐다면 `chmod`가 아니라 `chown`으로 근본 원인을 고치는 것이 맞는 순서다.

## 다음 장에서는

[37장: find](/post/bashshell/find-command-search-files-conditions-linux/)에서는 조건에 맞는 파일을 트리 전체에서 찾아내는 법을 다룬다. 이 장에서 배운 `chmod`/`chown`을 `find ... -exec` 뒤에 붙이면, "권한이 644가 아닌 파일만 골라 고치기" 같은 작업을 한 번에 자동화할 수 있다.

## 평가 기준

- 권한(`chmod`)과 소유권(`chown`)이 커널 안에서 서로 독립적인 축이라는 점을 설명할 수 있다.
- 8진수 모드와 기호 모드로 같은 권한 변경을 표현하고, 상황에 따라 어느 쪽이 더 안전한지 선택할 수 있다.
- `-R` 재귀 적용 시 `-H`/`-L`/`-P`가 심볼릭 링크를 다르게 처리한다는 점과 `chown -h`의 역할을 구분할 수 있다.
- setuid/setgid/sticky bit가 무엇을 하는지, 그리고 일반 사용자가 소유권을 바꾸면 왜 이 비트가 자동으로 해제될 수 있는지 설명할 수 있다.
- 소유자 변경이 왜 보통 root로 제한되는지 설명하고, `chmod 777` 같은 임시방편 대신 근본 원인(소유자·그룹)을 진단할 수 있다.

## 참고

- [chmod(1) - Linux manual page](https://man7.org/linux/man-pages/man1/chmod.1.html)
- [chown(1) - Linux manual page](https://man7.org/linux/man-pages/man1/chown.1.html)
- [chown(2) - Linux manual page (시스템 호출, setuid/setgid 해제 동작)](https://man7.org/linux/man-pages/man2/chown.2.html)
- [chmod - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/chmod.html)
- [chown - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/chown.html)
