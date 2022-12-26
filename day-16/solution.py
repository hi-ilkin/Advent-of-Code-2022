
from copy import copy, deepcopy

import numpy as np


class Node:

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.connections = []


class Path:

    def __init__(self):
        self.total_value = 0
        self.flow_every_minute = 0
        self.visited_nodes = []

    def add_initial_nodes(self, from_node, to_node):
        self.visited_nodes.append(from_node)
        self.visited_nodes.append(to_node)

    def update(self):
        self.total_value += self.flow_every_minute

        cur = self.visited_nodes[-1]
        final_node = cur.connections[-1]

        result = []

        if cur == self.visited_nodes[-2] and final_node == self.visited_nodes[3]:
            return None

        if cur.rate > 0:
            split_path = Path()
            split_path.visited_nodes = deepcopy(self.visited_nodes)
            split_path.total_value = deepcopy(split_path.total_value)
            split_path.flow_every_minute += cur.rate
            result.append(split_path)

        for _, connection in enumerate(cur.connections[:-1]):
            split_path = Path()
            split_path.visited_nodes = deepcopy(self.visited_nodes)
            split_path.total_value = deepcopy(self.total_value)
            split_path.visited_nodes.append(connection)
            result.append(split_path)

        self.visited_nodes.append(final_node)
        return set(result)


a = Node('AA', 0)
b = Node('BB', 13)
c = Node('CC', 2)
d = Node('DD', 20)
e = Node('EE', 3)
f = Node('FF', 0)
g = Node('GG', 0)
h = Node('HH', 22)
i = Node('II', 0)
j = Node('JJ', 21)

a.connections = [d, i, b]
b.connections = [c, a]
c.connections = [d, b]
d.connections = [c, a, e]
e.connections = [f, d]
f.connections = [e, g]
g.connections = [f, h]
h.connections = [g]
i.connections = [a, j]
j.connections = [i]

possible_paths = []


def create_path(from_node, to_node):
    path = Path()
    path.add_initial_nodes(from_node, to_node)
    return path


possible_paths.append(create_path(a, d))
possible_paths.append(create_path(a, b))
possible_paths.append(create_path(a, i))


def should_we_keep_path(path, avg_flow, cur_iteration, best_path):
    # return (path.total_value + highest_flow * (30 - cur_iteration)) > best_path.flow_every_minute * (30 - cur_iteration)
    return path.flow_every_minute > avg_flow or cur_iteration < 5


def get_best_path(paths):
    return max(paths, key=lambda x: x.flow_every_minute)


visited = []

for it in range(30):
    print(f'Processing iteration: {it}')
    paths_to_add = []

    average_flow = np.average([path.flow_every_minute for path in possible_paths])
    print(f'Number of possible paths before: {len(possible_paths)} / avg flow: {average_flow}')
    possible_paths = list(
        filter(lambda x: should_we_keep_path(x, average_flow * 1.5, it, None), possible_paths))
    print(f'Number of possible paths after: {len(possible_paths)}')

    for p in possible_paths:
        append_path = p.update()
        # append_path = list(
        #     filter(lambda x: should_we_keep_path(x, average_flow, it, None), append_path))
        if len(append_path) != 0:
            paths_to_add.extend(append_path)

    if len(paths_to_add) != 0:
        possible_paths.extend(paths_to_add)

for p in possible_paths:
    print(p.total_value, p.flow_every_minute)
    for v in p.visited_nodes:
        print(v.name, end=",")
    print()
