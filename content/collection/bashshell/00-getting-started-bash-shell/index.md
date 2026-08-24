---
draft: false
collection_order: 0
slug: getting-started-bash-shell
title: "[Bash Shell] 00. 과정 개요와 커리큘럼"
date: 2026-08-22
lastmod: 2026-08-22
description: "Bash Shell 44챕터 커리큘럼의 과정 개요. 셸이 개발자에게 근본 역량인 이유, 7개 Part 학습 순서의 설계 근거, 00-43장 전체 목차, 선수 지식과 완주 후 갖추는 실무 역량을 정리한 과정 개요 챕터다."
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Automation(자동화)
- File-System
- Process
- Pipeline
- System-Design
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Productivity(생산성)
- Beginner
- DevOps
- Networking(네트워킹)
- SSH(Secure Shell)
- Curriculum
- Command-Line
- Text-Processing
- Scripting
- POSIX
- GNU
- 커리큘럼
- 셸스크립팅
- 리눅스입문
- 텍스트처리
- 파이프라인
- 로드맵
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 챕터는 "Bash Shell" 컬렉션의 첫 챕터이므로 선행 챕터가 없다. 필요한 선수 지식은 이 장의 "선수 지식" 절에서 별도로 정리한다.

난이도는 입문(터미널을 처음 열어보는 수준)에서 중급(커리큘럼 전체 구조와 각 Part의 순서 논리를 판단할 수 있는 수준) 사이를 오간다. 특정 명령어의 옵션이나 실행 예시는 다루지 않는다. 이 장은 지도(map)이지 명령어 레퍼런스가 아니다.

이 장이 다루지 않는 것은 다음과 같다. `cd`·`ls`처럼 개별 명령어의 옵션과 예시는 [01장: cd, pwd](/post/bashshell/cd-pwd-change-directory-linux-commands/) 이후 각 번호 챕터에서 다룬다. 파이프라인·리다이렉션 같은 개념의 상세 동작 원리는 3부(19–22장)에서, 스크립트 작성 문법은 5부(27–35장)에서 각각 독립된 챕터로 다룬다. 이 장에서는 "왜 이런 순서로 배워야 하는가"와 "각 Part가 최종 역량에 어떻게 기여하는가"만 설명한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 터미널이 처음인 완전 초보자 | 전체를 순서대로 | 셸이 왜 필요한지, 어디서부터 시작해야 하는지 이해한다 |
| CMD/PowerShell 등 다른 커맨드라인 경험자 | 도입, 핵심 개념, 비교/트레이드오프 | 이미 아는 커맨드라인 개념이 Bash 생태계 어디에 대응하는지 파악한다 |
| 명령어를 몇 개 알고 레퍼런스를 찾으러 온 개발자 | 커리큘럼 전체 구성 표 | 자신이 아는 명령어가 몇 장인지, 비어 있는 지식(예: `trap`, 배열)이 무엇인지 확인한다 |
| 팀 온보딩·커리큘럼 설계자 | 커리큘럼 전체 구성 표, 비판적 시각 | 이 로드맵을 팀 교육 자료로 그대로 쓸 수 있는지, 어디를 보강해야 하는지 판단한다 |

## 도입

명령어를 무작위 순서로 익히면 지식에 구멍이 생기기 쉽다. `awk`를 이해하려면 먼저 파이프와 정규식 개념을 알아야 하고, `trap`이 왜 유용한지 온전히 이해하려면 함수와 종료 코드를 먼저 알아야 한다. 이 컬렉션은 44개 챕터를 명령어 사전순으로 나열하지 않고, 각 챕터가 이전 챕터의 지식을 전제하고 다음 챕터로 자연스럽게 이어지도록 하나의 학습 경로로 설계했다. 하드링크, `PATH` 탐색, 셸 설정 파일, `case`와 산술 연산, `read`, 배열, `trap`, 디스크 사용량 확인처럼 개별 명령어만 훑어서는 놓치기 쉬운 핵심 개념도 별도 챕터로 포함했다.

