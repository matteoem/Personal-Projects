import pygame
from utils import *
from player_class import Player, obstacle
import os 

pygame.init()
project_folder = os.path.dirname(os.path.abspath(__file__))  # Percorso della cartella del progetto

class init_variables():
    def __init__(self):
        self.obstacles=[]   
        self.obst_pos_occupied = []
        self.player_missing=True
        self.goal_missing = True
        self.player_goal_switch=False
        self.player=None
        self.goal=None
        self.goal_pos=(-1,-1)
        self.player_pos=(-1,-1)
        self.can_move=True
        self.collision = False
        self.pressed = True
        self.you_win = False
        self.bounds = []


cell_dimension = 32   
step_size = cell_dimension  #we move 1 cell at the time
over_font = pygame.font.Font('freesansbold.ttf', 64)
bg_path = os.path.join(project_folder, 'pics', 'background.png')
obstacleImg_path = os.path.join(project_folder, 'pics', 'brickwall.png')
goalImg_path = os.path.join(project_folder, 'pics', 'coin32.png')
playerImg_right_path = os.path.join(project_folder, 'pics', 'player32_right.png')
playerImg_left_path = os.path.join(project_folder, 'pics', 'player32_left.png')

bg = pygame.image.load(bg_path)
obstacleImg = pygame.image.load(obstacleImg_path)
goalImg = pygame.image.load(goalImg_path)
playerImg_right = pygame.image.load(playerImg_right_path)
playerImg_left = pygame.image.load(playerImg_left_path)


# bg = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/background.png')
# obstacleImg = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/brickwall.png')
# goalImg = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/coin32.png')
# playerImg_right = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/player32_right.png')
# playerImg_left = pygame.image.load('C:/Users/rikuh/Desktop/personal projects/supermario_labirynth/pics/player32_left.png')




custom_map_maker = True

init = init_variables()

if not custom_map_maker: 
    map = load_map(1)
    init.obstacles, init.goal, init.player, window_dim = map_parser(map,cell_dimension)
    windowX=window_dim[0]       
    windowY=window_dim[1]
    window = pygame.display.set_mode((windowX,windowY))      #pronto ad usare la GPU
    bg = pygame.transform.scale(bg, (windowX, windowY))
    player_hitbox=init.player.applyCollision()
    goal_hitbox = init.goal.applyCollision()
    render_1 = False
    render_2 = True
else:
    render_1= True
    render_2=False
    render = True
    windowX=960 
    windowY=480
    cell_size = 32
    window = pygame.display.set_mode((windowX,windowY))      #pronto ad usare la GPU
    bg = pygame.transform.scale(bg, (windowX, windowY))

init.bounds=calculate_bounds(windowX,windowY,cell_size)

########################################TODO########################################################
"""capire come scrivere questo ciclo di for per riempire beforehand la lista obstacles 
con gli ostacoli così da inizializzare a prescindere la mappa con il contorno fatto da ostacoli"""

# for bound in init.bounds:
#     for cell in bound:
#         print(cell)
#         init.obstacles.append(obstacle(obstacleImg,cell_size, cell[0], cell[1]))

########################################TODO########################################################


print(init.bounds)
where_we_moving = None

bg_music = '8bit_mario_theme'
bump_sound ='8bit_mario_bump' 
win_sound = "8bit_mario_win"

bg_music_handler = SoundHandler(bg_music,channel_id=0)
bump_sound_handler = SoundHandler(bump_sound,channel_id=1)
win_sound_handler = SoundHandler(win_sound,channel_id=2)
bg_music_handler.play(volume=0.15)

running = True

