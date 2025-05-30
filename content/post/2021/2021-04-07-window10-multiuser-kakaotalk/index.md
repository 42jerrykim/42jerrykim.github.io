---
image: "tmp_wordcloud.png"
categories: KakalTalk
date: "2021-04-07T00:00:00Z"
tags:
- Windows
- Account
- KakaoTalk
title: '[KakaoTalk] Windows 10 다른 사용자도 카카오톡을 사용할 수 있도록 사용권한 주기'
---

하나의 윈도우 PC를 여러 사람이 사용하는 경우에는 사용자를 추가하는것이 좋다. 사용자끼리 설치된 프로그램은 공유가 되지만 정보들은 구분이 되어 있어 다른 사용자가 내 정보를 보지못하도록 할 수 있다.

## 문제 상황

다른 프로그램들은 대부분 잘 실행이 되는 반면 카카오톡은 접근 권한이 없다며 실행이 되지 않는다.

## 해결 방법

[카카오톡 실행 안됨 문제(지정한 장치, 경로 또는 파일에 엑세스할 수 없습니다.)](https://doya-life.tistory.com/32)을 참고하여 권한을 추가한다.

권한을 추가해도 아래의 팝업처럼 **'응용프로그램이 올바로 시작될 수 없습니다(0xc0000022). 확인을 클릭하여 응용프로그램을 닫습니다.'**가 발생을 한다면 카카오톡을 재 설치 하고 권한을 추가 하면 문제가 해결 된다.

| ![문제 발생](/assets/images/2021/2021-04-07-122050.png) |
|:--:|
| *문제 발생시 팝업창* |

## 주의 사항

카카오톡이 업데이트 될때마다 위 작업을 해 주어야 한다