셸을 배우는 일은 특정 운영체제의 특기가 아니라 소프트웨어 개발 전반에 걸쳐 반복적으로 요구되는 기초 역량이다. 첫째, 자동화의 최소 단위가 셸이다. CI/CD 파이프라인의 빌드 스크립트, 배포 스크립트, cron으로 도는 정기 작업 대부분은 결국 셸 스크립트 위에서 돌아가며, 이를 이해하지 못하면 파이프라인이 실패했을 때 로그 한 줄도 스스로 해석할 수 없다. 둘째, 서버·컨테이너·클라우드 인스턴스 같은 원격 시스템을 운영하는 유일한 공통 인터페이스가 셸이다. GUI가 없는 리눅스 서버에 SSH로 접속했을 때 파일을 옮기고 프로세스를 죽이고 로그를 뒤지는 능력은 대체할 도구가 없다. 셋째, 텍스트 처리는 프로그래밍 언어를 가리지 않는 보편 기술이다. 로그 파일에서 에러 줄만 뽑아내고, CSV의 특정 열만 추출하고, 수백 개 파일에서 문자열을 한 번에 바꾸는 작업은 `grep`·`awk`·`sed`·`tr` 몇 줄이면 끝나지만, 셸을 모르면 매번 별도 스크립트 언어로 파서를 새로 짜야 한다. 이 세 가지가 이 컬렉션이 7개 Part로 나뉘는 이유이기도 하다 — 각 Part는 이 역량들을 순서대로 습득하도록 설계되어 있다.

## 핵심 개념

<strong>셸(Shell)</strong>은 사용자의 명령을 해석해 운영체제 커널에 전달하고, 그 결과를 다시 사용자에게 보여주는 프로그램이다. <strong>Bash(Bourne Again SHell)</strong>는 그중 리눅스·macOS를 포함한 대부분의 유닉스 계열 시스템에서 기본값으로 쓰이는 구현체다. 셸을 처음 배우는 사람이 가장 먼저 바꿔야 할 사고방식은 "명령어를 하나씩 외운다"가 아니라 "셸이 세상을 어떻게 보는가"를 이해하는 것이다. 유닉스 철학에서 모든 것은 <strong>텍스트 스트림</strong>이다. 파일의 내용, 명령의 출력, 프로세스 목록, 심지어 환경변수까지 셸 안에서는 결국 줄 단위 텍스트로 다뤄진다. 그리고 각 명령어는 "한 가지 일을 잘하는" 작은 필터로 설계되어 있어서, `|`(파이프)로 한 명령의 출력을 다른 명령의 입력으로 흘려보내면 복잡한 작업을 여러 개의 단순한 도구 조합으로 풀 수 있다.

이 정신 모델이 커리큘럼 순서를 결정한다. 파일과 디렉터리를 탐색하지 못하면(1부) 처리할 텍스트 자체를 찾을 수 없고, 텍스트를 다루는 도구(2부)를 모르면 파이프(3부)로 조합할 재료가 없다. 프로세스를 제어하는 법(4부)을 모르면 오래 걸리는 작업을 백그라운드로 돌리거나 멈춘 작업을 재개할 수 없고, 이 모든 것을 반복 가능한 절차로 자동화하려면 스크립팅 문법(5부)이 필요하다. 마지막으로 파일 시스템을 관리하고(6부) 원격 시스템까지 다루는 능력(7부)은 지금까지 배운 것을 로컬 환경을 넘어 실제 서버 운영으로 확장한다.

## 비교/트레이드오프

이 컬렉션을 활용하는 방식은 두 가지다. 아래 표는 그 두 방식의 장단점과 적합한 상황을 정리한 것이다.

