# import
from shapely.geometry import LineString, Polygon
import pygame
import random
import time
import playerScript
import asteroidScript
import bulletScript
import UIScript
import menu
import AAI
import Neural_network
import SaveScript

pygame.init()  # initialise pygame

# set the size of window
screen_width = 800
screen_height = 800

# set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("game")


# Game class---------------------------------------------------------------------------------------
class Game:

    # Initialisation of class----------------------------------------------------------------------
    def __init__(
        self,
        max_speed,
        speed_factor,
        screen,
        iteration,
        mode,
        generation=None,
        ai=None,
        best_nn=None,
    ):

        self.screen = screen
        self.backgrounds = []
        self.asteroids = []
        self.bullets = []
        self.mode = mode
        self.x = 0
        self.iterations = iteration
        self.generation = generation
        self.max_speed = max_speed
        self.speed_factor = speed_factor
        for i in range(4):
            background = pygame.transform.scale(
                pygame.image.load("New Asteroid/Sprite/space_background.png").convert(),
                (1000, 1000),
            )
            self.backgrounds.append(background)
        # create 50 asteroid
        for i in range(50):
            asteroid = asteroidScript.Asteroid(
                screen, random.randint(1, 3), [-10, 0], self.speed_factor
            )
            self.asteroids.append(asteroid)
        self.epoch = time.time()
        self.time = time.time()
        self.iteration = 0
        self.i = 0
        self.last_bullet = 0
        self.score = 0
        self.background_pos = [0, 0]
        self.move = [0.001, 0.001]
        self.move_speed = [0, 0]
        self.contine = True
        self.exit_neuron = None
        self.running = True
        self.main_running = True
        self.player = playerScript.Player(screen)
        self.counter = UIScript.Counter(0, (900, 0), 48, screen)
        self.counter_time = UIScript.Counter(0, (0, 0), 36, self.screen)
        if self.mode == "AI":
            self.counter_gen = UIScript.Counter(0, (0, 975), 36, self.screen)
            self.counter_iteration = UIScript.Counter(0, (850, 975), 36, self.screen)
        self.clock = pygame.time.Clock()
        self.screen_surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)
        self.ai = ai
        self.best_nn = best_nn

    # Event function------------------------------------------------------------------------------
    def event(self):

        self.i += 1

        for event in pygame.event.get():  # if event is get

            if event.type == pygame.QUIT:  # if it is close the game
                # close the game
                self.running = False

            if self.mode == "player":
                if event.type == pygame.KEYDOWN:  # get key pressed

                    if event.key == pygame.K_RIGHT:  # get the key pressed
                        self.move_speed[0] = (
                            0.1 * self.speed_factor
                        )  # modify movement speed
                    elif event.key == pygame.K_LEFT:  # same
                        self.move_speed[0] = -0.1 * self.speed_factor
                    elif event.key == pygame.K_UP:  # same
                        self.move_speed[1] = -0.1 * self.speed_factor
                    elif event.key == pygame.K_DOWN:  # same
                        self.move_speed[1] = 0.1 * self.speed_factor

                    elif event.key == pygame.K_SPACE:  # get the key pressed
                        if self.i > self.last_bullet + 5:
                            bullet = bulletScript.Bullet(
                                self.speed_factor, self.move, self.screen
                            )  # create a bullet
                            self.bullets.append(bullet)  # add him to the list
                            self.last_bullet = self.i

            if event.type == pygame.KEYDOWN:  # get key pressed

                if event.key == pygame.K_ESCAPE:
                    diff = time.time() - self.epoch
                    pauseMenu = menu.Pause_Menu(
                        self.speed_factor, self.screen, self.generation, self.best_nn
                    )
                    self.running, self.speed_factor = pauseMenu.run()
                    if self.running == False:
                        self.main_running = False
                    for asteroid in self.asteroids:
                        asteroid.motion[0] = asteroid.motion[0] * (
                            self.speed_factor / asteroid.speed_factor
                        )
                        asteroid.motion[1] = asteroid.motion[1] * (
                            self.speed_factor / asteroid.speed_factor
                        )
                        asteroid.speed_factor = self.speed_factor
                    for bullet in self.bullets:
                        bullet.speed_factor = self.speed_factor
                    self.epoch = time.time() - diff

            elif event.type == pygame.KEYUP:  # get key released

                if (
                    event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT
                ):  # get the key released
                    self.move_speed[0] = 0  # modify the movement speed
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:  # same
                    self.move_speed[1] = 0

    # Update function-----------------------------------------------------------------------------
    def update(self):

        self.last_pos = self.player.player_pos

        if self.mode == "AI":
            asteroid_on_screen = []
            for asteroid in self.asteroids:
                if (
                    1000 - asteroid.image_size > asteroid.pos[0] > 0
                    and 1000 - asteroid.image_size > asteroid.pos[1] > 0
                ):
                    asteroid_on_screen.append(asteroid)

            # get the value of all the enter neuron
            value_box = []
            for column in range(10):
                row_value = []
                for row in range(10):
                    value = False
                    for asteroid in asteroid_on_screen:
                        # get if one asteroid is in the enter neuron
                        if (
                            row * 100 + 100 > asteroid.pos[0] > row * 100
                            and column * 100 + 100 > asteroid.pos[1] > column * 100
                        ):
                            value = True
                    if value == True:  # if one asteroid is on enter neuron
                        row_value.append(1)  # set the neuron to 1
                    else:
                        row_value.append(0)  # else set the neuron to 0
                value_box.append(row_value)

            self.ai.update(
                value_box
            )  # run the neuronal network get him and the value of the exit neuron

            self.exit_neuron = []
            for exit_neuron in self.ai.exit_neuron:
                self.exit_neuron.append(exit_neuron.value)

            if self.exit_neuron[0] >= 0.5:
                self.move_speed[0] += 0.1 * self.speed_factor  # modify movement speed
            if self.exit_neuron[1] >= 0.5:  # same
                self.move_speed[0] += -0.1 * self.speed_factor
            if self.exit_neuron[2] >= 0.5:  # same
                self.move_speed[1] += -0.1 * self.speed_factor
            if self.exit_neuron[3] >= 0.5:  # same
                self.move_speed[1] += 0.1 * self.speed_factor

            if self.exit_neuron[4] >= 0.5:  # get the key pressed
                if self.speed_factor > 10 or self.i > self.last_bullet + 5:
                    bullet = bulletScript.Bullet(
                        self.speed_factor, self.move, self.screen
                    )  # create a bullet
                    self.bullets.append(bullet)  # add him to the list
                    self.last_bullet = self.i

        for bullet in self.bullets:
            bullet.move()

        self.player.update(self.move)  # update the position and angle of player

        self.contine_list = []
        segment = LineString([self.player.player_pos, self.last_pos])

        for asteroid in self.asteroids:  # for all asteroids

            asteroid_carre = Polygon(
                [
                    asteroid.pos,
                    (asteroid.pos[0] + asteroid.image_size, asteroid.pos[1]),
                    (
                        asteroid.pos[0] + asteroid.image_size,
                        asteroid.pos[1] + asteroid.image_size,
                    ),
                    (asteroid.pos[0], asteroid.pos[1] + asteroid.image_size),
                    asteroid.pos,
                ]
            )

            self.contine_list.append(segment.intersects(asteroid_carre))

            for bullet in self.bullets:  # for all bullets

                new_pos_bullet = [
                    bullet.pos[0] - bullet.motion[0],
                    bullet.pos[1] - bullet.motion[1],
                ]
                segment_bullet = LineString([bullet.pos, new_pos_bullet])

                if segment_bullet.intersects(asteroid_carre) == True:
                    self.bullets.remove(bullet)  # delet bullet from the list
                    del bullet  # delete the bullet object
                    if asteroid.image_size == 50:
                        self.score += 30
                        self.counter.update(self.score)
                    elif asteroid.image_size == 80:
                        self.score += 10
                        self.counter.update(self.score)
                    elif asteroid.image_size == 100:
                        self.score += 5
                        self.counter.update(self.score)
                    asteroids = asteroid.collision()  # create new asteroid
                    self.asteroids.remove(asteroid)  # delete asteroid from list
                    del asteroid  # delete asteroid object
                    for new_asteroid in asteroids:  # for all new asteroids

                        self.asteroids.append(new_asteroid)  # add it to the list
                    break
                if asteroid == self.asteroids[len(self.asteroids) - 1]:
                    if bullet.border() == True:
                        self.bullets.remove(bullet)  # delet bullet from the list
                        del bullet  # delete the bullet object
                        break
                    else:
                        continue

        for i in range(2):  # modify the x and y of backgrounds
            self.move[i] += self.move_speed[i]
            if self.move[i] < -self.max_speed * self.speed_factor:
                self.move[i] = -self.max_speed * self.speed_factor
            if self.move[i] > self.max_speed * self.speed_factor:
                self.move[i] = self.max_speed * self.speed_factor
            self.background_pos[i] -= self.move[i]
            if self.background_pos[i] > 1000:
                self.background_pos[i] -= 1000
            if self.background_pos[i] < -1000:
                self.background_pos[i] += 1000
            if self.mode == "AI":
                self.move_speed[i] = 0

        if self.epoch + (30 / self.speed_factor) <= time.time():  # if timer > 30 second
            # create 50 new asteroid
            for i in range(50):
                asteroid = asteroidScript.Asteroid(
                    screen, random.randint(1, 3), [-10, 0], self.speed_factor
                )
                self.asteroids.append(asteroid)
            self.epoch = time.time()  # reset timer

    # Display function----------------------------------------------------------------------------
    def display(self):

        other_background_pos = [0, 0]  # set the position of other background at 0
        if self.background_pos[0] < 0:  # if first background is out border
            other_background_pos[0] = (
                self.background_pos[0] + 1000
            )  # set the other background pos
        if self.background_pos[0] > 0:  # same
            other_background_pos[0] = self.background_pos[0] - 1000
        if self.background_pos[1] < 0:  # same
            other_background_pos[1] = self.background_pos[1] + 1000
        if self.background_pos[1] > 0:  # same
            other_background_pos[1] = self.background_pos[1] - 1000

        # blit all background
        screen.blit(self.backgrounds[0], self.background_pos)
        screen.blit(
            self.backgrounds[1], (other_background_pos[0], self.background_pos[1])
        )
        screen.blit(
            self.backgrounds[2], (self.background_pos[0], other_background_pos[1])
        )
        screen.blit(self.backgrounds[3], other_background_pos)

        self.player.blit()

        for i in self.bullets:
            i.blit()  # move all bullets

        for i in self.asteroids:
            i.blit(self.move)  # move all asteroids

        self.counter.blit()

        self.screen.blit(self.screen_surface, (0, 0))

        if mode == "AI":
            self.counter_time.update(
                round((time.time() - self.time) * self.speed_factor, 1)
            )
            self.counter_time.blit()
            self.counter_gen.update("Generation : " + str(self.generation))
            self.counter_gen.blit()
            self.counter_iteration.update("Iteration : " + str(self.iterations))
            self.counter_iteration.blit()
            self.ai.blit()

        pygame.display.update()  # update screen

    # Run function--------------------------------------------------------------------------------
    def run(self):

        while self.running:  # while running is true

            # run all function of game
            self.event()
            self.update()
            self.display()

            if self.speed_factor < 100:
                # set the game speed at 60 image per seconde
                self.clock.tick(60)

            self.x += 1

            if (time.time() - self.time) * self.speed_factor >= 60:
                if self.mode == "AI":
                    print(self.x)
                    return (
                        True,
                        time.time() - self.time,
                        self.counter.count,
                        self.speed_factor,
                        True,
                    )
            for contine in self.contine_list:
                if contine == True:
                    self.running = False
        if self.mode == "player":
            if self.main_running == False:
                return False
            else:
                return True
        elif self.mode == "AI":
            if self.main_running == False:
                print(self.x)
                return (
                    False,
                    time.time() - self.time,
                    self.counter.count,
                    self.speed_factor,
                    False,
                )
            else:
                print(self.x)
                return (
                    False,
                    time.time() - self.time,
                    self.counter.count,
                    self.speed_factor,
                    True,
                )


