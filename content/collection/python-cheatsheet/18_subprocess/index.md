---

image: "wordcloud.png"
title: "[Python Cheatsheet] 18. subprocess - 외부 프로세스 실행"
slug: "external-process-run-execute-command-subprocess-guide-security"
description: "외부 명령어와 프로세스를 실행하기 위한 치트시트입니다. subprocess.run() 기본, 출력 캡처, 입력 전달, 타임아웃, 에러 처리, 셸 모드 주의점, 실무 패턴과 보안 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 18
tags:
  - Python
  - 파이썬
  - Cheatsheet
  - 치트시트
  - Quick-Reference
  - OS
  - shell
  - 셸
  - command
  - IO
  - automation
  - 자동화
  - DevOps
  - security
  - 보안
  - Best-Practices
  - pitfalls
  - 함정
  - Tutorial
  - 튜토리얼
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Git
  - GitHub
  - String
  - Process
  - Design-Pattern
  - Bash
  - Deployment
  - Error-Handling
  - 에러처리
  - Debugging
  - 디버깅
  - Documentation
  - 문서화
  - Testing
  - 테스트
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Performance
  - 성능
  - Optimization
  - 최적화
  - Logging
  - 로깅
  - Configuration
---
subprocess는 외부 명령어와 프로세스를 실행하는 파이썬 표준 라이브러리입니다. 이 치트시트는 `run()` 기본 사용, 출력 캡처, 타임아웃, 에러 처리, 보안 주의점을 정리합니다.

## 언제 이 치트시트를 보나?

- 파이썬에서 **외부 명령어**(git, ffmpeg, curl 등)를 실행하고 싶을 때
- 명령어의 **출력을 캡처**하거나 **입력을 전달**해야 할 때

## 핵심 패턴

- `subprocess.run()`: 명령 실행 후 완료까지 대기 (권장)
- `capture_output=True`: stdout/stderr 캡처
- `check=True`: 실패 시 예외 발생
- `text=True`: 바이트 대신 문자열로 결과 반환
- **shell=True 지양**: 보안 위험, 리스트로 인자 전달 권장

## 최소 예제

```python
import subprocess

# 기본 실행
result = subprocess.run(["echo", "Hello, World!"])
print(result.returncode)  # 0 (성공)
```

```python
# 출력 캡처
result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,  # stdout, stderr 캡처
    text=True,            # 문자열로 반환 (bytes 대신)
)
print(result.stdout)
print(result.stderr)
print(result.returncode)
```

```python
# check=True: 실패 시 예외
try:
    subprocess.run(
        ["ls", "nonexistent_file"],
        capture_output=True,
        text=True,
        check=True,  # returncode != 0이면 예외
    )
except subprocess.CalledProcessError as e:
    print(f"Command failed with code {e.returncode}")
    print(f"stderr: {e.stderr}")
```

```python
# 타임아웃
try:
    subprocess.run(
        ["sleep", "10"],
        timeout=2,  # 2초 후 타임아웃
    )
except subprocess.TimeoutExpired:
    print("Command timed out!")
```

```python
# 입력 전달 (stdin)
result = subprocess.run(
    ["cat"],
    input="Hello from Python\n",
    capture_output=True,
    text=True,
)
print(result.stdout)  # Hello from Python
```

## run() 주요 매개변수

| 매개변수 | 설명 |
|----------|------|
| `args` | 명령어와 인자 (리스트 권장) |
| `capture_output` | stdout/stderr 캡처 |
| `text` | 문자열로 입출력 (encoding 자동) |
| `check` | 실패 시 CalledProcessError 발생 |
| `timeout` | 타임아웃(초) |
| `input` | stdin으로 전달할 데이터 |
| `cwd` | 작업 디렉토리 |
| `env` | 환경변수 딕셔너리 |
| `shell` | 셸 통해 실행 (보안 주의) |

## CompletedProcess 객체

```python
result = subprocess.run(["echo", "test"], capture_output=True, text=True)

result.args        # ['echo', 'test']
result.returncode  # 0
result.stdout      # 'test\n'
result.stderr      # ''
```

## 셸 모드 (주의!)

```python
# shell=True: 셸을 통해 실행
# ⚠️ 보안 위험: 사용자 입력이 포함되면 인젝션 가능
result = subprocess.run(
    "echo $HOME",  # 문자열로 전달
    shell=True,
    capture_output=True,
    text=True,
)

# 🔴 위험한 예시 (절대 하지 말 것)
user_input = "file.txt; rm -rf /"  # 악의적 입력
subprocess.run(f"cat {user_input}", shell=True)  # 인젝션!

# ✅ 안전한 방법: 리스트로 전달
subprocess.run(["cat", user_input])  # 인자가 이스케이프됨
```

## 파이프라인

```python
# 파이프: cmd1 | cmd2
from subprocess import Popen, PIPE

# ls | grep .py
p1 = Popen(["ls", "-la"], stdout=PIPE)
p2 = Popen(["grep", ".py"], stdin=p1.stdout, stdout=PIPE, text=True)
p1.stdout.close()  # SIGPIPE 허용
output = p2.communicate()[0]
print(output)
```

```python
# shell=True로 파이프 (간단하지만 덜 안전)
result = subprocess.run(
    "ls -la | grep .py",
    shell=True,
    capture_output=True,
    text=True,
)
```

## Popen (고급: 비동기/스트리밍)

```python
from subprocess import Popen, PIPE

# 실시간 출력 읽기
with Popen(["ping", "-c", "3", "google.com"], stdout=PIPE, text=True) as proc:
    for line in proc.stdout:
        print(f">> {line.strip()}")

print(f"Exit code: {proc.returncode}")
```

```python
# communicate()로 입출력 처리
proc = Popen(
    ["python", "-c", "import sys; print(sys.stdin.read().upper())"],
    stdin=PIPE,
    stdout=PIPE,
    text=True,
)
stdout, stderr = proc.communicate(input="hello world")
print(stdout)  # HELLO WORLD
```

## 실무 패턴

```python
# Git 명령 실행
def git_commit(message: str) -> bool:
    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e.stderr}")
        return False
```

```python
# 환경변수 설정
import os

env = os.environ.copy()
env["MY_VAR"] = "custom_value"

subprocess.run(["printenv", "MY_VAR"], env=env)
```

```python
# 작업 디렉토리 변경
subprocess.run(
    ["ls", "-la"],
    cwd="/tmp",  # /tmp에서 실행
)
```

## 자주 하는 실수/주의점

- **shell=True 남용**: 보안 위험 + 플랫폼 의존성 증가
- **출력 캡처 안 함**: `capture_output=True` 없으면 stdout이 터미널로 출력
- **check=True 빠뜨림**: 명령 실패해도 예외 없이 계속 진행
- **Windows 호환**: 명령어 이름이 다를 수 있음 (예: `ls` → `dir`)
- **인코딩**: `text=True` 없으면 bytes 반환 → `.decode()` 필요
- **좀비 프로세스**: Popen 사용 시 `wait()` 또는 `communicate()` 호출 필수

## os.system() vs subprocess

```python
# os.system(): 레거시, 출력 캡처 불가
import os
os.system("echo hello")  # 사용 지양

# subprocess.run(): 권장
subprocess.run(["echo", "hello"])
```

## 관련 링크(공식 문서)

- [subprocess](https://docs.python.org/3/library/subprocess.html)
- [Replacing os.system()](https://docs.python.org/3/library/subprocess.html#replacing-older-functions-with-the-subprocess-module)
