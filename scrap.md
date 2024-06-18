
`GDI+` 대신 `BITMAPINFO`를 사용하여 비트맵 이미지를 표시하고, 윈도우의 크기에 따라 이미지를 동적으로 조정하는 코드를 작성할 수 있다. 이를 위해 `StretchBlt` 함수를 사용하여 비트맵을 그릴 때 크기를 조정하고, `WM_SIZE` 메시지를 처리하여 윈도우 크기가 변경될 때 이미지를 다시 그리도록 한다.

### 주요 단계

1. **비트맵 로드 및 초기화**
2. **윈도우 클래스 등록 및 창 생성**
3. **윈도우 프로시저에서 `WM_SIZE` 메시지 처리**
4. **비율 유지하며 비트맵 그리기**

### 코드 예제

```cpp
#include <windows.h>
#include <stdio.h>

BITMAPINFOHEADER createBitmapHeader(int width, int height)
{
    BITMAPINFOHEADER bi;

    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = width;
    bi.biHeight = -height;  // top-down DIB
    bi.biPlanes = 1;
    bi.biBitCount = 24;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;
    bi.biXPelsPerMeter = 0;
    bi.biYPelsPerMeter = 0;
    bi.biClrUsed = 0;
    bi.biClrImportant = 0;

    return bi;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static HBITMAP hBitmap = NULL;
    static BITMAPINFOHEADER bi;
    static int imageWidth = 2560;
    static int imageHeight = 1440;

    switch (uMsg)
    {
        case WM_CREATE:
        {
            // 비트맵 로드 (여기서는 파일에서 로드하지 않고 메모리에서 직접 생성)
            bi = createBitmapHeader(imageWidth, imageHeight);

            // 예제용으로 빨간색으로 채운 비트맵 생성
            HDC hdc = GetDC(hwnd);
            HDC hdcMem = CreateCompatibleDC(hdc);
            hBitmap = CreateCompatibleBitmap(hdc, imageWidth, imageHeight);
            SelectObject(hdcMem, hBitmap);

            // 비트맵을 빨간색으로 초기화
            RECT rect = {0, 0, imageWidth, imageHeight};
            HBRUSH hBrush = CreateSolidBrush(RGB(255, 0, 0));
            FillRect(hdcMem, &rect, hBrush);

            DeleteObject(hBrush);
            DeleteDC(hdcMem);
            ReleaseDC(hwnd, hdc);

            return 0;
        }
        case WM_SIZE:
        {
            InvalidateRect(hwnd, NULL, TRUE); // 창 크기 변경 시 화면 갱신
            return 0;
        }
        case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            if (hBitmap)
            {
                RECT clientRect;
                GetClientRect(hwnd, &clientRect);

                int winWidth = clientRect.right;
                int winHeight = clientRect.bottom;

                // 이미지 비율 유지
                float imageRatio = static_cast<float>(imageWidth) / imageHeight;
                float windowRatio = static_cast<float>(winWidth) / winHeight;

                int drawWidth, drawHeight;

                if (windowRatio > imageRatio)
                {
                    drawHeight = winHeight;
                    drawWidth = static_cast<int>(drawHeight * imageRatio);
                }
                else
                {
                    drawWidth = winWidth;
                    drawHeight = static_cast<int>(drawWidth / imageRatio);
                }

                int offsetX = (winWidth - drawWidth) / 2;
                int offsetY = (winHeight - drawHeight) / 2;

                HDC hdcMem = CreateCompatibleDC(hdc);
                SelectObject(hdcMem, hBitmap);

                StretchBlt(hdc, offsetX, offsetY, drawWidth, drawHeight, hdcMem, 0, 0, imageWidth, imageHeight, SRCCOPY);

                DeleteDC(hdcMem);
            }

            EndPaint(hwnd, &ps);
            return 0;
        }
        case WM_DESTROY:
        {
            if (hBitmap)
            {
                DeleteObject(hBitmap);
            }
            PostQuitMessage(0);
            return 0;
        }
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    const wchar_t CLASS_NAME[]  = L"Sample Window Class";

    WNDCLASS wc = {};
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        L"Display Bitmap",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL)
    {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
```

### 설명

1. **비트맵 로드 및 초기화**
   - `createBitmapHeader` 함수를 통해 비트맵 헤더를 생성하고, 메모리에서 직접 빨간색으로 채워진 비트맵을 생성한다.

2. **윈도우 클래스 등록 및 창 생성**
   - 윈도우 클래스를 등록하고 창을 생성한다.

3. **윈도우 프로시저에서 `WM_SIZE` 메시지 처리**
   - `WM_SIZE` 메시지를 처리하여 창 크기가 변경될 때 화면을 갱신한다.

