import re
from Directory import Directory

TOTAL_SIZE = 70_000_000
REQUIRED_SPACE = 30_000_000


def get_file_size(cmd):
    f_size = re.search(r'\d+', cmd)
    if f_size:
        return int(f_size.group())
    return 0


def is_file(cmd):
    f_size_exist = re.search(r'\d+', cmd)
    return f_size_exist is not None


def create_dirs(lines):
    directories = []

    parent_dir = None
    cur_dir = None
    for command in lines:
        command = command.strip()

        if command.startswith('$ cd ') and '..' not in command:
            dir_name = command.split('cd ')[-1]
            parent_dir = cur_dir
            cur_dir = Directory(name=dir_name, size=0, parent=parent_dir)

            if parent_dir is not None:
                parent_dir.children.append(cur_dir)
            directories.append(cur_dir)

        elif is_file(command):
            cur_dir.files.append(command)
            cur_dir.size += get_file_size(command)

        elif command.startswith('$ cd ..'):
            if not cur_dir.processed:
                parent_dir.size += cur_dir.size
                cur_dir.processed = True

            cur_dir = cur_dir.parent
            parent_dir = parent_dir.parent

    parent_dir.size += cur_dir.size

    return directories


def get_small_dirs(directories):
    sub_total = 0
    for d in directories:
        # print(d.name, d.size, d.processed, [c.name for c in d.children], d.files)
        if d.size < 100000:
            sub_total += d.size
    return sub_total


def get_smallest_folder_to_delete(directories):
    smallest_dir_size = TOTAL_SIZE
    available_space = TOTAL_SIZE - directories[0].size

    for d in directories:
        if REQUIRED_SPACE - available_space <= d.size < smallest_dir_size:
            smallest_dir_size = d.size
    return smallest_dir_size


if __name__ == '__main__':
    _fp = open('input.txt')
    _directories = create_dirs(_fp.readlines())
    result = get_small_dirs(_directories)
    print(f'Result 1: {result}')

    result_2 = get_smallest_folder_to_delete(_directories)
    print(f'Result 2: {result_2}')
