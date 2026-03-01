from __future__ import annotations

from src.utils.config import load_yaml


def test_default_config_contract():
    cfg = load_yaml("configs/default.yaml")
    assert "paths" in cfg
    assert "raw_csv" in cfg["paths"]
    assert "window_size_default" in cfg
    assert "train" in cfg
    assert "quant" in cfg
    assert "ptq" in cfg["quant"]
    assert "strict_full_int8" in cfg["quant"]["ptq"]
    assert "require_tflm_compatible" in cfg["quant"]["ptq"]
    assert cfg["quant"]["ptq"].get("representative_source") in {"train", "test"}
    assert "accepted_integer_io_dtypes" in cfg["quant"]["ptq"]
    assert set(cfg["quant"]["ptq"]["accepted_integer_io_dtypes"]) >= {"int8", "uint8"}
    assert "qat" in cfg["quant"]
    assert cfg["quant"]["qat"].get("representative_source") in {"train", "test"}
    assert "accepted_integer_io_dtypes" in cfg["quant"]["qat"]
    assert set(cfg["quant"]["qat"]["accepted_integer_io_dtypes"]) >= {"int8", "uint8"}
    assert cfg["quant"]["qat"].get("strict_full_int8") is True
    assert cfg["quant"]["qat"].get("require_tflm_compatible") is True
    assert "deploy" in cfg


def test_smoke_config_ptq_strict_contract():
    cfg = load_yaml("configs/smoke.yaml")
    assert "quant" in cfg
    assert "ptq" in cfg["quant"]
    assert cfg["quant"]["ptq"].get("strict_full_int8") is True
    assert cfg["quant"]["ptq"].get("require_tflm_compatible") is True
    assert cfg["quant"]["ptq"].get("representative_source") == "train"
    assert set(cfg["quant"]["ptq"].get("accepted_integer_io_dtypes", [])) >= {"int8", "uint8"}
    assert "qat" in cfg["quant"]
    assert cfg["quant"]["qat"].get("strict_full_int8") is True
    assert cfg["quant"]["qat"].get("require_tflm_compatible") is True
    assert cfg["quant"]["qat"].get("representative_source") == "train"
    assert set(cfg["quant"]["qat"].get("accepted_integer_io_dtypes", [])) >= {"int8", "uint8"}
