from random import randint

''' корабли здесь предствляются в следующем виде [длина, координата по x, координата по y,ориентация]'''


def is_correct_with_walls(n, k, sheep):  # проверка не пересекает ли корабль стенки поля
    if sheep[3] == 1:
        if sheep[1] + sheep[0] - 1 < k:
            return True
        return False
    else:
        if sheep[2] + sheep[0] - 1 < n:
            return True
        return False


def intersection(n, k, sheep1, sheep2):  # проверка перескаются ли два корабля
    s1 = [[sheep1[1] - 1, sheep1[2] - 1], [sheep1[1] - 1, sheep1[2]], [sheep1[1] - 1, sheep1[2] + 1],
          [sheep1[1], sheep1[2] - 1], [sheep1[1], sheep1[2] + 1], [sheep1[1] + 1, sheep1[2] - 1],
          [sheep1[1] + 1, sheep1[2]], [sheep1[1] + 1, sheep1[2] + 1]]
    if sheep1[3] == 1:
        s1.append([sheep1[1] + sheep1[0], sheep1[2] - 1])
        s1.append([sheep1[1] + sheep1[0], sheep1[2]])
        s1.append([sheep1[1] + sheep1[0], sheep1[2] + 1])
        for i in range(sheep1[0]):
            s1.append([sheep1[1] + i, sheep1[2]])
            s1.append([sheep1[1] + i, sheep1[2] + 1])
            s1.append([sheep1[1] + i, sheep1[2] - 1])

    if sheep1[3] == 0:
        s1.append([sheep1[1] - 1, sheep1[2] + sheep1[0]])
        s1.append([sheep1[1], sheep1[2] + sheep1[0]])
        s1.append([sheep1[1] + 1, sheep1[2] + sheep1[0]])
        for i in range(sheep1[0]):
            s1.append([sheep1[1], sheep1[2] + i])
            s1.append([sheep1[1] + 1, sheep1[2] + i])
            s1.append([sheep1[1] - 1, sheep1[2] + i])

    if sheep2[3] == 1:
        for i in range(sheep2[0]):
            if [sheep2[1] + i, sheep2[2]] in s1:
                return True
    if sheep2[3] == 0:
        for i in range(sheep2[0]):
            if [sheep2[1], sheep2[2] + i] in s1:
                return True

    return False


def is_correct(n, k, plcmnt, new_sheep):  # проверка не пересекает ли корабль какой-нибудь из предыдущих кораблей
    if not is_correct_with_walls(n, k, new_sheep):
        return False

    for sheep in plcmnt:
        if intersection(n, k, sheep, new_sheep):
            return False
    return True


def placement_of_ship(n, k, m):  # функция генерации корабля
    plcmnt = []
    size_of_sheep = 1
    cnt_of_sheep_with_this_size = 0
    for i in range(0, int((m * (m + 1)) / 2)):
        plcmnt.append([size_of_sheep, 0, 0, 0])
        cnt_of_sheep_with_this_size += 1
        if cnt_of_sheep_with_this_size == m - size_of_sheep + 1:
            size_of_sheep += 1
            cnt_of_sheep_with_this_size = 0

    plcmnt.reverse()

    kol_of_sheeps = int(((m * (m + 1)) / 2))
    keys = [[]] * kol_of_sheeps
    random_mod = [[randint(0, 100), randint(0, 100), randint(0, 1)] for _ in
                  range(kol_of_sheeps)]

    answer = []
    cnt = 0

    while cnt < kol_of_sheeps:
        flag = False
        for i in range(k):
            for j in range(n):
                r = 0
                for z in range(2):
                    if z == 0:
                        r = random_mod[cnt][2]
                    else:
                        r += 1
                    i1 = (i + random_mod[cnt][0]) % k
                    j1 = (j + random_mod[cnt][1]) % n
                    z1 = (z + r) % 2

                    if i1 * 100000 + j1 * 100 + z1 in keys[cnt]:
                        continue  # если мы уже пытались поставить корабль с такими координатами в предыдущей расстановке от которой снова вернулись
                    plcmnt[cnt][1] = i1
                    plcmnt[cnt][2] = j1
                    plcmnt[cnt][3] = z1
                    new_sheep = plcmnt[cnt]

                    if is_correct(n, k, answer, new_sheep):
                        flag = True
                        keys[cnt].append(i1 * 100000 + j1 * 100 + z1)
                        answer.append(new_sheep)
                        break
                if flag:
                    break
            if flag:
                break
        if not flag:
            keys[
                cnt] = []  # обнуляем ключ, если никак не получилось поставить новый корабль (пробуем переставить предыдущие)
            if cnt > 0:
                cnt -= 1
            answer.pop()
            continue
        cnt += 1
    return answer
