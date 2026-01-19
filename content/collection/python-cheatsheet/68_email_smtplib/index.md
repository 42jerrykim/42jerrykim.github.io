---

image: "wordcloud.png"
title: "[Python Cheatsheet] 68. email & smtplib - 이메일 작성/발송"
slug: "smtp-email-sending-guide-attach-html-auth-secure-tips"
description: "파이썬 email과 smtplib 모듈을 빠르게 사용하기 위한 치트시트입니다. 이메일 메시지 생성, SMTP 발송, 첨부파일, HTML 메일 등 핵심 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 68
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - email
  - 이메일
  - smtp
  - SMTP
  - smtplib
  - send-email
  - 이메일발송
  - attachment
  - 첨부파일
  - html-email
  - HTML이메일
  - mime
  - MIME
  - gmail
  - outlook
  - ssl
  - tls
  - authentication
  - 인증
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - automation
  - 자동화
---
`email` 모듈은 **이메일 메시지 생성**을, `smtplib`는 **SMTP 프로토콜로 발송**을 담당합니다. 알림 메일, 리포트 발송, 자동화 등에 유용합니다.

## 언제 이 치트시트를 보나?

- 파이썬으로 **이메일을 발송**하고 싶을 때
- **첨부 파일**이 있는 메일을 보내야 할 때
- **HTML 형식**의 메일을 보내야 할 때

## 기본 구조

```python
from email.message import EmailMessage
import smtplib

# 1. 메시지 생성
msg = EmailMessage()
msg['Subject'] = '제목'
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'
msg.set_content('본문')

# 2. SMTP로 발송
with smtplib.SMTP('smtp.example.com', 587) as server:
    server.starttls()
    server.login('user', 'password')
    server.send_message(msg)
```

## 최소 예제

### 1. 기본 텍스트 메일

```python
from email.message import EmailMessage
import smtplib

msg = EmailMessage()
msg['Subject'] = '테스트 메일'
msg['From'] = 'sender@gmail.com'
msg['To'] = 'recipient@example.com'
msg.set_content('안녕하세요, 테스트 메일입니다.')

# Gmail SMTP (앱 비밀번호 필요)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login('sender@gmail.com', 'your-app-password')
    server.send_message(msg)
    print("메일 발송 완료!")
```

### 2. HTML 메일

```python
from email.message import EmailMessage
import smtplib

msg = EmailMessage()
msg['Subject'] = 'HTML 메일'
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'

# 텍스트 대체 본문
msg.set_content('HTML을 볼 수 없는 클라이언트용 텍스트')

# HTML 본문
html_content = """
<html>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 <strong>HTML</strong> 메일입니다.</p>
    <ul>
        <li>항목 1</li>
        <li>항목 2</li>
    </ul>
</body>
</html>
"""
msg.add_alternative(html_content, subtype='html')

with smtplib.SMTP('smtp.example.com', 587) as server:
    server.starttls()
    server.login('user', 'password')
    server.send_message(msg)
```

### 3. 파일 첨부

```python
from email.message import EmailMessage
import smtplib
import mimetypes

msg = EmailMessage()
msg['Subject'] = '첨부 파일 테스트'
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'
msg.set_content('첨부 파일을 확인해주세요.')

# 파일 첨부
filename = 'report.pdf'
with open(filename, 'rb') as f:
    file_data = f.read()
    file_type, encoding = mimetypes.guess_type(filename)
    if file_type is None:
        file_type = 'application/octet-stream'
    maintype, subtype = file_type.split('/')
    
    msg.add_attachment(
        file_data,
        maintype=maintype,
        subtype=subtype,
        filename=filename
    )

with smtplib.SMTP('smtp.example.com', 587) as server:
    server.starttls()
    server.login('user', 'password')
    server.send_message(msg)
```

### 4. 여러 수신자

```python
from email.message import EmailMessage

msg = EmailMessage()
msg['Subject'] = '단체 메일'
msg['From'] = 'sender@example.com'
msg['To'] = 'user1@example.com, user2@example.com'
msg['Cc'] = 'cc@example.com'
msg['Bcc'] = 'bcc@example.com'  # 숨은 참조

msg.set_content('모두에게 보내는 메일입니다.')
```

### 5. 이미지 삽입 (인라인)

