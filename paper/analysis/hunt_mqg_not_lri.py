import numpy as np
from scipy.optimize import linprog, minimize, differential_evolution
from scipy.stats import binom
rng = np.random.default_rng(7)

NS, NX, NY = 3, 2, 3   # states, X-signals, Y-signals

def is_tp2_rows(M, tol=1e-11):
    n, m = M.shape
    for i in range(n-1):
        for y1 in range(m):
            for y2 in range(y1+1, m):
                if M[i, y2]*M[i+1, y1] > M[i, y1]*M[i+1, y2] + tol: return False
    return True

def build_eq(F, G):
    """Equalities for kernel L[i,x,y]: row sums 1; sum_x F[i,x] L[i,x,y] = G[i,y]."""
    nv = NS*NX*NY
    vid = lambda i,x,y: i*NX*NY + x*NY + y
    A, b = [], []
    for i in range(NS):
        for x in range(NX):
            r = np.zeros(nv)
            for y in range(NY): r[vid(i,x,y)] = 1
            A.append(r); b.append(1.0)
        for y in range(NY):
            r = np.zeros(nv)
            for x in range(NX): r[vid(i,x,y)] = F[i,x]
            A.append(r); b.append(G[i,y])
    return np.array(A), np.array(b)

def mqg_lp(F, G):
    """FOSD-reversed kernel feasibility (linear)."""
    nv = NS*NX*NY; vid = lambda i,x,y: i*NX*NY + x*NY + y
    Aeq, beq = build_eq(F, G)
    Aub, bub = [], []
    for i in range(NS-1):
        for x in range(NX):
            for j in range(NY-1):
                r = np.zeros(nv)
                for y in range(j+1):
                    r[vid(i,x,y)] = 1; r[vid(i+1,x,y)] = -1
                Aub.append(r); bub.append(0.0)
    res = linprog(np.zeros(nv), A_ub=np.array(Aub), b_ub=np.array(bub),
                  A_eq=Aeq, b_eq=beq, bounds=[(0,1)]*nv, method="highs")
    return res.status == 0

def lr_violation(L):
    """Total violation of reversely-LR monotonicity (lower state LR-dominates)."""
    v = 0.0
    for i in range(NS-1):
        for x in range(NX):
            for y1 in range(NY):
                for y2 in range(y1+1, NY):
                    v += max(0.0, L[i,x,y1]*L[i+1,x,y2] - L[i,x,y2]*L[i+1,x,y1])
    return v

def lr_feasibility(F, G, n_de=2, n_ms=40):
    """Global-ish search for reversely-LR kernel: nullspace parametrization +
    differential evolution + SLSQP multistart. Returns best violation found."""
    Aeq, beq = build_eq(F, G)
    x0, *_ = np.linalg.lstsq(Aeq, beq, rcond=None)
    U, S, Vt = np.linalg.svd(Aeq)
    null = Vt[np.sum(S > 1e-10):].T          # nv x k
    k = null.shape[1]
    def unpack(z):
        return (x0 + null @ z).reshape(NS, NX, NY)
    def penalty(z):
        L = unpack(z)
        box = np.sum(np.maximum(0, -L)**2) + np.sum(np.maximum(0, L-1)**2)
        return 1000*box + lr_violation(np.clip(L, 0, 1))
    best = np.inf; bestz = None
    for _ in range(n_de):
        r = differential_evolution(penalty, bounds=[(-3,3)]*k, seed=int(rng.integers(1e6)),
                                   maxiter=300, tol=1e-12, polish=True)
        if r.fun < best: best, bestz = r.fun, r.x
    for _ in range(n_ms):
        z0 = rng.normal(scale=1.0, size=k)
        r = minimize(penalty, z0, method="Nelder-Mead",
                     options={"maxiter": 4000, "fatol": 1e-14, "xatol": 1e-12})
        if r.fun < best: best, bestz = r.fun, r.x
    return best, unpack(bestz)

def fosd_rev_kernels_hard():
    """FOSD-reversed kernels engineered to be far from LR-ordered:
    lower-state rows bimodal (mass at extremes), higher-state rows unimodal."""
    Ks = []
    base = []
    for x in range(NX):
        a = rng.uniform(0.2, 0.45); b = rng.uniform(0.2, 0.45)
        base.append(np.array([a, 1-a-b, b]))   # state 0 row: spread
    Ks.append(np.array(base))
    for i in range(1, NS):
        K = Ks[-1].copy()
        for x in range(NX):
            # move mass downward (FOSD reversal), deliberately from the top
            # into the MIDDLE (kills LR comparability)
            amt = rng.uniform(0.3, 0.9) * K[x,2]
            K[x,2] -= amt; K[x,1] += amt
            amt2 = rng.uniform(0.0, 0.3) * K[x,1]
            K[x,1] -= amt2; K[x,0] += amt2
        Ks.append(K)
    return Ks

found = []
for trial in range(60):
    ps = np.sort(rng.uniform(0.15, 0.85, NS))
    if np.min(np.diff(ps)) < 0.15: continue
    F = np.array([[1-p, p] for p in ps])       # binary-signal MLR family
    Ks = fosd_rev_kernels_hard()
    G = np.array([F[i] @ Ks[i] for i in range(NS)])
    if not is_tp2_rows(G): continue            # want G MLR (paper-relevant)
    if np.min(G) < 1e-3: continue
    assert mqg_lp(F, G), "construction guarantees MQG"
    best, L = lr_feasibility(F, G, n_de=1, n_ms=15)
    if best > 1e-7:
        found.append((best, F.copy(), G.copy()))
        print(f"trial {trial}: candidate! min LR-violation = {best:.3e}")
    if len(found) >= 3: break

if not found:
    print("No MQG-but-not-LRI candidate found in this sweep (all LR-feasible).")
else:
    # harden the best candidate with a heavier search
    found.sort(key=lambda t: -t[0])
    best0, F, G = found[0]
    b2, L2 = lr_feasibility(F, G, n_de=4, n_ms=150)
    np.set_printoptions(precision=5, suppress=True)
    print("\n=== BEST CANDIDATE after heavy search ===")
    print("F=\n", F, "\nG=\n", G)
    print(f"min LR-violation: light={best0:.3e}, heavy={b2:.3e}")
    np.savez("candidate.npz", F=F, G=G)
