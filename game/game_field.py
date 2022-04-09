from Players import Players
from placement import placement_of_ship


class Field(object):

    def __init__(self, n, k, m):
        self.n = n
        self.k = k
        self.m = m
        self.list_of_player_sheep = placement_of_ship(self.n, self.k, self.m)  # генерируем корабли
        self.list_of_computer_sheep = placement_of_ship(self.n, self.k, self.m)

        self.player = Players(self.n, self.k, self.m, self.list_of_player_sheep)
        self.computer = Players(self.n, self.k, self.m, self.list_of_computer_sheep)

    def update_generation(self):  # обновляет генерации полей
        self.list_of_player_sheep = placement_of_ship(self.n, self.k, self.m)
        self.list_of_computer_sheep = placement_of_ship(self.n, self.k, self.m)
        self.player = Players(self.n, self.k, self.m, self.list_of_player_sheep)
        self.computer = Players(self.n, self.k, self.m, self.list_of_computer_sheep)

    def coordinates(self, width_of_window):
        padding_x = int((width_of_window / 2 - self.k * 2) / 2)
        padding_y = 3
        dx = int(width_of_window / 2)

        data = []
        for i in range(0, self.k + 2):
            data.append([padding_x + i * 2, padding_y, "# "])
            data.append([padding_x + i * 2, padding_y + self.n + 1, "# "])
            data.append([padding_x + dx + i * 2, padding_y, "# "])
            data.append([padding_x + dx + i * 2, padding_y + self.n + 1, "# "])
        for i in range(0, self.n + 2):
            data.append([padding_x  , padding_y + i, "#"])
            data.append([padding_x  + self.k * 2 + 2, padding_y + i, "#"])
            data.append([padding_x + dx, padding_y + i, "#"])
            data.append([padding_x + dx + self.k * 2 + 2, padding_y + i, "#"])

        return data

    def sheep_coordinates(self, width_of_window):
        padding_x = int((width_of_window / 2 - self.k * 2) / 2) + 2
        padding_y = 3

        sheeps = self.list_of_player_sheep
        data = []
        for sheep in sheeps:
            if sheep[3] == 1:
                for i in range(sheep[0]):
                    data.append([padding_x + sheep[1] * 2 + i * 2, padding_y + sheep[2] + 1, "■ "])
            else:
                for i in range(sheep[0]):
                    data.append([padding_x + sheep[1] * 2, padding_y + sheep[2] + i + 1, "■ "])
        return data

    def computer_sheeps_coordinates(self, width_of_window):
        padding_x = int((width_of_window / 2 - self.k * 2) / 2) + 2
        padding_y = 3
        data = []
        sheeps = self.list_of_computer_sheep
        for sheep in sheeps:
            if sheep[3] == 1:
                for i in range(sheep[0]):
                    data.append(
                        [padding_x + sheep[1] * 2 + i * 2 + int(width_of_window / 2), padding_y + sheep[2] + 1, "■ "])
            else:
                for i in range(sheep[0]):
                    data.append(
                        [padding_x + sheep[1] * 2 + int(width_of_window / 2), padding_y + sheep[2] + i + 1, "■ "])
        return data

    def shots_coordinates(self, width_of_window):
        padding_x = int((width_of_window / 2 - self.k * 2) / 2) + 2
        padding_y = 3
        data = []
        for st in self.player.shots:
            if st[2] == 1:
                data.append([st[0] * 2 + padding_x, st[1] + padding_y + 1, 'X'])
            else:
                data.append([st[0] * 2 + padding_x, st[1] + padding_y + 1, '.'])

        return data

    def computer_shots_coordinates(self, width_of_window):
        padding_x = int((width_of_window / 2 - self.k * 2) / 2) + 2
        padding_y = 3
        data = []
        for st in self.computer.shots:
            if st[2] == 1:
                data.append([st[0] * 2 + padding_x + int(width_of_window / 2), st[1] + padding_y + 1, 'X'])
            else:
                data.append([st[0] * 2 + padding_x + int(width_of_window / 2), st[1] + padding_y + 1, '.'])

        return data

    def correction_of_fire(self, width_of_window, impact_x, impact_y):
        padding_x = int((width_of_window / 2 - self.k * 2) / 2) + 2
        padding_y = 3
        data = [[padding_x + impact_x * 2 + int(width_of_window / 2), padding_y - 1, 'V'],
                [padding_x + int(width_of_window / 2) - 3, padding_y + impact_y + 1, '>']]
        return data
