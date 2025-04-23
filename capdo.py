import pygame
import sys

pygame.init()

# --- Cấu hình ---
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT_SIZE = 24
FONT = pygame.font.Font("fonts/Montserrat-Regular.ttf", FONT_SIZE)
font_dan = pygame.font.Font("fonts/Montserrat-Regular.ttf", 15)
# Khởi tạo âm thanh hiệu ứng (ngắn)
effect_sound = pygame.mixer.Sound("AmThanh\TiengBamNut.mp3")  # Tải hiệu ứng âm thanh (ví dụ: nhấn nút)

# --- Khởi tạo màn hình ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chọn Cấp Độ Game")

clock = pygame.time.Clock()

# --- Hàm vẽ nút ---
def draw_button(surface, rect, text):
    pygame.draw.rect(surface, (173, 216, 230), rect, border_radius=8)  # Màu nút xanh nhạt
    text_surface = font_dan.render(text, True, (0, 0, 0))  # Chữ đen
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# --- Hàm chuyển màn hình (giả lập) ---
def change_screen(level):
    return level
    # Chuyển đến màn hình khác (ở đây bạn có thể mở màn hình game hoặc giao diện khác)
    # Ví dụ: return hoặc sử dụng pygame để mở màn hình mới

# --- Vòng lặp chính ---
running = True
current_level = "easy"  # Cấp độ mặc định là "easy"
def chon_cap_do():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    effect_sound.play()
                    pygame.time.wait(int(effect_sound.get_length() * 1000))
                    if easy_button_rect.collidepoint(event.pos):
                        return "easy"
                    elif medium_button_rect.collidepoint(event.pos):
                        return "medium"
                    elif hard_button_rect.collidepoint(event.pos):
                        return "hard"

        screen.fill((255, 228, 181))

        title_surface = FONT.render("CHỌN CẤP ĐỘ GAME", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_surface, title_rect)

        easy_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
        medium_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        hard_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

        draw_button(screen, easy_button_rect, "Dễ ")
        draw_button(screen, medium_button_rect, "Vừa")
        draw_button(screen, hard_button_rect, "Khó")

        pygame.display.flip()

if __name__ == "__main__":
    level = chon_cap_do()
    pygame.quit()
    import subprocess
    subprocess.run(["python", "main_pygame.py", level])
