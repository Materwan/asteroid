#import
import random
import time
import pygame
import AI
import Button
import statistics

pygame.init()

#define-------------------------------------------------------------------------------------

#screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroid")

#background
background_image = pygame.image.load('Asteroid/image/background.png').convert()
background1 = pygame.transform.scale(background_image,(screen_width, screen_height))
background2 = pygame.transform.scale(background_image,(screen_width, screen_width))
y_background1 = 0
y_background2 = -600

#asteroid
asteroid_image = pygame.image.load('Asteroid/image/asteroid.png').convert_alpha()
asteroid1_image = pygame.transform.scale(asteroid_image, (50, 50))


#player
image_width = 50
image_height = 50
image_original = pygame.image.load('Asteroid/image/ship.png').convert_alpha()
x_image = (screen_width / 2)
y_image = 500
image = pygame.transform.scale(image_original, (image_width, image_height))
player_x_change = 0

#ammo
ammo_width = 7
ammo_height = 18
image_ammo = pygame.image.load('Asteroid/image/ammo.png').convert_alpha()
image_ammo = pygame.transform.scale(image_ammo, (ammo_width, ammo_height))
x_ammo = -100
y_ammo = -100
ammo_speed = -0.2

#explosion
explosion_width = 100
explosion_height = 100
image_explosion1 = pygame.image.load('Asteroid/image/explosion.png').convert_alpha()
image_explosion = pygame.transform.scale(image_explosion1, (explosion_width, explosion_height))

#game
game_over = False
win = False
menu = True

#text
text_font_timer = pygame.font.SysFont("Arial", 30)
text_font_speed_selector = pygame.font.SysFont("Arial", 30)
text_font_lose = pygame.font.SysFont("Arial", 50)
transparent = (0, 0, 0, 0)

#point
point = 0

#function-----------------------------------------------------------------------------
#player move
def player(x, y):
    screen.blit(image, (x, y)) #print the player image on the screen

def explosion(x, y, epoch):
    screen.blit(image_explosion, (x, y)) #print an explosion image on the screen
    pygame.display.update() #refresh the screen

#ammo move
def ammo(x, y):
    screen.blit(image_ammo, (x, y)) #print the ammo image on the screen

#asteroid class
class Asteroid:
    
    #__init__
    def __init__(self, speed_factor):
        
        #define the different variable use in all the differents functions
        self.x_asteroid = random.randint(0, 750)
        self.y_asteroid = -50
        self.speed_asteroid = round(random.uniform(0.1, 0.2), 2)
        self.x = 0
        self.speed_asteroid_factor = 1 * speed_factor
    
    #asteroid update
    def asteroid_update(self, asteroid1, x_ammo, y_ammo, point):
        #destuction of an asteroid
        if self.x_asteroid < x_ammo < (self.x_asteroid + 50) and self.y_asteroid < y_ammo < (self.y_asteroid + 50): #get if collision between ammo an asteroid
            
            #reset the asteroid
            self.y = 0
            self.y_asteroid = -50
            self.x_asteroid = random.randint(0, 750)
            self.speed_asteroid = round(random.uniform(0.1, 0.2), 2)
            self.x += 1
            
            #reset the ammo
            x_ammo = -100
            y_ammo = -100
            
            #add one point
            point += 1
            
        self.y_asteroid += self.speed_asteroid * self.speed_asteroid_factor #move the asteroid
        
        #reset asteroid after go out of the screen
        if self.y_asteroid > 600: #get if the asteroid if out of the screen
            
            #reset asteroid
            self.y_asteroid = -50
            self.x_asteroid = random.randint(0, 750)
            self.speed_asteroid = round(random.uniform(0.1, 0.2), 2)
            self.x += 1
            
            #increase the asteroid speed
            if self.x > 10: #get if the asteroid done 10 fall
                self.speed_asteroid_factor += 0.1 #increse the speed
                self.x = 0 #reset the number of fall
        screen.blit(asteroid1, (self.x_asteroid, self.y_asteroid)) #print the asteroid on the screen
        return self.x_asteroid, self.y_asteroid, x_ammo, y_ammo, point #return the differents values

