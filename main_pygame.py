import copy
import math
import os
import time
import random

import pygame

from box_pygame import ovuong, o_diem,box
from pygame import Color, FULLSCREEN
from docx import Document
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

import sys

AI_LEVEL = "easy"  # mặc định nếu không truyền cấp độ

# Màu sắc
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
#

BROWN = '#63371E'
# BROWN = '#7B4425'
NEN = '#BED8CF'

pygame.init()
# Lấy độ phân giải hiện tại của màn hình
info = pygame.display.Info()
# WIDTH = 800
# HEIGHT = 400
size = 120
WIDTH = info.current_w - 400
HEIGHT = info.current_h - 200
# WIDTH = info.current_w
# HEIGHT = info.current_h
xS = WIDTH//2 - (7*size)/2
yS = HEIGHT//2 - size
choosed = -1
CHOOSING = True
current_player = 0  # Người chơi 1 (0) bắt đầu
players = [0, 0]  # Tổng số hạt ăn được của mỗi người chơi
huong = 0
END = False

# Cập nhật điểm
font_dan = pygame.font.Font("fonts\\Montserrat-Regular.ttf", 15)


# Thời gian
time_font = pygame.font.Font('fonts\\Montserrat-Medium.ttf', 30)
font_mon = pygame.font.Font("fonts\\Montserrat-Light.ttf", 20)
menu_mon = pygame.font.Font("fonts\\Montserrat-LightItalic.ttf", 40)

# Load hình nut am thanh
anh_at_bat = pygame.image.load(r"asset\loud-sound.png")
anh_at_bat = pygame.transform.scale(anh_at_bat, (30, 30))
anh_at_tat = pygame.image.load(r"asset\enable-sound.png")
anh_at_tat = pygame.transform.scale(anh_at_tat, (30, 30))

#Xu ly phu
current_anh_at = anh_at_bat

# Khởi tạo pygame mixer
pygame.mixer.init()

# Tải và phát nhạc
pygame.mixer.music.load("AmThanh\\YourNameSong.mp3")  # Thay "your_song.mp3" bằng tên file nhạc của bạn
pygame.mixer.music.play(-1, 0.0)  # -1 để phát nhạc lặp lại vô tận, 0.0 là bắt đầu từ đầu

def draw_board():
    for i in board:
        if i.isQuan == False:
            pygame.draw.rect(screen,BROWN,i.rect,1)
        else:
            if i.index == 0:
                start_angle = math.radians(90)
                end_angle = math.radians(270)
                i.rect = pygame.Rect(i.x,i.y,i.size*2,i.size*2)
                pygame.draw.arc(screen, BROWN, i.rect, start_angle, end_angle)

            if i.index == 6:
                start_angle = math.radians(-90)
                end_angle = math.radians(90)
                i.rect = pygame.Rect(i.x-i.size, i.y-i.size, i.size * 2, i.size * 2)
                pygame.draw.arc(screen, BROWN, i.rect, start_angle, end_angle)

        text = font_dan.render(str(i.numDan), True, BLACK)
        screen.blit(text, (i.x + 2, i.y + i.size-20))

# Hàm để xử lý sự kiện click chuột
def chon_o():
    global choosed
    if CHOOSING == True and choosed != -1 and is_moving == False:
        pygame.draw.rect(screen, GREEN, board[choosed].rect, 3)  # Vẽ lại ô khi chọn
        arrow(board[choosed])
    if CHOOSING == False and choosed != -1 and is_moving == False:
        pygame.draw.rect(screen, GREEN, board[choosed].rect, 3)  # Vẽ lại ô khi chọn
        print("chon")


# hình bàn tay dải dân
def dai_dan_hand(hientai):
    if hientai != -1:
        hand = pygame.image.load('asset\\hand.png')
        hand_rect = hand.get_rect()
        hand_rect.topleft = (board[hientai].x, board[hientai].y)
        screen.blit(hand, hand_rect)

# Vẽ cờ lượt chơi
def ve_co():
    flagImg = pygame.image.load('asset\\flag_red_sm.png')
    flagImg = pygame.transform.scale(flagImg, (60, 60))
    flag_rect = flagImg.get_rect()
    fx = flagImg.get_width()
    fy = flagImg.get_height()
    if current_player == 0:
        flag_rect.bottomleft = (WIDTH / 2 + 50, HEIGHT)
    else:
        flag_rect.bottomleft = (WIDTH / 2+50, fy)
    screen.blit(flagImg, flag_rect)


def click(pos):
    global choosed
    if CHOOSING == True:
        if current_player==0:
            for i in range(7, 12, 1):
                if board[i].rect.collidepoint(pos[0], pos[1]):
                    if board[i].numDan > 0:
                        choosed = i
                        print(choosed)
                        break
                else:
                    choosed = -1
        else:
            for i in range(1, 6, 1):
                if board[i].rect.collidepoint(pos[0], pos[1]):
                    if board[i].numDan > 0:
                        choosed = i
                        print(choosed)
                        break
                    choosed = -1

def ve_player():
    player_img = pygame.image.load("asset\\teo.png")
    ai_img = pygame.image.load("asset\\ti.png")
    player_rect = player_img.get_rect()
    ai_rect = ai_img.get_rect()
    player_rect.bottom = HEIGHT
    player_rect.left = WIDTH//2 - player_img.get_width()/2
    ai_rect.top = 0
    ai_rect.left = WIDTH//2 - ai_img.get_width()/2

    screen.blit(player_img,player_rect)
    screen.blit(ai_img,ai_rect)

