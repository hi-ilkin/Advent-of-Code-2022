import numpy as np

# For part one, set both values to 1
MIX_COUNT = 10
DECRYPTION_KEY = 811589153

original_input = np.loadtxt('input.txt', dtype=np.int64) * DECRYPTION_KEY
inputs_with_position = np.vstack([np.arange(0, len(original_input)), original_input])
input_len = len(original_input)


def calculate_coordinates():
    item = np.where(inputs_with_position[1, :] == 0)[0][0]
    special_val_idx = [(item + nth) % input_len for nth in [1000, 2000, 3000]]
    special_vals = inputs_with_position[0:, special_val_idx][1, :]

    print(f'Specials: {special_vals}')
    print(f'Final result: {np.sum(special_vals)}')


def move_item(items, value, old_pos):
    new_pos = (value + old_pos) % (input_len - 1)

    item_to_insert = items[:, old_pos]
    items = np.delete(items, old_pos, 1)
    items = np.insert(items, new_pos,
                      item_to_insert,
                      axis=1)

    # print(f'Move {item_to_insert} to {new_pos} from {old_pos}')
    return items


def main():
    global inputs_with_position
    for _ in range(MIX_COUNT):
        for idx, value in enumerate(original_input):
            item = np.where(inputs_with_position[0, :] == idx)[0][0]
            # print(f'Item : {item}')

            inputs_with_position = move_item(inputs_with_position, value, item)

            # print(inputs_with_position)
            # print()

    calculate_coordinates()


if __name__ == '__main__':
    main()
