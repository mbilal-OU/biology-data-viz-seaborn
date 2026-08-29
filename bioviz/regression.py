"""Regression plots and simple curve-fitting helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit


def michaelis_menten(s: np.ndarray, vmax: float, km: float) -> np.ndarray:
    """Michaelis-Menten rate equation: v = Vmax * [S] / (Km + [S])."""
    return vmax * s / (km + s)


def fit_michaelis_menten(df: pd.DataFrame) -> pd.DataFrame:
    """Fit Vmax and Km per inhibitor condition via nonlinear least squares.

    Parameters
    ----------
    df : DataFrame with columns ``inhibitor``, ``substrate_conc``, ``rate``.

    Returns
    -------
    DataFrame with one row per inhibitor: fitted ``vmax``, ``km``, and
    their standard errors from the covariance matrix.
    """
    records = []
    for inhibitor, group in df.groupby("inhibitor"):
        s = group["substrate_conc"].to_numpy()
        v = group["rate"].to_numpy()
        popt, pcov = curve_fit(michaelis_menten, s, v, p0=[max(v), np.median(s)])
        perr = np.sqrt(np.diag(pcov))
        records.append(
            {
                "inhibitor": inhibitor,
                "vmax": popt[0],
                "km": popt[1],
                "vmax_se": perr[0],
                "km_se": perr[1],
            }
        )
    return pd.DataFrame(records)


def enzyme_kinetics_lmplot(df: pd.DataFrame):
    """Faceted regression plot (log-x) of rate vs. substrate concentration.

    Uses sns.lmplot with a 2nd-order polynomial fit on log-scaled
    substrate concentration, which visually approximates saturation
    kinetics without requiring a custom nonlinear estimator inside
    lmplot itself. For the *actual* Michaelis-Menten parameter
    estimates, see :func:`fit_michaelis_menten`.
    """
    plot_df = df.copy()
    plot_df["log_substrate"] = np.log2(plot_df["substrate_conc"])
    g = sns.lmplot(
        data=plot_df,
        x="log_substrate",
        y="rate",
        hue="inhibitor",
        order=2,
        height=5,
        aspect=1.2,
        scatter_kws={"alpha": 0.6},
    )
    g.set_axis_labels("log2(substrate concentration)", "Reaction rate")
    g.figure.suptitle("Enzyme Kinetics: Inhibitor Effects", y=1.03, fontweight="bold")
    return g
