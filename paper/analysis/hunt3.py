import numpy as np
from scipy.optimize import linprog
rng = np.random.default_rng(23)
exec(open("hunt2.py").read().split("candidates = []")[0].replace('rng = np.random.default_rng(11)','')) # reuse helpers

def rand_fosd_rev_kernels_mild(n, m, my, strength):
    K0 = rng.dirichlet(np.ones(my)*rng.uniform(0.5,2), size=m)
    Ks = [K0]
    for i in range(1, n):
        K = Ks[-1].copy()
        for x in range(m):
            for _ in range(rng.integers(1, 3)):
                hi = rng.integers(1, my); lo = rng.integers(0, hi)
                amt = rng.uniform(0, strength) * K[x, hi]
                K[x, hi] -= amt; K[x, lo] += amt
        Ks.append(K)
    return Ks

stats = {"A_tested":0, "A_cand":0, "B_tested":0, "B_cand":0}
cands = []
for trial in range(1200):
    NS = int(rng.integers(3, 5)); NX = int(rng.integers(2, 4)); NY = int(rng.integers(3, 5))
    F = rand_tp2(NS, NX)
    strength = rng.uniform(0.1, 0.9)
    Ks = rand_fosd_rev_kernels_mild(NS, NX, NY, strength)
    G = np.array([F[i] @ Ks[i] for i in range(NS)])
    track = "A" if is_tp2_rows(G) else "B"
    if track == "B" and rng.random() < 0.5: continue   # keep both tracks populated
    stats[track+"_tested"] += 1
    L, status = seq_lr_lp(F, G, NS, NX, NY, n_restarts=8)
    if status != "feasible" and mqg_lp_ok(F, G, NS, NX, NY):
        stats[track+"_cand"] += 1
        cands.append((track, NS, NX, NY, F.copy(), G.copy()))
        print(f"trial {trial} [{track}] NS={NS} NX={NX} NY={NY}: no LR kernel found")
        if len(cands) >= 6: break
print("\nstats:", stats)
if cands:
    import pickle; pickle.dump(cands, open("cands3.pkl","wb"))
