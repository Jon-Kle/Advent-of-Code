
with open('pi8.txt') as f:
    rows = f.read().split('\n')

forest = []
for i, r in enumerate(rows):
    forest.append([])
    for c in r:
        forest[i].append(int(c))

visible = set()

for column in range(len(forest[0])):
    # fly along north
    row = 0
    height = -1
    while row < len(forest):
        if forest[row][column] > height:
            height = forest[row][column]
            visible.add((row, column))
        row += 1
    # fly along south
    height = -1
    row -= 1
    while row >= 0:
        if forest[row][column] > height:
            height = forest[row][column]
            visible.add((row, column))
        row -= 1

for row in range(len(forest)):
    # fly along west
    column = 0
    height = -1
    while column < len(forest[0]):
        if forest[row][column] > height:
            height = forest[row][column]
            visible.add((row, column))
        column += 1
    # fly along east
    height = -1
    column -= 1
    while column >= 0:
        if forest[row][column] > height:
            height = forest[row][column]
            visible.add((row, column))
        column -= 1

print(f'visible trees from the edges: {len(visible)}')

# part 2
scenic_score = []
for row, c in enumerate(forest):
    scenic_score.append([])
    for column, tree in enumerate(c):
        ...
        # look down
        v_dist_down = 0
        x = row + 1
        while x < len(forest):
            if forest[x][column] >= tree:
                v_dist_down += 1
                break
            else:
                v_dist_down += 1
            x += 1
        # look up
        v_dist_up = 0
        x = row - 1
        while x >= 0:
            if forest[x][column] >= tree:
                v_dist_up += 1
                break
            else:
                v_dist_up += 1
            x -= 1
        # look right
        v_dist_right = 0
        y = column + 1
        while y < len(c):
            if forest[row][y] >= tree:
                v_dist_right += 1
                break
            else:
                v_dist_right += 1
            y += 1
        # look left
        v_dist_left = 0
        y = column -1
        while y >= 0:
            if forest[row][y] >= tree:
                v_dist_left += 1
                break
            else:
                v_dist_left += 1
            y -= 1
        # calculate scenic_score
        scenic_score[row].append(v_dist_down * v_dist_up * v_dist_right * v_dist_left)

maximum = 0
for r in scenic_score:
    for c in r:
        if c > maximum:
            maximum = c

print(f'max scenic score: {maximum}')