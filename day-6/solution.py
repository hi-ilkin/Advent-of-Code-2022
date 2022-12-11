def get_marker(lines, marker):
    for line in lines:
        line = line.strip()
        for i in range(marker, len(line)):
            if len(set(line[i-marker:i])) == marker:
                print(i)
                break


if __name__ == '__main__':
    _lines = open('input.txt').readlines()

    get_marker(_lines, marker=14)
