"""Core helpers for exploring and summarizing tabular data.

All functions accept a :class:`pandas.DataFrame` and return plain pandas
objects (lists, ``Series`` or ``DataFrame``) so results compose naturally
with the rest of the pandas ecosystem.
"""

from __future__ import annotations

from typing import List

import pandas as pd
from pandas.api import types as ptypes

__all__ = [
    "numeric_columns",
    "categorical_columns",
    "missing",
    "summarize",
]


def _require_dataframe(df: object) -> pd.DataFrame:
    """Validate that ``df`` is a DataFrame, raising a clear error otherwise."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"expected a pandas DataFrame, got {type(df).__name__!r}"
        )
    return df


def numeric_columns(df: pd.DataFrame) -> List[str]:
    """Return the names of the numeric columns in ``df``.

    Boolean columns are treated as non-numeric, matching how they are usually
    handled in exploratory analysis.

    Parameters
    ----------
    df:
        The DataFrame to inspect.

    Returns
    -------
    list of str
        Column names whose dtype is numeric, in column order.
    """
    df = _require_dataframe(df)
    return [
        col
        for col in df.columns
        if ptypes.is_numeric_dtype(df[col]) and not ptypes.is_bool_dtype(df[col])
    ]


def categorical_columns(df: pd.DataFrame) -> List[str]:
    """Return the names of the non-numeric columns in ``df``.

    This is the complement of :func:`numeric_columns`: object, string,
    category and boolean columns are all considered categorical.

    Parameters
    ----------
    df:
        The DataFrame to inspect.

    Returns
    -------
    list of str
        Column names that are not numeric, in column order.
    """
    df = _require_dataframe(df)
    numeric = set(numeric_columns(df))
    return [col for col in df.columns if col not in numeric]


def missing(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize missing values per column.

    Parameters
    ----------
    df:
        The DataFrame to inspect.

    Returns
    -------
    pandas.DataFrame
        One row per column with two fields, sorted by ``percent`` descending:

        ``count``
            Number of missing (NaN/None) values in the column.
        ``percent``
            Percentage of values missing, in the range ``0``–``100``.
    """
    df = _require_dataframe(df)
    counts = df.isna().sum()
    n_rows = len(df)
    percent = (counts / n_rows * 100) if n_rows else counts * 0.0
    result = pd.DataFrame({"count": counts, "percent": percent})
    return result.sort_values("percent", ascending=False)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Produce a per-numeric-column summary of a DataFrame.

    Unlike :meth:`pandas.DataFrame.describe`, this reports missing-value
    information alongside the usual descriptive statistics, which makes it a
    convenient first look at a new dataset.

    Parameters
    ----------
    df:
        The DataFrame to summarize.

    Returns
    -------
    pandas.DataFrame
        One row per numeric column with the columns: ``count``, ``missing``,
        ``missing_percent``, ``mean``, ``std``, ``min``, ``25%``, ``50%``,
        ``75%`` and ``max``. If ``df`` has no numeric columns, an empty frame
        with those columns is returned.
    """
    df = _require_dataframe(df)
    cols = numeric_columns(df)
    fields = [
        "count",
        "missing",
        "missing_percent",
        "mean",
        "std",
        "min",
        "25%",
        "50%",
        "75%",
        "max",
    ]
    if not cols:
        return pd.DataFrame(columns=fields)

    numeric = df[cols]
    n_rows = len(df)
    missing_count = numeric.isna().sum()
    rows = {
        "count": numeric.count(),
        "missing": missing_count,
        "missing_percent": (missing_count / n_rows * 100) if n_rows else missing_count * 0.0,
        "mean": numeric.mean(),
        "std": numeric.std(),
        "min": numeric.min(),
        "25%": numeric.quantile(0.25),
        "50%": numeric.quantile(0.50),
        "75%": numeric.quantile(0.75),
        "max": numeric.max(),
    }
    return pd.DataFrame(rows, index=cols)[fields]
