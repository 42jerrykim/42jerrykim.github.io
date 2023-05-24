---
title: "[Linux] 용량 측정할때 Symlink도 포함하기"
category: 
- Linux
tag:
- Linux
- Symlink
- du
- df
- File
- Size
- Direstory
- Link
# header:
#   teaser: /assets/images/2023/cover.jpg
---

심링크(symlink)는 파일 시스템에서 사용되는 특별한 파일 유형입니다. 심링크는 파일이나 디렉터리에 대한 다른 이름을 제공합니다. 심링크는 실제 파일 또는 디렉터리를 가리키는 링크로, 실제 파일을 복사하는 것이 아니라 심링크를 생성하여 그것을 가리킵니다.

용량 측정에 심링크를 포함하려면, 용량 측정 명령어(예: du, df)에 ```-L``` 옵션을 추가하면 됩니다. 이렇게 하면 심링크가 가리키는 실제 파일의 용량이 측정됩니다.

예를 들어, ```du -L /path/to/symlink```를 실행하면 ```/path/to/symlink```가 가리키는 실제 파일의 용량이 측정됩니다.
