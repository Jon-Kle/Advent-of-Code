
def calc_wrapping_paper(l, w, h):
    faces = [l*w, w*h, h*l]
    smallest = min(faces)
    return sum(faces)*2 + smallest

def calc_ribbon(l, w, h):
    sides = [l, w, h]
    min_sides = min(sides)
    sides.remove(min_sides)
    perimeter = min_sides*2 + min(sides)*2
    bow = l*w*h
    return perimeter+bow


with open('pi2.txt') as f:
    total = 0
    total_ribbon = 0
    for l in f:
        split = l.split('x')
        l = int(split[0])
        w = int(split[1])
        h = int(split[2])
        total += calc_wrapping_paper(l, w, h)
        total_ribbon += calc_ribbon(l, w, h)


print(total) # part 1
print(total_ribbon) # part 2