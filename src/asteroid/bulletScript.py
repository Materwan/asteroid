import pygame

#Bullet class------------------------------------------------------------------------------------------
class Bullet:

    #Initialisation of class---------------------------------------------------------------------------
    def __init__(self, speed_factor, player_move, screen):
        
        self.pos = [500, 500]
        self.last_pos = self.pos
        self.speed_factor = speed_factor
        self.motion = [0, 0]
        if player_move[0] == 0.001 and player_move[0] == 0.001:
            self.pos = [2000, 2000]
        else:
            for i in range(2):
                self.motion[i] = player_move[i] * 10 * self.speed_factor
        self.screen = screen
    
    #Move function-------------------------------------------------------------------------------------
    def move(self):
        
        #set the new position
        for i in range(2):
            self.pos[i] += self.motion[i]
    
    #Blit function----------------------------------------------------------------------
    def blit(self):
        pygame.draw.circle(self.screen, (255, 255, 255), self.pos, 3, 3) #draw the bullet
    
    #Collision function--------------------------------------------------------------------------------
    def border(self):
        
        #get if are a collision with an asteroid or return if bullet is out border and if need to destroy it
        if self.pos[0] <= 0 or self.pos[0] > 1000 or self.pos[1] <= 0 or self.pos[1] > 1000:
            return True
        else:
            return False