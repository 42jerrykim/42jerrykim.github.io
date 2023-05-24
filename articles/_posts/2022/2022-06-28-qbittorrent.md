---
title: "[Torrent] qBittorrent - RSS 자동 다운로드를 위한 Torrent Client 추천"
categories:
- Torrent
tags: 
- qBittorrent
- µTorrent
- ruTorrent
- Transmission
- Torrent
- Windows
- Mac
- Linux
- RSS
- 토렌트
- 다운로드
header:
  teaser: /assets/images/undefined/800px-Qbittorrent_4.1.5.png
---

토렌트를 사용하다 보면 RSS를 사용해서 자동으로 다운로드할 수 있는 기능이 있다. 여러 클라이언트가 있지만 그중에서도 qBittorrent에 대해서 알아보고 자동으로 다운로드할 방법에 대해서 알아본다.

# qBittorrent

|![qBittorrent](/assets/images/undefined/800px-Qbittorrent_4.1.5.png)|
|:---:|
|qBittorrent 화면|

# RSS 자동 다운로드

RSS를 이용해서 자동으로 토렌트를 다운받기 위해서는 아래위 두 단계를 설정해야 한다.

1. RSS 주소 등록
1. 다운로드 규칙 등록

## RSS 등록

qBittorrent를 설치하고 나면 처음 보는 화면에서는 RSS 관련된 화면이 안 보일 수 있다. 아래의 화면처럼 ```보기(V)```메뉴에서 ```RSS 리더(R)```를 선택하면 RSS 관련 화면을 볼 수 있다.

|![](/assets/images/2022/2022-06-28-093524.png)|
|:---:|
|RSS 리더 화면 활성화|

```새 구독```을 눌러서 RSS 주소를 추가한다. 그러면 아래와 같이 다운로드할 수 있는 토렌트 목록을 확인할 수 있다.

|![](/assets/images/2022/2022-06-28-094052.png)|
|:---:|
|다운로드할 수 있는 토렌트 파일 목록|

RSS 주소만 등록하는 것으로는 토렌트 파일을 자동으로 다운로드할 수 없다.

## 다운로드 규칙 등록

자동으로 RSS에 있는 토렌트 파일을 다운로드하기 위해서 규칙을 등록하는 방법을 알아보자. 오른쪽 위에 있는 ```RSS 내려받기 도구``` 버튼을 클릭하고 새 규칙을 추가한다.

|![](/assets/images/2022/2022-06-28-093719.png)|
|:---:|
|규칙 등록|

모든 파일을 다운로드할 것이기 때문에 별다른 규칙을 사용하지 않았다. 중요한 것은 규칙을 적용할 피드를 선택해야 한다는 것이다. 아까 등록했던 피드를 선택하면 된다.

# 추천하지 않는 클라이언트

## µTorrent

|![](/assets/images/undefined/ui-classic-bd3481be0133059729c5a937070f8b69.png)|
|:---:|
|µTorrent 화면|

아주 대중적인 클라이언트이지만 아래와 같은 단점이 있어서 사용하지 않는다.

* 기본적으로 5개의 다운로드만 가능. 늘릴수 있지만 불안정하게 동작함
* RSS를 통한 자동 다운로드 기능이 활성화가 되지 않는다.
* 광고

## ruTorrent

|![ruTorrent](/assets/images/undefined/30dxlTc.png)|
|:---:|
|ruTorrent 화면|

대중적이지는 않지만 리눅스PC에서 사용하기 위해서 꽤 오랜 기간동안 사용했지만 이제는 사용하지 않는다.

* 유지보수가 안되는것 같음
* 완료된 파일을 특정 경로에 저장하는 기능에 버그가 있음
* 완료가 되었어도 다운로드 중이라고 표시되는 버그가 있음

## Transmission

|![](/assets/images/undefined/64b32980-a756-11e9-9bd1-89110eed7c55.png)|
|:---:|
|Transmission Remote 화면|

기능이 간단해서 다운로드 하는것은 좋지만 RSS를 통한 자동 다운로드가 되지 않음