4. **비율 유지하며 비트맵 그리기**
   - `WM_PAINT` 메시지에서 `StretchBlt` 함수를 사용하여 비트맵을 그리며, 창의 크기에 따라 비트맵의 크기를 조정한다.
   - 창의 클라이언트 영역과 이미지의 비율을 비교하여 비율을 유지한 상태로 이미지를 중앙에 배치한다.

이 예제는 기본적으로 메모리에서 생성된 비트맵을 사용하지만, 실제로는 파일에서 비트맵을 로드하여 사용할 수 있다. 파일에서 비트맵을 로드하는 경우, `LoadImage` 함수나 다른 비트맵 로드 함수를 사용할 수 있다.


윈도우 창의 크기를 변경할 때 초기 비율(예: 2560x1440)을 유지하면서 크기를 조정하려면 `WM_SIZING` 메시지를 처리하여 사용자가 창 크기를 조정할 때 비율이 유지되도록 해야 한다. 이를 위해 사용자가 크기를 조정할 때 새로운 크기를 계산하고 설정하는 코드를 작성할 수 있다.

다음은 그 방법을 보여주는 코드 예제이다.

### 코드 예제

```cpp
#include <windows.h>
#include <stdio.h>

BITMAPINFOHEADER createBitmapHeader(int width, int height)
{
    BITMAPINFOHEADER bi;

    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = width;
    bi.biHeight = -height;  // top-down DIB
    bi.biPlanes = 1;
    bi.biBitCount = 24;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;
    bi.biXPelsPerMeter = 0;
    bi.biYPelsPerMeter = 0;
    bi.biClrUsed = 0;
    bi.biClrImportant = 0;

    return bi;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static HBITMAP hBitmap = NULL;
    static BITMAPINFOHEADER bi;
    static int imageWidth = 2560;
    static int imageHeight = 1440;
    static float aspectRatio = 2560.0f / 1440.0f;

    switch (uMsg)
    {
        case WM_CREATE:
        {
            // 비트맵 로드 (여기서는 파일에서 로드하지 않고 메모리에서 직접 생성)
            bi = createBitmapHeader(imageWidth, imageHeight);

            // 예제용으로 빨간색으로 채운 비트맵 생성
            HDC hdc = GetDC(hwnd);
            HDC hdcMem = CreateCompatibleDC(hdc);
            hBitmap = CreateCompatibleBitmap(hdc, imageWidth, imageHeight);
            SelectObject(hdcMem, hBitmap);

            // 비트맵을 빨간색으로 초기화
            RECT rect = {0, 0, imageWidth, imageHeight};
            HBRUSH hBrush = CreateSolidBrush(RGB(255, 0, 0));
            FillRect(hdcMem, &rect, hBrush);

            DeleteObject(hBrush);
            DeleteDC(hdcMem);
            ReleaseDC(hwnd, hdc);

            return 0;
        }
        case WM_SIZE:
        {
            InvalidateRect(hwnd, NULL, TRUE); // 창 크기 변경 시 화면 갱신
            return 0;
        }
        case WM_SIZING:
        {
            RECT* rect = (RECT*)lParam;
            int width = rect->right - rect->left;
            int height = rect->bottom - rect->top;
            float currentAspectRatio = (float)width / (float)height;

            if (currentAspectRatio > aspectRatio) {
                // 너비에 비례하여 높이를 조정
                width = (int)(height * aspectRatio);
                rect->right = rect->left + width;
            } else {
                // 높이에 비례하여 너비를 조정
                height = (int)(width / aspectRatio);
                rect->bottom = rect->top + height;
            }

            return TRUE;
        }
        case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            if (hBitmap)
            {
                RECT clientRect;
                GetClientRect(hwnd, &clientRect);

                int winWidth = clientRect.right;
                int winHeight = clientRect.bottom;

                // 이미지 비율 유지
                float imageRatio = static_cast<float>(imageWidth) / imageHeight;
                float windowRatio = static_cast<float>(winWidth) / winHeight;

                int drawWidth, drawHeight;

                if (windowRatio > imageRatio)
                {
                    drawHeight = winHeight;
                    drawWidth = static_cast<int>(drawHeight * imageRatio);
                }
                else
                {
                    drawWidth = winWidth;
                    drawHeight = static_cast<int>(drawWidth / imageRatio);
                }

                int offsetX = (winWidth - drawWidth) / 2;
                int offsetY = (winHeight - drawHeight) / 2;

                HDC hdcMem = CreateCompatibleDC(hdc);
                SelectObject(hdcMem, hBitmap);

                StretchBlt(hdc, offsetX, offsetY, drawWidth, drawHeight, hdcMem, 0, 0, imageWidth, imageHeight, SRCCOPY);

                DeleteDC(hdcMem);
            }

            EndPaint(hwnd, &ps);
            return 0;
        }
        case WM_DESTROY:
        {
            if (hBitmap)
            {
                DeleteObject(hBitmap);
            }
            PostQuitMessage(0);
            return 0;
        }
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    const wchar_t CLASS_NAME[]  = L"Sample Window Class";

    WNDCLASS wc = {};
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    // 클라이언트 영역의 크기를 2560x1440으로 설정
    RECT clientRect = { 0, 0, 2560, 1440 };
    AdjustWindowRectEx(&clientRect, WS_OVERLAPPEDWINDOW, FALSE, 0);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        L"Display Bitmap",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 
        clientRect.right - clientRect.left, // 조정된 너비
        clientRect.bottom - clientRect.top, // 조정된 높이
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL)
    {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
```

