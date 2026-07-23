# Literature candidates for the introduction

Prepared by Claude (2026-07-23) in response to the two research notes in
Outline.docx: (1) "Provide other papers (especially by Vikram
Krishnamurthy)... Give me a list with summaries and I can decide which
papers to include," and (2) "Does Krishnamurthy have papers that use
Lehmann's order instead? Provide me with citations and summaries."

Verification status is marked on each item. Items marked [verified] were
checked against arXiv/publisher pages during drafting; items marked
[verify] are from Claude's knowledge or from the reference lists of the
papers you uploaded and should be double-checked before citing.

## Direct answer to Note 2 (Krishnamurthy and Lehmann's order): YES

1. **Krishnamurthy (2018), "New Sufficient Conditions for Lower Bounding
   the Optimal Policy of a POMDP using Lehmann Precision"**
   (arXiv:1806.08733). [verified on arXiv]
   Uses *Lehmann precision* to compare observation distributions in
   controlled-sensing POMDPs and to lower-bound the optimal policy.
   Exploits both the monotonicity and the convexity of the value
   function, whereas classical Blackwell dominance exploits only
   convexity — precisely the contrast your introduction draws. Check
   whether a journal version exists (possibly in IEEE TAC / Automatica);
   cite the journal version if so. **Strong candidate — this is the
   closest antecedent to your paper in the POMDP literature and should
   probably be cited and differentiated explicitly** (his comparison
   appears to be for controlled sensing with finite states and a fixed
   policy-bounding purpose; your LR-better order is a garbling-based
   order with value comparisons for general monotone POMDPs).

2. **Krishnamurthy (2017), "POMDP Structural Results for Controlled
   Sensing"** (arXiv:1701.00179). [verified on arXiv]
   Short review of structural results: monotone value functions,
   Blackwell dominance, quickest detection. Useful as a compact survey
   citation alongside the 2016 book.

## Other structural-results candidates (Note 1)

3. **Krishnamurthy (2016), *Partially Observed Markov Decision
   Processes: From Filtering to Controlled Sensing*, Cambridge.**
   [already in refs.bib] Chapters on monotonicity of the value function
   for POMDPs and on Blackwell-dominance-based comparisons of
   observation kernels; the natural blanket citation for structural
   POMDP results.

4. **Krishnamurthy & Djonin (2007), "Structured threshold policies for
   dynamic sensor scheduling — a POMDP approach," IEEE Transactions on
   Signal Processing 55(10).** [verify volume/pages]
   Supermodularity + MLR conditions giving threshold optimal policies in
   sensor scheduling POMDPs.

5. **Krishnamurthy & Wahlberg (2009), "Partially observed Markov
   decision process multiarmed bandits — structural results,"
   Mathematics of Operations Research 34(2):287–302.** [verify]
   MLR-order structural results for POMDP bandits; opportunistic
   sensing.

6. **Albright (1979), "Structural results for partially observable
   Markov decision processes," Operations Research 27(5):1041–1053.**
   [verified against Lovejoy 1987's reference list, which gives
   27:1041–1053] Early two-state monotonicity results; Lovejoy notes his
   results generalize Albright's.

7. **White (1980), "Monotone control laws for noisy, countable-state
   Markov chains," European Journal of Operational Research
   5:124–132.** [verified against Lovejoy 1987's reference list]
   Monotone policies under FOSD-type orderings; illustrates the
   difficulty (FOSD not preserved under conditioning) that motivates the
   MLR order.

8. **Rieder (1991), "Structural results for partially observed control
   models."** [NOT verified — Claude is unsure of this reference;
   please check before citing or drop]

9. **Smallwood & Sondik (1973).** [already in refs.bib] Convexity of the
   POMDP value function — needed for the Blackwell-garbling argument
   you describe in the introduction.

10. **Li & Zhou (2020), "Information order in monotone decision problems
    under uncertainty," Journal of Economic Theory.** [surfaced in
    search results; verify authors/volume] Robustness of Lehmann's
    ordering under ambiguity-averse DMs; cited by Kim (2023). Optional —
    static setting, but rounds out the Lehmann literature paragraph.

## Suggested placement

- Paragraph 3 of the introduction (structural properties of POMDPs):
  items 3–7 (choose 2–4).
- Paragraph 4 (information orders): item 1 belongs here (or in the
  Section 4 discussion) as the closest POMDP antecedent using Lehmann's
  order; item 10 optional.

## Already-drafted intro citations added by Claude (verify)

Lehmann (1988) [verified], Persico (2000), Quah & Strulovici (2009),
Jewitt (2007) [existence verified; unpublished], Topkis (1978)
[verified via Lovejoy's references], Whitt (1979) [verified via Ulu &
Smith's references].