| 구분 | 필요할 때 검색해서 익히기 | 커리큘럼을 순서대로 읽기 |
|---|---|---|
| 장점 | 당장 급한 문제를 가장 빠르게 해결한다 | 빠진 개념 없이 체계적으로 습득하고, 다음에 부딪힐 문제를 미리 대비한다 |
| 위험 | 이미 아는 명령어에만 의존해 더 나은 대안(예: 반복문 대신 `find -exec`)을 놓치기 쉽다 | 초반 진입 비용이 검색보다 크다 |
| 적합한 상황 | 이미 기초가 있고 특정 옵션만 확인하려는 경우 | 처음 셸을 배우거나, 체계적으로 빈 지식을 점검하려는 경우 |

이 컬렉션은 두 방식 모두를 지원하도록 설계됐다. 처음부터 순서대로 읽어 전체 흐름을 익힐 수도 있고, 특정 명령어의 옵션만 궁금하면 해당 장의 URL로 바로 이동해 사전처럼 찾아볼 수도 있다.

아래 다이어그램은 7개 Part가 어떤 순서로 서로를 전제하는지 요약한 것이다.

```mermaid
flowchart LR
    explore["Part 1</br>셸 기초와 탐색"]
    text["Part 2</br>텍스트 처리"]
    pipeline["Part 3</br>파이프라인과 입출력"]
    process["Part 4</br>프로세스와 작업 제어"]
    scripting["Part 5</br>셸 스크립팅"]
    filesystem["Part 6</br>파일 시스템과 권한"]
    network["Part 7</br>네트워크와 원격 접속"]

    explore --> text --> pipeline --> process --> scripting --> filesystem --> network
```

이 화살표는 물리적으로 강제되는 순서가 아니라 학습 효율을 위한 권장 순서다. 예를 들어 이미 다른 언어로 프로그래밍을 해본 독자는 5부(셸 스크립팅)의 문법 자체는 낯설지 않겠지만, 그 문법으로 무엇을 자동화할지 예제로 쓰이는 로그 필터링·파일 정리 작업은 2–3부를 모르면 이해하기 어렵다. 그래서 이 화살표는 "건너뛰면 절대 안 된다"가 아니라 "건너뛰면 이후 챕터의 예제를 이해하는 데 필요한 재료가 없다"는 경고에 가깝다.

## 흔한 오개념

<strong>"셸 스크립팅은 레거시 기술이라 몰라도 된다"</strong>는 생각은 가장 흔한 오해다. Python이나 Node.js로 자동화 스크립트를 짤 수 있다는 이유로 셸을 건너뛰는 경우가 많지만, 실제 서버의 부팅 절차·컨테이너 엔트리포인트·CI 러너 내부는 지금도 대부분 셸 스크립트로 짜여 있다. 다른 언어로 자동화를 짜더라도 그 스크립트를 호출하고 조합하는 계층은 여전히 셸이며, 5부(셸 스크립팅)에서 다루는 종료 코드와 `trap` 같은 견고성 장치를 모르면 그 자동화가 왜 조용히 실패했는지 진단할 수 없다.

<strong>"명령어 하나에 옵션은 하나의 정답만 있다"</strong>는 생각도 흔한 함정이다. 같은 작업(예: 파일 목록 조회)도 GNU 계열(리눅스)과 BSD 계열(macOS)에서 옵션 의미가 다르거나 아예 지원하지 않는 경우가 있다. 이 컬렉션의 참조형 챕터마다 "주의사항·함정" 절을 필수로 둔 이유가 여기에 있다 — 리눅스 서버에서 배운 옵션을 그대로 macOS 터미널에 옮기면 다른 결과가 나올 수 있다는 전제를 항상 확인해야 한다.

## 커리큘럼 전체 구성

