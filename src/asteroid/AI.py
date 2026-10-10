import pygame
import Neural_network
import random

pygame.init()


class AI:

    def __init__(self, screen_surface, neuronal_network=None):

        self.box_size = 10
        self.neuron_size = 10
        self.screen_surface = screen_surface
        self.running = True
        self.draw_surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)
        self.connection = []
        self.neuron_layers = []
        self.all_neuron = []

        if neuronal_network == None:
            # create the exit neuron
            exit_neuron_layer = {}
            exit_neurons = []
            for y in range(5):
                exit_neuron = Neural_network.Exit_Neuron(
                    self.screen_surface,
                    (500, 50 + (y * self.neuron_size * 2)),
                    self.neuron_size,
                )
                exit_neuron_layer[
                    (exit_neuron.pos[0] - exit_neuron.neuron_size, exit_neuron.pos[1])
                ] = exit_neuron
                exit_neurons.append(exit_neuron)
            self.neuron_layers.append(exit_neuron_layer)
            self.all_neuron.append(exit_neurons)
            del exit_neuron_layer

            neuron_layer = {}
            neurons = []
            # create an layer of neuron
            for y in range(10):
                neuron = Neural_network.Neuron(
                    [300, 10 + (y * self.neuron_size * 2)],
                    self.neuron_size,
                    self.neuron_layers,
                    self.draw_surface,
                    self.screen_surface,
                )  # create a neuron
                self.connection.append(list(neuron.connection))
                neuron_layer[(neuron.pos[0] - neuron.neuron_size, neuron.pos[1])] = (
                    neuron  # save the neuron in a dict with his number
                )
                neurons.append(neuron)  # save the neuron in a list for
            self.neuron_layers.append(neuron_layer)
            self.all_neuron.append(neurons)
            del neuron_layer

            # create the enter neuron
            enter_neurons = []
            neuron_pos = [0, 50]
            for column in range(10):
                neuron_pos[1] += self.box_size + 1
                neuron_pos[0] = 0
                for row in range(10):
                    neuron_pos[0] += self.box_size + 1
                    enter_neuron = Neural_network.Enter_Neuron(
                        self.screen_surface,
                        (neuron_pos[0], neuron_pos[1]),
                        self.box_size,
                        self.neuron_layers,
                        self.draw_surface,
                    )
                    self.connection.append(list(enter_neuron.connection))
                    enter_neurons.append(enter_neuron)
            self.all_neuron.append(enter_neurons)
        else:
            self.all_neuron = neuronal_network
            for layer in self.all_neuron:
                for neuron in layer:
                    if layer != self.all_neuron[0]:
                        for connection in neuron.connection:
                            connection.draw_surface = self.draw_surface
                        self.connection.append(neuron.connection)
                    neuron.screen = self.screen_surface
                    neuron.draw_surface = self.draw_surface

    def create_neuron(self, neuronal_network, layer):
        for position in range(10):
            position_check = [position * self.neuron_size * 2]
            neurons_pos = []
            for neuron in neuronal_network[layer]:
                neuron_pos = neuron.pos
                neurons_pos.append(neuron_pos)
            if all(item in neurons_pos for item in position_check) == False:
                neuron = Neural_network.Neuron(
                    (300, position * self.neuron_size * 2),
                    self.neuron_size,
                    self.neuron_layers,
                    self.draw_surface,
                    self.screen_surface,
                )
                neuronal_network[layer].append(neuron)
                break
            else:
                break
        return neuronal_network

    def update(self, value_box):
        # set the value of enter neuron
        for column in range(10):
            for row in range(10):
                self.all_neuron[-1][column * 10 + row].value = value_box[column][row]
        # calculate the value of all neuron exept enter because our value isn't calculate
        for layer_index in range(len(self.all_neuron)):
            layer = self.all_neuron[len(self.all_neuron) - layer_index - 1]
            if layer != self.all_neuron[0]:
                for neuron in layer:
                    neuron.get_value()
        # get the value of exit neuron and return it
        exit_neuron_value = []
        for neuron in self.all_neuron[0]:
            exit_neuron_value.append(neuron.value)
        return exit_neuron_value

    def display(self):

        self.screen_surface.fill((255, 255, 255, 0))

        # blit the line between enter neuron
        for i in range(11):
            origin_pos = 50
            self.box_size = 11
            pygame.draw.line(
                self.screen_surface,
                (255, 255, 255),
                (i * self.box_size + self.box_size - 1, self.box_size - 1 + origin_pos),
                (
                    i * self.box_size + self.box_size - 1,
                    self.box_size * 10 + self.box_size - 1 + origin_pos,
                ),
                1,
            )
            pygame.draw.line(
                self.screen_surface,
                (255, 255, 255),
                (self.box_size - 1, i * self.box_size + self.box_size - 1 + origin_pos),
                (
                    self.box_size * 10 + self.box_size - 1,
                    i * self.box_size + self.box_size - 1 + origin_pos,
                ),
                1,
            )
        # blit all neurons
        for neuron_layer in self.all_neuron:
            for neuron in neuron_layer:
                neuron.blit()
                if neuron_layer != self.all_neuron[-1]:
                    neuron.value = 0
        # blit all connections on connection surface
        for neuron in self.connection:
            for connection in neuron:
                self.draw_surface = connection.blit()
        # blit the connection on the AI surface
        self.screen_surface.blit(self.draw_surface, (0, 0))

        pygame.display.update()

    def run(self, value_box):

        exit_neuron_value = self.update(value_box)
        self.display()

        return self.screen_surface, exit_neuron_value
