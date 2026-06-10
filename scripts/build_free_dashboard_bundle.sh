#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-"$ROOT/outputs/free-dashboard-site"}"

mkdir -p "$OUT_DIR"
cp "$ROOT/docs/dashboard/welcome.html" "$OUT_DIR/index.html"
cp "$ROOT/docs/dashboard/free.html" "$OUT_DIR/dashboard.html"
cp "$ROOT/docs/dashboard/generated-dashboard-data.js" "$OUT_DIR/generated-dashboard-data.js"

echo "Built free dashboard bundle:"
echo "$OUT_DIR/index.html"
echo "$OUT_DIR/dashboard.html"
echo "$OUT_DIR/generated-dashboard-data.js"
