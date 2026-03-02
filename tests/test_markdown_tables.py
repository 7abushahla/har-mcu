from __future__ import annotations

import pandas as pd

from src.utils.markdown_tables import dataframe_to_pipe_markdown


def test_dataframe_to_pipe_markdown_formats_nulls_and_escapes():
    df = pd.DataFrame(
        [
            {"name": "a|b", "value": 1.23, "note": None},
            {"name": "plain", "value": float("nan"), "note": "ok"},
        ]
    )
    md = dataframe_to_pipe_markdown(df)

    assert "| name | value | note |" in md
    assert r"a\|b" in md
    assert "—" in md


def test_dataframe_to_pipe_markdown_empty():
    df = pd.DataFrame(columns=["a", "b"])
    md = dataframe_to_pipe_markdown(df)
    assert "(no rows)" in md
