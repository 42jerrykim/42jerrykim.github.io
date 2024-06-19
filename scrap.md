주어진 색상 팔레트를 사용하여 Jarvis-Judice-Ninke 디더링을 C++로 구현하는 예제를 제공하겠다. 사용할 수 있는 색상 팔레트는 다음과 같다:

- 흰색: (255, 255, 255)
- 검은색: (0, 0, 0)
- 노란색: (255, 255, 0)
- 파란색: (0, 0, 255)
- 빨간색: (255, 0, 0)
- 초록색: (0, 255, 0)
- 오렌지색: (255, 165, 0)

### 1. 헤더 파일 및 유틸리티 함수 정의

먼저, 필요한 헤더 파일을 포함하고 이미지 데이터 처리를 위한 유틸리티 함수를 정의한다.

```cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <cstdint>

using namespace std;

struct Pixel {
    uint8_t b, g, r;
};

// 이미지 데이터를 1차원 벡터로 저장
using Image = vector<Pixel>;

// 이미지 크기
struct Size {
    int width;
    int height;
};

// 색상 팔레트
const vector<Pixel> palette = {
    {255, 255, 255}, // 흰색
    {0, 0, 0},       // 검은색
    {255, 255, 0},   // 노란색
    {0, 0, 255},     // 파란색
    {255, 0, 0},     // 빨간색
    {0, 255, 0},     // 초록색
    {255, 165, 0}    // 오렌지색
};

// 픽셀 값을 클램핑
uint8_t clamp(int value, int min = 0, int max = 255) {
    return static_cast<uint8_t>(std::max(min, std::min(value, max)));
}

// 두 픽셀 간의 유클리드 거리 계산
int colorDistance(const Pixel& p1, const Pixel& p2) {
    return (p1.r - p2.r) * (p1.r - p2.r) +
           (p1.g - p2.g) * (p1.g - p2.g) +
           (p1.b - p2.b) * (p1.b - p2.b);
}

// 가장 가까운 팔레트 색상 찾기
Pixel findClosestPaletteColor(const Pixel& pixel) {
    Pixel closestColor = palette[0];
    int minDistance = colorDistance(pixel, palette[0]);

    for (const auto& color : palette) {
        int distance = colorDistance(pixel, color);
        if (distance < minDistance) {
            minDistance = distance;
            closestColor = color;
        }
    }

    return closestColor;
}

// 픽셀의 색상 차이를 계산
Pixel colorDifference(const Pixel& p1, const Pixel& p2) {
    return Pixel {
        static_cast<uint8_t>(p1.b - p2.b),
        static_cast<uint8_t>(p1.g - p2.g),
        static_cast<uint8_t>(p1.r - p2.r)
    };
}

// 픽셀에 색상 차이를 적용
Pixel applyColorDifference(const Pixel& p, const Pixel& diff, double factor) {
    return Pixel {
        clamp(static_cast<int>(p.b) + static_cast<int>(diff.b * factor)),
        clamp(static_cast<int>(p.g) + static_cast<int>(diff.g * factor)),
        clamp(static_cast<int>(p.r) + static_cast<int>(diff.r * factor))
    };
}
```

### 2. Jarvis-Judice-Ninke 디더링 구현

다음으로, Jarvis-Judice-Ninke 알고리즘을 사용하여 이미지에 디더링을 적용하는 함수를 정의한다.

```cpp
void jarvisJudiceNinkeDithering(Image& img, Size size) {
    const int matrix[3][5] = {
        { 0, 0, 0, 7, 5 },
        { 3, 5, 7, 5, 3 },
        { 1, 3, 5, 3, 1 }
    };
    const int matrixSum = 48; // 3 + 5 + 7 + 5 + 3 + 1 + 3 + 5 + 3 + 1 = 48

    for (int y = 0; y < size.height; ++y) {
        for (int x = 0; x < size.width; ++x) {
            int index = y * size.width + x;
            Pixel oldPixel = img[index];
            
            // 가장 가까운 팔레트 색상으로 양자화
            Pixel newPixel = findClosestPaletteColor(oldPixel);

            img[index] = newPixel;
            Pixel quantError = colorDifference(oldPixel, newPixel);

            // 오류 확산
            for (int dy = 0; dy < 3; ++dy) {
                for (int dx = -2; dx <= 2; ++dx) {
                    if (x + dx >= 0 && x + dx < size.width && y + dy < size.height) {
                        int neighborIndex = (y + dy) * size.width + (x + dx);
                        img[neighborIndex] = applyColorDifference(img[neighborIndex], quantError, matrix[dy][dx + 2] / static_cast<double>(matrixSum));
                    }
                }
            }
        }
    }
}
```

