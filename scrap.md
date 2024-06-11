https://comsmart.co.kr/cmart/shop/item.php?it_id=1644305465&num=19&ca_id2=
[https://plantuml.com/ko/link#google_vignette](https://plantuml.com/ko/link)

https://blog.naver.com/yally23232/220793048885

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from plantuml import PlantUML

class PlantUMLApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('PlantUML Sequence Diagram Generator')
        
        self.layout = QVBoxLayout()
        
        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)
        
        self.generateButton = QPushButton('Generate Diagram', self)
        self.generateButton.clicked.connect(self.generate_diagram)
        self.layout.addWidget(self.generateButton)
        
        self.imageLabel = QLabel(self)
        self.layout.addWidget(self.imageLabel)
        
        self.setLayout(self.layout)
        self.show()
        
    def generate_diagram(self):
        plantuml_text = self.textEdit.toPlainText()
        
        # Save the PlantUML text to a temporary file
        temp_file = 'temp_diagram.puml'
        with open(temp_file, 'w') as file:
            file.write(plantuml_text)
        
        # Generate the diagram using PlantUML
        plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        diagram_file = 'diagram.png'
        plantuml.processes_file(temp_file, outfile=diagram_file)
        
        # Display the diagram
        pixmap = QPixmap(diagram_file)
        self.imageLabel.setPixmap(pixmap)
        
        # Clean up the temporary file
        os.remove(temp_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlantUMLApp()
    sys.exit(app.exec_())


buffalo_l
min detection score  0.5
max recog distance 0.3
min recog faces: 2


#include <windows.h>
#include <tchar.h>

// 전역 변수
HBITMAP hBitmap;

// 함수 선언
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

// WinMain: 프로그램의 진입점
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const TCHAR CLASS_NAME[] = _T("Sample Window Class");

    WNDCLASS wc = { };

    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        _T("Learn to Program Windows"),
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    // 메시지 루프
    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

// 윈도우 프로시저 함수
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_CREATE:
        // 비트맵 로드
        hBitmap = (HBITMAP)LoadImage(NULL, _T("sample.bmp"), IMAGE_BITMAP, 0, 0, LR_LOADFROMFILE);
        if (hBitmap == NULL) {
            MessageBox(hwnd, _T("Failed to load bitmap"), _T("Error"), MB_OK);
            PostQuitMessage(0);
        }
        break;
    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);

        HDC hdcMem = CreateCompatibleDC(hdc);
        HGDIOBJ oldBitmap = SelectObject(hdcMem, hBitmap);

        BITMAP bitmap;
        GetObject(hBitmap, sizeof(bitmap), &bitmap);

        BitBlt(hdc, 0, 0, bitmap.bmWidth, bitmap.bmHeight, hdcMem, 0, 0, SRCCOPY);

        SelectObject(hdcMem, oldBitmap);
        DeleteDC(hdcMem);

        EndPaint(hwnd, &ps);
        break;
    }
    case WM_DESTROY:
        if (hBitmap) {
            DeleteObject(hBitmap);
        }
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

```
#include <windows.h>
#include <tchar.h>
#include <cstdlib>
#include <ctime>

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    static TCHAR szAppName[] = _T("RandomBitmapApp");
    HWND hwnd;
    MSG msg;
    WNDCLASS wndclass;

    wndclass.style = CS_HREDRAW | CS_VREDRAW;
    wndclass.lpfnWndProc = WndProc;
    wndclass.cbClsExtra = 0;
    wndclass.cbWndExtra = 0;
    wndclass.hInstance = hInstance;
    wndclass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);
    wndclass.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
    wndclass.lpszMenuName = NULL;
    wndclass.lpszClassName = szAppName;

    if (!RegisterClass(&wndclass))
    {
        MessageBox(NULL, _T("This program requires Windows NT!"), szAppName, MB_ICONERROR);
        return 0;
    }

    hwnd = CreateWindow(szAppName, _T("Random Bitmap Display Program"),
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
        CW_USEDEFAULT, CW_USEDEFAULT, NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    static HBITMAP hBitmap;
    static BITMAP bm;
    static HDC hdcMem;
    static PAINTSTRUCT ps;
    HDC hdc;
    static int width = 800;
    static int height = 600;

    switch (message)
    {
    case WM_CREATE:
        {
            srand((unsigned int)time(NULL)); // Seed the random number generator

            BITMAPINFO bmi;
            ZeroMemory(&bmi, sizeof(BITMAPINFO));
            bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
            bmi.bmiHeader.biWidth = width;
            bmi.bmiHeader.biHeight = -height; // Negative to indicate a top-down DIB
            bmi.bmiHeader.biPlanes = 1;
            bmi.bmiHeader.biBitCount = 24; // 24-bit bitmap
            bmi.bmiHeader.biCompression = BI_RGB;

            hdc = GetDC(hwnd);
            hBitmap = CreateDIBSection(hdc, &bmi, DIB_RGB_COLORS, NULL, NULL, 0);
            ReleaseDC(hwnd, hdc);

            if (hBitmap == NULL)
            {
                MessageBox(hwnd, _T("Could not create bitmap!"), _T("Error"), MB_OK | MB_ICONEXCLAMATION);
                return -1;
            }

            GetObject(hBitmap, sizeof(BITMAP), &bm);

            // Fill bitmap with random colors
            HDC hdcMem = CreateCompatibleDC(NULL);
            SelectObject(hdcMem, hBitmap);

            for (int y = 0; y < height; ++y)
            {
                for (int x = 0; x < width; ++x)
                {
                    COLORREF color = RGB(rand() % 256, rand() % 256, rand() % 256);
                    SetPixel(hdcMem, x, y, color);
                }
            }

            DeleteDC(hdcMem);
        }
        return 0;

    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);
        hdcMem = CreateCompatibleDC(hdc);
        SelectObject(hdcMem, hBitmap);
        BitBlt(hdc, 0, 0, bm.bmWidth, bm.bmHeight, hdcMem, 0, 0, SRCCOPY);
        DeleteDC(hdcMem);
        EndPaint(hwnd, &ps);
        return 0;

    case WM_DESTROY:
        DeleteObject(hBitmap);
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, message, wParam, lParam);
}
```

