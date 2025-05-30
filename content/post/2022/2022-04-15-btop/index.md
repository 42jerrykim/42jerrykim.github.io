---
image: "tmp_wordcloud.png"
categories:
- Linux
- Monitor
- Util
date: "2022-04-15T00:00:00Z"
header:
  teaser: /assets/images/2022/2022-04-15-122101.png
tags:
- Linux
- Monitor
- CPU
- Disks
- Disk
- Memory
- Processor
- Network
- Processes
- 모니터링
- 모니터
- 사용량
- 프로세스
- 메모리
- 네트워크
- 리눅스
- 디스크
- Resource
- 리소스
title: '[Linux] btop++ - 리눅스용 Processor, Memory, Disks, Network and Processes 모니터'
---

리눅스를 사용할 때 `top`명령어를 사용해서 CPU를 모니터링 해본적이 있는가? 너무 보잘것 없는 UI에 실망한적이 있는가? 다른 리소스의 사용량도 확인 해 보고 싶은 생각은 없었는가? 본 글에서는 PC의 자원은 한 화면헤서 확인 할 수 있는 btop++에 개해서 소개 한다.

btop++을 사용하면 아래의 그림처럼 이쁜 UI와 함꼐 다양한 리소스의 사용량을 모니터링 할 수 있다.

|![/assets/images/2022/2022-04-15-122101.png](/assets/images/2022/2022-04-15-122101.png)|
|:---:|
|Main UI showing details for a selected process|

## btop++

[aristocratos/btop](https://github.com/aristocratos/btop)에 접속 하면 다양한 정보를 확인 할 수 있다.

아래와 같은 대표적인 특징을 가지고 있다.

- bashtop/bpytop 의 C++ 재작성 버전
- 프로세서, 메모리, 디스크, 네트워크, 프로세스 등의 리소스 모니터링 툴
- 사용하기 쉬운 게임 형태의 메뉴 시스템
- 전체 마우스 조작 지원
- 프로세스 필터링 및 소팅, 시그널 보내기 지원
- 네트웍 사용량 그래프, IO