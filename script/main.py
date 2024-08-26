import sys
from web_scraper import get_web_content
from token_counter import num_tokens_from_string
from openai_blog_generator import generate_blog_post_outline, gernerate_header, generate_section_content
from wordcloud_generator import create_wordcloud_image
from file_utils import save_to_file, save_to_file_no_commant, get_current_datetime

sources = """
https://42jerrykim.github.io/collections/computerterms/algotithm_classify/
http://www.ktword.co.kr/test/view/view.php?no=5735
https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98
https://namu.wiki/w/%EC%BD%94%EB%94%A9%20%ED%85%8C%EC%8A%A4%ED%8A%B8
https://school.programmers.co.kr/learn/challenges?tab=algorithm_practice_kit
"""

mandatory_text = "Algorothm CodingTest"

format = """
|![]()|
|:---:|
||
"""

if __name__ == "__main__":
    urls = sources.strip().split('\n')
    contents = [get_web_content(url) for url in urls]

    for string in contents:
        num_tokens = num_tokens_from_string(string)
        print(f"토큰 수: {num_tokens}")
    
    combined_string = " ".join(contents)
    total_tokens = num_tokens_from_string(combined_string)
    print(f"전체 문자열의 토큰 수: {total_tokens}")
    if total_tokens > 128000:
        print(f"전체 문자열의 토큰 수가 128,000을 초과하여 프로그램을 중단합니다. (토큰 수: {total_tokens})")
        sys.exit(1)

    blog_post_outline = generate_blog_post_outline(contents)
    header = gernerate_header(contents)
    save_to_file_no_commant("result.md", header)
    save_to_file_no_commant("result.md", format)
    save_to_file("result.md", "##### Outline #####")
    save_to_file("result.md", blog_post_outline)

    toc = blog_post_outline.strip().split('\n\n')
    for table in toc:
        table_lines = table.split('\n')
        if len(table_lines) >= 3:
            save_to_file("result.md", table)
            section_content = generate_section_content(blog_post_outline, table)
            save_to_file_no_commant("result.md", section_content)

    reference = ""
    for url in urls:
        reference += "* [" + url + "](" + url + ")\n"
    save_to_file("result.md", "##### Reference #####")
    save_to_file_no_commant("result.md", "## Reference\n")
    save_to_file_no_commant("result.md", reference)

    for content in contents:
        save_to_file("result.md", content)
        save_to_file("result.md", "\n\n\n\n\n")

    input_text_file = get_current_datetime() + "result.md"
    output_image_file = get_current_datetime() + 'wc.png'
    create_wordcloud_image(input_text_file, output_image_file, mandatory_text)