https://www.codeproject.com/script/Articles/ViewDownloads.aspx?aid=5378622


e-paper, 즉 전자종이 기술을 사용하는 것은 다양한 장단점을 가지고 있다.

### 장점

1. **저전력 소비**: e-paper는 이미지를 변경할 때만 전력을 소비하며, 이미지를 유지하는 데 추가적인 전력을 필요로 하지 않는다. 이는 장기적으로 에너지 비용을 절감하고 배터리 수명을 연장하는 효과가 있다.
2. **햇빛 아래에서의 가독성**: e-paper는 반사형 디스플레이이기 때문에 직사광선 아래에서도 뛰어난 가독성을 제공한다. 이는 옥외 환경에서 특히 유용하다.
3. **눈의 피로 감소**: e-paper는 백라이트를 사용하지 않기 때문에 장시간 독서나 화면을 바라보아도 눈의 피로가 덜하다.
4. **얇고 가벼움**: e-paper 디스플레이는 일반적으로 얇고 가벼워 이동성이 뛰어나며 다양한 제품에 쉽게 통합될 수 있다.

### 단점

1. **색상과 동적 콘텐츠 표현의 한계**: 대부분의 e-paper 디스플레이는 흑백 또는 제한된 색상만을 지원하며, 동영상과 같은 동적 콘텐츠의 표현에 있어 LCD나 OLED와 같은 다른 디스플레이 기술에 비해 뒤떨어진다.
2. **갱신 속도**: e-paper 디스플레이의 페이지 갱신 속도는 전통적인 디스플레이 기술보다 느리다. 이는 실시간으로 빠르게 변하는 정보를 표시하는 데 제한을 줄 수 있다.
3. **비용**: 초기 설치 비용이 높을 수 있으며, 특히 대형 e-paper 디스플레이의 경우 비용이 더욱 상승한다.
4. **온도에 따른 성능 변화**: 극단적인 온도에서 e-paper의 성능이 저하될 수 있으며, 특히 추운 환경에서는 페이지 전환 속도가 더욱 느려질 수 있다.

e-paper 기술을 사용함으로써 얻을 수 있는 환경적 이점과 장기적인 비용 절감 효과는 매우 크지만, 적용하려는 프로젝트의 요구 사항에 따라 단점들도 고려해야 한다.

e-paper 기반 옥외 광고 장치 프로젝트의 목적은 다음과 같다. 첫째, 전력 소비가 적은 e-paper 기술을 활용하여 환경 친화적이면서도 효율적인 옥외 광고 솔루션을 개발하는 것이다. 둘째, 기존의 LED나 LCD 방식에 비해 유지 관리 비용이 적게 드는 광고 장치를 제작함으로써 장기적인 경제성을 제공한다. 셋째, e-paper의 장점인 뛰어난 가독성과 넓은 시야각을 살려, 어떤 환경에서도 사용자가 명확하게 정보를 인식할 수 있도록 한다. 넷째, 변화하는 광고 내용을 신속하고 원활하게 업데이트할 수 있는 시스템을 구축하여, 빠르게 변화하는 시장 환경에 능동적으로 대응할 수 있도록 한다. 이 프로젝트를 통해 지속 가능한 옥외 광고의 새로운 패러다임을 제시하고자 한다.

이 프로젝트는 e-paper 기술을 기반으로 한 옥외 광고 장치 개발을 목표로 하고 있다. e-paper는 저전력 소비의 전자 디스플레이 기술로, 이미지를 변경할 때만 에너지를 소비하며, 표시된 내용을 전력 공급 없이 유지할 수 있다는 점에서 특별하다. 이 기술의 주요 장점은 햇빛 아래에서도 뛰어난 가독성을 제공하고, 눈의 피로를 줄여주며, 얇고 가벼워 다양한 환경에 적용 가능하다는 것이다. 이러한 특성은 e-paper를 옥외 광고 장치에 이상적인 선택으로 만든다.


#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

