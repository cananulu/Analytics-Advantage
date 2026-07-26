import numpy as np
from scipy.optimize import linprog
from scipy.stats import binom
rng = np.random.default_rng(1)

def a7_finite(F, G, tol=1e-10):
    X = F.shape[0]-1
    for i in range(F.shape[0]):
        if G[i,0]*F[X,0] > F[i,0]*G[X,0] + tol: return False
        if G[i,-1]*F[X,-1] < F[i,-1]*G[X,-1] - tol: return False
    return True

def mlr_matrix(n, m):
    ps = np.sort(rng.uniform(0.05, 0.95, size=n))
    return np.array([binom.pmf(np.arange(m), m-1, p) for p in ps])

def mqg_kernels(n, m, my):
    """State-dependent kernels, reversely FOSD-monotone by construction:
    start from a random kernel for the LOWEST state, then for each higher
    state repeatedly move random mass from a higher-y bin to a lower-y bin."""
    Ks = [rng.dirichlet(np.ones(my), size=m)]
    for i in range(1, n):
        K = Ks[-1].copy()
        for x in range(m):
            for _ in range(rng.integers(1, 4)):
                y_hi = rng.integers(1, my); y_lo = rng.integers(0, y_hi)
                amt = rng.uniform(0, K[x, y_hi])
                K[x, y_hi] -= amt; K[x, y_lo] += amt
        Ks.append(K)
    return Ks

viol = 0; total = 0
for trial in range(2000):
    n, m, my = rng.integers(2,5), rng.integers(2,5), rng.integers(2,5)
    F = mlr_matrix(n, m)
    Ks = mqg_kernels(n, m, my)
    G = np.array([F[i] @ Ks[i] for i in range(n)])
    total += 1
    if not a7_finite(F, G):
        viol += 1
        if viol == 1:
            np.set_printoptions(precision=4, suppress=True)
            print("VIOLATION EXAMPLE:\nF=\n", F, "\nG=\n", G)
print(f"Test 1 (MQG + MLR(F) => A7-finite): {total} instances, {viol} violations")
