import pygame
import random
import UIScript
import asteroidScript
import SaveScript

#Lunch Menu class----------------------------------------------------------------------------------------------------------------------------------------------------------
class Lunch_Menu:
    
    def __init__(self, screen):
        
        self.asteroids = []
        self.background = pygame.transform.scale(pygame.image.load('New Asteroid/Sprite/space_background.png').convert_alpha(), (1000, 1000))
        for i in range(50):
            asteroid = asteroidScript.Asteroid(screen, random.randint(1, 3), [-10, 0], 1)
            self.asteroids.append(asteroid)
        self.running = True
        self.settings = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.speed_factor = 1
        self.mode = 'AI'
        self.save = ''
        self.play_button = UIScript.Clickable_Button((400, 350), (200, 50), 'New Asteroid/Sprite/Menu Button/Play Button.png', 'New Asteroid/Sprite/Menu Button/Play Button Clicked.png', self.screen)
        self.settings_button = UIScript.Clickable_Button((400, 475), (200, 50), 'New Asteroid/Sprite/Menu Button/Settings Button.png', 'New Asteroid/Sprite/Menu Button/Settings Button Clicked.png', self.screen)
        self.quit_button = UIScript.Clickable_Button((400, 600), (200, 50), 'New Asteroid/Sprite/Menu Button/Quit Button.png', 'New Asteroid/Sprite/Menu Button/Quit Button Clicked.png', self.screen)
    
    def event(self):
        
        self.play = self.play_button.event()
        self.settings = self.settings_button.event()
        self.running = self.quit_button.event()
        
        if self.settings == False:
            self.settings, self.running, self.speed_factor, self.mode, self.save = Settings_Menu(self.asteroids, self.background, self.screen).run()
            self.settings_button.click = False
        else:
            self.settings = True
        
        if self.play == False:
            self.running = False
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
    
    def display(self):
        
        self.screen.blit(self.background, (0, 0))
        
        for i in self.asteroids:
            i.blit([0, 0]) #move all asteroids
        
        self.play_button.blit()
        self.settings_button.blit()
        self.quit_button.blit()
        
        pygame.display.flip()
    
    def run(self):
        
        while self.running:
            
            self.event()
            self.display()
            
            self.clock.tick(60)
        
        for asteroid in self.asteroids:
            del asteroid
        
        if self.running == False and self.play == False:
            return True, self.speed_factor, self.mode, self.save
        else:
            return False, 0, '', ''

#Settings Menu class----------------------------------------------------------------------------------------------------------------------------------------------------------
class Settings_Menu:
    
    def __init__(self, asteroids, background, screen):
        
        self.asteroids = asteroids
        self.background = background
        self.clock = pygame.time.Clock()
        self.running = True
        self.main_running = True
        self.screen = screen
        self.mode_box = UIScript.Text_Box((400, 150), (200, 50), (450, 160),'New Asteroid/Sprite/Menu Button/Empty Button.png', 'Mode :', 48, self.screen)
        self.mode_AI_button = [UIScript.Clickable_Button((275, 225), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen),
                               UIScript.Counter('AI', (350, 235), 48, self.screen)]
        self.mode_player_button = [UIScript.Clickable_Button((525, 225), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen),
                                   UIScript.Counter('Player', (575, 235), 48, self.screen)]
        self.speed_box = UIScript.Text_Box((400, 325), (200, 50), (450, 335),'New Asteroid/Sprite/Menu Button/Empty Button.png', 'Speed :', 48, self.screen)
        self.input_box_speed = UIScript.Input_Box((400, 400), (500, 500), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen, '1')
        self.import_box = UIScript.Text_Box((400, 500), (200, 50), (450, 510), 'New Asteroid/Sprite/Menu Button/Empty Button.png', 'Import :', 48, self.screen)
        self.input_box_import = UIScript.Input_Box((400, 575), (500, 585), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen)
        self.quit_button = UIScript.Clickable_Button((400, 675), (200, 50), 'New Asteroid/Sprite/Menu Button/Back Button.png', 'New Asteroid/Sprite/Menu Button/Back Button Clicked.png', self.screen)
        self.speed_factor = 1
        self.save = ''
        self.mode = 'AI'
    
    def event(self):
        
        self.running = self.quit_button.event()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.main_running = False
                self.running = False
            
            self.speed_clicked = self.input_box_speed.event()
            self.import_clicked = self.input_box_import.event()
            self.AI_clicked = self.mode_AI_button[0].event()
            self.player_clicked = self.mode_player_button[0].event()
            
            if self.speed_clicked == False:
                self.speed_factor = self.input_box_speed.input(event)
            elif self.import_clicked == False:
                self.save = self.input_box_import.input(event)
            elif self.AI_clicked == False:
                self.mode = 'AI'
            elif self.player_clicked == False:
                self.mode = 'player'
    
    def display(self):
        
        self.screen.blit(self.background, (0, 0))
        
        for i in self.asteroids:
            i.blit([0, 0]) #move all asteroids
        
        self.mode_box.blit()
        self.input_box_speed.blit()
        self.speed_box.blit()
        for i in range(2):
            self.mode_AI_button[i].blit()
            self.mode_player_button[i].blit()
        self.import_box.blit()
        self.input_box_import.blit()
        self.quit_button.blit()
        
        pygame.display.update()
    
    def run(self):
        
        while self.running:
            
            self.event()
            self.display()
            
            self.clock.tick(60)
        
        if self.main_running == False:
            return True, False, float(self.speed_factor), self.mode, self.save
        else:
            return True, True, float(self.speed_factor), self.mode, self.save

