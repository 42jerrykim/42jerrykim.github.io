---
image: "tmp_wordcloud.png"
categories:
- Shell
date: "2019-02-13T00:00:00Z"
description: "파일 경로에서 디렉터리 경로와 파일 이름을 분리하는 방법을 설명합니다. sed를 이용한 디렉터리 추출, basename을 이용한 파일명·확장자 추출, bash 함수 예제와 주의사항을 150자 분량으로 정리합니다."
redirect_from:
- /2019/02/13/
tags:
- Shell
- Bash
- Graph
- String
- Sci-Fi
- Process
- Command
- Design-Pattern
- Blog
- 블로그
- Technology
- 기술
- Web
- 웹
- Tutorial
- 가이드
- Review
- 리뷰
- Markdown
- 마크다운
- Implementation
- Guide
- Productivity
- 생산성
- Education
- 교육
- Reference
- 참고
- Best-Practices
- Documentation
- 문서화
- Open-Source
- 오픈소스
- Innovation
- 혁신
- Troubleshooting
- 트러블슈팅
- Configuration
- 설정
- How-To
- Tips
- Comparison
- 비교
- Career
- 커리어
- Workflow
- 워크플로우
- Migration
- 마이그레이션
- Hardware
- 하드웨어
- Cloud
- 클라우드
- Mobile
- 모바일
- Deployment
- Error-Handling
- Performance
- 성능
- Testing
- 테스트
title: '[Shell] Extract directory path and file name from file path'
---



## Extract directory path
### Use sed
`sed` (stream editor) is a Unix utility that parses and transforms text
~~~ shell
function extract_directory_path() {
    echo "${1}" | sed -r "s/(.+)\/.+/\1/"
}

FILE_PATH=/test/test/test/asdf.txt
RES=`extract_directory_path ${FILE_PATH}`

echo RES
~~~

### About sed
`sed` (stream editor) is a Unix utility that parses and transforms text, using a simple, compact programming language. sed was developed from 1973 to 1974 by Lee E. McMahon of Bell Labs,[1] and is available today for most operating systems.[2] sed was based on the scripting features of the interactive editor ed ("editor", 1971) and the earlier qed ("quick editor", 1965?66). sed was one of the earliest tools to support regular expressions, and remains in use for text processing, most notably with the substitution command. Popular alternative tools for plaintext string manipulation and "stream editing" include AWK and Perl.

## Extract file name
### Use sed
``` shell
#!/bin/bash
function extract_file_name() {
    echo "${1}" | sed -r "s/.*\///"
}

FILE_PATH=/test/test/test/asdf.txt
RES=`extract_file_name ${FILE_PATH}`

echo RES
```

### Use basename
Use the `basename` command to extract the filename from the path
``` shell
#!/bin/bash
FILE_PATH=/test/test/test/asdf.txt
RES=`extract_file_name ${FILE_PATH}`

echo RES`
```
### About basename
basename is a standard computer program on Unix and Unix-like operating systems. When basename is given a pathname, it will delete any prefix up to the last slash ('/') character and return the result. basename is described in the Single UNIX Specification and is primarily used in shell scripts.
#### Usage
The Single UNIX Specification specification for basename is.
~~~ bash
$ basename string [suffix]
~~~
* string : A pathname
* suffix : If specified, basename will also delete the suffix.

#### Examples

basename will retrieve the last name from a pathname ignoring any trailing slashes
~~~ bash
$ basename /home/jsmith/base.wiki 
base.wiki

$ basename /home/jsmith/
jsmith

$ basename /
/
~~~
basename can also be used to remove the end of the base name, but not the complete base name

~~~ bash
$ basename /home/jsmith/base.wiki .wiki
base

$ basename /home/jsmith/base.wiki ki
base.wi

$ basename /home/jsmith/base.wiki base.wiki
base.wiki
~~~
