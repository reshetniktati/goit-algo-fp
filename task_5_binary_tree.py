from task_4_heap import Node, add_edges, heap_to_tree
from typing import List, Tuple, Optional
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


def collect_nodes_bfs(root: Optional[Node]) -> List[Node]:

    """Збирає всі вузли дерева в BFS-порядку (для підрахунку N)."""
    if not root:
        return []
    q = deque([root])
    out = []
    while q:
        n = q.popleft()
        out.append(n)
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return out


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient_colors(
    n: int,
    start_rgb: Tuple[int, int, int] = (20, 40, 80),
    end_rgb: Tuple[int, int, int] = (200, 230, 255),
) -> List[str]:
    """n кольорів від темного до світлого."""
    if n <= 1:
        r, g, b = end_rgb
        return [f"#{r:02X}{g:02X}{b:02X}"]

    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = lerp(start_rgb[0], end_rgb[0], t)
        g = lerp(start_rgb[1], end_rgb[1], t)
        b = lerp(start_rgb[2], end_rgb[2], t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


def draw_tree_step(tree_root: Node, title: str = ""):
    """Одна “рамка” візуалізації."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.clf()
    if title:
        plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, node_size=2500, node_color=colors)


def visualize_bfs(root: Node, delay: float = 0.7):
    """Обхід в ширину (черга)."""
    nodes = collect_nodes_bfs(root)
    palette = gradient_colors(len(nodes))

    q = deque([root])
    visited = set()
    step = 0

    plt.figure(figsize=(9, 5))
    while q:
        node = q.popleft()
        if node.id in visited:
            continue
        visited.add(node.id)

        node.color = palette[step]
        step += 1

        draw_tree_step(root, title=f"BFS step {step}")
        plt.pause(delay)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    plt.show()


def visualize_dfs(root: Node, delay: float = 0.7):
    """Обхід в глибину (стек), pre-order: node, left, right."""
    nodes = collect_nodes_bfs(root)
    palette = gradient_colors(len(nodes))

    stack = [root]
    visited = set()
    step = 0

    plt.figure(figsize=(9, 5))
    while stack:
        node = stack.pop()
        if node.id in visited:
            continue
        visited.add(node.id)

        node.color = palette[step]
        step += 1

        draw_tree_step(root, title=f"DFS step {step}")
        plt.pause(delay)

        # щоб лівий був першим — додаємо правий, потім лівий
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    plt.show()


if __name__ == "__main__":
    heap = [1, 3, 6, 5, 9, 8]
    root = heap_to_tree(heap)
    assert root is not None

    # reset кольорів
    for n in collect_nodes_bfs(root):
        n.color = "skyblue"
    visualize_bfs(root, delay=0.6)

    for n in collect_nodes_bfs(root):
        n.color = "skyblue"
    visualize_dfs(root, delay=0.6)
