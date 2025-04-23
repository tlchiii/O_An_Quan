import pygame
from pygame import Color

pygame.init()

# Tạo cửa sổ game
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ô Ăn Quan - Trang Chủ")

# Load ảnh nền
background = pygame.image.load(r"asset/o_an_quan.png")
background = pygame.transform.scale(background, (800, 600))  # Đúng kích thước màn hình

# Tải font Unicode từ file .ttf
font = pygame.font.Font("fonts\Montserrat-Regular.ttf", 25)
# Text với ký tự tiếng Việt
text2 = font.render("Chơi Game", True, (0, 0, 0))
text3 = font.render("Hướng Dẫn", True, (0,0,0))
text4 = font.render("Thoát", True, (0,0,0))

# Load hình nut am thanh
anh_at_bat = pygame.image.load(r"asset\loud-sound.png")
anh_at_bat = pygame.transform.scale(anh_at_bat, (30, 30))
anh_at_tat = pygame.image.load(r"asset\enable-sound.png")
anh_at_tat = pygame.transform.scale(anh_at_tat, (30, 30))

#Khoi tao nut
btnvChoi,btnChoi = pygame.Rect(47, 473, 167, 53),pygame.Rect(50, 470, 170, 50)
btnvHD,btnHD = pygame.Rect(317, 473, 167, 53),pygame.Rect(320, 470, 170, 50)
btnvThoat,btnThoat = pygame.Rect(567, 473, 167, 53),pygame.Rect(570, 470, 170, 50)
btnColor = Color(223, 220, 170,100)
btn_hover_color = Color(186,181,163,100)
running = True

# Khởi tạo pygame mixer
pygame.mixer.init()

# Tải và phát nhạc
pygame.mixer.music.load("AmThanh\YourNameSong.mp3")  # Thay "your_song.mp3" bằng tên file nhạc của bạn
pygame.mixer.music.play(-1, 0.0)  # -1 để phát nhạc lặp lại vô tận, 0.0 là bắt đầu từ đầu

# Khởi tạo âm thanh hiệu ứng (ngắn)
effect_sound = pygame.mixer.Sound("AmThanh\TiengBamNut.mp3")  # Tải hiệu ứng âm thanh (ví dụ: nhấn nút)


#Xu ly phu
current_anh_at = anh_at_bat
while running:
    screen.blit(background, (0, 0))  # Vẽ ảnh nền

    # Lấy vị trí chuột
    mouse_pos = pygame.mouse.get_pos()

    # Kiểm tra nếu chuột đang nằm trên nút
    btnChoi_color = btn_hover_color if btnChoi.collidepoint(mouse_pos) else btnColor
    btnThoat_color = btn_hover_color if btnThoat.collidepoint(mouse_pos) else btnColor
    btnHD_color = btn_hover_color if btnHD.collidepoint(mouse_pos) else btnColor

    # Vẽ nút
    pygame.draw.rect(screen, (0, 0, 0, 0), btnvChoi, border_radius=25)
    pygame.draw.rect(screen, btnChoi_color, btnChoi, border_radius=25)  # Nút chơi game
    screen.blit(text2, text2.get_rect(center=btnChoi.center))
    pygame.draw.rect(screen, (0, 0, 0, 0), btnvHD, border_radius=25)
    pygame.draw.rect(screen, btnHD_color, btnHD, border_radius=25)  # Nút hướng dẫn
    screen.blit(text3, text3.get_rect(center=btnHD.center))
    pygame.draw.rect(screen, (0, 0, 0, 0), btnvThoat, border_radius=25)
    pygame.draw.rect(screen, btnThoat_color, btnThoat , border_radius=25)  # Nút thoát
    screen.blit(text4, text4.get_rect(center=btnThoat.center))

    # Hiển thị hình âm thanh
    screen.blit(current_anh_at, (750, 550))

    # Xác định vị trí ảnh
    anh_at_rect = pygame.Rect(750, 550, 30, 30)  # Tạo vùng bấm

    # Xử lý sự kiện
    for event in pygame.event.get():
        if current_anh_at == anh_at_tat: pygame.mixer.music.pause()
        else: pygame.mixer.music.unpause()
        if event.type == pygame.QUIT:
            running = False

        # Kiểm tra sự kiện nhấn chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btnChoi.collidepoint(event.pos):
                effect_sound.play()
                # Đợi âm thanh hiệu ứng kết thúc (giả sử âm thanh kéo dài 1 giây)
                pygame.time.wait(int(effect_sound.get_length() * 1000))
                pygame.quit()
                import subprocess
                subprocess.run(["python", "capdo.py"])
            if btnHD.collidepoint(event.pos):
                effect_sound.play()
                pygame.time.wait(int(effect_sound.get_length() * 1000))
                pygame.quit()
                import subprocess
                subprocess.run(["python", "huongdan.py"])

                print("Chuyển sang màn hình hướng dẫn!")  # Thay bằng code để chuyển màn hình
            if btnThoat.collidepoint(event.pos):
                effect_sound.play()
                pygame.time.wait(int(effect_sound.get_length() * 1000))
                print("Thoát trò chơi!")  # Đóng game
                running = False
            if anh_at_rect.collidepoint(event.pos):
                # Đổi ảnh khi nhấn
                current_anh_at = anh_at_tat if current_anh_at == anh_at_bat else anh_at_bat


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
# Dừng nhạc khi thoát game
pygame.mixer.music.stop()

pygame.quit()
