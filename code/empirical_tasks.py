"""Counting Steps - code for the empirical tasks (Module 1 and Module 2).

Each function counts how often the basic operation runs and compares the
measured number with the formula derived in the textbook.

How to run
----------
    python empirical_tasks.py        # both modules, ends with "ALL CHECKS PASSED"
    python empirical_tasks.py 1      # Module 1 only
    python empirical_tasks.py 2      # Module 2 only
    python empirical_tasks.py 1 --plot   # also saves module1_plot.png
    python empirical_tasks.py 2 --plot   # also saves module2_plot.png

Needs Python 3.8 or newer. The checks need no extra packages. The optional
plots need matplotlib (pip install matplotlib). The same counting code is
also given in the e-textbook (Quick checks and Task E1 / E2).
"""
import math
import random
import sys
import time

FAILED = []


def check(label, ok):
    """Print one line per comparison and remember failures."""
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        FAILED.append(label)


def popcount(n):
    return bin(n).count("1")


# =====================================================================
# MODULE 1
# =====================================================================

#<<m1_unique_fn
def unique_elements(A):
    """Returns (answer, number of comparisons A[i] == A[j])."""
    n = len(A)
    count = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            count += 1                # the basic operation
            if A[i] == A[j]:
                return False, count
    return True, count
#>>m1_unique_fn


