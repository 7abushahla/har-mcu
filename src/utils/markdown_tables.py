"""Dependency-free markdown table helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _fmt_cell(value: Any) -> str:
    if value is None or pd.isna(value):
        return "—"
    text = str(value)
    text = text.replace("|", r"\|")
    text = text.replace("\n", " ")
    return text


def dataframe_to_pipe_markdown(df: pd.DataFrame) -> str:
    """Render a pandas dataframe as a markdown pipe table without tabulate."""

    if df.empty:
        return "| (no rows) |\n| --- |\n| — |\n"

    cols = [str(c) for c in df.columns]
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows = [
        "| " + " | ".join(_fmt_cell(v) for v in row) + " |"
        for row in df.itertuples(index=False, name=None)
    ]
    return "\n".join([header, sep, *rows]) + "\n"
