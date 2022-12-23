
with open('pi9.txt') as f:
    lines = f.read().splitlines()

rope_length = 10
rope = []
for i in range(rope_length):
    rope.append([0, 0])
visited = set()

for l in lines:
    direction = l[0]
    count = int(l[2:])
    x_dif, y_dif = 0, 0 # x+ -> right; y+ -> up
    match direction:
        case 'R':
            x_dif = 1
        case 'L':
            x_dif = -1
        case 'U':
            y_dif = 1
        case 'D':
            y_dif = -1
    # print(f'line: {l}')
    for i in range(count):
        rope[0][0] += x_dif
        rope[0][1] += y_dif
        # print(f'move {i}')

        #update snake body
        j = 1
        while j < len(rope):
            x_stretch = rope[j-1][0] - rope[j][0]
            y_stretch = rope[j-1][1] - rope[j][1]
            # print(f'x_stretch: {x_stretch}, y_stretch: {y_stretch}')
            # movement horizontally or vertically
            if x_stretch == 2 and y_stretch == 0:
                rope[j][0] += 1
            elif x_stretch == -2 and y_stretch == 0:
                rope[j][0] += -1
            elif x_stretch == 0 and y_stretch == 2:
                rope[j][1] += 1
            elif x_stretch == 0 and y_stretch == -2:
                rope[j][1] += -1
            # movement in all 12 possible diagonal directions
            elif x_stretch == 2 and y_stretch == 1:
                rope[j][0] += 1
                rope[j][1] += 1
            elif x_stretch == 2 and y_stretch == -1:
                rope[j][0] += 1
                rope[j][1] += -1
            elif x_stretch == -2 and y_stretch == 1:
                rope[j][0] += -1
                rope[j][1] += 1
            elif x_stretch == -2 and y_stretch == -1:
                rope[j][0] += -1
                rope[j][1] += -1
            elif x_stretch == 1 and y_stretch == 2:
                rope[j][0] += 1
                rope[j][1] += 1
            elif x_stretch == -1 and y_stretch == 2:
                rope[j][0] += -1
                rope[j][1] += 1
            elif x_stretch == 1 and y_stretch == -2:
                rope[j][0] += 1
                rope[j][1] += -1
            elif x_stretch == -1 and y_stretch == -2:
                rope[j][0] += -1
                rope[j][1] += -1
            elif x_stretch == 2 and y_stretch == 2:
                rope[j][0] += 1
                rope[j][1] += 1
            elif x_stretch == 2 and y_stretch == -2:
                rope[j][0] += 1
                rope[j][1] += -1
            elif x_stretch == -2 and y_stretch == 2:
                rope[j][0] += -1
                rope[j][1] += 1
            elif x_stretch == -2 and y_stretch == -2:
                rope[j][0] += -1
                rope[j][1] += -1

            j += 1
        visited.add(tuple(rope[-1]))

    # print(rope)

print(f'number of visited by tail: {len(visited)}')