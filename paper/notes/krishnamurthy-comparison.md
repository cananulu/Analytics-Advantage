# LR-better vs. Krishnamurthy (2021), Theorem 3.4(1)

Analysis by Claude, 2026-07-26, from Krishnamurthy_2021.pdf
(arXiv:1806.08733v2, "New Sufficient Conditions for Lower Bounding the
Optimal Policy of a POMDP using Lehmann Precision," dated May 31, 2021)
and Kim (2023), now verified against the actual PDF. Verification
scripts: paper/analysis/check_a7b.py and check_lp.py.

## TL;DR

Canan's reading is essentially correct, with one important amendment:

1. **The ordering chain is right.** Under the MLR assumptions our
   Theorem 3.1 already makes, LR-better ⇒ MQG ⇒ Lehmann (Kim's
   Proposition 3 / Theorem 1, which require MLRP on the better
   process — we assume it). So on the *ordering* dimension his
   Lehmann-precision condition (A6) is weaker, i.e., more permissive,
   than LR-better.

2. **But the A7 escape route is closed in finite signal spaces.** For
   finite (and boundary-interval) signal spaces, LR-better — in fact
   already MQG — together with MLR of the better process *implies*
   (A7). Proof sketch below; confirmed on 2,000 random instances. **The
   example Canan hopes for (LR-better + A7 fails) cannot exist with
   finitely many signals.**

3. **The separation exists, but it lives elsewhere** (see §4 below):
   (a) model class — his Theorem 3.4 is stated only for finite-state
   *controlled sensing* POMDPs (transition matrix action-independent
   and common to both systems), which excludes machine replacement,
   technology adoption with absorbing adopt/reject, and every
   action-dependent-transition model our theorem covers; (b) state
   space — his machinery is intrinsically finite-state (line segments
   in the simplex), ours allows Θ ⊆ ℝ; (c) signal support — for
   continuum signals A7 is an *absolute-continuity* condition
   F(y|θ)/G(y|θ) < ∞, and our **Uniform-scaling family violates it**
   (details in §5 — this is the closest thing to the example Canan
   wants, with a caveat about his [a,b] carve-out).

4. **Honest flip side:** within finite-state, finite-signal controlled
   sensing, his Theorem 3.4(1) *subsumes* our Theorem 3.1 — his order
   is weaker AND his reward assumptions are weaker (A1 monotone
   rewards only; no increasing differences, no stochastic increasing
   differences, no monotone-policy machinery). Our positioning should
   not claim otherwise. It also raises a research question for us: can
   our Theorem 3.1 drop the supermodularity assumptions?

## 1. His setup and Theorem 3.4(1), in our notation

Finite states {1,…,X} ordered; observation space Y finite, ℝ, or
[a,b]; infinite-horizon discounted reward (results also hold finite
horizon). Assumptions used by Theorem 3.4(1), translated:

- (A1) r(i,u) increasing in i — our "r increasing in θ".
- (A2) P TP2 — our "g satisfies MLR". In Thm 3.4 P is
  action-independent and **common to the two systems** (controlled
  sensing).
- (A3) B(u) TP2 — our "likelihoods satisfy MLR".
- (A6) [Lehmann precision] For all j,l: i ↦ Σ_{y≤j} B̄_iy − Σ_{y≤l} B_iy
  changes sign at most once from − to + (B = better, B̄ = worse; his
  notation B(u+1) >_L B(u) with u+1 the better). This is the
  single-crossing/"integral precision" form of Lehmann's order.
- (A7) If Y = ℝ: B_iy/B̄_iy < ∞ (better's density absolutely continuous
  w.r.t. worse's, per state). If Y finite (or [a,b]): boundary
  conditions at the lowest and highest signals:
    B̄_{i,min} B_{X,min} ≤ B_{i,min} B̄_{X,min}  and
    B̄_{i,max} B_{X,max} ≥ B_{i,max} B̄_{X,max}  for all i.
  Its role (his Theorem 4.4): the range of the top component of the
  posterior under the worse system is contained in that under the
  better system — this feeds the wedge-function convex-dominance proof
  (Theorem 4.5, Case 2 is exactly where A7 prevents 𝒴₂^λ = ∅ with
  𝒴₁^λ ≠ ∅).

Theorem 3.4(1): two controlled sensing POMDPs with common P and
identical rewards, observation families B(u), B̄(u). If B(u) >_L B̄(u)
for every u and A1, A2, A3, A7 hold, then the optimal discounted value
satisfies J_{μ*(θ)}(π) ≥ J_{μ*(θ̄)}(π) for all π.

## 2. The ordering chain (now verified against Kim's PDF)

Kim Def 3 (MQG), Def 4 (Lehmann accuracy), Def 5 (MLRP), Props 1–4,
Thm 1 — all verified; our draft Section 4 states them correctly. Chain
under our Theorem 3.1's assumptions (MLR on L_X):

  X ⪰_B Y ⇒ X ⪰_LRI Y ⇒ X ⪰_MQG Y ⇔ X ⪰_L Y   (last step: Kim Thm 1)

Two residual items to nail down for the paper:
- A6 (single-crossing of CDF differences) vs. Kim's Def 4 (quantile
  map Φ increasing): these are the standard two formulations of
  Lehmann's order; Krishnamurthy cites Mizuno (2006) and Jewitt (2007)
  for the single-crossing form. We should either cite for the
  equivalence or prove a small lemma. NOT yet verified line-by-line.
- Kim's framework is continuum-signal (discrete handled by his
  footnote-8 smoothing). If we invoke his Thm 1 for discrete examples,
  we should say a word about that transformation.

