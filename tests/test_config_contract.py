from __future__ import annotations

from src.utils.config import load_yaml


def test_default_config_contract():
    cfg = load_yaml("configs/default.yaml")
    assert "paths" in cfg
    assert "raw_csv" in cfg["paths"]
    assert "window_size_default" in cfg
    assert "train" in cfg
    assert "quant" in cfg
    assert "deploy" in cfg
