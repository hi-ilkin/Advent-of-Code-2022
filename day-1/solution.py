lines = ''.join(open('input').readlines())

max_sums = []
sub_sum = 0

for line in lines:
    line = line.strip()
    if line == '':
        print(sub_sum)
        max_sums.append(sub_sum)
        sub_sum = 0
    else:
        sub_sum += int(line)

max_sums = sorted(max_sums, reverse=True)
print(f'Max {max_sums[:3]} {sum(max_sums[:3])}')