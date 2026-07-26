import numpy as np
from scipy.optimize import linprog

def is_tp2(M, tol=1e-12):
    n, m = M.shape
    for i in range(n-1):
        for y1 in range(m):
            for y2 in range(y1+1, m):
                if M[i, y2]*M[i+1, y1] > M[i, y1]*M[i+1, y2] + tol: return False
    return True

# Krishnamurthy p.6, hierarchical sensing example: B(1) = M x B(2)
F = np.array([[0.4387,0.5190,0.0423],[0.2455,0.6625,0.0920],[0.0615,0.2829,0.6556]])  # B(2) better
G = np.array([[0.3229,0.4703,0.2068],[0.2237,0.4902,0.2861],[0.1587,0.4620,0.3793]])  # B(1) worse
print("F TP2 (MLR):", is_tp2(F), "| G TP2 (MLR):", is_tp2(G))

X = 2
a7b = all(G[i,0]*F[X,0] <= F[i,0]*G[X,0] + 1e-10 for i in range(3))
a7t = all(G[i,-1]*F[X,-1] >= F[i,-1]*G[X,-1] - 1e-10 for i in range(3))
print("A7 finite (bottom, top):", a7b, a7t)

def mqg_lp(F, G, lr_pairs=None):
    """Feasibility LP for a state-dependent kernel Gam[i,x,y] with
    F[i]@Gam[i] = G[i], rows stochastic, reversely FOSD monotone.
    lr_pairs: optional extra linear constraints (for iterative LR check)."""
    n, m = F.shape; my = G.shape[1]; nv = n*m*my
    vid = lambda i,x,y: i*m*my + x*my + y
    Aeq, beq = [], []
    for i in range(n):
        for x in range(m):
            row = np.zeros(nv)
            for y in range(my): row[vid(i,x,y)] = 1
            Aeq.append(row); beq.append(1.0)
        for y in range(my):
            row = np.zeros(nv)
            for x in range(m): row[vid(i,x,y)] = F[i,x]
            Aeq.append(row); beq.append(G[i,y])
    Aub, bub = [], []
    for i in range(n-1):
        for x in range(m):
            for j in range(my-1):
                row = np.zeros(nv)
                for y in range(j+1):
                    row[vid(i,x,y)] = 1; row[vid(i+1,x,y)] = -1
                Aub.append(row); bub.append(0.0)
    res = linprog(np.zeros(nv), A_ub=np.array(Aub), b_ub=np.array(bub),
                  A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=[(0,1)]*nv, method="highs")
    return res

res = mqg_lp(F, G)
print("MQG (reversely FOSD) kernel exists:", res.status == 0)
if res.status == 0:
    Gam = res.x.reshape(3,3,3)
    def rev_lr_viol(Gam, tol=1e-9):
        v = []
        for i in range(2):
            for x in range(3):
                for y1 in range(3):
                    for y2 in range(y1+1,3):
                        lhs = Gam[i,x,y2]*Gam[i+1,x,y1]; rhs = Gam[i,x,y1]*Gam[i+1,x,y2]
                        if lhs < rhs - tol: v.append((i,x,y1,y2,lhs,rhs))
        return v
    v = rev_lr_viol(Gam)
    print("LR-monotonicity violations in this MQG solution:", len(v))
    np.set_printoptions(precision=4, suppress=True)
    for i in range(3): print(f"Gamma(state {i}) =\n", Gam[i])

# Also: try a randomized search for a reversely-LR kernel (nonconvex, so
# absence of success is only suggestive, not proof).
rng = np.random.default_rng(2)
found = False
for t in range(4000):
    # random objective pushes LP vertex solutions around the feasible polytope
    c = rng.normal(size=27)
    n, m, my = 3,3,3; vid = lambda i,x,y: i*9 + x*3 + y
    Aeq, beq, Aub, bub = [], [], [], []
    for i in range(3):
        for x in range(3):
            row = np.zeros(27)
            for y in range(3): row[vid(i,x,y)] = 1
            Aeq.append(row); beq.append(1.0)
        for y in range(3):
            row = np.zeros(27)
            for x in range(3): row[vid(i,x,y)] = F[i,x]
            Aeq.append(row); beq.append(G[i,y])
    for i in range(2):
        for x in range(3):
            for j in range(2):
                row = np.zeros(27)
                for y in range(j+1):
                    row[vid(i,x,y)] = 1; row[vid(i+1,x,y)] = -1
                Aub.append(row); bub.append(0.0)
    r = linprog(c, A_ub=np.array(Aub), b_ub=np.array(bub), A_eq=np.array(Aeq),
                b_eq=np.array(beq), bounds=[(0,1)]*27, method="highs")
    if r.status == 0:
        Gam = r.x.reshape(3,3,3)
        ok = True
        for i in range(2):
            for x in range(3):
                for y1 in range(3):
                    for y2 in range(y1+1,3):
                        if Gam[i,x,y2]*Gam[i+1,x,y1] < Gam[i,x,y1]*Gam[i+1,x,y2] - 1e-9: ok = False
        if ok:
            found = True
            print(f"Found reversely-LR kernel at trial {t}")
            for i in range(3): print(f"Gamma(state {i}) =\n", Gam[i])
            break
print("Reversely-LR (LR-better) kernel found by randomized search:", found)
