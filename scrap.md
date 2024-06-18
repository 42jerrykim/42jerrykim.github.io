
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


```
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
```
