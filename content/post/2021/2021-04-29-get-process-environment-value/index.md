---
image: "tmp_wordcloud.png"
categories:
- Shell
date: "2021-04-29T00:00:00Z"
tags:
- Shell
- environ
- proc
- process
- environment
- xargs
title: '[Shell] 리눅스 실행 프로세스의 환경변수 알아보기'
---

리눅스의 실행 프로세스의 환경변수는 /proc 파일시스템을 통해서 알 수 있다. 예를 들어 pid 1000번의 환경변수는 

```bash
cat /proc/1000/environ
```

로 확인 할 수 있다. 하지만, 이 결과는 변수간 구분이 잘 확인이 안된다. 변수간 구분을 '\0'으로 분리시켜 놓았기 때문이다. 실제 프로세스 메모리에서도 '\0'으로 구분되어 있고 이를 그대로 화면에 출력하는 것이다. 다음을 보자.

```bash
cat /proc/1000/environ | xargs -0 -n 1 echo
```

xargs 는 표준 입력을 명령의 argument로 전달해 실행해주는 함수인데, 이때 기본값은 공백을 사용하여 표준입력을 분리한다. 하지만 위와 같이 '-0' (zero) 옵션을 주면 구분자를 '\0'으로 하라는 뜻이며, '-n 1' 을 주어 하나의 인자마다 하나의 명령을 실행(여기서는 echo)하라는 의미가 된다.


사족으로 xargs의 -0 옵션은 find 의 -print0 옵션과 같이 사용하여 출력결과를 실행시에 적절하게 처리하는데 사용한다.