#pragma pack(push, 1)
struct BMPHeader {
    uint16_t file_type{0x4D42};          // File type always BM which is 0x4D42
    uint32_t file_size{0};               // Size of the file (in bytes)
    uint16_t reserved1{0};               // Reserved, always 0
    uint16_t reserved2{0};               // Reserved, always 0
    uint32_t offset_data{0};             // Start position of pixel data (bytes from the beginning of the file)
};

struct BMPInfoHeader {
    uint32_t size{0};                      // Size of this header (in bytes)
    int32_t width{0};                      // width of bitmap in pixels
    int32_t height{0};                     // width of bitmap in pixels
    uint16_t planes{1};                    // No. of planes for the target device, this is always 1
    uint16_t bit_count{0};                 // No. of bits per pixel
    uint32_t compression{0};               // 0 or 3 - uncompressed. This program can only deal with uncompressed bmp.
    uint32_t size_image{0};                // 0 - for uncompressed images
    int32_t x_pixels_per_meter{0};
    int32_t y_pixels_per_meter{0};
    uint32_t colors_used{0};               // No. color indexes in the color table. Use 0 for the max number of colors allowed by bit_count
    uint32_t colors_important{0};          // No. of colors used for displaying the bitmap. If 0 all colors are required
};

#pragma pack(pop)

struct BMP {
    BMPHeader header;
    BMPInfoHeader info_header;
    vector<uint8_t> data;

    void read(const string &filename) {
        ifstream inp{filename, ios_base::binary};
        if (inp) {
            inp.read((char*)&header, sizeof(header));
            if(header.file_type != 0x4D42) {
                throw runtime_error("Error! Unrecognized file format.");
            }
            inp.read((char*)&info_header, sizeof(info_header));

            // Move read position to start of pixel data
            inp.seekg(header.offset_data, ios_base::beg);

            // Adjust the header fields for output
            if(info_header.bit_count == 24) {
                info_header.size = sizeof(BMPInfoHeader);
                header.offset_data = sizeof(BMPHeader) + sizeof(BMPInfoHeader);
            }

            // Reading the data
            data.resize(info_header.width * info_header.height * info_header.bit_count / 8);
            inp.read((char*)data.data(), data.size());
        } else {
            throw runtime_error("Unable to open the input file.");
        }
    }

    void write(const string &filename) {
        ofstream out{filename, ios_base::binary};
        if(out) {
            out.write((char*)&header, sizeof(header));
            out.write((char*)&info_header, sizeof(info_header));
            out.write((char*)data.data(), data.size());
        } else {
            throw runtime_error("Unable to open the output file.");
        }
    }
};

int main() {
    try {
        BMP bmp;
        bmp.read("input.bmp");

        // Change color: Here you can insert the code to modify BMP colors
        // Example: Convert to grayscale
        for (auto &pixel : bmp.data) {
            // Simple example: average the colors (not accurate for true grayscale)
            pixel = static_cast<uint8_t>((pixel + pixel + pixel) / 3);
        }

        bmp.write("output.bmp");
    } catch (const exception &e) {
        cerr << e.what() << endl;
    }

    return 0;
}


본 프로젝트의 목적은 다음과 같다. 첫째, 환경 친화적이면서도 경제적인 옥외 광고 솔루션을 제공하여, 전통적인 LED나 LCD 방식 대비 운영 비용을 절감한다. 둘째, e-paper의 장점을 최대한 활용하여, 모든 조명 조건에서도 명확한 정보 전달이 가능하도록 한다. 셋째, 빠르게 변화하는 광고 내용을 신속하게 업데이트할 수 있는 효율적인 시스템을 개발한다.

이 프로젝트는 지속 가능한 옥외 광고의 새로운 모델을 제시할 뿐만 아니라, 광고 산업에 있어서 에너지 효율성과 경제성의 새로운 기준을 설정하는 것을 목표로 한다. e-paper 기술의 장단점을 면밀히 분석하고, 이를 바탕으로 실용적이면서도 혁신적인 옥외 광고 장치를 설계하여, 광고의 미래를 형성하는 데 기여하고자 한다.
