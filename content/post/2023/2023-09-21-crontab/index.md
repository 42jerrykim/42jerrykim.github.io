---
image: "wordcloud.png"
description: "리눅스 Crontab의 정의와 crond 데몬 역할, crontab -e/-l/-r 사용법, 5필드 표현식(분·시·일·월·요일), 특수문자와 스케줄 예제, 로그·백업·@reboot 활용, Anacron·systemd 타이머·Windows 작업 스케줄러 비교까지 150자 요약."
date: "2023-09-21T00:00:00Z"
lastmod: "2026-03-17"
header:
  teaser: /assets/images/2023/crontab.png
title: "[Linux] Crontab 사용법 — 예약 작업 편집·스케줄·로그·백업"
categories:
  - Linux
tags:
  - Linux
  - 리눅스
  - Automation
  - 자동화
  - Bash
  - Shell
  - 셸
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Reference
  - 참고
  - DevOps
  - Deployment
  - 배포
  - Monitoring
  - 모니터링
  - Configuration
  - 설정
  - Documentation
  - 문서화
  - Best-Practices
  - Troubleshooting
  - 트러블슈팅
  - Workflow
  - 워크플로우
  - Productivity
  - 생산성
  - Open-Source
  - 오픈소스
  - How-To
  - Tips
  - Technology
  - 기술
  - Web
  - 웹
  - Backend
  - 백엔드
  - File-System
  - Process
  - Error-Handling
  - 에러처리
  - Logging
  - 로깅
  - Quick-Reference
  - Cheatsheet
  - 치트시트
  - Terminal
  - 터미널
  - Windows
  - 윈도우
  - Cloud
  - 클라우드
  - Performance
  - 성능
  - Implementation
  - 구현
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Maintainability
  - Case-Study
  - 실습
  - Beginner
  - Education
  - 교육
  - Blog
  - 블로그
  - Markdown
  - 마크다운
  - Networking
  - 네트워킹
  - OS
  - 운영체제
  - Migration
  - 마이그레이션
  - Career
  - 커리어
  - Innovation
  - 혁신
  - Review
  - 리뷰
  - Git
  - GitHub
  - Database
  - 데이터베이스
  - Security
  - 보안
  - Comparison
  - 비교
  - Self-Hosted
  - 셀프호스팅
  - History
  - 역사
  - Science
  - 과학
  - Agile
  - 애자일
  - Deep-Dive
---

소프트웨어 개발과 시스템 운영에서 **자동화**는 반복 작업을 줄이고 일관된 실행을 보장하는 핵심 요소다. 리눅스에서는 **Crontab**을 통해 특정 시각·주기로 명령·스크립트를 예약할 수 있다. 이 글에서는 Crontab의 정의, 기본 사용법(편집·보기·삭제), 5필드 표현식과 스케줄 옵션, 로그·백업·`@reboot` 활용, FAQ, 그리고 Anacron·systemd 타이머·Windows 작업 스케줄러와의 비교까지 다룬다.

|![/assets/images/2023/crontab.png](/assets/images/2023/crontab.png)|
|:---:|
|Crontab 규칙 요약|

## Crontab이란

**Crontab**은 사용자가 **시간 기반 예약 작업(cron job)** 을 등록·편집·조회·삭제할 수 있게 해 주는 인터페이스다. 실제로 주기적으로 작업을 실행하는 것은 **crond** 데몬(서비스)이다. crond는 시스템에 상주하며 crontab에 등록된 시각이 되면 해당 줄의 명령을 실행한다. Windows의 **작업 스케줄러(Task Scheduler)** 와 개념이 비슷하다.