### 설명

1. **비트맵 로드 및 초기화**
   - 비트맵 헤더를 생성하고, 메모리에서 빨간색으로 채워진 비트맵을 생성한다.

2. **윈도우 클래스 등록 및 창 생성**
   - 윈도우 클래스를 등록하고, `AdjustWindowRectEx` 함수를 사용하여 클라이언트 영역의 크기를 2560x1440으로 맞추기 위해 전체 윈도우 크기를 조정한다.

3. **윈도우 프로시저에서 `WM_SIZE` 및 `WM_SIZING` 메시지 처리**
   - `WM_SIZE` 메시지를 처리하여 창 크기 변경 시 화면을 갱신한다.
   - `WM_SIZING` 메시지를 처리하여 사용자가 창의 크기를 변경할 때, 초기 비율을 유지하도록 한다. 사용자가 크기를 조정할 때 새로운 크기를 계산하고 설정한다.

4. **비율 유지하며 비트맵 그리기**
   - `WM_PAINT` 메시지에서 `StretchBlt` 함수를 사용하여 비트맵을 그리며, 창의 크기에 따라 비트맵의 크기를 조정한다.
   - 창의 클라이언트 영역과 이미지의 비율을 비교하여 비율을 유지한 상태로 이미지를 중앙에 배치한다.

이 코드는 사용자가 창 크기를 변경할 때 초기 비율을 유지하도록 하며, 이미지가 올바르게 비율을 유지하며 표시되도록 한다.






윈도우 내부의 비율을 유지하도록 변경하기 위해 `WM_SIZING` 메시지를 처리하여 사용자가 창 크기를 조정할 때 내부 비율을 유지하도록 할 수 있다. 이를 위해 창의 크기 조정 범위 내에서 비율을 유지하면서 클라이언트 영역의 크기를 조정하는 코드를 작성할 수 있다.

### 코드 예제

