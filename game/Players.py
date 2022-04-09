from random import randint


class Players(object):       #класс хранящий территории игроков, обработку выстрелов
 
    def __init__(self, n, k, m, sheeps):
        self.n = n
        self.k = k
        self.m = m
        self.sheeps = sheeps
        self.enemy_field = [[0 for _ in range(self.n)] for _ in range(self.k)]   #территория врага куда еще не стреляли
        self.lively_territory = self.all_territory()
        self.shots = []                                #список сделанных выстрелов
        self.square = len(self.all_territory())

    def all_territory(self):
        data = []
        for sheep in self.sheeps:
            if sheep[3] == 1:
                for i in range(sheep[0]):
                    data.append([sheep[1] + i, sheep[2]])
            else:
                for i in range(sheep[0]):
                    data.append([sheep[1], sheep[2] + i])
        return data

    def shot_in(self, x, y):
        if [x, y] in self.lively_territory:       #попадание
            self.lively_territory.remove([x, y])
            self.shots.append([x,y,1])
            return True
        else:
            if not [x,y,1] in self.shots:
                self.shots.append([x, y, 0])
            return False

    def shot_out(self):        #используется только объектом computer , генерирует координаты нового стрела
        x = randint(0, self.k)
        y = randint(0, self.n)
        for i in range(self.k):
            for j in range(self.n):
                if self.enemy_field[(x + i) % self.k][(y + j) % self.n] == 0:
                    self.enemy_field[(x + i) % self.k][(y + j) % self.n] = 1
                    return [(x + i) % self.k,(y + j) % self.n]