# vẽ ô điêm
def ve_o_diem():
    screen.blit(odiem[0].image,odiem[0].rect)
    screen.blit(odiem[1].image,odiem[1].rect)
    # pygame.draw.circle(screen, BROWN, ((WIDTH / 4)*3, HEIGHT-50), 50, 1)
    for i in range(2):
        text = font_mon.render(str(players[i]), True, BLACK)
        screen.blit(text, (odiem[i].rect.x + 3*(odiem[i].rect.width/5)  ,odiem[i].rect.y +3*(odiem[i].rect.height/5)))
    for x in odiem:
        x.eated_stone(screen)

def repaint():
    screen.blit(bg_img, bg_img_rect)
    draw_board()
    ve_o_diem()
    draw_button(screen, menu_button_rect, "Menu")
    # Hiển thị hình âm thanh
    screen.blit(current_anh_at, (WIDTH - 100, HEIGHT - 600))
    pygame.draw.rect(screen, (255, 204, 102), suggest_button_rect)
    text_surface = button_font.render("Gợi ý", True, BLACK)
    screen.blit(text_surface, (suggest_button_rect.x + 10, suggest_button_rect.y + 10))
    suggest_text = font.render(f"Gợi ý còn: {suggest_limit - suggest_count}", True, (0, 0, 0))
    screen.blit(suggest_text, (suggest_button_rect.x, suggest_button_rect.y - 25))

    # Tạo vùng bấm0
    for i in board:
        i.ve_quan(screen)
        i.draw_stone(screen)
    ve_player()
    ve_co()
    ve_timer()
    chon_o()

    # Xác định vị trí ảnh
anh_at_rect = pygame.Rect(WIDTH - 100, HEIGHT - 600, 30, 30)
def update():
    repaint()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("pause")
        pauseGame()

def arrow(o):
    arrow_left = pygame.image.load("asset\\arrow_left_sz.png")
    arrow_right = pygame.image.load('asset\\arrow_right_sz.png')
    arrow_green_left = pygame.image.load('asset\\green_arrow_left.png')
    arrow_green_right = pygame.image.load('asset\\green_arrow_right.png')
    arrow_left_rec = arrow_left.get_rect()
    arrow_right_rec = arrow_right.get_rect()
    arrow_left_rec.center = (o.x,o.y + o.size/2)
    arrow_right_rec.center = (o.x+ o.size,o.y + o.size/2)
    if huong ==0:
        screen.blit(arrow_left, arrow_left_rec)
        screen.blit(arrow_right, arrow_right_rec)
    else:
        if current_player == 0:
            if huong == -1:
                screen.blit(arrow_green_left, arrow_left_rec)
            elif huong == 1:
                screen.blit(arrow_green_right, arrow_right_rec)
        else:
            if huong == 1:
                screen.blit(arrow_green_left, arrow_left_rec)
            elif huong == -1:
                screen.blit(arrow_green_right, arrow_right_rec)

# Lượt của ngươi chơi
def set_dichuyen():
    global huong,choosed, is_moving, move_info, CHOOSING, game_state
    # if het_dan():
    #     tra_dan()
    #     update()
    print("set_dichuyen")

    CHOOSING = False
    is_moving = True
    move_info["hientai"] = choosed
    move_info["num"] = board[choosed].numDan
    board[choosed].numDan = 0
    board[choosed].xoa_dan()
    boxs[choosed].numDan = 0

def tinh_toan(so_o,huong,board_copy):
    cal = 0
    if huong != 0 and so_o != -1:
        hientai = so_o
        num = board_copy[so_o].numDan
        board_copy[so_o].numDan = 0
        # board_copy[so_o].xoa_dan()
        while num > 0:
            #  -1 : trái, 1: phải
            if (huong == -1): hientai = (hientai + 1) % len(board_copy)
            if (huong == 1): hientai = (hientai - 1) % len(board_copy)

            # board_copy[hientai].add_stone()
            board_copy[hientai].numDan +=1
            num -= 1
        if matLuot(hientai,huong,board_copy):
            is_ok = an_check(hientai)
            cal += Cal_an(hientai,huong,board_copy)
            print("matluot " + str(cal))
            # để xem có được ăn cách ô liên tiêp hay khong
            if is_ok:
                next_2 = (hientai - huong * 2) % len(board)
                if an_check(next_2):
                    print("an tiep " + str(next_2))
                    cal += Cal_an(next_2,huong,board_copy)
            return cal
        else:
            # nếu đi tiếp thì lấy ô tiếp theo gọi hàm tính toán
            tiep = (hientai - huong) % len(board_copy)
            return tinh_toan(tiep, huong,board_copy)
    # return cal

def dichuyen():
    global choosed, CHOOSING
    global huong
    global current_player
    global time_left
    global is_moving, running
    global move_info, game_state
    if huong != 0 and move_info["hientai"] != None and is_moving:
        hientai = move_info["hientai"]
        num = move_info["num"]
        if num > 0:
            if (huong == -1): hientai = (hientai + 1) % len(board)
            if (huong == 1): hientai= (hientai - 1) % len(board)

            board[hientai].add_stone()
            boxs[hientai].numDan +=1
            move_info["num"] -= 1
            move_info["hientai"] = hientai
            repaint()
            dai_dan_hand(hientai)
            pygame.display.flip()
            # clock.tick(2.5)
            pygame.time.delay(400)
        else:
            if matLuot(hientai,huong,board):
                is_ok = an_check(hientai)
                # để xem có được ăn cách ô liên tiêp hay khong
                if is_ok:
                    an(hientai)



                huong = 0
                choosed = -1
                is_moving = False
                current_player = 1 - current_player
                if current_player == 0:
                    time_left = 15
                print("mat luot - " + str(hientai))
                # kiểm tra dải quân
                if ket_thuc():
                    game_state = "END"
                    return
                else:
                    if het_dan() == True and players[current_player] >= 5:
                        tra_dan()
                    elif het_dan() == True and players[current_player] < 5:
                        game_state = "END"
                        return

                CHOOSING = True
            else:
                is_moving = False
                choosed = (hientai - huong) % len(board)
                print(choosed)
                repaint()
                # chon_o()
                dai_dan_hand(choosed)
                pygame.display.flip()
                pygame.time.delay(400)
                # clock.tick(2.5)
                move_info["hientai"] = choosed
                move_info["num"] = board[choosed].numDan
                board[choosed].numDan = 0
                board[choosed].xoa_dan()
                boxs[choosed].numDan = 0
                is_moving = True

