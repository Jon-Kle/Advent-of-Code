
with open('pi6.txt') as f:
    s = f.read()

for i in range(len(s)-14):
    character_set = set()
    for j in range(14):
        character_set.add(s[i+j])
    if len(character_set) == 14:
        print(i+14)
        break