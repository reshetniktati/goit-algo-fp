from __future__ import annotations

import uuid
from collections import deque
from typing import List, Tuple, Optional

import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key: int, color: str = "skyblue"):
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph: nx.DiGraph, node: Optional[Node], pos: dict, x=0, y=0, layer=1):
    """Рекурсивно додає вузли й ребра в граф (лише для побудови структури)."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            lx = x - 1 / 2 ** layer
            pos[node.left.id] = (lx, y - 1)
            add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            rx = x + 1 / 2 ** layer
            pos[node.right.id] = (rx, y - 1)
            add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)
    return graph


def heap_to_tree(heap: List[int]) -> Optional[Node]:
    """Створює бінарне дерево з масиву купи (індексація: i -> 2i+1, 2i+2)."""
    if not heap:
        return None

    nodes = [Node(v) for v in heap]
    for i in range(len(nodes)):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(nodes):
            nodes[i].left = nodes[li]
        if ri < len(nodes):
            nodes[i].right = nodes[ri]
    return nodes[0]

def draw_tree(tree_root, *, save_path=None):
    """Малює дерево. Якщо save_path заданий — зберігає PNG."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        node_size=2500,
        node_color=colors
    )

    # Якщо треба зберегти png — savefig має бути ДО plt.show()
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=200)

    plt.show()



if __name__ == "__main__":
    # приклад: мін-купа
    heap = [1, 3, 6, 5, 9, 8]
    root = heap_to_tree(heap)
    draw_tree(root, save_path="heap_tree.png")