# kiểm tra xem đi tiếp, ăn hay mất lượt
def matLuot(hientai,huong,board):
    otieptheo = -1
    if huong == -1:
        otieptheo = (hientai + 1) % len(board)
    else:
        otieptheo = (hientai - 1) % len(board)

    if otieptheo == 0 or otieptheo == 6:
        # nếu ô tiếp theo là ô quan -> mất lượt
        return True
    elif board[otieptheo].numDan > 0:
        return False
    elif board[otieptheo].numDan == 0:
        return True
    return False

def an(hientai):
    otieptheo = -1
    if huong == -1:
        otieptheo = (hientai + 1) % len(board)
        tiep_otieptheo = (otieptheo + 1) % len(board)
    if huong == 1:
        otieptheo = (hientai - 1) % len(board)
        tiep_otieptheo = (otieptheo - 1) % len(board)

    if (board[otieptheo].numDan == 0 and board[otieptheo].isQuan == False):
        if tiep_otieptheo == 0 or tiep_otieptheo == 6:
            #    neu la o quan thi so dan >= 5 moi dc an
            if board[tiep_otieptheo].numQuan>0 and board[tiep_otieptheo].numDan >= 5:
                players[current_player] += board[tiep_otieptheo].numDan + board[tiep_otieptheo].numQuan
                board[tiep_otieptheo].numDan = 0
                board[tiep_otieptheo].numQuan = 0
                # bbox để tính toán
                boxs[tiep_otieptheo].numDan = 0
                boxs[tiep_otieptheo].numQuan = 0

                board[tiep_otieptheo].move_dan(odiem[current_player])
                # board[tiep_otieptheo].xoa_dan()b

                print("an")
            elif board[tiep_otieptheo].numQuan==0 and board[tiep_otieptheo].numDan >0:
                players[current_player] += board[tiep_otieptheo].numDan + board[tiep_otieptheo].numQuan
                board[tiep_otieptheo].numDan = 0
                board[tiep_otieptheo].numQuan = 0
                # bbox để tính toán
                boxs[tiep_otieptheo].numDan = 0
                boxs[tiep_otieptheo].numQuan = 0

                board[tiep_otieptheo].move_dan(odiem[current_player])

        elif board[tiep_otieptheo].numDan > 0:
            players[current_player] += board[tiep_otieptheo].numDan
            board[tiep_otieptheo].numDan = 0
            board[tiep_otieptheo].move_dan(odiem[current_player])
            # board[tiep_otieptheo].xoa_dan()
            boxs[tiep_otieptheo].numDan = 0
            print("an")

    if an_check(tiep_otieptheo):
        print("an tiep" + str(tiep_otieptheo))
        an(tiep_otieptheo)

# kiểm tra có ăn dc k
def an_check(hientai):
    otieptheo = -1
    tiep_otieptheo = -1  # ✅ Khởi tạo mặc định

    if huong == -1:
        otieptheo = (hientai + 1) % len(board)
        tiep_otieptheo = (otieptheo + 1) % len(board)
    elif huong == 1:
        otieptheo = (hientai - 1) % len(board)
        tiep_otieptheo = (otieptheo - 1) % len(board)
    else:
        return False  # ✅ nếu huong không hợp lệ

    if (board[otieptheo].numDan == 0 and board[otieptheo].isQuan == False):
        if  tiep_otieptheo == 0 or tiep_otieptheo == 6:
            if board[tiep_otieptheo].numQuan >0 and board[tiep_otieptheo].numDan >= 5:
                return True
            elif board[tiep_otieptheo].numQuan == 0 and board[tiep_otieptheo].numDan > 0:
                return True
        elif board[tiep_otieptheo].numDan == 0:
            return False
        else:
            return True
    return False

# tính toán an dc bao nhiêu dân
def Cal_an(hientai,huong,board_cp):
    count = 0
    otieptheo = -1
    tiep_otieptheo = -1
    if huong == -1:
        otieptheo = (hientai + 1) % 12
        tiep_otieptheo = (otieptheo + 1) % 12
    if huong == 1:
        otieptheo = (hientai - 1) % 12
        tiep_otieptheo = (otieptheo - 1) % 12

    if (board_cp[otieptheo].numDan == 0):
        if tiep_otieptheo == 0 or tiep_otieptheo == 6:
            #    neu la o quan thi so dan >= 5 moi dc an
            if board[tiep_otieptheo].numQuan==5 and  board_cp[tiep_otieptheo].numDan >= 5:
                count += board_cp[tiep_otieptheo].numDan + board_cp[tiep_otieptheo].numQuan

                board_cp[tiep_otieptheo].numDan = 0
                board_cp[tiep_otieptheo].numQuan = 0
            elif board[tiep_otieptheo].numQuan == 0 and board[tiep_otieptheo].numDan > 0:
                count += board_cp[tiep_otieptheo].numDan + board_cp[tiep_otieptheo].numQuan

                board_cp[tiep_otieptheo].numDan = 0
                board_cp[tiep_otieptheo].numQuan = 0

        else:
            count += board_cp[tiep_otieptheo].numDan
            board_cp[tiep_otieptheo].numDan = 0
            board_cp[tiep_otieptheo].numQuan = 0

    return count
