import AAI
import pygame
import random

"""screen = pygame.display.set_mode((1000, 1000))
neuronal_network = AAI.Neuronal_Network(10, 5, 10, screen)"""

def save_nn(file_path, gen, neuronal_network):
    file = open(file_path, "w")
    file.writelines([str(gen), "/n"])
    file.writelines([str(neuronal_network.enter_neuron_size), "/n"])
    file.writelines([str(neuronal_network.normal_neuron_radius), "/n"])
    file.writelines([str(neuronal_network.exit_neuron_radius), "/n"])
    #Enters Neurons
    for enter_neuron in neuronal_network.enter_neuron:
        file.writelines(["Enter Neuron/n"])
        for i in range(2):
            file.writelines([str(enter_neuron.pos[i]), "/n"])
    #Normals Neurons
    for normal_neuron_layer in neuronal_network.normal_neuron:
        file.writelines(["Normal Layer/n"])
        for normal_neuron in normal_neuron_layer:
            file.writelines(["Normal Neuron/n"])
            for i in range(2):
                file.writelines([str(normal_neuron.pos[i]), "/n"])
            file.writelines([str(normal_neuron.weight), "/n"])
            for connection in normal_neuron.connection:
                for connection_index in range(len(neuronal_network.connection)):
                    if connection == neuronal_network.connection[connection_index]:
                        file.writelines([str(connection_index), "/n"])
    #Exits Neurons
    for exit_neuron in neuronal_network.exit_neuron:
        file.writelines(["Exit Neuron/n"])
        for i in range(2):
            file.writelines([str(exit_neuron.pos[i]), "/n"])
        for connection in exit_neuron.connection:
            for connection_index in range(len(neuronal_network.connection)):
                if connection == neuronal_network.connection[connection_index]:
                    file.writelines([str(connection_index), "/n"])
    #Connections
    all_neuron = []
    for neuron in neuronal_network.enter_neuron:
        all_neuron.append(neuron)
    for neuron_layer in neuronal_network.normal_neuron:
        for neuron in neuron_layer:
            all_neuron.append(neuron)
    for connection in neuronal_network.connection:
        file.writelines(["Connection/n"])
        for i in range(2):
            file.writelines([str(connection.start_pos[i]), "/n"])
        for i in range(2):
            file.writelines([str(connection.end_pos[i]), "/n"])
        file.writelines([str(connection.weight), "/n"])
        g = False
        for neuron_index in range(len(all_neuron)):
            if connection.start_neuron == all_neuron[neuron_index]:
                file.writelines([str(neuron_index), "/n"])
                g = True
        if g == False:
            file.writelines([str(-100000000000000000000000000000000000), "/n"])
    file.close
    return all_neuron

def read(save_file):
    file = open(save_file, "r")
    lines = file.readlines()
    enter_neuron_values = []
    normal_neuron_values = []
    exit_neuron_values = []
    connection_values = []
    for line in range(len(lines)):
        enter_neuron_size = int(lines[0])
        normal_neuron_radius = int(lines[1])
        exit_neuron_radius = int(lines[2])
        if lines[line] == "Enter Neuron/n":
            enter_neuron_values.append((int(lines[line + 1]), int(lines[line + 2])))
        if lines[line] == "Normal Layer/n":
            the_line = line + 1
            normal_layer = []
            while lines[the_line] != "Normal Layer/n" and lines[the_line] != "Exit Neuron/n":
                i = the_line + 4
                normal_neuron_connection = []
                while lines[i] != "Normal Neuron/n" and lines[i] != "Normal Layer/n" and lines[i] != "Exit Neuron/n":
                    normal_neuron_connection.append(int(lines[i]))
                    i += 1
                normal_layer.append([(int(lines[the_line + 1]), int(lines[the_line + 2])), int(lines[the_line + 3]), normal_neuron_connection])
                the_line += i - the_line
            normal_neuron_values.append(normal_layer)
        if lines[line] == "Exit Neuron/n":
            exit_neuron_connections = []
            i = line + 3
            while lines[i] != "Exit Neuron/n" and lines[i] != "Connection/n":
                exit_neuron_connections.append(int(lines[i]))
                i += 1
            exit_neuron_values.append([(int(lines[line + 1]), int(lines[line + 2])), exit_neuron_connections])
        if lines[line] == "Connection/n":
            connection_values.append([(int(lines[line + 1]), int(lines[line + 2])), (int(lines[line + 3]), int(lines[line + 4])), float(lines[line + 5]), int(lines[line + 6])])
    return [enter_neuron_size,
            normal_neuron_radius,
            exit_neuron_radius,
            enter_neuron_values,
            normal_neuron_values,
            exit_neuron_values,
            connection_values]

"""colors = []
for i in range(1000):
    the_color = []
    for column in range(10):
        the_row = []
        for row in range(10):
            the_row.append(random.randint(0, 1))
        the_color.append(the_row)
    colors.append(the_color)

game = AAI.Game(neuronal_network, screen)
values1 = game.run(colors)

neuronal_network2 = AAI.Neuronal_Network(10, 5, 10, screen, enter_neuron_values, normal_neuron_values, exit_neuron_values, connection_values)
if neuronal_network == neuronal_network2:
    print(True)
else:
    print(False)
game = AAI.Game(neuronal_network2, screen)
values2 = game.run(colors)

print(values1, values2)

if values1 == values2:
    print(True)
else:
    print(False)"""