---
title: "[RDPWrapper] Windows 10 Pro 20H2에서 not supported issue 해결하기"
categories:
  - RDPWrapper
tags:
  - RDPWrapper
  - 20H2
  - Windows
header:
  teaser: https://user-images.githubusercontent.com/11385249/112481810-73097380-8d88-11eb-90ae-27adaa456182.png
---

RDP Wrapper는 윈도우 원격을 여러명이서 동시에 사용할 수 있도록 해주는 좋은 프로그램이다. 하지만 그냥 설치 했을때는 not supported 문제가 발생하여 사용을 할 수 없는 경우가 있다. 본 게시물에서는 Win 10 Pro 20H2에서 not supported문제를 해결 할 수 있는 방법을 알려준다.

# 문제 상황

Win 10 Pro 20H2에서 not supported가 발생했을때 처리 하는 방법이다.

![Not supported](https://user-images.githubusercontent.com/11385249/112481810-73097380-8d88-11eb-90ae-27adaa456182.png)

RDP Wrapper를 설치 하였으나 붉은색으로 [not supported]가 표시되는것을 확인 할 수 있다.

![Image Alt 텍스트](https://user-images.githubusercontent.com/81416060/112618075-3482c000-8e3f-11eb-874a-9b38e9849e10.png)

추가적으로 윈도우의 버전을 확인해야 한다. 윈도위 버전이 20H2인경우 아래의 대응 방법에 따라서 조치를 취한다.

# 대응 방법

아래의 내용을 순서대로 수행한다.

## 1. 관련 파일 다운로드
 [LINK#1](https://github.com/stascorp/rdpwrap/releases) 또는 [LINK#2](https://sabercathost.com/e2bm/RDPWrap-v1.6.2.zip)에서 "RDPWrap-v1.6.2.zip"을 다운 받아서 "%ProgramFiles%\RDP Wrapper"경로에 압축을 푼다.

> RDP Wrapper 파일을 다른 폴더에 풀지 말아라

> "%ProgramFiles%\RDP Wrapper" 경로만 사용해라 (보통 C:\Program Files\RDP Wrapper을 사용한다.)

## 2. 다운로드한 파일 설치
[autoupdate.zip](https://github.com/asmtron/rdpwrap/raw/master/autoupdate.zip) 파일을 받아서 "%ProgramFiles%\RDP Wrapper" 경로에 압축을 푼다.

## 3. 부팅시 자동 실행 설정
부팅시 autoupdate.bat의 자동실행을 활성화 하기 위해서, 아래의 파일을 관리자 권한으로 실행시킨다.

```
"%ProgramFiles%\RDP Wrapper\helper\autoupdate__enable_autorun_on_startup.bat"
```

## 4. Windows Defender 설정

바이러스 백신 또는 Windows Defender의 설정에서 "% ProgramFiles % \ RDP Wrapper"폴더의 제외를 설정하여 RDP 래퍼 파일의 삭제를 방지한다.(적용하지 않아도 동작에 문제 없는것 같음)

## 5. 실행
이제 autoupdate.bat 파일을 사용하여 RDP 래퍼를 설치하고 업데이트 할 수 있도록 설정이 완료되었다. 관리자 권한으로 autoupdate.bat을 실행시킨다..

```
"%ProgramFiles%\RDP Wrapper\autoupdate.bat"
```

[not supported]가 [supported]로 바뀐것을 확인한다. 추가적으로 재부팅을 해주면 좀 더 안정적으로 동작하는것 같았다.

# 참고
원문 링크 : [INSTALL of RDP Wrapper and Autoupdater](https://github.com/asmtron/rdpwrap/blob/77e846f8bace8ac4f91ed0c2332aa1604beef5f6/binary-download.md)
