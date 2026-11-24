import re

print("=" * 65)
print("DAY 2 - SET 2: INSURANCE CLAIMS PROCESSING")
print("=" * 65)


# ================================================================
# TASK 1: BINARY SEARCH TREE OF CLAIM IDS
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
        self.size = 0

    def insert(self, root, data):
        if root is None:
            self.size += 1
            return Node(data)

        if data < root.data:
            root.left = self.insert(root.left, data)
        elif data > root.data:
            root.right = self.insert(root.right, data)
        # equal: duplicate claim ID is ignored

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


claim_ids = [5040, 3020, 7010, 2010, 4050, 6030, 8080, 3550, 4800, 9100]

bst = BST()

for cid in claim_ids:
    bst.root = bst.insert(bst.root, cid)

print("Inserted in this order:", claim_ids)
print("Inorder Traversal  :", bst.inorder(bst.root, []))
print("Preorder Traversal :", bst.preorder(bst.root, []))
print("Postorder Traversal:", bst.postorder(bst.root, []))
print("Inorder is sorted  :", bst.inorder(bst.root, []) == sorted(claim_ids))
print("Search 6030        :", bst.search(bst.root, 6030) is not None)
print("Search 1234        :", bst.search(bst.root, 1234) is not None)

bst.root = bst.insert(bst.root, 5040)
print("Duplicate 5040 ignored, size still:", bst.size)

empty = BST()
print("Empty tree: inorder =", empty.inorder(empty.root, []),
      "| search =", empty.search(empty.root, 1))

print("\nINORDER traversal gives claims in sorted order, because it visits")
print("the left subtree (smaller IDs), then the node, then the right subtree.")


# ================================================================
# TASK 2: HASHING - DUPLICATE AND NEAR-DUPLICATE CLAIMS
# ================================================================

print("\n\nTASK 2: DUPLICATE CLAIM DETECTION USING HASHING")


def normalise(policy, date):
    # ignore letter case and any spacing
    return (re.sub(r"\s+", "", policy).upper(), date.strip())


def find_duplicates(claims):
    seen = {}          # key -> first claim id
    duplicates = []

    for claim_id, policy, date in claims:
        key = normalise(policy, date)

        if key in seen:
            duplicates.append((seen[key], claim_id, key))
        else:
            seen[key] = claim_id

    return duplicates


claims = [
    ("C001", "pol-1001", "2026-03-10"),
    ("C002", "POL-2002", "2026-03-10"),
    ("C003", "POL-1001", "2026-03-10"),       # case only
    ("C004", "POL 3003", "2026-03-11"),
    ("C005", "POL3003", "2026-03-11"),        # spacing only
    ("C006", "POL-1001", "2026-03-12"),       # different date: valid claim
    ("C007", " Pol-2002 ", "2026-03-10"),     # case and spacing
    ("C008", "POL-1001", "2026-03-10"),       # exact repeat
]

print("Duplicates found:")
for first, again, key in find_duplicates(claims):
    print(f"  {first} and {again} -> {key}")

print("\nTest Cases:")
print("  Empty input     :", find_duplicates([]))
print("  Single claim    :", find_duplicates([("X1", "P1", "2026-01-01")]))
print("  All identical   :",
      len(find_duplicates([("A", "p 1", "d"), ("B", "P1", "d"), ("C", "P 1", "d")])),
      "duplicates")
print("  Different dates :", find_duplicates([("A", "P1", "d1"), ("B", "P1", "d2")]))

# Collision handling
print("\nCollision Handling:")
print("hash(8) % 8 =", hash(8) % 8, "| hash(16) % 8 =", hash(16) % 8, "-> same slot")
table = {8: "claim for key 8", 16: "claim for key 16"}
print("Both keys are stored and found:", table[8], "|", table[16])
print("Python's dict uses open addressing: on a collision it probes for a free")
print("slot and compares the full key, so two different claims never look equal.")
print("A chained table would keep both keys in one bucket list instead.")


# ================================================================
# TASK 3: GRAPH - CLAIM APPROVAL STAGES (BFS AND DFS)
# ================================================================

print("\n\nTASK 3: CLAIM APPROVAL STAGES GRAPH")

stages = {
    "Registration": ["Assessment"],
    "Assessment": ["Surveyor", "Settlement"],
    "Surveyor": ["Assessment", "Settlement"],   # sent back for re-assessment
    "Settlement": []
}


