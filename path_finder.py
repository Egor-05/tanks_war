def found(pathArr, finPoint):
    weight = 1
    for i in range(len(pathArr) * len(pathArr[0])):
        weight += 1
        for y in range(len(pathArr)):
            for x in range(len(pathArr[y])):
                if pathArr[y][x] == (weight - 1):
                    if y > 0 and pathArr[y - 1][x] == 0:
                        pathArr[y - 1][x] = weight
                    if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                        pathArr[y + 1][x] = weight
                    if x > 0 and pathArr[y][x - 1] == 0:
                        pathArr[y][x - 1] = weight
                    if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                        pathArr[y][x + 1] = weight

                    if (abs(y - finPoint[0]) + abs(x - finPoint[1])) == 1:
                        pathArr[finPoint[0]][finPoint[1]] = weight
                        return True
    return False


def printPath(pathArr, finPoint):
    y = finPoint[0]
    x = finPoint[1]
    weight = pathArr[y][x]
    result = list(range(weight))
    point = list(finPoint)
    while weight:
        weight -= 1
        if y > 0 and pathArr[y - 1][x] == weight:
            y -= 1
            point[0] -= 1
            result[weight] = (point[0], point[1])
        elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
            y += 1
            point[0] += 1
            result[weight] = (point[0], point[1])
        elif x > 0 and pathArr[y][x - 1] == weight:
            x -= 1
            point[1] -= 1
            result[weight] = (point[0], point[1])
        elif x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == weight:
            x += 1
            point[1] += 1
            result[weight] = (point[0], point[1])
    return result[1:]


def main(field, posIn, posOut):
    labirint = [[1 if field[i][j] == '#' else 0 for j in range(len(field[i]))] for i in range(len(field))]
    path = [[x if x == 0 else -1 for x in y] for y in labirint]
    path[posIn[0]][posIn[1]] = 1

    if not found(path, posOut):
        print("Путь не найден!")
        return

    result = printPath(path, posOut)
    return [i[::-1] for i in result]

