
import string

with open('pi3.txt') as f:
    s = f.read()
    lines = s.splitlines()

score = 0
score_list = [' '] + list(string.ascii_lowercase) + list(string.ascii_uppercase)
print(score_list)

for i, l in enumerate(lines):
    # splitting the line in half
    half_length = len(l)//2
    left = l[:half_length]
    right = l[half_length:]

    # making sets
    left_set = set(left[:])
    right_set = set(right[:])

    # intersection
    intersection = left_set.intersection(right_set)
    char = list(intersection)[0]
    
    # calculate score
    score += score_list.index(char)

print(score)

# part 2

score = 0

for i in range(0, len(lines), 3):
    # create groups as list of sets
    group = [set(l[:]) for l in lines[i:i+3]]

    # intersection
    intersection = group[0].intersection(group[1]).intersection(group[2])
    char = list(intersection)[0]
    
    # calculate score
    score += score_list.index(char)

print(score)


    


