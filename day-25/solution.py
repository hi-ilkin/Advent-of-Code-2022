fp = open('input.txt')

snafu_to_decimal = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2
}

decimal_to_snafu = {
    0: "0",
    1: "1",
    2: "2",
    -1: "-",
    -2: "=",
    4: "1-",
    3: '1='
}


def calculate_total():
    total_sum = 0
    for line in fp.readlines():
        tmp_sum = 0
        for i, num in enumerate(line.strip()[::-1]):
            tmp_sum += snafu_to_decimal[num] * pow(5, i)

        total_sum += tmp_sum
        # print(f' {line.strip()}: {tmp_sum}')
    return total_sum


def base5_to_snafu(base5):
    snafu = ''
    snafu_carry = 0
    for d in str(base5)[::-1]:
        d = int(d)
        d += snafu_carry
        if d == 3:
            snafu += '='
            snafu_carry = 1
        elif d == 4:
            snafu += '-'
            snafu_carry = 1
        elif d == 5:
            snafu += '0'
            snafu_carry = 1
        else:
            snafu += decimal_to_snafu[d]
            snafu_carry = 0

    while snafu_carry:
        d = snafu_carry
        if d == 3:
            snafu += '='
            snafu_carry = 1
        elif d == 4:
            snafu += '-'
            snafu_carry = 1
        else:
            snafu += decimal_to_snafu[d]
            snafu_carry = 0

    return snafu[::-1]


def convert_to_base_5(decimal):
    base = 1
    result = 0
    while decimal:
        d = decimal % 5 * base
        result = result + d
        decimal = decimal // 5
        base = base * 10

    return result, base5_to_snafu(result)


total = calculate_total()
print(convert_to_base_5(total))
