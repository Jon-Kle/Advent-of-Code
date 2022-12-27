import string
import time
import math
import console_colors as c_col

# read input
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

# find start, end and create letters grid from number_grid
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


# utilities
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
            char = c_col.GREEN.fg
            if backtrack_pos.origin[0]+1 == backtrack_pos[0]:
                char += 'V'
            elif backtrack_pos.origin[0]-1 == backtrack_pos[0]:
                char += '^'
            elif backtrack_pos.origin[1]+1 == backtrack_pos[1]:
                char += '>'
            else:
                char += '<'
            char += c_col.RESET
            path_grid[backtrack_pos.origin[0]][backtrack_pos.origin[1]] = char
        if backtrack_pos == start:
            break
        backtrack_pos = backtrack_pos.origin
    for i in path_grid:
        for j in i:
            if j == 'a':
                char = f'{c_col.RED.fg}a{c_col.RESET}'
            else:
                char = j
            print(char, end='')
        print()
    print()
    
class Time_Stats():
    def __init__(self):
        self.time_lists = {}
        self.last_time = None
        self.last_name = None
        self.start_time = None
    
    def measure(self, name:str):
        measurements = self.time_lists.get(name)
        t = time.time()
        if self.start_time is None:
            self.start_time = t
        if measurements is None:
            self.time_lists[name] = []
        if self.last_time is not None:
            measurement = t - self.last_time
            self.time_lists[self.last_name].append(measurement)
        self.last_time = t
        self.last_name = name
    
    def print_stats(self):
        name_list = self.time_lists.keys()
        for s in name_list:
            if len(self.time_lists[s]) > 0:
                print(s, ':', sep='')
                time_ = sum(self.time_lists[s])
                print(' ', time_, 's', sep='')
        print('total time: ', time.time()-self.start_time, 's', sep='')
        print()

class Tile(tuple):
    def __init__(self, pos:tuple, height:int = 1):
        tuple.__init__(pos)
        self.origin = None
        self.next_path = None
        self.height = height
        self.steps = math.inf
        self.connections = [False, False, False, False] # north, east, south, west
    
    def __eq__(self, other:tuple):
        return self[:] == other[:]

def check_movement(current:int, destination:int):
    '''
    standard movement rules as intended by the puzzle
    allows all tiles that are at most one higher than the current point
    '''
    if current >= destination-1:
        return True
    else: return False

def check_movement2(current:int, destination:int):
    '''
    does not allow falling to optimize the algorithm.
    used in the DFS implementation
    allows all tiles that are equal or one higher than the current point
    '''
    if current == destination-1 or current == destination:
        return True
    else: return False

def dist_decision(visiting:tuple, destination:tuple):
    '''
    used for Greedy BFS
    takes list and finds the tile that is the nearest to the endpoint in manhattan distance
    if multiple points are equally far away, it prioritizes the one, that is the nearest in euclidean distance
    '''
    best_dist = math.inf
    optimal = []
    for t in visiting:
        dist = abs(destination[0]-t[0])+abs(destination[1]-t[1])
        if dist < best_dist:
            optimal = [t]
            best_dist = dist
        elif dist == best_dist:
            optimal.append(t)
    if abs(destination[0]-t[0]) > abs(destination[1]-t[1]):
        priority = 0
    else:
        priority = 1
    if len(optimal) > 1:
        optimal.sort(key=lambda a: a[priority], reverse=True)
    return optimal[0]

def dist_decision2(visiting, destination):
    '''
    used for A*
    chooses tile from the list by calculating the sum of the distance to the destination and the steps needed to get to the tile
    '''
    optimal = None
    best_score = math.inf
    for t in visiting:
        score = t.steps + abs(destination[0]-t[0])+abs(destination[1]-t[1])
        if score < best_score:
            best_score = score
            optimal = t
    return optimal

def dist_decision3(visiting):
    '''
    used for Dijkstra
    finds the tile in the list with the least steps from the starting point
    '''
    min_steps = math.inf
    optimal = None
    for t in visiting:
        if t.steps < min_steps:
            min_steps = t.steps
            optimal = t
    return optimal


# path finding algorithms:
def bfs_not_optimized(num_grid:list, start:tuple, end:tuple, movement_decision) -> int:
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