#draw a text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color) #create an image with the text
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect) #print the image

#get if clic on a button
def clic_button(event, button, button_name, mode, mouse_pos, image_button1, image_button2):
    Clic = False
    
    #get if button is clic
    if event.type == pygame.MOUSEBUTTONDOWN:
        Clic = True
    elif event.type == pygame.MOUSEBUTTONUP:
        Clic = False
            
    #clic button animation
    if button.get_mouse_on(mouse_pos) == True and Clic == True: #get if clic and if on the button
        button.clic(pygame.image.load(image_button2).convert())
        mode = str(button_name)
    elif button.get_mouse_on(mouse_pos) != True or Clic != True:
        button.clic(pygame.image.load(image_button1).convert())
    return mode

#for write on text input
def write_on_text_input(event, button, mouse_pos, text, write):
    if event.type == pygame.MOUSEBUTTONDOWN: #left mouse clic
        if button.get_mouse_on(mouse_pos) == True:
            write = True
        else:
            write = False
    
    if event.type == pygame.KEYDOWN and write == True: #get if clic on keyboard
        if event.key == pygame.K_BACKSPACE: #get if clic on backspace
            text = text[:-1]
        else:
            text += event.unicode
    return text, write


#create the menu
def Menu(menu):
    pygame.display.set_caption("menu") #set name of the window
    
    #set the different variable an button
    mode = 'Player'
    play = ''
    Speed_text = '1'
    write = False
    Play = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [200, 75], [400, 500]
                         , "Play", (255, 255, 255),  text_font_lose) #create the play button
    Speed = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [500, 75], [400, 300]
                            , 'Speed Selector :', (255, 255, 255),  text_font_lose) #create the speed text
    Mode = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [500, 75], [400, 100]
                            , (f'Mode selector ({mode}) :'), (255, 255, 255),  text_font_lose) #create the mode text
    Mode_selector_player = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [100, 50], [300, 200]
                            , "Player", (255, 255, 255),  text_font_speed_selector) #create the player mode selector button
    Mode_selector_AI = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [100, 50], [500, 200]
                            , "AI", (255, 255, 255),  text_font_speed_selector) #create the AI mode selector button
    Speed_selector = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [100, 50], [400, 400]
                            , str(Speed_text), (255, 255, 255),  text_font_speed_selector) #create the speed selector input text box
    
    #the loop
    while menu == True:
        #update
        screen.fill("black") #black background
        mouse_pos = pygame.mouse.get_pos() #get mouse position
        Play.update(screen) #update play button
        Speed.update(screen) #update speed text
        Mode.update_text_input(screen, (f'Mode selector ({mode}) :'), text_font_lose) #update mode text
        Mode_selector_player.update(screen) #update player mode selector button
        Mode_selector_AI.update(screen) #update AI mode selector button
        Speed_selector.update_text_input(screen, Speed_text, text_font_speed_selector) # update speed selector input text box
        
        #verif modification
        for event in pygame.event.get(): #define event and get it
            if event.type == pygame.QUIT: #close tab
                pygame.quit()
                menu = False
            
            #get if speed selector is select
            if event.type == pygame.MOUSEBUTTONDOWN: #left mouse clic
                if Speed_selector.get_mouse_on(mouse_pos) == True:
                    write = True
                else:
                    write = False
            
            #get the writed text
            if event.type == pygame.KEYDOWN and write == True: #get if clic on keyboard
                if event.key == pygame.K_BACKSPACE: #get if clic on backspace
                    Speed_text = Speed_text[:-1]
                else:
                    Speed_text += event.unicode
            
            mode = clic_button(event, Mode_selector_player, "Player", mode, mouse_pos, ('Asteroid/image/button1.png'), ('Asteroid/image/button2.png'))
            mode = clic_button(event, Mode_selector_AI, "AI", mode, mouse_pos, ('Asteroid/image/button1.png'), ('Asteroid/image/button2.png'))
            play = clic_button(event, Play, "Play", play, mouse_pos, ('Asteroid/image/button1.png'), ('Asteroid/image/button2.png'))
            
            #lunch the game
            if play == "Play":
                if Speed_text != '': #get the speed of game
                    speed = float(Speed_text)
                menu = False
                if mode == "Player": #lunch game play by a player
                    game_player(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, speed)
                if mode == "AI": #lunch game play by the AI
                    AI_Menu(True, speed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if Speed_text != '': #get the speed of game
                        speed = float(Speed_text)
                    menu = False
                    if mode == "Player": #lunch game play by a player
                        game_player(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, speed)
                    if mode == "AI": #lunch game play by the AI
                        AI_Menu(True, speed)
        pygame.display.update() #refresh the window
    return speed #return the speed of game

#create the menu of AI
def AI_Menu(menu, speed_factor):
    
    play = ''
    Exploration_rate_text = ''
    Exploration_rate_write = False
    Exploration_Rate_Selector = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [100, 40], [400, 150]
                                              ,Exploration_rate_text, (255, 255, 255), text_font_speed_selector)
    Exploration_Rate = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [400, 80], [400, 75]
                                              , ('Exploration rate :'), (255, 255, 255), text_font_lose)
    Learning_rate_text = ''
    Learning_rate_write = False
    Learning_Rate_Selector = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [100, 40], [400, 300]
                                              ,Learning_rate_text, (255, 255, 255), text_font_speed_selector)
    Learning_Rate = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [400, 80], [400, 225]
                                              , ('Learning rate :'), (255, 255, 255), text_font_lose)
    
    Discount_factor_text = ''
    Discount_factor_write = False
    Discount_Factor_Selector = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [100, 40], [400, 450]
                                              ,Discount_factor_text, (255, 255, 255), text_font_speed_selector)
    Discount_Factor = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [400, 80], [400, 375]
                                              , ('Discount factor :'), (255, 255, 255), text_font_lose)
    
    Play = Button.Button(pygame.image.load('Asteroid/image/button1.png').convert_alpha(), [200, 75], [400, 525]
                         , "Play", (255, 255, 255),  text_font_lose) #create the play button
    
    while menu == True:
        screen.fill("black") #black background
        mouse_pos = pygame.mouse.get_pos() #get mouse position
        Exploration_Rate_Selector.update_text_input(screen, Exploration_rate_text, text_font_speed_selector)
        Exploration_Rate.update_text_input(screen, ('Exploration rate :'), text_font_lose)
        Learning_Rate_Selector.update_text_input(screen, Learning_rate_text, text_font_speed_selector)
        Learning_Rate.update_text_input(screen, ('Learning rate :'), text_font_lose)
        Discount_Factor_Selector.update_text_input(screen, Discount_factor_text, text_font_speed_selector)
        Discount_Factor.update_text_input(screen, ('Discount factor :'), text_font_lose)
        Play.update(screen) #update play button
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #close tab
                pygame.quit()
                menu = False
            Exploration_rate_text, Exploration_rate_write = write_on_text_input(event, Exploration_Rate_Selector, mouse_pos, Exploration_rate_text, Exploration_rate_write)
            Learning_rate_text, Learning_rate_write = write_on_text_input(event, Learning_Rate_Selector, mouse_pos, Learning_rate_text, Learning_rate_write)
            Discount_factor_text, Discount_factor_write = write_on_text_input(event, Discount_Factor_Selector, mouse_pos, Discount_factor_text, Discount_factor_write)
            
            play = clic_button(event, Play, "Play", play, mouse_pos, ('Asteroid/image/button1.png'), ('Asteroid/image/button2.png'))
            
            #lunch the game
            if play == "Play":
                exploration_rate = float(Exploration_rate_text)
                learning_rate = float(Learning_rate_text)
                discount_factor = float(Discount_factor_text)
                game_AI(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, exploration_rate, learning_rate, discount_factor, speed_factor)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exploration_rate = float(Exploration_rate_text)
                    learning_rate = float(Learning_rate_text)
                    discount_factor = float(Discount_factor_text)
                    game_AI(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, exploration_rate, learning_rate, discount_factor, speed_factor)
        pygame.display.update()

