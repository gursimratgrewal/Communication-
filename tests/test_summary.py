import numpy as np
import pandas as pd
import pytest

import communication as comm


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "age": [25, 30, None, 45],
            "score": [1.5, 2.5, 3.5, 4.5],
            "name": ["a", "b", "c", None],
            "active": [True, False, True, True],
        }
    )


def test_numeric_columns_excludes_bool_and_object(df):
    assert comm.numeric_columns(df) == ["age", "score"]


def test_categorical_columns_is_complement(df):
    assert comm.categorical_columns(df) == ["name", "active"]


def test_numeric_and_categorical_partition_all_columns(df):
    combined = set(comm.numeric_columns(df)) | set(comm.categorical_columns(df))
    assert combined == set(df.columns)


def test_missing_counts_and_percent(df):
    result = comm.missing(df)
    assert result.loc["age", "count"] == 1
    assert result.loc["name", "count"] == 1
    assert result.loc["score", "count"] == 0
    assert result.loc["age", "percent"] == pytest.approx(25.0)
    assert result.loc["score", "percent"] == pytest.approx(0.0)


def test_missing_sorted_descending(df):
    percents = comm.missing(df)["percent"].tolist()
    assert percents == sorted(percents, reverse=True)


def test_summarize_only_numeric_columns(df):
    result = comm.summarize(df)
    assert list(result.index) == ["age", "score"]


def test_summarize_reports_missing(df):
    result = comm.summarize(df)
    assert result.loc["age", "missing"] == 1
    assert result.loc["age", "missing_percent"] == pytest.approx(25.0)
    assert result.loc["age", "count"] == 3


def test_summarize_statistics(df):
    result = comm.summarize(df)
    assert result.loc["score", "mean"] == pytest.approx(3.0)
    assert result.loc["score", "min"] == pytest.approx(1.5)
    assert result.loc["score", "max"] == pytest.approx(4.5)
    assert result.loc["score", "50%"] == pytest.approx(3.0)


def test_summarize_no_numeric_columns_returns_empty():
    df = pd.DataFrame({"x": ["a", "b"], "y": ["c", "d"]})
    result = comm.summarize(df)
    assert result.empty
    assert "mean" in result.columns


def test_empty_dataframe_missing_no_division_error():
    result = comm.missing(pd.DataFrame({"a": []}))
    assert result.loc["a", "count"] == 0
    assert result.loc["a", "percent"] == 0.0


@pytest.mark.parametrize("func", [comm.numeric_columns, comm.missing, comm.summarize])
def test_non_dataframe_raises_typeerror(func):
    with pytest.raises(TypeError):
        func([1, 2, 3])
