---
title: "Linux User Management 기초"
date: 2024-02-17T10:00:00+09:00
draft: false
categories:
  - Linux
  - Shell
tags:
  - Linux
  - User Management
  - Shell Command
---

Linux system에서 user management는 system 관리의 핵심적인 부분이다. 이 글에서는 Linux user management의 기본적인 개념과 명령어들을 살펴보겠다.

## User 정보가 저장되는 위치

Linux system에서 user 정보는 다음 파일들에 저장된다:

- `/etc/passwd`: user account 정보
- `/etc/shadow`: user password 정보
- `/etc/group`: group 정보

## User 관련 기본 명령어

### 1. User 생성 (useradd)

새로운 user를 생성하는 기본 명령어는 다음과 같다:

```bash
sudo useradd username
```

주요 옵션:
- `-m`: home 디렉토리 생성
- `-s`: shell 지정
- `-G`: 보조 group 지정

예시:
```bash
sudo useradd -m -s /bin/bash newuser
```

### 2. Password 설정 (passwd)

User의 password를 설정하거나 변경할 때 사용한다:

```bash
sudo passwd username
```

### 3. User 정보 수정 (usermod)

기존 user의 속성을 변경할 때 사용한다:

```bash
sudo usermod [options] username
```

주요 옵션:
- `-l`: username 변경
- `-G`: group 추가
- `-s`: shell 변경

### 4. User 삭제 (userdel)

User를 system에서 제거할 때 사용한다:

```bash
sudo userdel username
```

주요 옵션:
- `-r`: home 디렉토리와 mail spool 함께 삭제

### 5. User 정보 조회

현재 user 정보를 확인하는 명령어들:

```bash
# 현재 user 확인
whoami

# user ID 확인
id username

# user 목록 확인
cat /etc/passwd
```

## Group 관리

### 1. Group 생성 (groupadd)

```bash
sudo groupadd groupname
```

### 2. Group 삭제 (groupdel)

```bash
sudo groupdel groupname
```

### 3. Group 수정 (groupmod)

```bash
sudo groupmod [options] groupname
```

## 권한 관리

Linux에서 file과 directory의 권한은 다음과 같이 관리된다:

- Read (r): 4
- Write (w): 2
- Execute (x): 1

권한 변경 명령어:
```bash
# 파일 권한 변경
chmod [permissions] filename

# 소유자 변경
chown user:group filename
```

## 보안 고려사항

1. 강력한 password 정책 적용
2. 최소 권한 원칙 준수
3. 정기적인 user 계정 감사
4. sudo 권한 제한적 부여
5. 불필요한 user 계정 제거

## 결론

Linux system에서 user management는 system 보안과 관리의 기본이다. 위에서 설명한 기본적인 명령어들을 이해하고 적절히 활용하면 효과적인 system 관리가 가능하다. 







## 리눅스 시스템의 사용자 관리 체계에 대한 종합적 고찰

리눅스 시스템은 다중 사용자 환경을 지원하는 운영체제로서 사용자 관리 체계가 시스템 보안과 자원 관리의 핵심 요소로 작동한다. 본 연구는 UID(User Identity) 기반의 계층적 권한 구조부터 현대적인 인증 모듈 통합에 이르기까지 리눅스 사용자 관리 시스템의 전반적인 아키텍처를 체계적으로 분석한다. 특히 시스템 계정과 일반 사용자의 상호작용, 그룹 기반 접근 제어 메커니즘, PAM(Pluggable Authentication Modules)을 활용한 확장형 보안 프레임워크를 집중적으로 조명한다.

## 1. 리눅스 사용자 식별 체계의 구조적 특성

### 1.1 UID 체계의 계층적 분류
리눅스 커널은 사용자 식별을 위해 UID(User Identity)라는 고유한 정수 값을 할당하며, 이 값은 프로세스 실행 권한과 파일 시스템 접근 제어의 근간이 된다[1]. UID 0은 슈퍼유저(root)에게 예약되어 있으며 모든 시스템 자원에 대한 무제한 접근 권한을 부여한다. 일반 사용자 UID는 배포판별로 상이한 할당 전략을 보이는데, 레드햇 계열은 500번대부터 데비안 계열은 1000번대부터 순차적 할당이 이루어진다[1].

