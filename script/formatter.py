import re

def format_markdown_with_newline(file_path):
    # 파일 열기
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # '** 글자 **' 패턴을 '**글자**'로 변경하는 정규식
    formatted_content = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', content)

    # '**글자**' 뒤에 공백 및 줄바꿈이 하나만 있는 경우 줄바꿈을 두 개로 변경하는 정규식
    formatted_content = re.sub(r'(\*\*.*?\*\*)\s*\n(?!\n)', r'\1\n\n', formatted_content)

    # 파일 덮어쓰기
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_content)

    print(f"{file_path} 파일의 Markdown 형식과 줄바꿈이 수정되었습니다.")

if __name__ == "__main__":
    # 예시 파일 경로
    file_path = r''  # 수정하려는 파일 경로를 지정

    # 스크립트 실행
    format_markdown_with_newline(file_path)