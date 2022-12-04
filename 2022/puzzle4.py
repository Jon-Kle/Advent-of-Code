
with open('pi4.txt') as f:
    lines = f.readlines()

def parse(line:str):
    line = line.rstrip('\n')
    elf_pair = line.split(',')
    elf_sections = []
    for e in elf_pair:
        sections = e.split('-')
        elf_sections.append(list(map(lambda l: int(l), sections)))
    return elf_sections

parsed_lines = list(map(parse, lines))

score = 0

for e in parsed_lines:
    if e[0][0] <= e[1][0] and e[0][1] >= e[1][1]:
        score += 1
    elif e[0][0] >= e[1][0] and e[0][1] <= e[1][1]:
        score += 1

print(score)

# part 2

score = 0

# 10 - 00
# 10 - 01
# 11 - 00
# 11 - 01
def calc_dif(line):
    dif = [None for e in range(4)]
    dif[0] = line[1][0]-line[0][0]>=0
    dif[1] = line[1][0]-line[0][1]>0
    dif[2] = line[1][1]-line[0][0]>=0
    dif[3] = line[1][1]-line[0][1]>0
    return dif

parsed_lines_test=[
    [[15, 20],[20, 30]],
    [[15, 40],[20, 30]],
    [[25, 26],[20, 30]],
    [[25, 35],[20, 30]]
]

dif_list = list(map(calc_dif, parsed_lines))

solutions = [
    [True, False, True, True], 
    [True, False, True, False], 
    [False, False, True, True], 
    [False, False, True, False]
    ]

for l in dif_list:
    if l in solutions:
        score += 1

print(score)