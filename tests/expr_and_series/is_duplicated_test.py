from typing import Any

import pytest

import narwhals.stable.v1 as nw
from tests.utils import compare_dicts

data = {
    "a": [1, 1, 2],
    "b": [1, 2, 3],
}


def test_is_duplicated(request: Any, constructor: Any) -> None:
    if "pyarrow_table" in str(constructor):
        request.applymarker(pytest.mark.xfail)
    df = nw.from_native(constructor(data), eager_only=True)
    result = df.select(nw.all().is_duplicated())
    expected = {
        "a": [True, True, False],
        "b": [False, False, False],
    }
    compare_dicts(result, expected)