#game---------------------------------------------------------------------------------
def game_player(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, speed_factor):
    
    epoch = time.time() #set the actual time
    
    #create the differents asteroids
    asteroid1 = Asteroid(speed_factor)
    asteroid2 = Asteroid(speed_factor)
    asteroid3 = Asteroid(speed_factor)
    asteroid4 = Asteroid(speed_factor)
    asteroid5 = Asteroid(speed_factor)
    
    #time before start
    screen.fill("black") #black background
    draw_text("3", text_font_lose, (255, 255, 255), screen_width / 2, screen_height / 2) #draw 3 on screen
    pygame.display.update() #update screen
    time.sleep(1) #wait one seconde
    screen.fill("black") #same
    draw_text("2", text_font_lose, (255, 255, 255), screen_width / 2, screen_height / 2)
    pygame.display.update()
    time.sleep(1)
    screen.fill("black") #same
    draw_text("1", text_font_lose, (255, 255, 255), screen_width / 2, screen_height / 2)
    pygame.display.update()
    time.sleep(1)

    #game loop
    while not game_over:
        
        #set the differents values
        x = 0 #set the number of scroll of the background
        speed_background_factor = 1
        screen.blit(background1,(0,y_background1))
        screen.blit(background2,(0,y_background2))
        epoch_now = time.time()
        Time = epoch_now - epoch
        draw_text(str(round((epoch_now - epoch), 2)), text_font_timer, (255, 255, 255), 30, 10) #draw the timer
        point_draw = str(point)
        draw_text(point_draw, text_font_timer, (255, 255, 255), (screen_width - 30), 10) #draw the point counter
        
        #get if are a collision between player and asteroid
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid1.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid2.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid3.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid4.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid5.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        
        #quit
        for event in pygame.event.get(): #get if close the window
            if event.type == pygame.QUIT:
                pygame.quit()
            
            #get if an action is done
            if event.type == pygame.KEYDOWN: #get if clic on key
                if event.key == pygame.K_RIGHT: #get if this key is the right arrow
                    player_x_change = 0.1
                if event.key == pygame.K_LEFT: #get if this key is the left arrow
                    player_x_change = -0.1
                if event.key == pygame.K_SPACE: #get if clic on space key
                    if y_ammo < 0: #get if ammo is out of the screen
                        x_ammo = x_image + 25 - 5 / 2
                        y_ammo = y_image + 25 - 18 / 2
            if event.type == pygame.KEYUP: #get if release key
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #get if this key is right or left arrow
                    player_x_change = 0
        
        #modify the player position if it go out of the border
        if x_image < 0: #get if is too at left
            x_image += 0.1
        if x_image > 750: #get if is too at right
            x_image += -0.1
        
        #update the screen and values
        if point >= 100: #get if have 100 point, if is win
            game_over = True
        y_ammo += ammo_speed * speed_factor #move the ammo
        x_image = x_image + player_x_change #move the player
        ammo(x_ammo, y_ammo) #print the ammo
        player(x_image, y_image) #print the player
        y_background1 += 0.1 * speed_factor * speed_background_factor #move the first background
        y_background2 += 0.1 * speed_factor * speed_background_factor #move the second background
        if y_background1 >= 600: #get if background is out of the screen
            y_background1 = -600 #replace it on top of the screen
        if y_background2 >= 600: #same
            y_background2 = -600
            x += 1 #increase the number of scroll of background
        if x >= 10: #get if the background scoll 10 time
            speed_background_factor += 0.1 #increase the speed of background
            x = 0 #reset the number of scroll
        pygame.display.update() #update the screen

    #out of the loop (game finish)
    if point >= 100: #get if win
        draw_text(str(f'You win in {Time} secondes'), text_font_lose, (255, 255, 255), (screen_width / 2), (screen_height / 2)) #draw the win text
        pygame.display.update() #update the screen
        time.sleep(3) #wait 3 second
        pygame.quit() #close the window
    if point < 100: #get if lose
        screen.blit(image_explosion, ((x_image - 25), (y_image - 25))) #print an explosion on space ship
        draw_text(str(f'You lose in {Time} secondes with {point_draw} point'), text_font_lose, (255, 255, 255), (screen_width / 2), (screen_height / 2)) #print the lose text
        pygame.display.update() #update the screen
        time.sleep(3) #wait 3 second
        pygame.quit() #close the window

