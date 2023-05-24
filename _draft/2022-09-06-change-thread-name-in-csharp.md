---
title: "[C#] "
category: 
- CSharp
tag:
- Thread
# header:
#   teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

```csharp
using System;
using System.Runtime.InteropServices;
using System.Threading;

namespace ThreadUtil
{
    public class Thread
    {
        [DllImport("libpthread.so")]
        private static extern IntPtr pthread_self();

        [DllImport("libpthread.so")]
        private  static extern void pthread_setname_np(IntPtr threadHandle, string name);

        public static void SetName(string name)
        {
            IntPtr handle = pthread_self();
            pthread_setname_np(handle, name);

            Thread.CurrentThread.Name = name;
        }
    }
}
```
