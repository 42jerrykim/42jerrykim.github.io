---
draft: true
title: "06. 파일 입출력"
description: "파일 읽기, 쓰기, 경로 처리 및 다양한 파일 형식 다루기"
collection_order: 6
---

# 챕터 6: 파일 입출력

> "데이터는 프로그램의 연료다" - 파일을 통해 데이터를 영구적으로 저장하고 불러오는 방법을 마스터해봅시다.

## 학습 목표
- 파일을 안전하게 열고 닫을 수 있다
- 다양한 모드로 파일을 읽고 쓸 수 있다
- 파일 경로와 디렉토리를 효과적으로 다룰 수 있다
- 다양한 파일 형식을 처리할 수 있다

## 기본 파일 연산

### 파일 열기와 닫기

**기본 파일 열기:**

```python
# 기본적인 파일 열기 (권장하지 않는 방법)
file = open('example.txt', 'r', encoding='utf-8')
content = file.read()
file.close()  # 반드시 닫아야 함!

print(content)
```

**문제점과 개선된 방법:**

```python
# 예외 발생 시에도 안전한 파일 처리
file = None
try:
    file = open('example.txt', 'r', encoding='utf-8')
    content = file.read()
    print(content)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except IOError:
    print("파일을 읽는 중 오류가 발생했습니다.")
finally:
    if file:
        file.close()
```

### with 문을 사용한 안전한 파일 처리

```python
# with 문 (컨텍스트 매니저) - 권장 방법
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)
# 자동으로 파일이 닫힘

# 여러 파일 동시 처리
with open('input.txt', 'r', encoding='utf-8') as infile, \
     open('output.txt', 'w', encoding='utf-8') as outfile:
    data = infile.read()
    processed_data = data.upper()  # 대문자로 변환
    outfile.write(processed_data)
```

### 파일 모드

```python
# 텍스트 모드
# 'r' - 읽기 (기본값)
# 'w' - 쓰기 (파일 내용 덮어쓰기)
# 'a' - 추가 (파일 끝에 내용 추가)
# 'x' - 배타적 생성 (파일이 이미 존재하면 에러)

# 읽기 모드
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 쓰기 모드 (기존 내용 삭제)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("새로운 내용")

# 추가 모드 (기존 내용 유지)
with open('log.txt', 'a', encoding='utf-8') as f:
    f.write("로그 메시지\n")

# 바이너리 모드
# 'rb', 'wb', 'ab' - 바이너리 읽기/쓰기/추가

with open('image.jpg', 'rb') as f:
    binary_data = f.read()

with open('copy.jpg', 'wb') as f:
    f.write(binary_data)
``` 