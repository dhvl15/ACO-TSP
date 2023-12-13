from Ant import *
import numpy as np
import copy

class ACS(object):

    def __init__(self, num_ant=10, w_heuristic=2, w_pheromone_vapor=0.1, q0=0.9, p=0.1, max_gen=2500, city_name=""):
        self.m = num_ant  # Number of ants
        self.b = w_heuristic  # Heuristic information weight
        self.a = w_pheromone_vapor  # Pheromone evaporation factor
        self.t0 = 0.0  # Initial pheromone
        self.q0 = q0  # Pseudo-random factor
        self.p = p  # Local pheromone evaporation factor
        self.gen = max_gen  # Maximum generations

        self.ant = np.zeros(self.m, dtype=Ant)  # Ant colony
        self.best = Ant()  # Historical best ant
        self.city = City(city_name)  # City object
        self.dis_matrix = self.city.get_dis_matrix()  # Distance matrix
        self.num_city = self.city.num_city  # Number of cities
        self.pheromone_matrix = np.zeros((self.num_city, self.num_city), dtype=float)  # Pheromone matrix

    def init(self):
        # Initialize all ants
        for i in range(self.m):
            self.ant[i] = Ant()
            self.ant[i].path.resize(self.num_city)

        # Pheromone initialization (greedy selection of a road)
        seq = np.zeros(self.num_city, dtype=int)
        flag = np.zeros(self.num_city, dtype=int)
        seq[0] = np.random.randint(self.num_city)
        flag[seq[0]] = 1

        # Create an array for the information of the next city
        next_city = np.zeros(shape=self.num_city, dtype=NextCityInit)
        for i in range(self.num_city):
            next_city[i] = NextCityInit()

        # Greedy selection
        s = 0.0
        for i in range(self.num_city - 1):
            for j in range(self.num_city):
                next_city[j].dis = self.dis_matrix[seq[i]][j]
                next_city[j].id = j
            next_city.sort()
            for j in range(1, self.num_city):
                if flag[next_city[j].id] == 0:
                    seq[i + 1] = next_city[j].id
                    s = s + next_city[j].dis
                    flag[next_city[j].id] = 1
                    break
        s = s + self.dis_matrix[0][seq[self.num_city - 1]]

        # Calculate pheromones
        self.t0 = 1.0 / (self.num_city * s)
        for i in range(self.num_city):
            for j in range(self.num_city):
                self.pheromone_matrix[i][j] = self.t0

    def path_construct(self):
        # Calculate pheromone and heuristic information weights
        t = np.zeros((self.num_city, self.num_city), dtype=float)
        n = np.zeros((self.num_city, self.num_city), dtype=float)
        for j in range(self.num_city):
            for k in range(j + 1, self.num_city):
                t[j][k] = t[k][j] = np.power(self.pheromone_matrix[j][k], 1.0)
                n[j][k] = n[k][j] = np.power(1.0 / self.dis_matrix[j][k], self.b)

        # Construct paths for each ant
        for i in range(self.m):
            flag = np.zeros(self.num_city, dtype=bool)  # Record visited cities

            # Randomly select the starting city
            city_now = self.ant[i].path[0] = np.random.randint(0, self.num_city)
            flag[city_now] = 1

            # Select subsequent cities
            for j in range(self.num_city - 1):
                next_city = np.zeros(self.num_city, dtype=NextCityCons)
                for k in range(self.num_city):
                    next_city[k] = NextCityCons()
                    next_city[k].id = k
                    next_city[k].product = 0

                pp = np.random.random()  # Pseudo-random probability

                if pp < self.q0:  # Exploitation
                    for k in range(self.num_city):
                        if flag[k] == 0:
                            next_city[k].product = t[self.ant[i].path[j]][k] * n[self.ant[i].path[j]][k]
                    next_city.sort()
                    city_now = self.ant[i].path[j + 1] = next_city[0].id
                    flag[city_now] = 1

                    # Local update
                    self.pheromone_matrix[self.ant[i].path[j]][city_now] = \
                        self.pheromone_matrix[city_now][self.ant[i].path[j]] = \
                        (1 - self.p) * self.pheromone_matrix[self.ant[i].path[j]][city_now] + self.p * self.t0
                else:
                    p_sum = 0.0
                    p = np.zeros(self.num_city, dtype=float)

                    # Calculate sum
                    for k in range(self.num_city):
                        if flag[k] == 0:
                            p_sum = p_sum + t[self.ant[i].path[j]][k] * n[self.ant[i].path[j]][k]

                    # Calculate probabilities
                    for k in range(self.num_city):
                        if flag[k] == 0:
                            p[k] = (t[self.ant[i].path[j]][k] * n[self.ant[i].path[j]][k]) / p_sum

                    # Roulette wheel selection
                    rp = np.random.random()
                    rwsp = 0.0
                    for k in range(self.num_city):
                        if flag[k] == 0:
                            rwsp = rwsp + p[k]
                            if rwsp > rp:
                                city_now = self.ant[i].path[j + 1] = k
                                flag[city_now] = 1
                                break
                    # Local update
                    self.pheromone_matrix[self.ant[i].path[j]][city_now] = \
                        self.pheromone_matrix[city_now][self.ant[i].path[j]] = \
                        (1 - self.p) * self.pheromone_matrix[self.ant[i].path[j]][city_now] + self.p * self.t0

            # Local update for the last edge
            self.pheromone_matrix[self.ant[i].path[self.num_city - 1]][self.ant[i].path[0]] = \
                self.pheromone_matrix[self.ant[i].path[0]][self.ant[i].path[self.num_city - 1]] = \
                (1 - self.p) * \
                self.pheromone_matrix[self.ant[i].path[self.num_city - 1]][self.ant[i].path[0]] + \
                self.p * self.t0

    def pheromone_update(self):
        # Calculate the total distance for each ant
        for i in range(self.m):
            self.ant[i].dis = 0
            for j in range(self.num_city):
                if j != self.num_city - 1:
                    self.ant[i].dis = \
                        self.ant[i].dis + self.dis_matrix[self.ant[i].path[j]][self.ant[i].path[j + 1]]
                else:
                    self.ant[i].dis = \
                        self.ant[i].dis + self.dis_matrix[self.ant[i].path[j]][self.ant[i].path[0]]
        self.ant.sort()

        # Update the historical best ant
        if self.ant[0].dis < self.best.dis:
            self.best = copy.deepcopy(self.ant[0])
            print("New Optimal distance is ", self.best.dis)

        # Evaporate pheromones on all paths
        for i in range(self.num_city):
            for j in range(i, self.num_city):
                self.pheromone_matrix[j][i] = \
                    self.pheromone_matrix[i][j] = \
                    (1 - self.a) * self.pheromone_matrix[i][j]

        # Deposit pheromones on the paths of the historical best ant
        for i in range(self.num_city):
            if i != self.num_city - 1:
                self.pheromone_matrix[self.best.path[i]][self.best.path[i + 1]] = \
                    self.pheromone_matrix[self.best.path[i + 1]][self.best.path[i]] = \
                    self.pheromone_matrix[self.best.path[i]][self.best.path[i + 1]] + \
                    self.a * (1.0 / self.best.dis)
            else:
                self.pheromone_matrix[self.best.path[i]][self.best.path[0]] = \
                    self.pheromone_matrix[self.best.path[0]][self.best.path[i]] = \
                    self.pheromone_matrix[self.best.path[i]][self.best.path[0]] + \
                    self.a * (1.0 / self.best.dis)

# Auxiliary classes
class NextCityInit(object):
    def __init__(self):
        self.id = 0
        self.dis = 0.0

    def __lt__(self, other):
        return self.dis < other.dis

class NextCityCons(object):
    def __init__(self):
        self.id = 0
        self.product = 0.0

    def __lt__(self, other):
        return self.product > other.product
