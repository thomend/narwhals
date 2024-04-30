from __future__ import annotations

import pandas as pd
import polars as pl
import pytest
from hypothesis import example
from hypothesis import given
from hypothesis import strategies as st

import narwhals as nw
from tests.utils import compare_dicts


#@example([0, 0, 0], [0, 0, 0], [0.0, 0.0, -0.0], ["c"])  # type: ignore[misc]
@given(
    st.lists(
        st.integers(min_value=-9223372036854775807, max_value=9223372036854775807),
        min_size=3,
        max_size=3,
    ),
    st.lists(
        st.integers(min_value=-9223372036854775807, max_value=9223372036854775807),
        min_size=3,
        max_size=3,
    ),
    st.lists(
        st.floats(min_value=-9223372036854775807.0, max_value=9223372036854775807.0),
        min_size=3,
        max_size=3,
    ),
    st.sampled_from(["horizontal", "vertical"]),
)  # type: ignore[misc]
def test_concat(
    integers: st.SearchStrategy[list[int]],
    other_integers: st.SearchStrategy[list[int]],
    floats: st.SearchStrategy[list[float]],
    how: st.SearchStrategy[str],
) -> None:
    data = {"a": integers, "b": other_integers, "c": floats}

    df_polars = pl.DataFrame(data)
    df_polars2 = pl.DataFrame(data)
    
    if how == "horizontal":
        df_pl = nw.LazyFrame(df_polars).collect().rename({"a": "d", "b": "e"}).lazy().drop("c")
    else:
        df_pl = nw.LazyFrame(df_polars)

    other_pl = nw.LazyFrame(df_polars2)
    dframe_pl_horizontal = nw.concat([df_pl, other_pl], how=how)
    
    df_pandas = pd.DataFrame(data)
    df_pandas2 = pd.DataFrame(data)

    if how == "horizontal":
        df_pd = nw.LazyFrame(df_pandas).collect().rename({"a": "d", "b": "e"}).lazy().drop("c")
    else:
        df_pd = nw.LazyFrame(df_pandas)
    
    other_pd = nw.LazyFrame(df_pandas2)
    dframe_pd_horizontal = nw.concat([df_pd, other_pd], how=how)

    dframe_pd1 = nw.to_native(dframe_pl_horizontal)
    dframe_pd2 = nw.to_native(dframe_pd_horizontal)
    
    compare_dicts(dframe_pd1, dframe_pd2)