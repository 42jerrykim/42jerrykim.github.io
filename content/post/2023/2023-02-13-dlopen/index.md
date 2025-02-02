---
image: "tmp_wordcloud.png"
date: "2023-02-13T00:00:00Z"
tag:
- Cpp
- dlopen
- dlclose
- dlerror
title: '[C/C++] gcc로 dlopen 하는 방법'

---

dlopen을 사용하는 이유는 프로그램이 실행되는 동안 동적으로 라이브러리를 로드하거나 언로드하고 함수를 호출할 수 있기 때문입니다. 또한, 라이브러리를 동적으로 로딩하면 그 라이브러리의 코드를 전체 프로그램의 코드에 미리 포함시키지 않고도 필요할 때마다 로드할 수 있기 때문입니다.

|![](/plantuml/dlopen-class-diagram.svg)|
|:---:|
|클래스 다이어그램|

|![](/plantuml/dlopen-sequence-diagram.svg)|
|:---:|
|시퀀스 다이어그램|


이제 예시 코드를 작성해보겠습니다. 이 코드는 라이브러리를 동적으로 로딩하는 예시입니다.

여기서 ```[executable_name]```은 실행 파일의 이름이고 ```[source_file]```은 소스 파일의 이름입니다.

```c
#include <dlfcn.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    char *lib_name;

    if (argc < 2) {
        printf("Usage: %s <library_name>\\n", argv[0]);
        return 1;
    }

    lib_name = argv[1];

    void *handle;
    handle = dlopen(lib_name, RTLD_NOW);
    if (!handle) {
        printf("Error opening library: %s\\n", dlerror());
        return 1;
    }

    printf("Library %s loaded successfully\\n", lib_name);
    dlclose(handle);
    return 0;
}

```

이 코드를 컴파일하기 위해서는 `gcc`를 사용해야 합니다. 다음의 명령을 사용하여 소스 파일을 컴파일할 수 있습니다.

```bash
gcc -o [executable_name] [source_file] -ldl
```

위에서 생성한 실행 파일(executable_name)을 실행하기 위해서는 다음과 같은 명령을 사용할 수 있습니다.

```bash
./[executable_name] [library_name]
```

여기서 `[executable_name]`은 생성한 실행 파일의 이름이고 `[library_name]`은 동적으로 로드할 라이브러리의 이름입니다.