
with open('pi1.txt') as f:
    s = f.read()
    floor = 0
    first_basement = None
    for i, c in enumerate(s):
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1
        if not first_basement and floor < 0:
            first_basement = i+1
print(floor) # part 1
print(first_basement) # part 2