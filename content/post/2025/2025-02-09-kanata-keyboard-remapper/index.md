---
title: "Kanata - Rust로 작성된 강력한 키보드 리매퍼"
date: 2025-02-09
categories:
  - Tool
tags:
  - Keyboard
  - Remapper
  - Rust
  - Windows
  - Linux
  - MacOS
image: "image.png"
---

Kanata는 Rust 프로그래밍 언어로 작성된 강력한 키보드 리매퍼입니다. Windows, Linux, MacOS 등 다양한 운영체제를 지원하며, 키보드의 동작을 사용자가 원하는 대로 커스터마이징할 수 있는 도구입니다.

[Kanata GitHub](https://github.com/jtroo/kanata)

## 주요 기능

1. **다중 레이어 지원**

   - 여러 레이어를 만들어 키보드의 기능을 확장할 수 있습니다.
   - 각 레이어마다 다른 키 매핑을 설정할 수 있습니다.

2. **Tap-Hold 기능**
   - 키를 짧게 누르면 한 기능, 길게 누르면 다른 기능을 수행하도록 설정할 수 있습니다.
   - 예: 'a'키를 짧게 누르면 'a'가 입력되고, 길게 누르면 Ctrl 키로 동작

3. **복합 키 설정**
   - 여러 키를 조합하여 새로운 기능을 만들 수 있습니다.
   - 매크로 기능을 통해 복잡한 키 입력을 자동화할 수 있습니다.

4. **설정 파일 기반**
   - 텍스트 기반의 설정 파일을 통해 쉽게 키 매핑을 구성할 수 있습니다.
   - 설정 파일을 공유하여 다른 사용자와 키 매핑을 공유할 수 있습니다.

## 설치 방법

### Windows

```powershell
winget install kanata
```

### Linux

```bash
cargo install kanata
```

### MacOS

```bash
brew install kanata
```

## 기본 설정 예시

```
(defsrc
  esc  1    2    3    4    5    6    7    8    9    0    -    =    bspc
  tab  q    w    e    r    t    y    u    i    o    p    [    ]    \
  caps a    s    d    f    g    h    j    k    l    ;    '    ret
  lsft z    x    c    v    b    n    m    ,    .    /    rsft
  lctl lmet lalt           spc            ralt rmet rctl
)

(deflayer base
  esc  1    2    3    4    5    6    7    8    9    0    -    =    bspc
  tab  q    w    e    r    t    y    u    i    o    p    [    ]    \
  @cap a    s    d    f    g    h    j    k    l    ;    '    ret
  lsft z    x    c    v    b    n    m    ,    .    /    rsft
  lctl lmet lalt           spc            ralt rmet rctl
)
```

## 장점

1. **높은 성능**
   - Rust로 작성되어 매우 빠르고 안정적입니다.
   - 시스템 자원을 적게 사용합니다.

2. **크로스 플랫폼**
   - 주요 운영체제를 모두 지원합니다.
   - 동일한 설정을 여러 환경에서 사용할 수 있습니다.

3. **확장성**
   - 사용자의 필요에 따라 다양한 기능을 추가할 수 있습니다.
   - 커뮤니티를 통한 설정 공유가 활발합니다.

## 결론

Kanata는 키보드 사용을 최적화하고자 하는 사용자들에게 매우 유용한 도구입니다. Rust로 작성되어 안정적이며, 다양한 기능을 제공하여 사용자의 생산성을 크게 향상시킬 수 있습니다. 특히 프로그래머나 파워 유저들에게 강력히 추천하는 도구입니다. 