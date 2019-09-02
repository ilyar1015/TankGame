import sys
import time
from random import randint

import pygame as pg
import pygame.locals as pl


class TankMain(object):
    width = 600
    height = 500
    my_tank_missile = []
    enemy_list = []
    my_tank = None

    def __init__(self):
        pg.init()

    def start_game(self):

        # 创建一个屏幕，屏幕的大小（宽，高）
        # 窗口的属性0不可变,32表示颜色的位数
        screem = pg.display.set_mode((TankMain.width, TankMain.height), 0, 32)
        pg.display.set_caption("坦克大战")
        TankMain.my_tank = My_tank(screem)

        for _ in range(5):
            TankMain.enemy_list.append(Enemy_tank(screem))
        while True:
            screem.fill((0, 0, 0))
            # 显示左上角的文字
            for i, text in enumerate(self.write_text(), 0):
                screem.blit(text, (0, 5 + (20 * i)))

            self.get_event(TankMain.my_tank)

            TankMain.my_tank.display()
            TankMain.my_tank.move()

            for enemy in TankMain.enemy_list:
                enemy.display()
                enemy.random_move()
            # 显示所有炮弹
            for m in TankMain.my_tank_missile:
                if m.live:
                    m.display()
                    m.move()
                else:
                    TankMain.my_tank_missile.remove(m)
            # 睡眠时间（秒）
            time.sleep(0.05)
            pg.display.update()

    def get_event(self, my_tank):
        for event in pg.event.get():
            if event.type == pl.QUIT:
                self.stop_game()
            if event.type == pl.KEYDOWN:

                if event.key == pl.K_LEFT or event.key == pl.K_a:
                    my_tank.direction = "L"
                    my_tank.stop = False
                if event.key == pl.K_RIGHT or event.key == pl.K_d:
                    my_tank.direction = "R"
                    my_tank.stop = False
                if event.key == pl.K_UP or event.key == pl.K_w:
                    my_tank.direction = "U"
                    my_tank.stop = False
                if event.key == pl.K_DOWN or event.key == pl.K_s:
                    my_tank.direction = "D"
                    my_tank.stop = False
                if event.key == pl.K_ESCAPE:
                    self.stop_game()
                if event.key == pl.K_SPACE:
                    TankMain.my_tank_missile.append(my_tank.fire())
            if event.type == pl.KEYUP:
                if event.key == pl.K_LEFT or event.key == pl.K_a or event.key == pl.K_RIGHT \
                        or event.key == pl.K_d or event.key == pl.K_UP or event.key == pl.K_w \
                        or event.key == pl.K_DOWN or event.key == pl.K_s:
                    my_tank.stop = True

    def stop_game(self):
        sys.exit()

    def write_text(self):
        # pygame.font.get_fonts() 可以例句出所有字体
        font = pg.font.SysFont("隶书", 20)
        text1 = font.render("敌方坦克的数量：%d" % len(TankMain.enemy_list), True, (255, 0, 0))
        text2 = font.render("我方子弹的数量：%d" % len(TankMain.my_tank_missile), True, (255, 20, 0))
        return text1, text2


# 坦克大战游戏中所有对象的父类
class BaseItem(pg.sprite.Sprite):
    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        # 所有对象共享的属性
        self.screen = screen

    # 把坦克对应的图片显示在游戏窗口上
    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screen.blit(self.image, self.rect)


class Tank(BaseItem):
    # 定义类属性，所有坦克的宽高都是一样的
    width = 50
    height = 50

    def __init__(self, screen, left, top):
        super().__init__(screen)
        # 坦克默认方向向下（上下左右）
        self.direction = "U"
        # 坦克的运行状态
        self.stop = False
        # 坦克移动的速度
        self.speed = 5
        # 坦克的所有图片
        self.images = {
            "L": pg.image.load("images/tankL.gif"),
            "R": pg.image.load("images/tankR.gif"),
            "U": pg.image.load("images/tankU.gif"),
            "D": pg.image.load("images/tankD.gif")
        }
        # 坦克的图片由方向决定
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True

    def move(self):
        if not self.stop:
            if self.direction == "L":
                # p判断坦克是否在屏幕左边的边界上
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankMain.width
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0
            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom = TankMain.height

    def fire(self):
        m = Missile(self.screen, self)
        return m


class My_tank(Tank):
    def __init__(self, screen):
        super().__init__(screen, 275, 400)
        self.stop = True


class Enemy_tank(Tank):

    def __init__(self, screen):
        super().__init__(screen, randint(1, 5) * 100, 200)
        self.speed = 4
        # 坦克按照某个方向连续移动的步数
        self.step = randint(6, 20)
        self.get_random_direction()

    def get_random_direction(self):
        r = randint(0, 4)
        if r == 4:
            self.stop = True
        elif r == 1:
            self.direction = "L"
            self.stop = False
        elif r == 2:
            self.direction = "R"
            self.stop = False
        elif r == 3:
            self.direction = "U"
            self.stop = False
        elif r == 0:
            self.direction = "D"
            self.stop = False

    # 敌方坦克，按照随机的方向，连续移动6部，然后才能再次改变方向
    def random_move(self):
        if self.live:
            if self.step == 0:
                self.get_random_direction()
                self.step = randint(6, 12)
            else:
                self.move()
                self.step -= 1


class Missile(BaseItem):
    width = 12
    height = 12

    def __init__(self, screen, tank):
        super().__init__(screen)
        self.tank = tank
        # 炮弹的方向由所发射的坦克方向决定的
        self.direction = tank.direction
        # 炮弹移动的速度
        self.speed = 12
        # 坦克的所有图片
        self.images = {
            "L": pg.image.load("images/MissileL.gif"),
            "R": pg.image.load("images/MissileR.gif"),
            "U": pg.image.load("images/MissileD.gif"),
            "D": pg.image.load("images/MissileU.gif")
        }
        # 坦克的图片由方向决定
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left + (tank.width - self.width) / 2
        self.rect.top = tank.rect.top + (tank.height - self.height) / 2
        self.live = True

    def move(self):
        if self.live:
            if self.direction == "L":
                # p判断坦克是否在屏幕左边的边界上
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.live = False
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.live = False
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False
            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.live = False


game = TankMain()
game.start_game()
