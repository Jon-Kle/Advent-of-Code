import json

with open('pi7.txt') as f:
    s = f.read()
    lines = s.split('\n')


data = {}

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
print(data)

with open('data_structure.json', 'w') as f:
    f.write(json.dumps(data, indent=4))