### 3. 메인 함수 및 테스트

마지막으로, 메인 함수에서 이미지를 로드하고 디더링을 적용한 후 결과를 저장하는 코드를 작성한다.

```cpp
int main() {
    // 예제 이미지 데이터 (단순히 1차원 벡터로 초기화)
    Size size = { 5, 5 }; // 5x5 크기의 이미지
    Image img(size.width * size.height, { 128, 128, 128 });

    // Jarvis-Judice-Ninke 디더링 적용
    jarvisJudiceNinkeDithering(img, size);

    // 결과 출력 (예시)
    for (int y = 0; y < size.height; ++y) {
        for (int x = 0; x < size.width; ++x) {
            Pixel p = img[y * size.width + x];
            cout << "(" << (int)p.r << "," << (int)p.g << "," << (int)p.b << ") ";
        }
        cout << endl;
    }

    return 0;
}
```

이 코드는 5x5 크기의 예제 이미지를 Jarvis-Judice-Ninke 디더링 알고리즘을 사용하여 처리하고 결과를 출력한다. 실제 이미지 파일을 처리하려면 이미지 파일을 읽고 쓰는 코드를 추가해야 한다. 이 예제에서는 단순화된 구조로 디더링의 동작 원리를 이해하는 데 집중하였다.



JPEG 이미지를 RGB 데이터의 나열로 변경하여 1차원 벡터에 저장하는 C++ 코드를 작성하기 위해 OpenCV 라이브러리를 사용할 수 있다. 다음은 이미지의 RGB 데이터를 1차원 벡터로 저장하는 예제 코드이다:

```cpp
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>

// JPEG 이미지를 RGB 데이터로 변환하여 1차원 벡터에 저장하는 함수
std::vector<int> jpegToRgb1DArray(const std::string& imagePath) {
    // 이미지 로드
    cv::Mat img = cv::imread(imagePath, cv::IMREAD_COLOR);

    if (img.empty()) {
        std::cerr << "Could not open or find the image" << std::endl;
        return {};
    }

    // 1차원 벡터 초기화
    std::vector<int> rgbArray;

    // RGB 데이터 추출 및 1차원 벡터에 저장
    for (int i = 0; i < img.rows; ++i) {
        for (int j = 0; j < img.cols; ++j) {
            cv::Vec3b pixel = img.at<cv::Vec3b>(i, j);
            rgbArray.push_back(pixel[2]); // R
            rgbArray.push_back(pixel[1]); // G
            rgbArray.push_back(pixel[0]); // B
        }
    }

    return rgbArray;
}

int main() {
    // 예제 이미지 파일 경로
    std::string imagePath = "path_to_your_image.jpeg";

    // 함수 호출
    std::vector<int> rgbArray = jpegToRgb1DArray(imagePath);

    // RGB 데이터 출력 (일부 픽셀만 출력)
    for (size_t i = 0; i < 15; i += 3) {
        std::cout << "Pixel " << i / 3 << ": R=" 
                  << rgbArray[i] << ", G=" 
                  << rgbArray[i + 1] << ", B=" 
                  << rgbArray[i + 2] << std::endl;
    }

    return 0;
}
```

이 코드는 OpenCV를 사용하여 JPEG 이미지를 로드하고, 각 픽셀의 RGB 값을 추출하여 1차원 벡터에 저장한다. 각 픽셀의 RGB 값은 연속적인 세 개의 요소로 저장된다. 예를 들어, 첫 번째 픽셀의 R 값은 `rgbArray[0]`, G 값은 `rgbArray[1]`, B 값은 `rgbArray[2]`에 저장된다.

