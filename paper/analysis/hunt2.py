import numpy as np
from scipy.optimize import linprog, minimize
rng = np.random.default_rng(11)

def is_tp2_rows(M, tol=1e-11):
    n, m = M.shape
    for i in range(n-1):
        for y1 in range(m):
            for y2 in range(y1+1, m):
                if M[i, y2]*M[i+1, y1] > M[i, y1]*M[i+1, y2] + tol: return False
    return True

def rand_tp2(n, m):
    """General positive TP2 matrix: row_{i+1} = normalize(row_i * increasing factors)."""
    M = [rng.dirichlet(np.ones(m)*rng.uniform(0.5,3))]
    for _ in range(n-1):
        r = np.cumsum(rng.uniform(0.05, 1.0, m))   # increasing positive factors
        v = M[-1]*r
        M.append(v/v.sum())
    return np.array(M)

def rand_fosd_rev_kernels(n, m, my, allow_zero=True):
    K0 = rng.dirichlet(np.ones(my)*rng.uniform(0.3,2), size=m)
    Ks = [K0]
    for i in range(1, n):
        K = Ks[-1].copy()
        for x in range(m):
            for _ in range(rng.integers(1, 5)):
                hi = rng.integers(1, my); lo = rng.integers(0, hi)
                frac = rng.uniform(0.2, 1.0) if allow_zero else rng.uniform(0.1, 0.8)
                amt = frac * K[x, hi]
                K[x, hi] -= amt; K[x, lo] += amt
        Ks.append(K)
    return Ks

def build_eq(F, G, NS, NX, NY):
    nv = NS*NX*NY; vid = lambda i,x,y: i*NX*NY + x*NY + y
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

def seq_lr_lp(F, G, NS, NX, NY, n_restarts=25):
    """Sequential/alternating LP: pick Lam_1 with marginal G_1 (random vertex),
    then Lam_{i+1} in the polytope {marginal G_{i+1}, rows LR-below Lam_i's rows}.
    LR-below-fixed-nu is LINEAR. Multiple random restarts + alternating sweeps."""
    vidx = lambda x,y: x*NY + y
    def state_lp(Fi, Gi, prev=None, nxt=None, cobj=None):
        nv = NX*NY
        Aeq, beq = [], []
        for x in range(NX):
            r = np.zeros(nv)
            for y in range(NY): r[vidx(x,y)] = 1
            Aeq.append(r); beq.append(1.0)
        for y in range(NY):
            r = np.zeros(nv)
            for x in range(NX): r[vidx(x,y)] = Fi[x]
            Aeq.append(r); beq.append(Gi[y])
        Aub, bub = [], []
        for x in range(NX):
            for y1 in range(NY):
                for y2 in range(y1+1, NY):
                    if prev is not None:  # need prev(x,·) LR-dominates THIS row
                        r = np.zeros(nv)
                        r[vidx(x,y2)] = prev[x,y1]; r[vidx(x,y1)] = -prev[x,y2]
                        Aub.append(r); bub.append(0.0)
                    if nxt is not None:   # THIS row LR-dominates nxt(x,·)
                        r = np.zeros(nv)
                        r[vidx(x,y1)] = nxt[x,y2]; r[vidx(x,y2)] = -nxt[x,y1]
                        Aub.append(r); bub.append(0.0)
        c = cobj if cobj is not None else np.zeros(nv)
        res = linprog(c, A_ub=np.array(Aub) if Aub else None,
                      b_ub=np.array(bub) if bub else None,
                      A_eq=np.array(Aeq), b_eq=np.array(beq),
                      bounds=[(0,1)]*nv, method="highs")
        return (res.x.reshape(NX,NY) if res.status == 0 else None)
    for _ in range(n_restarts):
        L = [None]*NS
        L[0] = state_lp(F[0], G[0], cobj=rng.normal(size=NX*NY))
        if L[0] is None: return None, "state0_infeasible"
        ok = True
        for i in range(1, NS):
            L[i] = state_lp(F[i], G[i], prev=L[i-1], cobj=rng.normal(size=NX*NY))
            if L[i] is None: ok = False; break
        if ok: return L, "feasible"
        # alternating sweeps: refit middle states given both neighbors
        for sweep in range(6):
            L[0] = state_lp(F[0], G[0], nxt=L[1] if L[1] is not None else None,
                            cobj=rng.normal(size=NX*NY))
            good = L[0] is not None
            for i in range(1, NS):
                if not good: break
                L[i] = state_lp(F[i], G[i], prev=L[i-1],
                                nxt=L[i+1] if (i+1 < NS and L[i+1] is not None) else None,
                                cobj=rng.normal(size=NX*NY))
                good = L[i] is not None
            if good: return L, "feasible"
    return None, "not_found"

def mqg_lp_ok(F, G, NS, NX, NY):
    nv = NS*NX*NY; vid = lambda i,x,y: i*NX*NY + x*NY + y
    Aeq, beq = build_eq(F, G, NS, NX, NY)
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

candidates = []
tested = 0
for trial in range(400):
    NS = int(rng.integers(3, 5))
    NX = int(rng.integers(2, 4))
    NY = int(rng.integers(3, 5))
    F = rand_tp2(NS, NX)
    Ks = rand_fosd_rev_kernels(NS, NX, NY)
    G = np.array([F[i] @ Ks[i] for i in range(NS)])
    if not is_tp2_rows(G): continue
    tested += 1
    L, status = seq_lr_lp(F, G, NS, NX, NY, n_restarts=12)
    if status != "feasible":
        # confirm MQG really holds via the joint LP (it should, by construction)
        if mqg_lp_ok(F, G, NS, NX, NY):
            candidates.append((NS, NX, NY, F.copy(), G.copy()))
            print(f"trial {trial}: LR search failed (NS={NS},NX={NX},NY={NY}) — candidate")
    if len(candidates) >= 5: break

print(f"\ntested {tested} MQG instances with MLR F and MLR G; "
      f"{len(candidates)} candidates where no LR kernel was found")
if candidates:
    np.savez("candidates2.npz", n=len(candidates),
             **{f"F{k}": c[3] for k, c in enumerate(candidates)},
             **{f"G{k}": c[4] for k, c in enumerate(candidates)})
