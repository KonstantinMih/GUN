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
LIGHTPINK = 0xFFB6C1
GAME_COLORS = [BLUE, YELLOW, MAGENTA, CYAN]

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


class Rocket(Ball):
    """ Второй тип снарядов """
    def __init__(self, screen: pygame.Surface, x=20, y=450):
        super().__init__(screen, x, y)
        self.color = GREEN
        self.live = 1
        self.r = 5

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


class Gun:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = 20
        self.y = 450
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
            new_rocket = Rocket(self.screen, self.x, self.y)
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
           new_ball = Ball(self.screen, self.x, self.y)
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
            self.an = math.atan2(event.pos[1]-self.y, event.pos[0]-self.x)
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = GREY

    def draw(self):
        if self.f2_on == 0:
            pygame.draw.rect(screen, YELLOW, (self.x - 10, self.y - 15, 20, 30))
            pygame.draw.rect(screen, RED, (self.x - 5, self.y - 10, 10, 20))
            pygame.draw.line(self.screen, self.color, (self.x, self.y), (self.x + 35 * math.cos(self.an), self.y + 35 * math.sin(self.an)), 7)
        else:
            pygame.draw.rect(screen, YELLOW, (self.x - 10, self.y - 15, 20, 30))
            pygame.draw.rect(screen, RED, (self.x - 5, self.y - 10, 10, 20))
            pygame.draw.line(self.screen, self.color, (self.x, self.y), (self.x + (35 + self.f2_power) * math.cos(self.an), self.y + (35 + self.f2_power) * math.sin(self.an)), 7)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY

    def move(self, keys):
        if keys[pygame.K_w]:
            if self.y >= 20:
                self.y -= 5
            else:
                pass
        if keys[pygame.K_s]:
            if self.y <= 450:
                self.y += 5
            else:
                pass


class Target:
    def __init__(self, screen: pygame.Surface):
        """ Инициализация новой цели. """
        self.screen = screen
        self.x = rnd.randint(450, 690)
        self.y = rnd.randint(250, 450)
        self.r = rnd.randint(20, 50)
        self.v = rnd.randint(-15, 15)
        self.points = 0
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        """Двигает цели по вертикали со случайной скоростью"""
        if self.v == 0:
            while self.v == 0:
                self.v = rnd.randint(-15, 15)
        if (self.y + self.r) >= 500 or (self.y - self.r) <= 0:
            self.v = -self.v
        self.y += self.v


class LissajousTarget(Target):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.color = LIGHTPINK
        self.time = 0
        self.omegaX = rnd.randrange(-15, 15)
        self.omegaY = rnd.randrange(-15, 15)
        self.Ax = rnd.randint(-100, 100)
        self.Ay = rnd.randint(-100, 100)
        self.phase = rnd.randrange(-4, 4)
        self.x_0 = self.x
        self.y_0 = self.y

    def check(self):
        """Смотрит, чтобы цели не были слишком медленными и не топтались на месте"""
        if -5 <= self.omegaX <= 5:
            while -5 <= self.omegaX <= 5:
                self.omegaX = rnd.randrange(-15, 15)
        if -5 <= self.omegaY <= 5:
            while -5 <= self.omegaY <= 5:
                self.omegaY = rnd.randrange(-15, 15)
        if -30 <= self.Ax <= 30:
            while -30 <= self.Ax <= 30:
                self.Ax = rnd.randrange(-100, 100)
        if -30 <= self.Ay <= 30:
            while -30 <= self.Ay <= 30:
                self.Ay = rnd.randrange(-100, 100)

    def move(self):
        self.check()
        self.x = self.x_0 + self.Ax * math.cos(self.omegaX * self.time + self.phase)
        self.y = self.y_0 + self.Ay * math.cos(self.omegaY * self.time)
        self.time += 1/30

    def hit(self, points=1):
        self.points += 3 * points


def targets_append(targets: list, screen: pygame.Surface):
    """ Создаёт новую цель (с вероятностью 2/5 - обычную, с 1/5 - Лиссажу)

        targets - список целей
        screen - экран"""

    if rnd.randint(-2, 1) != 0:
        target = Target(screen)
        targets.append(target)
    else:
        target = LissajousTarget(screen)
        targets.append(target)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
rockets = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
while len(targets) < 2:
    targets_append(targets, screen)

finished = False

while not finished:
    screen.fill(WHITE)
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    for r in rockets:
        r.draw()

    keys = pygame.key.get_pressed()

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

    gun.move(keys)
    gun.draw()

    for r in rockets:
        r.move()
        for i in range(2):
            if r.hittest(targets[i]):
                targets[i].hit()
                targets.remove(targets[i])
                if r in rockets:
                    rockets.remove(r)
                targets_append(targets, screen)

    for b in balls:
        b.move()
        for i in range(2):
            if b.hittest(targets[i]):
                targets[i].hit()
                targets.remove(targets[i])
                if b in balls:
                    balls.remove(b)
                targets.append(Target(screen))

    for t in targets:
        t.move()
    gun.power_up()
    pygame.display.update()

pygame.quit()