CMakeLists.txt 파일은 다음과 같이 작성할 수 있다:

```cmake
cmake_minimum_required(VERSION 3.10)
project(JpegToRgb1DArray)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(JpegToRgb1DArray main.cpp)
target_link_libraries(JpegToRgb1DArray ${OpenCV_LIBS})
```

위의 C++ 코드와 CMakeLists.txt 파일을 사용하여 프로젝트를 설정하고 빌드할 수 있다. `path_to_your_image.jpeg`를 실제 이미지 파일 경로로 변경하는 것을 잊지 말자. CMake 빌드 및 실행 방법은 다음과 같다:

```bash
mkdir build
cd build
cmake ..
make
./JpegToRgb1DArray
```

이렇게 하면 JPEG 이미지의 RGB 데이터를 1차원 벡터로 변환하고 출력할 수 있다.





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







Stucki 디더링 알고리즘을 사용한 C++ 코드를 작성해보겠다. Stucki 디더링은 오류를 더 넓은 범위에 걸쳐 분산시켜 부드러운 결과를 제공하는 디더링 알고리즘이다.

```cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

struct Color {
    int r, g, b;
};

Color closestColor(const Color& c) {
    std::vector<Color> palette = {
        {255, 255, 255},  // White
        {0, 0, 0},        // Black
        {0, 255, 0},      // Green
        {0, 0, 255},      // Blue
        {255, 0, 0},      // Red
        {255, 255, 0}     // Yellow
    };

    Color closest = palette[0];
    int minDistance = INT_MAX;

    for (const auto& p : palette) {
        int distance = std::pow(c.r - p.r, 2) + std::pow(c.g - p.g, 2) + std::pow(c.b - p.b, 2);
        if (distance < minDistance) {
            minDistance = distance;
            closest = p;
        }
    }

    return closest;
}

void applyDithering(std::vector<std::vector<Color>>& image) {
    int height = image.size();
    int width = image[0].size();

    std::vector<std::vector<int>> errorR(height, std::vector<int>(width, 0));
    std::vector<std::vector<int>> errorG(height, std::vector<int>(width, 0));
    std::vector<std::vector<int>> errorB(height, std::vector<int>(width, 0));

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            Color oldColor = {
                std::clamp(image[y][x].r + errorR[y][x], 0, 255),
                std::clamp(image[y][x].g + errorG[y][x], 0, 255),
                std::clamp(image[y][x].b + errorB[y][x], 0, 255)
            };

            Color newColor = closestColor(oldColor);
            image[y][x] = newColor;

            int errR = oldColor.r - newColor.r;
            int errG = oldColor.g - newColor.g;
            int errB = oldColor.b - newColor.b;

            std::vector<std::pair<int, int>> offsets = {
                {1, 0}, {2, 0}, {-2, 1}, {-1, 1}, {0, 1}, {1, 1}, {2, 1}, {-2, 2}, {-1, 2}, {0, 2}, {1, 2}, {2, 2}
            };
            std::vector<int> coefficients = {8, 4, 2, 4, 8, 4, 2, 1, 2, 4, 2, 1};

            for (int k = 0; k < offsets.size(); ++k) {
                int newX = x + offsets[k].first;
                int newY = y + offsets[k].second;
                if (newX >= 0 && newX < width && newY >= 0 && newY < height) {
                    errorR[newY][newX] += errR * coefficients[k] / 42;
                    errorG[newY][newX] += errG * coefficients[k] / 42;
                    errorB[newY][newX] += errB * coefficients[k] / 42;
                }
            }
        }
    }
}

int main() {
    int width = 5;
    int height = 5;
    std::vector<std::vector<Color>> image(height, std::vector<Color>(width));

    // 예시 RGB 데이터 초기화
    image[0] = {{100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}};
    image[1] = {{100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}};
    image[2] = {{100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}};
    image[3] = {{100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}};
    image[4] = {{100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}, {100, 150, 200}};

    applyDithering(image);

    // 결과 출력
    for (const auto& row : image) {
        for (const auto& pixel : row) {
            std::cout << "(" << pixel.r << ", " << pixel.g << ", " << pixel.b << ") ";
        }
        std::cout << "\n";
    }

    return 0;
}
```