시스템 계정의 경우 일반적으로 1-499(레드햇) 또는 1-999(데비안) 범위의 UID가 부여되며, 이러한 계정은 주로 데몬 프로세스 실행이나 특정 서비스 운영을 위해 자동 생성된다[1]. 예를 들어 httpd 서비스는 일반적으로 apache 사용자로 실행되어 웹 서버 프로세스의 권한 범위를 제한한다. 이러한 설계는 최소 권한 원칙(Principle of Least Privilege)을 구현하여 잠재적 보안 위협을 완화한다.

### 1.2 계정 정보 저장 구조
사용자 계정 정보는 /etc/passwd 파일에 텍스트 형식으로 저장되며 각 필드는 콜론(:)으로 구분된다[2]. 저장 형식은 `username:password:UID:GID:comment:home_directory:shell` 구조를 가지며, 역사적 경위로 인해 암호화된 비밀번호는 /etc/shadow 파일로 분리 관리된다[2]. 이중화 저장 체계는 1980년대 이후로 지속된 보안 강화 조치의 결과물로서, shadow 파일은 루트 권한자만 접근 가능하도록 퍼미션이 설정된다.

/etc/passwd 파일의 각 레코드에서 password 필드는 'x'로 표기되며, 이는 실제 암호 해시가 /etc/shadow에 별도 저장됨을 의미한다[2]. shadow 파일은 비밀번호의 마지막 변경일, 만료 기간, 비활성 기간 등의 추가 메타데이터를 포함하여 계정 수명 주기 관리를 지원한다. 예를 들어, `kuki:$6$MViHlkf0YW.EY5iW$xvVtiHuKRCcbSO4wuk8SFGKR0VhjlY37bEZj0A6GHDinMdO1GPOqiP4C/W6Ad7NQYcfY4EDOdfyhdkB4lIEvv0:18998:0:99999:7:::` 형식의 엔트리는 SHA-512 해시 알고리즘을 사용한 비밀번호 저장 방식을 보여준다[2].

## 2. 사용자 생명주기 관리 프로토콜

### 2.1 계정 생성 메커니즘
useradd 명령어는 새로운 사용자 계정을 생성하는 표준 인터페이스로서, 시스템 관리자가 -d, -m, -g 등의 옵션을 통해 홈 디렉터리 위치, 기본 그룹 지정, 스켈레톤 파일 복사 등을 제어할 수 있다[1]. Red Hat 계열과 Debian 계열의 차이는 주로 홈 디렉터리 자동 생성 여부에 있으며, -m 플래그 사용 시 /etc/skel 디렉터리의 템플릿 파일들이 새로운 홈 디렉터리로 복제된다[1].

계정 생성 시 UID 자동 할당 알고리즘은 배포판별로 상이한데, 최신 시스템에서는 getent passwd 명령어를 통해 현재 사용 중인 UID 목록을 확인한 후 최소 미사용 값을 선택한다. 관리자는 -u 옵션으로 명시적 UID 지정이 가능하지만, 기존 UID와의 충돌 방지를 위해 유의해야 한다[1]. 다음은 사용자 생성의 전형적인 예시이다:

```bash
useradd -m -d /home/newuser -s /bin/bash -g developers newuser
```

이 명령어는 newuser 계정을 생성하며 홈 디렉터리를 /home/newuser에 배치하고 기본 셸을 bash로 지정하며 developers 그룹에 소속시킨다[1].

### 2.2 인증 정보 관리 체계
passwd 명령어는 사용자 비밀번호 설정 및 변경을 담당하며, 암호화된 해시 값을 /etc/shadow 파일에 저장한다[1]. 비밀번호 정책은 /etc/login.defs 파일에서 정의되며, 최소 길이, 최대 유효 기간, 복잡성 요구사항 등을 설정할 수 있다[2]. PAM(Pluggable Authentication Modules) 구성 파일(/etc/pam.d/passwd)을 수정하여 추가적인 비밀번호 강도 검증 규칙을 적용할 수 있다.

chage 명령어는 계정 만료 정책을 세부적으로 제어하는 도구로서, -M 옵션으로 최대 사용 일수, -E 옵션으로 절대 만료일을 지정할 수 있다[2]. 예를 들어 `chage -M 90 -E 2025-12-31 newuser`는 newuser 계정의 비밀번호를 90일마다 변경하도록 강제하며 2025년 말에 계정을 만료시킨다[2].

## 3. 권한 상승 및 전환 메커니즘

