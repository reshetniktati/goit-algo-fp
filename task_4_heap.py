import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає вузли/ребра в граф та рахує координати для малювання."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            lx = x - 1 / 2**layer
            pos[node.left.id] = (lx, y - 1)
            add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            rx = x + 1 / 2**layer
            pos[node.right.id] = (rx, y - 1)
            add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


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


def heap_to_tree(heap_list):
    """
    Перетворює бінарну купу (масив) у дерево Node.
    Важливо: heap_list має відображати структуру купи в масиві.
    """
    if not heap_list:
        return None

    nodes = [Node(value) for value in heap_list]

    for i in range(len(nodes)):
        left_i = 2 * i + 1
        right_i = 2 * i + 2

        if left_i < len(nodes):
            nodes[i].left = nodes[left_i]
        if right_i < len(nodes):
            nodes[i].right = nodes[right_i]

    return nodes[0]


# ====== ПРИКЛАД 1: якщо у тебе вже є купа у вигляді масиву ======
heap_data = [0, 3, 1, 4, 10, 8, 2]
root = heap_to_tree(heap_data)
draw_tree(root, save_path="./heap.png")


# ====== ПРИКЛАД 2: min-heap зі звичайного списку ======
data = [10, 4, 7, 1, 3, 9, 2]
heapq.heapify(data)  # тепер data — це min-heap у вигляді масиву
root2 = heap_to_tree(data)
draw_tree(root2, save_path="./heap_heapify.png")
