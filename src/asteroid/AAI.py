import pygame
import random
import time
from .UIScript import Counter


class Enter_Neuron:

    def __init__(self, position, size, screen):
        self.screen = screen
        self.value = 0
        self.pos = position
        self.size = size
        self.points = [
            self.pos,
            (self.pos[0] + self.size, self.pos[1]),
            (self.pos[0] + self.size, self.pos[1] + self.size),
            (self.pos[0], self.pos[1] + self.size),
        ]

    def blit(self):
        if self.value == 0:
            self.color = (100, 100, 100, 200)
        if self.value == 1:
            self.color = (200, 200, 200, 200)
        pygame.draw.lines(self.screen, (255, 255, 255, 200), True, self.points)
        pygame.draw.rect(
            self.screen,
            self.color,
            pygame.Rect(self.pos[0] + 1, self.pos[1] + 1, self.size - 1, self.size - 1),
        )


class Normal_Neuron:

    def __init__(self, position, radius, screen, weight=None, connection=None):
        self.screen = screen
        self.pos = position
        self.radius = radius
        if weight != None:
            self.weight = weight
        else:
            self.weight = random.randint(-100, 100)
        if connection != None:
            self.connection = connection
        self.counter = Counter(0, self.pos, 24, self.screen)

    def create_connection(self, last_layer, draw_surface):
        self.connection = []
        for start_neuron in last_layer:
            if type(start_neuron) == Normal_Neuron:
                self.connection.append(
                    Connection(
                        (
                            start_neuron.pos[0] + start_neuron.radius,
                            start_neuron.pos[1],
                        ),
                        (self.pos[0] - self.radius, self.pos[1]),
                        start_neuron,
                        draw_surface,
                    )
                )
            if type(start_neuron) == Enter_Neuron:
                self.connection.append(
                    Connection(
                        (
                            start_neuron.pos[0] + start_neuron.size,
                            start_neuron.pos[1] + start_neuron.size // 2,
                        ),
                        (self.pos[0] - self.radius, self.pos[1]),
                        start_neuron,
                        draw_surface,
                    )
                )
        return self.connection

    def add_one_connection(self, start_neuron, draw_surface):
        if type(start_neuron) == Normal_Neuron:
            new_connection = Connection(
                (start_neuron.pos[0] + start_neuron.radius, start_neuron.pos[1]),
                (self.pos[0] - self.radius, self.pos[1]),
                start_neuron,
                draw_surface,
            )
        if type(start_neuron) == Enter_Neuron:
            new_connection = Connection(
                (
                    start_neuron.pos[0] + start_neuron.size,
                    start_neuron.pos[1] + start_neuron.size / 2,
                ),
                (self.pos[0] - self.radius, self.pos[1]),
                start_neuron,
                draw_surface,
            )
        self.connection.append(new_connection)
        return new_connection

    def get_value(self):
        self.value = 0
        for connection in self.connection:
            self.value += connection.start_neuron.value * connection.weight
        self.value += self.weight

    def blit(self):
        pygame.draw.circle(self.screen, (255, 255, 255, 100), self.pos, self.radius, 1)
        self.counter.update(self.value)
        self.counter.blit()


class Exit_Neuron:

    def __init__(self, position, radius, screen, connection=None):
        self.screen = screen
        self.pos = position
        self.radius = radius
        if connection != None:
            self.connection = connection
        self.counter = Counter(0, self.pos, 36, self.screen)

    def create_connection(self, last_layer, draw_surface):
        self.connection = []
        for start_neuron in last_layer:
            self.connection.append(
                Connection(
                    (start_neuron.pos[0] + start_neuron.radius, start_neuron.pos[1]),
                    (self.pos[0] - self.radius, self.pos[1]),
                    start_neuron,
                    draw_surface,
                )
            )
        return self.connection

    def add_one_connection(self, start_neuron, draw_surface):
        new_connection = Connection(
            (start_neuron.pos[0] + start_neuron.radius, start_neuron.pos[1]),
            (self.pos[0] - self.radius, self.pos[1]),
            start_neuron,
            draw_surface,
        )
        self.connection.append(new_connection)
        return new_connection

    def get_value(self):
        self.value = 0
        for connection in self.connection:
            self.value += connection.start_neuron.value * connection.weight

    def blit(self):
        pygame.draw.circle(self.screen, (255, 255, 255, 100), self.pos, self.radius, 1)
        if self.value >= 0.5:
            self.value = 1
        else:
            self.value = 0
        self.counter.update(self.value)
        self.counter.blit()


