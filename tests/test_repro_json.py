from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from src.utils.repro import dump_json, save_json


def test_dump_json_handles_numpy_and_path_types(tmp_path: Path):
    out = tmp_path / "payload.json"
    payload = {
        "f32": np.float32(1.5),
        "i64": np.int64(7),
        "b": np.bool_(True),
        "arr": np.asarray([1, 2, 3], dtype=np.int32),
        "nested": {"v": np.float64(2.25)},
        "path": tmp_path / "artifact.bin",
    }

    dump_json(out, payload)
    loaded = json.loads(out.read_text(encoding="utf-8"))

    assert loaded["f32"] == 1.5
    assert loaded["i64"] == 7
    assert loaded["b"] is True
    assert loaded["arr"] == [1, 2, 3]
    assert loaded["nested"]["v"] == 2.25
    assert loaded["path"] == str(tmp_path / "artifact.bin")


def test_dump_json_handles_keras_like_history(tmp_path: Path):
    out = tmp_path / "history.json"
    history_like = {
        "loss": [np.float32(1.2866), np.float32(1.0692)],
        "accuracy": [np.float32(0.4292)],
        "val_accuracy": [np.float32(0.4907)],
        "lr": [np.float32(0.001)],
    }

    dump_json(out, history_like)
    loaded = json.loads(out.read_text(encoding="utf-8"))

    assert loaded["loss"] == pytest.approx([1.2866, 1.0692])
    assert loaded["accuracy"] == pytest.approx([0.4292])
    assert loaded["val_accuracy"] == pytest.approx([0.4907])
    assert loaded["lr"] == pytest.approx([0.001])


def test_save_json_keeps_sorted_key_behavior(tmp_path: Path):
    out = tmp_path / "sorted.json"
    payload = {"z": np.int64(1), "a": np.int64(2)}

    save_json(out, payload)
    text = out.read_text(encoding="utf-8")
    loaded = json.loads(text)

    assert loaded == {"a": 2, "z": 1}
    assert text.index('"a"') < text.index('"z"')
