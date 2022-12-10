import string

with open('pi5.txt') as f:
    strings = f.read().strip().split('\n')

vowels = ['a', 'e', 'i', 'o', 'u']
naughty = ['ab', 'cd', 'pq', 'xy']
nice_string_count = 0
for s in strings:
    # check if there are at least 3 vowels
    vowel_score = 0
    for v in vowels:
        if v in s:
            vowel_score += s.count(v)
    if vowel_score < 3:
        print(s)
        continue

    # check if there is a pair of the same letter
    double_letters = False
    for i, c in enumerate(s):
        if i+1 < len(s) and c == s[i+1]:
            double_letters = True
    if not double_letters:
        continue

    # check for ab, cd, pq, xy
    contains_naughty = False
    for n in naughty:
        if n in s:
            # print(s)
            contains_naughty = True
    if contains_naughty:
        continue

    nice_string_count += 1

print(f'nice string count: {nice_string_count}')

# part 2

nice_string_count2 = 0
for s in strings:
    # pair appears twice
    pair = False
    for i, c in enumerate(s):
        if i+1 < len(s) and s.count(s[i:i+2]) >= 2:
            pair = True
    if not pair:
        continue

    # letter repeated with one in between
    repeated = False
    for i, c in enumerate(s):
        if i+2 < len(s) and c == s[i+2]:
            repeated = True
    if not repeated:
        continue

    nice_string_count2 += 1

print(f'nice string count #2: {nice_string_count2}')
