import pygame
import math

class Player:
    
    def __init__(self, screen):
        self.player_pos = [500, 500]
        self.screen = screen
    
    #Get angle function-------------------------------------------------------------------------------------------------------------------------------------------
    def get_angle(self, move):
        
        #if no movement angle = 90
        if move[0] == 0 or move[1] == 0:
            angle = 90
        #else the angle equal to direction of movement
        else:
            angle = math.atan(move[1] / move[0]) * (180 / 3.1415926535)
        
        return angle

    #Update function----------------------------------------------------------------------------------------------------------------------------------------------
    def update(self, move):
        
        angle = self.get_angle(move)
        
        distance_1_3 = math.sqrt(20 ** 2 + 12 ** 2) #get distance with point 1 and 3
        
        #calcul the new point with the new angle
        if move[0] >= 0:
            angle = - angle
            point1 = (distance_1_3 * math.cos(math.radians(angle - 144)) + self.player_pos[0], -distance_1_3 * math.sin(math.radians(angle - 144)) + self.player_pos[1])
            point2 = (20 * math.cos(math.radians(angle)) + self.player_pos[0], -20 * math.sin(math.radians(angle)) + self.player_pos[1])
            point3 = (distance_1_3 * math.cos(math.radians(angle + 144)) + self.player_pos[0], -distance_1_3 * math.sin(math.radians(angle + 144)) + self.player_pos[1])
            point4 = (10 * math.cos(math.radians(angle + 180)) + self.player_pos[0], -10 * math.sin(math.radians(angle + 180)) + self.player_pos[1])
        if move[0] < 0:
            point1 = (-distance_1_3 * math.cos(math.radians(angle - 144)) + self.player_pos[0], -distance_1_3 * math.sin(math.radians(angle - 144)) + self.player_pos[1])
            point2 = (-20 * math.cos(math.radians(angle)) + self.player_pos[0], -20 * math.sin(math.radians(angle)) + self.player_pos[1])
            point3 = (-distance_1_3 * math.cos(math.radians(angle + 144)) + self.player_pos[0], -distance_1_3 * math.sin(math.radians(angle + 144)) + self.player_pos[1])
            point4 = (-10 * math.cos(math.radians(angle + 180)) + self.player_pos[0], -10 * math.sin(math.radians(angle + 180)) + self.player_pos[1])
        self.points = [point1, point2, point3, point4]

    def blit(self):
        pygame.draw.lines(self.screen, (255, 255, 255), True, self.points, 2) #draw the new figure

    def get_collision(self, asteroid_pos, asteroid_image_size):
        
        if asteroid_pos[0] < self.player_pos[0] < asteroid_pos[0] + asteroid_image_size and asteroid_pos[1] < self.player_pos[1] < asteroid_pos[1] + asteroid_image_size:
            return False
        else:
            return True