import pygame
import sys
import os

# --- Khởi tạo ---
pygame.init()
WIDTH, HEIGHT = 750, 550  # Kích thước cửa sổ mới
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kết quả trận đấu")

# --- Load font từ file TTF bạn gửi ---
font_path = "fonts/Montserrat-Italic.ttf"
if not os.path.exists(font_path):
    print("Không tìm thấy file font!")
    sys.exit()

font = pygame.font.Font(font_path, 20)
big_font = pygame.font.Font(font_path, 24)

# --- Màu sắc (quản lý bằng list) ---
colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "LIGHT_BLUE": (200, 255, 255),
    "HOVER_BLUE": (150, 220, 255),
    "BG_COLOR": (255, 239, 196)
}

# --- Dữ liệu kết quả ---
# Kiểm tra số lượng tham số
import sys

if len(sys.argv) >= 3:
    diem_doi_thu = int(sys.argv[1])      # players[0]
    diem_nguoi_choi = int(sys.argv[2])   # players[1]

    if diem_nguoi_choi > diem_doi_thu:
        ket_qua = "Bạn thua"
    elif diem_nguoi_choi < diem_doi_thu:
        ket_qua = "Bạn thắng"
    else:
        ket_qua = "Hoà"



# --- Hàm hành động ---
def menu_action():
    pygame.quit()
    import subprocess
    subprocess.run(["python", "gd_trangchu.py"])


def tiep_tuc_action():
    pygame.quit()
    import subprocess
    subprocess.run(["python", "capdo.py"])


# --- Hàm vẽ nút với hiệu ứng và hành động ---
def draw_button(rect, text, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, colors["HOVER_BLUE"], rect)
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, colors["LIGHT_BLUE"], rect)

    pygame.draw.rect(screen, colors["BLACK"], rect, 1)
    label = font.render(text, True, colors["BLACK"])
    screen.blit(label, label.get_rect(center=rect.center))


# --- Hàm vẽ hộp điểm ---
def draw_score_box(x, y, score):
    width, height = 100, 80  # Cập nhật kích thước hộp điểm
    pygame.draw.rect(screen, colors["WHITE"], (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, colors["BLACK"], (x, y, width, height), 2, border_radius=10)
    score_text = big_font.render(str(score), True, colors["BLACK"])
    screen.blit(score_text, score_text.get_rect(center=(x + width // 2, y + height // 2)))


# --- Vòng lặp chính ---
running = True
while running:
    screen.fill(colors["BG_COLOR"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ hộp kết quả (Cập nhật kích thước và vị trí cho phù hợp với cửa sổ lớn hơn)
    box = pygame.Rect(200, 120, 400, 300)  # Vị trí và kích thước hộp kết quả
    pygame.draw.rect(screen, colors["WHITE"], box)
    pygame.draw.rect(screen, colors["BLACK"], box, 1)

    # Tiêu đề
    title_text = font.render(ket_qua, True, colors["BLACK"])
    screen.blit(title_text, (box.x + 10, box.y + 5))

    # Biểu tượng tròn
    pygame.draw.circle(screen, colors["LIGHT_BLUE"], (box.right - 15, box.y + 15), 10, 1)

    # Vị trí căn giữa cho 2 ô điểm và vạch phân cách
    score_box_width = 100
    total_width = 2 * score_box_width + 50  # Tổng chiều rộng của 2 ô điểm và khoảng cách
    score_x = box.x + (box.width - total_width) // 2 # Căn giữa

    # Vẽ điểm số 1
    draw_score_box(score_x, box.y + 100, diem_nguoi_choi)

    # Vẽ vạch phân cách
    line_x = score_x + score_box_width + 20  # Vị trí vạch phân cách
    pygame.draw.line(screen, colors["BLACK"], (line_x, box.y + 100),
                     (line_x, box.y + 180), 2)

    # Vẽ điểm số 2
    draw_score_box(line_x + 20, box.y + 100, diem_doi_thu)

    # Vẽ 2 nút có tương tác (Chuyển nút xuống dưới và căn sang hai bên)
    draw_button(pygame.Rect(box.x + 30, box.y + 230, 120, 40), "Menu", menu_action)
    draw_button(pygame.Rect(box.x + 250, box.y + 230, 120, 40), "Tiếp tục", tiep_tuc_action)

    pygame.display.flip()

pygame.quit()
sys.exit()
