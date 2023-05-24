---
title: "[C#] Plugin 구조를 위한 Custom AssemblyLoadContext 만들기"
categories:
  - .NET
tags:
  - Reflection
  - Plugin
  - AssemblyLoadContext
  - AssemblyDependencyResolver
  - Dll
  - Loader
  - CSharp
  - .NET
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

다른 위치에 있는 dll을 pligin으로 사용하려고 할때 dll을 못 찾는 이슈가 발생 할 수 있다.

# 배경
3가지 Dll이 있다고 가정해보자.

* Core.dll
* Plugin.dll
* Library.dll

> Core.dll이 Plugin.dll을 Reflection을 사용하려 로드 한다.
> Plugin.dll은 Library.dll을 사용한다. Plugin.dll과 Library.dll은 같은 위치에 배치되어 있다.

이때 Library.dll을 못 찾는 문제가 발생 한다.

# 해결 방법

## AssemblyDependencyResolver를 사용하는 방법

[.NET Core에서 어셈블리 언로드 기능을 사용하고 디버그하는 방법](https://docs.microsoft.com/ko-kr/dotnet/standard/assembly/unloadability)을 참고해서 Custom으로 어셈블리 로더를 작성 할 수 있다.

``` csharp
using System.Reflection;
using System.Runtime.Loader;

namespace complex
{
    class TestAssemblyLoadContext : AssemblyLoadContext
    {
        private AssemblyDependencyResolver _resolver;

        public TestAssemblyLoadContext(string mainAssemblyToLoadPath) : base(isCollectible: true)
        {
            _resolver = new AssemblyDependencyResolver(mainAssemblyToLoadPath);
        }

        protected override Assembly Load(AssemblyName name)
        {
            string assemblyPath = _resolver.ResolveAssemblyToPath(name);
            if (assemblyPath != null)
            {
                return LoadFromAssemblyPath(assemblyPath);
            }

            return null;
        }
    }
}
```

이런 방식으로 resolver를 구성하여 작성 할 수 있다.

부가적인 문제가 발생 하는 경우에는 아래처럼 Custom으로 resolver를 작성해야 사용하자

## Custom으로 reslover를 작성하는 방법

[AssemblyLoadContext](https://docs.microsoft.com/ko-kr/dotnet/api/system.runtime.loader.assemblyloadcontext) 클래스에는 [Resolving](https://docs.microsoft.com/ko-kr/dotnet/api/system.runtime.loader.assemblyloadcontext.resolving) 이벤트가 있다. 해당 이벤트는 AssemblyLoadContext에 로드 하려고 할 때 어셈블리를 확인하는데 실패하는 경우에 발생 한다.

이를 이용하여 확인에 실패 했을때 같은 위치에 있는 dll을 로드 하는것으로 해결 하는 방법을 생각 할 수 있다.

아래의 코드는 아이디어를 구현한 코드이다.

``` csharp
using System.Reflection;
using System.Runtime.Loader;

namespace complex
{
    public class AssemblyLoader : AssemblyLoadContext
    {
        private const string DllAssemblySuffix = ".dll";
        private static readonly string[] s_suffixes = new string[] {  DllAssemblySuffix };

        private SortedSet<string> _dllDirectories = new SortedSet<string>();

        private HashSet<FileInfo> _assemblyCache = new HashSet<FileInfo>();

        public AssemblyLoader()
        {
            AssemblyLoadContext.Default.Resolving += OnResolving;
        }

        public void AddSearchableDirectory(string directory)
        {
            if (Directory.Exists(directory))
            {
                _dllDirectories.Add(directory);

                foreach (var file in Directory.GetFiles(directory))
                {
                    var info = new FileInfo(file);

                    if (s_suffixes.Contains(info.Extension))
                    {
                        _assemblyCache.Add(info);
                    }
                }
            }
        }

        public void RemoveSearchableDirectory(string directory)
        {
            _dllDirectories.Remove(directory);

            _assemblyCache.RemoveWhere(x => x.DirectoryName == directory);
        }

        private Assembly Resolve(AssemblyName assemblyName)
        {
            foreach (string suffix in s_suffixes)
            {
                var info = _assemblyCache.FirstOrDefault(x => x.Name == assemblyName.Name + suffix);

                if (info != null)
                {
                    return LoadFromAssemblyPath(info.FullName);
                }
            }

            return null;
        }

        private Assembly OnResolving(AssemblyLoadContext context, AssemblyName assemblyName)
        {
            return Resolve(assemblyName);
        }
    }
```

이처럼 Plugin.dll을 로드할때 Library.dll을 확인 하는데 실패하면 OnResolveing이 호출되고 Plugin.dll과 같은 폴더에 있는 dll을 로드 하는 방식으로 문제를 해결 할 수 있다.
