# 代码阅读指南

你是零基础，不要第一天就从第 1 行读到最后 1 行。正确方式是按层次看。

## 第一层：Shell 入口

先看：

```bash
cat bin/flowctl
```

核心内容只有几行：

```bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export FLOWOPS_ROOT="$PROJECT_ROOT"
python3 "$PROJECT_ROOT/scripts/python/flowops/flowctl.py" "$@"
```

逐句解释：

- 找到项目根目录。
- 设置 `FLOWOPS_ROOT`。
- 调用 Python 主程序。
- `"$@"` 表示把你输入的参数原样传给 Python。

比如你输入：

```bash
flowctl run --design alu --flow testchip
```

Shell 最后会变成调用 Python：

```bash
python3 scripts/python/flowops/flowctl.py run --design alu --flow testchip
```

## 第二层：Python 命令分发

打开：

```text
scripts/python/flowops/flowctl.py
```

先找：

```text
build_parser()
```

它定义了有哪些命令：

```text
init
doctor
run
status
qa
report
compare
archive
ask
learn
clean
```

每个命令会对应一个函数。

例如：

```text
run -> cmd_run()
qa -> cmd_qa()
compare -> cmd_compare()
```

## 第三层：主流程 `cmd_run`

这是最重要的函数。

它做的事可以翻译成：

1. 找到设计目录，例如 `designs/alu`。
2. 找到 flow 配置，例如 `config/testchip_flow.yaml`。
3. 创建新的 run 目录，例如 `runs/run_001`。
4. 写入初始 `manifest.json`。
5. 按配置里的 steps 一个个执行。
6. 每步成功就记录 PASS。
7. 最后生成报告。
8. 如果出错，就写日志并把状态标成 FAIL。

你不需要马上懂所有 Python 语法，但要懂这个流程。

## 第四层：Tcl 步骤

Python 看到这些步骤：

```text
synth
floorplan
place
route
signoff
```

会调用：

```text
scripts/tcl/synth.tcl
scripts/tcl/floorplan.tcl
scripts/tcl/place.tcl
scripts/tcl/route.tcl
scripts/tcl/signoff.tcl
```

核心函数：

```text
run_tcl_step()
```

如果 Linux 里安装了 `tclsh`，它就真正执行 Tcl。

如果没安装，它就用 Python fallback 生成模拟报告。

这就是为什么你没有 Tcl 时也能跑通。

## 第五层：IP QA

核心函数：

```text
run_ip_qa()
```

它检查：

- `README.md`
- `ip.yaml`
- RTL 文件
- SDC 文件
- version 字段
- 空文件
- 硬编码绝对路径

输出：

```text
ip_qa_report.json
ip_qa_report.md
ip_qa_report.html
```

## 第六层：测试数据分析

核心函数：

```text
analyze_testchip_data()
```

它读取：

```text
data/testchip_results.csv
```

然后统计：

- 总测试数
- PASS 数
- FAIL 数
- 良率
- 哪个 IP 失败最多
- 哪个 testcase 失败最多
- 哪个 fail_reason 最多

## 第七层：报告生成

核心函数：

```text
build_report()
```

它汇总：

- manifest
- metrics
- IP QA
- testchip analysis

输出：

```text
flow_report.md
flow_report.html
```

## Tcl 脚本怎么看

以 `scripts/tcl/synth.tcl` 为例。

开头：

```tcl
set run_dir [lindex $argv 0]
set design_dir [lindex $argv 1]
set metrics_path [lindex $argv 2]
set report_path [lindex $argv 3]
```

意思：从命令行参数里拿到运行目录、设计目录、指标输出路径、报告输出路径。

写文件：

```tcl
set fp [open $metrics_path w]
puts $fp "step=synth"
puts $fp "cell_count=$cell_count"
close $fp
```

意思：打开 metrics 文件，写入指标，再关闭文件。

真实 EDA 工具里，这些模拟指标会被真实命令替换。

## 你看代码的顺序

按这个顺序：

1. `bin/flowctl`
2. `config/testchip_flow.yaml`
3. `scripts/python/flowops/flowctl.py` 里的 `build_parser`
4. `scripts/python/flowops/flowctl.py` 里的 `cmd_run`
5. `scripts/python/flowops/flowctl.py` 里的 `run_tcl_step`
6. `scripts/tcl/synth.tcl`
7. `scripts/python/flowops/flowctl.py` 里的 `run_ip_qa`
8. `scripts/python/flowops/flowctl.py` 里的 `analyze_testchip_data`

不要一上来读所有函数。先抓主线。

