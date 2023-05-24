---
title: "[GBS] device is busy 문제 해결 방법"
categories:
  - Linux
tags:
  - Linux
  - Ubuntu
  - mount
  - gbs
---

리눅스에서 gbs로 개발을 하다보면 gbsroot가 제대로 unmount가 되지 않아서 문제가 발생할 수 있다. 이러한 경우에 해결하는 방법을 알아 보자.

# 문제 상황 

``` bash
error: there're mounted directories to build root. Please unmount them manually to avoid being deleted unexpectly:
        / ==> /home1/jong-min.kim/VBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0/dev/shm
error: <gbs>some packages failed to be built
```
위 로그 처럼 제대로 unmount가 되지 않아서 문제가 발생한것을 알 수 있다.

# Unmount 사용

``` bash
$ sudo umount -n /home1/jong-min.kim/VBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0/dev/shm
[sudo] password for jong-min.kim:
umount: /home1/jong-min.kim/VBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0/dev/shm: device is busy.
        (In some cases useful info about processes that use
         the device is found by lsof(8) or fuser(1))
```

unount 명령어를 사용해서 문제가 되는 디렉토리 제거를 시도해보면 제거가 잘 되지 않는것을 볼 수 있다.

## -l 또는 -f 옵션 사용

```bash
$ umount -l /datadisk
```
또는
```bash
$ umount -f /datadisk
```
* -f 옵션 : 않되는 경우도 있음
* -l 옵션 : 지연된 언마운트(lazy umount), 지연된 언마운트(lazy umount)는 디바이스가 사용되지 않을 때까지 대기한 후에 디렉토리 트리로부터 파일시스템을 언마운트한다.

``` bash
$ sudo umount -nl /home1/jong-min.kim/VBS-ROOT/local/BUILD-ROOTS/scratch.armv7l.0/dev/shm
```

이때 -l 옵션을 사용하여 디렉토리를 unmount 시켜주면 원하는 동작이 잘 이루어지는것을 볼 수 있다.

# fuser 사용
```bash
fuser -ck /datadisk
umount /datadisk
```

## fuser 명령어 

fuser명령어는 특정파일을 어떤프로세스에서 사용하고 있는지 확인이 필요할 때, 또는 특정 파일이 사용되고 있는 프로세스 ID를 확인하고자 할때 사용되는 명령어로 특정 파일과 PID를 KILL 또는 재시작 할 수도 있다.

### 옵션
* -a : 사용되고 있지 않은 파일까지도 표시한다.
* -k : 지정된 파일과 관련된 모든 프로세스들을 KILL 한다.
* -i : 프로세스를 KILL 하기전에 사용자에게 확인한다.
* -n space : 지정된 공간(file, udp, or , tcp)내에서 검색한다.
* -s : 결과를 간략히 출력한다.
* -u : 프로세스 ID(PID)의 소유자를 보여준다.