class Connection:

    def __init__(self, start_pos, end_pos, start_neuron, screen, weight=None):
        self.screen = screen
        self.start_neuron = start_neuron
        if weight != None:
            self.weight = weight
        else:
            self.weight = random.randint(-1000, 1000) / 100
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.transparency = abs(self.weight * 10)

    def blit(self):
        pygame.draw.line(
            self.screen,
            (255, 255, 255, self.transparency),
            self.start_pos,
            self.end_pos,
            1,
        )


class Neuronal_Network:

    def __init__(
        self,
        enter_neuron_size,
        normal_neuron_radius,
        exit_neuron_radius,
        screen,
        enter_neuron_values=None,
        normal_neuron_values=None,
        exit_neuron_values=None,
        connection_values=None,
    ):
        self.screen = screen
        self.draw_surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)
        self.enter_neuron_size = enter_neuron_size
        self.normal_neuron_radius = normal_neuron_radius
        self.exit_neuron_radius = exit_neuron_radius
        self.enter_neuron = []
        self.normal_neuron = []
        self.exit_neuron = []
        self.connection = []
        self.neuron = []
        if (
            enter_neuron_values != None
            and normal_neuron_values != None
            and exit_neuron_values != None
            and connection_values != None
        ):
            for enter_neuron in enter_neuron_values:
                enter_neuron = Enter_Neuron(
                    enter_neuron, self.enter_neuron_size, self.draw_surface
                )
                self.enter_neuron.append(enter_neuron)
                self.neuron.append(enter_neuron)

            for layer in range(len(normal_neuron_values)):
                normal_layer = []
                for neuron in normal_neuron_values[layer]:
                    connections = []
                    connection_to_create = neuron[2]
                    for nb in connection_to_create:
                        the_connection = Connection(
                            connection_values[nb][0],
                            connection_values[nb][1],
                            self.neuron[connection_values[nb][3]],
                            self.draw_surface,
                            connection_values[nb][2],
                        )
                        self.connection.append(the_connection)
                        connections.append(the_connection)
                    normal_neuron = Normal_Neuron(
                        neuron[0],
                        self.normal_neuron_radius,
                        self.draw_surface,
                        neuron[1],
                        connections,
                    )
                    normal_layer.append(normal_neuron)
                    self.neuron.append(normal_neuron)
                self.normal_neuron.append(normal_layer)

            for neuron in exit_neuron_values:
                connections = []
                connection_to_create = neuron[1]
                for nb in connection_to_create:
                    the_connection = Connection(
                        connection_values[nb][0],
                        connection_values[nb][1],
                        self.neuron[connection_values[nb][3]],
                        self.draw_surface,
                        connection_values[nb][2],
                    )
                    self.connection.append(the_connection)
                    connections.append(the_connection)
                self.exit_neuron.append(
                    Exit_Neuron(
                        neuron[0],
                        self.normal_neuron_radius,
                        self.draw_surface,
                        connections,
                    )
                )

        else:
            for column in range(10):
                for row in range(10):
                    self.enter_neuron.append(
                        Enter_Neuron(
                            (
                                row * self.enter_neuron_size + 20,
                                column * self.enter_neuron_size + 20,
                            ),
                            self.enter_neuron_size,
                            self.draw_surface,
                        )
                    )

            for layer in range(1):
                normal_layer = []
                for y in range(10):
                    normal_layer.append(
                        Normal_Neuron(
                            (
                                layer * (self.normal_neuron_radius * 2 + 50)
                                + self.enter_neuron_size * 10
                                + 80,
                                y * self.normal_neuron_radius * 2
                                + self.normal_neuron_radius
                                + 20,
                            ),
                            self.normal_neuron_radius,
                            self.draw_surface,
                        )
                    )
                self.normal_neuron.append(normal_layer)

            for y in range(5):
                self.exit_neuron.append(
                    Exit_Neuron(
                        (950, y * exit_neuron_radius * 2 + exit_neuron_radius + 20),
                        exit_neuron_radius,
                        self.draw_surface,
                    )
                )

            for i in self.normal_neuron:
                self.neuron.append(i)
            self.neuron.append(self.exit_neuron)
            for end_neuron_layer in range(len(self.neuron)):
                if end_neuron_layer == 0:
                    for end_neuron in self.neuron[end_neuron_layer]:
                        add_connection = end_neuron.create_connection(
                            self.enter_neuron, self.draw_surface
                        )
                        for connection in add_connection:
                            self.connection.append(connection)
                else:
                    for end_neuron in self.neuron[end_neuron_layer]:
                        add_connection = end_neuron.create_connection(
                            self.neuron[end_neuron_layer - 1], self.draw_surface
                        )
                        for connection in add_connection:
                            self.connection.append(connection)

    def update(self, value_box=None):
        for column in range(10):
            for row in range(10):
                index = str(row) + str(column)
                index = int(index)
                self.enter_neuron[index].value = value_box[row][column]
        for normal_neuron_layer in self.normal_neuron:
            for normal_neuron in normal_neuron_layer:
                normal_neuron.get_value()
        for exit_neuron in self.exit_neuron:
            exit_neuron.get_value()

    def blit(self):
        self.draw_surface.fill((0, 0, 0, 0))
        for connection in self.connection:
            connection.blit()
        for enter_neuron in self.enter_neuron:
            enter_neuron.blit()
        for normal_neuron_layer in self.normal_neuron:
            for normal_neuron in normal_neuron_layer:
                normal_neuron.blit()
        for exit_neuron in self.exit_neuron:
            exit_neuron.blit()
        self.screen.blit(self.draw_surface, (0, 0))

    def merge(self, best_NN):
        # modify normals neurons
        for normal_neuron_layer in range(len(self.normal_neuron)):
            for normal_neuron in self.normal_neuron[normal_neuron_layer]:
                if random.randint(0, 2) == 2:
                    if random.randint(0, 9) == 9:
                        connection_to_remove = []
                        for connection in self.connection:
                            if connection.start_neuron == normal_neuron:
                                connection_to_remove.append(connection)
                        for connection_remove in connection_to_remove:
                            for neuron2 in self.neuron[normal_neuron_layer + 1]:
                                for connection_in_neuron in neuron2.connection:
                                    if connection_in_neuron == connection_remove:
                                        neuron2.connection.remove(connection_remove)
                            self.connection.remove(connection_remove)
                            del connection_remove
                        self.normal_neuron[normal_neuron_layer].remove(normal_neuron)
                        del normal_neuron
                    else:
                        if random.randint(0, 1) == 1:
                            for normal_neuron_layer2 in best_NN.normal_neuron:
                                for normal_neuron2 in normal_neuron_layer2:
                                    if normal_neuron2.pos == normal_neuron.pos:
                                        normal_neuron.weight = normal_neuron2.weight
                        else:
                            normal_neuron.weight += random.randint(-10000, 10000)

        # modify connections
        for connection in self.connection:
            if random.randint(0, 1) == 1:
                if random.randint(0, 9) == 9:
                    self.connection.remove(connection)
                    del connection
                else:
                    if random.randint(0, 1) == 1:
                        # search the same connection in best NN
                        for connection2 in best_NN.connection:
                            if (
                                connection2.start_pos == connection.start_pos
                                and connection2.end_pos == connection.end_pos
                            ):
                                connection.weight = connection2.weight
                    else:
                        connection.weight = random.randint(-1000, 1000) / 100

        # add a new object
        for normal_neuron_layer in range(len(self.normal_neuron)):
            if random.randint(0, 1) == 1:
                y = 0
                # get a free position for new neuron
                for normal_neuron in self.normal_neuron[normal_neuron_layer]:
                    if (
                        normal_neuron.pos[1]
                        == y * self.normal_neuron_radius * 2
                        + self.normal_neuron_radius
                        + 20
                    ):
                        y += 1
                new_neuron = Normal_Neuron(
                    (
                        normal_neuron_layer * (self.normal_neuron_radius * 2 + 50)
                        + self.enter_neuron_size * 10
                        + 80,
                        y * self.normal_neuron_radius * 2
                        + self.normal_neuron_radius
                        + 20,
                    ),
                    self.normal_neuron_radius,
                    self.draw_surface,
                )
                # create the connection before the neuron
                if normal_neuron_layer == 0:
                    add_connection = new_neuron.create_connection(
                        self.enter_neuron, self.draw_surface
                    )
                    for connection in add_connection:
                        self.connection.append(connection)
                else:
                    add_connection = new_neuron.create_connection(
                        self.normal_neuron[normal_neuron_layer - 1], self.draw_surface
                    )
                    for connection in add_connection:
                        self.connection.append(connection)
                # add the neuron on list
                self.normal_neuron[normal_neuron_layer].append(new_neuron)
                # create the connection after the neuron
                for next_neuron in self.neuron[normal_neuron_layer + 1]:
                    self.connection.append(
                        next_neuron.add_one_connection(new_neuron, self.draw_surface)
                    )
            if random.randint(0, 1) == 1:
                # get if a place is free for a new connection
                for normal_neuron in self.normal_neuron[normal_neuron_layer]:
                    for connection in normal_neuron.connection:
                        is_connected = []
                        if normal_neuron_layer == 0:
                            for last_neuron in self.enter_neuron:
                                if connection.start_neuron == last_neuron:
                                    is_connected.append(last_neuron)
                                    break
                        else:
                            for last_neuron in self.normal_neuron[
                                normal_neuron_layer - 1
                            ]:
                                if connection.start_neuron == last_neuron:
                                    is_connected.append(last_neuron)
                    # if a place is free choice an randomly and create a new connection
                    if is_connected != []:
                        the_last_neuron = random.choice(is_connected)
                        self.connection.append(
                            normal_neuron.add_one_connection(
                                the_last_neuron, self.draw_surface
                            )
                        )

        if len(self.normal_neuron) < 10:
            if random.randint(0, 99) == 99:
                normal_layer = []
                layer = len(self.normal_neuron)
                for y in range(10):
                    new_neuron = Normal_Neuron(
                        (
                            layer * (self.normal_neuron_radius * 2 + 50)
                            + self.enter_neuron_size * 10
                            + 80,
                            y * self.normal_neuron_radius * 2
                            + self.normal_neuron_radius
                            + 20,
                        ),
                        self.normal_neuron_radius,
                        self.draw_surface,
                    )
                    add_connection = new_neuron.create_connection(
                        self.normal_neuron[layer - 1], self.draw_surface
                    )
                    for connection in add_connection:
                        self.connection.append(connection)
                    normal_layer.append(new_neuron)
                self.normal_neuron.append(normal_layer)
            self.neuron = []
            for i in self.normal_neuron:
                self.neuron.append(i)
            self.neuron.append(self.exit_neuron)


class Game:

    def __init__(self, neuronal_network, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.neuronal_network = neuronal_network
        self.epoch = time.time()
        self.x = 0
        self.image = 0

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, color_boxs):
        self.x += 1
        if self.epoch + 1 < time.time():
            self.image = self.x
            self.x = 0
            self.epoch = time.time()

    def display(self):
        self.screen.fill((0, 0, 0))
        self.neuronal_network.blit()
        Counter(self.image, (500, 500), 48, self.screen).blit()
        pygame.display.update()

    def run(self, color_box):

        while self.running == True:

            self.event()
            self.update(color_box)
            self.display()

            self.clock.tick(60)