#AI game------------------------------------------------------------------------------
#same as the game_player but with some little modif
def game_AI(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, exploration_rate, learning_rate, discount_factor, speed_factor):
    
    #create differents asteroids
    asteroid1 = Asteroid(speed_factor)
    asteroid2 = Asteroid(speed_factor)
    asteroid3 = Asteroid(speed_factor)
    asteroid4 = Asteroid(speed_factor)
    asteroid5 = Asteroid(speed_factor)
    
    '''
    #time before start
    screen.fill("black") #black background
    draw_text("3", text_font_lose, (255, 255, 255), screen_width / 2, screen_height / 2) #draw 3 on screen
    pygame.display.update() #update screen
    time.sleep(1) #wait one seconde
    screen.fill("black") #same
    draw_text("2", text_font_lose, (255, 255, 255), screen_width / 2, screen_height / 2)
    pygame.display.update()
    time.sleep(1)
    screen.fill("black") #same
    draw_text("1", text_font_lose, (255, 255, 255), screen_width / 2, screen_height / 2)
    pygame.display.update()
    time.sleep(1)
    '''
    
    epoch = time.time() #set the actual time
    
    #game loop
    while not game_over:
        x = 0
        speed_background_factor = 1
        AI1 = AI.ai(point, exploration_rate, x_image, y_image, learning_rate, discount_factor)
        screen.blit(background1,(0,y_background1))
        screen.blit(background2,(0,y_background2))
        epoch_now = time.time()
        Time = round((epoch_now - epoch) * speed_factor, 2)
        Time_text = str(round((epoch_now - epoch)* speed_factor, 2))
        draw_text(Time_text, text_font_timer, (255, 255, 255), 30, 10)
        point_draw = str(point)
        draw_text(point_draw, text_font_timer, (255, 255, 255), (screen_width - 30), 10)
        
        #get if are a collision between player and asteroid the distance with the asteroid and if an asteroid is on the y axis of space ship
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid1.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        AI1.get_distance(x_asteroid, y_asteroid)
        AI1.get_axis(x_asteroid)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid2.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        AI1.get_distance(x_asteroid, y_asteroid)
        AI1.get_axis(x_asteroid)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid3.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        AI1.get_distance(x_asteroid, y_asteroid)
        AI1.get_axis(x_asteroid)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid4.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        AI1.get_distance(x_asteroid, y_asteroid)
        AI1.get_axis(x_asteroid)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        x_asteroid, y_asteroid, x_ammo, y_ammo, point = asteroid5.asteroid_update(asteroid1_image, x_ammo, y_ammo, point)
        AI1.get_distance(x_asteroid, y_asteroid)
        AI1.get_axis(x_asteroid)
        if x_asteroid < x_image < (x_asteroid + 50) and y_asteroid < y_image < (y_asteroid + 50) or x_asteroid < (x_image + 50) < (x_asteroid + 50) and y_asteroid < (y_image + 50) < (y_asteroid + 75):
            game_over = True
        
        #create fake asteroid for prevent AI go at border
        AI1.get_distance(-50, 500)
        AI1.get_distance(750, 500)
        
        #get only the distance with the nearest asteroid
        AI1.get_lowest_distance()
        
        #update the Q value
        AI1.get_Q_value(point, y_ammo)
        
        #get the action with all of the previous values
        action = AI1.choose_A()
        
        #the rest is same as game_player
        
        #quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        #move
        if action == 0:
            player_x_change = -0.1
        elif action == 1:
            player_x_change = 0.1
        else:
            player_x_change = 0
            
        #ammo
        if action == 2:
            if y_ammo < 0:
                x_ammo = x_image + 25 - 5 / 2
                y_ammo = y_image + 25 - 18 / 2
        
        #border
        if x_image < 0:
            x_image += 0.05 * speed_factor
        if x_image > 750:
            x_image -= 0.05 * speed_factor
        
        #update
        if point >= 100:
            game_over = True
        y_ammo += ammo_speed * speed_factor
        x_image = x_image + player_x_change * speed_factor
        ammo(x_ammo, y_ammo)
        player(x_image, y_image)
        y_background1 += 0.1 * speed_factor * speed_background_factor
        y_background2 += 0.1 * speed_factor * speed_background_factor
        if y_background1 >= 600:
            y_background1 = -600
        if y_background2 >= 600:
            y_background2 = -600
            x += 1
        if x >= 10:
            speed_background_factor += 0.1
            x = 0
        pygame.display.update()

    if point >= 100:
        win_text = str(f'You win in {Time_text} secondes')
        draw_text(win_text, text_font_lose, (255, 255, 255), (screen_width / 2), (screen_height / 2))
        pygame.display.update()
        time.sleep(0)
        game_over = True
    if point < 100:
        screen.blit(image_explosion, ((x_image - 25), (y_image - 25)))
        lose_text = str(f'You lose in {Time_text} secondes with {point_draw} point')
        draw_text(lose_text, text_font_lose, (255, 255, 255), (screen_width / 2), (screen_height / 2))
        pygame.display.update()
        time.sleep(0)
        game_over = True
    return Time, point


