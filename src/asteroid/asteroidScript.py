import pygame
import random

class Asteroid:
    
    #Initialisation of class-----------------------------------------------------------------------------------------
    def __init__(self, screen, asteroid_size, position, speed_factor):
        
        self.speed_factor = speed_factor
        if position[0] < 0:
            self.pos = [random.randint(-1000, 2000), random.randint(-1000, 2000)]
        else:
            self.pos = [0, 0]
            for i in range(2):
                self.pos[i] = position[i]
        self.motion = [(random.randint(-500, 500) / 1000) * self.speed_factor, (random.randint(-500, 500) / 1000) * self.speed_factor]
        if asteroid_size == 3:
            #get a random asteroid sprite
            self.asteroid_sprite = pygame.transform.scale(pygame.image.load('New Asteroid/Sprite/Asteroid Sprite/asteroid3.png').convert_alpha(), (80, 80))
            self.image_size = 80
        if asteroid_size == 2:
            self.image_size = 50
            self.asteroid_sprite = pygame.transform.scale(pygame.image.load('New Asteroid/Sprite/Asteroid Sprite/asteroid2.png').convert_alpha(), (50, 50))
        if asteroid_size == 1:
            self.image_size = 30
            self.asteroid_sprite = pygame.transform.scale(pygame.image.load('New Asteroid/Sprite/Asteroid Sprite/asteroid1.png').convert_alpha(), (30, 30))
        self.screen = screen
    
    #Blit function---------------------------------------------------------------------------------------------------
    def blit(self, move):
        
        #reset position if out border
        if self.pos[0] < -1000 or self.pos[0] > 2000 or self.pos[1] < -1000 or self.pos[1] > 2000:
            self.pos = [random.choice((random.randint(-1000, -200), random.randint(1200, 2000))), random.choice((random.randint(-1000, -200), random.randint(1200, 2000)))]
        
        #update the position of asteroid
        for i in range(2):
            self.pos[i] -= move[i]
            self.pos[i] += self.motion[i]

        self.screen.blit(self.asteroid_sprite, (self.pos)) #blit asteroid
    
    #Collision function---------------------------------------------------------------------------------------------
    def collision(self):
        
        asteroids = []
        if self.image_size == 80:
            for i in range(random.randint(1, 3)):
                asteroid = Asteroid(self.screen, 2, self.pos, self.speed_factor)
                asteroids.append(asteroid)
        elif self.image_size == 50:
            for i in range(random.randint(1, 3)):
                asteroid = Asteroid(self.screen, 1, self.pos, self.speed_factor)
                asteroids.append(asteroid)
        else:
            pass
        return asteroids
    
    #Get pos and size function--------------------------------------------------------------------------------------
    def get_pos_size(self):
        
        return self.pos, self.image_size