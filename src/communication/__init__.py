"""communication: lightweight helpers for summarizing tabular data.

Example
-------
>>> import pandas as pd
>>> import communication as comm
>>> df = pd.DataFrame({"a": [1, 2, None], "b": ["x", "y", "z"]})
>>> comm.numeric_columns(df)
['a']
>>> comm.missing(df)["count"]["a"]
1
"""

from .summary import (
    categorical_columns,
    missing,
    numeric_columns,
    summarize,
)

__version__ = "0.1.0"

__all__ = [
    "numeric_columns",
    "categorical_columns",
    "missing",
    "summarize",
    "__version__",
]
