import string
import time
import math

# parse input
with open('pi12.txt') as f:
    lines = f.read().splitlines()
    grid = []
    num_grid = []
    for l in lines:
        grid.append([])
        num_grid.append([])
        row = list(l)
        for r in row:
            grid[-1].append(r)
            num_grid[-1].append(0)

# print(*grid, sep='\n')

# find start, end and convert letters into numbers
start = None
end = None
for i, col in enumerate(grid):
    for j, char in enumerate(col):
        # get start and end and change them into numbers
        if char == 'S':
            start = (i, j) # row, column
            char = 'a'
        elif char == 'E':
            end = (i, j) # row, column
            char = 'z'
        # convert into numbers
        num_grid[i][j] = string.ascii_lowercase.index(char)+1

# print(*grid, sep='\n')

def visualize(pos, start):
    path_grid = []
    for i in range(len(grid)):
        path_grid.append([])
        for j in range(len(grid[0])):
            path_grid[i].append(grid[i][j])
    backtrack_pos = pos
    while True:
        # draw found path
        if backtrack_pos.origin is not None:
            if backtrack_pos.origin[0]+1 == backtrack_pos[0]:
                char = 'V'
            elif backtrack_pos.origin[0]-1 == backtrack_pos[0]:
                char = '^'
            elif backtrack_pos.origin[1]+1 == backtrack_pos[1]:
                char = '>'
            else:
                char = '<'
            path_grid[backtrack_pos.origin[0]][backtrack_pos.origin[1]] = char
        if backtrack_pos == start:
            break
        backtrack_pos = backtrack_pos.origin
    for i in path_grid:
        print(*i, sep='')
    print()
    

class Tile(tuple):
    def __init__(self, pos:tuple, height:int = 1):
        tuple.__init__(pos)
        self.origin = None
        self.next_path = None
        self.height = height
    
    def __eq__(self, other:tuple):
        return self[:] == other[:]

def check_movement(current:int, destination:int):
    if current >= destination-1:
        return True
    else: return False

def dist_decision(point:tuple, destination:tuple):
    return abs(destination[0]-point[0])+abs(destination[1]-point[1])

# path finding algorithms:
def bfs_unoptimized(num_grid:list, start:tuple, end:tuple, movement_decision) -> int:
    '''
    Breadth-fists search algorithm
    return the minimum amount of steps
    '''
    # data structure: queue
    visiting = [Tile(start)]
    end = Tile(end)

    for t in visiting:
        x, y = t[0], t[1]
        # as long, as the final destination is not reached
        if t == end:
            break
        # find all possible adjacent tiles and add them to the queue
        # north
        if x-1 > -1: # if north is inside of the grid
            north = Tile((x-1, y), height = num_grid[x-1][y])
            if north not in visiting and movement_decision(t.height, north.height): # if north has not been visited and accessible
                north.origin = t # origin of north is the current tile
                visiting.append(north)
        # same as with north
        # east
        if y+1 < len(num_grid[0]): # if the adjacent tile is inside of the grid
            east = Tile((x, y+1), height = num_grid[x][y+1])
            if east not in visiting and movement_decision(t.height, east.height):
                east.origin = t
                visiting.append(east)
        # south
        if x+1 < len(num_grid): # if the adjacent tile is inside of the grid
            south = Tile((x+1, y), height = num_grid[x+1][y])
            if south not in visiting and movement_decision(t.height, south.height):
                south.origin = t
                visiting.append(south)
        # west
        if y-1 > -1: # if the adjacent tile is inside of the grid
            west = Tile((x, y-1), height = num_grid[x][y-1])
            if west not in visiting and movement_decision(t.height, west.height):
                west.origin = t
                visiting.append(west)

    # backtrack
    backtracking_position = t
    steps = 0
    while True:
        if backtracking_position == start:
            break
        steps += 1
        backtracking_position = backtracking_position.origin
    return steps