### 3.1 su 명령어의 작동 원리
substitute user(su) 명령어는 현재 세션에서 다른 사용자의 권한으로 셸을 실행할 수 있게 해주며, 주로 root 권한 획득에 사용된다[1]. 옵션 없이 실행할 경우 환경 변수가 현재 사용자의 설정을 유지하지만, -l 또는 - 옵션 사용 시 대상 사용자의 로그인 스크립트를 완전히 실행한다[1]. 이 차이는 중요한 보안 함의를 가지는데, 예를 들어 root로의 전환 시 - 옵션을 생략하면 PATH 환경변수가 제대로 설정되지 않아 악성 스크립트 실행 위험이 증가할 수 있다.

su 명령어의 작동 로그는 /var/log/secure 파일에 기록되며, 이는 사후 감사(audit)를 위해 반드시 모니터링해야 할 항목이다[4]. 다음은 su 명령어의 전형적인 사용 예시이다:

```bash
su - root -c "apt-get update"
```

이 명령어는 root 권한으로 apt-get update를 일회성 실행하며, 명령어 완료 후 자동으로 원래 사용자 세션으로 복귀한다[1].

### 3.2 sudo 권한 위임 시스템
sudo(superuser do)는 특정 명령어에 대해 사전 정의된 권한을 위임하는 시스템으로, /etc/sudoers 파일을 통해 구성된다[4]. visudo 명령어로 이 파일을 수정해야 하며, 문법 오류 방지를 위해 구문 검증 기능이 내장되어 있다. 사용자별 또는 그룹별로 허용된 명령어, 인자 제한, 비밀번호 요구 여부 등을 세밀하게 설정할 수 있다.

일반적인 sudoers 엔트리 형식은 `user host=(runas) command` 구조를 가지며, 예를 들어 `newuser ALL=(root) /usr/bin/apt-get`은 newuser가 모든 호스트에서 root 권한으로 apt-get 명령어를 실행할 수 있도록 허용한다[4]. 현대 시스템에서는 wheel 그룹을 통해 관리자 권한을 그룹 단위로 관리하는 것이 권장된다.

## 4. 그룹 기반 접근 제어 모델

### 4.1 그룹 멤버십 관리 체계
리눅스에서 각 사용자는 최소 한 개의 기본 그룹(Primary Group)에 반드시 소속되어야 하며, 추가로 15개의 보조 그룹(Secondary Group)에 가입할 수 있다[2]. /etc/group 파일은 그룹명, GID, 멤버 목록을 저장하며, groupadd, groupmod, groupdel 명령어를 통해 관리된다[2]. 사용자의 그룹 멤버십 변경은 반드시 로그아웃 후 재로그인해야 적용되는 점에 유의해야 한다.

효율적인 권한 관리를 위해 프로젝트 단위 또는 역할 기반 그룹을 구성하는 것이 바람직하다. 예를 들어 웹 개발자 그룹(webdev)에 Apache 구성 파일에 대한 쓰기 권한을 부여하면 개별 사용자 관리 없이 그룹 단위로 접근 제어가 가능해진다[2]. 다음은 그룹 생성 및 사용자 추가 예시이다:

```bash
groupadd webdev
usermod -aG webdev newuser
```

### 4.2 파일 권한 상속 모델
파일 시스템의 접근 권한은 사용자-그룹-기타(other)의 3계층 모델로 작동하며, chmod 명령어를 통해 8진수 또는 기호 모드로 설정된다[2]. setgid 비트(2000)는 디렉터리 내 신규 파일이 부모 디렉터리의 그룹을 상속받도록 하여 협업 환경을 용이하게 한다. 예를 들어 공유 디렉터리에 setgid를 설정하면 모든 신규 파일이 해당 그룹 소유로 생성되어 구성원들의 접근성이 보장된다.

ACL(Access Control List)은 전통적인 UNIX 권한 모델을 확장하여 더 세분화된 접근 제어를 가능하게 한다. getfacl과 setfacl 명령어를 사용하면 특정 사용자나 그룹에게 개별 파일/디렉터리에 대한 사용자 정의 권한을 부여할 수 있다[2]. 이는 복잡한 권한 구조가 필요한 엔터프라이즈 환경에서 특히 유용하게 활용된다.

## 5. 계정 보안 강화 전략

### 5.1 root 계정 보호 메커니즘
root 계정의 직접 로그인 차단은 기본적인 보안 조치로서, /etc/ssh/sshd_config 파일에서 PermitRootLogin 값을 no로 설정하여 SSH 접근을 제한할 수 있다[4]. 대신 sudo를 통한 권한 상승을 권장하며, /etc/sudoers 파일에 `Defaults rootpw`를 설정하면 root 비밀번호 대신 사용자 본인의 비밀번호를 요구하도록 강제할 수 있다[4].

