#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LATEST_RUN="$(find "$PROJECT_ROOT/runs" -maxdepth 1 -type d -name 'run_*' | sort | tail -n 1)"

if [[ -z "${LATEST_RUN:-}" ]]; then
    echo "还没有 run。先执行：flowctl run --design alu --flow ref"
    exit 1
fi

tail -n 80 "$LATEST_RUN/logs/flow.log"