def bfs(num_grid:list, start:tuple, end:tuple, movement_decision, show = False) -> int:
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
    if show:
        visualize(t, start)
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
    # create grid of bools
    for i in num_grid:
        visited.append([])
        for j in i:
            visited[-1].append(False)
    visiting_grid = []
    # create grid of bools
    for i in num_grid:
        visiting_grid.append([])
        for j in i:
            visiting_grid[-1].append(False)
    min_steps = math.inf
    # as long as there are still new tiles to uncover
    while len(visiting) > 0:
        current = visiting.pop()
        x, y = current[0], current[1]
        visiting_grid[x][y] = False
        visited[x][y] = True
        if len(visiting)%50 == 0:
            print('visiting', len(visiting), 'shortest:', min_steps)
            # visualize(current, start)
            print(*[string.ascii_lowercase[i%26] for i in range(179)], sep='')
            for i, row in enumerate(visited):
                for j, tile in enumerate(row):
                    if x == i and y == j:
                        print('O', end='', flush=False)
                    elif visited[i][j]:
                        print('X', end='', flush=False)
                    else: print(' ', end='', flush=False)
                print('', flush=False)
            print(f'\033[2J\033[H')

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
            # create grid of bools
            for i in num_grid:
                visited.append([])
                for j in i:
                    visited[-1].append(False)
            current = visiting.pop()
            x, y = current[0], current[1]
            visiting_grid[x][y] = False
            visited[x][y] = True
            backtracking_position = current.origin
            while True:
                if backtracking_position == start:
                    visited[start[0]][start[1]] = True
                    break
                visited[backtracking_position[0]][backtracking_position[1]] = True
                backtracking_position = backtracking_position.origin

        # find all possible adjacent tiles and add them to the stack
        # north
        if x-1 > -1: # if north is inside of the grid
            north = Tile((x-1, y), height=num_grid[x-1][y])
            if not visited[x-1][y] and not visiting_grid[x-1][y] and movement_decision(current.height, north.height): # if north has not been visited and accessible
                north.origin = current # set the origin of north to the current tile
                current.next_path = north # set the next path of current to north
                visiting.append(north) # add north to stack of tiles to visit
                visiting_grid[north[0]][north[1]] = True
        # same as with north
        # east
        if y+1 < len(num_grid[0]):
            east = Tile((x, y+1), height=num_grid[x][y+1])
            if not visited[x][y+1] and not visiting_grid[x][y+1] and movement_decision(current.height, east.height):
                east.origin = current
                current.next_path = east
                visiting.append(east)
                visiting_grid[east[0]][east[1]] = True
        # south
        if x+1 < len(num_grid):
            south = Tile((x+1, y), height=num_grid[x+1][y])
            if not visited[x+1][y] and not visiting_grid[x+1][y] and movement_decision(current.height, south.height):
                south.origin = current
                current.next_path = south
                visiting.append(south)
                visiting_grid[south[0]][south[1]] = True
        # west
        if y-1 > -1:
            west = Tile((x, y-1), height=num_grid[x][y-1])
            if not visited[x][y-1] and not visiting_grid[x][y-1] and movement_decision(current.height, west.height):
                west.origin = current
                current.next_path = west
                visiting.append(west)
                visiting_grid[west[0]][west[1]] = True

        # if current does not have any next paths i.e. current is in a dead end
        # reset system up to next possible path (as seen above)
        if current.next_path is None and len(visiting) > 0:
            visited = []
            # create grid of bools
            for i in num_grid:
                visited.append([])
                for j in i:
                    visited[-1].append(False)
            current = visiting.pop()
            x, y = current[0], current[1]
            visiting_grid[x][y] = False
            visited[x][y] = True
            backtracking_position = current.origin
            while True:
                if backtracking_position == start:
                    visited[start[0]][start[1]] = True
                    break
                visited[backtracking_position[0]][backtracking_position[1]] = True
                backtracking_position = backtracking_position.origin
            
    return min_steps

