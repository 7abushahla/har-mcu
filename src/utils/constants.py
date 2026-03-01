"""Project-wide constants."""

from __future__ import annotations

REQUIRED_WISDM_COLUMNS = ["user", "activity", "timestamp", "x-axis", "y-axis", "z-axis"]
AXIS_COLUMNS = ["x-axis", "y-axis", "z-axis"]

DEFAULT_CLASS_ORDER = [
    "Walking",
    "Jogging",
    "Upstairs",
    "Downstairs",
    "Sitting",
    "Standing",
]

SPLIT_PROTOCOLS = {"random_stratified", "user_holdout"}
LABEL_POLICIES = {"drop_cross_boundary", "majority_vote"}
