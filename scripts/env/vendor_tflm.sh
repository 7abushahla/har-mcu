#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/env/vendor_tflm.sh <tflm_commit>
# Example:
#   scripts/env/vendor_tflm.sh 5f9d9d6

COMMIT="${1:-5f9d9d6}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET_DIR="${ROOT_DIR}/third_party/tflite-micro"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

rm -rf "${TARGET_DIR}"
mkdir -p "${TARGET_DIR}"

git clone --depth 1 https://github.com/tensorflow/tflite-micro.git "${TMP_DIR}/repo"
cd "${TMP_DIR}/repo"

git fetch --depth 1 origin "${COMMIT}" || true
git checkout "${COMMIT}"

cp -R . "${TARGET_DIR}/"

echo "Vendored tflite-micro at commit ${COMMIT} into ${TARGET_DIR}"
