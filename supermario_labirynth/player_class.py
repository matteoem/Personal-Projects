import pygame 

class Player():

    def __init__(self, playerImg_left,playerImg_right,player_thickness,x=0,y=0):
        self.playerImg_left = playerImg_left
        self.playerImg_right = playerImg_right
        self.x = x
        self.y = y
        self.thickness = player_thickness
        self.old_x = -1
        self.old_y = -1
        self.original_x=x
        self.original_y=y
        self.direction = "right"
        self.lastimgused = self.playerImg_right

    def blitPlayer(self,surface):
        
        if self.direction=="right":
            img_to_use = self.playerImg_right
        elif self.direction=="left":
            img_to_use = self.playerImg_left
        else:
            img_to_use = self.lastimgused

        surface.blit(img_to_use, (self.x,self.y))    #blit=draw on screen

    def applyCollision(self):
        hitbox_player = pygame.Rect(self.x, self.y, self.thickness, self.thickness)   #x,y,width,height
        return hitbox_player

    def updatePlayer(self,x_,y_,direction):
        self.x = x_
        self.y = y_
        self.direction = direction




class obstacle():
    def __init__(self,obstacleImg,obstacle_thickness,x,y):
        self.obstacleImg = obstacleImg
        self.x = x
        self.y = y
        self.thickness = obstacle_thickness

    def blitObstacle(self, surface):
        surface.blit(self.obstacleImg, (self.x, self.y))    #blit=draw on screen


    def applyCollision(self):
        hitbox_obstacle = pygame.Rect(self.x, self.y,self.thickness,self.thickness)   #x,y,width,height
        return hitbox_obstacle

