from __future__ import annotations

from src.utils.artifacts import ptq_tflite_path, qat_tflite_path


def test_variant_paths_do_not_overwrite_default_artifacts():
    base_ptq = str(ptq_tflite_path("models_tflite", 100, "random_stratified"))
    train_ptq = str(ptq_tflite_path("models_tflite", 100, "random_stratified", variant="traincal"))
    author_ptq = str(ptq_tflite_path("models_tflite", 100, "random_stratified", variant="authorcal"))

    assert base_ptq != train_ptq
    assert base_ptq != author_ptq
    assert train_ptq != author_ptq
    assert train_ptq.endswith("_traincal.tflite")
    assert author_ptq.endswith("_authorcal.tflite")

    base_qat = str(qat_tflite_path("models_tflite", 100, "random_stratified"))
    train_qat = str(qat_tflite_path("models_tflite", 100, "random_stratified", variant="traincal"))
    author_qat = str(qat_tflite_path("models_tflite", 100, "random_stratified", variant="authorcal"))

    assert base_qat != train_qat
    assert base_qat != author_qat
    assert train_qat != author_qat
    assert train_qat.endswith("_traincal.tflite")
    assert author_qat.endswith("_authorcal.tflite")
