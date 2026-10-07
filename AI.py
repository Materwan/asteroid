import random
import math

class ai:

    def __init__(self, point, exploration_rate, x_player, y_player, learning_rate, discount_factor):
        self.Q_table = {}
        self.asteroid_distance_A0 = []
        self.asteroid_distance_A1 = []
        self.asteroid_distance = []
        self.lowest_distance = float()
        self.lowest_distance_A0 = float()
        self.lowest_distance_A1 = float()
        self.point = point
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.S = (x_player, y_player)
        self.possible_A = [0, 1, 2]
        self.reward = 0
        self.fire = False
        for A in self.possible_A:
            self.Q_table[A] = {self.S: 0}
    
    def get_Q_value(self, point, y_ammo):
        for A in range(3):
            if A == 0:
                if self.S[0] < 0:
                    self.Q_table[A][self.S] = -1000
                    break
                else:
                    self.Q_table[A][self.S] = self.Q_table[A][self.S] + self.learning_rate * (self.get_reward(point) + self.discount_factor * self.lowest_distance_A0 - self.Q_table[A][self.S])
            elif A == 1:
                if self.S[0] > 750:
                    self.Q_table[A][self.S] = -1000
                    continue
                else:
                    self.Q_table[A][self.S] = self.Q_table[A][self.S] + self.learning_rate * (self.get_reward(point) + self.discount_factor * self.lowest_distance_A1 - self.Q_table[A][self.S])
            elif A == 2:
                if y_ammo < 0:
                    if self.fire == True:
                        self.Q_table[A][self.S] = self.Q_table[A][self.S] + self.learning_rate * (self.get_reward(point) + self.discount_factor * 1000 - self.Q_table[A][self.S])
                    else:
                        self.Q_table[A][self.S] = self.Q_table[A][self.S] + self.learning_rate * (self.get_reward(point) - self.discount_factor * 1000 - self.Q_table[A][self.S])
                else:
                    self.Q_table[A][self.S] = self.Q_table[A][self.S] + self.learning_rate * (self.get_reward(point) - self.discount_factor * 1000 - self.Q_table[A][self.S])
        return self.Q_table
    
    def choose_A(self):
        if random.random() < self.exploration_rate:
            best_Q = random.choice(list(self.possible_A))
        else:
            max_value = max(max(d.values()) for d in self.Q_table.values())
            max_keys = [key for key, value_dict in self.Q_table.items() for state, value in value_dict.items() if value == max_value]
            best_Q = max_keys[0] if max_keys else random.choice(list(self.possible_A))
        return best_Q
    
    def get_distance(self, x_asteroid, y_asteroid):
        self.asteroid_distance.append(math.sqrt(abs(self.S[0] - x_asteroid)**2 + abs(self.S[1] - y_asteroid)**2))
        self.asteroid_distance_A0.append(math.sqrt(abs(self.S[0] - 0.1 - x_asteroid)**2 + abs(self.S[1] - y_asteroid)**2))
        self.asteroid_distance_A1.append(math.sqrt(abs(self.S[0] + 0.1 - x_asteroid)**2 + abs(self.S[1] - y_asteroid)**2))
    
    def get_axis(self, x_asteroid):
        if (x_asteroid + 10) < (self.S[0] + 25) < (x_asteroid + 40):
            self.fire = True
        return self.fire
    
    def get_lowest_distance(self):
        self.lowest_distance = min(self.asteroid_distance)
        self.lowest_distance_A0 = min(self.asteroid_distance_A0)
        self.lowest_distance_A1 = min(self.asteroid_distance_A1)
    
    def get_reward(self, point):
        if self.point < point:
            self.reward =+ 500
        else:
            self.reward = -1000 + self.lowest_distance
        return self.reward