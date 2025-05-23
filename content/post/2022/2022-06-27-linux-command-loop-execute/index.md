---
image: "tmp_wordcloud.png"
categories:
- Shell
date: "2022-06-27T00:00:00Z"
tags:
- Shell
- Linux
- Watch
- While
title: '[Shell] 명령어 반복 실행 (watch, while)'

---

가끔 같은 명령어를 주기적으로 실행해야 할 때가 있다. 예를 들어 시스템의 자원 사용량을 모니터링하거나, 특정 명령어를 반복적으로 입력해서 결과를 확인해야 할 때, 사용할 수 있는 방법을 알아보자.

## 1. watch


```watch```명령어는 주기적으로 실행 결과 표시한다. 사용법은 아래와 같이 단순하다. 결과 화면은 전체화면으로 표시된다. 빠져나올 때는 ^C로 나오면 된다.
 
```bash
watch -n [시간:초] <명령어>
```
 
예를 들어, 라우팅 갱신 상태를 1초 단위로 확인하고 싶다면

```bash
watch -n 1 ip ro
```
​
 이렇게 하면 main 라우팅 테이블의 상태를 1초마다 확인할 수 있습니다.

```bash
watch -n 1 ls -la /tmp
```

 /tmp 디렉토리의 파일 리스트 결과를 1초마다 확인합니다.
​
## 2. while

리눅스는 쉘 프롬프트에서 간단한 프로그래밍으로 명령어를 실행할 수 있다. 만약 ```netstat | grep aaa```를 1초에 한 번씩 실행해서 결과를 계속 보고 싶다면 명령 프롬프트에서 아래의 내용을 입력하면 된다.

```bash
while true; do netstat | grep aaa; sleep 1 ; done ;
```

빠져나올 때는 ^C로 나오면 된다.
 