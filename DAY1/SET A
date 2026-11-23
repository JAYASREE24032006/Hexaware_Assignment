
## Set 1 – Retail Order Desk

### Business Scenario

A retail company processes thousands of customer orders every day. The order management system needs efficient searching, sorting, duplicate detection, order undo operations, dispatch queue management, and refund calculation.

---

## Task 1 – Linear Search and Binary Search

**Objective:** Search for customer orders using Linear Search and Binary Search and compare their performance.


```
import csv
import random
import time

def load_orders(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["orderId"] = int(r["orderId"])
        r["amount"] = float(r["amount"])
    return rows

def linear_search(orders, target):
    comparisons = 0
    for order in orders:
        comparisons += 1
        if order["orderId"] == target:
            return order, comparisons
    return None, comparisons

def binary_search(orders, target):
    low, high, comparisons = 0, len(orders) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if orders[mid]["orderId"] == target:
            return orders[mid], comparisons
        if orders[mid]["orderId"] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None, comparisons

def timed(fn, orders, targets):
    total_cmp = 0
    start = time.perf_counter()
    for t in targets:
        _, c = fn(orders, t)
        total_cmp += c
    return time.perf_counter() - start, total_cmp

orders = load_orders("orders.csv")
orders.sort(key=lambda o: o["orderId"])

print("Records loaded :", len(orders))
print("Sample record :", orders[0])

last_id = orders[-1]["orderId"]
t_lin, c_lin = timed(linear_search, orders, [last_id])
t_bin, c_bin = timed(binary_search, orders, [last_id])

print("\nWorst-case look-up of order", last_id)
print(f"Linear search : {c_lin} comparisons, {t_lin * 1e6:.1f} microseconds")
print(f"Binary search : {c_bin} comparisons, {t_bin * 1e6:.1f} microseconds")

random.seed(7)
targets = [random.choice(orders)["orderId"] for _ in range(1000)]

t_lin, c_lin = timed(linear_search, orders, targets)
t_bin, c_bin = timed(binary_search, orders, targets)

print("\n1,000 random look-ups")
print(f"Linear search : avg {c_lin / 1000:.1f} comparisons, total {t_lin:.4f} s")
print(f"Binary search : avg {c_bin / 1000:.1f} comparisons, total {t_bin:.4f} s")
print(f"Binary search is about {t_lin / t_bin:,.0f} times faster")

missing, c = binary_search(orders, 999999)
print("\nLook-up of a non-existent ID:", missing, "after", c, "comparisons")
```

**Time Complexity:**

- Linear Search: O(n)
- Binary Search: O(log n)

---

## Task 2 – Bubble Sort, Merge Sort and Built-in Sort

**Objective:** Sort order amounts in descending order and compare sorting algorithms.



```
import csv
import time

def bubble_sort(a, trace=False):
    a = a[:]
    n = len(a)

    for p in range(1, n):
        swapped = False
        for j in range(n - p):
            if a[j] < a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True

        if trace and p <= 3:
            print(f"After pass {p}: {a}")

        if not swapped:
            break

    return a

def merge_sort(a):
    if len(a) <= 1:
        return a

    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])

    out = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1

    return out + left[i:] + right[j:]

small = [250, 90, 410, 130, 320, 175]

print("Trace of first three bubble sort passes")
print("Initial list:", small)
bubble_sort(small, trace=True)

with open("orders.csv", newline="") as f:
    amounts = [float(r["amount"]) for r in csv.DictReader(f)][:10000]

t = time.perf_counter()
b = bubble_sort(amounts)
t_b = time.perf_counter() - t

t = time.perf_counter()
m = merge_sort(amounts)
t_m = time.perf_counter() - t

t = time.perf_counter()
s = sorted(amounts, reverse=True)
t_s = time.perf_counter() - t

print("\nBenchmark on 10,000 records")
print(f"Bubble sort O(n^2): {t_b:.4f} s")
print(f"Merge sort O(n log n): {t_m:.4f} s")
print(f"Built-in sorted(): {t_s:.4f} s")
print("All results identical:", b == m == s)
print("Top 3 amounts:", s[:3])
```

**Time Complexity:**

- Bubble Sort: O(n²)
- Merge Sort: O(n log n)
- Built-in Sorting: O(n log n)

---

## Task 3 – Duplicate Order Detection

**Objective:** Identify duplicate orders using a dictionary-based approach.


```
import csv
import time

def find_duplicates(rows):
    seen = {}
    duplicates = []

    for r in rows:
        minute = r["createdAt"][:16]
        key = (r["customerId"], r["amount"], minute)

        if key in seen:
            duplicates.append((seen[key], r["orderId"], key))
        else:
            seen[key] = r["orderId"]

    return duplicates

with open("orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))

start = time.perf_counter()
dups = find_duplicates(rows)
elapsed = time.perf_counter() - start

print("Orders scanned:", len(rows))
print("Duplicates detected:", len(dups))

for first, again, (cust, amt, minute) in dups:
    print(f"Order {first} repeated as {again} | {cust} | {amt} | {minute}")

print(f"Time taken: {elapsed * 1000:.2f} ms")
```

