---
image: "tmp_wordcloud.png"
title: "del - 파일 삭제"
date: 2022-01-01
categories: CMD
---

마이크로소프트를 비롯한 여러 회사의 도스, OS/2 및 윈도우의 명령 줄 인터페이스(셸), 윈도우 파워셸 등에서, del (또는 erase)는 하나 이상의 파일이나 디렉터리를 파일 시스템에서 삭제하는 용도로 제공되어 있다. 유닉스 계열의 운영 체제에서 제공하는 rm과 역할 면에서 비슷하다.

윈도 파워셸에서는 del 과 erase가 Remove-Item 커맨드릿의 앨리어스로 설정되어 있으나, 역할은 같다. 

**디렉토리를 삭제할때는 rmdir를 사용한다.**

## 옵션
* /p: 파일을 삭제하기 전에 삭제를 확인하는 메시지를 표시한다.
* /f: 읽기전용 파일도 삭제한다.
* /s: 모든 하위 디렉터리에서 파일을 삭제한다.
* /q: 파일을 삭제할것인지 묻는 메시지를 표시하지 않는다.

## 예시
C 드라이브의 여러개의 하위 폴대 내에 산재되어 있는 ABC 가 포함된 파일들을 삭제하려면(확장자 .txt 일 경우) CMD 에 아래와 같이 입력하시면 됩니다. 

```
c:\>del /s /q "*abc*.txt"  또는 c:\>del /s "*abc*.txt"
```
