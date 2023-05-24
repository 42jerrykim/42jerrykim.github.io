---

title: "PIP 패키지 인스톨 Proxy 환경에서 사용하기"
description: ""
categories: [Proxy]
tags: [Shell, Proxy, PIP]
redirect_from:
  - /2019/04/02/
---



# PIP 패키지 인스톨 Proxy 환경에서 사용하기

아래 명령어는 프록시 설정을 추가한 패키지 인스톨 방법이다.

``` bash
pip install --proxy [Proxy http url] [Package name]
```

위에 보시는 것과 같이 프록시 값을 먼저 설정 후 뒤에 설치할 패키지명을 추가한다. 예를들어 아래와 같이 사용한다.

```bash
pip installl --proxy http://000.111.222.333:4444 Flask
```

이제 정상적으로 인스톨이 수행 될 것입니다.