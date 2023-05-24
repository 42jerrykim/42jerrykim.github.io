---
title: "[Plex] Windows에서 Plex media server 재실행하는 스크립트"
category: 
- Plex
tag:
- Plex
- Windows
- Script
- CMD
- Taskkill
- Server
header:
  teaser: /assets/images/2023/plex.png
---

소프트웨어에 문제가 발생했을때, 보통은 재부팅이나 재실행을 하는 경우에 문제가 해결되는 경우가 많다. 그러나 서버에 접근하기 힘들거나 반복적으로 재실행을 하는 경우에는 스크립트를 사용하면 편하다. 본 글에서는 Plex media server를 스크립트로 재 실행 하는 방법에 대해서 알아본다.

# Plex media server 재실행 스크립트

```shell
TASKKILL /f /im "Plex Media Server.exe"
TASKKILL /f /im "PlexScriptHost.exe"
"C:\Program Files (x86)\Plex\Plex Media Server\Plex Media Server.exe"
```

TASKKILL을 사용해서 실행되고 있는 앱을 죽인다.

# 더 좋은 방법

더 좋은 방법은 Python을 작성된 [Plex Checker](https://gitlab.com/Flaming_Keyboard/plex-checker)를 사용하는 것이다. 해당 코드는 Linux와 Windows에서 동작한다. 또한 확실하진 않지만 macOS나 BSD에서도 동작할것으로 예상한다.

해당 코드는 Plex server에 접속해서 반응이 없으면 재시작 하도록 작성되어 있다. 이것의 장점은 Plex server가 중단되었을때만 실행되기 때문에 불필요하기 재시작 하지 않도록 할 수 있다. 추가로 서버가 오프라인이거나 Respond가 중단되는 경우에도 재시작을 할 수 있는 조건을 추가 할 수도 있다.