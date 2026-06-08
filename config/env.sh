#!/usr/bin/env bash

# 用法：
#   source config/env.sh
#
# 这类文件在真实公司环境里很常见，用来设置工具路径、license 路径、项目路径等。

export FLOWOPS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$FLOWOPS_ROOT/bin:$PATH"

echo "FLOWOPS_ROOT=$FLOWOPS_ROOT"
echo "flowctl 已加入 PATH，可以直接运行：flowctl doctor"

