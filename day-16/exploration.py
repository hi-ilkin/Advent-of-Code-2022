from itertools import product
from itertools import combinations

import numpy as np

# 'AHDJBEC'
cost_matrix = {
    'AB': 1,
    'AD': 1,
    'AH': 5,
    'AJ': 2,
    'AE': 2,
    'AC': 2,
    'HD': 4,
    'HJ': 7,
    'HB': 6,
    'HE': 3,
    'HC': 5,
    'DJ': 3,
    'DB': 2,
    'DE': 1,
    'DC': 1,
    'JB': 3,
    'JE': 4,
    'JC': 4,
    'BE': 3,
    'BC': 1,
    'EC': 2
}

rewards = {
    'H': 22,
    'J': 21,
    'D': 20,
    'B': 13,
    'E': 3,
    'C': 2
}


def get_cost(p1, p2):
    key = ''.join([p1, p2])
    return cost_matrix.get(key, cost_matrix.get(key[::-1]))


def get_possible_future_rewards(paths):
    available_rewards = sorted([rewards[p] for p in paths])
    return sum([(i + 1) * r for i, r in enumerate(available_rewards)])


all_nodes = ['H', 'J', 'D', 'B', 'E', 'C']


# possible_paths = ['D', 'B', 'J', 'H', 'E', 'C']


# possible_paths = ['D', 'H', 'J', 'B', 'E', 'C']


def find_optimal_next_node(start, unvisited_nodes, remaining_steps):
    max_future_reward = 0
    possible_opt_paths = []
    tmp_unvisited = unvisited_nodes.copy()

    while len(tmp_unvisited) > 0:
        nodes_to_visit = unvisited_nodes.copy()
        cur_node = tmp_unvisited.pop(0)
        nodes_to_visit.remove(cur_node)

        steps = remaining_steps - get_cost(start, cur_node) - 1
        cur_future_reward = steps * (rewards[cur_node]) + get_possible_future_rewards(nodes_to_visit)
        print(f'Node: {cur_node} max future: {max_future_reward} cur future: {cur_future_reward}')

        if cur_future_reward > max_future_reward:
            possible_opt_paths = [(cur_node, steps)]
            max_future_reward = cur_future_reward
        elif cur_future_reward == max_future_reward:
            possible_opt_paths.append((cur_node, steps))
    return possible_opt_paths


def find_optimal_path():
    nodes = all_nodes.copy()
    unvisited_nodes = nodes.copy()
    start = 'A'
    possible_start_nodes = find_optimal_next_node(start, unvisited_nodes, remaining_steps=30)
    print(possible_start_nodes)

    optimal_path = [possible_start_nodes[0]]
    node, remaining_steps = possible_start_nodes[0]
    print(unvisited_nodes, node)
    unvisited_nodes.remove(node)

    while len(unvisited_nodes) != 0:
        next_optimal_node = find_optimal_next_node(node, unvisited_nodes, remaining_steps)
        optimal_path.append(next_optimal_node[0])
        node, remaining_steps = next_optimal_node[0]
        unvisited_nodes.remove(node)

    print(optimal_path)


def main():
    start = 'A'
    total_flow = 0
    prev_cost = 0
    cur_path = ['A']

    un_visited_points = all_nodes.copy()
    remaining_steps = 30

    while len(un_visited_points) != 0:
        next_node = un_visited_points.pop(0)
        cur_path.append(next_node)
        possible_future_reward = get_possible_future_rewards(un_visited_points)

        remaining_steps -= get_cost(start, next_node) + 1
        total_flow += remaining_steps * rewards[next_node]

        print(
            f'{remaining_steps}: Start: {start} next_node: {next_node} cost: {get_cost(start, next_node)},  '
            f'reward: {rewards[next_node]} added to flow: {remaining_steps * rewards[next_node]} '
            f'total flow: {total_flow} possible future reward: {get_possible_future_rewards(un_visited_points)}')

        start = next_node

    print(''.join(cur_path), total_flow)


find_optimal_path()