이 과정은 7개 Part, 총 44개 챕터(00장 포함)로 구성된다. Part 구분은 임의의 분류가 아니라 "탐색 가능 → 내용을 읽고 검색 가능 → 조합 가능 → 실행을 제어 가능 → 스크립트로 자동화 가능 → 시스템을 관리 가능 → 원격까지 확장 가능"이라는 의존성 순서를 따른다. 예를 들어 파이프라인(3부)은 텍스트 처리 명령(2부)을 알아야 조합할 재료가 생기고, 셸 스크립팅(5부)은 `if`/`for` 이전에 텍스트 처리와 파이프를 알아야 실전 예제(로그에서 에러만 걸러 반복 처리하기 등)를 이해할 수 있다. 5부 내부 순서도 의존성을 지킨다 — 기본 제어(`if-test`/`for-while`) 다음에 조건 확장(`case`·산술 연산), 입력 처리(`read`), 자료구조(배열), 추상화(함수) 순으로 쌓은 뒤, 함수까지 알아야 이해하기 쉬운 `trap` 핸들러를 마지막에 배치했다. `which`/`whereis`/`locate`는 "명령어를 셸이 어떻게 찾는가"라는 같은 주제로 `PATH`/`type`/`hash`/`command` 챕터와 묶여 1부에 배치돼 있다.

