import time

import pygame
import random

from pygame.cursors import sizer_y_strings


class box:
    def __init__(self,index):
        super().__init__()
        self.numQuan = 0
        self.isQuan = False
        self.numDan = 0
        self.index = index

        if self.index==0 or self.index==6:
            self.isQuan = True
            self.numQuan=5
        else:
            self.numDan=5


class ovuong():
    def __init__(self,x,y,index):
        super().__init__()
        self.size = 120
        self.numQuan = 0
        self.isQuan = False
        self.numDan = 0
        self.d = 0

        self.x = x + (6 - abs(6 - index)) * (self.size + self.d)
        self.y = y + (index // 6) * (self.size + self.d)
        self.index = index
        self.rect = pygame.Rect(self.x,self.y,self.size,self.size)

        self.stone_group = pygame.sprite.Group()
        self.quan_group = pygame.sprite.Group()

        if self.index==0 or self.index==6:
            self.isQuan = True
            self.numQuan=5
        else:
            self.numDan=5

        for i in range(self.numDan):
            x = self.x + random.randint(10, 40)
            y = self.y + random.randint(10, 40)
            s = stone(x, y)
            self.stone_group.add(s)

        # if self.isQuan == True:
        #     # lay toa do tam
        #     Ix = self.x + self.size / 2 - self.size/3*(index // 6)
        #     Iy = self.y + self.size / 2
        #     s = stone_quan(Ix,Iy)
        #     self.quan_group.add(s)
        if self.index == 0:
            # lay toa do tam
            Ix = self.x + self.size /2
            Iy = self.y + self.size
            s = stone_quan(Ix,Iy)
            self.quan_group.add(s)
        if self.index == 6:
            # lay toa do tam
            Ix = self.x + self.size /2
            Iy = self.y
            s = stone_quan(Ix,Iy)
            self.quan_group.add(s)



    def draw_stone(self,screen):
        self.quan_group.draw(screen)
        self.stone_group.draw(screen)

    def ve_quan(self,screen):
        pass

    def xoa_dan(self):
        self.stone_group.empty()

    # di chuyển dân về ô diểm
    def move_dan(self, odiem):
        for i in self.stone_group:
            x = odiem.rect.x + random.randint(20, 60)
            y = odiem.rect.y + random.randint(20, 60)
            i.rect.center = (x,y)
            odiem.stone_group.add(i)
            self.stone_group.remove(i)
        if self.isQuan:
            x = odiem.rect.x + random.randint(20, 60)
            y = odiem.rect.y + random.randint(20, 60)
            for m in self.quan_group:
                m.rect.center = (x,y)
                odiem.quan_group.add(m)
                self.quan_group.remove(m)
        # self.stone_group.empty()
        # self.quan_group.empty()


    def add_dan(self,stone):
        self.numDan +=1
        self.stone_group.add(stone)

    def add_stone(self):
        self.numDan += 1
        x = self.x + random.randint(10, 60)
        y = self.y + random.randint(10, 60)
        if self.isQuan ==True:
            x = self.x + random.randint(10, 55)
            y = self.y + random.randint(10, 55)
        s = stone(x, y)
        self.stone_group.add(s)


class stone(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('asset\\stone_2d.png')
        self.rect = self.image.get_rect()

        #         vi tri cua anh
        self.rect.topleft = (x, y)

    def move_ip(self,x,y):
        self.rect.move_ip(x,y)

class stone_quan(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("asset\\da_quan.png")
        self.rect = self.image.get_rect()
        #         vi tri cua anh
        self.rect.center = (x, y)

    def move_ip(self,x,y):
        self.rect.move_ip(x,y)


class o_diem:
    def __init__(self,x,y):
        self.image = pygame.image.load("asset\\o_diem.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.stone_group = pygame.sprite.Group()
        self.quan_group = pygame.sprite.Group()

    def eated_stone(self,screen):
        self.stone_group.draw(screen)
        self.quan_group.draw(screen)

class button_menu:
    def __init__(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.Text = "Menu"

