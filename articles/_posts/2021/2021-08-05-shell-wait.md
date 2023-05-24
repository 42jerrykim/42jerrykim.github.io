---
title: "[Shell] 서브 프로세스의 실행 종료를 대기하는 wait 커맨드"
categories:
  - Shell
tags:
  - Shell
  - Bash
  - wait
  - process
---

Wait 커맨드는 프로세스의 실행 종료를 대기하게 한다. 특정 프로세스를 대히하게 할 수도 있고, 전체 프로세스의 종료를 대기 할 수도 있다.

# 사용 방법

* **wait %Background ID** : jobs 로 확인할 수 있는 백그라운드 번호로 대기
* **wait PID** : PID 번호의 프로세스 대기
* **wait** : 전체 서브 프로세스 종료 대기 

# 예시

``` bash
#!/bin/bash

a &
b &
c &

wait
echo "end"
```

위와 같이 스크립트를 작성해서 실행하면 a, b, c의 작업이 종료되고, "end"를 출력한다.
