import copy
from doctest import master
from hashlib import new
from tracemalloc import start

import cv2
import numpy as np

import config
from utils import data, intro, keyEvent_handler
from mouse_callback import mouse_click
from utils import *

# pyinstaller --onefile C:\Users\MATTEO\Desktop\python_scripts\DnD_map_revealer\main.py %% QUESTO PER CREARE IL FILE EXE


image_path = intro()
config.image = cv2.imread(image_path)


obscuring_mask = np.zeros(config.image.shape, dtype=np.uint8)
shaded_mask = np.full(config.image.shape,fill_value=config.shaded_color, dtype=np.uint8)

config.master_data = data(config.image,shaded_mask)
config.player_data = data(config.image,obscuring_mask)

config.starting_state = (copy.deepcopy(config.master_data),copy.deepcopy(config.player_data))
config.history.append(config.starting_state)

cv2.namedWindow(winname=config.master_window)
cv2.namedWindow(winname=config.player_window)


config.white = (255, 255, 255)

#cv2.setMouseCallback(config.player_window, mouse_click)
cv2.setMouseCallback(config.master_window, mouse_click)


# Load an image
Running = True



config.master_data.imshow(config.master_window)
config.player_data.imshow(config.player_window)

while Running:
    check = cv2.waitKey(1)
    if check==27:   #se clicco esc, chiudo tutto
        break
    keyEvent_handler(check)


cv2.destroyAllWindows()
