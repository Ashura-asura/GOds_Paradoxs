"""
TASK 3 — TWIN NUCLEATION LAW
Rule-2 pre-registration:
  Candidate predictors of a twin-formation event (new twin PAIR created by
  a step, TwinGain = twin_pairs_after - twin_pairs_before > 0):
    R   = |extremal removable edge set|          (tie multiplicity, removal)
    A   = |extremal addable non-edge set|         (tie multiplicity, addition)
    TH0 = pre-step Theta (neighborhood-overlap potential proxy)
    DV  = pre-step degree variance (binned)
    DE  = pre-step degree entropy (binned)
  H: ranking by exact mutual information I(TwinGain>0 ; X) will show R,A
     (tie geometry, Z30/Z34's own hypothesis) dominating over DV/DE
     (degree-convergence, Z35's H1), matching the Z35 H2 result.
  Falsifier: if I(TwinGain>0;DV)+I(TwinGain>0;DE) > 2 * (I(...;R)+I(...;A))
     then H2 is rejected in favor of H1, recorded regardless of outcome.

No correlation is used anywhere below -- only histogram-based exact MI in
bits, per the task instruction.
"""
import math, random, json, collections
from z100_core import random_graph, step, theta, twin_partition, degree_variance, degree_entropy

N, M = 10, 15
NCHAINS = 250
STEPS = 25
SEED0 = 20260803999


def twin_pairs_count(classes):
    return sum(len(c) * (len(c) - 1) // 2 for c in classes)


def bin3(x, edges):
    if x <= edges[0]:
        return "low"
    if x <= edges[1]:
        return "med"
    return "high"


def mutual_info(pairs):
    """pairs: list of (x_bin, y_bool). Exact MI in bits from empirical joint."""
    n = len(pairs)
    if n == 0:
        return 0.0
    joint = collections.Counter(pairs)
    px = collections.Counter(x for x, y in pairs)
    py = collections.Counter(y for x, y in pairs)
    mi = 0.0
    for (x, y), c in joint.items():
        pxy = c / n
        mi += pxy * math.log2(pxy / (px[x] / n * py[y] / n))
    return mi


def entropy_binary(pairs):
    n = len(pairs)
    p1 = sum(1 for _, y in pairs if y) / n
    if p1 in (0, 1):
        return 0.0
    return -(p1 * math.log2(p1) + (1 - p1) * math.log2(1 - p1))


def main():
    rng_global = random.Random(SEED0)
    records = []  # each: dict of R,A,TH0,DV,DE, TwinGain(bool)

    for c in range(NCHAINS):
        rng = random.Random(SEED0 + c)
        G = random_graph(N, M, rng)
        for t in range(STEPS):
            classes_before = twin_partition(G)
            tp_before = twin_pairs_count(classes_before)
            th0, _ = theta(G)
            dv = degree_variance(G)
            de = degree_entropy(G)
            out = step(G, rng, selector="random")
            if out[1] is None:
                break
            Gp, r_edge, a_edge, Rsize, Asize = out
            classes_after = twin_partition(Gp)
            tp_after = twin_pairs_count(classes_after)
            gain = tp_after - tp_before
            records.append(dict(R=Rsize, A=Asize, TH0=th0, DV=dv, DE=de,
                                 gain_pos=(gain > 0)))
            G = Gp

    # Determine tertile bin edges from the pooled data (pre-registered method:
    # empirical tertiles, computed once, used for all binning below)
    def tertiles(vals):
        s = sorted(vals)
        n = len(s)
        return (s[n // 3], s[2 * n // 3])

    R_edges = tertiles([r["R"] for r in records])
    A_edges = tertiles([r["A"] for r in records])
    TH0_edges = tertiles([r["TH0"] for r in records])
    DV_edges = tertiles([r["DV"] for r in records])
    DE_edges = tertiles([r["DE"] for r in records])

    pairs_R = [(bin3(r["R"], R_edges), r["gain_pos"]) for r in records]
    pairs_A = [(bin3(r["A"], A_edges), r["gain_pos"]) for r in records]
    pairs_TH0 = [(bin3(r["TH0"], TH0_edges), r["gain_pos"]) for r in records]
    pairs_DV = [(bin3(r["DV"], DV_edges), r["gain_pos"]) for r in records]
    pairs_DE = [(bin3(r["DE"], DE_edges), r["gain_pos"]) for r in records]
    # joint (R,A) for conditional / minimal-sufficient-statistic testing
    pairs_RA = [((bin3(r["R"], R_edges), bin3(r["A"], A_edges)), r["gain_pos"]) for r in records]
    pairs_RATH0 = [((bin3(r["R"], R_edges), bin3(r["A"], A_edges), bin3(r["TH0"], TH0_edges)), r["gain_pos"]) for r in records]

    H_T = entropy_binary([(0, r["gain_pos"]) for r in records])

    I = {
        "R": mutual_info(pairs_R),
        "A": mutual_info(pairs_A),
        "TH0": mutual_info(pairs_TH0),
        "DV": mutual_info(pairs_DV),
        "DE": mutual_info(pairs_DE),
        "R,A_joint": mutual_info(pairs_RA),
        "R,A,TH0_joint": mutual_info(pairs_RATH0),
    }

    base_rate = sum(1 for r in records if r["gain_pos"]) / len(records)

    ranking = sorted([(k, v) for k, v in I.items() if "," not in k], key=lambda kv: -kv[1])

    I_RA = I["R,A_joint"]
    I_deg = I["DV"] + I["DE"]
    I_tie = I["R"] + I["A"]

    verdict = None
    if I_tie >= 2 * I_deg:
        verdict = "H2 (tie geometry R,A dominates) -- SURVIVES"
    elif I_deg >= 2 * I_tie:
        verdict = "H1 (degree convergence DV,DE dominates) -- SURVIVES; Z35 H2 REJECTED"
    else:
        verdict = "MIXED -- neither dominates by the pre-registered 2x margin"

    report = {
        "N": N, "M": M, "n_events": len(records),
        "base_rate_twin_gain_positive": base_rate,
        "H_binary_bits": H_T,
        "mutual_information_bits": I,
        "ranking_single_variables": ranking,
        "minimal_sufficient_statistic_check": {
            "I(gain;R,A)": I_RA,
            "I(gain;R,A,TH0)": I["R,A,TH0_joint"],
            "additional_info_from_TH0_given_R_A": I["R,A,TH0_joint"] - I_RA,
            "interpretation": (
                "If I(gain;R,A,TH0) - I(gain;R,A) is small relative to H_T, "
                "(R,A) alone is close to a minimal sufficient statistic."
            ),
        },
        "verdict": verdict,
    }
    print(json.dumps(report, indent=2))
    with open("task3_results.json", "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    main()
