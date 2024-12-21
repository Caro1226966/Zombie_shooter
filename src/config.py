import pygame as p
import math
import os
import tkinter
import random

# DO NOT CHANGE!!!
RES_DIR = "..\\res"
SCREEN = p.display.set_mode((0, 0))
TARGET_FPS = 300
# tkinter
root = tkinter.Tk()
root.winfo_screenwidth()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
root.destroy()
BG_IMAGE_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# You can change these
p.display.set_caption('Zombie Shooter')

PLAYER_SPEED = SCREEN_WIDTH / 3000
BULLET_LIFESPAN = 5
SHOOT_COOLDOWN = 0.5