이 코드는 Stucki 디더링 알고리즘을 사용하여 입력된 RGB 데이터를 처리한다. Stucki 디더링은 오류를 넓게 분산시켜 매우 부드러운 이미지를 생성한다. `closestColor` 함수는 주어진 색상에 가장 가까운 팔레트 색상을 찾고, `applyDithering` 함수는 전체 이미지를 처리하여 디더링을 적용한다. 각 픽셀의 색상 오류를 주변 픽셀에 분산시켜 처리한다.


JPEG 이미지를 RGB 데이터의 나열로 변경하는 C++ 코드를 작성하기 위해 OpenCV 라이브러리를 사용할 수 있다. OpenCV는 이미지 처리를 위한 강력한 라이브러리로, JPEG 이미지를 로드하고 RGB 데이터를 추출하는 작업을 쉽게 할 수 있다.

다음은 C++ 코드 예제이다:

```cpp
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>

// JPEG 이미지를 RGB 데이터로 변환하는 함수
std::vector<std::vector<std::vector<int>>> jpegToRgbArray(const std::string& imagePath) {
    // 이미지 로드
    cv::Mat img = cv::imread(imagePath, cv::IMREAD_COLOR);

    if (img.empty()) {
        std::cerr << "Could not open or find the image" << std::endl;
        return {};
    }

    // 이미지 크기 가져오기
    int rows = img.rows;
    int cols = img.cols;

    // RGB 데이터를 저장할 벡터 초기화
    std::vector<std::vector<std::vector<int>>> rgbArray(rows, std::vector<std::vector<int>>(cols, std::vector<int>(3)));

    // RGB 데이터 추출
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            cv::Vec3b pixel = img.at<cv::Vec3b>(i, j);
            rgbArray[i][j][0] = pixel[2]; // R
            rgbArray[i][j][1] = pixel[1]; // G
            rgbArray[i][j][2] = pixel[0]; // B
        }
    }

    return rgbArray;
}

int main() {
    // 예제 이미지 파일 경로
    std::string imagePath = "path_to_your_image.jpeg";

    // 함수 호출
    std::vector<std::vector<std::vector<int>>> rgbArray = jpegToRgbArray(imagePath);

    // RGB 데이터 출력 (일부 픽셀만 출력)
    if (!rgbArray.empty()) {
        for (int i = 0; i < 5; ++i) {
            for (int j = 0; j < 5; ++j) {
                std::cout << "Pixel (" << i << ", " << j << "): R=" 
                          << rgbArray[i][j][0] << ", G=" 
                          << rgbArray[i][j][1] << ", B=" 
                          << rgbArray[i][j][2] << std::endl;
            }
        }
    }

    return 0;
}
```

이 코드는 OpenCV를 사용하여 JPEG 이미지를 로드하고, 이미지의 각 픽셀에 대해 RGB 값을 추출하여 3차원 벡터에 저장한다. 이 벡터는 이미지의 각 픽셀에 대한 RGB 값을 포함한다. 코드에서 `path_to_your_image.jpeg`를 실제 이미지 파일 경로로 변경해야 한다.

OpenCV를 설치하지 않았다면, 다음과 같이 설치할 수 있다:
1. OpenCV를 설치하려면, 패키지 매니저를 사용하거나 소스 코드에서 직접 컴파일할 수 있다.
2. CMakeLists.txt 파일에 OpenCV 라이브러리를 링크하여 프로젝트를 설정해야 한다.

CMakeLists.txt 예제:
```cmake
cmake_minimum_required(VERSION 3.10)
project(JpegToRgbArray)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(JpegToRgbArray main.cpp)
target_link_libraries(JpegToRgbArray ${OpenCV_LIBS})
```

이제 `main.cpp` 파일과 `CMakeLists.txt` 파일이 있는 디렉토리에서 CMake를 사용하여 빌드할 수 있다:
```bash
mkdir build
cd build
cmake ..
make
./JpegToRgbArray
```
