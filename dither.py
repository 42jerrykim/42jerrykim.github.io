import os
import random
import logging
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageOps
import exifread
import numpy as np
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from collections import defaultdict

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def floyd_steinberg_dithering(image, palette):
    logging.info("Applying Floyd-Steinberg Dithering...")
    img_array = np.array(image, dtype=np.float32)
    height, width, _ = img_array.shape

    color_usage = defaultdict(int)

    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy()
            new_pixel = find_closest_palette_color(old_pixel, palette)
            color_usage[tuple(new_pixel)] += 1
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            if x + 1 < width:
                img_array[y, x + 1] += quant_error * 7 / 16
            if x - 1 >= 0 and y + 1 < height:
                img_array[y + 1, x - 1] += quant_error * 3 / 16
            if y + 1 < height:
                img_array[y + 1, x] += quant_error * 5 / 16
            if x + 1 < width and y + 1 < height:
                img_array[y + 1, x + 1] += quant_error * 1 / 16

    for color, count in color_usage.items():
        logging.info(f"Color {color} used {count} times in Floyd-Steinberg Dithering")

    logging.info("Floyd-Steinberg Dithering applied successfully.")
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def jarvis_judice_ninke_dithering(image, palette):
    logging.info("Applying Jarvis-Judice-Ninke Dithering...")
    img_array = np.array(image, dtype=np.float32)
    height, width, _ = img_array.shape

    color_usage = defaultdict(int)

    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy()
            new_pixel = find_closest_palette_color(old_pixel, palette)
            color_usage[tuple(new_pixel)] += 1
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            for dy, dx, factor in JARVIS_JUDICE_NINKE_MATRIX:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    img_array[ny, nx] += quant_error * factor

    for color, count in color_usage.items():
        logging.info(f"Color {color} used {count} times in Jarvis-Judice-Ninke Dithering")

    logging.info("Jarvis-Judice-Ninke Dithering applied successfully.")
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def stucki_dithering(image, palette):
    logging.info("Applying Stucki Dithering...")
    img_array = np.array(image, dtype=np.float32)
    height, width, _ = img_array.shape

    color_usage = defaultdict(int)

    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x].copy()
            new_pixel = find_closest_palette_color(old_pixel, palette)
            color_usage[tuple(new_pixel)] += 1
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            for dy, dx, factor in STUCKI_MATRIX:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    img_array[ny, nx] += quant_error * factor

    for color, count in color_usage.items():
        logging.info(f"Color {color} used {count} times in Stucki Dithering")

    logging.info("Stucki Dithering applied successfully.")
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def find_closest_palette_color(pixel, palette):
    distances = [np.linalg.norm(pixel - color) for color in palette]
    return palette[np.argmin(distances)]

JARVIS_JUDICE_NINKE_MATRIX = [
    (0, 1, 7/48), (0, 2, 5/48),
    (1, -2, 3/48), (1, -1, 5/48), (1, 0, 7/48), (1, 1, 5/48), (1, 2, 3/48),
    (2, -2, 1/48), (2, -1, 3/48), (2, 0, 5/48), (2, 1, 3/48), (2, 2, 1/48)
]

STUCKI_MATRIX = [
    (0, 1, 8/42), (0, 2, 4/42),
    (1, -2, 2/42), (1, -1, 4/42), (1, 0, 8/42), (1, 1, 4/42), (1, 2, 2/42),
    (2, -2, 1/42), (2, -1, 2/42), (2, 0, 4/42), (2, 1, 2/42), (2, 2, 1/42)
]

palette = [
    np.array([0, 0, 0]),        # Black
    np.array([255, 255, 255]),  # White
    np.array([255, 0, 0]),      # Red
    np.array([0, 0, 255]),      # Blue
    np.array([0, 255, 0]),      # Green
    np.array([255, 255, 0]),    # Yellow
    np.array([255, 165, 0])     # Orange
]

