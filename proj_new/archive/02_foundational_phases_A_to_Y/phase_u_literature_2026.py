"""
Phase U: Live Literature Re-Check (Backlog items 6, 8, 9, 15, 17, 18, 28)
[L1/L2 -- lit-only, new, 2026-07-28]
=========================================================================

MOTIVATION
----------
PHASE_R_HYPOTHESIS_BACKLOG.md's Section G says its own items 17/18 ("re-run
Phase I's literature search monthly... this field is more active than Phase
I's 2026-07-27 snapshot suggested") should be treated as RECURRING, not
one-time. Phase I's search happened same-day as project closure. This phase
re-runs it, honestly, using live web search rather than training-data
recall (training-data recall would silently miss anything published this
year, which is exactly the failure mode Phase I warned about).

WHAT THIS PHASE IS AND IS NOT
------------------------------
This is a [lit] phase, not a [cheap] or [real] one: it identifies and reads
papers, it does not re-derive their mathematics in this project's own code.
Per this project's own Rule 2 (don't reverse-engineer / fake a result),
nothing here is promoted to "verified" or "computed" status. Every item
below stays at "literature identified" until someone actually builds the
construction in code against Phase A1/A2's own conventions, the way Phases
Q/S/T did for the SU(2)_R and triality questions. That follow-up work is
listed explicitly as still open at the end.

FINDING 1 -- Item 6 (Cl(8) S3 family symmetry) has a DIRECT Cl(10) sequel
--------------------------------------------------------------------------
The backlog's own citation (Gourlay & Gresnigt, Eur. Phys. J. C 84 (2024)
1129) is Cl(8), not Cl(10) -- a real difference the backlog already flagged
as "not a rerun". Live search finds the group has since published the
Cl(10) extension directly:

    N. Gresnigt, "Electroweak Structure and Three Fermion Generations in
    Clifford Algebra with S3 Family Symmetry," arXiv:2601.07857
    (submitted 2026-01-09, v2 2026-04-13).

This is the SAME base algebra (complex Cl(10)) as this project's own
Phase A1, but a DIFFERENT mechanism for 3 generations: fermions are
minimal left ideals of Cl(10) (a Witt-basis construction, like Phase A1),
and three generations come from an intrinsic S3 automorphism acting on
that ideal structure -- not from branching an external E8 the way this
project's Phase A2 does it. The abstract states the construction
reproduces the correct SM quantum numbers for three linearly independent
generations, with SM gauge generators required to commute with the S3
action (so gauge bosons are not tripled).

A follow-up extends this to the Higgs/Yukawa sector:

    N. Gresnigt, "Higgs Sector and Flavour Structure in an Algebraic
    Three-Generation Model with S3 Family Symmetry," arXiv:2604.24795
    (2026-04, v2 2026-06-18).

Reported result (read from the abstract/HTML, not re-derived here): two
first-generation Higgs doublets with quantum numbers (1,2,-1) and (1,2,+1),
a Type-II-like up/down Yukawa selection rule, and a generation-space Yukawa
matrix that is FIXED ALGEBRAICALLY but NON-DIAGONAL in the S3 generation
basis. Explicitly note what this is NOT: the abstract does not claim
absolute mass values or a specific numerical hierarchy -- it claims a
structural (non-diagonal, Type-II) Yukawa pattern, with tree-level FCNCs
naturally absent in the exact-S3 limit. This does not (yet, on its own)
supply Phase D's missing FN-charge derivation.

WHY THIS MATTERS FOR THIS PROJECT SPECIFICALLY: because it uses the same
Cl(10) as Phase A1, this is the single most directly comparable external
construction found anywhere in this project's literature sweeps (more
comparable than the E8-branching-based mechanism this project itself
uses). It is a genuinely different candidate answer to the "where do 3
generations come from, mechanically" question this project's own Phase
A2/B/C could not answer without external input. It is NOT verified here.

FINDING 2 -- Items 8/9 (exceptional Jordan algebra J3(O)) have grown into
a small active sub-field since the backlog's single citation
--------------------------------------------------------------------------
The backlog cites one paper (arXiv:2508.10131, T.P. Singh, rigid
parameter-free mass ratios from J3(O_C), fixed geometric spread
delta^2 = 3/8). Live search finds two direct sequels:

    B. Gupta Teli, T.P. Singh, "Fermion Mass Hierarchies and the
    Exceptional Jordan Algebra," arXiv:2605.24866 (2026-05-24).
    -- Promotes the rigid delta^2=3/8 point to a fitted "spectral moduli
    space"; reports a global log-fit to six charged-fermion mass ratios
    at the Z mass that improves on the rigid point (mainly via the
    top/charm ratio) with best-fit hierarchy exponent p ~ 1. Explicitly
    self-described as "not a parameter-free replacement" for the rigid
    construction -- i.e. this sequel re-introduces fitted parameters the
    original paper didn't have.

    B. Gupta Teli et al., "Fermion Mixing Matrices and the Exceptional
    Jordan Algebra," arXiv:2607.00412 (~2026-06).
    -- Extends the same framework to CKM/PMNS angles via a "Fritzsch-type
    two-state texture," explicitly flagged by its own authors as "an
    effective bridge ansatz rather than a theorem of the Jordan spectrum
    alone."

Read plainly: this sub-field is itself moving from "rigid, parameter-free"
(closer in spirit to what would actually help Phase D) toward "fitted,
phenomenological" (closer to what Phase D already does, with the same
kind of caveats Phase C's honest accounting already logs for this
project's own model). It has NOT, as of this search, produced a
free-of-new-fit-parameters derivation of the SM Yukawa hierarchy. This is
consistent with -- not a resolution of -- this project's own Phase C/D
conclusions.

FINDING 3 -- Item 28 (Furey & Hughes, trio of trialities) -- read, not
reproduced
--------------------------------------------------------------------------
    N. Furey, M.J. Hughes, "Three Generations and a Trio of Trialities,"
    Phys. Lett. B 865 (2025) 139473 (also arXiv:2409.17948).

Mechanism (division-algebra, not Cl(10)xE8): identifies the SM's
su(3)+su(2)+u(1) inside tri(C)+tri(H)+tri(O) (triality algebras of the
division algebras themselves, not an E8 branching). Two generations come
from a triality pair (Psi_+, Psi_-); a third comes from a separate
"Cartan factorization" of a triality-scalar object V -- explicitly a
DIFFERENT mechanism from both this project's E8-branching route and from
Finding 1's Cl(10)-S3 route. The retrieved abstract/text makes no mention
of the Distler-Garibaldi non-chirality theorem (Priority 0's subject) one
way or the other; this project's own Phase R Priority-0 check does NOT
transfer to this construction, since it is not an E8-adjoint-248
placement. Whether this construction is chiral is a genuinely separate
question this search did not resolve either way -- logged as open, not
assumed either way, per this project's own rules.

FINDING 4 -- Items 17/18 general sweep
--------------------------------------------------------------------------
No new Cl(10)-specific sin^2(theta_W) or Cabibbo-angle derivation was
found beyond what Phase K/Phase I already checked. The overall picture
Phase I already reported -- multiple active, independent algebraic
programs, none yet delivering a parameter-free SM-parameter derivation --
still holds; if anything more strongly, given Findings 1-2 above.

DISPOSITION -- what changes in this project, and what does not
--------------------------------------------------------------------------
Does NOT change: Phase C's 0/19 count, Phase D's fitted FN charges, or any
existing L1 result. Nothing here is code-verified against this project's
own conventions.

DOES change: backlog items 6, 8, 9, 17, 18, 28 move from "unrun" to
"[lit] DONE - Phase U" (see PHASE_R_HYPOTHESIS_BACKLOG.md). The single
highest-value next step this search identifies is now sharper than Phase
R's item-43 ranking: build arXiv:2601.07857's S3-on-Witt-ideals
construction directly against Phase A1's own Cl(10) code (same base
algebra, same Witt-pair conventions available already) and check by direct
computation whether it reproduces Phase A1's charge assignment -- this is
now a same-algebra comparison, not a "read and hope it transfers" one, and
is the most concrete unfinished task this project has identified for
itself.
"""

