import pygame
import sys
import os
from docx import Document
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hướng dẫn chơi game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_ORANGE = (255, 223, 186)
BUTTON_COLOR = (135, 206, 250)
BUTTON_HOVER_COLOR = (100, 149, 237)
BUTTON_TEXT_COLOR = BLACK

# Font
font_path = "fonts/Montserrat-Italic.ttf"
FONT_SIZE = 15
font = pygame.font.Font(font_path, FONT_SIZE)
button_font = pygame.font.Font(font_path, 18)

# Hàm thu nhỏ ảnh nếu quá lớn
# Hàm thu nhỏ ảnh nếu quá lớn và giảm thêm 50% nữa
def scale_image(image_path, max_width):
    image = pygame.image.load(image_path)
    width, height = image.get_size()

    if width > max_width:
        scale_factor = max_width / width
        new_width = int(width * scale_factor * 0.5)  # giảm thêm một nửa nữa
        new_height = int(height * scale_factor * 0.5)
    else:
        # Dù không vượt quá max_width thì vẫn giảm một nửa
        new_width = int(width * 0.5)
        new_height = int(height * 0.5)

    image = pygame.transform.scale(image, (new_width, new_height))
    return image


# 👉 Hàm đọc văn bản + hình ảnh từ file Word
def extract_docx_content(docx_path, image_dir="images"):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    doc = Document(docx_path)
    content = []
    image_count = 0

    for block in doc.element.body:
        if block.tag == qn("w:p"):
            paragraph_text = ""
            for run in block.iter(qn("w:r")):
                drawing = run.find(qn("w:drawing"))
                if drawing is not None:
                    blip = drawing.find(".//a:blip", namespaces={"a": "http://schemas.openxmlformats.org/drawingml/2006/main"})
                    if blip is not None:
                        r_embed = blip.attrib.get(qn("r:embed"))
                        image_part = doc.part.related_parts[r_embed]
                        image_data = image_part.blob

                        image_count += 1
                        image_filename = os.path.join(image_dir, f"image_{image_count}.png")
                        with open(image_filename, "wb") as f:
                            f.write(image_data)
                        content.append(('image', image_filename))
                text_elem = run.find(qn("w:t"))
                if text_elem is not None:
                    paragraph_text += text_elem.text
            if paragraph_text.strip():
                content.append(('text', paragraph_text.strip()))

    return content

# 👉 Đọc nội dung từ huongdan.docx
docx_content = extract_docx_content("huongdan.docx")

# Ngắt dòng văn bản dài
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Xử lý nội dung + ảnh
content_lines = []
for item in docx_content:
    if item[0] == 'text':
        wrapped = wrap_text(item[1], font, WIDTH - 80)
        content_lines.extend([('text', line) for line in wrapped])
        content_lines.append(('text', ''))  # dòng trống
    elif item[0] == 'image':
        content_lines.append(('image', item[1]))
        content_lines.append(('text', ''))  # dòng trống

# Tạo surface hiển thị nội dung
content_surface_height = 0
temp_lines = []

for item in content_lines:
    if item[0] == 'text':
        content_surface_height += FONT_SIZE + 10
    elif item[0] == 'image':
        try:
            image = scale_image(item[1], WIDTH - 80)
            content_surface_height += image.get_height() + 10
        except:
            content_surface_height += 100  # dự phòng nếu ảnh lỗi

content_surface_height += 50  # khoảng cách cuối
content_surface = pygame.Surface((WIDTH - 40, content_surface_height), pygame.SRCALPHA)
content_surface.fill((255, 255, 255, 230))

# Vẽ nội dung
y = 10
for item in content_lines:
    if item[0] == 'text':
        rendered_line = font.render(item[1], True, BLACK)
        content_surface.blit(rendered_line, (10, y))
        y += FONT_SIZE + 5
    elif item[0] == 'image':
        try:
            image = scale_image(item[1], WIDTH - 80)
            content_surface.blit(image, (10, y))
            y += image.get_height() + 10
        except:
            pass

# Nút trở về
button_text = button_font.render("Trở về", True, BUTTON_TEXT_COLOR)
button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

scroll_y = 0
scroll_speed = 20
running = True

while running:
    screen.fill(LIGHT_ORANGE)

    visible_area = pygame.Rect(20, 20, WIDTH - 40, HEIGHT - 100)
    screen.blit(content_surface, (visible_area.x, visible_area.y), area=pygame.Rect(0, scroll_y, visible_area.width, visible_area.height))

    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR, button_rect)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                running = False
                pygame.quit()
                import subprocess
                subprocess.run(["python", "gd_trangchu.py"])
            elif event.button == 4:
                scroll_y = max(scroll_y - scroll_speed, 0)
            elif event.button == 5:
                max_scroll = max(0, content_surface_height - (HEIGHT - 100))
                scroll_y = min(scroll_y + scroll_speed, max_scroll)

pygame.quit()
sys.exit()
