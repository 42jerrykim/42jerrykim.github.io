---
title: "[Shell] 파일 이름에서 경로와 확장자를 추출하는 법"
categories:
  - Shell
tags:
  - Shell
  - file name
  - path
  - extract
  - bash
---

bash shell script 에서 file path 에서 확장자나 Path 를 제거하고 파일명만 뽑아내는 방법(bash shell 에서만 동작함)

# Path 제거하고 file 명만 추출

```
$ s=/the/path/foo.txt
$ echo ${s##*/}
foo.txt
```

# 파일명에서 확장자 제거(확장자가 .txt 에만 동작함. "basename foo.txt .txt" 와 동일)

```
$ s=foo.txt
$ echo ${s%.txt}
foo
```

# . 뒤에 붙은 임의의 확장자 제거

```
$ s=foo.txt
$ echo ${s%.*}
foo
```