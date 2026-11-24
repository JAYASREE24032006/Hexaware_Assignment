import random
import time

print("=" * 65)
print("DAY 2 - SET 1: E-COMMERCE CATALOGUE AND TRAFFIC ANALYSIS")
print("=" * 65)


# ================================================================
# TASK 1: BINARY SEARCH TREE OF PRODUCT CATEGORIES
# ================================================================

print("\nTASK 1: BINARY SEARCH TREE")


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, data):
        if root is None:
            return Node(data)

        if data < root.data:
            root.left = self.insert(root.left, data)
        elif data > root.data:
            root.right = self.insert(root.right, data)

        return root

    def search(self, root, key):
        if root is None or root.data == key:
            return root

        if key < root.data:
            return self.search(root.left, key)

        return self.search(root.right, key)

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.data)
            self.inorder(root.right, result)
        return result

    def preorder(self, root, result):
        if root:
            result.append(root.data)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def postorder(self, root, result):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.data)
        return result


bst = BST()

categories = [
    "Electronics", "Clothing", "Books", "Furniture",
    "Groceries", "Mobiles", "Laptops", "Shoes",
    "Watches", "Beauty", "Sports", "Toys",
    "Kitchen", "Gaming", "Accessories"
]

for category in categories:
    bst.root = bst.insert(bst.root, category)

print("15 Categories Inserted Successfully")
print("Inorder Traversal  :", bst.inorder(bst.root, []))
print("Preorder Traversal :", bst.preorder(bst.root, []))
print("Postorder Traversal:", bst.postorder(bst.root, []))

for key in ("Mobiles", "Jewellery"):
    if bst.search(bst.root, key):
        print("Category Found    :", key)
    else:
        print("Category Not Found:", key)


# ================================================================
# TASK 2: HASH TABLE WITH CHAINING AND BUILT-IN DICTIONARY
# ================================================================

print("\n\nTASK 2: HASHING AND HASH MAPS")


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        hash_value = 0

        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size

        return hash_value

    def insert(self, key, value):
        index = self.hash_function(key)

        for i, (old_key, old_value) in enumerate(self.table[index]):
            if old_key == key:
                self.table[index][i] = (key, value)
                return

        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)

        for old_key, value in self.table[index]:
            if old_key == key:
                return value

        return None


# Demonstrate a collision: two different keys, same bucket (size 16)
small_table = HashTable(16)

small_table.insert("SKU-A101", "Kettle")
small_table.insert("SKU-B201", "Toaster")

print("Collision Demonstration:")
print("SKU-A101 Hash Index:", small_table.hash_function("SKU-A101"))
print("SKU-B201 Hash Index:", small_table.hash_function("SKU-B201"))
print("Bucket Contents    :", small_table.table[small_table.hash_function("SKU-A101")])
print("SKU-A101 Lookup    :", small_table.search("SKU-A101"))
print("SKU-B201 Lookup    :", small_table.search("SKU-B201"))
print("Both keys are stored in the same bucket using chaining.")


# Create 100,000 SKUs
print("\nComparing lookup time for 100,000 SKUs...")

sku_count = 100000

custom_table = HashTable(200003)
builtin_map = {}

for i in range(sku_count):
    sku = "SKU" + str(i)
    value = "Product" + str(i)

    custom_table.insert(sku, value)
    builtin_map[sku] = value

random.seed(11)
queries = ["SKU" + str(random.randrange(sku_count)) for _ in range(sku_count)]

# Custom Hash Table Lookup
start = time.perf_counter()

for sku in queries:
    custom_table.search(sku)

custom_time = time.perf_counter() - start

# Built-in Dictionary Lookup
start = time.perf_counter()

for sku in queries:
    builtin_map.get(sku)

builtin_time = time.perf_counter() - start

print("Total SKUs:", sku_count)
print(f"Custom Hash Table Lookup Time  : {custom_time:.4f} seconds")
print(f"Built-in Dictionary Lookup Time: {builtin_time:.4f} seconds")
print(f"Built-in dictionary is about {custom_time / builtin_time:.1f} times faster")


# ================================================================
# TASK 3: GRAPH - BFS, DFS AND CYCLE DETECTION
# ================================================================

print("\n\nTASK 3: MICROSERVICE DEPLOYMENT GRAPH")

# service -> services that depend on it (edge: dependency -> dependent)
graph = {
    "Database": ["Auth", "Inventory"],
    "Auth": ["Cart", "Payment"],
    "Inventory": ["Pricing"],
    "Pricing": ["Cart"],
    "Cart": ["Checkout"],
    "Payment": ["Checkout"],
    "Checkout": ["Notification"],
    "Notification": []
}


# BFS Traversal
def bfs(graph, start):
    visited = {start}
    queue = [start]
    order = []

    while queue:
        node = queue.pop(0)
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


# DFS Traversal
def dfs(graph, node, visited=None, order=None):
    if visited is None:
        visited, order = set(), []

    visited.add(node)
    order.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, order)

    return order