speed_factor = Menu(menu) #lunch the menu

best = 100
exploration_rate = 0
learning_rate = 0.4 #0.41251764175009126
discount_factor = 0.6 #0.5726526728084583

while True:
    time_list = []
    point_list = []
    speed_factor = 100
    for i in range(4):
        time_get, point_get = game_AI(game_over, point, x_ammo, y_ammo, x_image, y_image, player_x_change, y_background1, y_background2, exploration_rate, learning_rate, discount_factor, speed_factor)
        time_list.append(time_get)
        point_list.append(point_get)
    time_average_normal = statistics.mean(time_list)
    point_average_normal = statistics.mean(point_list)
    reward = time_average_normal / point_average_normal
    if reward < best:
        best = reward
        best_exploration_rate = exploration_rate
        best_learning_rate = learning_rate
        best_discount_factor = discount_factor
        print(f'{exploration_rate}, {learning_rate}, {discount_factor}, is best than last')
        #exploration_rate = statistics.mean([random.random(), best_exploration_rate, best_exploration_rate, best_exploration_rate, best_exploration_rate, best_exploration_rate])
        exploration_rate = 0
        learning_rate = statistics.mean([random.uniform(best_learning_rate - 0.01, best_learning_rate + 0.01), best_learning_rate, best_learning_rate, best_learning_rate, best_learning_rate, best_learning_rate])
        discount_factor = statistics.mean([random.uniform(best_discount_factor - 0.01, best_discount_factor + 0.01), best_discount_factor, best_discount_factor, best_discount_factor, best_discount_factor, best_discount_factor])
    else:
        print(f'{reward, exploration_rate, learning_rate, discount_factor}, isn t best than last, best is {best, best_exploration_rate, best_learning_rate, best_discount_factor}')
        #exploration_rate = statistics.mean([random.random(), best_exploration_rate, best_exploration_rate, best_exploration_rate, best_exploration_rate, best_exploration_rate])
        exploration_rate = 0
        learning_rate = statistics.mean([random.uniform(best_learning_rate - 0.01, best_learning_rate + 0.01), best_learning_rate, best_learning_rate, best_learning_rate, best_learning_rate, best_learning_rate])
        discount_factor = statistics.mean([random.uniform(best_discount_factor - 0.01, best_discount_factor + 0.01), best_discount_factor, best_discount_factor, best_discount_factor, best_discount_factor, best_discount_factor])