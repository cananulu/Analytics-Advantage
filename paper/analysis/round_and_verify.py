import numpy as np
from scipy.optimize import linprog, minimize, differential_evolution
rng = np.random.default_rng(9)
np.set_printoptions(precision=4, suppress=True)
d = np.load("verified_candidate.npz"); F0, G0 = d["F"], d["G"]
NS, NX, NY = 3, 2, 3

# round to 3 decimals, renormalize rows exactly
F = np.round(F0, 3); F[:, -1] = 1 - F[:, :-1].sum(1)
G = np.round(G0, 3); G[:, -1] = 1 - G[:, :-1].sum(1)
print("F=\n", F, "\nG=\n", G)

def is_tp2_rows(M, tol=1e-12):
    for i in range(M.shape[0]-1):
        for y1 in range(M.shape[1]):
            for y2 in range(y1+1, M.shape[1]):
                if M[i,y2]*M[i+1,y1] > M[i,y1]*M[i+1,y2] + tol: return False
    return True
print("F MLR:", is_tp2_rows(F), "| G MLR:", is_tp2_rows(G))

vid3 = lambda i,x,y: i*NX*NY + x*NY + y
def build_eq(F, G):
    nv = NS*NX*NY; A,b = [],[]
    for i in range(NS):
        for x in range(NX):
            r = np.zeros(nv)
            for y in range(NY): r[vid3(i,x,y)] = 1
            A.append(r); b.append(1.0)
        for y in range(NY):
            r = np.zeros(nv)
            for x in range(NX): r[vid3(i,x,y)] = F[i,x]
            A.append(r); b.append(G[i,y])
    return np.array(A), np.array(b)

# MQG feasibility (joint FOSD LP) on the rounded instance
Aeq, beq = build_eq(F, G)
Aub, bub = [], []
for i in range(NS-1):
    for x in range(NX):
        for j in range(NY-1):
            r = np.zeros(NS*NX*NY)
            for y in range(j+1):
                r[vid3(i,x,y)] = 1; r[vid3(i+1,x,y)] = -1
            Aub.append(r); bub.append(0.0)
res = linprog(np.zeros(NS*NX*NY), A_ub=np.array(Aub), b_ub=np.array(bub),
              A_eq=Aeq, b_eq=beq, bounds=[(0,1)]*(NS*NX*NY), method="highs")
print("MQG (FOSD-reversed kernel) feasible:", res.status == 0)
if res.status == 0:
    K = res.x.reshape(NS,NX,NY)
    print("an MQG kernel (rows y=1..3):")
    for i in range(NS): print(f" state {i+1}:\n", K[i])

# Blackwell LP
nv2 = NX*NY; vid = lambda x,y: x*NY+y
A2,b2 = [],[]
for x in range(NX):
    r = np.zeros(nv2)
    for y in range(NY): r[vid(x,y)] = 1
    A2.append(r); b2.append(1.0)
for i in range(NS):
    for y in range(NY):
        r = np.zeros(nv2)
        for x in range(NX): r[vid(x,y)] = F[i,x]
        A2.append(r); b2.append(G[i,y])
rB = linprog(np.zeros(nv2), A_eq=np.array(A2), b_eq=np.array(b2),
             bounds=[(0,1)]*nv2, method="highs")
print("Blackwell:", rB.status == 0)

# discrete Lehmann
Fc, Gc = np.cumsum(F,1), np.cumsum(G,1)
phi = lambda i,y: max([x for x in range(NX) if Fc[i,x] <= Gc[i,y]+1e-12], default=-1)
print("discrete Lehmann:", all(phi(i+1,y) >= phi(i,y) for i in range(NS-1) for y in range(NY)))

# heavy global LR search
x0,*_ = np.linalg.lstsq(Aeq,beq,rcond=None)
U,S,Vt = np.linalg.svd(Aeq); Nsp = Vt[np.sum(S>1e-10):].T; k = Nsp.shape[1]
def lrviol(L):
    v=0.0
    for i in range(NS-1):
        for x in range(NX):
            for y1 in range(NY):
                for y2 in range(y1+1,NY):
                    v += max(0.0, L[i,x,y1]*L[i+1,x,y2]-L[i,x,y2]*L[i+1,x,y1])
    return v
def pen(z):
    L=(x0+Nsp@z).reshape(NS,NX,NY)
    return 2000*(np.sum(np.maximum(0,-L)**2)+np.sum(np.maximum(0,L-1)**2)) + lrviol(np.clip(L,0,1))
best=np.inf
for seed in range(10):
    r = differential_evolution(pen, [(-4,4)]*k, seed=seed, maxiter=1000, popsize=45, tol=1e-15)
    best=min(best,r.fun)
for _ in range(500):
    r = minimize(pen, rng.normal(scale=1.5,size=k), method="Nelder-Mead",
                 options={"maxiter":8000,"fatol":1e-16,"xatol":1e-14})
    best=min(best,r.fun)
print(f"GLOBAL min LR-violation (rounded instance): {best:.6e}")
np.savez("counterexample_final.npz", F=F, G=G)
