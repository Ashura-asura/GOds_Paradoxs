"""
Generate GODS_PARADOX_FINAL.pdf -- detailed final report (v2).
Rebuilt with reportlab (no Windows font dependency). Includes Phase E, Phase F, Phase G, and Phase H.
"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUT = os.path.join(os.path.dirname(__file__) or '.', 'GODS_PARADOX_FINAL.pdf')

styles = getSampleStyleSheet()
NAVY = colors.HexColor('#12345C')
STEEL = colors.HexColor('#2C5C8C')
RED = colors.HexColor('#B0402C')
GREEN = colors.HexColor('#2E7D32')
GREY = colors.HexColor('#555555')
LIGHTBLUE = colors.HexColor('#EAF1FA')
LIGHTRED = colors.HexColor('#FBEAE7')
LIGHTGREEN = colors.HexColor('#E9F5E9')

styles.add(ParagraphStyle('TitleBig', fontName='Helvetica-Bold', fontSize=26,
                           textColor=NAVY, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle('Subtitle', fontName='Helvetica-Oblique', fontSize=13,
                           textColor=GREY, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle('Meta', fontName='Helvetica', fontSize=10,
                           textColor=GREY, alignment=TA_CENTER, spaceAfter=2))
styles.add(ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=17,
                           textColor=NAVY, spaceBefore=18, spaceAfter=8))
styles.add(ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=13,
                           textColor=STEEL, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle('Body', fontName='Helvetica', fontSize=10,
                           leading=14, spaceAfter=6, alignment=TA_LEFT))
styles.add(ParagraphStyle('BodyBold', parent=styles['Body'], fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Mono', fontName='Courier', fontSize=9,
                           leading=12.5, textColor=colors.HexColor('#1A1A1A'),
                           backColor=colors.HexColor('#F4F4F4'), spaceAfter=6,
                           leftIndent=8, borderPadding=6))
styles.add(ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=8.5,
                           textColor=GREY, spaceAfter=10))

story = []

def h1(t): story.append(Paragraph(t, styles['H1']))
def h2(t): story.append(Paragraph(t, styles['H2']))
def body(t): story.append(Paragraph(t, styles['Body']))
def mono(lines): story.append(Paragraph('<br/>'.join(lines), styles['Mono']))
def rule(): story.append(HRFlowable(width='100%', color=colors.HexColor('#CCCCCC'), spaceAfter=8, spaceBefore=2))
def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(i, styles['Body']), leftIndent=6) for i in items],
        bulletType='bullet', start='-', leftIndent=14))

def status_table(rows, header, colWidths=None, boxcolor=LIGHTBLUE):
    data = [header] + rows
    t = Table(data, colWidths=colWidths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.7),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, boxcolor]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

# =====================================================================
# TITLE PAGE
# =====================================================================
story.append(Spacer(1, 1.6*inch))
story.append(Paragraph("GOD'S PARADOX", styles['TitleBig']))
story.append(Paragraph("Final Assessment: Cl(10) &times; E8 &rarr; Standard Model", styles['Subtitle']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Author: Bishal Bhandari", styles['Meta']))
story.append(Paragraph("Project closed: 2026-07-27  |  Phase E, F, G, and H addenda: same day", styles['Meta']))
story.append(Paragraph("License: Open Knowledge -- may be freely shared and built upon", styles['Meta']))
story.append(Spacer(1, 0.5*inch))
story.append(HRFlowable(width='60%', color=NAVY, thickness=1.2, hAlign='CENTER'))
story.append(Spacer(1, 0.25*inch))
story.append(Paragraph(
    "This document is an honest final accounting, not a triumphant announcement. "
    "It states plainly what was proved, what was claimed but not proved, what two new "
    "post-closure tests (Phase E, Phase F, Phase G, and Phase H) found, and what avenues remain unexplored.",
    ParagraphStyle('boxed', parent=styles['Body'], alignment=TA_CENTER, fontSize=10.5,
                   textColor=GREY, leftIndent=40, rightIndent=40)))
story.append(PageBreak())

# =====================================================================
# EXECUTIVE SUMMARY
# =====================================================================
h1("Executive Summary")
body("An attempt to derive the Standard Model of particle physics from the algebraic "
     "structure Cl(10) (the Clifford algebra of 10-dimensional space) and E8 (the largest "
     "exceptional Lie group). The project ran 23 internal phases plus post-closure "
     "Phases E, F, G, and H, and an adversarial audit against eight self-imposed ground rules.")

status_table(
    header=["Claim", "Verdict"],
    rows=[
        ["Cl(10) &rarr; SU(3)&times;SU(2)&times;U(1) with charge quantization", "TRUE (L1) -- known since the 1980s"],
        ["E8 &rarr; 3 generations + right-handed neutrino", "TRUE (L1) -- standard E8 representation theory"],
        ["19/19 Standard Model parameters derived", "FALSE -- 0/19 derived"],
        ["Rule 6 (zero free parameters) satisfied", "FALSE -- ~13 free parameters required"],
        ["FN charges (3,2,0) derivable from anomaly cancellation (Phase E test)", "FALSE -- charges are anomalous; anomaly-free alternative can't fit the data either"],
        ["Messenger matter restores anomaly-freedom without new free parameters (Phase F test)", "FALSE -- restores consistency, but adds a messenger mass scale; free-parameter count is not reduced"],
        ["Messenger fix discriminates between candidate FN charges (Phase G test)", "FALSE -- rescues 100% of hierarchy-compatible triples tested; zero selection power"],
        ["Full Green-Schwarz mixed-anomaly universality adds a new constraint (Phase H test)", "FALSE -- automatically satisfied for any complete-16-plet matter; adds nothing beyond Phase E/F/G"],
    ],
    colWidths=[3.6*inch, 3.0*inch],
)

body("<b>Bottom line:</b> the algebraic core correctly explains structural features of the "
     "Standard Model that the Standard Model itself simply assumes -- the gauge group, "
     "charge quantization, and the existence of exactly three generations. It does not "
     "predict a single one of the Standard Model's 19 numerical parameters (masses, mixing "
     "angles, the Higgs mass, coupling constants). This limitation is shared by every known "
     "theory of particle physics; it is not unique to this project.")

# =====================================================================
# PART 1: WHAT WAS PROVED
# =====================================================================
h1("Part I -- What Was Proved (L1: mathematical theorem, no free parameters)")

status_table(
    header=["Result", "Source"],
    rows=[
        ["Gauge group SU(3)&times;SU(2)&times;U(1) embeds in Cl(10) via 5 Witt pairs; all charges are multiples of 1/3", "Phase A1"],
        ["E8's 248 branches to (16,3): three copies of an SO(10) spinor, each a full SM family + &nu;<sub>R</sub>", "Phase A2"],
        ["CKM = I, PMNS = I in the minimal E8 248 (no 126 Higgs present)", "Phase B"],
        ["No mass scale, no flavor hierarchy from algebra alone (algebra is dimensionless)", "Phase B"],
        ["0/19 Standard Model parameters derived; ~13 free parameters needed for any extension", "Phase C"],
    ],
    colWidths=[5.3*inch, 1.3*inch],
    boxcolor=LIGHTGREEN,
)
body("These are genuine mathematical results. They are also, by the project's own honest "
     "accounting, <b>not new physics</b> -- the Cl(10) fermion construction has been known "
     "since Benn-Tucker, Crawford, and Furey in the 1980s, and the E8 branching follows from "
     "textbook representation theory.")

# =====================================================================
# PART 2: WHAT WAS CLAIMED BUT NOT PROVED
# =====================================================================
h1("Part II -- What Was Claimed but Could NOT Be Proved")
status_table(
    header=["Claim (as originally stated)", "Reality"],
    rows=[
        ["\"19/19 SM parameters derived\"", "0/19 derived. ~13 free parameters fitted."],
        ["\"CKM angles predicted\"", "CKM &ne; I is possible (L2), but exact angles are fitted with free parameters; V<sub>us</sub> off by 25%."],
        ["\"&epsilon; = 0.225 from E8\"", "&epsilon; is an input from observation. SU(3)<sub>f</sub> alone gives a flat direction -- no invariant fixes it."],
        ["\"m<sub>H</sub> = 125 GeV from spectral action\"", "142 GeV computed without thresholds. 125 GeV needs uncomputed threshold corrections."],
        ["\"Rule 6 (zero free parameters) satisfied\"", "Violated: ~13 free parameters."],
        ["\"Zero free parameters, remarkably close to succeeding\" (original closing thought)", "Retracted in the Closing Statement -- conflated structural derivation with numerical derivation."],
    ],
    colWidths=[3.0*inch, 3.6*inch],
    boxcolor=LIGHTRED,
)

# =====================================================================
# PART 3: GROUND RULES + FREE PARAMETER ACCOUNTING
# =====================================================================
h1("Part III -- Ground Rules Compliance and Free-Parameter Accounting")
status_table(
    header=["Rule", "Status"],
    rows=[
        ["1. No numerology", "VIOLATED (pre-audit): FN charges, VEVs, Clebsch coefficients chosen to fit data"],
        ["2. No reverse-engineering", "VIOLATED (pre-audit): &epsilon; solved from its observed value"],
        ["3. Level labeling (L1/L2/L3)", "VIOLATED (pre-audit): L2/L3 claims labeled as L1; corrected in final audit"],
        ["4. Adversarial audit always on", "PARTIAL: violations were found but had been ignored in practice until audit"],
        ["5. Document failures", "HONORED"],
        ["6. Zero free parameters", "VIOLATED: ~13 free parameters remain (see table below)"],
        ["7. One step at a time", "HONORED"],
        ["8. Structural failure = result", "HONORED after audit; Phase E, Phase F, Phase G, and Phase H each add a new structural-failure result"],
    ],
    colWidths=[2.6*inch, 4.0*inch],
)

h2("Free Parameters Required (Phase D / Phase C accounting)")
status_table(
    header=["Parameter", "Role", "Count"],
    rows=[
        ["FN charges q=(3,2,0)", "Flavor hierarchy", "2 free (shown anomalous in Phase E)"],
        ["&epsilon; = 0.225", "FN breaking ratio", "1 free (proved flat direction, Phase B)"],
        ["&phi;<sub>126</sub> = (A,B,1)", "CKM fitting", "2 free (grid-scanned)"],
        ["SO(10) Clebsch (r<sub>u</sub>, r<sub>d</sub>)", "Up/down splitting", "2 free (grid-scanned)"],
        ["M<sub>R</sub> (M1, M2, off)", "Seesaw scale/structure", "3 free (grid-scanned)"],
        ["y<sub>&nu;</sub>/y<sub>t</sub> ratio", "Higgs mass correction", "1 free (scanned)"],
        ["v = 246 GeV", "Electroweak scale", "1 free (external input)"],
        ["g1, g2, g3 at M<sub>Z</sub>", "Gauge couplings", "3 free (from QFT, not algebra)"],
    ],
    colWidths=[2.1*inch, 2.3*inch, 2.2*inch],
    boxcolor=LIGHTRED,
)
body("<b>Total: ~13 free parameters produce ~6 approximate fits.</b> None of the structural "
     "limits proved in Phase B (CKM=I, PMNS=I, &epsilon; flat direction, no mass scale) are "
     "resolved by this parametric extension -- they are bypassed by inputting free values.")

story.append(PageBreak())

# =====================================================================
# PART 4: PHASE E
# =====================================================================
h1("Part IV -- Phase E (New, 2026-07-27): Can Anomaly Cancellation Derive the FN Charges?")
body("This is the one substantive new result added after the project's original closure. "
     "The question: instead of fitting q=(3,2,0) to match observed masses (Phase D), could "
     "<i>gauging</i> the horizontal family symmetry U(1)<sub>F</sub> and demanding anomaly "
     "cancellation -- a real, independently-motivated physical constraint used successfully "
     "in the flavor-model literature -- force those charges instead?")

h2("Setup")
body("The minimal fermion content this framework actually produces is exactly 3 chiral "
     "SO(10) 16-plets (one per generation, from the E8 &rarr; (16,3) branching), with no "
     "extra matter. Each generation's entire 16-plet carries a single family charge q<sub>i</sub>.")

h2("The anomaly conditions")
mono([
    "[SU(3)<sub>c</sub>]&sup2; U(1)<sub>F</sub>,  [SU(2)<sub>L</sub>]&sup2; U(1)<sub>F</sub>,",
    "[U(1)<sub>Y</sub>]&sup2; U(1)<sub>F</sub>,  gravity-U(1)<sub>F</sub>",
    "  all reduce to:      q1 + q2 + q3 = 0",
    "",
    "[U(1)<sub>F</sub>]&sup3;  reduces to:        q1&sup3; + q2&sup3; + q3&sup3; = 0",
])
body("(Verified numerically: the sum of hypercharges within one SO(10) 16-plet, weighted "
     "by color/isospin multiplicity, is exactly zero -- the standard fact underlying "
     "Standard Model anomaly freedom per generation. This makes the U(1)<sub>Y</sub>[U(1)<sub>F</sub>]&sup2; "
     "condition automatically satisfied for any charges, but leaves the two conditions above "
     "as genuine constraints.)")

h2("Exact solution")
mono([
    "Identity:  a&sup3;+b&sup3;+c&sup3; - 3abc = (a+b+c)(a&sup2;+b&sup2;+c&sup2;-ab-bc-ca)",
    "If a+b+c = 0, then a&sup3;+b&sup3;+c&sup3; = 3abc.",
    "Combined with a&sup3;+b&sup3;+c&sup3; = 0  =>  abc = 0",
    "=>  at least one charge must be exactly zero.",
    "=>  every anomaly-free solution has the form  (n, -n, 0).",
])
body("Confirmed by brute-force search over all integer charges with |q<sub>i</sub>| &le; 6: "
     "every solution found matches this pattern, with no exceptions.")

h2("Testing the project's own charges")
status_table(
    header=["Charge set", "&Sigma;q<sub>i</sub>", "&Sigma;q<sub>i</sub>&sup3;", "Anomaly-free?"],
    rows=[
        ["(3, 2, 0) -- used in Phase D", "5", "35", "NO"],
        ["(1, -1, 0)", "0", "0", "YES"],
        ["(2, -2, 0)", "0", "0", "YES"],
    ],
    colWidths=[2.4*inch, 1.3*inch, 1.4*inch, 1.4*inch],
    boxcolor=LIGHTRED,
)

h2("But the anomaly-free charges can't fit the data either")
body("The diagonal Yukawa suppression from the FN mechanism scales as &epsilon;<sup>|2q<sub>i</sub>|</sup>. "
     "For any (n,-n,0), the diagonal powers are {2n, 2n, 0} -- generations 1 and 2 are forced "
     "<b>degenerate</b> at leading order, no matter what n is chosen. The observed mass "
     "hierarchy (e.g. m<sub>u</sub> &lt;&lt; m<sub>c</sub> &lt;&lt; m<sub>t</sub>) needs three distinct, well-separated tiers.")

h2("Result")
story.append(Table([[Paragraph(
    "<b>THEOREM (L1):</b> For the minimal Cl(10)&times;E8 fermion content (3 chiral 16-plets, "
    "no extra matter), gauged-U(1)<sub>F</sub> anomaly-freedom and the observed 3-generation "
    "mass hierarchy are structurally incompatible. Anomaly cancellation does not derive "
    "q=(3,2,0) -- it rules it out -- and the charges it does allow cannot reproduce the data. "
    "Rescuing this requires new vector-like matter beyond the 3 complete 16-plets, whose "
    "charges and masses are themselves new free parameters. The free-parameter problem is "
    "relocated, not solved.", styles['Body'])]], colWidths=[6.6*inch])
)
story[-1].setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHTBLUE),
    ('BOX', (0,0), (-1,-1), 1, STEEL),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(Spacer(1, 12))
body("Full derivation and verification code: <font name='Courier'>phase_e_anomaly_constraints.py</font>")

story.append(PageBreak())

# =====================================================================
# PART 4b: PHASE F
# =====================================================================
h1("Part V -- Phase F (New, 2026-07-27): Does Messenger Matter Fix It?")
body("The literature's actual answer to the Phase E obstruction is to add vector-like "
     "\"messenger\" matter -- fields that are non-chiral under the Standard Model (so they "
     "introduce no new light SM states or SM gauge anomalies) but can be chiral under "
     "U(1)<sub>F</sub>, shifting the U(1)<sub>F</sub> anomaly sums. This section tests whether "
     "that actually rescues q=(3,2,0), by solving for the required messenger charges "
     "explicitly rather than searching or fitting them.")

h2("Explicit construction")
mono([
    "Need:  5 + (x+y) = 0        [linear deficit from q=(3,2,0)]",
    "       35 + (x&sup3;+y&sup3;) = 0     [cubic deficit from q=(3,2,0)]",
    "",
    "=>  x+y = -5,  xy = 6   =>   (x,y) = (-3,-2)",
    "",
    "One vector-like SO(10) pair (16<sub>M</sub>, 16bar<sub>M</sub>) with",
    "  charge(16<sub>M</sub>)    = -3",
    "  charge(16bar<sub>M</sub>) = +2",
    "exactly cancels both anomaly conditions.",
])
body("Verified: 5 + (&minus;3) + (&minus;2)<sub>effective</sub> = 0 (linear); "
     "35 + (&minus;3)&sup3; + (&minus;2)&sup3;<sub>effective</sub> = 0 (cubic). "
     "This is a genuine, checked result -- anomaly-freedom and the fitted hierarchy "
     "<b>can</b> coexist once this field is added.")

h2("Why this doesn't restore Rule 6")
bullets([
    "The messenger's charges were <b>solved for</b> specifically to cancel the anomaly of "
    "charges (3,2,0) that were themselves fitted to observed masses in Phase D -- "
    "reverse-engineering applied one level removed from where it happened the first time.",
    "The messenger's mass scale M is completely unconstrained by this argument -- "
    "a new free parameter, not fewer.",
    "Nothing forces the messenger representation to be (16, 16bar) specifically -- any "
    "SO(10) representation pair with the right anomaly bookkeeping would work equally "
    "well. That choice is itself undetermined.",
])

story.append(Table([[Paragraph(
    "<b>CONCLUSION:</b> Consistency between gauged-U(1)<sub>F</sub> anomaly-freedom and the "
    "fitted mass hierarchy is achievable, but only by adding back exactly as much freedom "
    "as Phase E removed. The free-parameter count after Phase F is <b>&ge; 13 (Phase D) + "
    "&ge; 1 new (messenger mass scale)</b> -- not fewer. This is the honest end of the "
    "anomaly-cancellation avenue for this specific model: a real, verified construction "
    "that relocates the free-parameter problem rather than solving it.", styles['Body'])]],
    colWidths=[6.6*inch])
)
story[-1].setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHTRED),
    ('BOX', (0,0), (-1,-1), 1, RED),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(Spacer(1, 12))
body("Full derivation and verification code: <font name='Courier'>phase_f_messenger_matter.py</font>")

story.append(PageBreak())

# =====================================================================
# PART 4c: PHASE G
# =====================================================================
h1("Part VI -- Phase G (New, 2026-07-27): Does the Messenger Fix Select Anything?")
body("The obvious follow-up to Phase F, tested directly rather than assumed: does the "
     "messenger construction actually prefer or constrain q=(3,2,0) in any way, or would it "
     "rescue any candidate FN charges equally well? Phase F's algebra is generalized from "
     "the one specific triple (3,2,0) to arbitrary integer triples, and integer-solution "
     "existence is checked across a sweep of candidates.")

h2("What was tested")
bullets([
    "Under this project's own convention (one generation's charge normalized to 0, exactly "
    "how q=(3,2,0) was produced), a single-messenger-pair fix was attempted for every "
    "integer FN-charge triple with 3 distinct mass-hierarchy tiers, in a &plusmn;8 range.",
    "The same test was repeated without the zero-normalization, as a sanity check.",
])

h2("Result")
mono([
    "Hierarchy-compatible triples (q3=0) tested: 208",
    "Fixable by a single messenger pair:         208  (100%)",
    "",
    "Algebraic identity: with q3=0, the solved messenger charges are",
    "always exactly (x, y) = (-q1, -q2) -- true for EVERY (q1, q2),",
    "not a special property of (3,2,0).",
    "",
    "Same test with q3 unconstrained (no zero charge): only 336/1176",
    "triples (29%) are fixable -- confirming the 100% figure above is",
    "an artifact of this project's own charge convention.",
])

story.append(Table([[Paragraph(
    "<b>CONCLUSION:</b> The messenger-matter mechanism has <b>zero selection power</b>. It "
    "cannot derive, favor, or even partially narrow down the FN charges -- any candidate "
    "assignment, matching observation or not, can be rescued the same way. This is stronger "
    "than the Phase F finding: Phase F showed the fix doesn't reduce the free-parameter "
    "count; Phase G shows it doesn't discriminate between candidate parameter values either, "
    "so it cannot be a step toward deriving them. The literature's stronger claim -- that a "
    "fuller Green-Schwarz construction can reduce charge freedom to a handful of integers -- "
    "relies on genuine string-compactification data (fixed modular weights, an "
    "anomalous-U(1) normalization tied to the string coupling) with no counterpart in the "
    "Cl(10)&times;E8 algebraic core. Importing it would graft on an unrelated string model, "
    "not derive anything from this framework. This closes the messenger/anomaly-cancellation "
    "line of attack for this project.", styles['Body'])]],
    colWidths=[6.6*inch])
)
story[-1].setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHTRED),
    ('BOX', (0,0), (-1,-1), 1, RED),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(Spacer(1, 12))
body("Full derivation and verification code: <font name='Courier'>phase_g_no_selection_power.py</font>")

story.append(PageBreak())

# =====================================================================
# PART 6b: PHASE H
# =====================================================================
h1("Part VII -- Phase H (New, 2026-07-27): The Actual Green-Schwarz Universality Condition")
body("Phases E/F/G only tested the pure U(1)_F conditions (linear, cubic) plus gravity. "
     "\"Green-Schwarz\" properly refers to something more specific: the mixed anomalies "
     "U(1)_F&ndash;SU(3)&sup2;, U(1)_F&ndash;SU(2)&sup2;, U(1)_F&ndash;U(1)_Y&sup2; must all be "
     "proportional across gauge factors (&quot;universality&quot;), not merely individually "
     "zero. Tested directly, not assumed: does this add any new constraint?")

h2("What was tested")
bullets([
    "The GUT-normalized Dynkin index of a full SO(10) 16-plet was computed explicitly under "
    "SU(3), SU(2), and U(1)_Y.",
    "For any matter content built from complete 16-plets (chiral generations or vector-like "
    "messenger pairs), the mixed anomaly with each gauge factor is A_a = (&Sigma;q_i) &times; "
    "I_a, so proportionality across gauge groups depends only on whether the indices I_a "
    "themselves are equal.",
])

h2("Result")
mono([
    "Index of one SO(10) 16 under SU(3):            2",
    "Index of one SO(10) 16 under SU(2):            2",
    "Index of one SO(10) 16 under U(1)_Y (GUT-norm): 2",
    "",
    "I3 : I2 : IY  =  2 : 2 : 2   -- identical, for every charge assignment.",
    "",
    "sum(q_i) = 0  (already required by Phase E/F/G)",
    "   =>  A3 = A2 = AY = 0   automatically, with no further condition.",
])

story.append(Table([[Paragraph(
    "<b>CONCLUSION:</b> the Green-Schwarz mixed-anomaly universality condition is "
    "<b>automatically satisfied</b> for any matter content built from complete SO(10) "
    "16-plets -- it falls out of GUT-normalized representation theory for free, and is not "
    "an extra condition to solve. Rigorous Green-Schwarz analysis adds zero new constraints "
    "beyond Phases E-G, closing off the possibility that a more careful anomaly analysis "
    "-- rather than more messenger fields -- was the missing ingredient. The literature's "
    "stronger claim (charge freedom reduced to as few as three integers) needs additional "
    "input from a specific string compactification -- a fixed anomalous-U(1) normalization "
    "against the string coupling, quantized modular weights tied to a particular compact "
    "manifold -- that is not group-theory data about SO(10) or E8, and that Cl(10)&times;E8 "
    "has no mechanism to supply. Reproducing it would mean importing a separate string "
    "model's numbers, not deriving anything from this framework -- exactly the "
    "reverse-engineering Ground Rule 2 forbids. This is as far as the anomaly/Green-Schwarz "
    "avenue can be taken from inside this framework.", styles['Body'])]],
    colWidths=[6.6*inch])
)
story[-1].setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHTRED),
    ('BOX', (0,0), (-1,-1), 1, RED),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(Spacer(1, 12))
body("Full derivation and verification code: <font name='Courier'>phase_h_green_schwarz_universality.py</font>")

story.append(PageBreak())

# =====================================================================
# PART 5: OTHER AVENUES (literature survey, not yet attempted)
# =====================================================================
h1("Part VIII -- Other Avenues")
body("Phase E tested one specific idea and it failed cleanly; Phase F tested the "
     "literature's fix for that failure and found it works but doesn't help; Phase G showed "
     "that fix has no power to select or constrain the charges at all; Phase H showed the "
     "full, properly-done Green-Schwarz condition adds nothing further either (Parts V-VII). "
     "A literature survey (2026-07-27) found three threads live in the field. Phase I "
     "(2026-07-27) then went back and actually tested the other two rather than leaving them "
     "as description -- see Part IX. All three have now been tried against this model.")

h2("1. Anomalous U(1) with extra (vector-like) matter -- TRIED (see Parts V-VII)")
body("This is exactly what Phase F implemented above: a single vector-like messenger pair "
     "with solved-for charges (&minus;3, +2) restores anomaly-freedom for q=(3,2,0), "
     "confirmed working, confirmed not to reduce the free-parameter count. Phase G then "
     "tested whether this fix discriminates between candidate charges at all, and found it "
     "does not -- it rescues essentially any hierarchy-compatible assignment equally well. In "
     "the wider literature, a related but distinct approach -- tying the anomalous U(1) to "
     "genuine string-derived Green-Schwarz data -- has been shown to reduce a flavor model's "
     "charge freedom to as few as three integers, but that relies on string-compactification "
     "specifics with no counterpart in this framework's algebraic core.")

h2("2. Modular flavor symmetry -- TRIED (see Part IX)")
body("Replaces the arbitrary flavon VEV direction with a single complex modulus &tau; valued "
     "in a discrete group (A4, S4&prime;, etc.), motivated by string-theoretic compactification. "
     "Phase I found this has already been combined with SO(10) in the literature (Ding, King, "
     "Lu, 2021) -- but every such construction needs the modulus and discrete group supplied by "
     "a specific string compactification, the same missing ingredient identified for "
     "Green-Schwarz in Phase H.")

h2("3. Entanglement-minimization principle -- TRIED (see Part IX)")
body("A genuinely different kind of argument, unrelated to gauge symmetry: Thaler and "
     "Trifinopoulos (arXiv:2410.23343) showed that the quantum entanglement generated in "
     "electroweak quark scattering is minimized when the CKM matrix is close to, but not "
     "exactly, the identity, and the same logic applied to leptons reproduces the observed "
     "PMNS pattern of two large angles and one small one. Phase I reproduced their central "
     "result independently rather than taking the abstract on faith -- see Part IX for what "
     "that confirmed.")

h2("Honest assessment of these avenues")
body("None of the three would, on current evidence, get this framework to zero free "
     "parameters. Avenue 1 has already been tried, exhaustively, in Parts V-VII "
     "(Phase F, Phase G, Phase H): a single vector-like messenger pair does restore "
     "anomaly-freedom, but adds a free mass scale rather than removing one; Phase G showed "
     "this fix has no power to select or constrain the charges at all; and Phase H showed the "
     "full, properly-done Green-Schwarz mixed-anomaly condition adds nothing further either -- "
     "it is automatically satisfied by SO(10) representation theory alone. Avenues 2 and 3 "
     "were tried directly in Phase I (Part IX): Avenue 2 shares Avenue 1's stronger-version "
     "blocker (string-compactification data this framework can't supply), and Avenue 3 turned "
     "out to be a self-contained principle that doesn't connect to or sharpen anything in "
     "Cl(10)&times;E8. That is the honest boundary of all three avenues for this framework.")

story.append(PageBreak())

# =====================================================================
# PART 9: PHASE I -- ACTUALLY TESTING THE REMAINING AVENUES
# =====================================================================
h1("Part IX -- Phase I (New, 2026-07-27): Actually Testing the Remaining Avenues")
body("\"Try everything possible\" was taken literally: rather than continuing to only "
     "describe Avenues 2 and 3 qualitatively, both were tested directly, and R1 (Part X of "
     "RESEARCH_ROADMAP.md) was re-grounded against real published work.")

h2("Entanglement-minimization -- independently reproduced")
body("The Thaler-Trifinopoulos two-generation calculation (their Eq. 32) was reimplemented "
     "from scratch, not taken on faith from the abstract.")
mono([
    "Using measured sin^2(theta_W) = 0.2312:",
    "  entangling-power minimum at theta_C = 6.20 deg",
    "  (published result: ~6 deg; measured Cabibbo angle: ~13.0 deg)",
    "",
    "Robustness check -- GUT-scale sin^2(theta_W) = 3/8 instead:",
    "  entangling-power minimum at theta_C = 7.04 deg  (barely moves)",
])
body("The principle uses exactly the SM charges (Q, T3) that Cl(10)&times;E8 already "
     "derives for free (Part I of this document) -- but its one remaining input, "
     "sin&sup2;&theta;_W, is not derived by this framework, and swapping in the GUT-scale "
     "value instead of the measured one barely changes the result. There is no sense in "
     "which this framework's own structure sharpens the prediction, and on its own numbers "
     "the principle undershoots the real Cabibbo angle by roughly a factor of 2 -- exactly as "
     "its original authors note. It does not reduce this project's free-parameter count.")

h2("Modular flavor symmetry -- literature-checked, not assumed")
body("A literature check found that modular-flavor-symmetric SO(10) models already exist "
     "(Ding, King, Lu, \"SO(10) models with A4 modular symmetry,\" JHEP 11 (2021) 007) -- so "
     "this avenue is not simply unconnected to SO(10). But in every such construction, the "
     "modular group and modulus &tau; are extra data from a specific string compactification "
     "-- the same missing ingredient Phase H identified for the fuller Green-Schwarz "
     "mechanism. Neither avenue can be honestly presented as a Cl(10)&times;E8 derivation; "
     "both would mean starting a different, string-model-building project.")

h2("R1 (spectral action / NCG) -- re-grounded against existing work")
body("Chamseddine, Connes, and van Suijlekom already extended the spectral-action / "
     "noncommutative-geometry Standard Model specifically to Pati-Salam unification (JHEP 11 "
     "(2013) 132; JHEP 11 (2015) 011, including gauge-coupling unification running). "
     "Pati-Salam is a maximal subgroup in the SO(10)-breaking chain this project's own "
     "Cl(10)&rarr;SO(10) embedding passes through. The honest next step for R1 is therefore "
     "not building a spectral triple from scratch, but checking whether that existing, "
     "peer-reviewed construction's finite algebra and Hilbert space match the fermion content "
     "Cl(10)&times;E8 already derives -- a smaller, better-defined lift than originally "
     "scoped. Full detail in RESEARCH_ROADMAP.md.")

story.append(PageBreak())

# =====================================================================
# PHASE U -- LIVE LITERATURE RE-CHECK
# =====================================================================
h1("Phase U: Live Literature Re-Check (2026-07-28)")
body("The hypothesis backlog (PHASE_R_HYPOTHESIS_BACKLOG.md) flags several items as "
     "recurring literature checks, not one-time. Phase U re-ran the most relevant of "
     "these -- items 6, 8, 9, 17, 18, 28 -- using live web search rather than static "
     "training-data recall, on the same day as Phase R.")

h2("Finding 1: item 6 (Cl(8) S3 family symmetry) has a direct Cl(10) sequel")
body("The backlog's own citation (Gourlay &amp; Gresnigt, Eur. Phys. J. C 84 (2024) "
     "1129) uses Cl(8), not Cl(10). Live search finds the same group has since "
     "published <b>N. Gresnigt, \"Electroweak Structure and Three Fermion Generations "
     "in Clifford Algebra with S3 Family Symmetry,\" arXiv:2601.07857</b> (2026-01, v2 "
     "2026-04) -- fermions as minimal left ideals of complex Cl(10), the SAME base "
     "algebra as this project's own Phase A1, with three generations produced by an "
     "intrinsic S3 automorphism rather than this project's E8-branching route. A "
     "Yukawa-sector follow-up, <b>arXiv:2604.24795</b> (2026-04/06), reports a "
     "Type-II-like, algebraically-fixed but non-diagonal Yukawa matrix in the S3 basis "
     "-- a structural result, not a claim of absolute mass values.")
body("Neither paper is reproduced or code-verified in this project. Because it shares "
     "Phase A1's exact base algebra, it is the single most directly comparable "
     "external construction found in any of this project's literature sweeps, and is "
     "flagged as the highest-leverage concrete next step this project has identified "
     "for itself: implement the S3-on-Witt-ideals mechanism against Phase A1's own "
     "code and check, by computation, whether it reproduces Phase A1's charge "
     "assignment.")

h2("Finding 2: items 8/9 (exceptional Jordan algebra) -- sub-field moving toward fits")
body("The backlog cites one rigid, parameter-free paper (T.P. Singh, arXiv:2508.10131). "
     "Two sequels were found: <b>Gupta Teli &amp; Singh, arXiv:2605.24866</b> (2026-05) "
     "promotes the rigid point to a fitted spectral-moduli-space model (global log-fit "
     "to six mass ratios, explicitly described by its authors as not a parameter-free "
     "replacement); and <b>arXiv:2607.00412</b> (~2026-06) extends this to CKM/PMNS "
     "mixing via a bridge ansatz its own authors call effective, not a theorem. This "
     "sub-field is moving toward fitted models -- the same direction Phase D already "
     "went -- not away from it.")

h2("Finding 3: item 28 (Furey &amp; Hughes trialities) -- read, chirality status open")
body("<b>Furey &amp; Hughes, Phys. Lett. B 865 (2025) 139473</b> uses a division-algebra "
     "triality mechanism (tri(C)+tri(H)+tri(O)), structurally distinct from both this "
     "project's E8 route and Finding 1's Cl(10)-S3 route. The retrieved text does not "
     "address the Distler-Garibaldi non-chirality theorem (Priority 0's subject) for "
     "this specific construction. Since it is not an E8-adjoint-248 placement, this "
     "project's own Priority-0 check (Phase R) does not automatically clear it. Logged "
     "as genuinely open.")

h2("Net effect")
body("Zero change to Phase C's ~13 free parameters. No item is promoted past "
     "\"[lit] DONE\" -- identified and read, not reproduced -- per this project's own "
     "rule against faking verification. Full detail in phase_u_literature_2026.py, "
     "README.md, solution.md, and PHASE_R_HYPOTHESIS_BACKLOG.md.")

story.append(PageBreak())

# =====================================================================
# PHASE V -- REAL-TIER BACKLOG ITEMS COMPUTED DIRECTLY
# =====================================================================
h1("Phase V: Backlog Items 20 and 33 (2026-07-28)")
body("Of the backlog's remaining [real]-tier items, two turned out to need no "
     "external Lie-theory package -- only this project's own octonion code plus "
     "elementary number theory. Both were run directly.")

h2("Item 33: Malcev-algebra invariant")
body("The imaginary octonions under the commutator bracket are known (Kuzmin 1968, "
     "Sagle 1961) to form a simple Malcev algebra. This project's own structure "
     "constants had never been checked against the Malcev identity directly -- done "
     "here for the first time in this repo, and it holds exactly (residual 0). The "
     "induced trace-form invariant tr(ad_x ad_y) is proportional to the identity "
     "matrix on the 7-dimensional imaginary-octonion basis -- the unique "
     "G2-invariant form, carrying no extra structure (no distinguished 3-dimensional "
     "subspace, no eigenvalue splitting) that could be read as \"3 generations.\" "
     "CLOSED, negative.")

h2("Item 20: p-adic (p=3) Froggatt-Nielsen charges")
body("Tested whether a 3-adic valuation, rather than ordinary absolute value, gives "
     "a natural 3-tier ordering of the fitted FN charges (3,2,0). It does not: the "
     "3-adic valuation is undefined at charge 0, breaking the ordering outright, and "
     "on the anomaly-free family (n,-n,0) it reproduces exactly the 2-tier "
     "degeneracy Phase E already proved with real numbers, since v_3(n)=v_3(-n) "
     "always. Also flagged, honestly, as not statistically meaningful given only 3 "
     "data points. CLOSED, negative / not meaningful as posed.")

h2("Item 15: explicitly considered, not attempted")
body("Checking Phase B's CKM=I/PMNS=I claim with real branching multiplicities (not "
     "just dimension counts) needs a weight-multiplicity engine of the kind LiE, "
     "Sage, or GAP provide. This environment doesn't have one, and computing E8/E6 "
     "tensor-product multiplicities by hand risks producing an unverified result "
     "dressed up as a derived one -- exactly what this project's own rules forbid. "
     "Left open, correctly scoped.")

body("Net effect on Phase C's ~13 free parameters: zero. Full detail in "
     "phase_v_realtier_items.py.")

story.append(PageBreak())



# =====================================================================
# CLOSING
# =====================================================================
h1("Closing Statement")
body("The algebraic core (Cl(10) &times; E8) correctly derives structural features of the "
     "Standard Model that the Standard Model itself simply postulates: the gauge group, "
     "charge quantization, and the 3-generation structure. This is mathematically sound but "
     "not new -- these results were already known from 1980s Clifford-algebra work and "
     "standard E8 representation theory.")
body("The project does <b>not</b> predict any numerical Standard Model parameter. Phase E, "
     "Phase F, Phase G, and Phase H, the four new results added after closure, show that one "
     "natural attempt to fix this -- gauged family-symmetry anomaly cancellation -- fails for a "
     "specific, provable structural reason (Phase E); that the literature's own fix for that "
     "failure -- adding vector-like messenger matter -- restores consistency but only by "
     "adding a new free mass scale, not by removing any existing freedom (Phase F); that "
     "this fix cannot even discriminate between candidate charge values, so it offers no path "
     "toward deriving them (Phase G); and that even the full, properly-done Green-Schwarz "
     "mixed-anomaly condition adds nothing further, since it is automatically satisfied by "
     "SO(10) representation theory alone (Phase H). This limitation is shared by all known "
     "theories of particle physics; deriving the 19 Standard Model parameters from a deeper "
     "symmetry remains an open problem in the field, not a gap specific to this project.")
rule()
story.append(Paragraph("God's Paradox -- Final Assessment, with Phase E-V addenda (2026-07-27/28). Project closed 2026-07-27; Phases Q-V added post-closure as checks and re-checks, not reopenings.",
                        styles['Caption']))

doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                         topMargin=0.85*inch, bottomMargin=0.85*inch,
                         leftMargin=0.9*inch, rightMargin=0.9*inch,
                         title="God's Paradox -- Final Assessment")
doc.build(story)
print(f"Wrote {OUT}")
