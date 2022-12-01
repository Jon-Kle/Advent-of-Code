
elf_carriage = []
with open('pi1.txt') as f:
    s = f.read()
    s = s.splitlines()
    buffer = []
    for i in s:
        if i:
            buffer.append(int(i))
        else:
            elf_carriage.append(buffer)
            buffer = []

values = []
for e in elf_carriage:
    val = sum(e)
    values.append(val)
print(max(values))

# part 2 of the puzzle

sum_of_top_three = max(values)
values.pop(values.index(max(values)))
sum_of_top_three += max(values)
values.pop(values.index(max(values)))
sum_of_top_three += max(values)
print(sum_of_top_three)
        
