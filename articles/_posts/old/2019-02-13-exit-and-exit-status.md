---

title: "[Shell] Exit and exit status"
description: ""
categories: [Shell]
tags: [Shell, bash, exit]
redirect_from:
  - /2019/02/13/
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

# Example exit / exit status
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

# Negating a condition using !
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