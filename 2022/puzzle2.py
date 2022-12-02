
with open('pi2.txt') as f:
    s = f.read()
    l = s.split('\n')

rounds = [line.split() for line in l]

mapping = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3
}

score = 0

for i, r in enumerate(rounds):
    for j, e in enumerate(r):
        rounds[i][j] = mapping[e]
    score += r[1]
    dif = r[1]-r[0]
    if dif == 0:
        score += 3
    elif dif in [1, -2]:
        score += 6

print(score)

# part 2

mapping2 = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 0,
    'Y': 3,
    'Z': 6
}

rounds2 = [line.split() for line in l]
score2 = 0

for i, r in enumerate(rounds2):
    for j, e in enumerate(r):
        rounds2[i][j] = mapping2[e]
    score2 += r[1]
    if r[1] == 3: # draw
        score2 += r[0]
    elif r[1] == 6: # win
        num = r[0]+1
        if num == 4:
            num = 1
        score2 += num
    else: # lose
        num = r[0]-1
        if num == 0:
            num = 3
        score2 += num
        
print(score2)


# rock paper (1, 2)
# paper scissors (2, 3)
# scissors rock (3, 1)

