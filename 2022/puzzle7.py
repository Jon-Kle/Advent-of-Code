import json

# parse data into lines
with open('pi7.txt') as f:
    s = f.read()
    lines = s.split('\n')

# directory structure
data = {}

# add a file to a path, creating the
def add_data(data:dict, current_path:list, name, entry:int):
    # print(current_path)
    if current_path[0] not in data.keys():
        data[current_path[0]] = dict()

    if len(current_path) > 1:
        data[current_path[0]] = add_data(data[current_path[0]], current_path[1:], name, entry)
    else:
        data[current_path[0]][name] = entry
    return data

def get_data(data, current_path:list, name:str=None):
    if len(current_path) > 1:
        result = get_data(data[current_path[0]], current_path[1:], name)
    else:
        if name is None:
            result = list(data[current_path[0]].values())
        else:
            result = data[current_path[0]][name]
    return result

# create directory tree from input
current_path = []
i = 0
state = 'normal'
while i<len(lines):
    if lines[i].startswith('$'):
        state = 'normal'
    if lines[i].startswith('$ cd ..'):
        current_path.pop()
    elif lines[i].startswith('$ cd'):
        current_path.append(lines[i][5:])
    elif lines[i].startswith('$ ls'):
        state = 'ls'
    elif state == 'ls':
        if lines[i].startswith('dir'):
            pass
        else:
            data = add_data(data, current_path, lines[i].split()[1], int(lines[i].split()[0]))
    i += 1
# print(data)

# with open('data_structure.json', 'w') as f:
#     f.write(json.dumps(data, indent=4))

dirs = []

def get_size(data:dict, path:list=[]):
    # print(path)
    size = 0
    # get list of content
    keys = data.keys()
    # iterate through list
    for k in keys:
        # if element is dict call self
        if isinstance(data[k], dict):
            size += get_size(data[k], path+[k])
        # else add to total size
        else:
            size += data[k]
    # add tuple of path and size to list of dirs
    dirs.append((path, size))
    return size

total_size = get_size(data)

# part 1
score = 0
for d in dirs:
    if d[1] <= 100000:
        score += d[1] 
print(f'{score:,}')

# part 2
free_space = 70_000_000-total_size
print(f'free space: {free_space:,}')
space_to_be_freed = 30_000_000-free_space
print(f'space to be freed: {space_to_be_freed:,}')

possible_dirs = []
for d in dirs:
    if d[1] >= space_to_be_freed:
        possible_dirs.append(d)
possible_dirs.sort(key = lambda v: v[1])
# solution
print('path to smallest possible file:')
path_to_smallest_possible_file = ''
for d in possible_dirs[0][0]:
    path_to_smallest_possible_file += f'{d}/'
path_to_smallest_possible_file = path_to_smallest_possible_file.rstrip('/')[1:]
print(f'path to smallest_possible file: {path_to_smallest_possible_file}')
print(f'size of smallest possible file: {possible_dirs[0][1]}')