일정 시간 동안의 비활성 상태 후 자동 로그아웃을 구현하기 위해 /etc/profile에 TMOUT 변수를 설정할 수 있다[1]. 예를 들어 `export TMOUT=600`은 10분간의 활동 없을 시 세션을 종료한다. 이와 병행하여 pam_tally2 모듈을 구성하면 실패한 로그인 시도 횟수에 따라 계정을 잠그는 조치를 취할 수 있다[2].

### 5.2 PAM 통합 인증 프레임워크
PAM(Pluggable Authentication Modules)은 인증 과정을 모듈화하여 유연한 보안 정책 구현을 가능하게 한다[2]. /etc/pam.d 디렉터리의 구성 파일들은 로그인, sudo, su 등 다양한 인증 시나리오에 적용되는 모듈 스택을 정의한다. 예를 들어 암호 복잡성 요구사항은 pam_pwquality.so 모듈을 통해 강제하며, 다중 인증 요소 추가를 위해 pam_google_authenticator.so와 같은 타사 모듈을 통합할 수 있다.

PAM 설정 시 주의해야 할 점은 모듈 스택의 처리 유형(required, requisite, sufficient, optional)에 따라 인증 흐름이 달라진다는 것이다[2]. requisite 타입은 모듈 검증 실패 시 즉시 인증을 거부하는 반면, required 타입은 스택 내 모든 모듈을 평가한 후 최종 결정을 내린다. 이러한 미묘한 차이는 시스템 전체의 보안 수준에 중대한 영향을 미칠 수 있다.

## 6. 계정 감사 및 모니터링 체계

### 6.1 로그 분석 기법
/var/log/auth.log 파일(데비안 계열) 또는 /var/log/secure(레드햇 계열)는 모든 인증 관련 이벤트를 기록하는 핵심 로그 파일이다[4]. 이 파일을 모니터링하여 비정상적인 로그인 시도, sudo 권한 남용, 계정 생성/삭제 이력을 추적할 수 있다. fail2ban 같은 도구는 이러한 로그를 실시간 분석하여 반복적인 실패 시도를 차단하는 자동화된 방어 체계를 구축한다.

last 명령어는 /var/log/wtmp 파일을 파싱하여 최근 로그인 기록을 보여주며, lastb는 /var/log/btmp에서 실패한 시도 목록을 표시한다[4]. 이러한 도구들을 주기적으로 실행하여 미인가 접근 시도를 탐지하고 대응 조치를 취해야 한다. 예를 들어, `last -f /var/log/wtmp.1`은 이전 달의 로그인 기록까지 검토할 수 있다.

### 6.2 계정 활동 감사 도구
auditd 데몬은 커널 수준의 시스템 호출을 모니터링하여 상세한 감사 로그를 생성한다[4]. 사용자 계정 관련 규칙을 /etc/audit/rules.d/ 디렉터리에 정의하면, 예를 들어 passwd 파일 수정이나 useradd 명령어 실행 같은 중요한 이벤트를 추적할 수 있다. 생성된 로그는 ausearch 유틸리티로 필터링하여 특정 사용자의 활동 이력을 재구성할 수 있다.

Linux Audit Framework의 고급 설정을 통해 실시간 경고 시스템을 구축할 수 있다. 예를 들어, 다음 규칙은 root 계정의 su 시도를 감시한다:

```bash
-a always,exit -F arch=b64 -S execve -F path=/bin/su -F auid>=1000 -k privileged-priv_change
```

이 규칙은 su 명령어 실행 시 사용자 ID(auid)를 캡처하여 /var/log/audit/audit.log에 기록하며, 키워드 'privileged-priv_change'로 검색이 가능하다[4].

## 7. 결론 및 향후 전망

리눅스 사용자 관리 시스템은 50년 가까운 UNIX 전통을 계승하면서도 현대적인 보안 요구사항을 수용하기 위해 지속적으로 진화해왔다. 최근에는 RBAC(Role-Based Access Control)과 ABAC(Attribute-Based Access Control) 같은 고급 권한 관리 모델이 도입되면서 전통적인 UID/GID 체계를 보완하고 있다. 컨테이너 기술의 부상은 사용자 네임스페이스 구현을 촉진하여 호스트 시스템과 격리된 사용자 ID 매핑 체계를 가능하게 했다.