- **cron 파일 위치**: 사용자별 crontab은 보통 `/var/spool/cron/crontabs/`(Debian/Ubuntu) 또는 `/var/spool/cron/`(RHEL/CentOS) 등에 사용자명으로 저장된다. **직접 이 파일을 편집하지 말고** 반드시 `crontab` 명령으로만 수정해야 한다.
- **적합한 용도**: 매일 백업, 로그 로테이션, 주기적인 패키지 업데이트, 디스크 사용량 체크 등 **최소 1분 단위**로 반복되는 작업에 적합하다. 1분 미만 간격이 필요하면 다른 도구(예: systemd 타이머, 스크립트 루프)를 고려해야 한다.

아래 Mermaid 다이어그램은 사용자가 crontab을 편집한 뒤 crond가 작업을 실행하기까지의 흐름을 단순화한 것이다.

```mermaid
flowchart LR
  subgraph userSide["사용자"]
    A[사용자]
    B["crontab -e 편집"]
    C["crontab 파일 저장"]
  end
  subgraph daemonSide["시스템"]
    D[crond 데몬]
    E["스케줄 매칭"]
    F["명령 실행"]
  end
  A --> B
  B --> C
  C -->|"파일 갱신"| D
  D --> E
  E -->|"시각 일치"| F
```

- 노드 ID: `userSide`, `daemonSide`, `A`~`F` (예약어 미사용).
- 라벨에 특수문자·등호가 있는 엣지는 `"파일 갱신"`, `"시각 일치"`처럼 큰따옴표로 감쌌다.

## 기본 사용법

### crontab 명령 요약

| 옵션 | 설명 |
|------|------|
| `crontab -e` | 현재 사용자의 crontab을 편집(기본 편집기 사용). 저장 후 자동 반영 |
| `crontab -l` | 현재 사용자의 crontab 내용 나열 |
| `crontab -r` | 현재 사용자의 crontab 전체 삭제(모든 예약 작업 제거) |
| `crontab -u 사용자명 -e` | 지정 사용자의 crontab 편집(root 등 권한 필요) |
| `crontab -i -r` | 삭제 전 확인 프롬프트 |

### 크론탭 항목 편집하기

편집 시에는 `crontab -e`를 사용한다. `VISUAL` 또는 `EDITOR` 환경 변수에 설정된 편집기(예: vi, nano)로 crontab 파일이 열린다. 한 줄이 하나의 예약 작업이며, 형식은 다음과 같다.

```
* * * * * 명령
```

앞의 다섯 필드는 **분(0–59), 시(0–23), 일(1–31), 월(1–12), 요일(0–7)** 이며, 공백으로 구분한다. 요일에서 **0과 7은 일요일**이다.

예: 매일 오전 8시에 실행하려면

```
0 8 * * * /path/to/your/command
```

저장 후 편집기를 종료하면 crond가 변경 사항을 반영한다.

### 크론탭 항목 보기·삭제

- **보기**: `crontab -l` 로 현재 사용자의 crontab 전체를 출력한다.
- **삭제**: 특정 줄만 지우려면 `crontab -e` 로 해당 줄을 수동 삭제한다. **전체 삭제**는 `crontab -r` (확인 없음) 또는 `crontab -i -r` (확인 후 삭제)를 사용한다.

삭제·수정 후에는 반드시 `crontab -l` 로 결과를 확인하는 것이 안전하다.

## 스케줄 표현식(5필드)

필드 순서와 허용 값, 자주 쓰는 특수문자를 정리하면 아래와 같다.

| 필드 | 의미 | 허용 값 | 특수문자 예 |
|------|------|---------|-------------|
| 1 | 분 | 0–59 | `*` `,` `-` `/` |
| 2 | 시 | 0–23 | 동일 |
| 3 | 일 | 1–31 | 동일 |
| 4 | 월 | 1–12 | 동일 |
| 5 | 요일 | 0–7 (0,7=일요일) | 동일 |

- `*`: 해당 필드의 모든 값(매분/매시/매일 등).
- `,`: 나열 (예: `1,15` → 1일과 15일).
- `-`: 범위 (예: `9-17` → 9시~17시).
- `/`: 간격 (예: `*/15` → 15분마다, `0-30/10` → 0,10,20,30분).

