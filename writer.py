import os
import requests
from bs4 import BeautifulSoup
import tiktoken
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

GPT_35_TURBO = "gpt-3.5-turbo"
GPT_35_TURBO_16K = "gpt-3.5-turbo-16k"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_web_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def summarize_content(content):
    response = openai.ChatCompletion.create(
        model=GPT_35_TURBO_16K,
        messages=[
            {"role": "system", "content": "Summarize content"},
            {"role": "user", "content": content}
        ],
        temperature=0,
        max_tokens=2000
    )
    
    print("##### summarize_content ##########################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def gernerate_tags(contents):
    all_contents = ' '.join(contents)
    prompt = """
    Please perform the following tasks:
    1. Generate tags related to the given content
    2. Tags should be in a format suitable for a blog.
    3. Format the tags in markdown list format.
    """
    response = openai.ChatCompletion.create(
        model=GPT_35_TURBO_16K,
        messages=[
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": all_contents}
        ],
        temperature=0,
        max_tokens=2000
    )
    
    print("##### gernerate_tags #############################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def generate_blog_post_introduction(contents):
    all_contents = ' '.join(contents)

    prompt = """
    You're a software developer who works on a wide variety of topics.
    You are a developer familiar with python or csharp.
    The blog post should be informative and engaging.
    You are going to write a blog based on the given information. 
    I need you to write an introduction
    """

    response = openai.ChatCompletion.create(
        model=GPT_35_TURBO,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": all_contents}
        ],
        temperature=0,
        max_tokens=2000
    )
    print("##### generate_blog_post_introduction ############")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def generate_blog_post_outline(contents):
    all_contents = ' '.join(contents)

    prompt = """
    You're a software developer who works on a wide variety of topics.
    You are a developer familiar with python or csharp.
    The blog post should be informative and engaging.
    It should have an introduction, several sections, Practical Examples, Frequently Asked Questions, Related Technologies, and a conclusion summarizing the main points.
    Write a blog post outline using markdown format.
    """

    response = openai.ChatCompletion.create(
        model=GPT_35_TURBO,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": all_contents}
        ],
        temperature=0,
        max_tokens=2000
    )
    print("##### generate_blog_post_outline #################")
    print(response.choices[0].message.content)    
    print("##################################################")
    return response.choices[0].message.content

def generate_section_content(toc, table):
    system_prompt = f"""
    You are a developer familiar with python or csharp.
    Write an article about the table of contents entered by the user by referring to the table of contents entered by the assistant 
    The content to be written must have titles using markdown format
    Please write sample code in python or csharp if possible
    """
    user_prompt = f"""
    The content separated by (```) is the table of contents of the blog post to be written.
    Please provide detailed information based on the given table of contents.

    ```{table}```
    """
    response = openai.ChatCompletion.create(
        model=GPT_35_TURBO,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": toc},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=2000
    )
    return response.choices[0].message.content

def save_to_file(file_path, content):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)

sources = """

"""

if __name__ == "__main__":
    
    urls = sources.strip().split('\n')
    contents = [get_web_content(url) for url in urls]
    summaries = [summarize_content(content) for content in contents]
    blog_post_outline = generate_blog_post_outline(summaries)
    save_to_file("result.md", "<!-- ##### Outline ##### -->\n")
    save_to_file("result.md", blog_post_outline + "\n\n")

    blog_post_introduction = generate_blog_post_introduction(summaries)
    save_to_file("result.md", "<!-- ##### Intro ##### -->\n")
    save_to_file("result.md", blog_post_introduction + "\n\n")

    tags = gernerate_tags(summaries)
    # print(tags)
    save_to_file("result.md", "<!-- ##### Tags ##### -->\n")
    save_to_file("result.md", tags + "\n\n")

    toc = blog_post_outline.strip().split('\n\n')
    for table in toc:
        print("##### table ######################################")
        print(table)
        section_content = generate_section_content(blog_post_outline, table)
        print("##### section_content ############################")
        print(section_content)
        print("##################################################")

        save_to_file("result.md", "<!-- ##### Table ##### -->\n")
        save_to_file("result.md", table + "\n")
        save_to_file("result.md", "<!-- ##### Content ##### -->\n")
        save_to_file("result.md", section_content + "\n\n")
    save_to_file("result.md", "<!-- ##### Reference ##### -->\n")
    save_to_file("result.md", "## Reference\n")
    for url in urls:
        save_to_file("result.md", "* [" + url + "](" + url + ")\n")