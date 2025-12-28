import heapq
import networkx as nx
import matplotlib.pyplot as plt


def dijkstra_heap(graph: nx.Graph, start):
    """
    Алгоритм Дейкстри з бінарною купою (heapq).
    Повертає:
      dist  - найкоротші відстані від start до всіх вершин
      prev  - попередники для відновлення маршруту
    """
    # Ініціалізація: всім нескінченність, старту 0
    dist = {v: float("inf") for v in graph.nodes}
    prev = {v: None for v in graph.nodes}
    dist[start] = 0

    # Купа містить пари (поточна_відстань, вершина)
    heap = [(0, start)]

    while heap:
        cur_dist, u = heapq.heappop(heap)

        # Якщо витягнули "застарілий" запис — пропускаємо
        if cur_dist != dist[u]:
            continue

        # Релаксація ребер
        for v, attrs in graph[u].items():
            w = attrs.get("weight", 1)  # якщо ваги нема — вважаємо 1
            new_dist = cur_dist + w

            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def restore_path(prev, start, target):
    """Відновлення шляху start -> target за словником prev."""
    if start == target:
        return [start]

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]

    path.reverse()
    # Якщо старт не досягнуто — шляху нема
    if not path or path[0] != start:
        return []
    return path


def build_weighted_graph():
    """
    Приклад: умовна 'транспортна лінія' (станції з твого списку).
    Ваги — умовні (наприклад, хвилини між станціями).
    """
    G = nx.Graph()

    edges = [
        ("Bakirkoy", "Zeytinburnu", 6),
        ("Zeytinburnu", "Topkapi", 5),
        ("Topkapi", "Aksaray", 4),
        ("Aksaray", "Yenikapi", 3),
        ("Yenikapi", "Taksim", 10),
        ("Taksim", "Sisli", 4),
        ("Sisli", "Mecidiyekoy", 3),
        ("Mecidiyekoy", "Levent", 6),
        ("Aksaray", "Taksim", 12),
    ]

    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    return G


def draw_and_save_png(G: nx.Graph, filename="graph.png"):
    """
    Візуалізація графа і збереження в PNG.
    """
    plt.figure(figsize=(12, 6))

    # Розкладка вузлів (щоб виглядало стабільно)
    pos = nx.spring_layout(G, seed=42)

    # Малюємо вершини/ребра
    nx.draw_networkx_nodes(G, pos, node_size=1200)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Підписи ваг ребер
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.axis("off")
    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()  # закриваємо фігуру, щоб не "залипала" в середовищі


if __name__ == "__main__":
    G = build_weighted_graph()

    # 1) Аналіз базових характеристик
    print("К-сть вершин:", G.number_of_nodes())
    print("К-сть ребер:", G.number_of_edges())
    print("Ступені вершин:", dict(G.degree()))

    # 2) Дейкстра з купою
    start = "Bakirkoy"
    dist, prev = dijkstra_heap(G, start)

    print("\nНайкоротші відстані від", start)
    for node in G.nodes:
        print(f"  -> {node}: {dist[node]}")

    # Приклад: відновимо шлях до Levent
    target = "Levent"
    path = restore_path(prev, start, target)
    print(f"\nШлях {start} -> {target}:", " -> ".join(path) if path else "нема шляху")

    # 3) Збережемо png
    draw_and_save_png(G, filename="istanbul_graph.png")
    print("\nPNG збережено у файл: istanbul_graph.png")
