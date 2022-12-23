with open('pi10.txt') as f:
    lines = f.read().splitlines()

instr = []
for l in lines:
    action = l[:4]
    number = 0
    if action == 'addx':
        action = True
        number = int(l[5:])
    else: action = False
    instr.append((action, number))
    
cycle = 0
x_register = 1
current_com = None
sum_ = 0

while 0 < len(instr):
    current_instr = instr.pop(0)
    # set up process time
    if current_instr[0]:
        process_time = 2
    else:
        process_time = 1

    # wait for process time to end
    while process_time > 0:
        if cycle%40 in (x_register-1, x_register, x_register+1):
            print('o', end='')
        else:
            print(' ', end='')
        # print(x_register, cycle)

        if cycle+1 in [40, 80, 120, 160, 200, 240]:
            # sum_ += cycle*x_register
            print()
        process_time -= 1
        cycle += 1

    if current_instr[0]:
        x_register += current_instr[1]

# print('\n', sum_)
print(x_register, cycle)



    
