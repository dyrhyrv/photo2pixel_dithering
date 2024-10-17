from PIL import Image

def load_and_process_image(path, new_width=(int(input("Укажите новую ширину (рекомендую 180): ")))):
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print(f"Не нашёл изображения по пути {path}")
        return None

    width, height = img.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    img = img.resize((new_width, new_height)).convert('L')
    return img

def image_to_ascii(img):
    chars = ["@", "#", "$", "=", "*", "!", ";", ":", "~", "-", ",", ".", "_"]
    pixels = img.getdata()
    ascii_pixels = [chars[pixel // 25] for pixel in pixels]
    ascii_image = "\n".join(
        ''.join(ascii_pixels[i:i + img.width]) for i in range(0, len(ascii_pixels), img.width)
    )
    return ascii_image

def ascii_to_pattern(ascii_image, patterns):
    rows_list = []
    for line in ascii_image.splitlines():
        rows = ["", "", "", ""]
        for char in line:
            if char in patterns:
                for i in range(4):
                    rows[i] += patterns[char][i]
        rows_list.append("\n".join(rows))
    return "\n".join(rows_list)

def text_to_image(ascii_pattern, output_image):
    lines = [line.strip() for line in ascii_pattern.splitlines() if line.strip()]
    width = max(len(line) for line in lines)
    height = len(lines)

    image = Image.new('1', (width, height))
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            image.putpixel((x, y), 1 if char == '■' else 0)

    image.save(output_image)

patterns = {
    '@': ["□□□□", "□□□□", "□□□□", "□□□■"],
    '#': ["□□□□", "□■□□", "□□□□", "□□□■"],
    '$': ["□□□□", "□■□■", "□□□□", "□□□■"],
    '=': ["□□□□", "□■□■", "□□□□", "□■□■"],
    '*': ["□□□□", "□■□■", "□□■□", "□■□■"],
    '!': ["□□■□", "□■□■", "□□■□", "□■□■"],
    ';': ["□□■□", "□■□■", "■□■□", "□■□■"],
    ':': ["■□■□", "□■□■", "■□■□", "□■□■"],
    '~': ["■□■□", "■■□■", "■□■□", "■■■■"],
    '-': ["■□■□", "■■■■", "■□■□", "■■■■"],
    ',': ["■□■■", "■■■■", "■■■□", "■■■■"],
    '.': ["■□■■", "■■■■", "■■■■", "■■■■"],
    '_': ["■■■■", "■■■■", "■■■■", "■■■■"],
}

path = input("Укажите путь к изображению: ")
img = load_and_process_image(path)

if img:
    ascii_image = image_to_ascii(img)
    ascii_pattern = ascii_to_pattern(ascii_image, patterns)
    text_to_image(ascii_pattern, 'output_image.png')
    print("Изображение сохранено в 'output_image.png'")