def greedy_bfs(num_grid:list, start:tuple, end:tuple, movement_decision, dist_decision, show = False) -> int:
    '''
    best first search algorithm
    return (the minimum amount of steps) a path to the goal
    '''
    # list of all possible next moves
    visiting = [Tile(start)]
    visited = []
    for row in num_grid:
        visited.append([])
        for tile in row:
            visited[-1].append(False)
    end = Tile(end)    

    while len(visiting) > 0:
        # search for the best and switch to this tile
        current = dist_decision(visiting, end)
        visiting.remove(current)
        x, y = current[0], current[1]
        if current == end:
            break
        # find all adjacent tiles and add them to the list of visiting
        # north
        if x-1 > -1: # if north is inside of the grid
            north = Tile((x-1, y), height = num_grid[x-1][y])
            if not visited[x-1][y] and north not in visiting and movement_decision(current.height, north.height): # if north has not been visited and accessible
                north.origin = current # origin of north is the current tile
                visiting.append(north)
        # same as with north
        # east
        if y+1 < len(num_grid[0]): # if the adjacent tile is inside of the grid
            east = Tile((x, y+1), height = num_grid[x][y+1])
            if not visited[x][y+1] and east not in visiting and movement_decision(current.height, east.height):
                east.origin = current
                visiting.append(east)
        # south
        if x+1 < len(num_grid): # if the adjacent tile is inside of the grid
            south = Tile((x+1, y), height = num_grid[x+1][y])
            if not visited[x+1][y] and south not in visiting and movement_decision(current.height, south.height):
                south.origin = current
                visiting.append(south)
        # west
        if y-1 > -1: # if the adjacent tile is inside of the grid
            west = Tile((x, y-1), height = num_grid[x][y-1])
            if not visited[x][y-1] and west not in visiting and movement_decision(current.height, west.height):
                west.origin = current
                visiting.append(west)
        # mark the visited in a grid of booleans
        visited[x][y] = True
    
    if show:
        visualize(current, start)
    backtracking_position = current
    steps = 0
    while True:
        if backtracking_position == start:
            break
        steps += 1
        backtracking_position = backtracking_position.origin
    return steps

def a_star(num_grid:list, start:tuple, end:tuple, movement_decision, dist_decision, show = False) -> int:
    '''
    A-star algorithm
    return the minimum amount of steps
    '''
    # list of all possible next moves
    visiting = [Tile(start)]
    visiting[0].steps = 0
    visited = []
    for row in num_grid:
        visited.append([])
        for tile in row:
            visited[-1].append(False)
    end = Tile(end)    

    while len(visiting) > 0:
        # search for the best and switch to this tile
        current = dist_decision(visiting, end)
        visiting.remove(current)
        x, y = current[0], current[1]
        if current == end:
            break
        # find all adjacent tiles and add them to the list of visiting
        # north
        if x-1 > -1: # if north is inside of the grid
            north = Tile((x-1, y), height = num_grid[x-1][y])
            if not visited[x-1][y] and north not in visiting and movement_decision(current.height, north.height): # if north has not been visited and accessible
                north.origin = current # origin of north is the current tile
                north.steps = current.steps+1
                visiting.append(north)
        # same as with north
        # east
        if y+1 < len(num_grid[0]): # if the adjacent tile is inside of the grid
            east = Tile((x, y+1), height = num_grid[x][y+1])
            if not visited[x][y+1] and east not in visiting and movement_decision(current.height, east.height):
                east.origin = current
                east.steps = current.steps+1
                visiting.append(east)
        # south
        if x+1 < len(num_grid): # if the adjacent tile is inside of the grid
            south = Tile((x+1, y), height = num_grid[x+1][y])
            if not visited[x+1][y] and south not in visiting and movement_decision(current.height, south.height):
                south.origin = current
                south.steps = current.steps+1
                visiting.append(south)
        # west
        if y-1 > -1: # if the adjacent tile is inside of the grid
            west = Tile((x, y-1), height = num_grid[x][y-1])
            if not visited[x][y-1] and west not in visiting and movement_decision(current.height, west.height):
                west.origin = current
                west.steps = current.steps+1
                visiting.append(west)
        # mark the visited in a grid of booleans
        visited[x][y] = True
    
    if show:
        visualize(current, start)
    return current.steps

