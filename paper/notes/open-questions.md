# Open questions for the authors

Updated 2026-07-23 after the first full draft (v1). Resolved items from
the previous version are logged at the bottom. Every open item below is
also flagged in the draft text with a teal \Claude{...} comment at the
exact spot where it matters.

## Open — mathematical content

1. **Main theorem (Section 3, Theorem 3.1).** Statement and induction
   proof drafted by Claude per your instruction. Please verify:
   (a) the hypothesis set — in particular, the stochastic
   increasing-differences condition is imposed only on the X process
   (the induction needs LR-increasing differences of V_{X,k-1} only);
   confirm the asymmetry is intended; (b) the proof itself.

2. **A step in the lemma proof (Section 3, proof of Lemma 3.1).** Your
   notes end the chain with E[u(Π_X(x), a'(x)) | x]; the step from
   E[u(Π_XY(x,ỹ), a'(x)) | x] to u(Π_X(x), a'(x)) uses the tower
   property of posteriors, which is immediate when u(·,a) is linear in
   the belief argument but needs justification for general u with
   LR-increasing differences (e.g., u = V_{X,k-1} includes nonlinear
   continuation terms). Flagged in the draft — please advise how you
   want this argued (this looks like a genuine gap worth resolving
   before anything else builds on the lemma).

3. **Lemma 2.1(ii) (monotone selections).** The notes had only the
   placeholder "increasing differences to increasing policies". Claude
   drafted a statement using the greatest maximizer. Verify.

4. **Section 4 strictness claims.** (a) Verify that the Normal example
   with strictly decreasing d is not Blackwell-comparable (needs an
   argument that *no* state-independent kernel generates the same G);
   (b) construct an example separating LR-better from MQG (reversely
   FOSD- but not LR-monotone garbling); your uniform-example margin
   note suggests candidates. *Update (2026-07-26): (b) appears
   IMPOSSIBLE under MLR + continuous signal distributions — Kim's
   quantile-kernel construction is deterministic with atoms decreasing
   in the state, which makes it reversely LR-monotone, giving
   Lehmann ⇒ LR-better and hence LR-better = MQG = Lehmann there. Any
   strict separation must come from discrete/atomic signal structures.
   See krishnamurthy-comparison.md §9 — needs your verification, and
   if it holds it reshapes Section 4's nesting display.*
   *Update 2 (2026-07-26, after Canan's challenge): CONFIRMED that the
   separation exists in discrete signal spaces — explicit 3-state
   example (F MLR, binary X-signals, ternary Y-signals) that is MQG
   and discrete-Lehmann but NOT LR-better and NOT Blackwell;
   numerically certified, analytic proof pending. All discrete
   counterexamples found have G non-MLR; open conjecture that MLR on
   both processes restores the equivalence. See
   krishnamurthy-comparison.md §9a and paper/analysis/.*

5. **Two-action equivalence claim.** The outline's claim "2-action
   models: BW = Lehmann = LR-better = MQG under MLR" is not (as far as
   Claude can tell) in Kim (2023); Jewitt (2007) concerns two *states*
   (dichotomies), not two actions. Clarify the intended statement and
   provenance; currently flagged in Section 4 with the question.

6. **Is MQG sufficient in dynamic problems?** Section 4 currently poses
   as an open question whether the gap between LR-better and MQG is
   essential in monotone POMDPs. If you have a counterexample (MQG
   holds but value comparison fails at some horizon), it would sharpen
   the contribution; please advise. *Update (2026-07-26): partially
   answered — within finite-state controlled sensing, Krishnamurthy
   (2021, Thm 3.4(1)) shows Lehmann precision (= MQG under MLR)
   suffices; the question remains open for action-dependent
   transitions and general state spaces. See item 14.*

14. **Positioning vs. Krishnamurthy (2021).** Full analysis in
    notes/krishnamurthy-comparison.md. Headlines: (a) in finite signal
    spaces LR-better (even MQG) + MLR implies his (A7), so the hoped-for
    "LR-better but not A7" example cannot exist there — proof sketch
    and 2,000-instance numerical check included; (b) the genuine
    separations are action-dependent transitions, general state
    spaces, and the continuum absolute-continuity version of A7, which
    the Uniform-scaling family violates; (c) his hierarchical-sensing
    example is LR-better comparable (explicit kernel found by LP) —
    usable as our Blackwell-strictness example; (d) on the overlap
    (finite controlled sensing) his theorem is stronger — no
    supermodularity needed — raising the question of whether our
    Theorem 3.1 can drop increasing differences. Decisions needed:
    adopt recommended positioning? verify the two-line q_F/q_G
    computation? pursue dropping supermodularity?

7. **Definition 3.1 action dependence.** LR-better is stated with the
   action suppressed (as in your notes); Claude assumes conditions hold
   per action a with kernels P_a. Confirm.

## Open — exposition and format

8. **Proofs of Section 2 propositions** are omitted with guiding text
   per your instruction, but OR will expect complete proofs in an
   e-companion at submission. Decide timing.

9. **Jim Smith's affiliation/email** (title page placeholder). Also
   confirm author order and Canan's affiliation line.

10. **Risk-aversion extension**: currently one framing sentence in the
    conclusion; expand or leave as future work?

11. **Table 1 loose ends** (as-is per your instruction): two "?" cells
    (transitions under adopt/reject and produce) and your margin notes
    ("There are more states", "we can use something like our notation
    here").

12. **Spreadsheet Blackwell check.** The xlsx contains a cell "There is
    a feasible solution to Blackwell." next to a candidate kernel whose
    product F·Pᵀ does **not** reproduce G (nonzero differences shown in
    the adjacent block). Claude did not use this in the draft — the
    text argues no-dominance from the value functions crossing, which
    is airtight. Please clarify what the feasibility cell refers to.

13. **Literature selections.** Choose from notes/literature-candidates.md
    which structural-results papers to add to intro paragraph 3, and
    whether to cite Krishnamurthy (2018, Lehmann precision, arXiv
    1806.08733) — recommended, as it is the closest POMDP antecedent.

## Resolved (v0 → v1)

- Main theorem identified as the value-comparison induction (confirmed
  by Canan; draft now in Section 3). — was item 1
- Section on order relationships drafted from Kim (2023). — was item 2
- Monotonicity propositions inserted without proof, with guiding text
  and literature pointers. — was item 3
- Two-state example primitives recovered from the uploaded xlsx
  (Binomial(2, θ) trials; d(0.1)=0.4, d(0.7)=0.7; A=1, K=0.3, prior
  0.4). — was item 4
- Three-model table inserted as-is. — was item 5
- INFORMS OPRE template received and adopted (informs4.cls,
  informs2014.bst). — was item 6
- Duplicate label prop:monotone_beliefs fixed; prop:monotone_policies
  now defined; lemma stub replaced by drafted statement (see item 3
  above).
