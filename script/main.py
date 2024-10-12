import sys
from web_scraper import get_web_content
from token_counter import num_tokens_from_string
from openai_blog_generator import generate_blog_post_outline, gernerate_header, generate_section_content
from wordcloud_generator import create_wordcloud_image
from file_utils import save_to_file, save_to_file_no_commant, get_current_datetime

sources = """
https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex
https://stackoverflow.com/questions/1252194/regex-performance-optimization-tips-and-tricks
https://blog.aliencube.org/ko/2013/10/15/improving-performances-while-using-regular-expressions/
https://www.syncfusion.com/succinctly-free-ebooks/regularexpressions/optimizing-your-regex
https://www.loggly.com/blog/five-invaluable-techniques-to-improve-regex-performance/
https://library.humio.com/kb/kb-regex-vs-string-performance.html
https://jack-vanlightly.com/blog/2016/2/25/optimizing-regex-performance-with-regexoptionsrighttoleft
"""

mandatory_text = ""

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

    
    header = gernerate_header(contents)
    save_to_file_no_commant("result.md", header)
    save_to_file_no_commant("result.md", format)
    save_to_file("result.md", "##### Outline #####")
    blog_post_outline = generate_blog_post_outline(contents)
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