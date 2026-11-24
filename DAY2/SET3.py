import re

print("=" * 65)
print("DAY 2 - SET 3: LOGISTICS NETWORK AND DELIVERY WINDOWS")
print("=" * 65)


# ================================================================
# TASK 1: BINARY SEARCH TREE OF HUB CODES AND TREE HEIGHT
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

    def search(self, key):
        node = self.root
        comparisons = 0

        while node:
            comparisons += 1
            if key == node.data:
                return True, comparisons
            node = node.left if key < node.data else node.right

        return False, comparisons

    def height(self, root):
        if root is None:
            return 0
        return 1 + max(self.height(root.left), self.height(root.right))


def build(codes):
    tree = BST()
    for code in codes:
        tree.root = tree.insert(tree.root, code)
    return tree


hubs = ["MUM", "DEL", "BLR", "CHE", "HYD", "KOL",
        "PUN", "AMD", "JAI", "LKO", "NAG"]

mixed_order = ["MUM", "DEL", "PUN", "BLR", "KOL", "NAG",
               "AMD", "CHE", "JAI", "HYD", "LKO"]
sorted_order = sorted(hubs)

mixed_tree = build(mixed_order)
sorted_tree = build(sorted_order)

print("Number of hubs:", len(hubs), "| minimum possible height: 4")
print("Mixed insertion order :", mixed_order)
print("  Height =", mixed_tree.height(mixed_tree.root))
print("Sorted insertion order:", sorted_order)
print("  Height =", sorted_tree.height(sorted_tree.root))
print("  Sorted input makes every hub the right child of the previous one,")
print("  so the tree becomes a linked list and search drops to O(n).")

print("\nSearch for NAG:")
print("  Mixed tree  :", mixed_tree.search("NAG")[1], "comparisons")
print("  Sorted tree :", sorted_tree.search("NAG")[1], "comparisons")
print("Search for XXX (absent):", mixed_tree.search("XXX"))


# ================================================================
# TASK 2: HASH MAP - PARCELS SCANNED TWICE AT THE SAME HUB
# ================================================================

print("\n\nTASK 2: PARCEL TRACKING USING HASH MAP")

scans = [
    ("TRK1001", "MUM"), ("TRK1002", "MUM"), ("TRK1001", "DEL"),
    ("TRK1003", "BLR"), ("TRK1002", "MUM"),          # TRK1002 repeated at MUM
    ("TRK1004", "CHE"), ("TRK1003", "HYD"), ("TRK1003", "BLR"),
    ("TRK1001", "DEL"),                              # TRK1001 repeated at DEL
]


def build_lookup(scans):
    lookup = {}               # tracking number -> {hub: scan count}

    for tracking, hub in scans:
        if tracking not in lookup:
            lookup[tracking] = {}
        lookup[tracking][hub] = lookup[tracking].get(hub, 0) + 1

    return lookup


def scanned_twice(lookup):
    result = []

    for tracking, hub_counts in lookup.items():
        for hub, count in hub_counts.items():
            if count > 1:
                result.append((tracking, hub, count))

    return result


lookup = build_lookup(scans)

print("Scans processed :", len(scans))
print("Parcels tracked :", len(lookup))
print("TRK1003 history :", lookup["TRK1003"])

print("\nParcels scanned more than once at the same hub:")
for tracking, hub, count in scanned_twice(lookup):
    print(f"  {tracking} at {hub}: {count} scans")

print("\nTest Cases:")
print("  Empty input     :", scanned_twice(build_lookup([])))
print("  Unknown parcel  :", lookup.get("TRK9999", "not found"))
print("  Same hub 3 times:", scanned_twice(build_lookup([("A", "X")] * 3)))


# ================================================================
# TASK 3: GRAPH - ADJACENCY LIST, BFS AND DFS
# ================================================================

print("\n\nTASK 3: HUB NETWORK GRAPH")

# Adjacency list of 10 hubs (NAG is the central depot)
routes = {
    "NAG": ["MUM", "HYD", "DEL"],
    "MUM": ["NAG", "PUN", "AMD"],
    "PUN": ["MUM", "BLR"],
    "AMD": ["MUM", "DEL"],
    "DEL": ["NAG", "AMD", "JAI"],
    "JAI": ["DEL"],
    "HYD": ["NAG", "BLR"],
    "BLR": ["PUN", "HYD", "CHE"],
    "CHE": ["BLR"],
    "KOL": []                      # not yet linked to the network
}