| Part | 챕터 | 제목 | 슬러그 |
|---|---|---|---|
| 0. 개요 | 00 | 과정 개요와 커리큘럼 | 이 챕터 |
| 1. 셸 기초와 탐색 | 01 | [cd, pwd - 디렉터리 이동과 현재 위치](/post/bashshell/cd-pwd-change-directory-linux-commands/) | cd-pwd-change-directory-linux-commands |
| 1. 셸 기초와 탐색 | 02 | [ls - 파일 목록 조회](/post/bashshell/ls-command-list-files-directories-linux/) | ls-command-list-files-directories-linux |
| 1. 셸 기초와 탐색 | 03 | [cat - 파일 내용 출력](/post/bashshell/cat-head-tail-commands-view-file-contents/) | cat-head-tail-commands-view-file-contents |
| 1. 셸 기초와 탐색 | 04 | [less, more - 페이저로 긴 파일 보기](/post/bashshell/less-more-commands-view-large-files-linux/) | less-more-commands-view-large-files-linux |
| 1. 셸 기초와 탐색 | 05 | [touch - 파일 생성과 타임스탬프 갱신](/post/bashshell/touch-command-create-file-update-timestamp/) | touch-command-create-file-update-timestamp |
| 1. 셸 기초와 탐색 | 06 | [mkdir, rmdir - 디렉터리 생성과 삭제](/post/bashshell/mkdir-rmdir-commands-create-delete-directories/) | mkdir-rmdir-commands-create-delete-directories |
| 1. 셸 기초와 탐색 | 07 | [cp, mv, rm - 파일 복사·이동·삭제](/post/bashshell/cp-mv-rm-commands-copy-move-delete-files/) | cp-mv-rm-commands-copy-move-delete-files |
| 1. 셸 기초와 탐색 | 08 | [ln - 하드링크와 심볼릭 링크](/post/bashshell/ln-command-hard-symbolic-links-linux/) | ln-command-hard-symbolic-links-linux |
| 1. 셸 기초와 탐색 | 09 | [which, whereis, locate - 명령어와 파일 위치 찾기](/post/bashshell/which-whereis-locate-commands-find-command-location/) | which-whereis-locate-commands-find-command-location |
| 1. 셸 기초와 탐색 | 10 | [PATH, type, hash, command - 명령어 탐색 메커니즘](/post/bashshell/path-type-hash-command-shell-command-lookup/) | path-type-hash-command-shell-command-lookup |
| 1. 셸 기초와 탐색 | 11 | [.bashrc와 로그인·비로그인 셸](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/) | bashrc-bash-profile-login-shell-startup-files |
| 1. 셸 기초와 탐색 | 12 | [man, history - 매뉴얼 조회와 명령 히스토리](/post/bashshell/man-history-commands-manual-pages-shell-history/) | man-history-commands-manual-pages-shell-history |
| 2. 텍스트 처리 | 13 | [grep - 패턴 검색](/post/bashshell/grep-command-search-text-pattern-linux/) | grep-command-search-text-pattern-linux |
| 2. 텍스트 처리 | 14 | [sed - 스트림 편집](/post/bashshell/sed-command-stream-editor-linux/) | sed-command-stream-editor-linux |
| 2. 텍스트 처리 | 15 | [awk - 필드 기반 텍스트 처리](/post/bashshell/awk-command-text-processing-field-records/) | awk-command-text-processing-field-records |
| 2. 텍스트 처리 | 16 | [cut - 열 추출](/post/bashshell/cut-command-extract-columns-linux/) | cut-command-extract-columns-linux |
| 2. 텍스트 처리 | 17 | [tr - 문자 치환·삭제](/post/bashshell/tr-command-translate-delete-characters/) | tr-command-translate-delete-characters |
| 2. 텍스트 처리 | 18 | [sort, uniq, wc - 정렬·중복 제거·개수 세기](/post/bashshell/sort-uniq-wc-commands-sort-count-lines/) | sort-uniq-wc-commands-sort-count-lines |
| 3. 파이프라인과 입출력 | 19 | [pipe - 파이프라인 개념](/post/bashshell/pipe-operator-linux-command-chaining/) | pipe-operator-linux-command-chaining |
| 3. 파이프라인과 입출력 | 20 | [redirection - 입출력 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/) | io-redirection-linux-bash-tutorial |
| 3. 파이프라인과 입출력 | 21 | [xargs - 인자 변환과 명령 조합](/post/bashshell/xargs-command-build-execute-command-lines/) | xargs-command-build-execute-command-lines |
| 3. 파이프라인과 입출력 | 22 | [quoting - 인용과 이스케이프](/post/bashshell/bash-quoting-escaping-special-characters/) | bash-quoting-escaping-special-characters |
| 4. 프로세스와 작업 제어 | 23 | [ps - 프로세스 상태 조회](/post/bashshell/ps-command-process-status-linux/) | ps-command-process-status-linux |
| 4. 프로세스와 작업 제어 | 24 | [top - 실시간 시스템 모니터링](/post/bashshell/top-command-realtime-process-monitoring/) | top-command-realtime-process-monitoring |
| 4. 프로세스와 작업 제어 | 25 | [kill, jobs - 시그널 전송과 작업 제어](/post/bashshell/kill-jobs-commands-process-signal-job-control/) | kill-jobs-commands-process-signal-job-control |
| 4. 프로세스와 작업 제어 | 26 | [nohup - 세션 독립 실행](/post/bashshell/nohup-command-run-process-background-linux/) | nohup-command-run-process-background-linux |
| 5. 셸 스크립팅 | 27 | [if, test - 조건 분기](/post/bashshell/if-test-command-bash-conditional-statements/) | if-test-command-bash-conditional-statements |
| 5. 셸 스크립팅 | 28 | [for, while - 반복문](/post/bashshell/for-while-loop-bash-shell-scripting/) | for-while-loop-bash-shell-scripting |
| 5. 셸 스크립팅 | 29 | [case, 산술 연산 - 조건 확장](/post/bashshell/case-statement-arithmetic-expansion-bash/) | case-statement-arithmetic-expansion-bash |
| 5. 셸 스크립팅 | 30 | [read - 표준입력 읽기](/post/bashshell/read-command-standard-input-bash-scripting/) | read-command-standard-input-bash-scripting |
| 5. 셸 스크립팅 | 31 | [배열, 셸 확장 - 자료구조](/post/bashshell/bash-arrays-brace-parameter-expansion/) | bash-arrays-brace-parameter-expansion |
| 5. 셸 스크립팅 | 32 | [functions - 함수 정의와 재사용](/post/bashshell/bash-shell-functions-code-reuse/) | bash-shell-functions-code-reuse |
| 5. 셸 스크립팅 | 33 | [종료 코드, set -e/-x, trap - 스크립트 안정성](/post/bashshell/exit-status-set-trap-bash-error-handling/) | exit-status-set-trap-bash-error-handling |
| 5. 셸 스크립팅 | 34 | [echo, export, env - 출력과 환경변수](/post/bashshell/echo-export-env-commands-shell-variables/) | echo-export-env-commands-shell-variables |
| 5. 셸 스크립팅 | 35 | [alias - 명령어 별칭](/post/bashshell/alias-command-shell-command-shortcuts/) | alias-command-shell-command-shortcuts |
| 6. 파일 시스템과 권한 | 36 | [chmod, chown - 권한과 소유자 관리](/post/bashshell/chmod-chown-commands-file-permissions-ownership/) | chmod-chown-commands-file-permissions-ownership |
| 6. 파일 시스템과 권한 | 37 | [find - 파일 탐색과 조건 검색](/post/bashshell/find-command-search-files-conditions-linux/) | find-command-search-files-conditions-linux |
| 6. 파일 시스템과 권한 | 38 | [gzip - 압축과 해제](/post/bashshell/gzip-command-compress-decompress-files/) | gzip-command-compress-decompress-files |
| 6. 파일 시스템과 권한 | 39 | [tar - 아카이브 묶기](/post/bashshell/tar-command-archive-files-linux/) | tar-command-archive-files-linux |
| 6. 파일 시스템과 권한 | 40 | [du, df - 디스크 사용량 확인](/post/bashshell/du-df-commands-disk-usage-linux/) | du-df-commands-disk-usage-linux |
| 7. 네트워크와 원격 접속 | 41 | [curl, wget - HTTP 요청과 파일 다운로드](/post/bashshell/curl-wget-commands-download-http-files/) | curl-wget-commands-download-http-files |
| 7. 네트워크와 원격 접속 | 42 | [scp - 원격 파일 복사](/post/bashshell/scp-command-secure-copy-remote-files/) | scp-command-secure-copy-remote-files |
| 7. 네트워크와 원격 접속 | 43 | [ssh - 원격 접속](/post/bashshell/ssh-command-remote-login-secure-shell/) | ssh-command-remote-login-secure-shell |

