
import csv
import random
import time
from bisect import bisect_right


# Task 1 – Linear and Binary Search on Patient Records
# Objective: Implement linear and binary search over 20,000 patient records keyed by patient ID; measure the time for 1,000 look-ups and explain the result.

def linear_search(records, target):
    for r in records:
        if r["patientId"] == target:
            return r
    return None


def binary_search(records, target):
    low, high = 0, len(records) - 1

    while low <= high:
        mid = (low + high) // 2
        key = records[mid]["patientId"]

        if key == target:
            return records[mid]
        if key < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


with open("patients.csv", newline="") as f:
    patients = list(csv.DictReader(f))

patients.sort(key=lambda r: r["patientId"])

if not patients:
    raise ValueError("patients.csv contains no patient records")

random.seed(3)
lookups = [random.choice(patients)["patientId"] for _ in range(1000)]

start = time.perf_counter()
found_lin = [linear_search(patients, p) for p in lookups]
t_lin = time.perf_counter() - start

start = time.perf_counter()
found_bin = [binary_search(patients, p) for p in lookups]
t_bin = time.perf_counter() - start

print("Patient records :", len(patients))
print("Look-ups        :", len(lookups))
print(f"Linear search   : {t_lin:.4f} s ({t_lin / 1000:.6f} s per look-up)")
print(f"Binary search   : {t_bin:.4f} s ({t_bin / 1000:.6f} s per look-up)")
print(f"Speed-up        : about {t_lin / t_bin:,.0f} times")
print("Both found the same records:", found_lin == found_bin)


# Task 2 – Selection Sort and Quick Sort
# Objective: Sort the day's appointments by urgency level and then by arrival time using selection sort and quick sort; compare the number of swaps and the running time.

def key(a):
    return (a["urgency"], a["arrival"])


def selection_sort(rows, trace=False):
    a, swaps = rows[:], 0

    for i in range(len(a) - 1):
        m = i

        for j in range(i + 1, len(a)):
            if key(a[j]) < key(a[m]):
                m = j

        if m != i:
            a[i], a[m] = a[m], a[i]
            swaps += 1

        if trace and i < 3:
            print(
                f"Pass {i + 1}:",
                [f"{x['appointmentId']}({x['urgency']},{x['arrival']})" for x in a]
            )

    return a, swaps


def quick_sort(rows):
    a, swaps = rows[:], [0]

    def sort(low, high):
        while low < high:
            p = random.randint(low, high)
            a[p], a[high] = a[high], a[p]
            swaps[0] += 1

            pivot = key(a[high])
            i = low - 1

            for j in range(low, high):
                if key(a[j]) <= pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
                    swaps[0] += 1

            a[i + 1], a[high] = a[high], a[i + 1]
            swaps[0] += 1

            if i - low < high - i:
                sort(low, i)
                low = i + 2
            else:
                sort(i + 2, high)
                high = i

    sort(0, len(a) - 1)
    return a, swaps[0]


with open("appointments.csv", newline="") as f:
    rows = list(csv.DictReader(f))

for r in rows:
    r["urgency"] = int(r["urgency"])

sample = [
    {"appointmentId": "A1", "urgency": 3, "arrival": "09:10"},
    {"appointmentId": "A2", "urgency": 2, "arrival": "09:40"},
    {"appointmentId": "A3", "urgency": 1, "arrival": "08:50"},
    {"appointmentId": "A4", "urgency": 4, "arrival": "08:15"},
    {"appointmentId": "A5", "urgency": 1, "arrival": "08:30"},
    {"appointmentId": "A6", "urgency": 2, "arrival": "09:05"}
]

print("\nTrace - selection sort, first three passes")
print("Start:", [f"{x['appointmentId']}({x['urgency']},{x['arrival']})" for x in sample])
selection_sort(sample, trace=True)

random.seed(5)

t = time.perf_counter()
s_res, s_swaps = selection_sort(rows)
t_sel = time.perf_counter() - t

t = time.perf_counter()
q_res, q_swaps = quick_sort(rows)
t_qs = time.perf_counter() - t

t = time.perf_counter()
b_res = sorted(rows, key=key)
t_bi = time.perf_counter() - t

print(f"\n{len(rows)} appointments")
print(f"{'Algorithm':<16}{'Swaps':>10}{'Time (s)':>12}")
print(f"{'Selection sort':<16}{s_swaps:>10,}{t_sel:>12.4f}")
print(f"{'Quick sort':<16}{q_swaps:>10,}{t_qs:>12.4f}")
print(f"{'Built-in sorted':<16}{'-':>10}{t_bi:>12.4f}")

print(
    "Order matches built-in sort:",
    [key(x) for x in s_res] == [key(x) for x in b_res] == [key(x) for x in q_res]
)

print("\nFirst five appointments:")
for r in s_res[:5]:
    print(
        f"{r['appointmentId']} {r.get('patientId', '')} "
        f"urgency {r['urgency']} arrived {r['arrival']}"
    )


# Task 3 – Double-Booked Slots
# Objective: Detect double-booked slots (same patient and slot) with the most suitable data structure and explain why a list scan is not acceptable at this volume.

with open("bookings.csv", newline="") as f:
    bookings = list(csv.DictReader(f))


def with_hash_set(rows):
    seen, doubles = set(), []

    for b in rows:
        k = (b["patientId"], b["slot"])

        if k in seen:
            doubles.append(b)
        else:
            seen.add(k)

    return doubles


