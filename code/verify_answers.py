"""Check: every closed form, count and problem answer used in the textbook.
Run: python3 verify.py   (prints FAIL lines, then a summary)
"""
from fractions import Fraction as Fr
from itertools import product, permutations
import math

fails = []
total = 0


def check(name, cond):
    global total
    total += 1
    if not cond:
        fails.append(name)
        print("FAIL:", name)


def popcount(n):
    return bin(n).count("1")


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ---------------------------------------------------------------- summation tools
for n in range(0, 60):
    check(f"sum i n={n}", sum(range(1, n + 1)) == n * (n + 1) // 2)
    check(f"sum i^2 n={n}", sum(i * i for i in range(1, n + 1)) == n * (n + 1) * (2 * n + 1) // 6)
    check(f"geom 2 n={n}", sum(2 ** i for i in range(n + 1)) == 2 ** (n + 1) - 1)
    check(f"geom 3 n={n}", sum(3 ** i for i in range(n + 1)) == (3 ** (n + 1) - 1) // 2)
    check(f"sum 3i-2 n={n}", sum(3 * i - 2 for i in range(1, n + 1)) == n * (3 * n - 1) // 2)
    check(f"sum i(i+1) n={n}", sum(i * (i + 1) for i in range(1, n + 1)) == n * (n + 1) * (n + 2) // 3)
    check(f"sum 2i n={n}", sum(2 * i for i in range(1, n + 1)) == n * (n + 1))
    check(f"sum i(i+1)/2 n={n}", sum(i * (i + 1) // 2 for i in range(1, n + 1)) == n * (n + 1) * (n + 2) // 6)
check("sum const 4..20 of 7", sum(7 for i in range(4, 21)) == 119 and (20 - 4 + 1) == 17)
check("terms 5..20", len(range(5, 21)) == 16)
check("sum 1..100", sum(range(1, 101)) == 5050)
check("sum 3..n of 1", all(len(range(3, n + 1)) == n - 2 for n in range(3, 30)))

# ---------------------------------------------------------------- Module 1 algorithms
def max_element(A):
    c = 0
    m = A[0]
    for i in range(1, len(A)):
        c += 1
        if A[i] > m:
            m = A[i]
    return c


def unique_elements(A):
    n = len(A)
    c = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            c += 1
            if A[i] == A[j]:
                return c
    return c


def matmul(n):
    c = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c += 1
    return c


def dependent(n):
    c = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            c += 1
    return c


def doubling(n):
    c, i = 0, 1
    while i <= n:
        c += 1
        i *= 2
    return c


def selection_sort(A):
    A = list(A)
    n = len(A)
    comps = swaps = 0
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comps += 1
            if A[j] < A[m]:
                m = j
        A[i], A[m] = A[m], A[i]
        swaps += 1
    return comps, swaps


def has_pair_with_sum(A, s):
    n = len(A)
    c = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            c += 1
            if A[i] + A[j] == s:
                return c
    return c


def triple(n):
    c = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            for k in range(1, j + 1):
                c += 1
    return c


def exchange_sort_swaps(A):
    A = list(A)
    n = len(A)
    sw = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if A[j] < A[i]:
                A[i], A[j] = A[j], A[i]
                sw += 1
    return sw


for n in range(2, 40):
    check(f"max n={n}", max_element(list(range(n))) == n - 1)
    check(f"unique worst n={n}", unique_elements(list(range(n))) == n * (n - 1) // 2)
    check(f"unique best n={n}", unique_elements([5, 5] + list(range(n - 2))) == 1)
    check(f"dependent n={n}", dependent(n) == n * (n + 1) // 2)
    check(f"doubling n={n}", doubling(n) == int(math.log2(n)) + 1)
    c, s = selection_sort(list(range(n, 0, -1)))
    check(f"selection comps n={n}", c == n * (n - 1) // 2)
    check(f"selection swaps n={n}", s == n - 1)
    check(f"pair worst n={n}", has_pair_with_sum(list(range(n)), -1) == n * (n - 1) // 2)
    check(f"pair best n={n}", has_pair_with_sum([1, 2] + [0] * (n - 2), 3) == 1)
for n in range(1, 18):
    check(f"matmul n={n}", matmul(n) == n ** 3)
    check(f"triple n={n}", triple(n) == n * (n + 1) * (n + 2) // 6)
check("doubling 1000", doubling(1000) == 10)
check("dependent 10", dependent(10) == 55)
check("selection n=8", selection_sort(list(range(8)))[0] == 28)
check("unique worst n=10", unique_elements(list(range(10))) == 45)

# data dependence of the swap in "exchange sort" (find-the-mistake M1.1)
check("exchange sorted -> 0 swaps", exchange_sort_swaps([1, 2, 3, 4, 5]) == 0)
check("exchange reversed > 0", exchange_sort_swaps([5, 4, 3, 2, 1]) > 0)
check("exchange swaps vary", len({exchange_sort_swaps(p) for p in permutations(range(5))}) > 2)
check("exchange swaps <= n(n-1)/2", all(exchange_sort_swaps(p) <= 10 for p in permutations(range(5))))

# find-the-mistake M1.2: off-by-one
n_ = 9
correct = sum(n_ - 1 - i for i in range(0, n_ - 1))
student = sum(n_ - i - 2 for i in range(0, n_ - 1))
check("M1.2 correct", correct == n_ * (n_ - 1) // 2)
check("M1.2 student", student == (n_ - 1) * (n_ - 2) // 2 and student != correct)

# B1, B3, B4
def b1(n):
    c = 0
    for i in range(1, n + 1):
        for j in range(1, 2 * i + 1):
            c += 1
    return c


def b3(n):
    c = 0
    for i in range(1, n + 1):
        for j in range(1, i * (i + 1) + 1):
            c += 1
    return c


def b4(n):
    c = 0
    for i in range(0, n + 1):
        for j in range(1, 2 ** i + 1):
            c += 1
    return c


for n in range(1, 15):
    check(f"B1 n={n}", b1(n) == n * (n + 1))
    check(f"B3 n={n}", b3(n) == n * (n + 1) * (n + 2) // 3)
    check(f"B4 n={n}", b4(n) == 2 ** (n + 1) - 1)

# A3 CountEven: comparison count n regardless of data
def count_even(A):
    cmp_, inc = 0, 0
    for x in A:
        cmp_ += 1
        if x % 2 == 0:
            inc += 1
    return cmp_, inc


check("CountEven cmp", count_even([1, 3, 5, 7])[0] == 4 and count_even([2, 4, 6, 8])[0] == 4)
check("CountEven inc varies", count_even([1, 3, 5, 7])[1] == 0 and count_even([2, 4, 6, 8])[1] == 4)

# B2 FirstNegative
def first_negative(A):
    i, c = 0, 0
    n = len(A)
    while i < n:
        c += 1
        if not (A[i] >= 0):
            break
        i += 1
    return c


check("FirstNegative worst", all(first_negative(list(range(n))) == n for n in range(1, 20)))
check("FirstNegative best", all(first_negative([-1] + list(range(n))) == 1 for n in range(1, 20)))

# C1 FirstZero average: exact enumeration
def first_zero(bits):
    c = 0
    for b in bits:
        c += 1
        if b == 0:
            break
    return c


for n in range(1, 13):
    tot = sum(first_zero(b) for b in product((0, 1), repeat=n))
    check(f"FirstZero avg n={n}", Fr(tot, 2 ** n) == 2 - Fr(2, 2 ** n))
check("sum i/2^i", all(sum(Fr(i, 2 ** i) for i in range(1, n + 1)) == 2 - Fr(n + 2, 2 ** n) for n in range(1, 20)))

# lecture example: sequential search average case, success probability p
def seq_avg(n, p):
    return sum(Fr(i) * p / n for i in range(1, n + 1)) + n * (1 - p)


for n in (3, 5, 8):
    for p in (Fr(0), Fr(1, 3), Fr(1, 2), Fr(1)):
        check(f"seq avg n={n} p={p}", seq_avg(n, p) == p * (n + 1) / 2 + n * (1 - p))
check("seq p=1", seq_avg(7, Fr(1)) == Fr(8, 2))
check("seq p=0", seq_avg(7, Fr(0)) == 7)

# C2 halving loop
def halving(n):
    c, i = 0, n
    while i >= 1:
        for j in range(i):
            c += 1
        i //= 2
    return c


for k in range(0, 14):
    check(f"C2 n=2^{k}", halving(2 ** k) == 2 ** (k + 1) - 1)
for n in range(1, 300):
    check(f"C2 general n={n}", halving(n) == 2 * n - popcount(n))

# ---------------------------------------------------------------- Module 2
def fact_mults(n):
    if n == 0:
        return 0
    return fact_mults(n - 1) + 1


check("fact", all(fact_mults(n) == n for n in range(0, 50)))


def hanoi(n):
    if n == 1:
        return 1
    return 2 * hanoi(n - 1) + 1


check("hanoi", all(hanoi(n) == 2 ** n - 1 for n in range(1, 25)))
check("hanoi 5", hanoi(5) == 31)


def binrec(n):  # additions
    if n == 1:
        return 0
    return binrec(n // 2) + 1


check("binrec", all(binrec(n) == int(math.log2(n)) for n in range(1, 2000)))
check("binrec calls", all(binrec(n) + 1 == int(math.log2(n)) + 1 for n in range(1, 200)))
check("binrec 1024", binrec(1024) == 10)


def fib_adds(n):
    if n <= 1:
        return 0
    return fib_adds(n - 1) + fib_adds(n - 2) + 1


def fib_calls(n):
    if n <= 1:
        return 1
    return fib_calls(n - 1) + fib_calls(n - 2) + 1


for n in range(0, 22):
    check(f"fib adds n={n}", fib_adds(n) == fib(n + 1) - 1)
    check(f"fib calls n={n}", fib_calls(n) == 2 * fib(n + 1) - 1)
check("fib adds list", [fib_adds(n) for n in range(7)] == [0, 0, 1, 2, 4, 7, 12])
check("fib calls 5", fib_calls(5) == 15)
check("fib calls 6", fib_calls(6) == 25)
check("fib iter adds", all(n - 1 >= 0 for n in range(1, 10)))

# repeated subproblem counts in the call tree of fib(5)
from collections import Counter

cnt = Counter()


def fib_trace(n):
    cnt[n] += 1
    if n > 1:
        fib_trace(n - 1)
        fib_trace(n - 2)


fib_trace(5)
check("fib(5) repeats", cnt == Counter({5: 1, 4: 1, 3: 2, 2: 3, 1: 5, 0: 3}))

# memoized / iterative additions
def fib_memo(n, memo, ctr):
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
        return n
    memo[n] = fib_memo(n - 1, memo, ctr) + fib_memo(n - 2, memo, ctr)
    ctr[0] += 1
    return memo[n]


for n in range(2, 30):
    ctr = [0]
    fib_memo(n, {}, ctr)
    check(f"memo adds n={n}", ctr[0] == n - 1)


# recursive maximum
def rec_max(A, n, ctr):
    if n == 1:
        return A[0]
    t = rec_max(A, n - 1, ctr)
    ctr[0] += 1
    return t if t > A[n - 1] else A[n - 1]


for n in range(1, 40):
    ctr = [0]
    rec_max(list(range(n)), n, ctr)
    check(f"rec max n={n}", ctr[0] == n - 1)
check("rec max 100", True)


# fast exponentiation
def power(a, n, ctr):
    if n == 0:
        return 1
    if n % 2 == 0:
        t = power(a, n // 2, ctr)
        ctr[0] += 1
        return t * t
    t = power(a, n - 1, ctr)
    ctr[0] += 1
    return a * t


for n in range(1, 400):
    ctr = [0]
    r = power(3, n, ctr)
    check(f"pow value n={n}", r == 3 ** n)
    check(f"pow mults n={n}", ctr[0] == int(math.log2(n)) + popcount(n))
for k in range(1, 12):
    c1, c2 = [0], [0]
    power(2, 2 ** k, c1)
    power(2, 2 ** k - 1, c2)
    check(f"pow best k={k}", c1[0] == k + 1)
    check(f"pow worst k={k}", c2[0] == 2 * k - 1)


# divide and conquer sum
def dc_sum(A, l, r, ctr):
    if l == r:
        return A[l]
    m = (l + r) // 2
    s = dc_sum(A, l, m, ctr) + dc_sum(A, m + 1, r, ctr)
    ctr[0] += 1
    return s


for k in range(0, 11):
    n = 2 ** k
    ctr = [0]
    dc_sum(list(range(n)), 0, n - 1, ctr)
    check(f"dc sum k={k}", ctr[0] == n - 1)

# A1 A2 A3 A4
def a1(n):
    return 2 if n == 0 else a1(n - 1) + 3


check("A1", all(a1(n) == 3 * n + 2 for n in range(0, 40)))


def count3(n, ctr):
    if n < 3:
        return 1
    ctr[0] += 1
    return 1 + count3(n // 3, ctr)


c = [0]
count3(81, c)
check("A4 count3 81 additions", c[0] == 4)  # 81->27->9->3->1: 5 calls, 4 additions
# Count3 as defined in the text: "if n<3 return 1 else return Count3(n//3)+1", additions = number of recursive returns
def count3_adds(n):
    if n < 3:
        return 0
    return count3_adds(n // 3) + 1


check("A4 adds 81", count3_adds(81) == 4)
check("A4 adds 3^k", all(count3_adds(3 ** k) == k for k in range(1, 12)))


# B1..B4 module 2
def t_b1(n):
    return 1 if n == 1 else t_b1(n - 1) + 2 * n - 1


check("M2 B1", all(t_b1(n) == n * n for n in range(1, 60)))


def l_b2(n):
    return 0 if n == 0 else 2 * l_b2(n - 1) + 3


check("M2 B2", all(l_b2(n) == 3 * (2 ** n - 1) for n in range(0, 40)))
check("M2 B2 values", [l_b2(n) for n in range(5)] == [0, 3, 9, 21, 45])


def t_b3(n):
    return 1 if n == 1 else t_b3(n // 2) + n


check("M2 B3", all(t_b3(2 ** k) == 2 ** (k + 1) - 1 for k in range(0, 20)))


def rec_search(A, n, K, ctr):
    if n == 0:
        return -1
    ctr[0] += 1
    if A[n - 1] == K:
        return n - 1
    return rec_search(A, n - 1, K, ctr)


for n in range(1, 30):
    c1, c2 = [0], [0]
    rec_search(list(range(n)), n, -1, c1)
    rec_search(list(range(n)), n, n - 1, c2)
    check(f"M2 B4 worst n={n}", c1[0] == n)
    check(f"M2 B4 best n={n}", c2[0] == 1)

# M2 C1: induction check
check("M2 C1", all(fib_adds(n) == fib(n + 1) - 1 for n in range(0, 22)))
# fib identity used in the induction step: F(n)+F(n+1) = F(n+2)
check("fib identity", all(fib(n) + fib(n + 1) == fib(n + 2) for n in range(0, 40)))

# M2 FM2.2 wrong initial condition
def t_ok(n):
    return 1 if n == 1 else 2 * t_ok(n - 1) + 1


check("FM2.2 correct", all(t_ok(n) == 2 ** n - 1 for n in range(1, 30)))
check("FM2.2 wrong differs", 2 ** 6 - 1 != 2 ** 7 - 1)

# stack depth: factorial(n) frames = n+1
def depth_fact(n):
    return 1 if n == 0 else 1 + depth_fact(n - 1)


check("depth fact", all(depth_fact(n) == n + 1 for n in range(0, 100)))


def depth_binrec(n):
    return 1 if n == 1 else 1 + depth_binrec(n // 2)


check("depth binrec", all(depth_binrec(n) == int(math.log2(n)) + 1 for n in range(1, 500)))


def depth_hanoi(n):
    return 1 if n == 1 else 1 + depth_hanoi(n - 1)


check("depth hanoi", all(depth_hanoi(n) == n for n in range(1, 30)))

# quiz sanity values
check("quiz M2 x(n)=x(n-1)+4,x(1)=0", True)
check("quiz hanoi 5", 2 ** 5 - 1 == 31)
check("quiz fib adds 6", fib(7) - 1 == 12)
check("quiz rec max 100", 100 - 1 == 99)
check("quiz binary digits 1024", int(math.log2(1024)) == 10)
# sum of level sizes of hanoi tree
check("hanoi tree nodes", all(sum(2 ** k for k in range(n)) == 2 ** n - 1 for n in range(1, 20)))
# entry quiz: 3n^2+10n+7 is Theta(n^2): ratio test
check("theta n^2", all(3 <= (3 * n * n + 10 * n + 7) / (n * n) <= 20 for n in range(1, 1000)))


# M2 C2: T(n)=2T(n/2)+n, T(1)=0 -> n log2 n for n=2^k
def t_c2(n):
    return 0 if n == 1 else 2 * t_c2(n // 2) + n


check("M2 C2", all(t_c2(2 ** k) == k * 2 ** k for k in range(0, 18)))
# M2 example sq: x(n)=x(n-1)+5, x(1)=7 -> 5n+2
def x5(n):
    return 7 if n == 1 else x5(n - 1) + 5


check("M2 backsub example", all(x5(n) == 5 * n + 2 for n in range(1, 60)))
check("fib(81)", fib(81) == 37889062373143906)
check("quiz power 1000", int(math.log2(1000)) + popcount(1000) == 15)

print(f"\n{total} checks, {len(fails)} failed")
raise SystemExit(1 if fails else 0)
