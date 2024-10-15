import sys
from web_scraper import get_web_content
from token_counter import num_tokens_from_string
from openai_blog_generator import generate_blog_post_outline, gernerate_header, generate_section_content
from wordcloud_generator import create_wordcloud_image
from file_utils import save_to_file, save_to_file_no_commant, get_current_datetime
from datetime import datetime
from formatter import format_markdown_with_newline
import os
import shutil

sources = """
"""

mandatory_text = ""

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
    save_to_file_no_commant("index.md", header)
    save_to_file("index.md", "##### Outline #####")
    blog_post_outline = generate_blog_post_outline(contents)
    save_to_file("index.md", blog_post_outline)

    toc = blog_post_outline.strip().split('\n\n')
    for table in toc:
        table_lines = table.split('\n')
        if len(table_lines) >= 3:
            save_to_file("index.md", table)
            section_content = generate_section_content(blog_post_outline, table)
            save_to_file_no_commant("index.md", section_content)

    reference = ""
    for url in urls:
        reference += "* [" + url + "](" + url + ")\n"
    save_to_file("index.md", "##### Reference #####")
    save_to_file_no_commant("index.md", "## Reference\n")
    save_to_file_no_commant("index.md", reference)

    for content in contents:
        save_to_file("index.md", content)
        save_to_file("index.md", "\n\n\n\n\n")

    input_text_file = "index.md"
    output_image_file = 'tmp_wordcloud.png'
    create_wordcloud_image(input_text_file, output_image_file, mandatory_text)

    format_markdown_with_newline(input_text_file)

    with open(input_text_file, 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        # 두 번째 줄에 'date: ' 추가
        if len(lines) >= 2:
            lines.insert(1, f'date: {datetime.now().strftime("%Y-%m-%d")}\n')  # 두 번째 줄에 삽입
        else:
            lines.append(f'date: {datetime.now().strftime("%Y-%m-%d")}\n')  # 파일이 두 줄 미만일 경우 추가

        file.seek(0)  # 파일 시작 지점으로 이동
        file.writelines(lines)  # 수정된 내용을 파일에 다시 씀

    # 현재 날짜 가져오기 (예: 2024-10-15 형식)
    current_date = datetime.now().strftime('%Y-%m-%d-%H_%M_%S')

    # 경로 설정
    base_dir = './content/post/2024/'  # root 디렉토리 경로
    new_folder_path = os.path.join(base_dir, current_date)

    # 새 폴더 생성
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # 이동할 파일들
    files_to_move = ['index.md', 'tmp_wordcloud.png']

    # 파일 이동
    for file_name in files_to_move:
        source_path = file_name
        destination_path = os.path.join(new_folder_path, file_name)
        
        # 파일이 존재하면 이동
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"{file_name} 파일이 {new_folder_path}로 이동되었습니다.")
        else:
            print(f"{file_name} 파일이 존재하지 않습니다.")

    print("폴더 생성 및 파일 이동이 완료되었습니다.")