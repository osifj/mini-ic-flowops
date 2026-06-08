#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(os.environ.get("FLOWOPS_ROOT", Path(__file__).resolve().parents[3])).resolve()
CONFIG_DIR = ROOT / "config"
DESIGNS_DIR = ROOT / "designs"
RUNS_DIR = ROOT / "runs"
REPORTS_DIR = ROOT / "reports"
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
TCL_DIR = ROOT / "scripts" / "tcl"

TCL_STEPS = {"synth", "floorplan", "place", "route", "signoff"}

FALLBACK_METRICS = {
    "synth": {
        "rtl_files": 1,
        "cell_count": 137,
        "area_um2": 856.25,
        "wns_ns": 0.18,
    },
    "floorplan": {
        "die_width_um": 1000,
        "die_height_um": 1000,
        "core_utilization": 0.62,
        "macro_count": 0,
    },
    "place": {
        "placed_instances": 137,
        "congestion_score": 0.21,
        "hpwl_um": 4200,
    },
    "route": {
        "routed_nets": 86,
        "drc_violations": 0,
        "antenna_violations": 0,
    },
    "signoff": {
        "setup_wns_ns": 0.11,
        "hold_wns_ns": 0.04,
        "lvs_errors": 0,
        "drc_errors": 0,
        "power_mw": 2.7,
    },
}


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs() -> None:
    for path in [RUNS_DIR, REPORTS_DIR, ROOT / "work"]:
        path.mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def print_ok(message: str) -> None:
    print(f"[OK] {message}")


def print_warn(message: str) -> None:
    print(f"[WARN] {message}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_simple_yaml(path: Path) -> dict:
    data: dict[str, object] = {}
    current_key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            if current_key is None:
                raise ValueError(f"YAML 列表项没有所属 key: {path}:{raw}")
            data.setdefault(current_key, [])
            assert isinstance(data[current_key], list)
            data[current_key].append(line[2:].strip().strip('"'))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if not value:
                data[key] = []
                current_key = key
            else:
                data[key] = value.strip('"')
                current_key = None
            continue
        raise ValueError(f"无法解析 YAML 行: {path}:{raw}")
    return data


def run_command(command: list[str], input_text: str | None = None) -> tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=ROOT,
            check=False,
        )
        return result.returncode, result.stdout.strip()
    except FileNotFoundError:
        return 127, "command not found"


def git_commit() -> str:
    code, out = run_command(["git", "rev-parse", "--short", "HEAD"])
    if code == 0:
        return out
    return "not-a-git-repo"


def tool_versions() -> dict:
    versions = {}
    for name, command in {
        "python3": ["python3", "--version"],
        "git": ["git", "--version"],
        "tclsh": ["tclsh"],
    }.items():
        if name == "tclsh":
            code, out = run_command(command, "puts [info patchlevel]\n")
        else:
            code, out = run_command(command)
        versions[name] = out if code == 0 else "missing"
    return versions


def next_run_id() -> str:
    existing = []
    for path in RUNS_DIR.glob("run_*"):
        match = re.fullmatch(r"run_(\d+)", path.name)
        if match:
            existing.append(int(match.group(1)))
    return f"run_{(max(existing) + 1) if existing else 1:03d}"


def latest_run_dir() -> Path:
    runs = sorted([p for p in RUNS_DIR.glob("run_*") if p.is_dir()])
    if not runs:
        raise SystemExit("还没有任何 run。请先执行：flowctl run --design alu --flow ref")
    return runs[-1]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def append_log(run_dir: Path, message: str) -> None:
    log_path = run_dir / "logs" / "flow.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"[{now()}] {message}\n")