print("Adjacency List:")
for hub, neighbours in routes.items():
    print(f"  {hub} -> {neighbours}")


# BFS: route with the fewest hops
def fewest_hops(graph, start, goal):
    parent = {start: None}
    queue = [start]

    while queue:
        node = queue.pop(0)

        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]

        for neighbor in graph[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)

    return None


# DFS: every hub reachable from the depot
def reachable(graph, node, visited=None, order=None):
    if visited is None:
        visited, order = set(), []

    visited.add(node)
    order.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            reachable(graph, neighbor, visited, order)

    return order


path = fewest_hops(routes, "JAI", "CHE")
print("\nFewest hops JAI -> CHE:", " -> ".join(path), f"({len(path) - 1} hops)")
print("Fewest hops NAG -> KOL:", fewest_hops(routes, "NAG", "KOL"))

found = reachable(routes, "NAG")
print("\nHubs reachable from depot NAG (DFS order):", found)
print("Count:", len(found), "| not reachable:", sorted(set(routes) - set(found)))


# ================================================================
# TASK 4: SLIDING WINDOW - 4-HOUR WINDOW WITH HIGHEST AVERAGE
# ================================================================

print("\n\nTASK 4: SLIDING WINDOW")

parcels = [
    120, 95, 80, 70, 65, 110, 240, 410, 560, 620, 580, 540,
    600, 570, 520, 530, 610, 690, 720, 650, 480, 320, 210, 150
]


def best_average_window(arr, k):
    if k <= 0 or k > len(arr):
        return None

    current_sum = sum(arr[:k])
    max_sum = current_sum
    best_start = 0

    for i in range(k, len(arr)):
        current_sum += arr[i] - arr[i - k]

        if current_sum > max_sum:
            max_sum = current_sum
            best_start = i - k + 1

    return best_start, max_sum / k


start_hour, average = best_average_window(parcels, 4)

print("Hourly Parcel Counts:", parcels)
print(f"Best 4-hour window: {start_hour:02d}:00 to {start_hour + 4:02d}:00")
print("Counts in window  :", parcels[start_hour:start_hour + 4])
print(f"Average per hour  : {average:.2f}")
print("Window longer than data:", best_average_window([5, 6], 4))


# ================================================================
# TASK 5: TWO POINTERS - ROUTE PALINDROME OF HUB CODES
# ================================================================

print("\n\nTASK 5: TWO POINTERS")


def is_route_palindrome(route):
    # split on any separator (-, >, comma, space) and ignore letter case
    codes = [c.lower() for c in re.split(r"[^A-Za-z0-9]+", route) if c]

    left = 0
    right = len(codes) - 1

    while left < right:
        if codes[left] != codes[right]:
            return False
        left += 1
        right -= 1

    return True


routes_to_check = [
    "MUM-DEL-BLR-DEL-MUM",
    "mum > del > blr > del > MUM",
    "MUM,DEL,BLR,CHE",
    "MUM - DEL - del - mum",
    "BLR-CHE-blr",
    "DEL",
    "",
    "MUM-DEL-MUM-DEL"
]

print(f"{'Route description':<32}{'Palindrome'}")
for route in routes_to_check:
    print(f"{route!r:<32}{is_route_palindrome(route)}")


# ================================================================
# ALGORITHM CHOICES
# ================================================================

print("\n\n" + "=" * 65)
print("ALGORITHM CHOICES")
print("=" * 65)

print("""
1. BST:
   Problem: Storing and searching hub codes
   Reason: O(log n) search and insert when balanced. Sorted insertion
   turns the tree into a chain (height n), so search becomes O(n).

2. Hash Map:
   Problem: Parcel look-up and repeat-scan check
   Reason: O(1) average look-up and update for every scan.

3. Graph (Adjacency List):
   Problem: Hub-to-hub routing
   Reason: Sparse network, so O(V + E) space. BFS gives the fewest
   hops; DFS lists every hub reachable from the depot.

4. Sliding Window:
   Problem: Best 4-hour delivery window
   Reason: Each hour is added and removed once, O(n).

5. Two Pointers:
   Problem: Route palindrome
   Reason: Compare from both ends, stop at first mismatch, O(n).
""")

print("=" * 65)
print("ALL 5 TASKS COMPLETED SUCCESSFULLY!")
print("=" * 65)
