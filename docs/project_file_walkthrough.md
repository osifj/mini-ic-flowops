# 项目文件逐个讲解

你不需要第一天看懂每一行代码，但必须知道每个文件夹是干什么的。

## 根目录

```text
mini-ic-flowops/
```

整个项目的根目录。运行命令时，通常要先进入这里。

## `START_HERE.md`

零基础入口。你不知道先看什么时，就打开它。

## `README.md`

项目总说明。它告诉你：

- 项目模拟什么岗位工作
- 怎么运行
- 目录结构是什么
- 最终要掌握什么

## `bin/`

命令入口目录。

### `bin/flowctl`

Linux 下的主命令入口。

它本身是 Shell 脚本，最后会调用：

```text
scripts/python/flowops/flowctl.py
```

### `bin/flowctl.ps1`

Windows PowerShell 入口。主要方便在 Windows 上临时验证。

实习和虚拟机练习时，重点看 `bin/flowctl`。

## `config/`

配置目录。

### `config/env.sh`

环境配置脚本。

运行：

```bash
source config/env.sh
```

它会设置：

```text
FLOWOPS_ROOT
PATH
```

### `config/ref_flow.yaml`

Reference Flow 配置。

它定义基础流程：

```text
precheck -> synth -> floorplan -> place -> route -> signoff -> report
```

### `config/testchip_flow.yaml`

Testchip Flow 配置。

它在基础流程后增加：

```text
ip_qa -> data_collect -> report
```

## `designs/`

设计输入目录。

### `designs/alu/`

示例 ALU IP。

里面有：

```text
README.md
ip.yaml
rtl/alu.v
constraints/alu.sdc
docs/interface.md
```

真实公司里的 IP 目录也会有类似结构，只是复杂很多。

### `designs/alu/rtl/alu.v`

Verilog RTL 文件。

你现在不需要精通 Verilog，只要知道它是设计输入。

### `designs/alu/constraints/alu.sdc`

时序约束文件。

真实 EDA flow 中，SDC 会告诉工具时钟周期、输入输出延迟等约束。

### `designs/alu/ip.yaml`

IP 元数据。

记录 IP 名字、版本、作者、顶层模块等信息。

QA 会检查它是否存在、是否有版本号。

## `scripts/`

脚本目录。

### `scripts/shell/`

Shell 小工具。

例如：

```text
show_latest_log.sh
```

它用于查看最新 run 的日志。

### `scripts/tcl/`

模拟 EDA Tcl 脚本。

包括：

```text
synth.tcl
floorplan.tcl
place.tcl
route.tcl
signoff.tcl
```

真实 EDA 工具常常用 Tcl 控制流程。

本项目用 Tcl 模拟这些步骤，并输出 `.rpt` 和 `.metrics`。

### `scripts/python/flowops/flowctl.py`

项目最核心的 Python 文件。

它负责：

- 解析命令行参数
- 读取 flow 配置
- 创建 run 目录
- 调用 Tcl 步骤
- 执行 IP QA
- 分析 testchip CSV
- 生成报告
- 记录 manifest
- 比较两次 run
- 搜索 docs

## `data/`

测试数据目录。

### `data/testchip_results.csv`

模拟 testchip 测试结果。

字段包括：

```text
chip_id, lot, wafer, die_x, die_y, ip_name, testcase, voltage, freq, result, fail_reason
```

Python 会读取它，统计良率和失败原因。

## `runs/`

每次运行的结果目录。

例如：

```text
runs/run_001/
```

它里面通常有：

```text
logs/flow.log
metrics/*.metrics
reports/*.rpt
reports/*.html
manifest.json
```

这就是一次 flow run 的完整记录。

## `reports/`

汇总报告和归档目录。

例如：

```text
reports/run_004.zip
reports/run_004_flow_report.html
```

## `docs/`

学习文档目录。

你现在最应该读：

```text
3_day_crash_plan.md
every_command_explained.md
project_file_walkthrough.md
code_reading_guide.md
final_self_test.md
```

## `Makefile`

快捷命令集合。

例如：

```bash
make testchip
```

等价于：

```bash
./bin/flowctl run --design alu --flow testchip
```

如果你还没学 Makefile，可以先不用它。

