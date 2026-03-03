"""Microsimulation loading and household classification."""

import pandas as pd
from policyengine_uk import Microsimulation

from .config import YEAR, GROUPS


def load_sim(reform=None):
    """Load a Microsimulation, optionally with a reform."""
    if reform is not None:
        return Microsimulation(reform=reform)
    return Microsimulation()


def classify_benunits(sim):
    """Return family_type and is_pensioner_benunit MicroSeries at benunit level."""
    family_type = sim.calculate("family_type", YEAR)
    is_sp_age = sim.calculate("is_SP_age", YEAR, map_to="benunit")
    benunit_adults = sim.calculate("benunit_count_adults", YEAR)
    is_pensioner_bu = (is_sp_age >= benunit_adults).astype(float)
    return family_type, is_pensioner_bu


def compute_group_stats(sim):
    """Return a DataFrame with weighted mean and median hnet per group."""
    family_type, is_pensioner_bu = classify_benunits(sim)
    hnet = sim.calculate("household_net_income", YEAR, map_to="benunit")

    rows = []
    for label, mask_fn in GROUPS.items():
        mask = mask_fn(family_type, is_pensioner_bu)
        mean_hnet = float(hnet[mask].mean())
        median_hnet = float(hnet[mask].median())
        count = float(mask.sum())
        rows.append({
            "group": label,
            "mean_hnet": mean_hnet,
            "median_hnet": median_hnet,
            "weighted_n": count,
        })
    return pd.DataFrame(rows)