dang_di_chuyen = False  # True khi bắt đầu rải quân, False khi rải xong

def ket_thuc():
    # các ô bên mình đã hết dân và không đủ dân để dải
    if het_dan()==True and players[current_player] < 5:
        return True
    # 2 ô quan bị ăn hết
    if board[0].numQuan ==0 and  board[0].numDan == 0 and board[6].numQuan == 0 and board[6].numDan == 0:
        return True

    return False



# kiểm tra các ô bên mình có hết dân k
def het_dan():
    if current_player == 0:
        for i in range(7, 12, 1):
            if board[i].numDan >0:
                return False
        return True
    elif current_player == 1:
        for i in range(1, 6, 1):
            if board[i].numDan > 0:
                return False
        return True

    return False

"trả lại dân vào ô chơi nêu hết dân để đi"
def tra_dan():
    if current_player == 0:
        for i in range(7, 12, 1):
            # dải lại 5 đá ăn được vào các ô của mình
            board[i].add_stone()
            boxs[i].numDan +=1
            # thêm đá vao ô
            stones = list(odiem[current_player].stone_group)
            if stones:
                da = stones.pop()  # lấy đá cuối cùng
                odiem[current_player].stone_group.remove(da)
        players[current_player] -= 5

    elif current_player == 1:
        for i in range(1, 6, 1):
            # dải lại 5 đá ăn được vào các ô của mình
            board[i].add_stone()
            # thêm đá vao ô
            stones = list(odiem[current_player].stone_group)
            if stones:
                da = stones.pop()  # lấy đá cuối cùng
                odiem[current_player].stone_group.remove(da)
        players[current_player] -= 5

def random_choosed():
    global choosed
    global huong
    if current_player ==0 :
        x = random.randint(7, 11)
        while board[x].numDan ==0 :
            x = random.randint(7, 11)

    if current_player == 1:
        x = random.randint(1, 5)
        while board[x].numDan ==0 :
            x = random.randint(1, 5)
    print(str(x))
    huong = random.choice([1, -1])
    choosed = x

def ve_timer():
    global time_left
    if time_left >= 0:
        tg_con_lai = time_font.render(str(time_left), True, GREEN)
        screen.blit(tg_con_lai, ((WIDTH/5)*2, HEIGHT - 40))

def pauseGame():
    global running, game_state
    global is_pause, is_moving
    is_pause = True
    while is_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_pause= False
                # is_moving = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tiepTuc_btn_rect.collidepoint(event.pos):
                    is_pause = False
                if menu_btn_rect.collidepoint(event.pos):
                    game_state = "begin"
                    is_pause = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    print("tiep tuc")
                    is_pause = False

        screen.blit(bg_img, bg_img_rect)
        draw_board()

        # btn_tiepTuc = menu_mon.render("Tiếp tục",True,'yellow')
        # btn_Menu = menu_mon.render("Menu",True,'yellow')

        tiepTuc_btn_rect = pygame.Rect(0,0,100,50)
        tiepTuc_btn_rect.center = (WIDTH/2,HEIGHT/2 -50)

        menu_btn_rect = pygame.Rect(0, 0, 100, 50)
        menu_btn_rect.center = (WIDTH / 2, HEIGHT / 2 + 50)

        draw_button(screen, tiepTuc_btn_rect, "Tiếp tục")
        draw_button(screen, menu_btn_rect, "Trang chủ")

        pygame.display.flip()

def draw_button(surface, rect, text):
    pygame.draw.rect(surface, (173, 216, 230), rect, border_radius=8)  # Màu nút xanh nhạt
    text_surface = font_mon.render(text, True, (0, 0, 0))  # Chữ đen
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def reset():
    global current_player, choosed,huong
    global CHOOSING,is_moving, time_left
    board.clear()
    boxs.clear()
    odiem.clear()
    for i in range(0, 12, 1):
        x = ovuong(xS, yS, i)
        board.append(x)
        b = box(i)
        boxs.append(b)
    player = o_diem((WIDTH / 4) * 2.5, HEIGHT - 84)
    ai = o_diem(WIDTH / 4, 0)
    odiem.append(player)
    odiem.append(ai)
    current_player = 0
    players[0] = 0
    players[1] = 0
    choosed = -1
    huong = 0
    CHOOSING = True
    is_moving = False
    time_left = 15

