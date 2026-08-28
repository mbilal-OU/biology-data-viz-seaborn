"""
bioviz
======
A small, importable plotting toolkit that wraps Seaborn/Matplotlib with
consistent styling and typed, documented functions for common biology
and bioinformatics visualization tasks.

Example
-------
>>> import pandas as pd
>>> from bioviz import theme, relational
>>> theme.set_theme()
>>> df = pd.read_csv("data/docking_scores.csv")
>>> fig, ax = relational.docking_scatter(df)
"""

from . import theme  # noqa: F401
from ._version import __version__  # noqa: F401

__all__ = ["theme", "__version__"]