**Time Complexity:** O(n) average time using a dictionary.

---

## Task 4 – Stack and Queue

**Objective:** Implement Stack for undo operations and Queue for order dispatch.


```
import time
from collections import deque

class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if not self._data:
            raise IndexError("stack is empty")
        return self._data.pop()

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return not self._data

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def enqueue(self, item):
        node = Node(item)

        if self._tail:
            self._tail.next = node
        else:
            self._head = node

        self._tail = node
        self._size += 1

    def dequeue(self):
        if self._head is None:
            raise IndexError("queue is empty")

        node = self._head
        self._head = node.next

        if self._head is None:
            self._tail = None

        self._size -= 1
        return node.value

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

order = {"orderId": 100001, "amount": 168.94}
undo = Stack()

print("Undo last order edit")

for new_amount in (180.00, 195.50, 210.00):
    undo.push(order["amount"])
    order["amount"] = new_amount
    print(f"Edited amount to {new_amount:.2f}")

order["amount"] = undo.pop()
print(f"Undo -> amount restored to {order['amount']:.2f}")

order["amount"] = undo.pop()
print(f"Undo -> amount restored to {order['amount']:.2f}")

print("\nDispatch line (FIFO)")

line = Queue()

for oid in (100001, 100002, 100003, 100004):
    line.enqueue(oid)
    print("Queued:", oid)

while not line.is_empty():
    print("Shipped:", line.dequeue())

N = 200000

def bench(label, fn):
    start = time.perf_counter()
    fn()
    return label, time.perf_counter() - start

def custom_stack():
    s = Stack()
    for i in range(N):
        s.push(i)
    while not s.is_empty():
        s.pop()

def builtin_stack():
    s = []
    for i in range(N):
        s.append(i)
    while s:
        s.pop()

def custom_queue():
    q = Queue()
    for i in range(N):
        q.enqueue(i)
    while not q.is_empty():
        q.dequeue()

def builtin_queue():
    q = deque()
    for i in range(N):
        q.append(i)
    while q:
        q.popleft()

def list_as_queue():
    q = list(range(N // 4))
    while q:
        q.pop(0)

print("\nTiming")

tests = [
    ("Custom Stack", custom_stack),
    ("Built-in list as stack", builtin_stack),
    ("Custom Queue", custom_queue),
    ("Built-in deque", builtin_queue),
    ("List as queue", list_as_queue)
]

for label, fn in tests:
    name, secs = bench(label, fn)
    print(f"{name:<25} {secs:.4f} s")
```

**Concepts Used:**

- Stack: LIFO (Last In, First Out)
- Queue: FIFO (First In, First Out)

---

## Task 5 – Greedy Algorithm and Dynamic Programming

**Objective:** Calculate the minimum number of notes and coins required for a refund and compare Greedy with Dynamic Programming.


```
def greedy_change(coins, amount):
    count, used = 0, []

    for c in sorted(coins, reverse=True):
        take = amount // c

        if take:
            used.append((c, take))
            count += take
            amount -= take * c

    return (count, used) if amount == 0 else (None, used)

def dp_change(coins, amount):
    INF = float("inf")
    best = [0] + [INF] * amount
    pick = [0] * (amount + 1)

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
                pick[a] = c

    if best[amount] == INF:
        return None, [], best

    used = []
    a = amount

    while a > 0:
        used.append(pick[a])
        a -= pick[a]

    return best[amount], sorted(used, reverse=True), best

print("Part A - Indian notes and coins")

inr = [500, 200, 100, 50, 20, 10, 5, 2, 1]
refund = 3787

n, used = greedy_change(inr, refund)

print(f"Refund Rs.{refund}: {n} notes/coins ->",
      ", ".join(f"{c} x {k}" for c, k in used))

n2, _, _ = dp_change(inr, refund)
print("DP gives the same minimum:", n2)

print("\nPart B - Denomination set where greedy fails")

for coins, amount in (([1, 3, 4], 6), ([1, 7, 10], 14)):
    g, g_used = greedy_change(coins, amount)
    d, d_used, table = dp_change(coins, amount)

    g_list = [c for c, k in g_used for _ in range(k)]

    print("Denominations:", coins, "Refund:", amount)
    print("Greedy:", g, "coins ->", g_list)
    print("DP:", d, "coins ->", d_used)

print("\nDP table for denominations [1, 3, 4], refund 6")

_, _, table = dp_change([1, 3, 4], 6)

print("Amount:", *range(7))
print("Coins:", *table)
```

**Time Complexity:**

- Greedy: O(n log n) including sorting denominations
- Dynamic Programming: O(amount × number of denominations)

---