def begin():
    global game_state, running

    # Load ảnh nền
    background = pygame.image.load(r"asset/o_an_quan.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Đúng kích thước màn hình

    # Tải font Unicode từ file .ttf
    font = pygame.font.Font("fonts\\Montserrat-Regular.ttf", 25)
    # Text với ký tự tiếng Việt
    text2 = font.render("Cấp Độ", True, (0, 0, 0))
    text3 = font.render("Hướng Dẫn", True, (0, 0, 0))
    text4 = font.render("Thoát", True, (0, 0, 0))


    # Khoi tao nut
    btnvChoi, btnChoi = pygame.Rect(WIDTH-953, HEIGHT-167, 167, 53), pygame.Rect(WIDTH-950, HEIGHT-170, 170, 50)
    btnvHD, btnHD = pygame.Rect(WIDTH-613, HEIGHT-167, 167, 53), pygame.Rect(WIDTH-610, HEIGHT-170, 170, 50)
    btnvThoat, btnThoat = pygame.Rect(WIDTH-303, HEIGHT-167, 167, 53), pygame.Rect(WIDTH-300, HEIGHT-170, 170, 50)
    btnColor = Color(223, 220, 170, 100)
    btn_hover_color = Color(186, 181, 163, 100)

    btnChoi.center = (WIDTH/5,(HEIGHT/5)*4)
    btnvChoi.center = ((WIDTH / 5)-3, ((HEIGHT / 5) * 4)+3)

    btnHD.center = ((WIDTH/5)*2.5,(HEIGHT/5)*4)
    btnvHD.center = ((WIDTH/5)*2.5 - 3, (HEIGHT/5)*4+ 3)

    btnThoat.center = ((WIDTH / 5) * 4, (HEIGHT / 5) * 4)
    btnvThoat.center = ((WIDTH / 5) * 4 - 3, (HEIGHT / 5) * 4+ 3)

    # Khởi tạo âm thanh hiệu ứng (ngắn)
    effect_sound = pygame.mixer.Sound("AmThanh\\TiengBamNut.mp3")  # Tải hiệu ứng âm thanh (ví dụ: nhấn nút)



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
    pygame.draw.rect(screen, btnThoat_color, btnThoat, border_radius=25)  # Nút thoát
    screen.blit(text4, text4.get_rect(center=btnThoat.center))



    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Kiểm tra sự kiện nhấn chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btnChoi.collidepoint(event.pos):
                effect_sound.play()
                game_state = "LEVEL"
            if btnHD.collidepoint(event.pos):
                effect_sound.play()
                game_state = "INSTRUCTION"

                print("Chuyển sang màn hình hướng dẫn!")  # Thay bằng code để chuyển màn hình
            if btnThoat.collidepoint(event.pos):
                effect_sound.play()
                pygame.time.wait(int(effect_sound.get_length() * 500))
                print("Thoát trò chơi!")  # Đóng game
                running = False


    pygame.display.flip()

def capdo():
    global game_state, running, AI_LEVEL
    FPS = 60
    FONT_SIZE = 24
    FONT = pygame.font.Font("fonts\\Montserrat-Regular.ttf", FONT_SIZE)
    font_dan = pygame.font.Font("fonts\\Montserrat-Regular.ttf", 15)
    # Khởi tạo âm thanh hiệu ứng (ngắn)
    effect_sound = pygame.mixer.Sound("AmThanh\\TiengBamNut.mp3")  # Tải hiệu ứng âm thanh (ví dụ: nhấn nút)

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


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                effect_sound.play()
                pygame.time.wait(int(effect_sound.get_length() * 500))
                if easy_button_rect.collidepoint(event.pos):
                    AI_LEVEL = "easy"
                    game_state = "PLAYING"
                elif medium_button_rect.collidepoint(event.pos):
                    AI_LEVEL = "medium"
                    game_state = "PLAYING"
                elif hard_button_rect.collidepoint(event.pos):
                    AI_LEVEL ="hard"
                    game_state = "PLAYING"

def scale_image(image_path, max_height):
    image = pygame.image.load(image_path)
    width, height = image.get_size()
    scale_ratio = max_height / height
    new_width = int(width * scale_ratio)
    new_image = pygame.transform.smoothscale(image, (new_width, max_height))
    return new_image

# Đọc nội dung từ Word
def extract_docx_content(docx_path, image_dir="images"):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    doc = Document(docx_path)
    content = []
    image_count = 0

    for block in doc.element.body:
        if block.tag == qn("w:p"):
            line_items = []
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
                        line_items.append(('image', image_filename))
                text_elem = run.find(qn("w:t"))
                if text_elem is not None:
                    line_items.append(('text', text_elem.text))
            if line_items:
                first_text = ''
                for item in line_items:
                    if item[0] == 'text' and item[1].strip():
                        first_text = item[1].strip()
                        break
                should_indent = not first_text.startswith('*')
                content.append(('line', line_items, should_indent))

    return content

# Hiển thị dòng có tự động xuống dòng
def render_text_line(surface, line_items, font, start_y, max_width, indent=False):
    x = 10 + (INDENT_WIDTH if indent else 0)
    y = start_y
    max_height = 0

    for item in line_items:
        if item[0] == 'text':
            text = item[1]
            words = text.split(' ')
            for word in words:
                rendered = font.render(word + ' ', True, BLACK)
                if x + rendered.get_width() > max_width:
                    x = 10
                    y += max_height + 5
                    max_height = 0
                surface.blit(rendered, (x, y))
                x += rendered.get_width()
                max_height = max(max_height, rendered.get_height())

        elif item[0] == 'image':
            try:
                image = scale_image(item[1], FONT_SIZE + 10)
                if x + image.get_width() > max_width:
                    x = 10
                    y += max_height + 5
                    max_height = 0
                surface.blit(image, (x, y))
                x += image.get_width() + 5
                max_height = max(max_height, image.get_height())
            except:
                pass

    return y + max_height + 10


def huongdan():
    global game_state, running, scroll_y, button_rect1
    screen.fill(LIGHT_ORANGE)

    # Vùng hiển thị nội dung
    visible_area = pygame.Rect(20, 20, WIDTH - 40, HEIGHT - 100)
    clip_rect = pygame.Rect(visible_area.x, visible_area.y, visible_area.width, visible_area.height)
    screen.set_clip(clip_rect)
    screen.blit(content_surface, (visible_area.x, visible_area.y - scroll_y))
    screen.set_clip(None)

    # Nút trở về
    button_text1 = button_font.render("Trở về", True, BUTTON_TEXT_COLOR)
    button_rect1 = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

    # Vẽ nút
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if button_rect1.collidepoint(mouse_pos) else BUTTON_COLOR, button_rect1)
    text_rect = button_text1.get_rect(center=button_rect1.center)
    screen.blit(button_text1, text_rect)

    #pygame.display.flip()

    # Sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect1.collidepoint(event.pos):
                game_state = "begin"
            elif event.button == 4:
                scroll_y = max(scroll_y - scroll_speed, 0)
            elif event.button == 5:
                scroll_y = min(scroll_y + scroll_speed, max_scroll)

