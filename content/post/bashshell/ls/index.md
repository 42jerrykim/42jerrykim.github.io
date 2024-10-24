---
image: "tmp_wordcloud.png"
title: "ls - 파일 목록 출력"
date: 2022-01-01
categories: "Shell"
---

## 사용법

ls [옵션] [파일]

## 옵션

* -a, --all : .을 포함한 디렉토라 안의 모든 내용을 출력한다.
* ​-b, --escape : 알파벳 형식의 리스트를 출력하며 그래픽 문자가 아닌 문자들을 사용한다. C와 같이 역 슬래쉬 문자('\')와 함께 오는 문자들을 사용한다.
* --block-size=SIZE : 지정한 바이트 SIZE만큼 블록을 사용한다.
* -B​, --ignore-backups : 파일 끝이 '~'인 백업 파일을 출력하지 않는다.​  
* -c, --time=ctime, --time=status : -it옵션과 함께 마지막 변경시간을 정열해서 출력하며 -l 옵션과 함께 마지막 변경된 시간을 출력하고 이름을 기준으로 정렬한다.​  
* -C​, --format=vertical : 열의 엔트리를 출력한다.​ 정열 방식을 세로로 한다.​
* ```--color[=WHEN]``` :​파일의 타입을 색깔로 구별할지 정한다. WHEN 값은 'never', 'always', 'auto'이다. 
* ​​-d, --directory : 경로안의 내용을 나열하지 않고, 그 경로를 출력한다.(쉘스크립트에서 유용하게 사용)​
* *-D, --dired : emacs를 위한 출력 형태를 생성한다.
* -f​ : 경로 내용을 정렬하지 않는다. 디스크에 저장된 순으로 보여주며 -a와 -U옵션과 같으며 -ls, --color 옵션을 비활성화하며 -l, -s, -f옵션들과는 반대의 뜻이다.
* -F​, clasify : 파일 형식을 알리는 문자를 각 파일 뒤에 ```*, /, =, >, @, |``` 중에 하나를 추가한다. 실행파일은 ```'*'```, 경로는 ```'/'```,

심블릭 링크는 ```'@'```, FIFO는 ```'|'```, 소켓은 ```'='```이며 일반 파일에는 추가되지 않는다.

## 예시

* ​--file-type : 위의 옵션과 비슷하나 실행 파일뒤에 추가되는 '*'은 붙지 않는다.​
* --format=[WORD] : 옵션 대신 워드 포멧을 지정하여 출력, -x는 across, -m은 commas, -x는 horizontal, -l은 long, -1은 single-coluumn, -I는 verbose 그리고 -C는 vertical을 지정하여 출력할 수 있다.
* --full-time : 시간을 간략히 표시하지 않고 모두 보여준다.
* -g : 소유자의 리스트를 출력하지 않으며 유닉스와의 호환성을 위해 존재.
* --group-directories-first : 파일 이전에 그룹 디렉토리를 먼저 출력.
* ​-G, --no-group : 자세한 리스트 형식으로 출력하나 group 정보를 제외한다.
* -h, --human-readable : 사람이 읽기 쉬운 크기로 출력한다.
* --si : 위 명령어와 비슷하지만 1024단위가 아닌 1000단위 형식으로 출력한다.
* --H, --dereference-command-line : 심볼릭 링크일 경우 실제로 참조하는 목록을 출력한다.
* --hide=[PATTERN] : 지정한 PATTERN과 매칭되는 리스트를 숨긴다.
* --indicator-style=[WORD] : 목록 이름에 WORD 스타일의 지시자를 추가한다. none, slash, file-type, classif
* -i, --inode : ​각 파일 왼쪽에 색인 번호를 보여준다.
* ​-k, --kilobytes : 파일 크기가 나열 되면 kb 단위로 보여준다. --block-size=1K와 비슷함
* -l, --format=long, --format=cerbose : 파일 나열에 있어, 파일형태, 사용권한, 하드링크 번호, 이름 크기 시간까지 자세하게 긴 리스트의 포맷으로 출력한다. 시간이 6달 전이면 시간은 생략되며 연도가 표시된다.
* -L, --dereference : 심볼링 링크의 파일 정보를 파일그대로 출력한다.
* -m, --format=commas : 파일 가로로 나열할 수 있는 만큼 최대한 나열한다.
* -n, --numeric-uid-gid : 이름의 나열에서 UID, GID 번호를 사용함
* -N, --liternal : 본래의 이름으로 출력, 이름이 영문이 아닌 경우 '\'를 붙여서 출력한다. ​
* -p : 파일 형태를 지시하는 문자를 각 파일에 추가한다.​
* -q​, --hide-control-chars : 파일 이름에 그래픽 문자가 아닌 것이 있으면, '?'로 표시한다.
* -Q, --quote-name : 목록에 ""를 사용하여 출력하며 N옵션의 반대
* ​-r, --reverse : 정열 순서를 내림차순으로 한다.
* -R, --recursive : 하위 디렉토리와 그 안에 있는 모든 파일들도 나열한다.
* ​-s, --size : 파일 크기를 1kb 단위로 나타낸다.
* -S, --sort=size : 파일​ 크기를 기준으로 가장 큰 파일부터 정열해서 출력한다.
* ​-t, --sort=time : 파일을 시간순으로 출력하며 최근 파일이 먼저 출력된다.
* -T, --tabsize cols : 탭이 사용될 때 cols값으로 지정하며 초기값은 8이다. 0으로 지정되면 탭 문자는 무시된다.
* -i, --ignore=pattern : pattern 지정된 파일들은 목록에서 제외. 다만 명령 행에서 그 파일이 지정되면 출력된다.
* -u, --time=atime, --time=access, -time=use : 파일 사용 시간 순으로 정열.
* -x, --format=across, --format=horizontal : 정열 방식을 가로로하여 출력.
* -X, --sort=extension : 파일 확장자 순으로 정열. 확장자가 없는 파일이 먼저 나열 되며 확장자를 기준으로 알파벳 순으로 출력.
* -1, --format=single-column : 한 줄에 하나의 파일을 출력한다.
* --help : 도움말 출력.
* --version : 버전 정보 출력.
