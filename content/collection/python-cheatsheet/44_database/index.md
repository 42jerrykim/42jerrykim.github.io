---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 44. Database - sqlite3/ORM 기본 패턴"
slug: "simple-sqlite-database-guide-for-fast-sql-crud-class-methods"
description: "파이썬 데이터베이스 연동을 빠르게 시작하기 위한 치트시트입니다. sqlite3 기본 CRUD, 파라미터 바인딩, 트랜잭션, 컨텍스트 매니저 패턴과 SQL 인젝션 방지 등 실무 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 44
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - database
  - 데이터베이스
  - sqlite3
  - sqlite
  - SQL
  - CRUD
  - create
  - read
  - update
  - delete
  - insert
  - select
  - query
  - 쿼리
  - connection
  - 연결
  - cursor
  - 커서
  - execute
  - executemany
  - fetchone
  - fetchall
  - fetchmany
  - commit
  - rollback
  - transaction
  - 트랜잭션
  - parameter-binding
  - 파라미터바인딩
  - placeholder
  - sql-injection
  - SQL인젝션
  - 보안
  - security
  - context-manager
  - 컨텍스트매니저
  - with
  - ORM
  - sqlalchemy
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - standard-library
  - 표준라이브러리
  - persistence
  - 영속성
  - data-storage
  - 데이터저장
---
sqlite3는 파이썬 표준 라이브러리에 포함된 경량 관계형 데이터베이스입니다. 이 치트시트는 sqlite3 기본 CRUD, 파라미터 바인딩, 트랜잭션 처리와 SQL 인젝션 방지 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- 간단한 로컬 데이터 저장이 필요할 때 (JSON/pickle보다 구조화된 쿼리가 필요할 때)
- SQL 문법은 아는데 파이썬 연동 방법이 헷갈릴 때

## 핵심 패턴

- 연결: `sqlite3.connect("db.sqlite3")` → 파일 또는 `:memory:`
- 쿼리 실행: `cursor.execute(sql, params)` → **항상 파라미터 바인딩 사용**
- 트랜잭션: `conn.commit()` / `conn.rollback()`
- 컨텍스트 매니저: `with conn:` 블록 안에서 자동 commit/rollback

## 최소 예제

```python
import sqlite3

# 연결 (파일 또는 메모리)
conn = sqlite3.connect("example.db")  # 또는 ":memory:"
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
""")
conn.commit()
```

```python
# INSERT - 파라미터 바인딩 (? 플레이스홀더)
cursor.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    ("Alice", "alice@example.com")
)
conn.commit()

# INSERT 다건 - executemany
users_data = [
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com"),
]
cursor.executemany(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    users_data
)
conn.commit()
```

```python
# SELECT - fetchone / fetchall
cursor.execute("SELECT * FROM users WHERE name = ?", ("Alice",))
row = cursor.fetchone()  # 한 건 또는 None
print(row)  # (1, 'Alice', 'alice@example.com')

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()  # 리스트
for row in rows:
    print(row)
```

```python
# UPDATE / DELETE
cursor.execute(
    "UPDATE users SET email = ? WHERE name = ?",
    ("alice_new@example.com", "Alice")
)
cursor.execute("DELETE FROM users WHERE name = ?", ("Charlie",))
conn.commit()
```

```python
# 컨텍스트 매니저로 자동 commit/rollback
with sqlite3.connect("example.db") as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Dave", "dave@example.com"))
    # 블록 끝에서 자동 commit (예외 발생 시 rollback)
```

```python
# Row 객체로 컬럼명 접근
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
row = cursor.fetchone()
print(row["name"], row["email"])  # 컬럼명으로 접근
```

```python
# 연결 종료
conn.close()
```

## 자주 하는 실수/주의점

- **SQL 인젝션 방지**: f-string이나 문자열 포맷으로 SQL 작성 금지 → 항상 `?` 플레이스홀더 사용
  ```python
  # BAD - SQL 인젝션 취약
  cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
  
  # GOOD - 파라미터 바인딩
  cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
  ```
- **commit 누락**: INSERT/UPDATE/DELETE 후 `conn.commit()` 호출 필수 (또는 `with conn:` 사용)
- **단일 값 튜플**: 파라미터가 하나일 때 `(value,)` 형태로 전달 (쉼표 필수)
- **동시 접근**: sqlite3는 파일 기반이라 동시 쓰기에 제한 있음 → 멀티스레드는 `check_same_thread=False` 필요
- **타입 매핑**: sqlite는 동적 타입이라 파이썬 타입과 1:1 매칭되지 않을 수 있음

## ORM 개념 (참고)

대규모 프로젝트에서는 SQLAlchemy 같은 ORM을 사용:

```python
# SQLAlchemy 예시 (설치 필요: pip install sqlalchemy)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

engine = create_engine("sqlite:///example.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ORM CRUD
user = User(name="Eve", email="eve@example.com")
session.add(user)
session.commit()
```

## 관련 링크(공식 문서)

- [sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Tutorial](https://www.sqlite.org/lang.html)
