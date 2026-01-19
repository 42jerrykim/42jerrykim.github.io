---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 17. argparse & CLI - 커맨드라인 인자 처리"
slug: "argparse-and-cli-command-line-arguments-parser-argumentparser-optional"
description: "커맨드라인 인자를 빠르게 처리하기 위한 치트시트입니다. argparse 기본, 위치/옵션 인자, 타입/기본값/필수 설정, 서브커맨드, 도움말 자동 생성, 실무 패턴과 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 17
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - argparse
  - cli
  - command-line
  - 커맨드라인
  - arguments
  - 인자
  - parser
  - 파서
  - ArgumentParser
  - positional
  - optional
  - flags
  - 플래그
  - options
  - 옵션
  - type
  - default
  - required
  - help
  - 도움말
  - subcommands
  - 서브커맨드
  - nargs
  - choices
  - action
  - store_true
  - sys.argv
  - script
  - 스크립트
  - automation
  - 자동화
  - devops
  - tools
  - 도구
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
---
argparse는 커맨드라인 인자를 파싱하는 파이썬 표준 라이브러리입니다. 이 치트시트는 위치/옵션 인자, 타입 변환, 서브커맨드, 도움말 생성의 핵심 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- CLI 도구나 스크립트에 **옵션/인자**를 받고 싶을 때
- `--help` 자동 생성이 필요할 때

## 핵심 패턴

- `ArgumentParser()`: 파서 생성
- `add_argument()`: 인자 정의 (위치/옵션)
- `parse_args()`: 파싱 후 `Namespace` 객체 반환
- 옵션: `-v`, `--verbose` (앞에 `-` 붙임)
- 위치 인자: `-` 없이 정의

## 최소 예제

```python
# basic_cli.py
import argparse

parser = argparse.ArgumentParser(
    description="파일 처리 도구"
)

# 위치 인자 (필수)
parser.add_argument("filename", help="처리할 파일 경로")

# 옵션 인자
parser.add_argument("-o", "--output", help="출력 파일 경로")
parser.add_argument("-v", "--verbose", action="store_true", help="상세 출력")
parser.add_argument("-n", "--count", type=int, default=1, help="반복 횟수")

args = parser.parse_args()

print(f"Input: {args.filename}")
print(f"Output: {args.output}")
print(f"Verbose: {args.verbose}")
print(f"Count: {args.count}")
```

```bash
# 실행 예시
python basic_cli.py input.txt
python basic_cli.py input.txt -o output.txt -v
python basic_cli.py input.txt --count 5
python basic_cli.py --help
```

```
# --help 출력
usage: basic_cli.py [-h] [-o OUTPUT] [-v] [-n COUNT] filename

파일 처리 도구

positional arguments:
  filename              처리할 파일 경로

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        출력 파일 경로
  -v, --verbose         상세 출력
  -n COUNT, --count COUNT
                        반복 횟수
```

## 주요 add_argument 옵션

```python
parser.add_argument(
    "name",           # 위치 인자 (또는 "-n", "--name" 옵션)
    type=int,         # 타입 변환 (int, float, str, pathlib.Path 등)
    default=10,       # 기본값
    required=True,    # 필수 여부 (옵션 인자에만)
    help="설명",      # 도움말
    choices=[1, 2, 3],# 허용 값 제한
    nargs="+",        # 인자 개수 (*, +, ?, N)
    action="store_true",  # 플래그 (값 없이 True/False)
    dest="var_name",  # 저장될 변수명
    metavar="FILE",   # 도움말에 표시될 이름
)
```

## nargs 옵션

| nargs | 의미 | 결과 타입 |
|-------|------|-----------|
| `N` (정수) | 정확히 N개 | list |
| `?` | 0개 또는 1개 | 값 또는 None |
| `*` | 0개 이상 | list |
| `+` | 1개 이상 | list |

```python
parser.add_argument("files", nargs="+", help="하나 이상의 파일")
# python script.py a.txt b.txt c.txt → args.files = ['a.txt', 'b.txt', 'c.txt']
```

## action 옵션

```python
# store_true: 플래그가 있으면 True
parser.add_argument("-v", "--verbose", action="store_true")

# store_false: 플래그가 있으면 False
parser.add_argument("--no-cache", action="store_false", dest="cache")

# count: 플래그 개수 카운트
parser.add_argument("-v", action="count", default=0)
# -vvv → args.v = 3

# append: 여러 번 지정 시 리스트에 추가
parser.add_argument("--include", action="append")
# --include a --include b → args.include = ['a', 'b']
```

## 서브커맨드

```python
# git처럼 서브커맨드 구현
import argparse

parser = argparse.ArgumentParser(prog="mytool")
subparsers = parser.add_subparsers(dest="command", help="서브커맨드")

# init 서브커맨드
parser_init = subparsers.add_parser("init", help="초기화")
parser_init.add_argument("--force", action="store_true")

# run 서브커맨드
parser_run = subparsers.add_parser("run", help="실행")
parser_run.add_argument("target", help="실행 대상")
parser_run.add_argument("-n", type=int, default=1)

args = parser.parse_args()

if args.command == "init":
    print(f"Initializing... force={args.force}")
elif args.command == "run":
    print(f"Running {args.target} {args.n} times")
```

```bash
python mytool.py init --force
python mytool.py run script.py -n 3
python mytool.py --help
python mytool.py run --help
```

## 실무 패턴

```python
# 타입 변환 함수
import argparse
from pathlib import Path

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value}는 양수여야 합니다")
    return ivalue

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=positive_int)
parser.add_argument("--path", type=Path)  # pathlib.Path로 변환
```

```python
# 환경변수 기본값
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--api-key",
    default=os.environ.get("API_KEY"),
    help="API 키 (기본: $API_KEY)"
)
```

```python
# main() 패턴
def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args(args)  # args=None이면 sys.argv 사용
    print(f"Hello, {args.name}")

if __name__ == "__main__":
    main()
```

## 자주 하는 실수/주의점

- **위치 인자 순서**: 정의 순서대로 파싱됨
- **옵션 이름 충돌**: `-h`는 기본적으로 help에 예약됨
- **type=bool 함정**: `type=bool`은 의도대로 동작 안 함 → `action="store_true"` 사용
- **required 옵션**: 위치 인자는 기본적으로 필수, `nargs="?"`로 선택적으로 변경 가능
- **dest 네이밍**: `--my-option`은 `args.my_option`으로 접근 (하이픈 → 언더스코어)

## 대안: click, typer

더 복잡한 CLI가 필요하면 서드파티 라이브러리 고려:

```python
# typer 예시 (pip install typer)
import typer

app = typer.Typer()

@app.command()
def hello(name: str, count: int = 1):
    for _ in range(count):
        print(f"Hello {name}")

if __name__ == "__main__":
    app()
```

## 관련 링크(공식 문서)

- [argparse](https://docs.python.org/3/library/argparse.html)
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)
