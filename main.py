'''
____________Алгоритмы для построения линий____________
1) Естественный алгоритм рисования прямой:
a = (y1-y0)/(x1-x0)
b = y0-a*x0
if (|x1-x0|<|y1-y0|)
    if (y1 < y0) for y := y1 to y0 Точка(y*a+b, y)
    else for y := y0 to y1 Точка(y*a+b, y)
else
    if (x1 < x0) for x := x1 to x0 Точка(x. x*a+b)
    else for x := x0 to x1 Точка(x, x*a+b)

2) Естественный алгоритм рисования окружности:
for x := x0+R*cos(3*pi/4) to x0+R*cos(pi/4)
    Точка(x, y0+sqrt(R*R-(x-x0)*(x-x0)))
    Точка(x, y0-sqrt(R*R-(x-x0)*(x-x0)))
for y := y0+R*sin(-pi/4) to y0+R*sin(pi/4)
    Точка(x0+sqrt(R*R-(y-y0)*(y-y0)), y)
    Точка(x0-sqrt(R*R-(y-y0)*(y-y0)), y)

3) Параметрический алгоритм для фигур Лиссажу:

____________Алгоритмы закраски____________
1) Рекурсивный алгоритм с затравкой (по паттерну)
2) Алгоритм короеда (сплошной цвет)
3) Мод. рекурсивный алгоритм с затравкой (сплошной цвет)
'''

import pygame
import math
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

W = 600
H = 500


# ---- Функции рисования линий и закраски ----
def DrawLine(x0, y0, x1, y1):
    if (abs(x1 - x0) < abs(y1 - y0)):
        a = (x1 - x0) / (y1 - y0)
        b = x0 - a * y0
        if (y1 < y0):
            for y in range(y1, y0):
                pygame.display.update()
                pygame.draw.circle(sc, (0, 0, 0), (y * a + b, y), 1)
        else:
            for y in range(y0, y1):
                pygame.display.update()
                pygame.draw.circle(sc, (0, 0, 0), (y * a + b, y), 1)

    else:
        a = (y1 - y0) / (x1 - x0)
        b = y0 - a * x0
        if (x1 < x0):
            for x in range(x1, x0):
                pygame.display.update()
                pygame.draw.circle(sc, (0, 0, 0), (x, x * a + b), 1)
        else:
            for x in range(x0, x1):
                pygame.display.update()
                pygame.draw.circle(sc, (0, 0, 0), (x, x * a + b), 1)


def DrawNRound(x0, y0, R):
    for x in range(x0 + int(R * math.cos(3 * math.pi / 4)), x0 + int(R * math.cos(math.pi / 4))):
        pygame.display.update()
        pygame.draw.circle(sc, (0, 0, 0), (x, y0 + math.sqrt(R * R - (x - x0) * (x - x0))), 1)
        pygame.draw.circle(sc, (0, 0, 0), (x, y0 - math.sqrt(R * R - (x - x0) * (x - x0))), 1)
    for y in range(y0 + int(R * math.sin(-math.pi / 4)), y0 + int(R * math.sin(math.pi / 4))):
        pygame.display.update()
        pygame.draw.circle(sc, (0, 0, 0), (x0 + math.sqrt(R * R - (y - y0) * (y - y0)), y), 1)
        pygame.draw.circle(sc, (0, 0, 0), (x0 - math.sqrt(R * R - (y - y0) * (y - y0)), y), 1)


def DrawPLissaz(x0, y0, R1, R2, o1, o2):
    t = 0
    h = 0.01
    pygame.draw.circle(sc, (0, 0, 0), (x0 + R1 * math.cos(o1 * t), y0 + R2 * math.sin(o2 * t)), 1)
    while t <= 2 * math.pi:
        pygame.display.update()
        #        pygame.draw.circle(sc, (0, 0, 0), (x0+R1*math.cos(o1*t), y0+R2*math.sin(o2*t)), 1)
        pygame.draw.line(sc, BLACK, (x0 + R1 * math.cos(o1 * (t - h)), y0 + R2 * math.sin(o2 * (t - h))),
                         (x0 + R1 * math.cos(o1 * t), y0 + R2 * math.sin(o2 * t)))
        t = t + h


