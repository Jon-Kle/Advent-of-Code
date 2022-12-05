
with open('pi5.txt') as f:
    lines = f.read().split('\n')
    moves = False
    move_list = []
    for i, l in enumerate(lines):
        if moves:
            line = l
            line = line.replace('move ', ' ').replace(' from ', ' ').replace(' to ', ' ')
            move_list.append(line.split())
        # find line of numbers
        if l[:2] == ' 1':
            crate_bottom = i-1
            crate_grid = []
            # for each line going up from line_bottom
            for j in range(crate_bottom, -1, -1):
                crate_row = []
                # get names of crates or ' ' if there is no crate
                for k in range(len(lines[j])):
                    if (k-1)%4 == 0:
                        crate_row.append(lines[j][k])
                crate_grid.append(crate_row)
            crate_stacks = []
            for width in range(len(crate_grid[0])):
                stack = []
                for height in range(len(crate_grid)):
                    if crate_grid[height][width] != ' ':
                        stack.append(crate_grid[height][width])
                crate_stacks.append(stack)
        elif l == '':
            moves = True
    
    # list of crate_stacks
    print(*crate_stacks, sep='\n')
    # list of moves in the format [num, from, to]
    print(*move_list, sep='\n')
                