# Topological Sorting using BFS (Kahn's Algorithm)
def topological_sort(graph):
    indegree = {node: 0 for node in graph}

    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1

    queue = [node for node in graph if indegree[node] == 0]
    order = []

    while queue:
        node = queue.pop(0)
        order.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(graph):
        return None

    return order


# Cycle Detection using DFS (returns the cycle path or None)
def detect_cycle(graph):
    visited = set()
    path = []

    def dfs_cycle(node):
        visited.add(node)
        path.append(node)

        for neighbor in graph[node]:
            if neighbor in path:
                return path[path.index(neighbor):] + [neighbor]
            if neighbor not in visited:
                found = dfs_cycle(neighbor)
                if found:
                    return found

        path.pop()
        return None

    for node in graph:
        if node not in visited:
            found = dfs_cycle(node)
            if found:
                return found

    return None


print("BFS Traversal:", bfs(graph, "Database"))
print("DFS Traversal:", dfs(graph, "Database"))
print("Deployment Order:", topological_sort(graph))
print("Circular Dependency:", detect_cycle(graph))

# Introduce a circular dependency
cyclic_graph = {
    "Cart": ["Pricing"],
    "Pricing": ["Inventory"],
    "Inventory": ["Payment"],
    "Payment": ["Cart"]
}

print("\nAfter Adding Circular Dependency:")
print("Circular Dependency:", " -> ".join(detect_cycle(cyclic_graph)))
print("Deployment Order:", topological_sort(cyclic_graph))


# ================================================================
# TASK 4: SLIDING WINDOW - BUSIEST CONTINUOUS 3 HOURS
# ================================================================

print("\n\nTASK 4: SLIDING WINDOW")

# Requests per minute, one value per hour (24 hours)
requests = [
    420, 380, 350, 310, 290, 340,
    520, 880, 1250, 1480, 1390, 1320,
    1410, 1350, 1290, 1330, 1480, 1620,
    1710, 1560, 1180, 860, 640, 510
]


def busiest_window(arr, window_size=3):
    current_sum = sum(arr[:window_size])
    max_sum = current_sum
    best_start = 0

    for i in range(window_size, len(arr)):
        current_sum += arr[i] - arr[i - window_size]

        if current_sum > max_sum:
            max_sum = current_sum
            best_start = i - window_size + 1

    return best_start, max_sum


start_hour, total = busiest_window(requests)

print("Total Hours:", len(requests))
print("Window Duration: 3 Hours")
print(f"Busiest Window: {start_hour:02d}:00 to {start_hour + 3:02d}:00")
print("Values in Window:", requests[start_hour:start_hour + 3])
print("Sum of Requests Per Minute:", total)
print("Average Requests Per Minute:", total / 3)


# ================================================================
# TASK 5: TWO POINTERS - GIFT CARD PAIR SUM
# ================================================================

print("\n\nTASK 5: TWO POINTERS")

order_values = [
    120, 250, 300, 350, 400, 450, 500,
    500, 550, 600, 650, 700, 800, 900, 950
]

gift_card_value = 1000


def find_pairs(arr, target):
    left = 0
    right = len(arr) - 1
    pairs = []

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            pairs.append((arr[left], arr[right]))
            left += 1
            right -= 1

            # skip repeated values so a pair is not reported twice
            while left < right and arr[left] == arr[left - 1]:
                left += 1
            while left < right and arr[right] == arr[right + 1]:
                right -= 1

        elif current_sum < target:
            left += 1

        else:
            right -= 1

    return pairs


pairs = find_pairs(order_values, gift_card_value)

print("Order Values:", order_values)
print("Gift Card Value:", gift_card_value)
print("Matching Pairs:")

for pair in pairs:
    print(pair)

print("Empty list:", find_pairs([], gift_card_value))
print("No match  :", find_pairs(order_values, 5))


# ================================================================
# FINAL DECISION TABLE
# ================================================================

print("\n\n" + "=" * 65)
print("FINAL DECISION TABLE")
print("=" * 65)

print("""
1. BST:
   Problem: Product Category Browsing
   Structure: Binary Search Tree
   Reason: Inorder gives sorted categories; O(log n) search.

2. Hashing:
   Problem: SKU Lookup
   Structure: Hash Table with Chaining / Dictionary
   Reason: Fast average O(1) lookup.

3. Graph:
   Problem: Microservice Dependencies
   Structure: Directed Graph
   Reason: BFS/DFS traversal, deployment ordering
   and cycle detection.

4. Sliding Window:
   Problem: Busiest 3-Hour Traffic
   Pattern: Sliding Window
   Reason: Avoids recalculating every 3-hour sum.

5. Two Pointers:
   Problem: Gift Card Pair Sum
   Pattern: Two Pointers
   Reason: Finds matching pairs in a sorted list
   without nested loops.
""")

print("=" * 65)
print("ALL 5 TASKS COMPLETED SUCCESSFULLY!")
print("=" * 65)