while running:

    while render_1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): #giù + esc chiude la finestra
                render_1=False
                running = False
            if event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                render_1=False
                render_2 = True
                
            if event.type==pygame.KEYDOWN and event.key == pygame.K_m:
                if(bg_music_handler.mute):
                    bg_music_handler.play(bg_music_handler.volume)
                    bg_music_handler.mute=False
                else:
                    bg_music_handler.pause()
                    bg_music_handler.mute = True

        buttons = pygame.mouse.get_pressed()
        
        if(buttons[0]): #clicca con il tasto destro del mouse per posizionare gli ostacoli sulla mappa. Un ostacolo non può essere sovrapposto ad uno già a schermo
            mouse_pos = pygame.mouse.get_pos()
            obst_pos = map_generator(init.bounds,mouse_pos)
            if (obst_pos in init.obst_pos_occupied) or (obst_pos==init.goal_pos) or (obst_pos==init.player_pos):
                continue
            else:
                init.obst_pos_occupied.append(obst_pos)
                init.obstacles.append(obstacle(obstacleImg,cell_size, obst_pos[0], obst_pos[1]))

        elif(buttons[2]): #se clicchi con il tasto sinistro la prima volta,scegli la posizione del player. Se clicchi di nuovo dopo aver posizionato il player, posizionerai il coin
            if(init.player_missing):
                mouse_pos = pygame.mouse.get_pos()
                init.player_pos = map_generator(init.bounds,mouse_pos)
                init.player = Player(playerImg_left,playerImg_right,cell_size,init.player_pos[0],init.player_pos[1])
                player_hitbox=init.player.applyCollision()
                init.player_goal_switch=True
                init.player_missing=False


            elif(init.goal_missing and not init.player_missing and not init.player_goal_switch):
                mouse_pos = pygame.mouse.get_pos()
                init.goal_pos = map_generator(init.bounds,mouse_pos)
                init.goal = obstacle(goalImg,cell_size,init.goal_pos[0],init.goal_pos[1])
                goal_hitbox = init.goal.applyCollision()
                init.goal_missing = False

        elif(event.type != pygame.KEYDOWN):
            init.player_goal_switch=False

        rendering(window,bg,init.player,init.obstacles,init.goal)


        #if I won, I'll stop rendering since I can make the win condition with a single frame


    while render_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): #giù + esc chiude la finestra
                render_2=False
                running = False
            if event.type==pygame.KEYDOWN and event.key == pygame.K_m:
                if(bg_music_handler.mute):
                    bg_music_handler.play(bg_music_handler.volume)
                    bg_music_handler.mute=False
                else:
                    bg_music_handler.pause()
                    bg_music_handler.mute = True

        if not init.you_win:
            init.player.old_x=init.player.x
            init.player.old_y=init.player.y
            move_happened,move_x,move_y = move_handling(event,step_size)
            if move_x<0: 
                where_we_moving="left"
            elif move_x>0:
                where_we_moving="right"

            
            if move_happened:
                if init.can_move:
                    init.player.x+=move_x
                    init.player.y+=move_y
                    if(init.player.x<=0 or init.player.x>=windowX-init.player.thickness): init.player.x=init.player.old_x
                    if(init.player.y<=0 or init.player.y>=windowY-init.player.thickness): init.player.y=init.player.old_y
                    init.player.updatePlayer(init.player.x, init.player.y,where_we_moving)
                    player_hitbox=init.player.applyCollision()
                    init.can_move=False
            else:
                init.can_move=True


            for obst in init.obstacles:
                if(obst.applyCollision().colliderect(player_hitbox)):
                    init.collision=True
                    break
                else: init.collision=False
            
            if init.collision:
                init.player.x=init.player.old_x
                init.player.y=init.player.old_y
                init.player.updatePlayer(init.player.old_x,init.player.old_y,where_we_moving)
                player_hitbox=init.player.applyCollision()
                bump_sound_handler.play()

            if (init.goal.applyCollision().colliderect(player_hitbox)):
                init.you_win = True
                render_2=False
                render_3=True
            
            rendering(window,bg,init.player,init.obstacles,init.goal)

        #if I won, I'll stop rendering since I can make the win condition with a single frame

    while render_3:
        if not win_sound_handler.flag: 
            bg_music_handler.flag = False
            bg_music_handler.stop()
            win_sound_handler.play(volume=0.35)
            win_sound_handler.flag = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): #esc chiude la finestra
                    render_3=False
                    running = False
                if event.type==pygame.KEYDOWN and event.key == pygame.K_r:
                    if custom_map_maker:
                        init = init_variables()
                        render_3=False
                        render_1=True
                    else:
                        init.player.x=init.player.original_x
                        init.player.y=init.player.original_y
                        player_hitbox = init.player.applyCollision()
                        init.you_win = False
                        render_3=False
                        render_2 = True

                    win_sound_handler.flag=False
                    win_sound_handler.stop()
                    bg_music_handler.play(0.15)


        window.blit(bg,(0,0))
        over_text = over_font.render("YOU WIN", True, (255, 255, 255))
        window.blit(over_text, (windowX/2 - 180,windowY/2 - 50))
        over_text1 = over_font.render("(press R to restart)", True, (255, 255, 255))
        window.blit(over_text1, (windowX/6,windowY/2 + 50))
        pygame.display.update()