def with_list_scan(rows):
    seen, doubles = [], []

    for b in rows:
        k = (b["patientId"], b["slot"])

        if k in seen:
            doubles.append(b)
        else:
            seen.append(k)

    return doubles


t = time.perf_counter()
d1 = with_hash_set(bookings)
t_set = time.perf_counter() - t

t = time.perf_counter()
d2 = with_list_scan(bookings)
t_list = time.perf_counter() - t

print("\nBooking requests:", len(bookings))
print("Double bookings:", len(d1))

for b in d1:
    print(f"{b['bookingId']} {b['patientId']} {b['slot']}")

print(f"\nHash set : {t_set * 1000:.2f} ms")
print(f"List scan : {t_list * 1000:.2f} ms")

if t_set > 0:
    print(f"List scan is about {t_list / t_set:,.0f} times slower")

print("Same result from both:", d1 == d2)


# Task 4 – Walk-in Token Queue and Recent Patients Stack
# Objective: Model the walk-in token line with a Queue and the recent patients viewed history with a Stack, each implemented from scratch.

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class TokenQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
        self.next_token = 1

    def issue_token(self, patient):
        node = Node((self.next_token, patient))
        self.next_token += 1

        if self.tail:
            self.tail.next = node
        else:
            self.head = node

        self.tail = node
        self.count += 1

        return node.value[0]

    def call_next(self):
        if not self.head:
            return None

        token, patient = self.head.value
        self.head = self.head.next

        if not self.head:
            self.tail = None

        self.count -= 1
        return token, patient


class RecentStack:
    def __init__(self):
        self.top = None

    def push(self, patient):
        node = Node(patient)
        node.next = self.top
        self.top = node

    def pop(self):
        if not self.top:
            return None

        node = self.top
        self.top = node.next
        return node.value

    def peek(self):
        return self.top.value if self.top else None

    def as_list(self):
        out = []
        n = self.top

        while n:
            out.append(n.value)
            n = n.next

        return out


print("\nWalk-in token line (FIFO)")

q = TokenQueue()

for p in ("P000412", "P009871", "P015230", "P000077"):
    print(f"Token {q.issue_token(p)} issued to {p}")

for _ in range(2):
    token, p = q.call_next()
    print(f"Now serving token {token} ({p})")

print("Waiting:", q.count)

print("\nRecently viewed patients (LIFO)")

s = RecentStack()

for p in ("P000412", "P009871", "P000077", "P015230"):
    s.push(p)
    print(f"Opened {p} | History: {s.as_list()}")

print("Back button ->", s.pop(), "| Now showing", s.peek())


# Task 5 – Maximum Appointments: Dynamic Programming and Greedy
# Objective: Use dynamic programming to find the maximum number of appointments a doctor can attend in a shift given a set of overlapping time slots with different durations (greedy comparison expected).

def to_min(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def fmt(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def dp_schedule(slots):
    s = sorted(slots, key=lambda x: x[1])
    ends = [x[1] for x in s]
    n = len(s)

    prev = [
        bisect_right(ends, s[i][0], 0, i)
        for i in range(n)
    ]

    best = [0] * (n + 1)

    for i in range(1, n + 1):
        best[i] = max(
            best[i - 1],
            s[i - 1][2] + best[prev[i - 1]]
        )

    chosen = []
    i = n

    while i > 0:
        if s[i - 1][2] + best[prev[i - 1]] >= best[i - 1]:
            chosen.append(s[i - 1])
            i = prev[i - 1]
        else:
            i -= 1

    return best[n], chosen[::-1]


def greedy(slots, order):
    picked = []
    last_end = -1

    for st, en, w in sorted(slots, key=order):
        if st >= last_end:
            picked.append((st, en, w))
            last_end = en

    return picked


raw = [
    ("09:00", "12:00"),
    ("09:00", "10:00"),
    ("10:00", "11:30"),
    ("09:30", "10:30"),
    ("10:30", "11:00"),
    ("11:00", "12:00"),
    ("11:30", "13:00"),
    ("12:00", "13:00"),
    ("12:00", "12:30"),
    ("09:45", "11:15")
]

slots = [(to_min(a), to_min(b), 1) for a, b in raw]

print(f"\n{len(slots)} overlapping requests, 09:00 to 13:00")

count, chosen = dp_schedule(slots)

print("Dynamic programming - maximum appointments:", count)

for st, en, _ in chosen:
    print(f"{fmt(st)} - {fmt(en)}")

greedy_methods = [
    ("Greedy: earliest finish first", lambda x: (x[1], x[0])),
    ("Greedy: shortest duration first", lambda x: (x[1] - x[0], x[0])),
    ("Greedy: earliest start first", lambda x: (x[0], x[1]))
]

for name, order in greedy_methods:
    picked = greedy(slots, order)
    print(f"\n{name} -> {len(picked)} appointments")
    print(" ".join(f"{fmt(a)}-{fmt(b)}" for a, b, _ in picked))


weighted = [
    (to_min("09:00"), to_min("11:00"), 5),
    (to_min("09:30"), to_min("10:00"), 1),
    (to_min("10:00"), to_min("10:30"), 1),
    (to_min("10:30"), to_min("11:00"), 1)
]

total, picked = dp_schedule(weighted)

print("\nWeighted case")
print("DP best total weight:", total)

g = greedy(weighted, lambda x: (x[1], x[0]))
print("Earliest-finish greedy total weight:", sum(w for _, _, w in g))
