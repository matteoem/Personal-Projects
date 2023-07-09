import pygame
from player_class import Player,obstacle

# obstacleImg = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/brickwall.png')
# goalImg = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/coin32.png')
# playerImg = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/player32_right.png')
player_missing=True
goal_missing = True
player_goal_switch=False
# player=None
# goal=None

obst_pos_occupied = []
goal_pos=player_pos=(-1,-1)

def move_handling(event,step_size):
    movement_step=step_size
    movement_happened=False
    x=y=0
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            x -= movement_step
            movement_happened = True

        if event.key == pygame.K_RIGHT:
            x += movement_step
            movement_happened = True

        if event.key == pygame.K_DOWN:
            y += movement_step
            movement_happened = True            

        if event.key == pygame.K_UP:
            y -= movement_step
            movement_happened = True            

    return movement_happened, x, y


def rendering(window,bg,player=None,obstacle_list=[],goal=None):
    window.blit(bg,(0,0))
    if(player!=None): player.blitPlayer(window)
    if(len(obstacle_list)!=0):    
        for obst in obstacle_list:
            obst.blitObstacle(window)
    if(goal!=None): goal.blitObstacle(window)
    pygame.display.update()


def map_parser(map,cell_dim):
    player_thickness = obstacle_thickness = goal_thickness = cell_dim
    x=y=0
    list_of_obst = []
    num_vertical_cells=num_horizontal_cells=horizontal_counter=0
    #x e y indicano la prima posizione da cui inizio a parsare la mappa
    # Parse the map: W = wall, G = goal, P = player
    for row in map:
        num_vertical_cells+=1
        for col in row:
            horizontal_counter+=1
            if col == "W":
                list_of_obst.append(obstacle(obstacleImg,obstacle_thickness,x,y))
            if col == "G":
                goal = obstacle(goalImg,goal_thickness,x,y)
            if col =="P":
                player=Player(playerImg,player_thickness,x,y)
            x += obstacle_thickness
        y += obstacle_thickness
        x = 0
    num_horizontal_cells=int(horizontal_counter/num_vertical_cells)
    window_dim = (int(num_horizontal_cells*cell_dim), int(num_vertical_cells*cell_dim))
    return list_of_obst,goal,player,window_dim


class SoundHandler():
    def __init__(self, sound_name,channel_id):
        sound_path = 'C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/sounds/'+sound_name+'.mp3'
        self.channel_id = channel_id
        self.sound = pygame.mixer.Sound(sound_path)
        self.flag = False
        self.old_volume = -1
        self.mute = False

    def play(self,volume=1):
        self.volume=volume
        pygame.mixer.Channel(self.channel_id).set_volume(self.volume)
        pygame.mixer.Channel(self.channel_id).play(self.sound)
    
    def stop(self):
        pygame.mixer.Channel(self.channel_id).stop()

    def pause(self):
        pygame.mixer.Channel(self.channel_id).pause()


def load_map(id):

    if id==1: 
        map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W  P                         W",
        "W         WWWWWW             W",
        "W   WWWW          W          W",
        "W   W            WWWW        W",
        "W      WWW     WWWW          W",
        "W   W      W     W           W",
        "W   W      W         WWW    WW",
        "W      WWW    WWW       W W  W",
        "W     W   W   W W        WWWWW",
        "WWW   W   WWWWW W   WWWWWWW  W",
        "W W          WW              W",
        "W W  WWWWW    WWWWWWW  WWW   W",
        "W     W         G   WWWWWW   W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
      
    elif id==2:
        map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W  P                              W",
        "W         WWWWWW                  W",
        "W   WWWW          W               W",
        "W   W            WWWW             W",  
        "W      WWW     WWWW               W",
        "W   W      W     W                W",
        "W   W      W         WWW         WW",
        "W      WWW    WWW       W W       W",
        "W     W   W   W W             WWWWW",
        "WWW   W   WWWWW W   WWWWWWW       W",
        "W W          WW                   W",
        "W W  WWWWW    WWWWWWW  WWW        W",
        "W     W         G   WWWWWW        W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    elif id==3:
        map = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W P                            W",
        "W         WWWWWW               W",
        "W      W          W            W",
        "W    WW           WW           W",
        "W    WWW          WW           W",
        "W   W      W      WW           W",
        "W   W      W        W         WW",
        "W      WWW    WWW  WW     W W  W",
        "W     W   W   W W          WWWWW",
        "WWW   W   WWWWW W     WWWWWWW  W",
        "W W            WW              W",
        "W W  W WWWWW    WWWWWWW  WWW   W",
        "W     W           G   WWWWWW   W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

    return map


# def calculate_bounds(windowX,windowY,cell_size):
#     row = windowX/cell_size
#     col = windowY/cell_size
#     cells=[]
#     for i in range(int(row)):
#         for j in range(int(col)):
#             x_bounds = (i*cell_size, (i+1)*cell_size-1)
#             y_bounds = (j*cell_size, (j+1)*cell_size-1)
#             cells.append([x_bounds,y_bounds])
#     return cells

def calculate_bounds(windowX, windowY, cell_size):
    row = int(windowX / cell_size)
    col = int(windowY / cell_size)
    cells = []
    for i in range(row):
        for j in range(col):
            x_bounds = (i * cell_size, (i + 1) * cell_size - 1)
            y_bounds = (j * cell_size, (j + 1) * cell_size - 1)
            cells.append([x_bounds, y_bounds])
    return cells

def map_generator(bounds,mouse_coord):

    for cell in bounds:
        if ( between(mouse_coord[0],cell[0]) and between(mouse_coord[1],cell[1]) ):
            obst_to_create_pos=(cell[0][0], cell[1][0])
            break
    
    return obst_to_create_pos


def between(num,tuple_):
    min=tuple_[0]
    max=tuple_[1]
    return min <= num <= max


def Close_handler():

    render=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): #giù + esc chiude la finestra
            render = False
        return render


# def map_builder(buttons,windowX,windowY,cell_size,obstacles):#,player,goal):
#     for event in pygame.event.get():
#         if(buttons[0]):
#             mouse_pos = pygame.mouse.get_pos()
#             obst_pos = map_generator(windowX,windowY,cell_size,mouse_pos)
#             if (obst_pos in obst_pos_occupied) or (obst_pos==goal_pos) or (obst_pos==player_pos):
#                 continue
#             else:
#                 obst_pos_occupied.append(obst_pos)
#                 obstacles.append(obstacle(obstacleImg,cell_size, obst_pos[0], obst_pos[1]))

#         elif(buttons[2]):
#             if(player_missing):
#                 mouse_pos = pygame.mouse.get_pos()
#                 player_pos = map_generator(windowX,windowY,cell_size,mouse_pos)
#                 player = Player(playerImg,cell_size,player_pos[0],player_pos[1])
#                 player_hitbox = player.applyCollision()
#                 player_goal_switch=True
#                 player_missing=False

#             elif(goal_missing and not player_missing and not player_goal_switch):
#                 mouse_pos = pygame.mouse.get_pos()
#                 goal_pos = map_generator(windowX,windowY,cell_size,mouse_pos)
#                 goal = obstacle(goalImg,cell_size,goal_pos[0],goal_pos[1])
#                 goal_hitbox = goal.applyCollision()
#                 goal_missing = False

#         elif(event.type != pygame.KEYDOWN):
#             player_goal_switch=False

#     if(player==None and goal == None): return obstacles
#     elif(goal==None): return obstacles,player,player_hitbox
#     BOH