def dijkstra(num_grid:list, start:tuple, end:tuple, movement_decision, d_decision, show = False) -> int:
    '''
    Dijkstra algorithm
    return the minimum amount of steps
    '''
    time_s = Time_Stats()
    # track the state of all connections √
    visiting = [Tile(start)]
    # for running it backwards
    # visiting[0].height = 26
    visiting[0].steps = 0
    visited = []
    for row in num_grid:
        visited.append([])
        for r in row:
            visited[-1].append(None)
    end = Tile(end)
    iteration = 0
    # get the tile in visiting with the least steps
    while len(visiting) > 0:
        # print(len(visiting))
        time_s.measure('finding the next tile')
        # find tile with least steps
        current = d_decision(visiting)
        occurrence = visiting.count(current)
        for i in range(occurrence):
            visiting.remove(current)
        x, y = current[0], current[1]
        time_s.measure('north')
        # north
        if x-1 > -1 and not current.connections[0]:
            north = Tile((x-1, y), height=num_grid[x-1][y])
            if not visited[x-1][y] and movement_decision(current.height, north.height):
                current.connections[0] = True
                north.connections[2] = True
                if current.steps + 1 < north.steps:
                    north.steps = current.steps + 1
                    north.origin = current
                visiting.append(north)
        time_s.measure('east')
        # east
        if y+1 < len(visited[0]) and not current.connections[1]:
            east = Tile((x, y+1), height=num_grid[x][y+1])
            if not visited[x][y+1] and movement_decision(current.height, east.height):
                current.connections[1] = True
                east.connections[3] = True
                if current.steps + 1 < east.steps:
                    east.steps = current.steps + 1
                    east.origin = current
                visiting.append(east)
        time_s.measure('south')
        # south
        if x+1 < len(visited) and not current.connections[2]:
            south = Tile((x+1, y), height=num_grid[x+1][y])
            if not visited[x+1][y] and movement_decision(current.height, south.height):
                current.connections[2] = True
                south.connections[0] = True
                if current.steps + 1 < south.steps:
                    south.steps = current.steps + 1
                    south.origin = current
                visiting.append(south)
        time_s.measure('west')
        # west
        if y-1 > -1 and not current.connections[3]:
            west = Tile((x, y-1), height=num_grid[x][y-1])
            if not visited[x][y-1] and movement_decision(current.height, west.height):
                current.connections[3] = True
                west.connections[1] = True
                if current.steps + 1 < west.steps:
                    west.steps = current.steps + 1
                    west.origin = current
                visiting.append(west)
        visited[x][y] = current

    if show:
        visualize(current, start)
        # look up the end tile in visited
        for i, row in enumerate(visited):
            for j, tile in enumerate(row):
                if visited[i][j] is not None:
                    if grid[i][j] == 'a':
                        with c_col.Background(c_col.RED): # c_col.rgb(200, (tile.steps*5)+80, 50)
                            print('a', end='')
                    else:
                        with c_col.Background(c_col.rgb(80, (tile.steps*5)+80, 180)):
                            print(grid[i][j], end='')
                else:
                    print(' ', end='')
            print()
        print()
        time_s.print_stats()
    return visited[end[0]][end[1]].steps


# execution of the algorithms
show = True

# not optimized BFS (~15s to finish)
# start_time = time.time()
# steps = bfs_not_optimized(num_grid, start, end, check_movement)
# end_time = time.time()
# print('BFS (not optimized):\n steps:', steps, '\n execution time:', end_time-start_time, 's\n')

# BFS
start_time = time.time()
steps = bfs(num_grid, start, end, check_movement, show = show)
end_time = time.time()
print('BFS:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n\n')

# DFS
# does not finish in a reasonable amount of time
# start_time = time.time()
# steps = dfs(num_grid, start, end, check_movement2)
# end_time = time.time()
# print('DFS:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n')

# Greedy BFS
# does not find the optimal path
start_time = time.time()
steps = greedy_bfs(num_grid, start, end, check_movement, dist_decision, show = show)
end_time = time.time()
print('Greedy bfs:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n\n')

# A*
start_time = time.time()
steps = a_star(num_grid, start, end, check_movement, dist_decision2, show = show)
end_time = time.time()
print('A-star:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n\n')

# Dijkstra
start_time = time.time()
steps = dijkstra(num_grid, start, end, check_movement, dist_decision3, show=show)
end_time = time.time()
print('Dijkstra:\n steps:', steps, '\n execution time:', end_time-start_time, 's\n\n')

# inefficiently iterating over all possible starting points
# it could also just run one time backwards with altered rules for walking down slopes
start_time = time.time()
min_steps = math.inf
for x in range(len(num_grid)):
    steps = dijkstra(num_grid, (x, 0), end, check_movement, dist_decision3, show=False)
    if min_steps > steps:
        min_steps = steps
end_time = time.time()
print('steps from the nearest point:', min_steps, '\n execution time:', end_time-start_time, 's\n')