def RecColor(x0, y0, r, g, b, pat):
    for (x, y) in [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]:
        if ((sc.get_at((x, y))[:3] != (0, 0, 0)) and (sc.get_at((x, y))[:3] != (r, g, b)) and (
                sc.get_at((x, y))[:3] != (b, g, r))):
            if (pat[x0 % 8][y0 % 8] == 1):
                sc.set_at(((x, y)), (r, g, b))
            else:
                sc.set_at(((x, y)), (b, g, r))
            RecColor(x, y, r, g, b, pat)


def Color1(x0, y0, r, g, b, pat):
    sys.setrecursionlimit(10 ** 6)

    if (pat[x0 % 8][y0 % 8] == 1):
        sc.set_at(((x0, y0)), (r, g, b))
    else:
        sc.set_at(((x0, y0)), (b, g, r))
    RecColor(x0, y0, r, g, b, pat)


def Color2(x0, y0, r, g, b):
    stack = []
    stack.append((x0, y0))
    while stack:
        p = stack.pop()
        if ((sc.get_at(p)[:3] != (0, 0, 0)) and (sc.get_at(p)[:3] != (r, g, b))):
            sc.set_at((p), (r, g, b))
            x0, y0 = p
            for (x, y) in [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]:
                if ((sc.get_at((x, y))[:3] != (0, 0, 0)) and (sc.get_at((x, y))[:3] != (r, g, b))):
                    stack.append((x, y))


def Color3(x0, y0, r, g, b):
    stack = []
    stack.append((x0, y0))
    while stack:
        pygame.display.update()
        p = stack.pop()
        print(p)
        if (sc.get_at(p)[:3] != (r, g, b)):
            x0, y0 = p
            xLeft = x0
            xRight = x0
            while (sc.get_at(((xLeft - 1), y0))[:3] != BLACK):
                xLeft = xLeft - 1
            while (sc.get_at(((xRight + 1), y0))[:3] != BLACK):
                xRight = xRight + 1
            pygame.draw.line(sc, (r, g, b), (xLeft, y0), (xRight, y0))

            x = xLeft
            while x <= xRight:
                if (sc.get_at((x, y0 + 1))[:3] != BLACK):
                    if (((sc.get_at((x + 1, y0 + 1))[:3] == BLACK) or (x == xRight)) and (
                            sc.get_at((x + 1, y0 + 1))[:3] != (r, g, b))):
                        stack.append((x, y0 + 1))
                x = x + 1

            x = xLeft
            while x <= xRight:
                if (sc.get_at((x, y0 - 1))[:3] != BLACK):
                    if (((sc.get_at((x + 1, y0 - 1))[:3] == BLACK) or (x == xRight)) and (
                            sc.get_at((x + 1, y0 - 1))[:3] != (r, g, b))):
                        stack.append((x, y0 - 1))
                x = x + 1


# --------------------------------------------

# --------------------  создание окна  -------------------------


pygame.init()

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Лабораторная работа N3")
sc.fill(WHITE)
FPS = 30
clock = pygame.time.Clock()
pygame.display.update()

# ---- Функции рисования линий и закраски ----

DrawLine(0, 0, 50, 50)
DrawLine(50, 50, 50, 0)
DrawLine(50, 0, 0, 0)
DrawNRound(25, 25, 15)
pattern = [[0, 1, 0, 0, 0, 1, 0, 0],
           [1, 1, 0, 0, 0, 0, 1, 0],
           [0, 0, 1, 0, 0, 0, 1, 1],
           [0, 0, 0, 1, 0, 0, 0, 1],
           [0, 0, 0, 0, 1, 0, 0, 1],
           [1, 0, 0, 0, 0, 1, 1, 0],
           [0, 1, 0, 0, 0, 1, 1, 0],
           [0, 0, 1, 1, 1, 0, 0, 1]]
Color1(40, 5, 164, 30, 25, pattern)
Color1(25, 30, 25, 30, 164, pattern)

DrawPLissaz(300, 250, 250, 200, 10, 9)

'''
DrawNRound(200, 200, 150)
DrawLine(190, 190, 210, 160)
DrawLine(190, 190, 149, 190)
DrawLine(149, 190, 159, 165)
DrawLine(210, 160, 185, 180)
DrawNRound(246, 238, 60)
DrawNRound(200, 360, 20)
DrawNRound(170, 238, 60)
Color3(180, 175, 128, 128, 16)
'''
# --------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(FPS)
# --------------------------------------------------------------
