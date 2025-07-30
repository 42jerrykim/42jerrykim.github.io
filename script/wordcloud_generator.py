from collections import Counter
from konlpy.tag import Okt
from nltk.corpus import stopwords as nltk_stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import re

# 필요한 리소스 다운로드
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('punkt')
nltk.download('punkt_tab')

# 한글 폰트 설정
font_path = './font.ttf'  # 이 경로는 OS에 따라 다를 수 있습니다.

# 텍스트 파일 읽기 함수
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 한국어 명사 추출 함수
def extract_korean_nouns(text):
    okt = Okt()
    nouns = okt.nouns(text)
    korean_stopwords = set(['및', '이', '그', '저', '것', '들', '에서', '그리고', '하지만', '그러나', '때문에', '이다', '등', '입니다', '로', '의', '가', '에', '와', '한', '가장', '더', '와', '을', '수', '를', '것', '있다', '해', '나', '자', '인', '다'])    
    return [noun for noun in nouns if noun not in korean_stopwords and len(noun) > 1]

# 영어 명사 추출 함수
def extract_english_nouns(text):
    tokens = word_tokenize(text)
    english_stopwords = set(['[', ']', '>', '*', '^', '+', '<', '@'])
    return [word.replace('\\', '') for word, pos in pos_tag(tokens) if pos.startswith('NN') and word not in english_stopwords and len(word) > 1]

# 텍스트에서 한글과 영어 명사 추출 함수
def extract_all_nouns(text):
    korean_text = ''.join([char if ord(char) > 127 else ' ' for char in text])
    english_text = ''.join([char if ord(char) <= 127 else ' ' for char in text])

    korean_nouns = extract_korean_nouns(korean_text)
    english_nouns = extract_english_nouns(english_text)

    return korean_nouns + english_nouns

# Word Cloud 생성 함수
def create_wordcloud(nouns, output_image_path, font_path):
    word_freq = Counter(nouns)
    wordcloud = WordCloud(
        font_path=font_path,
        width=1920, height=1080,
        colormap='hsv'
    ).generate_from_frequencies(word_freq)
    wordcloud.to_file(output_image_path)

# 메인 함수
def create_wordcloud_image(file_path, output_image_path, mandatory_text = "", font_path="./font.ttf"):
    text = read_text(file_path)
    nouns = extract_all_nouns(text)
    mandatory_words = re.split(r'\s+', mandatory_text)
    nouns += mandatory_words * 500  # 필수 단어 추가
    nouns += ['42JerryKim'] * 100
    create_wordcloud(nouns, output_image_path, font_path)

if __name__ == "__main__":
    mandatory_text = ""
    import sys

    if len(sys.argv) < 2:
        print("사용법: python wordcloud_generator.py <file_name(확장자 없는 경로)>")
        sys.exit(1)
    file_name = sys.argv[1]
    input_text_file = file_name + "/index.md"  # 읽을 텍스트 파일 경로
    output_image_file = file_name + '/wordcloud.png'  # 저장할 그림 파일 경로
    create_wordcloud_image(input_text_file, output_image_file, mandatory_text, font_path)