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
    assert cfg["quant"]["qat"].get("device_preference") in {"cpu", "gpu"}
    assert cfg["quant"]["qat"].get("auto_fallback_to_cpu") in {True, False}
    assert "deploy" in cfg
    assert cfg["deploy"].get("allowed_ops_profile") in {
        "default",
        "minimal",
        "nano33ble_minimal",
        "nano33ble_extended",
        "extended",
    }
    assert cfg["deploy"].get("allowed_ops") is None or isinstance(cfg["deploy"].get("allowed_ops"), list)
    assert cfg.get("experiment", {}).get("compression_focus") == "ptq_qat_only"
    assert "paper_targets" in cfg.get("experiment", {})
    for key in ("fp32_accuracy", "ptq_accuracy", "qat_accuracy", "notes"):
        assert key in cfg["experiment"]["paper_targets"]
    assert cfg.get("augment", {}).get("accel_rotation", {}).get("enabled") is False
    assert cfg["augment"]["accel_rotation"].get("mode") in {
        "uniform_so3",
        "bounded_so3",
        "target_gravity",
    }
    assert 0.0 <= float(cfg["augment"]["accel_rotation"].get("probability")) <= 1.0
    assert cfg["augment"]["accel_rotation"].get("apply_in_qat") in {True, False}
    assert cfg.get("runtime", {}).get("run_mode") in {"sanity_check", "full_run"}
    assert cfg.get("runtime", {}).get("gpu_fallback_to_cpu") in {True, False}
    assert cfg.get("runtime", {}).get("fail_if_gpu_missing") in {True, False}
    stage_devices = cfg.get("runtime", {}).get("stage_devices", {})
    for mode in ("sanity_check", "full_run"):
        assert mode in stage_devices
        for stage in ("train", "eval_fp32", "ptq", "eval_ptq", "qat", "eval_qat"):
            assert stage in stage_devices[mode]
            assert stage_devices[mode][stage] in {"cpu", "gpu"}
    assert "eval" in cfg
    assert "tflite_timing" in cfg["eval"]
    assert cfg["eval"]["tflite_timing"]["enabled"] in {True, False}
    assert int(cfg["eval"]["tflite_timing"]["warmup_samples"]) >= 0
    assert int(cfg["eval"]["tflite_timing"]["timed_samples"]) >= 0


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
    assert cfg["quant"]["qat"].get("device_preference") in {"cpu", "gpu"}
    assert cfg["quant"]["qat"].get("auto_fallback_to_cpu") in {True, False}
    assert cfg["quant"]["qat"].get("representative_source") == "train"
    assert set(cfg["quant"]["qat"].get("accepted_integer_io_dtypes", [])) >= {"int8", "uint8"}
    assert cfg.get("experiment", {}).get("compression_focus") == "ptq_qat_only"
    assert "paper_targets" in cfg.get("experiment", {})
    for key in ("fp32_accuracy", "ptq_accuracy", "qat_accuracy", "notes"):
        assert key in cfg["experiment"]["paper_targets"]
    assert cfg.get("runtime", {}).get("run_mode") in {"sanity_check", "full_run"}
    assert "eval" in cfg and "tflite_timing" in cfg["eval"]
    assert cfg["deploy"].get("allowed_ops_profile") in {
        "default",
        "minimal",
        "nano33ble_minimal",
        "nano33ble_extended",
        "extended",
    }
    assert cfg["deploy"].get("allowed_ops") is None or isinstance(cfg["deploy"].get("allowed_ops"), list)


def test_nested_paper_config_resolves_paths_to_repo_root():
    cfg = load_yaml("configs/papers/xtinyhar_wisdm.yaml")
    assert "WISDM_ar_v1.1" in cfg["paths"]["raw_csv"]
    assert cfg["paths"]["raw_csv"].startswith("/")
    assert cfg["experiment"]["paper_slug"] == "xtinyhar"
    assert cfg["experiment"]["compression_focus"] == "ptq_qat_only"
    assert "paper_targets" in cfg["experiment"]
    for key in ("fp32_accuracy", "ptq_accuracy", "qat_accuracy", "notes"):
        assert key in cfg["experiment"]["paper_targets"]
    assert cfg["runtime"]["run_mode"] in {"sanity_check", "full_run"}
    assert "eval" in cfg and "tflite_timing" in cfg["eval"]
    assert "annotation_policy" in cfg["quant"]["qat"]
    assert cfg["quant"]["qat"].get("device_preference") in {"cpu", "gpu"}
    assert cfg["quant"]["qat"].get("auto_fallback_to_cpu") in {True, False}
    assert cfg["deploy"].get("allowed_ops_profile") in {
        "default",
        "minimal",
        "nano33ble_minimal",
        "nano33ble_extended",
        "extended",
    }
    assert cfg["deploy"].get("allowed_ops") is None or isinstance(cfg["deploy"].get("allowed_ops"), list)


def test_paper_configs_gpu_stage_routing_for_qat():
    paper_cfgs = [
        "configs/papers/xtinyhar_wisdm.yaml",
        "configs/papers/repmobile_wisdm.yaml",
        "configs/papers/tcn_attention_wisdm.yaml",
        "configs/papers/daghero_wisdm.yaml",
        "configs/papers/tcn_inception_wisdm.yaml",
    ]
    for cfg_path in paper_cfgs:
        cfg = load_yaml(cfg_path)
        stage_devices = cfg.get("runtime", {}).get("stage_devices", {})
        assert stage_devices["sanity_check"]["qat"] == "gpu"
        assert stage_devices["sanity_check"]["eval_qat"] == "gpu"
        assert stage_devices["full_run"]["qat"] == "gpu"
        assert stage_devices["full_run"]["eval_qat"] == "gpu"
        assert cfg["quant"]["qat"].get("device_preference") == "gpu"
        assert cfg["quant"]["qat"].get("auto_fallback_to_cpu") is True
        assert cfg["deploy"].get("allowed_ops_profile") == "nano33ble_extended"