### 매분 실행

```
* * * * * /usr/local/bin/check.sh
```

### 특정 시각 실행

매일 오전 9시 30분:

```
30 9 * * * /usr/local/bin/daily-report.sh
```

### 범위 실행

오전 9시부터 오후 5시까지 매시 정각:

```
0 9-17 * * * /usr/local/bin/hourly-task.sh
```

### 간격 실행

15분마다:

```
*/15 * * * * /usr/local/bin/poll.sh
```

### 특수 키워드(일부 구현)

| 키워드 | 의미 | 대략적인 표현식 |
|--------|------|------------------|
| `@reboot` | 부팅 시 1회 실행 | — |
| `@yearly` / `@annually` | 매년 1월 1일 0시 | `0 0 1 1 *` |
| `@monthly` | 매월 1일 0시 | `0 0 1 * *` |
| `@weekly` | 매주 일요일 0시 | `0 0 * * 0` |
| `@daily` / `@midnight` | 매일 0시 | `0 0 * * *` |
| `@hourly` | 매시 0분 | `0 * * * *` |

배포판·버전에 따라 지원 여부가 다르므로 `man 5 crontab` 으로 확인하는 것이 좋다.

## Crontab 사용 팁

### 한 줄에 하나의 명령

한 줄에 하나의 예약만 두면 가독성과 유지보수가 쉬워진다. 여러 명령을 묶으려면 스크립트로 만들고 그 스크립트 한 개만 cron에 등록하는 방식을 권장한다.

### 주석 활용

`#` 부터 줄 끝까지 주석이다. 작업 목적·담당·변경 이력을 주석으로 남기면 나중에 이해하기 쉽다.

```
# 매일 새벽 2시 DB 백업
0 2 * * * /opt/scripts/backup-db.sh
```

### 출력 비활성화

cron 작업에서 stdout/stderr가 나가면 기본적으로 메일로 전송될 수 있다. 메일이 필요 없으면 `/dev/null` 로 리디렉션한다.

```
0 2 * * * /usr/bin/backup.sh > /dev/null 2>&1
```

### 파일에 출력·로그 저장

표준 출력과 표준 에러를 모두 로그 파일로 남기려면:

```
0 2 * * * /usr/bin/backup.sh >> /var/log/backup.log 2>&1
```

`>>` 는 추가, `>` 는 덮어쓰기다. 로그가 무한히 쌓이지 않도록 **logrotate** 등으로 로테이션하는 것이 좋다.

### @reboot — 부팅 시 1회 실행

시스템이 부팅된 직후 한 번만 실행하려면:

```
@reboot /opt/scripts/startup.sh
```

부팅 후 몇 분 뒤에 실행하고 싶다면 `sleep` 을 조합할 수 있다(구현에 따라 동작 여부가 다를 수 있음).

```
@reboot sleep 300 && /opt/scripts/delayed-start.sh
```

## 활용 예시

### 시스템 유지 관리

매일 새벽에 패키지 목록 갱신 및 자동 보안 업데이트(배포판에 맞는 명령 사용):

```
0 3 * * * apt update && apt upgrade -y
```

### 디스크 사용량 모니터링

매시 정각에 디스크 사용량을 체크하는 스크립트 실행:

```
0 * * * * /opt/scripts/check-disk.sh
```

스크립트 안에서 임계값 초과 시 알림(메일, 슬랙 등)을 보내도록 구현할 수 있다.

### 예약 백업

매일 새벽 3시에 DB·파일 백업 스크립트 실행:

```
0 3 * * * /opt/scripts/full-backup.sh
```

백업 스크립트는 경로·권한·저장소를 명확히 하고, 실패 시 로그에 남기거나 알림을 보내는 것이 좋다.

## FAQ

### 크론탭 작업의 출력을 로그 파일에 남기는 방법은?

