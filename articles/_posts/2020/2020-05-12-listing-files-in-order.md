---
title: "[Shell] 날짜로 정렬해서 파일 목록 뽑기"
excerpt_separator: "<!--more-->"
categories:
  - Shell
tags:
  - Shell
  - ls
  - date
  - order
  - file
  - linux
  - bash
  - 정렬
  - 날짜
  - 파일
  - 목록
---

# Method 1: 오래된 파일 부터 보이기
This is useful if you want to check and erase old files.
Check the old files by putting the -r option on top.

``` bash
# command
ls --time-style="+%Y-%m-%d %H:%M:%S" -altr | grep ^- | more

# example
ls --time-style="+%Y-%m-%d %H:%M:%S" -altr | grep ^- | more
-rw-------  1 root root 1907993 2013-02-12 12:30:01 audit.log
-r--------  1 root root 6291625 2013-01-24 21:35:24 audit.log.1
-r--------  1 root root 6291536 2013-01-11 18:03:39 audit.log.2
-r--------  1 root root 6291516 2013-01-02 14:10:15 audit.log.3
-r--------  1 root root 6291634 2012-12-05 09:39:43 audit.log.4
```

# Method 2: 최신 파일 부터 보이기
This is useful when checking whether the latest log file has been created.

``` bash
# command
ls --time-style="+%Y-%m-%d %H:%M:%S" -alt | grep ^- | more

# example
ls --time-style="+%Y-%m-%d %H:%M:%S" -alt | grep ^- | more
-r--------  1 root root 6291634 2012-12-05 09:39:43 audit.log.4
-r--------  1 root root 6291516 2013-01-02 14:10:15 audit.log.3
-r--------  1 root root 6291536 2013-01-11 18:03:39 audit.log.2
-r--------  1 root root 6291625 2013-01-24 21:35:24 audit.log.1
-rw-------  1 root root 1907993 2013-02-12 12:30:01 audit.log
```
