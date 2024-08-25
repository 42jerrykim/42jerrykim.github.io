import os
import requests
from bs4 import BeautifulSoup
import tiktoken
from openai import OpenAI
from datetime import datetime
from readability.readability import Document
from urllib.parse import urljoin
import sys
from readability import Document
import html2text
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 필요한 라이브러리 설치
# pip install wordcloud matplotlib

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# 한글 폰트 설정
font_path = './font.ttf'  # 이 경로는 OS에 따라 다를 수 있습니다.

# 텍스트 파일 읽기
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Word Cloud 생성 및 저장
def create_wordcloud_from_file(file_path, output_image_path, font_path, stopwords=None):
    # 텍스트 파일에서 텍스트 읽기
    text = read_text_file(file_path)

    # Word Cloud 생성
    wordcloud = WordCloud(
        font_path=font_path,
        width=1920, height=1080,
        stopwords=stopwords  # STOPWORDS를 여기서 적용
    ).generate(text)

    # Word Cloud를 그림 파일로 저장
    wordcloud.to_file(output_image_path)

if __name__ == "__main__":
    file_name = "./articles/_posts/2024/"

    # Word Cloud 생성
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update(['있다', '수', '은', '는', '이', '가', '을', '를', '및', '통해', '더', '따라', '두', '가지'])
    input_text_file = file_name + ".md"  # 읽을 텍스트 파일 경로
    output_image_file = file_name + '.png'  # 저장할 그림 파일 경로
    create_wordcloud_from_file(input_text_file, output_image_file, font_path, stopwords=custom_stopwords)