def bfs(num_grid:list, start:tuple, end:tuple, movement_decision) -> int:
    '''
    Breadth-fists search algorithm
    return the minimum amount of steps
    '''
    # data structure: queue
    visiting = [Tile(start)]
    # 2D list to store values, that have been visited
    visited = []
    for i in num_grid:
        visited.append([])
        for j in i:
            visited[-1].append(False)
    end = Tile(end)

    while len(visiting) > 0:
        t = visiting.pop(0)
        x, y = t[0], t[1]
        # as long, as the final destination is not reached
        if t == end:
            break
        # find all possible adjacent tiles and add them to the queue
        # north
        if x-1 > -1: # if north is inside of the grid
            north = Tile((x-1, y), height = num_grid[x-1][y])
            if not visited[x-1][y] and north not in visiting and movement_decision(t.height, north.height): # if north has not been visited and accessible
                north.origin = t # origin of north is the current tile
                visiting.append(north)
        # same as with north
        # east
        if y+1 < len(num_grid[0]): # if the adjacent tile is inside of the grid
            east = Tile((x, y+1), height = num_grid[x][y+1])
            if not visited[x][y+1] and east not in visiting and movement_decision(t.height, east.height):
                east.origin = t
                visiting.append(east)
        # south
        if x+1 < len(num_grid): # if the adjacent tile is inside of the grid
            south = Tile((x+1, y), height = num_grid[x+1][y])
            if not visited[x+1][y] and south not in visiting and movement_decision(t.height, south.height):
                south.origin = t
                visiting.append(south)
        # west
        if y-1 > -1: # if the adjacent tile is inside of the grid
            west = Tile((x, y-1), height = num_grid[x][y-1])
            if not visited[x][y-1] and west not in visiting and movement_decision(t.height, west.height):
                west.origin = t
                visiting.append(west)
        visited[x][y] = True

    # backtrack
    backtracking_position = t
    steps = 0
    while True:
        if backtracking_position == start:
            break
        steps += 1
        backtracking_position = backtracking_position.origin
    return steps


def dfs(num_grid:list, start:tuple, end:tuple, movement_decision) -> int:
    '''
    best first search
    return the minimum amount of steps
    '''
    # data structure: stack
    visiting = [Tile(start)]
    end = Tile(end)
    visited = []
    min_steps = math.inf
    # as long as there are still new tiles to uncover
    while len(visiting) > 0:
        current = visiting.pop()
        visited.append(current)
        # if the current position is the end
        if current == end and len(visiting) > 0:
            # backtrack and find number of steps
            backtracking_position = current
            steps = 0
            while True:
                if backtracking_position == start:
                    break
                steps += 1
                backtracking_position = backtracking_position.origin
            # if new count of steps is smaller than the old one, replace the old
            if steps < min_steps:
                min_steps = steps
            # delete the list of visited tiles and fill it again with all tiles in the path to the start of the next possible path
            visited = []
            current = visiting.pop()
            visited.append(current)
            backtracking_position = current.origin
            while True:
                if backtracking_position == start:
                    visited.append(start)
                    break
                visited.append(backtracking_position)
                backtracking_position = backtracking_position.origin

        x, y = current[0], current[1]
        # find all possible adjacent tiles and add them to the stack
        # north
        if x-1 > -1: # if north is inside of the grid
            north = Tile((x-1, y), height=num_grid[x-1][y])
            if north not in visited and movement_decision(current.height, north.height): # if north has not been visited and accessible
                north.origin = current # set the origin of north to the current tile
                current.next_path = north # set the next path of current to north
                visiting.append(north) # add north to stack of tiles to visit
        # same as with north
        # east
        if y+1 < len(num_grid[0]):
            east = Tile((x, y+1), height=num_grid[x][y+1])
            if east not in visited and movement_decision(current.height, east.height):
                east.origin = current
                current.next_path = east
                visiting.append(east)
        # south
        if x+1 < len(num_grid):
            south = Tile((x+1, y), height=num_grid[x+1][y])
            if south not in visited and movement_decision(current.height, south.height):
                south.origin = current
                current.next_path = south
                visiting.append(south)
        # west
        if y-1 > -1:
            west = Tile((x, y-1), height=num_grid[x][y-1])
            if west not in visited and movement_decision(current.height, west.height):
                west.origin = current
                current.next_path = west
                visiting.append(west)

        # if current does not have any next paths i.e. current is in a dead end
        # reset system up to next possible path (as seen above)
        if current.next_path is None and len(visiting) > 0:
            visited = []
            visited.append(current)
            backtracking_position = visiting[-1].origin
            while True:
                if backtracking_position == start:
                    visited.append(start)
                    break
                visited.append(backtracking_position)
                backtracking_position = backtracking_position.origin
            
    return min_steps

def best_first_search(grid:list, start:tuple, end:tuple, movement_decision, dist_decision) -> int:
    '''
    best first search algorithm
    return the minimum amount of steps
    '''
    ...

def a_star(grid:list, start:tuple, end:tuple, movement_decision) -> int:
    '''
    return the minimum amount of steps
    '''
    ...

def djikstra(grid:list, start:tuple, end:tuple, movement_decision) -> int:
    '''
    return the minimum amount of steps
    '''
    ...

start_time = time.time()
steps = bfs_unoptimized(num_grid, start, end, check_movement)
end_time = time.time()
steps = math.log(steps, 10)
print('BFS (unoptimized):\n steps:', steps, '\n execution time:', end_time-start_time, 's\n')

start_time = time.time()
steps = bfs(num_grid, start, end, check_movement)
end_time = time.time()
steps = math.log(steps, 10)
print('BFS:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n')

start_time = time.time()
steps = dfs(num_grid, start, end, check_movement)
end_time = time.time()
steps = math.log(steps, 10)
print('DFS:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n')

