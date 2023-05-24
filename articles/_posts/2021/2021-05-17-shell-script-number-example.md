---
title: "[Shell] 숫자로 메뉴 실행하는 셸스크립트 예제"
categories:
  - Shell
tags:
  - Shell
  - Navigation
---

숫자를 이용해서 여러 명령어를 실행 할 수 있는 셸스크립트

# 코드

```bash
while (true) ; do
clean
echo '
1. cmd 1
2. cmd 2
3. cmd 3
q. end
'
echo -n "select:"
read no
case $no in
"1" )
 ls;;
"2" )
 ls -al;;
"3" )
    ls -a;;
"q" )
 exit 0;;
esac
done
```