def demo_unique():
    print("\nUniqueElements: n, measured worst, formula n(n-1)/2, equal?, measured best")
    #<<m1_unique_demo
    for n in (2, 5, 10, 50, 100):
        worst = unique_elements(list(range(n)))[1]            # all different
        best = unique_elements([7, 7] + list(range(n - 2)))[1]  # first two equal
        formula = n * (n - 1) // 2
        print(n, worst, formula, worst == formula, best)
    #>>m1_unique_demo
    for n in range(2, 60):
        check("UniqueElements worst n=%d" % n,
              unique_elements(list(range(n)))[1] == n * (n - 1) // 2)
        check("UniqueElements best n=%d" % n,
              unique_elements([7, 7] + list(range(n - 2)))[1] == 1)


#<<m1_avg
def seq_search_count(A, K):
    """Sequential search. Returns the number of comparisons A[i] == K."""
    count = 0
    for x in A:
        count += 1                    # the basic operation
        if x == K:
            break
    return count


def average_cases(n=20, p=0.6, trials=100_000):
    A = list(range(n))
    total = 0
    for _ in range(trials):
        # with probability p the key is present, at a uniformly random position
        K = random.randrange(n) if random.random() < p else -1
        total += seq_search_count(A, K)
    return total / trials, p * (n + 1) / 2 + n * (1 - p)
#>>m1_avg


def demo_average():
    print("\nSequential search, average case: simulated mean vs formula p(n+1)/2 + n(1-p)")
    random.seed(1)
    for n, p in ((20, 0.6), (50, 1.0), (50, 0.0), (10, 0.25)):
        sim, formula = average_cases(n, p, 60_000)
        print("n=%d p=%.2f  simulated %.3f  formula %.3f" % (n, p, sim, formula))
        check("average n=%d p=%.2f within 2%%" % (n, p), abs(sim - formula) <= 0.02 * formula)


#<<m1_solution
def selection_sort_counts(A):
    """Returns (comparisons A[j] < A[min], swaps)."""
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


def pair_sum_worst(n):
    """HasPairWithSum on an input where no pair has the target sum."""
    A = list(range(n))                # all sums are >= 1, the target -1 never occurs
    count = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            count += 1
            if A[i] + A[j] == -1:
                return count
    return count


def triple_loop(n):
    count = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            for k in range(1, j + 1):
                count += 1
    return count


def first_zero(bits):
    """FirstZero: number of comparisons B[i] != 0."""
    count = 0
    for b in bits:
        count += 1
        if b == 0:
            break
    return count


def run_e1():
    print("n   selection  swaps  pair-sum  triple   (formulas: n(n-1)/2, n-1, n(n-1)/2, n(n+1)(n+2)/6)")
    for n in range(1, 13):
        sel, sw = selection_sort_counts(range(n, 0, -1))
        ps, tr = pair_sum_worst(n), triple_loop(n)
        ok = (sel == n * (n - 1) // 2 and sw == max(n - 1, 0)
              and ps == n * (n - 1) // 2 and tr == n * (n + 1) * (n + 2) // 6)
        print("%-3d %-10d %-6d %-9d %-8d %s" % (n, sel, sw, ps, tr, "ok" if ok else "MISMATCH"))

    # doubling test: ratio count(2n) / count(n) should approach 4, 4 and 8
    n = 100
    print("\nratio selection:", selection_sort_counts(range(2 * n))[0] / selection_sort_counts(range(n))[0])
    print("ratio pair-sum :", pair_sum_worst(2 * n) / pair_sum_worst(n))
    print("ratio triple   :", triple_loop(2 * n) / triple_loop(n))

    # average case of FirstZero, each bit is 0 with probability 1/2
    random.seed(7)
    n, trials = 10, 20_000
    total = sum(first_zero([random.getrandbits(1) for _ in range(n)]) for _ in range(trials))
    print("\nFirstZero n=10: simulated %.3f, formula 2 - 2^(1-n) = %.3f" % (total / trials, 2 - 2 ** (1 - n)))
#>>m1_solution


def module1():
    print("=" * 70 + "\nMODULE 1\n" + "=" * 70)
    demo_unique()
    demo_average()
    print("\nTask E1")
    run_e1()
    for n in range(1, 40):
        sel, sw = selection_sort_counts(range(n, 0, -1))
        check("E1 selection n=%d" % n, sel == n * (n - 1) // 2 and sw == max(n - 1, 0))
        check("E1 pair-sum n=%d" % n, pair_sum_worst(n) == n * (n - 1) // 2)
    for n in range(1, 25):
        check("E1 triple n=%d" % n, triple_loop(n) == n * (n + 1) * (n + 2) // 6)
    random.seed(7)
    n, trials = 10, 20_000
    sim = sum(first_zero([random.getrandbits(1) for _ in range(n)]) for _ in range(trials)) / trials
    check("E1 FirstZero average within 3%", abs(sim - (2 - 2 ** (1 - n))) <= 0.03 * 2)
    for n in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        total = 0
        for mask in range(2 ** n):
            total += first_zero([(mask >> t) & 1 for t in range(n)])
        check("FirstZero exact average n=%d" % n, total / 2 ** n == 2 - 2 ** (1 - n))


# =====================================================================
# MODULE 2
# =====================================================================

#<<m2_counters
def fib_naive(n, c):
    """Naive Fibonacci. c is a dict used as the counter."""
    c["calls"] += 1
    if n <= 1:
        return n
    c["adds"] += 1                    # the basic operation: one addition
    return fib_naive(n - 1, c) + fib_naive(n - 2, c)


def fib_iter(n):
    """Iterative Fibonacci. Returns (F(n), number of additions)."""
    if n <= 1:
        return n, 0
    a, b, adds = 0, 1, 0
    for _ in range(2, n + 1):
        a, b = b, a + b
        adds += 1
    return b, adds
#>>m2_counters


def demo_fib():
    print("\nNaive Fibonacci: n, additions, F(n+1)-1, calls, 2F(n+1)-1")
    for n in (5, 10, 15, 20, 25):
        c = {"calls": 0, "adds": 0}
        fib_naive(n, c)
        f_next = fib_iter(n + 1)[0]
        print(n, c["adds"], f_next - 1, c["calls"], 2 * f_next - 1)
    for n in range(0, 23):
        c = {"calls": 0, "adds": 0}
        value = fib_naive(n, c)
        f_next = fib_iter(n + 1)[0]
        check("fib n=%d additions = F(n+1)-1" % n, c["adds"] == f_next - 1)
        check("fib n=%d calls = 2F(n+1)-1" % n, c["calls"] == 2 * f_next - 1)
        check("fib n=%d value" % n, value == fib_iter(n)[0])
        check("fib iterative additions n=%d" % n, fib_iter(n)[1] == max(n - 1, 0))


#<<m2_solution
def hanoi(n, source, target, spare, c):
    """Tower of Hanoi. c['moves'] counts moved disks."""
    if n == 1:
        c["moves"] += 1
        return
    hanoi(n - 1, source, spare, target, c)
    c["moves"] += 1                   # move disk n
    hanoi(n - 1, spare, target, source, c)


def power(a, n, c):
    """Fast exponentiation. c['mults'] counts multiplications."""
    if n == 0:
        return 1
    if n % 2 == 0:
        t = power(a, n // 2, c)
        c["mults"] += 1
        return t * t
    t = power(a, n - 1, c)
    c["mults"] += 1
    return a * t


def fact(n, depth, c):
    """Recursive factorial. c['depth'] records the deepest stack level."""
    c["depth"] = max(c["depth"], depth)
    if n == 0:
        return 1
    return fact(n - 1, depth + 1, c) * n


def run_e2():
    # (a) naive Fibonacci
    for n in range(0, 26):
        c = {"calls": 0, "adds": 0}
        fib_naive(n, c)
        F = fib_iter(n + 1)[0]
        assert c["adds"] == F - 1 and c["calls"] == 2 * F - 1
    print("(a) naive Fibonacci: additions = F(n+1)-1 and calls = 2F(n+1)-1 for n = 0..25")

    # (b) Tower of Hanoi
    for n in range(1, 21):
        c = {"moves": 0}
        hanoi(n, "A", "C", "B", c)
        assert c["moves"] == 2 ** n - 1
    print("(b) Hanoi: moves = 2^n - 1 for n = 1..20")

    # (c) fast exponentiation
    for n in range(1, 1001):
        c = {"mults": 0}
        assert power(3, n, c) == 3 ** n
        assert c["mults"] == int(math.log2(n)) + popcount(n)
    print("(c) Power: multiplications = floor(log2 n) + (number of 1-bits of n) for n = 1..1000")

    # (d) stack depth of factorial
    for n in (0, 1, 5, 10, 100, 500):
        c = {"depth": 0}
        fact(n, 1, c)
        assert c["depth"] == n + 1
    print("(d) factorial: deepest stack level = n + 1")
    try:
        fact(5000, 1, {"depth": 0})
    except RecursionError:
        print("    fact(5000) raises RecursionError (default limit is %d)" % sys.getrecursionlimit())

    # (e) timing
    n = 27
    t0 = time.perf_counter()
    fib_naive(n, {"calls": 0, "adds": 0})
    t1 = time.perf_counter()
    fib_iter(n)
    t2 = time.perf_counter()
    print("(e) fib(%d): naive %.3f s, iterative %.6f s" % (n, t1 - t0, t2 - t1))
#>>m2_solution


def module2():
    print("\n" + "=" * 70 + "\nMODULE 2\n" + "=" * 70)
    demo_fib()
    print("\nTask E2")
    run_e2()
    for n in range(1, 21):
        c = {"moves": 0}
        hanoi(n, "A", "C", "B", c)
        check("hanoi n=%d" % n, c["moves"] == 2 ** n - 1)
    for k in range(1, 11):
        c1, c2 = {"mults": 0}, {"mults": 0}
        power(2, 2 ** k, c1)
        power(2, 2 ** k - 1, c2)
        check("power best 2^%d: k+1" % k, c1["mults"] == k + 1)
        check("power worst 2^%d-1: 2k-1" % k, c2["mults"] == 2 * k - 1)
    for n in range(1, 200):
        c = {"depth": 0}
        fact(n, 1, c)
        check("fact depth n=%d" % n, c["depth"] == n + 1)


# =====================================================================
# PLOTS (optional, need matplotlib): measured counts against the formula
# =====================================================================

def _plt():
    try:
        import matplotlib
        matplotlib.use("Agg")             # draw to a file, no window needed
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("matplotlib is not installed: run  pip install matplotlib  and try again")
        return None


def plot_module1(path="module1_plot.png"):
    plt = _plt()
    if plt is None:
        return
    ns = list(range(1, 41))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # left: three loops, measured dots on top of the exact formula lines
    data = (
        ("selection sort comparisons", [selection_sort_counts(range(n, 0, -1))[0] for n in ns],
         lambda n: n * (n - 1) / 2),
        ("triple loop", [triple_loop(n) for n in ns],
         lambda n: n * (n + 1) * (n + 2) / 6),
        ("selection sort swaps", [selection_sort_counts(range(n, 0, -1))[1] for n in ns],
         lambda n: max(n - 1, 0)),
    )
    for label, measured, formula in data:
        a1.plot(ns, [formula(n) for n in ns], "-", linewidth=1.5, label="formula: " + label)
        a1.plot(ns, measured, "o", markersize=3.5, color="black")
    a1.plot([], [], "o", color="black", markersize=3.5, label="measured")
    a1.set_xlabel("n")
    a1.set_ylabel("basic operations")
    a1.set_title("Module 1: measured = formula")
    a1.legend(fontsize=8)
    a1.grid(alpha=0.3)

    # right: average case of sequential search, simulation against p(n+1)/2 + n(1-p)
    random.seed(1)
    n = 30
    ps = [i / 10 for i in range(11)]
    sims = [average_cases(n, p, 20_000)[0] for p in ps]
    a2.plot(ps, [p * (n + 1) / 2 + n * (1 - p) for p in ps], "-", linewidth=1.5,
            label="formula p(n+1)/2 + n(1-p)")
    a2.plot(ps, sims, "o", color="black", markersize=4, label="simulated mean")
    a2.set_xlabel("probability p that the key is present")
    a2.set_ylabel("average comparisons (n = %d)" % n)
    a2.set_title("Sequential search, average case")
    a2.legend(fontsize=8)
    a2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print("saved", path)


def plot_module2(path="module2_plot.png"):
    plt = _plt()
    if plt is None:
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # left: operation counts on a logarithmic axis
    ns = list(range(1, 26))
    calls, moves = [], []
    for n in ns:
        c = {"calls": 0, "adds": 0}
        fib_naive(n, c)
        calls.append(c["calls"])
        h = {"moves": 0}
        hanoi(n, "A", "C", "B", h)
        moves.append(h["moves"])
    a1.plot(ns, [2 * fib_iter(n + 1)[0] - 1 for n in ns], "-", linewidth=1.5,
            label="formula 2F(n+1) - 1 (Fibonacci calls)")
    a1.plot(ns, calls, "o", color="black", markersize=3.5)
    a1.plot(ns, [2 ** n - 1 for n in ns], "-", linewidth=1.5, label="formula 2^n - 1 (Hanoi moves)")
    a1.plot(ns, moves, "s", color="gray", markersize=3.5)
    a1.plot(ns, [n - 1 for n in ns], "-", linewidth=1.5, label="iterative Fibonacci: n - 1 additions")
    a1.plot([], [], "o", color="black", markersize=3.5, label="measured Fibonacci calls")
    a1.plot([], [], "s", color="gray", markersize=3.5, label="measured Hanoi moves")
    a1.set_yscale("log")
    a1.set_xlabel("n")
    a1.set_ylabel("operations (log scale)")
    a1.set_title("Module 2: exponential against linear")
    a1.legend(fontsize=8)
    a1.grid(alpha=0.3, which="both")

    # right: running time, naive against iterative Fibonacci
    ns2 = list(range(10, 31, 2))
    t_naive, t_iter = [], []
    for n in ns2:
        t0 = time.perf_counter()
        fib_naive(n, {"calls": 0, "adds": 0})
        t1 = time.perf_counter()
        for _ in range(200):
            fib_iter(n)
        t2 = time.perf_counter()
        t_naive.append(t1 - t0)
        t_iter.append((t2 - t1) / 200)
    a2.plot(ns2, t_naive, "o-", label="naive recursive")
    a2.plot(ns2, t_iter, "s-", label="iterative")
    a2.set_yscale("log")
    a2.set_xlabel("n")
    a2.set_ylabel("seconds (log scale)")
    a2.set_title("Fibonacci running time")
    a2.legend(fontsize=8)
    a2.grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print("saved", path)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    which = args[0] if args else "all"
    want_plot = "--plot" in sys.argv
    if which in ("1", "all"):
        module1()
        if want_plot:
            plot_module1()
    if which in ("2", "all"):
        module2()
        if want_plot:
            plot_module2()
    print("\n%s" % ("ALL CHECKS PASSED" if not FAILED else "FAILED: %d check(s)" % len(FAILED)))
    sys.exit(1 if FAILED else 0)
