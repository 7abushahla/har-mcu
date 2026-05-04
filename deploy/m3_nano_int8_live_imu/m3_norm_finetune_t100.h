/* Generated from norm_stats JSON — train_zscore mean/std on Arduino train split. */
/* Source: norm_stats_T100_Prandom_stratified.json */
#pragma once

#define WINDOW_SIZE 100
#define SAMPLE_RATE_HZ 20
#define APPLY_NORMALIZATION 1
#define UNIT_PRE_MULTIPLY 1.00000000f
#define UNIT_SCALE 1.00000000f

static constexpr float kNormMean[3] = {-0.15676919f, 0.03439229f, 0.07540476f};
static constexpr float kNormStd[3] = {0.16741748f, 0.18228361f, 0.12568961f};
static constexpr const char* kNormalizationMode = "train_zscore";
static constexpr const char* kUnitMode = "raw_no_conversion";