6부(파일 시스템과 권한)와 7부(네트워크와 원격 접속)를 5부(셸 스크립팅) 뒤에 배치한 이유도 같은 의존성 논리를 따른다. `chmod`로 권한을 바꾸고 `find`로 조건에 맞는 파일을 찾는 작업은 대부분 스크립트 안에서 반복 실행되므로, 반복문과 조건문을 먼저 알아야 이 명령들을 "한 번 실행하고 끝"이 아니라 "자동화 파이프라인의 부품"으로 쓸 수 있다. 네트워크와 원격 접속(7부)을 맨 마지막에 둔 이유는 더 직접적이다. `scp`로 파일을 원격 서버에 올리거나 `ssh`로 접속해 작업을 수행하는 일은, 그 서버에 접속한 뒤 지금까지 배운 모든 것(탐색, 텍스트 처리, 프로세스 제어, 스크립팅, 파일 권한)을 그대로 다시 쓰는 행위이기 때문이다. 로컬에서 이 역량들을 갖추지 못한 채 원격 서버부터 만지기 시작하면, 원격 세션이 끊기거나 응답이 느릴 때 어디서부터 문제를 좁혀야 할지 판단할 기준이 없다.

## 선수 지식

이 과정을 시작하는 데 필요한 사전 지식은 많지 않다. 터미널(또는 콘솔) 창을 열고 텍스트로 명령을 입력하는 것에 거부감이 없으면 충분하며, 프로그래밍 경험은 필수가 아니다. 다만 5부(셸 스크립팅)에 들어가면 변수·조건문·반복문 같은 프로그래밍의 기본 개념을 다루므로, 다른 언어(Python, JavaScript 등)로 `if`/`for`를 써본 경험이 있으면 그 구간을 훨씬 빠르게 소화할 수 있다. 리눅스나 macOS 환경에 접근할 수 있어야 하며(가상 머신, WSL, 클라우드 인스턴스 어느 것이든 무방하다), 실습을 직접 해보며 읽는 것을 권장한다.