print('=' * 72)
print('Phase U: Live Literature Re-Check (items 6, 8, 9, 15, 17, 18, 28)')
print('=' * 72)

findings = [
    ("Item 6",
     "arXiv:2601.07857 (Gresnigt, 2026-01, v2 2026-04) -- 3 generations "
     "DIRECTLY from Cl(10) via S3 on Witt-basis minimal left ideals. "
     "Same base algebra as this project's Phase A1; different generation "
     "mechanism than this project's own E8-branching route. Not code-"
     "verified here."),
    ("Item 6 (Higgs follow-up)",
     "arXiv:2604.24795 (Gresnigt, 2026-04, v2 2026-06) -- Type-II-like, "
     "algebraically-fixed but non-diagonal Yukawa structure in the S3 "
     "basis. Structural result only; no absolute mass values claimed."),
    ("Items 8/9",
     "arXiv:2605.24866 (Gupta Teli & Singh, 2026-05) and arXiv:2607.00412 "
     "(~2026-06) extend the backlog's cited J3(O_C) paper from a rigid "
     "parameter-free point to a fitted spectral-moduli-space model. "
     "Sub-field is moving toward fitted, not away from it."),
    ("Item 28",
     "Phys. Lett. B 865 (2025) 139473 / arXiv:2409.17948 (Furey & Hughes) "
     "-- read directly. Division-algebra triality mechanism, distinct "
     "from both this project's route and Item 6's. Chirality status "
     "vs. Distler-Garibaldi: not addressed in the retrieved text, logged "
     "open, not assumed safe."),
    ("Items 17/18",
     "General re-sweep: no new Cl(10)-specific sin2(theta_W) or Cabibbo "
     "derivation found beyond Phase K/I. Field remains active; no "
     "parameter-free SM derivation found anywhere in this sweep."),
]

for tag, text in findings:
    print(f"\n[{tag}]\n  {text}")

print("\n" + "-" * 72)
print("Net effect on Phase C's free-parameter count: ZERO (no code-level")
print("verification performed in this phase -- literature status only).")
print("Backlog disposition: items 6, 8, 9, 17, 18, 28 -> '[lit] DONE - Phase U'")
print("Sharpened next step: build arXiv:2601.07857's S3-on-Cl(10)-ideals")
print("construction against Phase A1's own code -- same algebra, so this")
print("is now a direct comparison rather than a cross-framework guess.")
