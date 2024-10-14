from openai import OpenAI

client = OpenAI()

GPT_4O_MINI = "gpt-4o-mini"

def generate_blog_post_outline(contents):
    print(f"[INFO] Generating blog post outline using GPT-4o Mini model.")
    all_contents = ' '.join(contents)

    prompt = """
    너는 소프트웨어 기술 블로그의 목차를 작성하는 시스템이다. 
    목차는 개요, 여러 섹션들, 예제, FAQ, 관련 기술, 결론으로 구성하면 좋을 것 같다. 
    주어진 입력과 관련된 주제도 목차에 포함시켜서 풍부한 정보를 제공하자.
    기술용어는 영어로 작성해줘
    """

    user_prompt = f"""
    ```{all_contents}```

    위의 내용을 바탕으로 목차를 작성할 때, 관련된 내용도 함께 추가하여 더 풍부한 목차를 한글로 작성해줘.
    """

    response = client.chat.completions.create(
        model=GPT_4O_MINI,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    print(f"[INFO] Blog post outline generated successfully.")
    print("##### generate_blog_post_outline #################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def gernerate_header(contents):
    print(f"[INFO] Generating blog header using GPT-4o Mini model.")
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
    image: "tmp_wordcloud.png"
    ---

    한문단으로 작성된 도입글(1000자 분량, 문어체와 평어체를 사용하고 "~이다."로 문장이 끝나도록 작성. 기술용어는 영어로 작성)
    """
    response = client.chat.completions.create(
        model=GPT_4O_MINI,
        messages=[
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": all_contents}
        ],
        temperature=0
    )
    print(f"[INFO] Blog header generated successfully.")
    print("##### gernerate_header ###########################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def generate_section_content(toc, table):
    print(f"[INFO] Generating section content for TOC section.")
    system_prompt = f"""
    너는 소프트웨어 기술 블로그의 글을 작성하는 시스템이야
    문어체와 평어체를 사용하고 "~이다."로 문장이 끝나도록 작성해
    전체 목차중에서 일부 목차에 대해서 글을 작성할 예정이야.
    기술용어는 영어로 작성해줘
    """

    user_prompt = f"""
    전체 목차: ```{toc}```

    이번에 작성할 목차: ```{table}```

    이번에 작성할 목차에 대해서 내용을 작성하는데 다른 목차에서 작성할만한 내용을 제외하고 작성해줘.
    샘플 코드와 다이어그램(mermaid)도 추가하면 더 좋을 것 같아.
    
    제목은 ```##```를 사용해줘
    """

    response = client.chat.completions.create(
        model=GPT_4O_MINI,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    print("##### generate_section_content ###################")
    print(table)    
    print("##################################################")
    print(f"[INFO] Section content generated successfully.")
    return response.choices[0].message.content