윈도우 사용자라면 WSL(Windows Subsystem for Linux)을 설치하는 것이 가장 마찰이 적은 시작점이다. CMD나 PowerShell에 익숙한 독자는 이 컬렉션과 짝을 이루는 `content/collection/cmd/` 컬렉션에서 같은 개념의 윈도우 대응 명령을 먼저 훑어보면, 이후 각 장의 "이식성" 관련 설명에서 두 생태계의 차이를 더 명확하게 느낄 수 있다.

## 완주 시 갖추는 역량

이 컬렉션을 끝까지 따라가면 "명령어를 안다"는 수준을 넘어, 낯선 리눅스 환경에 던져졌을 때 스스로 상황을 진단하고 반복 작업을 자동화하는 실무 역량을 갖추는 것을 목표로 한다. 이는 취업 시장에서 요구하는 "리눅스/셸 사용 가능"이라는 문구 뒤에 실제로 기대되는 능력이기도 하다 — 백엔드·데브옵스·데이터 엔지니어링 직군은 채용 공고에 셸 능력을 명시하지 않아도 입사 첫 주부터 서버 로그를 뒤지고 배포 스크립트를 고치는 일을 전제로 한다. 아래 목록은 이 컬렉션의 각 Part가 구체적으로 어떤 실무 상황에 대응하는지 보여준다.

- 낯선 리눅스 서버에 SSH로 접속해 디렉터리를 탐색하고, 필요한 파일을 찾아 권한을 확인·조정할 수 있다.
- 수백 줄짜리 로그 파일에서 원하는 패턴만 `grep`/`awk`/`sed`로 걸러내고, 파이프로 조합해 통계를 뽑을 수 있다.
- 반복 작업을 셸 스크립트로 작성하고, 종료 코드와 `trap`으로 실패 상황을 방어하는 스크립트를 짤 수 있다.
- 오래 걸리는 작업을 백그라운드로 돌리고, 필요할 때 프로세스 상태를 확인하고 안전하게 종료할 수 있다.
- CI/CD 파이프라인이나 컨테이너 엔트리포인트에 쓰인 셸 스크립트를 읽고, 실패 원인을 로그와 종료 코드로 진단할 수 있다.
- `curl`/`scp`/`ssh`로 원격 시스템과 파일을 주고받고, GNU와 BSD/POSIX 환경의 옵션 차이로 인한 실수를 피할 수 있다.

## 다음 장에서는

[01장: cd, pwd - 디렉터리 이동과 현재 위치](/post/bashshell/cd-pwd-change-directory-linux-commands/)에서는 셸에서 가장 먼저 익히는 두 명령어로 디렉터리 구조를 탐색하는 방법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 체계적으로 순서대로 학습하는 방식과 필요할 때 검색하는 방식의 장단점을 설명하고, 자신의 상황에 맞게 선택할 수 있다.
- 셸을 배우는 것이 자동화·원격 시스템 운영·텍스트 처리라는 세 가지 이유에서 왜 근본적인 개발 역량인지 말할 수 있다.
- 7개 Part(탐색-텍스트 처리-파이프라인-프로세스 제어-스크립팅-파일 시스템-네트워크)가 왜 이 순서인지, 하나를 건너뛰면 어떤 한계가 생기는지 설명할 수 있다.
- 자신의 배경(완전 초보/다른 커맨드라인 경험/레퍼런스 탐색)에 따라 이 컬렉션의 어느 부분부터 읽어야 할지 판단할 수 있다.
- 00–43장 전체 목차에서 특정 주제(예: 배열, `trap`, 디스크 사용량)가 몇 장에서 다뤄지는지 찾을 수 있다.

## 참고 및 출처

- GNU, "Bash Reference Manual", gnu.org/software/bash/manual/bash.html
- The Open Group, "Shell Command Language(POSIX.1-2017)", pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html
