from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, Tuple


@dataclass
class Node:
    value: int
    next: Optional["Node"] = None


class SinglyLinkedList:
    def __init__(self, values: Iterable[int] = ()):
        self.head: Optional[Node] = None
        for v in values:
            self.append(v)

    def append(self, value: int) -> None:
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def to_list(self) -> list[int]:
        out: list[int] = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    # -------- Task 1.1: Reverse (in-place by pointers) --------
    def reverse(self) -> None:
        prev: Optional[Node] = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    # -------- Task 1.2: Sort (merge sort for linked list) --------
    def sort(self) -> None:
        self.head = merge_sort(self.head)


# ---------- Helpers for merge sort ----------
def split_middle(head: Node) -> Tuple[Optional[Node], Optional[Node]]:
    """
    Split list into two halves using slow/fast pointers.
    Returns (left_head, right_head).
    """
    slow: Node = head
    fast: Optional[Node] = head
    prev: Optional[Node] = None

    while fast and fast.next:
        prev = slow
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next

    # cut
    if prev:
        prev.next = None

    left = head
    right = slow
    return left, right


def merge_sorted_lists(a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
    """
    -------- Task 1.3: Merge two sorted singly linked lists --------
    Returns head of merged sorted list.
    """
    dummy = Node(0)
    tail = dummy

    while a and b:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a else b
    return dummy.next


def merge_sort(head: Optional[Node]) -> Optional[Node]:
    if head is None or head.next is None:
        return head

    left, right = split_middle(head)  # two halves
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)

    return merge_sorted_lists(left_sorted, right_sorted)


# ----------------- Demo -----------------
if __name__ == "__main__":
    ll = SinglyLinkedList([4, 1, 9, 2, 2, 7])
    print("Original:", ll.to_list())

    ll.reverse()
    print("Reversed:", ll.to_list())

    ll.sort()
    print("Sorted:", ll.to_list())

    a = SinglyLinkedList([1, 3, 5])
    b = SinglyLinkedList([2, 4, 6, 7])

    merged_head = merge_sorted_lists(a.head, b.head)
    merged = SinglyLinkedList()
    merged.head = merged_head
    print("Merged:", merged.to_list())
