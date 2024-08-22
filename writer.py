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

client = OpenAI()

GPT_4O_MINI = "gpt-4o-mini"

def get_readable_content(url):
    # URL로부터 HTML 페이지를 가져옴
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 요청 실패 시 에러를 발생시킴

    # 인코딩 설정
    response.encoding = response.apparent_encoding

    # Readability를 사용하여 문서 구조화
    doc = Document(response.text)
    readable_html = doc.summary()
    title = doc.title()

    # BeautifulSoup을 사용하여 정리된 HTML을 파싱
    soup = BeautifulSoup(readable_html, 'html.parser')

    # CSS 스타일 및 스크립트 태그 제거
    for tag in soup(['style', 'script']):
        tag.decompose()

    # 이미지 src 속성을 절대 URL로 변환
    for img in soup.find_all('img'):
        if img.has_attr('src'):
            img['src'] = urljoin(url, img['src'])

    # HTML을 Markdown으로 변환
    h = html2text.HTML2Text()
    h.ignore_links = False  # 링크를 무시하지 않도록 설정
    markdown = h.handle(soup.prettify())

    return title, markdown

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_web_content(url):
    title, content = get_readable_content(url)
    return content

def gernerate_header(contents):
    all_contents = ' '.join(contents)
    prompt = """
    Please perform the following tasks:
    1. 주어진 내용을 활용하여 포멧에 내용을 작성해줘
    2. TAG는 블로그에서 사용할 만한 영어 단어로 50개 이상 작성해줘
    3. CATEGORY는 띄어쓰기가 없는 영어 단어로 작성해줘
    4. TITLE은 한글로 적어줘
    
    아래는 포멧이야
    ---
    title: "[CATEGORY] TITLE"
    categories: CATEGORY
    tags:
    - TAG1
    - TAG2
    - TAG3
    header:
      teaser: /assets/images/undefined/teaser.jpg
    ---

    한문단으로 작성된 도입글(1000자 분량, 문어체와 평어체를 사용하고 "~이다."로 문장이 끝나도록 작성)
    """
    response = client.chat.completions.create(
        model=GPT_4O_MINI,
        messages=[
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": all_contents}
        ],
        temperature=0
    )
    
    print("##### gernerate_tags #############################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def generate_blog_post_outline(contents):
    all_contents = ' '.join(contents)

    prompt = """
    너는 소프트웨어 기술 블로그의 목차를 작성하는 시스템이야
    목차의 구성은 개요, 여러 섹션들, 예제, FAQ, 관련 기술, 결론으로 구성하면 좋을것 같아
    주어진 입력과 관련된 주제도 목차에 포함시켜서 풍부한 정보를 제공해
    """

    user_prompt = f"""
    ```{all_contents}```

    위 내용을 바탕으로 목차를 작성하는데, 위 내용과 관련된 내용도 같이 추가해서 풍부한 목차를 작성해

    """

    response = client.chat.completions.create(
        model=GPT_4O_MINI,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    print("##### generate_blog_post_outline #################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def generate_section_content(toc, table):
    system_prompt = f"""
    너는 소프트웨어 기술 블로그의 글을 작성하는 시스템이야
    문어체와 평어체를 사용하고 "~이다."로 문장이 끝나도록 작성해
    전체 목차중에서 일부 목차에 대해서 글을 작성할 예정이야.
    """

    user_prompt = f"""
    전체 목차: ```{toc}```

    이번에 작성할 목차: ```{table}```

    이번에 작성할 목차에 대해서 내용을 작성하는데 다른 목차에서 작성할만한 내용을 제외하고 작성해줘.
    샘플 코드와 다이어그램(mermaid)도 추가하면 더 좋을 것 같아.
    
    제목은 ```##```를 사용하고, 소제목은 ```###```대신 ```**```를 사용해서 강조만 해줘
    """

    assistant_prompt = f"""
    Start with heading level 2
    """
    response = client.chat.completions.create(
        model=GPT_4O_MINI,
        messages=[
            {"role": "system", "content": system_prompt},
            # {"role": "assistant", "content": toc},
            # {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S ")
def save_to_file(file_path, content):
    file_path = current_datetime + file_path
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write("<!--\n")
        file.write(content)
        file.write("\n-->\n\n")

def save_to_file_no_commant(file_path, content):
    file_path = current_datetime + file_path
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write("\n\n")

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

sources = """

"""

format = """
|![]()|
|:---:|
||
"""

if __name__ == "__main__":
    # save_to_file_no_commant("result.md", format)

    urls = sources.strip().split('\n')
    contents = [get_web_content(url) for url in urls]
    # print(contents)

    # 사용할 인코딩 이름 (예: "cl100k_base", "gpt2", 등)
    encoding_name = "cl100k_base"  # GPT-4o mini 모델에 적절한 인코딩 이름 사용
    
    # 각 문자열에 대해 토큰 수 계산 및 출력
    for string in contents:
        num_tokens = num_tokens_from_string(string, encoding_name)
        print(f"토큰 수: {num_tokens}")
    
    # 모든 문자열을 하나의 문자열로 결합하여 전체 토큰 수 계산
    combined_string = " ".join(contents)
    total_tokens = num_tokens_from_string(combined_string, encoding_name)
    print(f"전체 문자열의 토큰 수: {total_tokens}")
    if total_tokens > 128000:
        print(f"전체 문자열의 토큰 수가 128,000을 초과하여 프로그램을 중단합니다. (토큰 수: {total_tokens})")
        sys.exit(1)  # 프로그램 중단
    
    blog_post_outline = generate_blog_post_outline(contents)
    header = gernerate_header(contents)
    save_to_file_no_commant("result.md", header)
    save_to_file_no_commant("result.md", format)
    save_to_file("result.md", "##### Outline #####")
    save_to_file("result.md", blog_post_outline)

    toc = blog_post_outline.strip().split('\n\n')
    for table in toc:
        # table의 줄 수를 확인
        table_lines = table.split('\n')
        # table이 3줄 이상일 때만 generate_section_content을 수행
        if len(table_lines) >= 3:
            print("##### section_content ############################")
            print(table)
            save_to_file("result.md", table)
            section_content = generate_section_content(blog_post_outline, table)
            save_to_file_no_commant("result.md", section_content)
            print("##################################################")

    # Word Cloud 생성
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update(['있다', '수', '은', '는', '이', '가', '을', '를'])
    input_text_file = current_datetime + "result.md"  # 읽을 텍스트 파일 경로
    output_image_file = current_datetime + 'wc.png'  # 저장할 그림 파일 경로
    create_wordcloud_from_file(input_text_file, output_image_file, font_path, stopwords=custom_stopwords)

    reference = ""
    for url in urls:
        reference += "* [" + url + "](" + url + ")\n"
    save_to_file("result.md", "##### Reference #####")
    save_to_file_no_commant("result.md", "## Reference\n")
    save_to_file_no_commant("result.md", reference)

    for content in contents:
        save_to_file("result.md", content)
        save_to_file("result.md", "\n\n\n\n\n")



