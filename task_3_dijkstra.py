import heapq
from math import inf
from typing import Dict, List, Tuple, Any


Graph = Dict[Any, List[Tuple[Any, float]]]


def dijkstra(graph: Graph, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
    """
    Повертає:
      dist[v] = найкоротша відстань від start до v
      prev[v] = попередник v у найкоротшому шляху (для відновлення маршруту)
    """
    dist: Dict[Any, float] = {v: inf for v in graph}
    prev: Dict[Any, Any] = {v: None for v in graph}

    dist[start] = 0.0
    heap: List[Tuple[float, Any]] = [(0.0, start)]  # (distance, vertex)

    while heap:
        cur_dist, u = heapq.heappop(heap)

        # Якщо витягли "застарілий" запис — пропускаємо
        if cur_dist != dist[u]:
            continue

        for v, w in graph[u]:
            if w < 0:
                raise ValueError("Dijkstra не працює з від’ємними вагами ребер.")
            nd = cur_dist + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, prev


def restore_path(prev: Dict[Any, Any], start: Any, target: Any) -> List[Any]:
    """Відновлює шлях start -> target за словником prev."""
    if start == target:
        return [start]

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    if not path or path[0] != start:
        return []  # недосяжно
    return path


def main():
    # Приклад графа
    graph: Graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2)],
        "E": [("C", 10), ("D", 2)],
    }

    start = "A"
    dist, prev = dijkstra(graph, start)

    print("Найкоротші відстані від", start)
    for v in dist:
        print(f"  {v}: {dist[v]}")

    target = "E"
    path = restore_path(prev, start, target)
    print(f"\nШлях {start} -> {target}:", " -> ".join(path) if path else "недосяжно")


if __name__ == "__main__":
    main()