명령 끝에 `>> /path/to/logfile.log 2>&1` 를 붙이면 stdout과 stderr가 해당 파일에 추가된다.

```
* * * * * /usr/bin/myjob.sh >> /var/log/myjob.log 2>&1
```

로그 로테이션(logrotate) 설정을 함께 두면 디스크가 가득 차는 것을 방지할 수 있다.

### 크론탭 항목은 어떻게 백업하나요?

현재 사용자 crontab을 파일로 저장:

```bash
crontab -l > crontab_backup.txt
```

다른 사용자(root 권한 필요):

```bash
sudo crontab -u otheruser -l > otheruser_crontab_backup.txt
```

복원 시:

```bash
crontab crontab_backup.txt
```

백업 자체도 cron으로 정기 실행할 수 있다(예: 매일 23시 50분).

```
50 23 * * * crontab -l > /home/backup/crontab_$(date +\%Y\%m\%d).txt
```

(퍼센트 기호 `%`는 crontab 안에서는 이스케이프(`\%`) 해 주는 것이 안전하다.)

## 관련 기술

Crontab은 1분 단위·고정 시각 실행에 적합하다. 아래는 요구 사항에 따라 고려할 수 있는 대안이다.

### Anacron

시스템이 24시간 켜져 있지 않아도 **지난 실행을 보완**해 주는 도구다. 예를 들어 “매일 실행”이었는데 그날 전원이 꺼져 있으면, 다음 부팅 후에 한 번 실행해 준다. 랩톱·데스크톱처럼 항상 켜 두지 않는 환경에서 유용하다.

### Systemd 타이머

systemd를 쓰는 리눅스에서는 **systemd timer** 로 단위 서비스 실행 시각·간격을 정의할 수 있다. 캘린더식·초 단위 지정, 실패 시 재시도, 의존성 관리 등이 가능해 복잡한 스케줄이나 서비스 연동에 적합하다.

### Windows 작업 스케줄러(Task Scheduler)

Windows에서 cron과 유사한 역할을 한다. GUI로 작업을 만들고, 트리거(시각·이벤트)·동작(실행할 프로그램)·조건을 설정할 수 있다. 리눅스의 crontab + 일부 systemd 타이머 기능을 조합한 것과 비슷하다.

## 결론

- **Crontab**은 리눅스에서 **시간 기반 예약 작업**을 등록·관리하는 표준 방식이다. `crontab -e` 로 편집, `crontab -l` 로 확인, `crontab -r` 로 전체 삭제한다.
- **5필드 표현식**(분·시·일·월·요일)과 `*` `,` `-` `/` 조합으로 다양한 주기를 표현할 수 있다.
- **한 줄에 하나의 작업**, **주석 활용**, **출력은 `/dev/null` 또는 로그 파일로 리디렉션**, **정기 백업**을 습관화하면 운영이 안정적이다.
- 1분 미만 주기·부팅 후 보완 실행·복잡한 의존성이 필요하면 **systemd 타이머**, **Anacron**, **Windows 작업 스케줄러** 등 대안을 검토하면 된다.

Crontab을 잘 활용하면 반복 작업을 자동화하고, 서버·개발 환경의 운영 효율을 높일 수 있다.

## Reference

- [리눅스 크론탭(Linux Crontab) 사용법 — JDM's Blog](https://jdm.kr/blog/2)
- [crontab 사용법 알아보기 (크론탭, 옵션, 스케쥴러 예제) — iamfreeman 티스토리](https://iamfreeman.tistory.com/entry/crontab-%EC%82%AC%EC%9A%A9%EB%B2%95-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0-%ED%81%AC%EB%A1%A0%ED%83%AD-%EC%98%B5%EC%85%98-%EC%8A%A4%EC%BC%80%EC%A5%B4%EB%9F%AC)
- [리눅스 크론탭(Linux Crontab) 시간설정 표현식 정리 — danmilife 티스토리](https://danmilife.tistory.com/4)