def main():

    play, speed_factor, mode, save = menu.Lunch_Menu(screen).run()

    if mode == "player":
        while play:
            Lose_Menu = Game(5, speed_factor, screen, 0, mode).run()

            if Lose_Menu == True:
                menu_lose = menu.Lose_Menu(screen)
                play = menu_lose.run()
            else:
                play = False

    if mode == "AI":

        iteration = 0
        nb_nn = 100
        neuronal_networks = []
        best_score = None
        if save != "":
            file = open(save, "r")
            gen = int(file.readline(1))
            variables = SaveScript.read(save)
            ai = AAI.Neuronal_Network(
                variables[0],
                variables[1],
                variables[2],
                screen,
                variables[3],
                variables[4],
                variables[5],
                variables[6],
            )
            neuronal_networks.append(ai)
            for i in range(nb_nn - 1):
                nn = AAI.Neuronal_Network(10, 5, 10, screen)
                nn.merge(neuronal_networks[0])
                neuronal_networks.append(nn)
        else:
            gen = 0
            for i in range(nb_nn):
                neuronal_networks.append(AAI.Neuronal_Network(10, 5, 10, screen))

        while play:
            result = []
            for nn in neuronal_networks:
                iteration += 1
                if best_score == None:
                    Lose_Menu, timer, count, speed_factor, play = Game(
                        5,
                        speed_factor,
                        screen,
                        iteration,
                        mode,
                        gen,
                        nn,
                        random.choice(neuronal_networks),
                    ).run()
                else:
                    Lose_Menu, timer, count, speed_factor, play = Game(
                        5,
                        speed_factor,
                        screen,
                        iteration,
                        mode,
                        gen,
                        nn,
                        neuronal_networks[best_score[1]],
                    ).run()
                if timer < 10:
                    result.append(0)
                else:
                    result.append(timer + count)
                if play == False:
                    break

            if play == True:
                best_score = (0, 0)
                for index in range(len(result)):
                    if result[index] > best_score[0]:
                        best_score = (result[index], index)

                for nn_index in range(len(neuronal_networks)):
                    if nn_index != best_score[1]:
                        neuronal_networks[nn_index].merge(
                            neuronal_networks[best_score[1]]
                        )

                gen += 1
                iteration = 0

    pygame.quit()
