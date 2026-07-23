# Open questions for the authors

Status key: **[BLOCKING]** = needed before the affected section can be finalized;
**[SOON]** = needed before the full first draft is complete; **[LATER]** = can wait.

1. **[SOON] Main theorem statement.** The outline says "Insert the main theorem and
   its proof from latex," but LRMQG.tex contains the *lemma* (LR-Better Continuation
   Values) and its proof. Is the intended main theorem the induction consequence,
   i.e., if $\mathbb{X} \succeq_{LRI} \mathbb{Y}$ (plus MLR and increasing-differences
   conditions) then $V^*_{\mathbb{X},k}(\pi) \ge V^*_{\mathbb{Y},k}(\pi)$ for all
   $k, \pi$? Claude can draft the statement and the induction proof for the authors
   to verify, or the authors can supply it.

2. **[BLOCKING for Section 3] Formal results on order relationships.** The outline
   section "Relationship between LR better, Blackwell, Lehmann and MQG" lists claims
   (2-action equivalence under MLR; LR-better ⇒ MQG = Lehmann ⇒ Blackwell?; strictness
   example) but no formal statements or proofs are in the notes. Please supply, or
   tell Claude to draft candidate statements for review.

3. **[SOON] Missing proofs for Section 2 results.** No proofs in the notes for:
   Proposition (monotonicity of beliefs), Proposition (monotone value functions),
   Lemma (increasing differences — item (ii) is a stub: "increasing differences to
   increasing policies"), Proposition (monotone policies; its proof is referenced
   in the lemma proof as `prop:monotone_policies`). Options: (a) authors supply,
   (b) cite Lovejoy 1987 / standard references where applicable, (c) Claude drafts
   for verification. OR will expect proofs (typically in an e-companion).

4. **[SOON] Two-state technology adoption example — primitives.** The decision-tree
   figure hardcodes posteriors/predictives (e.g., .522/.276/.202). Please provide the
   signal likelihood matrices for experiments F and G (and the garbling P(y|x,θ) if
   used) so the text can present the example and the numbers can be checked.

5. **[SOON] Table of three POMDP examples.** Two cells contain "?" (transitions under
   adopt/reject and produce), and CU margin notes ("There are more states", "we can
   use something like our notation here") need resolution.

6. **[LATER] informs4 template.** The session's network policy blocks most external
   downloads; Claude could not fetch informs4.cls. Draft proceeds in article style
   with author-year natbib (INFORMS-compatible); please upload the INFORMS LaTeX
   template zip when convenient, or we convert at submission time.

7. **[LATER] Front matter.** Confirm author order, affiliations, emails, title,
   keywords, and any funding/acknowledgments.

8. **[LATER] Extensions section.** "Risk aversion" is listed with no material —
   keep as future work in the conclusion, or will material be provided?

9. **[LATER] Uniform-likelihood example.** The notes end with an unresolved remark
   about non-deterministic garblings (trapezoidal marginal, MLR unclear). Include the
   deterministic version only, or investigate the general case?
