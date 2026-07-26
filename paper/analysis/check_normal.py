import numpy as np
from scipy.stats import norm
np.set_printoptions(precision=5, suppress=True)

# Discretized Normal example: states mu_i, F = N(mu_i, sig^2),
# G = N(m_i, sig^2+nu^2), m(mu) = mu + d(mu).
sig, nu = 1.0, 0.7
s = np.sqrt(sig**2 + nu**2)
mus = np.array([0.0, 0.5, 1.0])

def run_case(name, mprime):
    """m(mu) = mprime*mu (so d(mu) = (mprime-1)*mu; d decreasing iff mprime<1)."""
    ms = mprime * mus
    print(f"--- {name}: m'(mu)={mprime}, s/sig={s:.4f} ---")
    # A3: both location families with increasing means => MLR (analytic).
    print(f"A3: F MLR (Gaussian location) True | G MLR (means increasing): {np.all(np.diff(ms)>0)}")
    # A6 single crossing: phi(i) = G_i(j) - F_i(l) crosses - to + at most once, all (j,l)
    grid = np.linspace(-6, 8, 141)
    ok = True
    for j in grid:
        Gj = norm.cdf((j - ms)/s)
        for l in grid:
            Fl = norm.cdf((l - mus)/sig)
            sgn = np.sign(np.round(Gj - Fl, 12))
            nz = sgn[sgn != 0]
            # violations: any +->- transition as i increases
            if np.any((nz[:-1] > 0) & (nz[1:] < 0)): ok = False
    print("A6 (single crossing - to +): ", ok)
    # A7 (Y=R): ratio f_F/f_G finite (and bounded) in y for each state
    y = np.linspace(-12, 12, 2001)
    maxratio = max(np.max(norm.pdf(y, mus[i], sig)/norm.pdf(y, ms[i], s)) for i in range(3))
    print(f"A7 (abs. continuity): max_y f_F/f_G over states = {maxratio:.4f} (finite, bounded)")
    # Quantile (Lehmann) kernel: y(x, mu_i) = m_i + (s/sig)(x - mu_i)
    # (a) decreasing in i  <=>  m' <= s/sig   (b) pushforward of F = G exactly
    slopes_in_i = np.diff(ms - (s/sig)*mus)   # y(x,mu_i) - (s/sig) x = m_i - (s/sig) mu_i
    print("Quantile kernel atom y(x,mu_i) decreasing in i:", np.all(slopes_in_i <= 1e-12))
    i = 1; xs = np.linspace(-6, 8, 400)
    push_cdf = norm.cdf(( (ms[i] + (s/sig)*(xs - mus[i])) - ms[i])/s)  # CDF of y at its own value: sanity
    # direct check: pushforward of N(mu_i, sig^2) under affine map = N(m_i, s^2)
    err = np.max(np.abs(norm.cdf((xs - mus[i])/sig) - norm.cdf(((ms[i] + (s/sig)*(xs-mus[i])) - ms[i])/s)))
    print(f"Pushforward affine map reproduces G exactly (CDF match err): {err:.2e}")
    print()

run_case("Her example (d decreasing, delta=0.5)", mprime=0.5)      # d(mu) = -0.5 mu
run_case("d mildly INCREASING (m'=1.15 < s/sig)", mprime=1.15)     # LR-better via quantile kernel?
run_case("Beyond Lehmann boundary (m'=1.35 > s/sig)", mprime=1.35) # A6 should FAIL
