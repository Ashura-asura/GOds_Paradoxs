"""
Phase P: Asymptotic Safety Unitarity -- Checked Against the Real,
Current Literature (2024-2026), Not Asserted [built on cited sources]
======================================================================
tests.zip's asymptotic_safety.py asserted a single fixed point
(g*=0.707, lambda*=0.193) and a flat "unitarity residue = -1.0 ->
FAIL" conclusion, both typed in rather than computed or cited. Checked
against the actual current literature below.
"""

print('=' * 72)
print('Phase P: What the real asymptotic-safety literature actually says')
print('=' * 72)

print("""
ON THE FIXED POINT: real papers (Reuter 1998; Litim, PRL 92, 201301
(2004); Codello-Percacci-Rahmede, Ann. Phys. 324, 414 (2009); and
dozens since) find a non-Gaussian ("Reuter") fixed point CONSISTENTLY
across increasingly elaborate truncations of the functional
renormalization group flow -- but the actual numerical values of g*
and lambda* DEPEND on the truncation and regulator scheme used; there
is no single universal number the way tests.zip's hardcoded
g*=0.707 implied. Existence of the fixed point is now considered
well-established; precise quantitative convergence across schemes is
explicitly listed as NOT yet achieved (arXiv:2003.00044, Sec 4.4,
"Key open questions").

ON UNITARITY: this WAS a genuinely open, actively debated question --
tests.zip's framing wasn't inventing the topic out of nothing. But the
specific claim ("ghost state, residue=-1.0, FAIL") is not what the
current literature finds. A 2024 Physical Review D paper
(PRD 110, 026001) computing momentum-dependent field redefinitions of
the graviton propagator found the asymptotically safe fixed point does
NOT feature the extra ghostly degrees of freedom naively expected,
"a good chance of being related to a unitary theory." A 2026 preprint
("The pole truth: an analytical graviton propagator from Asymptotic
Safety") goes further: analytic computation of the non-perturbative
graviton propagator finds no additional poles beyond the physical
massless one, stated directly as "significant evidence that Asymptotic
Safety is unitary and causal."
""")

print('=' * 72)
print('HONEST CONCLUSION')
print('=' * 72)
print("""
tests.zip's asymptotic_safety.py claimed a settled unitarity FAILURE.
The real, current (2024-2026) literature trend is the opposite
direction -- toward evidence FOR unitarity, though not yet fully
settled, and explicitly still an open research question rather than
either a proven pass or proven fail. The honest status, as of this
project's knowledge cutoff: asymptotic safety's fixed point is well-
established; its unitarity is actively being resolved IN FAVOR of the
theory by recent work, not against it. This is real, checkable,
citable physics -- not something computed here, but reported
accurately rather than asserted. Like Phase O, this does not connect
to or modify the Cl(10)xE8 / solution.md conclusions; it corrects a
specific false claim from tests.zip on its own terms.
""")
