
with open('pi5.txt') as f:
    lines = f.read().split('\n')
    moves = False
    move_list = []
    for i, l in enumerate(lines):
        # find line of numbers
        if l[:2] == ' 1':
            crate_bottom = i-1
            crate_grid = []
            # for each line going up from line_bottom
            for j in range(crate_bottom, -1, -1):
                # get names of crates or ' ' if there is no crate
                crate_row = list(lines[j][1::4])
                crate_grid.append(crate_row)
            crate_stacks = []
            # transpose matrix of crates
            for width in range(len(crate_grid[0])):
                stack = []
                for height in range(len(crate_grid)):
                    if crate_grid[height][width] != ' ':
                        stack.append(crate_grid[height][width])
                crate_stacks.append(stack)
        elif moves:
            line = l
            line = line.replace('move ', ' ').replace(' from ', ' ').replace(' to ', ' ')
            move_list.append(line.split())
        elif l == '':
            moves = True
    
    # list of crate_stacks
    print(*crate_stacks, sep='\n')
    # list of moves in the format [num, from, to]2
    move_list.pop()
    print(*move_list, sep='\n')
    print()

# part 1
# for l in move_list:
#     for i in range(int(l[0])):
#         crate = crate_stacks[int(l[1])-1].pop()
#         crate_stacks[int(l[2])-1].append(crate)
        
# print(*crate_stacks, sep='\n')
# print(*[c[-1] for c in crate_stacks], sep='')

# part 2
for l in move_list:
    crates = []
    for i in range(int(l[0])):
        crate = crate_stacks[int(l[1])-1].pop()
        crates.insert(0, crate)
        print(*crate_stacks, sep='\n')
        print()
    for i in range(int(l[0])):
        crate_stacks[int(l[2])-1].append(crates[i])
        
print(*crate_stacks, sep='\n')
print(*[c[-1] for c in crate_stacks], sep='')
    