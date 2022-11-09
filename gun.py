import math
from random import choice
import random as rnd

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.time = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.r >= 800:
            self.vx = -self.vx
        if self.y + self.r >= 550:
            self.vy = -self.vy/1.25
            if math.fabs(self.vy) < 5:
                self.vy = 0
                self.vx = 0
        if self.y > 550:
            self.y = 550
        if self.vy != 0:
            self.vy -= 9.8 * self.time
        self.x += self.vx
        self.y -= self.vy
        self.time += 1/30

    def draw(self):
        if self.vy != 0:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )
        else:
            if self.time < self.live:
                pygame.draw.circle(
                    self.screen,
                    self.color,
                    (self.x, self.y),
                    self.r
                )
            self.time += 3

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2) <= (self.r + obj.r)**2:
            return True
        else:
            return False

class Rocket:
    def __init__(self, screen: pygame.Surface, x = 40, y = 450):
        self.screen = screen
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.r = 5
        self.color = GREEN
        self.live = 1
        self.time = 0

    def draw(self):
        if self.live == 1:
         pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        else:
            pass

    def move(self):
        if (self.x + self.r) >= 800 or (self.y + self.r) >= 600:
            self.live = 0
        self.vy -= 9.8 * self.time
        self.x += self.vx
        self.y -= self.vy
        self.time += 1/30

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

class Gun:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.bullet = 0

    def fire2_start(self):
        if event.button == 1:
           self.f2_on = 1
        if event.button == 3:
            self.bullet += 5
            new_rocket = Rocket(self.screen)
            self.an = math.atan2((event.pos[1] - new_rocket.y), (event.pos[0] - new_rocket.x))
            new_rocket.vx = 50 * math.cos(self.an)
            new_rocket.vy = -50 * math.sin(self.an)
            rockets.append(new_rocket)
            self.f2_on = 0

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if event.button == 1:
          self.bullet += 1
          new_ball = Ball(self.screen)
          new_ball.r += 5
          self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
          new_ball.vx = self.f2_power * math.cos(self.an)
          new_ball.vy = - self.f2_power * math.sin(self.an)
          balls.append(new_ball)
          self.f2_on = 0
          self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2(event.pos[1]-450, event.pos[0]-20)
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = GREY

    def draw(self):
        if self.f2_on == 0:
            pygame.draw.line(self.screen, self.color, (20, 450), (20 + 35 * math.cos(self.an), 450 + 35 * math.sin(self.an)), 7)
        else:
            pygame.draw.line(self.screen, self.color, (20, 450), (20 + (35 + self.f2_power) * math.cos(self.an), 450 + (35 + self.f2_power) * math.sin(self.an)), 7)
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface):
        """ Инициализация новой цели. """
        self.screen = screen
        self.x = rnd.randint(600, 780)
        self.y = rnd.randint(250, 450)
        self.r = rnd.randint(20, 50)
        self.v = rnd.randint(-15, 15)
        self.points = 0
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        ''' Двигает цели по вертикали со случайной скоростью '''
        if self.v == 0:
            while self.v == 0:
                self.v = rnd.randint(-15, 15)
        if (self.y + self.r) >= 500 or (self.y - self.r) <= 0:
            self.v = -self.v
        self.y += self.v


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
rockets = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
while len(targets) < 2:
    target = Target(screen)
    targets.append(target)

finished = False

while not finished:
    screen.fill(WHITE)
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    for r in rockets:
        r.draw()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    gun.draw()

    for r in rockets:
        r.move()
        for i in range(2):
            if r.hittest(targets[i]):
                targets[i].hit()
                targets.remove(targets[i])
                targets.append(Target(screen))

    for b in balls:
        b.move()
        for i in range(2):
            if b.hittest(targets[i]):
                targets[i].hit()
                targets.remove(targets[i])
                targets.append(Target(screen))

    for t in targets:
        t.move()
    gun.power_up()
    pygame.display.update()

pygame.quit()