# --- Hàm xử lý nút ---
def menu_action():
    global game_state
    game_state = "begin"

def tiep_tuc_action():
    global game_state
    game_state = "LEVEL"


def draw_button1(rect, text, action):
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

def draw_score_box(x, y, score, label_text):
    width, height = 100, 80
    pygame.draw.rect(screen, colors["WHITE"], (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, colors["BLACK"], (x, y, width, height), 2, border_radius=10)

    # Vẽ nhãn (label_text) phía trên ô điểm
    label = font.render(label_text, True, colors["BLACK"])
    screen.blit(label, label.get_rect(center=(x + width // 2, y - 20)))

    # Vẽ điểm số bên trong ô
    score_text = big_font.render(str(score), True, colors["BLACK"])
    screen.blit(score_text, score_text.get_rect(center=(x + width // 2, y + height // 2)))

def ketthuc():
    global game_state, running, effect_end
    screen.fill(colors["BG_COLOR"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ khung
    box = pygame.Rect(20,0 , 500, 350)
    box.center = (WIDTH/2,HEIGHT/2)
    pygame.draw.rect(screen, colors["WHITE"], box, border_radius=12)
    pygame.draw.rect(screen, colors["BLACK"], box, 2, border_radius=12)

    # --- Dữ liệu kết quả ---
    diem_nguoi_choi = players[0]
    diem_doi_thu = players[1]

    if (diem_doi_thu < diem_nguoi_choi):
        nguoi_thang = "nguoi"  # hoặc "nguoi" để kiểm tra thắng thua
    elif diem_doi_thu > diem_nguoi_choi:
        nguoi_thang = "may"
    elif diem_doi_thu == diem_nguoi_choi:
        nguoi_thang = "hoa"

    if nguoi_thang == "nguoi":
        ket_qua = "Bạn thắng"
        if(effect_end == False):
            win_sound.play()
            effect_end = True
    elif nguoi_thang == "may":
        ket_qua = "Máy thắng"
        if (effect_end == False):
            lose_sound.play()
            effect_end = True
    elif nguoi_thang == "hoa":
        ket_qua = "Hòa"
        if (effect_end == False):
            lose_sound.play()
            effect_end = True

    # Tiêu đề
    title_text = big_font.render(ket_qua, True, colors["BLACK"])
    screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, box.y + 40)))

    # Vẽ 2 ô điểm: máy - bạn
    total_width = 250
    score_x = box.x + (box.width - total_width) // 2
    y_score = box.y + 140

    draw_score_box(score_x, y_score, diem_doi_thu, "MÁY")
    pygame.draw.line(screen, colors["BLACK"], (score_x + 120, y_score + 10),
                     (score_x + 120, y_score + 70), 3)
    draw_score_box(score_x + 150, y_score, diem_nguoi_choi, "BẠN")

    # Vẽ nút
    draw_button1(pygame.Rect(box.x + 50, box.bottom - 80, 150, 50), "TRANG CHỦ", menu_action)
    draw_button1(pygame.Rect(box.right - 200, box.bottom - 80, 150, 50), "TIẾP TỤC", tiep_tuc_action)


def ai_choose_move():
    if AI_LEVEL == "easy":
        # Chọn nước đi có điểm thấp nhất (tệ nhất)
        worst_score = math.inf
        for i in range(1, 6):
            if board[i].numDan == 0:
                continue
            for direction in [-1, 1]:
                board_copy = copy.deepcopy(boxs)
                score = tinh_toan(i, direction, board_copy)
                if score < worst_score:
                    worst_score = score
                    worst_move = (i, direction)
        return worst_move
        # Chọn ngẫu nhiên
        # valid_moves = []
        # for i in range(1, 6):
        #     if board[i].numDan > 0:
        #         for direction in [-1, 1]:
        #             valid_moves.append((i, direction))
        # if valid_moves:
        #     return random.choice(valid_moves)
        # else:
        #     return None
    # if AI_LEVEL == "easy":
    #     # Chọn nước đi ăn ít nhất nhưng phải > 0 (bắt buộc ăn)
    #     min_positive_score = math.inf
    #     best_move = None
    #
    #     for i in range(1, 6):
    #         if board[i].numDan == 0:
    #             continue
    #         for direction in [-1, 1]:
    #             board_copy = copy.deepcopy(boxs)
    #             score = tinh_toan(i, direction, board_copy)
    #
    #             if score > 0 and score < min_positive_score:
    #                 min_positive_score = score
    #                 best_move = (i, direction)
    #
    #     if best_move:
    #         print(
    #             f"[EASY AI] Chọn nước ăn ít nhất > 0: ô {best_move[0]}, hướng {best_move[1]}, ăn {min_positive_score} điểm")
    #         return best_move
    #     else:
    #         # Trường hợp không có nước nào ăn được (>0), thì chọn đại nước hợp lệ
    #         for i in range(1, 6):
    #             if board[i].numDan == 0:
    #                 continue
    #             for direction in [-1, 1]:
    #                 print(f"[EASY AI] Không có nước ăn > 0 → chọn đại: ô {i}, hướng {direction}")
    #                 return (i, direction)


    elif AI_LEVEL == "medium":

        # Duyệt và chọn nước đi ăn được nhiều nhất (độ sâu = 1)
        best_score = -math.inf
        best_move = None
        for i in range(1, 6):
            if board[i].numDan == 0:
                continue
            for direction in [-1, 1]:
                board_copy = copy.deepcopy(boxs)
                score = tinh_toan(i, direction, board_copy)
                if score > best_score:
                    best_score = score
                    best_move = (i, direction)
        return best_move

    elif AI_LEVEL == "hard":
        def minimax(depth, maximizingPlayer):
            best_score = -math.inf if maximizingPlayer else math.inf
            best_move = None
            for i in range(1, 6):
                if board[i].numDan == 0:
                    continue
                for direction in [-1, 1]:
                    board_copy = copy.deepcopy(boxs)
                    score = tinh_toan(i, direction, board_copy)
                    if maximizingPlayer:
                        if score > best_score:
                            best_score = score
                            best_move = (i, direction)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (i, direction)
            return best_move

        return minimax(depth=5, maximizingPlayer=True)

def suggest_move():
    best_score = -math.inf
    best_move = None
    for i in range(7, 12):  # ô của người chơi (vị trí 7 đến 11)
        if board[i].numDan == 0:
            continue
        for direction in [-1, 1]:
            board_copy = copy.deepcopy(boxs)
            score = tinh_toan(i, direction, board_copy)
            if score > best_score:
                best_score = score
                best_move = (i, direction)
    return best_move

time_left = 15
time_left_ai = 2
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("O An Quan")
clock = pygame.time.Clock()
running = True
is_pause = True
is_moving = False
game_state = "begin"
# game : BEGIN, PLAYING, END
# thông tin di chuyển đá
move_info  = {"hientai" : -1,"num" : 0}

# begin screen
# Load hình nut am thanh
anh_amt_bat = pygame.image.load(r"asset\loud-sound.png")
anh_amt_bat = pygame.transform.scale(anh_amt_bat, (35, 35))
anh_amt_tat = pygame.image.load(r"asset\enable-sound.png")
anh_amt_tat = pygame.transform.scale(anh_amt_tat, (35, 35))
current_anh_amt = anh_amt_bat

#huong dan
# Màu sắc

LIGHT_ORANGE = (255, 223, 186)
BUTTON_COLOR = (135, 206, 250)
BUTTON_HOVER_COLOR = (100, 149, 237)
BUTTON_TEXT_COLOR = BLACK

# Font
font_path = "fonts/Montserrat-Italic.ttf"
FONT_SIZE = 16
font = pygame.font.Font(font_path, FONT_SIZE)
button_font = pygame.font.Font(font_path, 18)

INDENT_WIDTH = 30

# Đọc file Word
docx_content = extract_docx_content("huongdan.docx")

# Chuẩn bị nội dung
content_lines = []
for line in docx_content:
    if line[0] == 'line':
        line_items = line[1]
        has_indent = True if len(line) > 2 and line[2] else False
        content_lines.append((line_items, has_indent))

# Tính chiều cao cần thiết
content_surface_height = 0
for line_items, has_indent in content_lines:
    temp_surface = pygame.Surface((WIDTH - 40, 1000), pygame.SRCALPHA)
    next_y = render_text_line(temp_surface, line_items, font, 0, WIDTH - 60, has_indent)
    content_surface_height += next_y

# Tạo bề mặt hiển thị nội dung
content_surface = pygame.Surface((WIDTH - 40, content_surface_height), pygame.SRCALPHA)
content_surface.fill((255, 255, 255, 230))

# Vẽ nội dung lên surface
y = 0
for line_items, has_indent in content_lines:
    y = render_text_line(content_surface, line_items, font, y, WIDTH - 60, has_indent)


# Cuộn
scroll_y = 0
scroll_speed = 20
max_scroll = max(0, content_surface_height - (HEIGHT - 100))


#end
win_sound = pygame.mixer.Sound("AmThanh\\win.wav")
lose_sound = pygame.mixer.Sound("AmThanh\\lose.wav")

font = pygame.font.Font(font_path, 20)
big_font = pygame.font.Font(font_path, 36)

# --- Màu sắc ---
colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "LIGHT_BLUE": (200, 255, 255),
    "HOVER_BLUE": (150, 220, 255),
    "BG_COLOR": (255, 239, 196)
}
effect_end = False


#playing
# Button# button
menu_button_rect = pygame.Rect(WIDTH-100, HEIGHT-50, 100, 50)
menu_button_rect.right = WIDTH
suggest_count = 0
suggest_limit = 3
# Khai báo ban đầu
end_game_time = None  # thêm ở đầu game loop


suggest_button_rect = pygame.Rect(20, HEIGHT - 60, 100, 40)


# o diem
odiem = []
player = o_diem((WIDTH/4)*2.5,HEIGHT-84)
ai = o_diem(WIDTH/4,0)
odiem.append(player)
odiem.append(ai)


bg_img = pygame.image.load('asset\\ground_brown.jpg').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bg_img_rect = bg_img.get_rect()
bg_img_rect.topleft = (0,0)

board = []
boxs = []
"khai báo thêm mảng box, mỗi khi trừ hay ăn dân thì tính luôn vào boxs, không có hiệu ứng"
for i in range(0,12,1):
    x = ovuong(xS,yS,i)
    board.append(x)
    b  = box(i)
    boxs.append(b)

interval = 1000  # 1000 ms = 1 giây
last_time = pygame.time.get_ticks()
last_time_ai = pygame.time.get_ticks()
is_waiting_for_effect = False
effect_start_time = 0


while running:

    for event in pygame.event.get():
        if current_anh_at == anh_at_tat: pygame.mixer.music.pause()
        else: pygame.mixer.music.unpause()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "INSTRUCTION" and button_rect1.collidepoint(event.pos):
                game_state = "begin"
            if anh_at_rect.collidepoint(event.pos):
                # Đổi ảnh khi nhấn
                current_anh_at = anh_at_tat if current_anh_at == anh_at_bat else anh_at_bat
            if game_state == "PLAYING":
                if CHOOSING:
                    click(event.pos)
                    if suggest_button_rect.collidepoint(event.pos):
                        if current_player == 0 and CHOOSING and suggest_count < suggest_limit:
                            move = suggest_move()
                            if move:
                                choosed, huong = move
                                print(
                                    f"Gợi ý: chọn ô {choosed}, hướng {'trái' if huong == -1 else 'phải'} (có thể ăn nhiều nhất)")
                                suggest_count += 1
                                update()
                                pygame.display.flip()
                                is_waiting_for_effect = True
                                effect_start_time = pygame.time.get_ticks()

                if menu_button_rect.collidepoint(event.pos):
                    pauseGame()  # Chuyển sang chế độ pause
        if event.type == pygame.KEYDOWN:
            if game_state == "PLAYING" and CHOOSING==True :
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if choosed != -1:
                        # Xử lý di chuyển sang trái
                        # huong = -1
                        # update()  # Vẽ hướng
                        # pygame.display.flip()
                        # is_waiting_for_effect = True
                        # effect_start_time = pygame.time.get_ticks()

                        # set_dichuyen()
                        pass
                if event.key == pygame.K_RIGHT:
                    # Xử lý di chuyển sang phải
                    if choosed != -1:
                        # huong = 1
                        # update()  # Vẽ hướng
                        # pygame.display.flip()
                        # is_waiting_for_effect = True
                        # effect_start_time = pygame.time.get_ticks()
                        # set_dichuyen()
                        pass

                "mấy đoạn trên k cần nưax mà cứ để "
                if event.type == pygame.K_RETURN:
                    pass

    if game_state == "begin":
        begin()

        print("begin")

    elif game_state == "LEVEL":
        reset()
        capdo()
        print("capdo")
    elif game_state == "INSTRUCTION":
        huongdan()
        print("huongdan")
    elif game_state == "PLAYING":
        update()

        current_time = pygame.time.get_ticks()
        if current_player == 0 and CHOOSING:
            if current_time - last_time >= interval:
                time_left -= 1
                last_time = current_time

            if time_left <= 0:
                is_waiting_for_effect = True
                effect_start_time = pygame.time.get_ticks()
                random_choosed()
                time_left = 15
            keys = pygame.key.get_pressed()
            if choosed != -1 and huong == 0:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    huong = -1
                    print(huong)
                    update()  # Vẽ hướng
                    pygame.display.flip()
                    is_waiting_for_effect = True
                    effect_start_time = pygame.time.get_ticks()
                    # set_dichuyen()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    huong = 1
                    update()  # Vẽ hướng
                    pygame.display.flip()
                    is_waiting_for_effect = True
                    effect_start_time = pygame.time.get_ticks()
                     # set_dichuyen()
                pass
        elif current_player == 1 and CHOOSING:
            if current_time - last_time_ai >= interval:
                time_left_ai -= 1
                last_time_ai = current_time
            if time_left_ai <= 0:
                move = ai_choose_move()
                if move:
                    choosed, huong = move
                    print(f"AI chọn ô {choosed}, hướng {huong}")
                    update()
                    pygame.display.flip()
                    is_waiting_for_effect = True
                    effect_start_time = pygame.time.get_ticks()
                time_left_ai = 2

            """ đoạn này là nhấn chuột cho bên ai"""
            keys = pygame.key.get_pressed()
            if choosed != -1 and huong == 0:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    huong = 1
                    print(huong)
                    update()  # Vẽ hướng
                    pygame.display.flip()
                    is_waiting_for_effect = True
                    effect_start_time = pygame.time.get_ticks()
                    # set_dichuyen()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    huong = -1
                    update()  # Vẽ hướng
                    pygame.display.flip()
                    is_waiting_for_effect = True
                    effect_start_time = pygame.time.get_ticks()
                    # set_dichuyen()
        if is_waiting_for_effect:
            now = pygame.time.get_ticks()
            if now - effect_start_time >= 400:
                is_waiting_for_effect = False
                set_dichuyen()
        if ket_thuc():
            if end_game_time is None:
                print("Trò chơi kết thúc - đang ăn nốt quân")
                pygame.mixer.music.stop()
                end_game_time = pygame.time.get_ticks()
            else:
                # Đợi hiệu ứng nếu đang hiển thị hướng đi
                if is_waiting_for_effect:
                    now = pygame.time.get_ticks()
                    if now - effect_start_time >= 400:
                        is_waiting_for_effect = False
                        set_dichuyen()

                # Gọi dichuyen() để ăn nốt
                #dichuyen()

                # Chỉ khi không còn đang đi nữa mới END
                if not is_moving:
                    if pygame.time.get_ticks() - end_game_time >= 3000:
                        game_state = "END"

        # chon_o()
        dichuyen()
        # update()

    elif game_state == "END":
        ketthuc()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

