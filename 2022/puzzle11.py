# objects for monkeys
class Monkey:
    def __init__(self, description:str):
        # description split into lines
        desc_list = description.splitlines()
        for i, d in enumerate(desc_list):
            desc_list[i] = d.strip()
        # parse for item_list
        self.item_list = desc_list[1].lstrip('Starting items: ')
        self.item_list = list(map(int, self.item_list.split(', ')))
        # parse for operation
        self.operation = desc_list[2][17:]
        # parse for test_num
        self.test_num = int(desc_list[3][19:])
        # parse for destination monkeys
        self.dest_monkeys = (int(desc_list[4][25:]), int(desc_list[5][26:]))

        self.action_count = 0
    
    def give_item(self, item:int):
        self.item_list.append(item)

    def pop_item(self):
        return self.item_list.pop(0)

    def inspect(self, item:int):
        old = item
        return eval(self.operation)
    
    def test(self, item:int):
        if item%self.test_num == 0:
            return self.dest_monkeys[0]
        else:
            return self.dest_monkeys[1]

# opening and parsing the input
with open("pi11.txt") as f:
    monkey_strings = f.read().split('\n\n')

# spawning monkeys
monkeys = []
for s in monkey_strings:
    monkeys.append(Monkey(s))

# calculating product of all divisors (test_nums)
maximum_worry_level = 1
for m in monkeys:
    maximum_worry_level *= m.test_num

# script to handle rounds (20)
round_ = 0
while round_ < 10000:
    for m in monkeys:
        for i in range(len(m.item_list)):
            # get first item from monkey list
            current_item = m.pop_item()
            # let the monkey inspect the item
            current_item = m.inspect(current_item)
            m.action_count += 1
            # divide by 3 floored
            # current_item = current_item // 3 # (part 1)
            current_item = current_item % maximum_worry_level # (part 2)
            # test worry level
            monkeys[m.test(current_item)].give_item(current_item)
            # print(current_item)
    round_ += 1

action_count_list = []
for m in monkeys:
    action_count_list.append(m.action_count)
action_count_list.sort(reverse=True)

# print(action_count_list)
print('monkey business:', action_count_list[0]*action_count_list[1])