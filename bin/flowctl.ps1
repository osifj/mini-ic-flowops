$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$env:FLOWOPS_ROOT = $ProjectRoot

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    python3 "$ProjectRoot/scripts/python/flowops/flowctl.py" @args
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python "$ProjectRoot/scripts/python/flowops/flowctl.py" @args
}
else {
    Write-Error "未找到 python3 或 python。建议在 Linux 虚拟机中运行 ./bin/flowctl。"
}