```cpp
#include <windows.h>
#include <stdio.h>

BITMAPINFOHEADER createBitmapHeader(int width, int height)
{
    BITMAPINFOHEADER bi;

    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = width;
    bi.biHeight = -height;  // top-down DIB
    bi.biPlanes = 1;
    bi.biBitCount = 24;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;
    bi.biXPelsPerMeter = 0;
    bi.biYPelsPerMeter = 0;
    bi.biClrUsed = 0;
    bi.biClrImportant = 0;

    return bi;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static HBITMAP hBitmap = NULL;
    static BITMAPINFOHEADER bi;
    static int imageWidth = 2560;
    static int imageHeight = 1440;
    static float aspectRatio = 2560.0f / 1440.0f;

    switch (uMsg)
    {
        case WM_CREATE:
        {
            // 비트맵 로드 (여기서는 파일에서 로드하지 않고 메모리에서 직접 생성)
            bi = createBitmapHeader(imageWidth, imageHeight);

            // 예제용으로 빨간색으로 채운 비트맵 생성
            HDC hdc = GetDC(hwnd);
            HDC hdcMem = CreateCompatibleDC(hdc);
            hBitmap = CreateCompatibleBitmap(hdc, imageWidth, imageHeight);
            SelectObject(hdcMem, hBitmap);

            // 비트맵을 빨간색으로 초기화
            RECT rect = {0, 0, imageWidth, imageHeight};
            HBRUSH hBrush = CreateSolidBrush(RGB(255, 0, 0));
            FillRect(hdcMem, &rect, hBrush);

            DeleteObject(hBrush);
            DeleteDC(hdcMem);
            ReleaseDC(hwnd, hdc);

            return 0;
        }
        case WM_SIZE:
        {
            InvalidateRect(hwnd, NULL, TRUE); // 창 크기 변경 시 화면 갱신
            return 0;
        }
        case WM_SIZING:
        {
            RECT* rect = (RECT*)lParam;
            int width = rect->right - rect->left;
            int height = rect->bottom - rect->top;

            // 클라이언트 영역의 크기를 가져옴
            RECT clientRect;
            GetClientRect(hwnd, &clientRect);
            int clientWidth = clientRect.right - clientRect.left;
            int clientHeight = clientRect.bottom - clientRect.top;

            // 현재 창 스타일을 가져옴
            DWORD dwStyle = GetWindowLong(hwnd, GWL_STYLE);
            DWORD dwExStyle = GetWindowLong(hwnd, GWL_EXSTYLE);

            // 창 크기를 조정하여 클라이언트 영역의 크기를 얻음
            RECT newRect = {0, 0, clientWidth, clientHeight};
            AdjustWindowRectEx(&newRect, dwStyle, FALSE, dwExStyle);

            // 조정된 창 크기를 사용하여 비율을 유지하도록 조정
            int newWidth = newRect.right - newRect.left;
            int newHeight = newRect.bottom - newRect.top;

            float currentAspectRatio = (float)newWidth / (float)newHeight;

            if (currentAspectRatio > aspectRatio) {
                // 높이에 비례하여 너비를 조정
                newWidth = (int)(newHeight * aspectRatio);
                rect->right = rect->left + newWidth;
            } else {
                // 너비에 비례하여 높이를 조정
                newHeight = (int)(newWidth / aspectRatio);
                rect->bottom = rect->top + newHeight;
            }

            return TRUE;
        }
        case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            if (hBitmap)
            {
                RECT clientRect;
                GetClientRect(hwnd, &clientRect);

                int winWidth = clientRect.right;
                int winHeight = clientRect.bottom;

                // 이미지 비율 유지
                float imageRatio = static_cast<float>(imageWidth) / imageHeight;
                float windowRatio = static_cast<float>(winWidth) / winHeight;

                int drawWidth, drawHeight;

                if (windowRatio > imageRatio)
                {
                    drawHeight = winHeight;
                    drawWidth = static_cast<int>(drawHeight * imageRatio);
                }
                else
                {
                    drawWidth = winWidth;
                    drawHeight = static_cast<int>(drawWidth / imageRatio);
                }

                int offsetX = (winWidth - drawWidth) / 2;
                int offsetY = (winHeight - drawHeight) / 2;

                HDC hdcMem = CreateCompatibleDC(hdc);
                SelectObject(hdcMem, hBitmap);

                StretchBlt(hdc, offsetX, offsetY, drawWidth, drawHeight, hdcMem, 0, 0, imageWidth, imageHeight, SRCCOPY);

                DeleteDC(hdcMem);
            }

            EndPaint(hwnd, &ps);
            return 0;
        }
        case WM_DESTROY:
        {
            if (hBitmap)
            {
                DeleteObject(hBitmap);
            }
            PostQuitMessage(0);
            return 0;
        }
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    const wchar_t CLASS_NAME[]  = L"Sample Window Class";

    WNDCLASS wc = {};
    wc.lpfnWndProc   = WindowProc;
    wc.hInstance     = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    // 클라이언트 영역의 크기를 2560x1440으로 설정
    RECT clientRect = { 0, 0, 2560, 1440 };
    AdjustWindowRectEx(&clientRect, WS_OVERLAPPEDWINDOW, FALSE, 0);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        L"Display Bitmap",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 
        clientRect.right - clientRect.left, // 조정된 너비
        clientRect.bottom - clientRect.top, // 조정된 높이
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL)
    {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
```

### 설명

1. **비트맵 로드 및 초기화**
   - 비트맵 헤더를 생성하고, 메모리에서 빨간색으로 채워진 비트맵을 생성한다.

2. **윈도우 클래스 등록 및 창 생성**
   - 윈도우 클래스를 등록하고, `AdjustWindowRectEx` 함수를 사용하여 클라이언트 영역의 크기를 2560x1440으로 맞추기 위해 전체 윈도우 크기를 조정한다.

3. **윈도우 프로시저에서 `WM_SIZE` 및 `WM_SIZING` 메시지 처리**
   - `WM_SIZE` 메시지를 처리하여 창 크기 변경 시 화면을 갱신한다.
   - `WM_SIZING` 메시지를 처리하여 사용자가 창의 크기를 변경할 때, 내부 비율을 유지하도록 한다. 사용자가 크기를 조정할 때 새로운 크기를 계산하고 설정한다.

4. **비율 유지하며 비트맵 그리기**
   - `WM_PAINT` 메시지에서 `StretchBlt` 함수를 사용하여 비트맵을 그리며, 창의 크기에 따라 비트맵의 크기를 조정한다.
   - 창의 클라이언트 영역과 이미지의 비율을 비교하여 비율을 유지한 상태로 이미지를 중앙에 배치한다.

이 코드는 사용자가 창 크기를 변경할 때 내부 비율을 유지하도록 하며, 이미지가 올바르게 비율을 유지하며 표시되도록 한다.
