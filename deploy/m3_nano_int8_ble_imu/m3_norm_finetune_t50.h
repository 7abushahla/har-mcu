/* Generated from norm_stats JSON — train_zscore mean/std on Arduino train split. */
/* Source: norm_stats_T50_Prandom_stratified.json */
#pragma once

#define WINDOW_SIZE 50
#define SAMPLE_RATE_HZ 20
#define APPLY_NORMALIZATION 1
#define UNIT_PRE_MULTIPLY 1.00000000f
#define UNIT_SCALE 1.00000000f

static constexpr float kNormMean[3] = {-0.15637834f, 0.03366828f, 0.07581268f};
static constexpr float kNormStd[3] = {0.16728248f, 0.18165129f, 0.12518984f};
static constexpr const char* kNormalizationMode = "train_zscore";
static constexpr const char* kUnitMode = "raw_no_conversion";
