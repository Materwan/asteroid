import pygame
import random
from .UIScript import Counter


# Neuron class--------------------------------------------------------------------------------------------------------------
class Neuron:
    def __init__(self, position, neuron_size, neuron_layers, draw_surface, screen):
        self.screen = screen
        self.pos = position
        self.weight = random.randint(-100, 100)
        self.value = 0
        self.draw_surface = draw_surface
        self.neuron_connect = []
        self.connection = []
        self.neuron_size = neuron_size
        # create a random number of connection between random neuron
        for y in range(len(neuron_layers)):
            neuron_layer = neuron_layers[y]
            for i in range(random.randint(1, len(neuron_layer))):
                self.create_connection(neuron_layer)

    def create_connection(self, neuron_layer):
        neuron_connect = random.choice(list(neuron_layer.keys()))
        connection = Connection(
            (self.pos[0] + self.neuron_size, self.pos[1] + (self.neuron_size / 2)),
            neuron_connect,
            self.screen,
            self.draw_surface,
            neuron_layer[neuron_connect],
        )
        for connection_index in range(len(self.connection)):
            # verify if the connection already exist
            if connection == self.connection[connection_index]:
                # and delete it if is true
                del connection
        self.connection.append(connection)

    def reset(self, ai, layer):
        self.weight = random.randint(-100, 100)
        self.value = 0
        self.connection = []
        for y in range(len(ai.neuron_layers) - layer):
            neuron_layer = ai.neuron_layers[y]
            for i in range(random.randint(1, len(neuron_layer))):
                self.create_connection(neuron_layer)

    def get_value(self):
        # calcule the value of all neuron how are connection with the actual
        self.value += self.weight
        for connection in self.connection:
            connection.neuron.value += self.value * connection.value

    def blit(self):
        # blit the neuron with his weight
        pygame.draw.circle(self.screen, (255, 255, 255), self.pos, self.neuron_size, 1)
        Counter(self.weight, self.pos, 24, self.screen, (0, 0, 0)).blit()


# Enter Neuron class---------------------------------------------------------------------------------------------------------
class Enter_Neuron:

    def __init__(self, screen, position, size_box, neuron_layers, draw_surface):
        self.screen = screen
        self.size_box = size_box
        self.pos = position
        self.value = 0
        self.neuron_connect = []
        self.connection = []
        self.draw_surface = draw_surface
        # same as Neuron class
        for y in range(len(neuron_layers)):
            neuron_layer = neuron_layers[y]
            for i in range(random.randint(1, len(neuron_layer))):
                self.create_connection(neuron_layer)

    def create_connection(self, neuron_layer):
        neuron_connect = random.choice(list(neuron_layer.keys()))
        connection = Connection(
            (self.pos[0] + self.size_box, self.pos[1] + (self.size_box / 2)),
            neuron_connect,
            self.screen,
            self.draw_surface,
            neuron_layer[neuron_connect],
        )
        for connection_index in range(len(self.connection)):
            # verify if the connection already exist
            if connection == self.connection[connection_index]:
                # and delete it if is true
                del connection
        self.connection.append(connection)

    def get_value(self):
        # same as Neuron class
        for connection in self.connection:
            connection.neuron.value += self.value * connection.value

    def blit(self):
        # set the color in function of his value and blit the neuron
        if self.value == 1:
            self.color = (100, 100, 100)
        elif self.value == 0:
            self.color = (200, 200, 200)
        pygame.draw.rect(
            self.screen,
            self.color,
            pygame.Rect(self.pos[0], self.pos[1], self.size_box, self.size_box),
        )


# Exit Neuron class---------------------------------------------------------------------------------------
class Exit_Neuron:
    def __init__(self, screen, position, neuron_size):
        self.screen = screen
        self.pos = position
        self.value = 0
        self.neuron_size = neuron_size
        self.connection_pos = self.pos[0] - self.neuron_size

    def blit(self):
        # set the value at 0 or 1
        if self.value >= 0.5:
            self.value = 1
        else:
            self.value = 0
        # blit neuron and value
        pygame.draw.circle(self.screen, (255, 255, 255), self.pos, self.neuron_size, 1)
        Counter(self.value, self.pos, 24, self.screen, (0, 0, 0)).blit()


# Connection class-----------------------------------------------------------------------------------------
class Connection:

    def __init__(self, start_pos, end_pos, screen, draw_surface, neuron):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.neuron = neuron
        # set the value of connection between -10 and 10
        self.value = random.randint(-10000, 10000) / 1000
        self.color = (255, 255, 255, abs(self.value) * 10)
        self.draw_surface = draw_surface
        self.screen = screen

    def blit(self):
        # blit connection on connection surface
        pygame.draw.line(self.draw_surface, self.color, self.start_pos, self.end_pos, 1)
        return self.draw_surface
