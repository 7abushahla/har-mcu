from __future__ import annotations

from contextlib import nullcontext

import pytest

from src.utils.device_runtime import (
    STAGES,
    resolve_run_mode,
    resolve_stage_device,
    runtime_device_report,
    stage_device_map,
    stage_device_scope,
)


class _FakeDevice:
    def __init__(self, name: str):
        self.name = name


class _FakeConfig:
    def __init__(self, gpu_count: int):
        self._gpus = [_FakeDevice(f"/physical_device:GPU:{i}") for i in range(gpu_count)]

    def list_physical_devices(self, kind: str):
        if kind.upper() == "GPU":
            return self._gpus
        return []


class _FakeTF:
    def __init__(self, gpu_count: int):
        self.config = _FakeConfig(gpu_count)
        self.entered_devices: list[str] = []

    def device(self, device_name: str):
        self.entered_devices.append(device_name)
        return nullcontext()


def _cfg(run_mode: str = "sanity_check", *, fallback: bool = True, fail_if_gpu_missing: bool = False):
    return {
        "runtime": {
            "run_mode": run_mode,
            "gpu_fallback_to_cpu": fallback,
            "fail_if_gpu_missing": fail_if_gpu_missing,
        }
    }


def test_sanity_check_uses_gpu_for_non_qat_when_available():
    cfg = _cfg("sanity_check")
    fake_tf = _FakeTF(gpu_count=1)

    assert resolve_stage_device(cfg, "train", fake_tf) == "gpu"
    assert resolve_stage_device(cfg, "eval_fp32", fake_tf) == "gpu"
    assert resolve_stage_device(cfg, "ptq", fake_tf) == "gpu"
    assert resolve_stage_device(cfg, "qat", fake_tf) == "cpu"
    assert resolve_stage_device(cfg, "eval_qat", fake_tf) == "cpu"


def test_full_run_forces_cpu_for_all_stages_even_with_gpu():
    cfg = _cfg("full_run")
    fake_tf = _FakeTF(gpu_count=2)
    mapping = stage_device_map(cfg, "full_run")
    assert set(mapping) == set(STAGES)
    for stage in STAGES:
        assert resolve_stage_device(cfg, stage, fake_tf) == "cpu"


def test_sanity_check_falls_back_to_cpu_when_gpu_missing():
    cfg = _cfg("sanity_check", fallback=True, fail_if_gpu_missing=False)
    fake_tf = _FakeTF(gpu_count=0)
    assert resolve_stage_device(cfg, "train", fake_tf) == "cpu"
    assert resolve_stage_device(cfg, "ptq", fake_tf) == "cpu"
    assert resolve_stage_device(cfg, "qat", fake_tf) == "cpu"


def test_missing_gpu_raises_when_fail_flag_enabled():
    cfg = _cfg("sanity_check", fallback=True, fail_if_gpu_missing=True)
    fake_tf = _FakeTF(gpu_count=0)
    with pytest.raises(RuntimeError, match="requested GPU"):
        resolve_stage_device(cfg, "train", fake_tf)


def test_invalid_run_mode_and_stage_raise_clear_errors():
    with pytest.raises(ValueError, match="Unsupported runtime.run_mode"):
        resolve_run_mode(_cfg("bad_mode"))

    with pytest.raises(ValueError, match="Unknown runtime stage"):
        resolve_stage_device(_cfg("sanity_check"), "bad_stage", _FakeTF(gpu_count=1))


def test_runtime_device_report_and_scope_expose_selected_devices():
    cfg = _cfg("sanity_check")
    fake_tf = _FakeTF(gpu_count=1)
    report = runtime_device_report(cfg, tf_module=fake_tf)

    assert report["run_mode"] == "sanity_check"
    assert report["gpu_available"] is True
    assert report["resolved_stage_devices"]["train"] == "gpu"
    assert report["resolved_stage_devices"]["qat"] == "cpu"

    with stage_device_scope(cfg, "train", tf_module=fake_tf):
        pass
    with stage_device_scope(cfg, "qat", tf_module=fake_tf):
        pass
    assert fake_tf.entered_devices[-2:] == ["/GPU:0", "/CPU:0"]


def test_runtime_stage_overrides_can_enable_gpu_for_qat_in_full_run():
    cfg = {
        "runtime": {
            "run_mode": "full_run",
            "gpu_fallback_to_cpu": True,
            "fail_if_gpu_missing": False,
            "stage_devices": {
                "full_run": {
                    "train": "gpu",
                    "eval_fp32": "gpu",
                    "ptq": "gpu",
                    "eval_ptq": "gpu",
                    "qat": "gpu",
                    "eval_qat": "gpu",
                }
            },
        }
    }
    fake_tf = _FakeTF(gpu_count=1)
    report = runtime_device_report(cfg, tf_module=fake_tf)
    assert report["run_mode"] == "full_run"
    for stage in STAGES:
        assert report["resolved_stage_devices"][stage] == "gpu"