def resize_and_pad(image, size, color=(255, 255, 255)):
    logging.info(f"Resizing and padding image to {size}...")
    aspect_ratio = min(size[0] / image.width, size[1] / image.height)
    new_size = (int(image.width * aspect_ratio), int(image.height * aspect_ratio))
    image = image.resize(new_size, Image.LANCZOS)
    
    new_image = Image.new("RGB", size, color)
    new_image.paste(image, ((size[0] - new_size[0]) // 2, (size[1] - new_size[1]) // 2))
    logging.info("Image resized and padded successfully.")
    return new_image

def add_text_to_image(image, text, position, font_size=20, color=(255, 255, 255), border_color=(0, 0, 0)):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    if position == "top_left":
        text_position = (10, 10)
    elif position == "bottom_right":
        text_position = (image.width - text_width - 10, image.height - text_height - 10)
    
    # Draw border
    x, y = text_position
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=border_color)
    
    # Draw main text
    draw.text(text_position, text, font=font, fill=color)
    return image

def get_photo_taken_date(photo_path):
    # 이미지 파일 열기
    img = Image.open(photo_path)
    
    # EXIF 데이터 가져오기
    exif_data = img._getexif()
    
    # EXIF 데이터가 존재하는지 확인
    if exif_data is not None:
        # EXIF 데이터 중 촬영 날짜 찾기
        for tag, value in exif_data.items():
            if tag in (36867, 36868):  # 36867: DateTimeOriginal, 36868: DateTimeDigitized
                return value.split(" ")[0]  # 날짜 부분만 반환
    else:
        # exifread 라이브러리를 사용하여 EXIF 데이터 읽기
        with open(photo_path, 'rb') as f:
            tags = exifread.process_file(f)
            if 'EXIF DateTimeOriginal' in tags:
                return str(tags['EXIF DateTimeOriginal']).split(" ")[0]
            elif 'EXIF DateTimeDigitized' in tags:
                return str(tags['EXIF DateTimeDigitized']).split(" ")[0]

    return ""

def process_image(folder_path):
    logging.info("Selecting a random JPEG file from the folder...")
    jpeg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.JPG')]
    
    if not jpeg_files:
        logging.error("No JPEG files found in the specified folder.")
        raise FileNotFoundError("No JPEG files found in the specified folder.")
    
    selected_file = random.choice(jpeg_files)
    logging.info(f"Selected file: {selected_file}")
    image_path = os.path.join(folder_path, selected_file)

    logging.info("Opening image...")
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)  # EXIF 데이터를 기반으로 이미지 회전 처리
    image = resize_and_pad(image, (800, 480))

    # Floyd-Steinberg 디더링
    logging.info("Applying Floyd-Steinberg Dithering...")
    fs_dithered_image = floyd_steinberg_dithering(image, palette)
    fs_output_path = os.path.join(folder_path, 'fs_output_image.bmp')
    fs_dithered_image.save(fs_output_path)
    logging.info(f"Floyd-Steinberg Dithered image saved to {fs_output_path}")

    # Jarvis-Judice-Ninke 디더링
    logging.info("Applying Jarvis-Judice-Ninke Dithering...")
    jjn_dithered_image = jarvis_judice_ninke_dithering(image, palette)
    jjn_output_path = os.path.join(folder_path, 'jjn_output_image.bmp')
    jjn_dithered_image.save(jjn_output_path)
    logging.info(f"Jarvis-Judice-Ninke Dithered image saved to {jjn_output_path}")

    # Stucki 디더링
    logging.info("Applying Stucki Dithering...")
    stucki_dithered_image = stucki_dithering(image, palette)
    stucki_output_path = os.path.join(folder_path, 'stucki_output_image.bmp')
    stucki_dithered_image.save(stucki_output_path)
    logging.info(f"Stucki Dithered image saved to {stucki_output_path}")

    # 이미지에 텍스트 추가
    file_name = os.path.basename(image_path)
    capture_date = get_photo_taken_date(image_path)  # 촬영 날짜 가져오기
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text_top_left = f"{file_name} {capture_date}"
    text_bottom_right = f"Updated:{current_time}"
    fs_dithered_image = add_text_to_image(fs_dithered_image, text_top_left, "top_left")
    fs_dithered_image = add_text_to_image(fs_dithered_image, "FS_" + text_bottom_right, "bottom_right", font_size=10)
    jjn_dithered_image = add_text_to_image(jjn_dithered_image, text_top_left, "top_left")
    jjn_dithered_image = add_text_to_image(jjn_dithered_image, "JJN_" + text_bottom_right, "bottom_right", font_size=10)
    stucki_dithered_image = add_text_to_image(stucki_dithered_image, text_top_left, "top_left")
    stucki_dithered_image = add_text_to_image(stucki_dithered_image, "S_" + text_bottom_right, "bottom_right", font_size=10)

    # 디더링 적용 후 이미지 저장
    fs_output_path_with_text = os.path.join(folder_path, 'fs_output_image_with_text.bmp')
    fs_dithered_image.save(fs_output_path_with_text)
    jjn_output_path_with_text = os.path.join(folder_path, 'jjn_output_image_with_text.bmp')
    jjn_dithered_image.save(jjn_output_path_with_text)
    stucki_output_path_with_text = os.path.join(folder_path, 'stucki_output_image_with_text.bmp')
    stucki_dithered_image.save(stucki_output_path_with_text)
    logging.info("Image processing complete with text.")

    return fs_output_path_with_text, jjn_output_path_with_text, stucki_output_path_with_text

def show_popup(image_paths):
    root = tk.Tk()
    root.title("Dithered Images")

    for image_path in image_paths:
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)

        panel = tk.Label(root, image=img)
        panel.image = img  # Keep a reference to avoid garbage collection
        panel.pack(side="top", fill="both", expand="yes")

    root.mainloop()

if __name__ == "__main__":
    folder_path = r'Z:\\Jerry\\Photos\\2024\\2024-05 김주호\\ZV-E10\\'  # 실제 폴더 경로로 변경
    try:
        logging.info("Starting image processing...")
        fs_output_path_with_text, jjn_output_path_with_text, stucki_output_path_with_text = process_image(folder_path)
        logging.info("Displaying images...")
        show_popup([fs_output_path_with_text, jjn_output_path_with_text, stucki_output_path_with_text])
    except FileNotFoundError as e:
        tk.Tk().withdraw()
        logging.error(f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        tk.Tk().withdraw()
        logging.error(f"Unexpected error: {str(e)}")
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")
