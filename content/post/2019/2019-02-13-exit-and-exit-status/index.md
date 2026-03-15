---
image: "tmp_wordcloud.png"
categories:
- Shell
date: "2019-02-13T00:00:00Z"
description: "셸 스크립트에서 exit 명령의 동작과 종료 상태(exit status)의 의미를 설명합니다. 성공 시 0, 실패 시 비영점 반환, exit nnn으로 부모 프로세스에 값 전달, 마지막 명령의 상태가 스크립트 종료값이 되는 규칙과 예제를 150자 분량으로 정리합니다."
redirect_from:
- /2019/02/13/
tags:
- Shell
- bash
- Sci-Fi
- Process
- Command
- Design-Pattern
- Blog
- 블로그
- Technology
- 기술
- Web
- 웹
- Tutorial
- 가이드
- Review
- 리뷰
- Markdown
- 마크다운
- Python
- Deployment
- Guide
- Productivity
- 생산성
- Education
- 교육
- Reference
- 참고
- Best-Practices
- Documentation
- 문서화
- Open-Source
- 오픈소스
- Innovation
- 혁신
- Troubleshooting
- 트러블슈팅
- Configuration
- 설정
- How-To
- Tips
- Comparison
- 비교
- Career
- 커리어
- Workflow
- 워크플로우
- Migration
- 마이그레이션
- Hardware
- 하드웨어
- Cloud
- 클라우드
- Mobile
- 모바일
title: '[Shell] Exit and exit status'
---



The `exit` command terminates a script, just as in a C program. It can also return a value, which is available to the script's parent process.

Every command returns an exit status (sometimes referred to as a return status or exit code). A successful command returns a 0, while an unsuccessful one returns a non-zero value that usually can be interpreted as an error code. Well-behaved UNIX commands, programs, and utilities return a 0 exit code upon successful completion, though there are some exceptions.

Likewise, functions within a script and the script itself return an exit status. The last command executed in the function or script determines the exit status. Within a script, an `exit nnn` command may be used to deliver an `nnn` exit status to the shell (nnn must be an integer in the 0 - 255 range).

When a script ends with an exit that has no parameter, the exit status of the script is the exit status of the last command executed in the script (previous to the exit).

``` bash
#!/bin/bash

COMMAND_1

. . .

COMMAND_LAST

exit # Will exit with status of last command.
```

The equivalent of a bare exit is exit $? or even just omitting the exit.


``` bash
#!/bin/bash

COMMAND_1

. . .

COMMAND_LAST

exit $? # Will exit with status of last command.
```

``` bash
#!/bin/bash

COMMAND1

. . . 

COMMAND_LAST

# Will exit with status of last command.
```

`$?` reads the exit status of the last command executed. After a function returns, $? gives the exit status of the last command executed in the function. This is Bash's way of giving functions a **return value.**[^1]

Following the execution of a pipe, a $? gives the exit status of the last command executed.

After a script terminates, a $? from the command-line gives the exit status of the script, that is, the last command executed in the script, which is, by convention, 0 on success or an integer in the range 1 - 255 on error.

## Example exit / exit status
``` bash
#!/bin/bash

echo hello
echo $?    # Exit status 0 returned because command executed successfully.

lskdf      # Unrecognized command.
echo $?    # Non-zero exit status returned -- command failed to execute.

echo

exit 113   # Will return 113 to shell.
           # To verify this, type "echo $?" after script terminates.
```
By convention, an `exit 0` indicates success, while a non-zero exit value means an error or anomalous condition. 
<!-- See the "Exit Codes With Special Meanings" appendix. -->

`$?` is especially useful for testing the result of a command in a script

The !, the logical not qualifier, reverses the outcome of a test or command, and this affects its exit status.

## Negating a condition using !
``` bash
true    # The "true" builtin.
echo "exit status of \"true\" = $?" # 0
```
``` bash
! true
echo "exit status of \"! true\" = $?" # 1
```
Note that the `!` needs a space between it and the command. `!true` leads to a **command not found** error

The `!` operator prefixing a command invokes the Bash history mechanism.

``` bash
true
!true
```
No error this time, but no negation either. It just repeats the previous command (true).

Preceding a _pipe_ with ! inverts the exit status returned.
``` bash
ls | bogus_command     # bash: bogus_command: command not found
echo $?                # 127
```
``` bash
! ls | bogus_command   # bash: bogus_command: command not found
echo $?                # 0
```
Note that the ! does not change the execution of the pipe. Only the exit status changes.

Certain exit status codes have reserved meanings and should not be user-specified in a script.

[^1]: In those instances when there is no return terminating the function.