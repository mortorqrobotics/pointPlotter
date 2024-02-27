import sys, pygame
import pygame.gfxdraw
from pygame.locals import *
import numpy as np
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WINDOW_WIDTH = 827
WINDOW_HEIGHT = 411
FPS = 60

pygame.init()

pts = []
knots = []
count = 0

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

BG = pygame.image.load("background.png")
BG = pygame.transform.scale(BG, (WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def clearAndRedraw():
    DISPLAYSURF.blit(BG,(0,0))
    #Line and rects
    for i in range(count - 1):
        pygame.draw.line(DISPLAYSURF, GREEN, pts[i], pts[i+1], 3)
    for i in range(count):
        pygame.draw.rect(DISPLAYSURF, BLUE, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)


#Bezier
def bezier():
    clearAndRedraw()
    N = len(pts)
    n = N-1
    for t in np.arange(0, 1, 0.01):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        pygame.draw.circle(DISPLAYSURF, RED, z.astype(int), 3)


def drawPolylines(color='GREEN', thick=3):
    if (count < 2): return
    for i in range(count):
        pygame.draw.rect(DISPLAYSURF, BLUE, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)

done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0
old_button3 = 0

selectedPoint = -1
buttonCheck = -1
font = pygame.font.Font('freesansbold.ttf', 12)
while not done:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        #Mouse click
        pts.append(pt)
        count += 1
        pygame.draw.rect(DISPLAYSURF, BLUE, (pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), 5)
    elif old_pressed == -1 and pressed == -1 and old_button1 == 1 and button1 == 1:
        #Mouse hold
        for i in range(len(pts)):
            if((math.isclose(x, pts[i][0], rel_tol=0.05)) and (math.isclose(y, pts[i][1], rel_tol=0.05))):
                selectedPoint = i
    elif old_pressed == 0 and pressed == 0 and old_button1 == 1 and button1 == 1:
        if selectedPoint != -1:
            DISPLAYSURF.blit(BG, (0,0))
            pts[selectedPoint][0] = x
            pts[selectedPoint][1] = y
    elif old_pressed == 1 and pressed == 1 and old_button1 == 0 and button1 == 0:
        selectedPoint = -1
    elif old_pressed == -1 and pressed == 1 and old_button3 == 1 and button3 == 0:
        #Right mouse
        for i in range(len(pts)):
            if((math.isclose(x, pts[i][0], rel_tol=0.05)) and (math.isclose(y, pts[i][1], rel_tol=0.05))):
                del pts[i]
                count -= 1
                DISPLAYSURF.blit(BG,(0,0))
                break
    
    for i in range(len(pts)):
        base = 20
        points = font.render("{}, {}".format(round((pts[i][0]/50) - pts[0][0]/50, 2 ), round(round(8.27-pts[i][1]/50, 2) - round(8.27-pts[0][1]/50, 2), 2)), True, GREEN)
        DISPLAYSURF.blit(points, (700, base + i*20))

    drawPolylines(GREEN, 3)
    pygame.display.flip()
    bezier()
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed
    old_button3 = button3

pygame.quit()
