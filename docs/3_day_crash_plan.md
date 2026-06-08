# 3 到 5 天冲刺计划

这个计划按“零基础小白”设计。你不要跳着学，照着做就行。

## Day 1：只求跑通

目标：你能在 Linux 虚拟机里运行完整 testchip flow。

### 学什么

- 进入目录
- 给脚本加执行权限
- source 环境
- 运行 flow
- 查看 run 状态

### 操作

```bash
cd mini-ic-flowops
chmod +x bin/flowctl
source config/env.sh
flowctl doctor
flowctl run --design alu --flow testchip
flowctl status
```

### 看什么

```bash
ls runs
ls runs/run_001
ls runs/run_001/reports
tail -n 80 runs/run_001/logs/flow.log
```

如果你的 run 编号不是 `run_001`，就用 `flowctl status` 里最新的编号。

### 今天必须能回答

- 我在哪里运行命令？
- `flowctl doctor` 是检查什么？
- `flowctl run` 会生成什么目录？
- 日志在哪？
- 报告在哪？

今天不要求你看懂 Python/Tcl 代码。

## Day 2：看懂项目结构和流程

目标：知道每个目录是干什么的，知道 testchip flow 每一步在做什么。

### 先读

```text
docs/every_command_explained.md
docs/project_file_walkthrough.md
docs/flow_concepts.md
docs/shell_tcl_python_map.md
```

### 操作

打开 flow 配置：

```bash
cat config/testchip_flow.yaml
```

你会看到：

```text
precheck -> synth -> floorplan -> place -> route -> signoff -> ip_qa -> data_collect -> report
```

检查每一步输出：

```bash
ls runs/run_001/reports
ls runs/run_001/metrics
cat runs/run_001/manifest.json
```

### 今天必须能回答

- Reference Flow 和 Testchip Flow 有什么区别？
- `precheck` 检查什么？
- `synth/floorplan/place/route/signoff` 为什么用 Tcl 模拟？
- `ip_qa` 检查什么？
- `data_collect` 分析什么数据？
- `report` 生成什么？

## Day 3：看懂关键代码，不死磕细节

目标：能看懂项目是怎么串起来的。

### 先读

```text
docs/code_reading_guide.md
```

### 操作

先看 Shell 入口：

```bash
cat bin/flowctl
```

再看 Python 入口：

```bash
grep -n "def cmd_run" scripts/python/flowops/flowctl.py
grep -n "def run_tcl_step" scripts/python/flowops/flowctl.py
grep -n "def run_ip_qa" scripts/python/flowops/flowctl.py
grep -n "def analyze_testchip_data" scripts/python/flowops/flowctl.py
```

再看一个 Tcl：

```bash
cat scripts/tcl/synth.tcl
```

### 今天必须能回答

- `bin/flowctl` 最后调用了哪个 Python 文件？
- `cmd_run` 为什么是主流程？
- Python 如何调用 Tcl？
- 如果没有安装 `tclsh`，项目怎么继续跑？
- QA 报告是哪个函数生成的？

## Day 4：动手改一次

目标：你不是只会跑，还能做一个小改动并比较结果。

### 操作 1：跑一个基准

```bash
flowctl run --design alu --flow ref
flowctl status
```

记住这个 run 编号，比如 `run_002`。

### 操作 2：修改一个模拟指标

打开：

```text
scripts/tcl/signoff.tcl
```

把：

```tcl
set power_mw 2.7
```

改成：

```tcl
set power_mw 3.1
```

如果你当前没有安装 Tcl，Python fallback 还会使用内置指标。那就先只理解这个动作；装好 Tcl 后再看变化。

### 操作 3：再跑一次并比较

```bash
flowctl run --design alu --flow ref
flowctl compare run_002 run_003
```

把编号换成你自己的。

### 今天必须能回答

- 我改了哪个文件？
- 为什么重新跑会生成新的 run？
- `compare` 比较了什么？
- 为什么真实公司里必须保留历史 run？

## Day 5：最终自测和实习表达

目标：能把项目讲给导师或面试官听。

### 先读

```text
docs/final_self_test.md
docs/internship_speaking_notes.md
```

### 操作

```bash
flowctl qa --design alu
flowctl ask "IP QA 检查什么"
flowctl archive --run latest
```

### 今天必须能讲

用 1 分钟讲：

> 我做了一个 mini IC flow 自动化项目。它用 Shell 做命令入口，用 YAML 配置 Reference Flow/Testchip Flow，用 Tcl 模拟 EDA 工具步骤，用 Python 做流程编排、IP QA、测试数据分析、报告生成和版本追踪。每次运行都会生成 run 目录，里面有日志、metrics、reports 和 manifest，方便定位失败和比较结果。