#Pause Menu class----------------------------------------------------------------------------------------------------------------------------------------------------------
class Pause_Menu:
    
    def __init__(self, speed_factor, screen, gen, neuronal_network):
        self.running = True
        self.clock = pygame.time.Clock()
        self.neuronal_network = neuronal_network
        self.gen = gen
        self.screen = screen
        self.speed_factor = speed_factor
        if neuronal_network != None:
            self.speed_box = UIScript.Text_Box((400, 375), (200, 50), (450, 385),'New Asteroid/Sprite/Menu Button/Empty Button.png', 'Speed :', 48, self.screen)
            self.input_box_speed = UIScript.Input_Box((400, 450), (500, 475), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen, '1')
            self.save_box = UIScript.Counter('Save', (465, 560), 48, self.screen)
            self.save_button = UIScript.Clickable_Button((400, 550), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen)
            self.resume_button = UIScript.Clickable_Button((400, 275), (200, 50), 'New Asteroid/Sprite/Menu Button/Resume Button.png', 'New Asteroid/Sprite/Menu Button/Resume Button Clicked.png', self.screen)
            self.quit_button = UIScript.Clickable_Button((400, 650), (200, 50), 'New Asteroid/Sprite/Menu Button/Quit Button.png', 'New Asteroid/Sprite/Menu Button/Quit Button Clicked.png', self.screen)
        else:
            self.speed_box = UIScript.Text_Box((400, 425), (200, 50), (450, 435),'New Asteroid/Sprite/Menu Button/Empty Button.png', 'Speed :', 48, self.screen)
            self.input_box_speed = UIScript.Input_Box((400, 525), (500, 535), (200, 50), 'New Asteroid/Sprite/Menu Button/Empty Button.png', self.screen, '1')
            self.resume_button = UIScript.Clickable_Button((400, 325), (200, 50), 'New Asteroid/Sprite/Menu Button/Resume Button.png', 'New Asteroid/Sprite/Menu Button/Resume Button Clicked.png', self.screen)
            self.quit_button = UIScript.Clickable_Button((400, 625), (200, 50), 'New Asteroid/Sprite/Menu Button/Quit Button.png', 'New Asteroid/Sprite/Menu Button/Quit Button Clicked.png', self.screen)
    
    def event(self):
        
        self.running = self.resume_button.event()
        self.main_running = self.quit_button.event()
        
        if self.main_running == False:
            self.running = False
        
        for event in pygame.event.get():
            
            self.input_box_clicked = self.input_box_speed.event()
            if self.neuronal_network != None:
                self.save_clicked = self.save_button.event()
            
            if self.input_box_clicked == False:
                self.speed_factor = self.input_box_speed.input(event)
            elif self.neuronal_network != None:
                if self.save_clicked == False:
                    SaveScript.save_nn('save.txt', self.gen, self.neuronal_network)
            
            if event.type == pygame.QUIT:
                self.main_running = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def display(self):
        
        self.resume_button.blit()
        self.input_box_speed.blit()
        self.speed_box.blit()
        if self.neuronal_network != None:
            self.save_button.blit()
            self.save_box.blit()
        self.quit_button.blit()
        
        pygame.display.update()
    
    def run(self):
        
        while self.running:
            
            self.event()
            self.display()
            
            self.clock.tick(60)
        
        if self.running == False and self.main_running == False:
            return False, float(self.speed_factor)
        elif self.running == False and self.main_running == True:
            return True, float(self.speed_factor)

#Lose Menu class-----------------------------------------------------------------------------------------------------------------------------------------------------------
class Lose_Menu:
    
    def __init__(self, screen):
        self.running = bool(True)
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.quit_button = UIScript.Clickable_Button((400, 600), (200, 50), 'New Asteroid/Sprite/Menu Button/Quit Button.png', 'New Asteroid/Sprite/Menu Button/Quit Button Clicked.png', self.screen)
        self.new_game_button = UIScript.Clickable_Button((400, 350), (200, 50), 'New Asteroid/Sprite/Menu Button/New game Button.png', 'New Asteroid/Sprite/Menu Button/Menu Button Clicked.png', self.screen)
    
    def event(self):
        
        self.new_game = self.new_game_button.event()
        self.running = self.quit_button.event()
        
        if self.new_game == False:
            self.running = False
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
    
    def display(self):
        
        self.new_game_button.blit()
        self.quit_button.blit()
        
        pygame.display.update()
    
    def run(self):
        
        while self.running:
            
            self.event()
            self.display()
            
            self.clock.tick(60)
        
        if self.running == False and self.new_game == False:
            return True
        else:
            return False