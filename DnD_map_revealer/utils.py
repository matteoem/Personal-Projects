from pathlib import Path
from tkinter import font
import cv2
import numpy as np
import pathlib
import config
import copy
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import colorama
from termcolor import cprint 
from pyfiglet import figlet_format


def demo(screen):
    effects = [
        Cycle(
            screen,
            FigletText("Dungeon    Map   Revealer"),
            int(screen.height / 2 - 4)),
        Cycle(
            screen,
            FigletText("Revealer"),
            int(screen.height / 2 + 3)),
        Cycle(
            screen,
            FigletText("Made by Matteo Emanuele",font="small"),
            int(screen.height / 2 + 3 )),
        #Stars(screen, 200)
        
    ]
    screen.play([Scene(effects, 500)])


class data:
    def __init__(self,image,mask):
        self.mask = mask.copy()
        self.masked_image= apply_mask(image,self.mask,[(0,0),(0,1),(1,0),(1,1)])
        self.points = []
    
    def imshow(self, window):
        cv2.imshow(window,self.masked_image)

    def clear_pixels(self):
        self.points=[]
    
    def add_pixels(self,x,y):
        self.points.append((x,y))

    def apply_mask(self,image,points=None): #only for player
        if points==None:
            points = self.points
        self.masked_image=apply_mask(image,self.mask,points)

    def copy_image(self):
        self.copy = self.masked_image.copy()
    
    def restore_to_copy(self):
        self.masked_image=self.copy.copy()

    def clone(self):
        new_data=data(None,self.mask) #masked image is None in this line
        new_data.masked_image = self.masked_image.copy()


def apply_mask(image_,mask_,vertices_list):
        if type(image_)==None:
            return None

        transformed_vertices_list=np.array([vertices_list], dtype=np.int32)
        white = (255, 255, 255)
        cv2.fillPoly(mask_, transformed_vertices_list, white)

        masked_image_ = cv2.bitwise_and(image_, mask_)
        return masked_image_


def intro():

    cprint(figlet_format('Dungeon Map Revealer!', font='big'),'yellow', attrs=['bold'])
    print("Please input the name of the map WITHOUT the file extension(it must be a .png file). Note that the file must be placed in a folder structure as follow:")
    text = ["\U0001F5A5 Desktop","├── \U0001F4C2 dnd_5e","│   ├── \U0001F4C2 dnd_maps","│   │   ├──\U0001F4F7 dungeon_map.PNG",]
    for elem in text:
        print(elem)
    print()
    print(colorama.Fore.YELLOW +"If you need additional information please type 'info'.")
    print()
    print("Waiting for input... ")
    input_=input()
    while input_=="info":
        print()
        print(colorama.Fore.GREEN + "Credits to Matteo Emanuele. Special thanks to my code sensei Alessio Annunziato.")
        print()
        print(colorama.Fore.GREEN + "Thanks for using 'Dungeon Map Revealer'. This tool will help the dungeon master in online games to handle dungeon exploration. Two windows will open: the dungeon master should be able to see both of them, while the players should only see the Black Screen. As the Dungeon Master, draw on the colored map to reveal portions of map on the blacked window as the dungeon exploration progess.")
        print()
        print(colorama.Fore.GREEN + "Here's the commands:")
        print(colorama.Fore.GREEN + "- LMB_____ hold-click with the left mouse button to draw general lines. Close the drawn path to reveal the highlighted region")
        print(colorama.Fore.GREEN + "- RMB_____ hold-click with the right mouse button to draw squared regions. Leave it to highlight the region")
        print(colorama.Fore.GREEN + "- CTRL+Z__ you can come back to the previous state with the CTRL+Z")
        print(colorama.Fore.GREEN + "- R_______ click the R(reset) button to restore the initial state of the map")
        print()
        print(colorama.Fore.YELLOW +"Waiting for input...")
        input_ = input()
    path_ = "C:\\Users\\MATTEO\\Desktop\\python_scripts\\DnD_map_revealer\\dnd_maps\\"+ input_
    image_path = str(path_)+'.PNG'
    return image_path


def keyEvent_handler(check):

    if check==26 and not (config.drawing_L or config.drawing_R): #ctr+z
        if len(config.history)>0:
            print("ctrl z")
            config.master_data,config.player_data = config.history.pop()
            config.player_data.imshow(config.player_window)
            config.master_data.imshow(config.master_window)

    
    elif (check==ord("r")) and not (config.drawing_L or config.drawing_R):
        config.master_data=copy.deepcopy(config.starting_state[0])
        config.player_data=copy.deepcopy(config.starting_state[1])
        config.history=[]
        config.history_jumper=1
        config.player_data.imshow(config.player_window)
        config.master_data.imshow(config.master_window)

def colored(text,r=52, g=235, b=152):
    return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"