def write_metrics(path: Path, step: str, metrics: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(f"step={step}\n")
        for key, value in metrics.items():
            fh.write(f"{key}={value}\n")


def read_metrics(path: Path) -> dict:
    data = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        data[key] = parse_value(value)
    return data


def parse_value(value: str):
    value = value.strip()
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def collect_run_metrics(run_dir: Path) -> dict:
    metrics = {}
    for path in sorted((run_dir / "metrics").glob("*.metrics")):
        data = read_metrics(path)
        step = str(data.get("step", path.stem))
        metrics[step] = data
    return metrics


def collect_input_manifest(design_dir: Path, flow_config: Path) -> dict:
    files = []
    for base in [design_dir, flow_config]:
        if base.is_file():
            files.append({"path": rel(base), "sha256": sha256_file(base)})
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file():
                files.append({"path": rel(path), "sha256": sha256_file(path)})
    return {"files": files}


def cmd_init(_args: argparse.Namespace) -> int:
    ensure_dirs()
    print_ok("项目目录已就绪")
    print("建议在 Linux 中执行：source config/env.sh")
    print("然后执行：flowctl doctor")
    return 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    ensure_dirs()
    print(f"项目根目录: {ROOT}")
    versions = tool_versions()
    for name, version in versions.items():
        if version == "missing":
            print_warn(f"{name} 未找到")
        else:
            print_ok(f"{name}: {version}")
    if versions.get("tclsh") == "missing":
        print_warn("没有 tclsh 也能跑通；但建议在 Linux 虚拟机安装 tcl 来练真实 Tcl 执行。")
    return 0


def design_dir(name: str) -> Path:
    path = DESIGNS_DIR / name
    if not path.exists():
        raise SystemExit(f"找不到设计：{name}，期望目录：{path}")
    return path


def flow_config_path(flow: str) -> Path:
    candidates = [
        CONFIG_DIR / f"{flow}_flow.yaml",
        CONFIG_DIR / f"{flow}.yaml",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise SystemExit(f"找不到 flow 配置：{flow}。可选示例：ref、testchip")


def precheck(design: Path, run_dir: Path) -> None:
    checks = []
    rtl_files = list((design / "rtl").glob("*.v"))
    sdc_files = list((design / "constraints").glob("*.sdc"))
    checks.append(("RTL 文件存在", bool(rtl_files), f"发现 {len(rtl_files)} 个 .v 文件"))
    checks.append(("SDC 约束存在", bool(sdc_files), f"发现 {len(sdc_files)} 个 .sdc 文件"))
    checks.append(("IP 元数据存在", (design / "ip.yaml").exists(), "需要 ip.yaml"))
    checks.append(("README 存在", (design / "README.md").exists(), "需要 README.md"))

    failed = [name for name, ok, _ in checks if not ok]
    report = ["# Precheck Report", ""]
    for name, ok, detail in checks:
        report.append(f"- {'PASS' if ok else 'FAIL'}: {name} - {detail}")

    report_path = run_dir / "reports" / "precheck.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    write_json(
        run_dir / "reports" / "precheck.json",
        [{"name": name, "status": "PASS" if ok else "FAIL", "detail": detail} for name, ok, detail in checks],
    )
    append_log(run_dir, f"precheck report: {rel(report_path)}")

    if failed:
        raise RuntimeError("precheck 失败：" + ", ".join(failed))


def run_tcl_step(step: str, design: Path, run_dir: Path) -> None:
    metrics_path = run_dir / "metrics" / f"{step}.metrics"
    report_path = run_dir / "reports" / f"{step}.rpt"
    script_path = TCL_DIR / f"{step}.tcl"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    if shutil.which("tclsh") and script_path.exists():
        command = ["tclsh", str(script_path), str(run_dir), str(design), str(metrics_path), str(report_path)]
        append_log(run_dir, f"run Tcl: {' '.join(command)}")
        code, out = run_command(command)
        if out:
            append_log(run_dir, out)
        if code != 0:
            raise RuntimeError(f"{step} Tcl 执行失败，退出码 {code}")
        return

    metrics = FALLBACK_METRICS[step]
    write_metrics(metrics_path, step, metrics)
    lines = [
        f"{step.upper()} REPORT",
        "Tcl 没有安装，当前使用 Python fallback 模拟结果。",
        f"Design dir: {design}",
        "",
    ]
    lines.extend([f"{key}: {value}" for key, value in metrics.items()])
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    append_log(run_dir, f"{step}: tclsh missing, used Python fallback")


def run_ip_qa(design: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []

    def add(name: str, status: str, detail: str) -> None:
        results.append({"check": name, "status": status, "detail": detail})

    add("README.md", "PASS" if (design / "README.md").exists() else "FAIL", "IP 说明文档")
    add("ip.yaml", "PASS" if (design / "ip.yaml").exists() else "FAIL", "IP 元数据文件")
    rtl_files = list((design / "rtl").glob("*.v"))
    add("RTL files", "PASS" if rtl_files else "FAIL", f"发现 {len(rtl_files)} 个 Verilog 文件")
    sdc_files = list((design / "constraints").glob("*.sdc"))
    add("SDC constraints", "PASS" if sdc_files else "WARN", f"发现 {len(sdc_files)} 个约束文件")

    ip_text = (design / "ip.yaml").read_text(encoding="utf-8") if (design / "ip.yaml").exists() else ""
    add("version field", "PASS" if "version:" in ip_text else "FAIL", "ip.yaml 需要 version 字段")

    empty_files = [rel(path) for path in design.rglob("*") if path.is_file() and path.stat().st_size == 0]
    add("no empty files", "PASS" if not empty_files else "WARN", ", ".join(empty_files) or "没有空文件")

    absolute_hits = []
    abs_pattern = re.compile(r"([A-Za-z]:\\|/home/|/mnt/|/eda/|/tools/)")
    for path in design.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".v", ".sdc", ".yaml", ".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if abs_pattern.search(text):
            absolute_hits.append(rel(path))
    add("no hard-coded absolute paths", "PASS" if not absolute_hits else "WARN", ", ".join(absolute_hits) or "没有硬编码绝对路径")

    fail_count = sum(1 for item in results if item["status"] == "FAIL")
    warn_count = sum(1 for item in results if item["status"] == "WARN")
    summary = {
        "design": design.name,
        "status": "FAIL" if fail_count else "WARN" if warn_count else "PASS",
        "fail_count": fail_count,
        "warn_count": warn_count,
        "results": results,
    }

    write_json(output_dir / "ip_qa_report.json", summary)
    md = ["# IP QA Report", "", f"- Design: `{design.name}`", f"- Status: **{summary['status']}**", ""]
    md.append("| Check | Status | Detail |")
    md.append("| --- | --- | --- |")
    for item in results:
        md.append(f"| {item['check']} | {item['status']} | {item['detail']} |")
    (output_dir / "ip_qa_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    rows = "\n".join(
        f"<tr><td>{html.escape(item['check'])}</td><td>{item['status']}</td><td>{html.escape(item['detail'])}</td></tr>"
        for item in results
    )
    page = f"""<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<title>IP QA Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.6; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; }}
th {{ background: #f3f3f3; }}
</style>
<h1>IP QA Report</h1>
<p>Design: <code>{html.escape(design.name)}</code></p>
<p>Status: <strong>{summary['status']}</strong></p>
<table>
<tr><th>Check</th><th>Status</th><th>Detail</th></tr>
{rows}
</table>
</html>
"""
    (output_dir / "ip_qa_report.html").write_text(page, encoding="utf-8")
    return summary


def analyze_testchip_data(run_dir: Path) -> dict:
    csv_path = DATA_DIR / "testchip_results.csv"
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    total = len(rows)
    pass_count = sum(1 for row in rows if row["result"] == "PASS")
    fail_rows = [row for row in rows if row["result"] != "PASS"]
    by_ip = Counter(row["ip_name"] for row in fail_rows)
    by_testcase = Counter(row["testcase"] for row in fail_rows)
    by_reason = Counter(row["fail_reason"] for row in fail_rows if row["fail_reason"])
    summary = {
        "total": total,
        "pass_count": pass_count,
        "fail_count": len(fail_rows),
        "yield": round(pass_count / total, 4) if total else 0,
        "fail_by_ip": dict(by_ip.most_common()),
        "fail_by_testcase": dict(by_testcase.most_common()),
        "fail_by_reason": dict(by_reason.most_common()),
    }
    out_dir = run_dir / "reports"
    write_json(out_dir / "testchip_analysis.json", summary)

    md = [
        "# Testchip Data Analysis",
        "",
        f"- Total tests: {summary['total']}",
        f"- Pass: {summary['pass_count']}",
        f"- Fail: {summary['fail_count']}",
        f"- Yield: {summary['yield']:.2%}",
        "",
        "## Failures by IP",
    ]
    for key, value in by_ip.most_common():
        md.append(f"- {key}: {value}")
    md.append("")
    md.append("## Failures by Testcase")
    for key, value in by_testcase.most_common():
        md.append(f"- {key}: {value}")
    md.append("")
    md.append("## Failures by Reason")
    for key, value in by_reason.most_common():
        md.append(f"- {key}: {value}")
    (out_dir / "testchip_analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    append_log(run_dir, f"testchip analysis: yield={summary['yield']:.2%}")
    return summary


def build_report(run_dir: Path) -> Path:
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    metrics = collect_run_metrics(run_dir)
    qa_path = run_dir / "reports" / "ip_qa_report.json"
    qa = json.loads(qa_path.read_text(encoding="utf-8")) if qa_path.exists() else None
    testchip_path = run_dir / "reports" / "testchip_analysis.json"
    testchip = json.loads(testchip_path.read_text(encoding="utf-8")) if testchip_path.exists() else None

    md = [
        f"# Flow Report: {run_dir.name}",
        "",
        f"- Status: **{manifest.get('status', 'UNKNOWN')}**",
        f"- Design: `{manifest.get('design', 'unknown')}`",
        f"- Flow: `{manifest.get('flow', 'unknown')}`",
        f"- Git commit: `{manifest.get('git_commit', 'unknown')}`",
        "",
        "## Step Metrics",
    ]
    for step, values in metrics.items():
        md.append(f"### {step}")
        for key, value in values.items():
            if key != "step":
                md.append(f"- {key}: {value}")
        md.append("")

    if qa:
        md.extend(["## IP QA", "", f"- Status: {qa['status']}", f"- FAIL: {qa['fail_count']}", f"- WARN: {qa['warn_count']}", ""])
    if testchip:
        md.extend([
            "## Testchip Analysis",
            "",
            f"- Total tests: {testchip['total']}",
            f"- Yield: {testchip['yield']:.2%}",
            f"- Fail by IP: {testchip['fail_by_ip']}",
            "",
        ])

    report_md = run_dir / "reports" / "flow_report.md"
    report_md.write_text("\n".join(md), encoding="utf-8")

    metric_rows = []
    for step, values in metrics.items():
        for key, value in values.items():
            if key != "step":
                metric_rows.append(
                    f"<tr><td>{html.escape(step)}</td><td>{html.escape(key)}</td><td>{html.escape(str(value))}</td></tr>"
                )
    qa_block = ""
    if qa:
        qa_block = f"<h2>IP QA</h2><p>Status: <strong>{qa['status']}</strong>, FAIL: {qa['fail_count']}, WARN: {qa['warn_count']}</p>"
    testchip_block = ""
    if testchip:
        testchip_block = f"<h2>Testchip Analysis</h2><p>Yield: <strong>{testchip['yield']:.2%}</strong>, Fail by IP: {html.escape(str(testchip['fail_by_ip']))}</p>"
    html_page = f"""<!doctype html>
<html lang="zh-CN">
<meta charset="utf-8">
<title>Flow Report {html.escape(run_dir.name)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.6; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
th, td {{ border: 1px solid #ddd; padding: 8px; }}
th {{ background: #f3f3f3; }}
code {{ background: #f6f6f6; padding: 2px 4px; }}
</style>
<h1>Flow Report: {html.escape(run_dir.name)}</h1>
<p>Status: <strong>{html.escape(str(manifest.get('status', 'UNKNOWN')))}</strong></p>
<p>Design: <code>{html.escape(str(manifest.get('design', 'unknown')))}</code></p>
<p>Flow: <code>{html.escape(str(manifest.get('flow', 'unknown')))}</code></p>
<h2>Step Metrics</h2>
<table>
<tr><th>Step</th><th>Metric</th><th>Value</th></tr>
{''.join(metric_rows)}
</table>
{qa_block}
{testchip_block}
</html>
"""
    report_html = run_dir / "reports" / "flow_report.html"
    report_html.write_text(html_page, encoding="utf-8")
    REPORTS_DIR.mkdir(exist_ok=True)
    shutil.copy2(report_html, REPORTS_DIR / f"{run_dir.name}_flow_report.html")
    return report_html


def cmd_run(args: argparse.Namespace) -> int:
    ensure_dirs()
    design = design_dir(args.design)
    config_path = flow_config_path(args.flow)
    flow = load_simple_yaml(config_path)
    steps = flow.get("steps", [])
    if not isinstance(steps, list) or not steps:
        raise SystemExit(f"flow 配置没有 steps: {config_path}")

    run_id = next_run_id()
    run_dir = RUNS_DIR / run_id
    for child in ["logs", "reports", "metrics", "outputs"]:
        (run_dir / child).mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": run_id,
        "status": "RUNNING",
        "design": args.design,
        "flow": args.flow,
        "flow_config": rel(config_path),
        "start_time": now(),
        "end_time": None,
        "git_commit": git_commit(),
        "tool_versions": tool_versions(),
        "inputs": collect_input_manifest(design, config_path),
        "steps": [],
    }
    write_json(run_dir / "manifest.json", manifest)
    append_log(run_dir, f"start run: design={args.design}, flow={args.flow}")

    try:
        for step in steps:
            step_start = time.time()
            append_log(run_dir, f"step start: {step}")
            if step == "precheck":
                precheck(design, run_dir)
            elif step in TCL_STEPS:
                run_tcl_step(step, design, run_dir)
            elif step == "ip_qa":
                run_ip_qa(design, run_dir / "reports")
            elif step == "data_collect":
                analyze_testchip_data(run_dir)
            elif step == "report":
                build_report(run_dir)
            else:
                raise RuntimeError(f"未知步骤：{step}")
            elapsed = round(time.time() - step_start, 3)
            manifest["steps"].append({"name": step, "status": "PASS", "seconds": elapsed})
            write_json(run_dir / "manifest.json", manifest)
            append_log(run_dir, f"step pass: {step}, seconds={elapsed}")
        manifest["status"] = "PASS"
        append_log(run_dir, "run completed: PASS")
        print_ok(f"运行完成：{run_id}")
        print(f"日志：{rel(run_dir / 'logs' / 'flow.log')}")
        print(f"报告：{rel(run_dir / 'reports' / 'flow_report.html')}")
        return 0
    except Exception as exc:
        manifest["status"] = "FAIL"
        manifest["error"] = str(exc)
        append_log(run_dir, f"run failed: {exc}")
        print(f"[FAIL] {run_id}: {exc}")
        print(f"请查看日志：{rel(run_dir / 'logs' / 'flow.log')}")
        return 1
    finally:
        manifest["end_time"] = now()
        write_json(run_dir / "manifest.json", manifest)


def cmd_status(_args: argparse.Namespace) -> int:
    runs = sorted([p for p in RUNS_DIR.glob("run_*") if p.is_dir()])
    if not runs:
        print("还没有 run。执行：flowctl run --design alu --flow ref")
        return 0
    print("Run ID    Status   Design   Flow      Start Time")
    print("------    ------   ------   ----      ----------")
    for run_dir in runs:
        manifest_path = run_dir / "manifest.json"
        if not manifest_path.exists():
            print(f"{run_dir.name:<9} UNKNOWN")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(
            f"{run_dir.name:<9} {manifest.get('status', 'UNKNOWN'):<8} "
            f"{manifest.get('design', ''):<8} {manifest.get('flow', ''):<9} "
            f"{manifest.get('start_time', '')}"
        )
    return 0


def cmd_qa(args: argparse.Namespace) -> int:
    ensure_dirs()
    design = design_dir(args.design)
    out_dir = REPORTS_DIR / f"{args.design}_standalone_ip_qa"
    summary = run_ip_qa(design, out_dir)
    print_ok(f"QA 完成：{summary['status']}")
    print(f"报告：{rel(out_dir / 'ip_qa_report.html')}")
    return 0 if summary["status"] != "FAIL" else 1


def resolve_run(name: str | None) -> Path:
    if not name or name == "latest":
        return latest_run_dir()
    path = RUNS_DIR / name
    if not path.exists():
        raise SystemExit(f"找不到 run：{name}")
    return path


def cmd_report(args: argparse.Namespace) -> int:
    run_dir = resolve_run(args.run)
    report = build_report(run_dir)
    print_ok(f"报告已生成：{rel(report)}")
    return 0


def flatten_metrics(metrics: dict) -> dict:
    flat = {}
    for step, values in metrics.items():
        for key, value in values.items():
            if key != "step":
                flat[f"{step}.{key}"] = value
    return flat


def cmd_compare(args: argparse.Namespace) -> int:
    run_a = resolve_run(args.run_a)
    run_b = resolve_run(args.run_b)
    a = flatten_metrics(collect_run_metrics(run_a))
    b = flatten_metrics(collect_run_metrics(run_b))
    keys = sorted(set(a) | set(b))
    print(f"Compare: {run_a.name} vs {run_b.name}")
    print("Metric                         A              B              Delta")
    print("------                         -              -              -----")
    for key in keys:
        av = a.get(key, "")
        bv = b.get(key, "")
        delta = ""
        if isinstance(av, (int, float)) and isinstance(bv, (int, float)):
            delta = round(bv - av, 4)
        print(f"{key:<30} {str(av):<14} {str(bv):<14} {delta}")
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    run_dir = resolve_run(args.run)
    archive = REPORTS_DIR / f"{run_dir.name}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in run_dir.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(ROOT))
    print_ok(f"归档完成：{rel(archive)}")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    query = " ".join(args.query).strip()
    if not query:
        raise SystemExit("请输入问题，例如：flowctl ask 怎么看日志")
    words = build_search_terms(query)
    matches = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        score = sum(lowered.count(word) * (5 if len(word) > 1 else 1) for word in words)
        if score:
            first_line = next((line.strip() for line in text.splitlines() if line.strip()), path.name)
            matches.append((score, path, first_line))
    if not matches:
        print("没有找到匹配文档。可以先读 docs/00_read_me_first.md")
        return 0
    for score, path, title in sorted(matches, reverse=True)[:5]:
        print(f"- {rel(path)}  score={score}  {title}")
    return 0


def build_search_terms(query: str) -> list[str]:
    terms: set[str] = set()
    stop_chars = set("怎么如何查看看一个一下的了呢吗")
    for token in re.findall(r"[\w\u4e00-\u9fff]+", query.lower()):
        terms.add(token)
        if re.search(r"[\u4e00-\u9fff]", token):
            for index in range(len(token) - 1):
                pair = token[index : index + 2]
                if not any(char in stop_chars for char in pair):
                    terms.add(pair)
    return sorted(terms, key=lambda item: (-len(item), item))


def cmd_clean(args: argparse.Namespace) -> int:
    targets = [RUNS_DIR, REPORTS_DIR / "alu_standalone_ip_qa"]
    if not args.yes:
        print("这是清理命令。为了避免误删，默认只预览：")
        for target in targets:
            print(f"- {target}")
        print("确认要清理时再执行：flowctl clean --yes")
        return 0
    for run_dir in RUNS_DIR.glob("run_*"):
        shutil.rmtree(run_dir)
    standalone = REPORTS_DIR / "alu_standalone_ip_qa"
    if standalone.exists():
        shutil.rmtree(standalone)
    print_ok("已清理生成的 run 和 standalone QA 报告")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flowctl",
        description="mini-ic-flowops: IC 流程自动化练习工具",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="初始化项目目录")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("doctor", help="检查 Linux/Python/Tcl/Git 环境")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("run", help="运行一个 flow")
    p.add_argument("--design", default="alu", help="设计名称，默认 alu")
    p.add_argument("--flow", default="ref", help="flow 名称：ref 或 testchip")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("status", help="查看 run 列表")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("qa", help="单独运行 IP QA")
    p.add_argument("--design", default="alu")
    p.set_defaults(func=cmd_qa)

    p = sub.add_parser("report", help="重新生成某个 run 的报告")
    p.add_argument("--run", default="latest")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("compare", help="比较两个 run 的指标")
    p.add_argument("run_a")
    p.add_argument("run_b")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("archive", help="把 run 打包成 zip")
    p.add_argument("--run", default="latest")
    p.set_defaults(func=cmd_archive)

    p = sub.add_parser("ask", help="在 docs 中做关键词检索")
    p.add_argument("query", nargs="+")
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("clean", help="清理生成结果")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_clean)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
