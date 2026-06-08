# Shell、Tcl、Python 分工

## Shell 适合做什么

Shell 像一个流程胶水。

本项目例子：

```bash
bin/flowctl
scripts/shell/show_latest_log.sh
```

Shell 常用于：

- 设置环境变量
- 调用工具
- 串联多个步骤
- 查看日志
- 简单文件操作

## Tcl 适合做什么

Tcl 在 EDA 里非常常见，因为很多工具内置 Tcl 命令。

本项目例子：

```text
scripts/tcl/synth.tcl
scripts/tcl/floorplan.tcl
scripts/tcl/place.tcl
scripts/tcl/route.tcl
scripts/tcl/signoff.tcl
```

真实公司里可能会看到类似：

```tcl
read_verilog ./rtl/top.v
create_clock -period 10 [get_ports clk]
compile
report_timing
```

## Python 适合做什么

Python 更适合复杂逻辑和数据处理。

本项目例子：

```text
scripts/python/flowops/flowctl.py
```

Python 常用于：

- 解析配置
- 生成报告
- 分析 CSV
- 做 QA 检查
- 管理 run 目录
- 记录 manifest