```python
from email.message import EmailMessage
import smtplib

msg = EmailMessage()
msg['Subject'] = '이미지 포함 메일'
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'

# HTML에서 cid로 참조
html = """
<html>
<body>
    <h1>이미지가 포함된 메일</h1>
    <img src="cid:image1">
</body>
</html>
"""
msg.add_alternative(html, subtype='html')

# 이미지 첨부 (인라인)
with open('logo.png', 'rb') as f:
    img_data = f.read()
    msg.get_payload()[1].add_related(
        img_data,
        maintype='image',
        subtype='png',
        cid='image1'
    )
```

### 6. Gmail 설정

```python
import smtplib

# Gmail 사용 시:
# 1. 2단계 인증 활성화
# 2. 앱 비밀번호 생성 (보안 → 앱 비밀번호)

GMAIL_USER = 'your-email@gmail.com'
GMAIL_APP_PASSWORD = 'xxxx xxxx xxxx xxxx'  # 앱 비밀번호

# SSL 사용 (포트 465)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.send_message(msg)

# 또는 TLS 사용 (포트 587)
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.send_message(msg)
```

### 7. 에러 처리

```python
import smtplib
from email.message import EmailMessage
import socket

msg = EmailMessage()
msg['Subject'] = '테스트'
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'
msg.set_content('내용')

try:
    with smtplib.SMTP('smtp.example.com', 587, timeout=10) as server:
        server.starttls()
        server.login('user', 'password')
        server.send_message(msg)
        print("발송 성공!")
        
except smtplib.SMTPAuthenticationError:
    print("인증 실패: 아이디/비밀번호 확인")
except smtplib.SMTPRecipientsRefused:
    print("수신자 거부됨")
except smtplib.SMTPServerDisconnected:
    print("서버 연결 끊김")
except socket.timeout:
    print("연결 타임아웃")
except Exception as e:
    print(f"에러: {e}")
```

### 8. 메일 서버별 설정

```python
# Gmail
smtp_server = 'smtp.gmail.com'
port = 465  # SSL

# Outlook/Office365
smtp_server = 'smtp.office365.com'
port = 587  # TLS

# Naver
smtp_server = 'smtp.naver.com'
port = 465  # SSL

# 직접 설정
smtp_server = 'mail.example.com'
port = 25  # 또는 587 (TLS), 465 (SSL)
```

### 9. 비동기 발송 (대량 메일)

```python
import smtplib
from email.message import EmailMessage
from concurrent.futures import ThreadPoolExecutor

def send_email(recipient, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'sender@example.com'
    msg['To'] = recipient
    msg.set_content(body)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('user', 'password')
        server.send_message(msg)
    
    return f"Sent to {recipient}"

recipients = ['user1@example.com', 'user2@example.com', 'user3@example.com']

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(send_email, r, '제목', '내용')
        for r in recipients
    ]
    for future in futures:
        print(future.result())
```

### 10. 템플릿 사용

```python
from email.message import EmailMessage
from string import Template

# 템플릿
html_template = Template("""
<html>
<body>
    <h1>안녕하세요, $name님!</h1>
    <p>주문번호 $order_id가 처리되었습니다.</p>
    <p>감사합니다.</p>
</body>
</html>
""")

def send_order_confirmation(recipient, name, order_id):
    msg = EmailMessage()
    msg['Subject'] = f'주문 확인 - {order_id}'
    msg['From'] = 'shop@example.com'
    msg['To'] = recipient
    
    html = html_template.substitute(name=name, order_id=order_id)
    msg.add_alternative(html, subtype='html')
    
    # 발송...
```

## 자주 하는 실수

### 1. Gmail 일반 비밀번호 사용

```python
# 잘못: Gmail 계정 비밀번호 직접 사용
# server.login('user@gmail.com', 'my-password')  # 실패!

# 올바름: 앱 비밀번호 사용
# 1. Google 계정 → 보안 → 2단계 인증 활성화
# 2. 앱 비밀번호 생성
server.login('user@gmail.com', 'xxxx xxxx xxxx xxxx')
```

### 2. 한글 제목 깨짐

```python
from email.message import EmailMessage

msg = EmailMessage()
# EmailMessage는 자동으로 인코딩 처리
msg['Subject'] = '한글 제목'  # OK
```

## 한눈에 정리

| 작업 | 코드 |
|------|------|
| 메시지 생성 | `EmailMessage()` |
| 본문 설정 | `msg.set_content(text)` |
| HTML 본문 | `msg.add_alternative(html, subtype='html')` |
| 파일 첨부 | `msg.add_attachment(data, ...)` |
| 발송 | `server.send_message(msg)` |

## 참고

- [email - Python Docs](https://docs.python.org/3/library/email.html)
- [smtplib - Python Docs](https://docs.python.org/3/library/smtplib.html)
