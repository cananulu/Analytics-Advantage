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