# BFS shortest path
def shortest_path(graph, start, goal):
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


# Loop detection using DFS
def find_loop(graph):
    visited = set()
    path = []

    def dfs(node):
        visited.add(node)
        path.append(node)

        for neighbor in graph[node]:
            if neighbor in path:
                return path[path.index(neighbor):] + [neighbor]
            if neighbor not in visited:
                found = dfs(neighbor)
                if found:
                    return found

        path.pop()
        return None

    for node in graph:
        if node not in visited:
            found = dfs(node)
            if found:
                return found

    return None


path = shortest_path(stages, "Registration", "Settlement")
print("Shortest path Registration -> Settlement:", " -> ".join(path),
      f"({len(path) - 1} steps)")
print("Shortest path Surveyor -> Registration  :",
      shortest_path(stages, "Surveyor", "Registration"))
print("Loop found with DFS:", " -> ".join(find_loop(stages)))

one_way = {
    "Registration": ["Assessment"],
    "Assessment": ["Surveyor"],
    "Surveyor": ["Settlement"],
    "Settlement": []
}
print("\nStrict one-way flow, loop:", find_loop(one_way))


# ================================================================
# TASK 4: SLIDING WINDOW - LONGEST RUN ABOVE 100 CLAIMS
# ================================================================

print("\n\nTASK 4: SLIDING WINDOW")


def longest_run_above(daily, limit=100):
    left = 0
    best = 0
    best_start = 0

    for right, value in enumerate(daily):
        if value <= limit:
            left = right + 1          # window broken: restart after this day
        elif right - left + 1 > best:
            best = right - left + 1
            best_start = left

    return best, best_start


daily_claims = [80, 95, 110, 130, 150, 90, 105, 120, 99,
                140, 160, 175, 180, 101, 60, 120, 130]

length, begin = longest_run_above(daily_claims)

print("Daily Claims:", daily_claims)
print(f"Longest run above 100: {length} days (day {begin + 1} to day {begin + length})")
print("Values in the run:", daily_claims[begin:begin + length])

print("\nTest Cases:")
print("  Empty input    :", longest_run_above([]))
print("  None above 100 :", longest_run_above([50, 100, 99]))
print("  All above 100  :", longest_run_above([101, 200, 150]))
print("  Exactly 100    :", longest_run_above([100, 100]))


# ================================================================
# TASK 5: TWO POINTERS - MERGE TWO SORTED CLAIM LISTS
# ================================================================

print("\n\nTASK 5: TWO POINTERS")


def merge_sorted(a, b):
    i = 0
    j = 0
    merged = []

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1

    merged.extend(a[i:])          # copy whatever is left
    merged.extend(b[j:])

    return merged


north = [1002, 1015, 1020, 1033, 1050, 1077]
south = [1001, 1015, 1040, 1041, 1099]

merged = merge_sorted(north, south)

print("North Office:", north)
print("South Office:", south)
print("Merged List :", merged)
print("Sorted      :", merged == sorted(north + south))

print("\nTest Cases:")
print("  First empty     :", merge_sorted([], [3, 5]))
print("  Second empty    :", merge_sorted([2, 4], []))
print("  Both empty      :", merge_sorted([], []))
print("  Duplicates kept :", merge_sorted([5, 5, 7], [5, 7, 7]))
print("  No overlap      :", merge_sorted([1, 2], [8, 9]))


# ================================================================
# COMPLEXITY TABLE
# ================================================================

print("\n\n" + "=" * 65)
print("COMPLEXITY PER SOLUTION")
print("=" * 65)

print(f"{'Solution':<32}{'Time':<22}{'Space'}")
print(f"{'BST insert / search':<32}{'O(log n), worst O(n)':<22}O(h)")
print(f"{'BST traversals':<32}{'O(n)':<22}O(h)")
print(f"{'Hash duplicate detection':<32}{'O(n) average':<22}O(n)")
print(f"{'BFS shortest path':<32}{'O(V + E)':<22}O(V)")
print(f"{'DFS loop detection':<32}{'O(V + E)':<22}O(V)")
print(f"{'Sliding window longest run':<32}{'O(n)':<22}O(1)")
print(f"{'Two-pointer merge':<32}{'O(m + n)':<22}O(m + n)")

print("\n" + "=" * 65)
print("ALL 5 TASKS COMPLETED SUCCESSFULLY!")
print("=" * 65)
