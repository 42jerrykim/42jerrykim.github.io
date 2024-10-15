from datetime import datetime

current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S ")
def get_current_datetime():
    return current_datetime

def save_to_file(file_path, content):
    file_path = file_path
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write("<!--\n")
        file.write(content)
        file.write("\n-->\n\n")

def save_to_file_no_commant(file_path, content):
    file_path = file_path
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content)
        file.write("\n\n")
