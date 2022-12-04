
import hashlib


puzzle_inp = 'iwrupvqb'

i = 1
while True:
    h = hashlib.md5(bytes(puzzle_inp + str(i), 'utf-8'))
    s_h = h.hexdigest()
    if s_h[:6] == '000000':
        print(i)
        break
    i += 1