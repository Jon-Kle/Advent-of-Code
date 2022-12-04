
with open('pi3.txt') as f:
    s = f.read()
    x1, y1 = 0, 0
    visited1 = set()
    for c in s:
        match c:
            case '^':
                y1 += 1
            case 'v':
                y1 -= 1
            case '>':
                x1 += 1
            case '<':
                x1 -= 1
        visited1.add((x1, y1))
        
    x1, y1 = 0, 0
    x2, y2 = 0, 0
    visited2 = set()
    for i, c in enumerate(s):
        x, y = 0, 0
        match c:
            case '^':
                y += 1
            case 'v':
                y -= 1
            case '>':
                x += 1
            case '<':
                x -= 1
        if i%2 == 1:
            x2 += x
            y2 += y
            visited2.add((x2, y2))
        else:
            x1 += x
            y1 += y
            visited2.add((x1, y1))


print(visited1.__len__())
print(visited2.__len__())