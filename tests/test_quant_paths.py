from __future__ import annotations

from src.utils.artifacts import (
    model_ckpt_path,
    model_ptq_tflite_path,
    model_qat_tflite_path,
    run_prefix,
)


def test_run_prefix_includes_model_protocol_and_run_id():
    prefix = run_prefix("tcn_inception", window_size=200, protocol="user_holdout", run_id="r1")
    assert "tcn_inception" in prefix
    assert "T200" in prefix
    assert "Puser_holdout" in prefix
    assert prefix.endswith("r1")


def test_model_specific_ptq_path_uses_model_name():
    p = model_ptq_tflite_path(
        "models_tflite",
        model_name="xtinyhar_student",
        window_size=200,
        protocol="random_stratified",
        run_id="wisdm_r0",
        variant="authorcal",
    )
    s = str(p)
    assert "xtinyhar_student" in s
    assert "ptq_int8_authorcal" in s


def test_model_specific_qat_path_uses_model_name():
    p = model_qat_tflite_path(
        "models_tflite",
        model_name="repmobile_folded",
        window_size=200,
        protocol="user_holdout",
        run_id="wisdm_r0",
        variant="traincal",
    )
    s = str(p)
    assert "repmobile_folded" in s
    assert s.endswith("_qat_traincal.tflite")


def test_model_checkpoint_path_is_not_deepconv_default_name():
    p = model_ckpt_path(
        "checkpoints",
        model_name="daghero_cnn_2layer",
        window_size=200,
        protocol="random_stratified",
        run_id="r0",
    )
    s = str(p)
    assert "daghero_cnn_2layer" in s
    assert s.endswith(".keras")