향후 발전 방향으로는 머신 러닝 기반의 이상 행동 탐지 시스템과 통합 인증 플랫폼(예: OAuth 2.0, OpenID Connect)과의 연동 강화가 예상된다. 또한, eBPF(extended Berkeley Packet Filter) 기술을 활용한 실시간 권한 사용 모니터링 시스템이 보안 강화에 기여할 것으로 전망된다. 시스템 관리자는 이러한 기술 동향을 주시하면서도 기본적인 사용자 관리 원칙을 견고히 이해해야 체계적인 보안 인프라를 구축할 수 있을 것이다.

Citations:
[1] https://velog.io/@gillog/Linux-%EC%82%AC%EC%9A%A9%EC%9E%90-%EA%B4%80%EB%A6%AC
[2] https://kukim.tistory.com/51
[3] https://circus7.tistory.com/5
[4] https://laughcryrepeat.tistory.com/59
[5] https://starrykss.tistory.com/1626
[6] https://www.runit.cloud/2020/12/Managing-Linux-user-accounts.html
[7] https://techplay.blog/%EC%B4%88%EB%B3%B4%EC%9E%90%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%84%9C%EB%B2%84-os-%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%9E%85%EB%AC%B8-%EC%95%88%EB%82%B4%EC%84%9C/
[8] https://withcoding.com/102
[9] https://pizza301.tistory.com/32
[10] https://jettstream.tistory.com/616
[11] https://leftday.tistory.com/92
[12] https://nkcnow.tistory.com/160
[13] https://takeknowledge.tistory.com/65
[14] https://inpa.tistory.com/entry/LINUX-%F0%9F%93%9A-%EC%82%AC%EC%9A%A9%EC%9E%90-%EA%B3%84%EC%A0%95-%EA%B4%80%EB%A6%AC-%EB%AA%85%EB%A0%B9%EC%96%B4-%F0%9F%92%AF-%EC%A0%95%EB%A6%AC
[15] https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/assembly_getting-started-with-managing-user-accounts_managing-users-and-groups
[16] https://blog.naver.com/hanajava/222933570476?viewType=pc
[17] https://wlsvud84.tistory.com/entry/%EB%A6%AC%EB%88%85%EC%8A%A4-User-Account-Management-useraddusermoduserdel
[18] https://93it-serverengineer.co.kr/101
[19] https://withcoding.com/101
[20] https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/8/html/configuring_basic_system_settings/assembly_getting-started-with-managing-user-accounts_managing-users-and-groups
[21] https://sailer.tistory.com/entry/%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%82%AC%EC%9A%A9%EC%9E%90-%EA%B4%80%EB%A6%AC-%EC%9C%A0%EC%A0%80%EC%B6%94%EA%B0%80-%EC%9C%A0%EC%A0%80%EC%82%AD%EC%A0%9C-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8-%EB%B3%80%EA%B2%BD
[22] https://blog.naver.com/jypit/221100878526
[23] https://virtualtech.tistory.com/74
[24] https://velog.io/@shawnhansh/Linux-Ubuntu%EC%97%90%EC%84%9C-%EA%B3%84%EC%A0%95-%EC%83%9D%EC%84%B1-%EC%82%AD%EC%A0%9C-%ED%95%98%EA%B8%B0
[25] https://velog.io/@jydecn4869/%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%83%9D%EC%84%B1-%EB%B0%8F-%EA%B4%80%EB%A6%AC
[26] https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/managing-users.html
[27] https://smallrich.tistory.com/80
[28] https://apro-developer.tistory.com/82
[29] https://www.leafcats.com/132
[30] https://ohaengsa.tistory.com/entry/Linux-%EC%82%AC%EC%9A%A9%EC%9E%90-%EA%B3%84%EC%A0%95-%EA%B4%80%EB%A6%AC-%EB%AA%85%EB%A0%B9%EC%96%B4-usermod
[31] https://takeknowledge.tistory.com/71
[32] https://thing-u.tistory.com/38
[33] https://docs.rockylinux.org/ko/books/admin_guide/06-users/
[34] https://hooongs.tistory.com/239
[35] https://velog.io/@gusdnr814/%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%82%AC%EC%9A%A9%EC%9E%90-%EB%B0%8F-%EA%B6%8C%ED%95%9C-%EA%B4%80%EB%A6%AC
[36] https://www.guru99.com/ko/linux-admin.html
[37] https://blog.naver.com/haejoon90/220736406478?viewType=pc