## 3. Result: MQG + MLR(better) ⇒ A7, finite signal case

Claim. Let F = L_X (better), G = L_Y (worse) on finite ordered signal
sets with G(y|θ) = Σ_x P(y|x,θ) F(x|θ) and P(·|x,θ) reversely
FOSD-monotone in θ (Kim's MQG condition — implied by our LR-better).
If F is MLR (TP2), then both A7 boundary inequalities hold.

Proof sketch (bottom inequality; top is symmetric). With θ̄ the top
state, we must show G(y_min|θ) F(x_min|θ̄) ≤ G(y_min|θ̄) F(x_min|θ).
Expand G(y_min|θ) = Σ_x P(y_min|x,θ) F(x|θ) and compare the sums term
by term:
- P(y_min|x,θ) ≤ P(y_min|x,θ̄): reversely monotone noise puts more
  mass on the lowest signal in higher states (FOSD reversal evaluated
  at the bottom of the signal range);
- F(x|θ) F(x_min|θ̄) ≤ F(x|θ̄) F(x_min|θ) for every x ≥ x_min: this is
  exactly the TP2 (MLR) inequality for F.
Multiplying the ordered nonnegative factors and summing over x gives
the claim. ∎ (No positivity needed; works with zeros.)

Numerical confirmation: 2,000 random instances (states 2–4, signals
2–4, random MLR F via Binomial rows, random reversely-FOSD kernels via
downward mass shifts): zero violations (paper/analysis/check_a7b.py).

Consequence: **in finite signal spaces, every LR-better pair satisfies
A6 (via Kim) and A7 (above), so it lies inside the assumption set of
Theorem 3.4(1) whenever the model itself is finite-state controlled
sensing.** The separation cannot be made through A7 there. This is
worth stating in the paper as a lemma — it sharpens the relationship
map and shows our order sits strictly inside his assumption set on the
overlap of the two model classes.

## 4. Where the two setups genuinely separate

(a) **Action-dependent state dynamics.** Thm 3.4 requires the two
POMDPs to share one action-independent transition matrix P. Machine
replacement (replace resets the state), technology adoption with
absorbing adopt/reject, patient treatment — all have action-dependent
transitions and are outside Thm 3.4 as stated. Our Theorem 3.1 covers
them. This is the cleanest and most defensible differentiation.

(b) **State space.** His proof machinery (MLR total order on line
segments l(e_X, π̄) of the simplex; piecewise-linear wedge
representation from Sondik) is intrinsically finite-state. Our Θ ⊆ ℝ
is general; all three of our garbling families (Normal, Poisson,
Uniform) have continuous states. (Two-state discretizations of our
examples do fall in his class — see §5.)

(c) **Signal support** (the A7 story, continuum case) — next section.

(d) **His side of the ledger:** no supermodularity anywhere. Our
Theorem 3.1 assumes increasing differences + stochastic increasing
differences (needed for the monotone-selection step in our
Lemma 3.1). On finite-state controlled sensing with finite signals,
his theorem is strictly stronger. Two implications for us: (i)
position the paper on (a)+(b), not on the ordering; (ii) open problem
worth attacking — can our main theorem drop increasing differences?
Kim's static sufficiency (his Thm 2) needs only general monotone
decision problems, and Krishnamurthy's dynamic result needs only
monotone rewards; both suggest our supermodularity assumptions may be
an artifact of our proof, not of the truth.

## 5. The Uniform-scaling family vs. A7 (continuum)

Take Θ = {θ₁ < θ₂}, F(·|θ) = U[0, θ], G(·|θ) = U[0, d(θ)θ] with d
decreasing, d(θ)θ increasing (our Section 5.2.3 example; LR-better
holds; both families MLR).

- **ℝ-reading of A7 fails:** for y ∈ (d(θ)θ, θ], the better density is
  1/θ > 0 while the worse density is 0, so F(y|θ)/G(y|θ) = ∞ — the
  absolute-continuity condition is violated on a positive-measure set.
- **[a,b]-reading is vacuous at the top:** at b = θ₂ both boundary
  products are 0, so inequality (6) holds trivially (bottom boundary
  holds because d is decreasing). BUT the conclusion A7 is designed to
  deliver — his Theorem 4.4's posterior-range nesting — genuinely
  FAILS for this pair: with two states, the top-component posterior
  under F takes values {q_F, 1} and under G takes values {q_G, 1}
  with q_G = 1/(1 + (π₁/π₂)(d₂θ₂/d₁θ₁)) > q_F =
  1/(1 + (π₁/π₂)(θ₂/θ₁)), and {q_G, 1} ⊄ {q_F, 1}. So under the
  literal [a,b] reading, the Uniform pair satisfies A2, A3, A7 but
  violates Theorem 4.4's conclusion — which indicates his [a,b]
  version implicitly presumes positive (or at least mutually
  absolutely continuous) densities, i.e., the operative content of A7
  is the absolute-continuity reading, and the Uniform family violates
  it. **Canan: please verify the q_F/q_G computation (it is two
  lines) — if you agree, this is the example you asked for, presented
  as "our assumptions hold, the assumption set of his Theorem 4.4/3.4
  does not," with the caveat about the [a,b] carve-out stated
  honestly.**
- Poisson thinning: his framework covers Y finite, ℝ, or [a,b] —
  a countably infinite signal alphabet (ℕ) is not covered at all as
  stated. Also F/G = e^{λ(d-1)} d^{-y} → ∞ as y → ∞, so any
  unbounded-support extension of A7 in the ratio form would fail at
  the top of the signal range.

## 6. Bonus: his hierarchical-sensing example is LR-better comparable

His p.6 example (B(1) = M × B(2), Blackwell provably fails, A3/A6/A7
hold): a randomized LP search over garbling kernels found an explicit
state-dependent kernel Γ_i(y|x) with B(2)_i Γ_i = B(1)_i, rows
stochastic, and Γ reversely LR-monotone across states
(paper/analysis/check_lp.py prints it). So **B(2) ⪰_LRI B(1)**: our
order covers his motivating non-Blackwell example. Two uses:
1. A concrete finite instance for our Proposition 4.1(i) strictness
   claim (LR-better holds, Blackwell fails — his paper supplies the
   Blackwell-failure proof, we supply the kernel).
2. It reinforces that the LRI-vs-Lehmann gap is not where the papers
   differ on examples like this; the model class is.
(If we use this, we verify the kernel symbolically/at higher precision
and credit the example to Krishnamurthy 2021.)

## 7. Recommended positioning (for Canan to accept/reject)

- Cite Krishnamurthy (2021) prominently as the closest antecedent:
  Lehmann precision for value comparison in finite-state controlled
  sensing POMDPs.
- State the lemma "LR-better ⇒ A6 ∧ A7 (finite signals)" — it makes
  the relationship exact rather than hand-wavy.
- Differentiate on: action-dependent transitions (our applications),
  general state spaces, continuum signal supports without absolute
  continuity (Uniform family), and necessity-side connections to Kim.
- Acknowledge that on the overlap (finite controlled sensing) his
  result is stronger, and flag "drop increasing differences?" as a
  question we either resolve or list as future work.

## 8. The Normal example vs. Krishnamurthy's assumptions (added 2026-07-26)

Setup (discretized to finitely many states, as his framework requires):
states μ₁ < … < μ_X; better system F_i = N(μ_i, σ²); worse system
G_i = N(m_i, σ² + ν²) with m(μ) = μ + d(μ) increasing. Signal space ℝ
(his continuum case). Script: paper/analysis/check_normal.py.

- **A3 (TP2 observations):** both hold — Gaussian location families
  with increasing means are MLR.
- **A6 (Lehmann precision):** holds if and only if m'(μ) ≤ s/σ where
  s = √(σ²+ν²). Derivation: the Lehmann quantile map is
  Φ(μ; y) = μ + (σ/s)(y − m(μ)), increasing in μ ⟺ m' ≤ s/σ; the
  single-crossing form (A6) then follows because {G_i(j) ≥ F_i(l)} ⟺
  {Φ(μ_i; j) ≥ l} is an upper set in i. Her conditions (d decreasing ⇒
  m' ≤ 1 < s/σ) land strictly inside. Numerically confirmed, including
  failure of A6 at m' = 1.35 > s/σ ≈ 1.221.
- **A7 (ℝ-version, absolute continuity):** HOLDS — Gaussians have full
  support, and with ν² > 0 the ratio f_F/f_G is even bounded (the
  better system has thinner tails). Numerically: max ratio ≈ 1.58 in
  her parameterization.
- **A2:** whatever TP2 action-independent P is attached (identity for
  a static state) — satisfiable.

**Conclusion: the Normal example does NOT separate our setup from
Krishnamurthy's.** After any finite discretization it satisfies every
assumption of his Theorem 3.4(1). Its only escapes from his framework
are (i) the continuous state space of the original example and (ii)
embedding in a model with action-dependent transitions (e.g.,
technology adoption). Among our three families, only the **Uniform**
family (Section 5) breaks A7 itself.

## 9a. CORRECTION (2026-07-26, after Canan's challenge): the equivalence
## is a continuum phenomenon ONLY — in discrete signal spaces
## LR-better is STRICTLY stronger than MQG. Explicit counterexample:

Canan challenged the §9 claim, and she was right to: a computational
hunt (paper/analysis/hunt_mqg_not_lri.py, round_and_verify.py) produced
an explicit discrete example that is MQG but NOT LR-better. Three
states, binary X-signals, ternary Y-signals:

    F = [ .787 .213 ]        G = [ .044 .282 .674 ]
        [ .654 .346 ]            [ .065 .726 .209 ]
        [ .515 .485 ]            [ .457 .351 .192 ]

Verified properties of this instance:
- F is MLR; G is NOT MLR.
- F ⪰_MQG G: an explicit reversely-FOSD kernel exists (LP; printed by
  the script).
- F ⪰_B G FAILS (Blackwell LP infeasible).
- Discrete Lehmann (Kim Def 4, sup version) HOLDS.
- NO reversely-LR kernel exists: global search over the entire
  6-dimensional feasible set (10 differential-evolution runs +
  500 Nelder-Mead restarts on a nullspace parametrization) bottoms out
  at LR-violation ≈ 4.6e-3, bounded away from zero; the same machinery
  provably returns 0 on LR-generated control instances.
  **Caveat: this is a strong numerical certificate, not yet an
  analytic proof — worth proving by hand (6 unknowns after
  elimination) before using in the paper.**

Two structural observations from the search:
- Every candidate found has THREE OR MORE states; two-state instances
  were always LR-feasible (consistent with Canan's "unless there are
  only two states" and with the Jewitt-dichotomy collapse).
- Every candidate found has G NOT MLR. In all searched instances where
  BOTH F and G are MLR (the assumption set of our Theorem 3.1), an
  LR kernel always existed. **Open conjecture: MQG + MLR on both
  processes ⇒ LR-better, even in discrete signal spaces.** If true,
  the equivalence survives exactly on our theorem's assumption set; if
  false, a counterexample with MLR G would be even more valuable.

Refined picture (replaces the unqualified claim of §9):
1. Atomless signal distributions + MLRP(F): LR-better = MQG = Lehmann
   (the §9 quantile-kernel argument stands, per the letter of
   Definition 3.1, which admits deterministic kernels — as does the
   authors' own Uniform example).
2. Discrete signal spaces: B ⇒ LR-better ⇒ MQG with BOTH inclusions
   strict (the second by the example above) — the outline's original
   nesting survives for discrete-signal models, which include the
   Poisson-count and Binomial-trial applications.
3. Whether MLR on G restores the equivalence in discrete spaces is
   open (see conjecture above).

## 9. Byproduct: under MLR + continuity, LR-better = MQG = Lehmann?!
## (SUPERSEDED in part — read §9a first; the argument below is correct
## for atomless signal distributions only.)

Working through A6 for the Normal case surfaced something bigger.
Kim's proof of Proposition 2 (Lehmann ⇒ MQG) constructs the garbling
kernel Γ(y|x,ω) = 1{x ≤ Φ(ω;y)} — as a distribution over y given
(x,ω), this is a **point mass** at the quantile-matching signal
y(x,ω) solving Φ(ω; y) = x. Two observations:

1. y(x,ω) is DECREASING in ω whenever Lehmann holds
   (∂y/∂ω = −Φ_ω/Φ_y ≤ 0 since Φ_ω ≥ 0 = Lehmann, Φ_y > 0).
2. For point masses, δ_a ⪰_LR δ_b ⟺ a ≥ b (the TP2 cross-product
   condition holds vacuously except at the atoms). So a deterministic
   kernel with atom decreasing in the state is reversely
   LR-monotone — it witnesses **LR-better**, not just MQG.

Hence, in Kim's continuum framework (continuous, strictly increasing
conditional CDFs) with MLRP on F:

   Lehmann ⇒ LR-better  (via the quantile kernel), and we already have
   LR-better ⇒ MQG ⇒ Lehmann. So **all three orders coincide**.

For the Normal family this is fully explicit: the quantile kernel is
the affine map y(x,μ) = m(μ) + (s/σ)(x − μ), whose pushforward of
N(μ,σ²) is exactly N(m(μ), s²) = G (verified to machine precision),
and which is decreasing in μ exactly on the Lehmann region m' ≤ s/σ.
Note this kernel is different from the natural additive-noise kernel
N(x + d(μ), ν²) in the notes — and it certifies LR-better on a
STRICTLY LARGER region (mildly increasing d, up to m' ≤ s/σ), where
the additive kernel is monotone the wrong way. The LR-better order is
about existence of SOME kernel; the natural one being non-monotone
does not settle the comparison.

Consequences if this holds up (please verify — the point-mass LR
convention and the measure-theoretic care in Lemma 3.1's proof with
deterministic kernels are exactly the places to poke):
- The outline's hoped-for example "LR-better strictly inside MQG"
  CANNOT exist under MLR + continuous signal distributions. Any
  strictness must come from discrete/atomic signal structures, where
  the quantile construction breaks. (Her Uniform garbling y = d(θ)x
  IS the quantile kernel for the Uniform family, reassuringly.)
- Section 4's nesting display should be revised: under MLR (and
  continuity), LR-better is not a new order strictly between
  Blackwell and MQG — it is an equivalent *garbling formulation* of
  Lehmann/MQG whose LR-monotone form is what survives Bayesian
  updating. The paper's contribution then rests cleanly on the
  dynamic theorem for general monotone POMDPs (action-dependent
  transitions, general state spaces), not on the novelty of the
  order itself. This is arguably a BETTER story: "the right dynamic
  formulation of Lehmann/MQG" + "value comparison beyond controlled
  sensing."

## Follow-ups / to verify

1. A6 ⇔ Kim's Lehmann accuracy under MLR: cite (Mizuno 2006 / Jewitt
   2007) or prove; not yet verified line-by-line.
2. The q_F/q_G range-nesting computation in §5 (two lines, decisive).
3. Symbolic verification of the found kernel in §6 if used in the
   paper.
4. New refs to add if adopted: Krishnamurthy 2021 (arXiv:1806.08733),
   Krishnamurthy & Pareek 2015 (Oper. Res. 62(2):428–434), Rieder 1991
   (Methods and Models of OR 35(6):473–490 — this also resolves the
   unverified item 8 in literature-candidates.md), Rieder & Zagst 1994,
   Mizuno 2006 (J. Appl. Prob. 43(4):1181–1185). All taken from
   Krishnamurthy 2021's reference list, so bibliographic details are
   verified against that PDF.