```
#include <windows.h>
#include <tchar.h>
#include <cstdlib>
#include <ctime>

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    static TCHAR szAppName[] = _T("RandomBitmapApp");
    HWND hwnd;
    MSG msg;
    WNDCLASS wndclass;

    wndclass.style = CS_HREDRAW | CS_VREDRAW;
    wndclass.lpfnWndProc = WndProc;
    wndclass.cbClsExtra = 0;
    wndclass.cbWndExtra = 0;
    wndclass.hInstance = hInstance;
    wndclass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);
    wndclass.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
    wndclass.lpszMenuName = NULL;
    wndclass.lpszClassName = szAppName;

    if (!RegisterClass(&wndclass))
    {
        MessageBox(NULL, _T("This program requires Windows NT!"), szAppName, MB_ICONERROR);
        return 0;
    }

    hwnd = CreateWindow(szAppName, _T("Random Bitmap Display Program"),
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
        CW_USEDEFAULT, CW_USEDEFAULT, NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    static HBITMAP hBitmap;
    static BITMAP bm;
    static HDC hdcMem;
    static PAINTSTRUCT ps;
    HDC hdc;
    static int width = 800;
    static int height = 600;
    static HWND hwndButton;

    switch (message)
    {
    case WM_CREATE:
        {
            hwndButton = CreateWindow(
                _T("BUTTON"), _T("Change to Red"), 
                WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
                10, 10, 150, 30, 
                hwnd, (HMENU)1, (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);

            srand((unsigned int)time(NULL)); // Seed the random number generator

            BITMAPINFO bmi;
            ZeroMemory(&bmi, sizeof(BITMAPINFO));
            bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
            bmi.bmiHeader.biWidth = width;
            bmi.bmiHeader.biHeight = -height; // Negative to indicate a top-down DIB
            bmi.bmiHeader.biPlanes = 1;
            bmi.bmiHeader.biBitCount = 24; // 24-bit bitmap
            bmi.bmiHeader.biCompression = BI_RGB;

            hdc = GetDC(hwnd);
            hBitmap = CreateDIBSection(hdc, &bmi, DIB_RGB_COLORS, NULL, NULL, 0);
            ReleaseDC(hwnd, hdc);

            if (hBitmap == NULL)
            {
                MessageBox(hwnd, _T("Could not create bitmap!"), _T("Error"), MB_OK | MB_ICONEXCLAMATION);
                return -1;
            }

            GetObject(hBitmap, sizeof(BITMAP), &bm);

            // Fill bitmap with random colors
            HDC hdcMem = CreateCompatibleDC(NULL);
            SelectObject(hdcMem, hBitmap);

            for (int y = 0; y < height; ++y)
            {
                for (int x = 0; x < width; ++x)
                {
                    COLORREF color = RGB(rand() % 256, rand() % 256, rand() % 256);
                    SetPixel(hdcMem, x, y, color);
                }
            }

            DeleteDC(hdcMem);
        }
        return 0;

    case WM_COMMAND:
        if (LOWORD(wParam) == 1) // Button was clicked
        {
            // Change bitmap to red
            HDC hdcMem = CreateCompatibleDC(NULL);
            SelectObject(hdcMem, hBitmap);

            for (int y = 0; y < height; ++y)
            {
                for (int x = 0; x < width; ++x)
                {
                    SetPixel(hdcMem, x, y, RGB(255, 0, 0));
                }
            }

            DeleteDC(hdcMem);
            InvalidateRect(hwnd, NULL, TRUE); // Request redraw
        }
        return 0;

    case WM_PAINT:
        hdc = BeginPaint(hwnd, &ps);
        hdcMem = CreateCompatibleDC(hdc);
        SelectObject(hdcMem, hBitmap);
        BitBlt(hdc, 0, 50, bm.bmWidth, bm.bmHeight, hdcMem, 0, 0, SRCCOPY); // Adjusted y-position for the button
        DeleteDC(hdcMem);
        EndPaint(hwnd, &ps);
        return 0;

    case WM_DESTROY:
        DeleteObject(hBitmap);
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, message, wParam, lParam);
}

```
