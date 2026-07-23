# Internal review log

## 2026-07-23 — v1: full first draft in the INFORMS OPRE template

What was drafted (25 pp., compiles clean):
- Converted to informs4.cls / informs2014.bst from the uploaded OPRE
  template; author-year natbib; INFORMS theorem/proof machinery.
- §1 Introduction: full draft per the outline's paragraph plan.
- §2 Monotone POMDPs: setup, LR/MLR definitions, Prop 2.1 (beliefs),
  DP, Prop 2.2 (values), Remark 2.1 (Lovejoy comparison, from the
  CU/JS margin dialogue), Def 2.2 (increasing differences), Lemma 2.1
  (part (ii) statement drafted — was a stub), Prop 2.3 (policies).
  Propositions without proof + guiding text, per instruction.
- §3 LR-better definition, Lemma 3.1 with the authors' proof
  (transcribed; one step tightened and flagged — see open-questions
  item 2), Theorem 3.1 (main result) statement + induction proof
  drafted by Claude, flagged for verification.
- §4 Order relationships from Kim (2023): Blackwell/MQG/Lehmann
  definitions restated in our notation, nesting proposition with the
  two easy implications proved, Kim's theorems cited, outline's
  unproven claims flagged rather than asserted.
- §5 Table 1 as-is; Normal/Poisson/Uniform garbling constructions;
  two-state example with primitives recovered from the xlsx; decision
  tree figure (INFORMS \FIGURE format).
- §6 Conclusion with risk-aversion placeholder.
- refs.bib: 6 entries added (marked, verification status noted);
  notes/literature-candidates.md written — includes the finding that
  Krishnamurthy (arXiv:1806.08733) DOES use Lehmann precision.

Checks performed:
- latexmk exit 0; zero LaTeX errors; zero undefined references or
  citations; bibtex zero warnings; all 20 bib entries cited.
- Visual check of rendered pages: title page, lemma proof, landscape
  table, figure, bibliography.
- Notation: consistent with LRMQG.tex macros (\iX, \ev, \dif, etc.);
  duplicate label from the notes fixed
  (prop:monotone_beliefs/values/policies now distinct);
  prop:monotone_policies now exists (was referenced but undefined).
- Numbers in the two-state example cross-checked against the xlsx
  (F: Binomial(2, theta); G: Binomial(2, theta*d(theta)); tree values
  0.123/0.109 at prior 0.4 match the figure and spreadsheet).

Known deviations / to restore before submission:
- Equation-width check relaxed from 240pt (published two-column) to
  470pt in main.tex — re-tighten and break ~9 flagged equations at
  submission time.
- Two overfull hboxes inside Table 1 (inserted as-is per instruction;
  one is the biopsy update formula already slated for notation
  rewrite).
- \Claude{} teal comments throughout mark items for the authors; see
  notes/open-questions.md for the consolidated list (items 1-13).
- documentclass[opre] without anonymous-review option; switch to
  [opre,dblanonrev] for submission.

Each drafting pass gets an entry: what changed, what was checked
(compile, refs/citations resolved, notation consistency, hypothesis/claim
match), and open items handed back to the authors.

## 2026-07-23 — v0 scaffold
- Created paper skeleton (main.tex + section stubs), refs.bib from the
  outline's reference list, staged source material.
- Checks: compiles clean with pdflatex+bibtex; all 14 bib entries parse.
- Noted issues found in source notes (see open-questions.md):
  duplicate label `prop:monotone_beliefs` used for both monotonicity
  propositions in LRMQG.tex; `prop:monotone_policies` referenced in the
  lemma proof but never defined; increasing-differences lemma item (ii)
  is a stub.
