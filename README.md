# mini-ic-flowops

这是一个面向零基础实习准备的 IC 流程自动化练习项目。

它模拟岗位截图里的几类工作：

- Linux 工作环境配置
- Shell 脚本入口和流程串联
- Tcl 脚本模拟 EDA 工具流程
- Python 做 QA、测试数据分析和报告生成
- Git/版本信息记录
- Reference Flow / Testchip Flow 自动化
- 简单的内部文档检索助手

本项目不包含真实公司数据、真实 PDK 或商业 EDA 工具。它的目标是让你先学会“工作方式”。

## 你现在怎么用

在 Linux 虚拟机或 WSL 里进入本目录：

```bash
cd mini-ic-flowops
chmod +x bin/flowctl
./bin/flowctl doctor
./bin/flowctl init
./bin/flowctl run --design alu --flow ref
./bin/flowctl run --design alu --flow testchip
./bin/flowctl status
./bin/flowctl qa --design alu
./bin/flowctl compare run_001 run_002
./bin/flowctl ask "怎么看日志"
```

如果 Linux 里没有 Tcl，可以先跑通项目；程序会用 Python 内置模拟器代替 Tcl。之后建议安装 Tcl：

```bash
sudo apt update
sudo apt install -y tcl git make
```

Rocky/CentOS 系：

```bash
sudo dnf install -y tcl git make
```

## 先读哪几个文档

建议顺序：

1. `docs/00_read_me_first.md`
2. `docs/env_setup.md`
3. `docs/linux_basics.md`
4. `docs/flow_concepts.md`
5. `docs/shell_tcl_python_map.md`
6. `docs/internship_playbook.md`

## 项目结构

```text
mini-ic-flowops/
  bin/                 命令入口
  config/              flow 配置
  designs/             示例 IP/设计数据
  scripts/shell/       Shell 小工具
  scripts/tcl/         模拟 EDA Tcl 脚本
  scripts/python/      Python 自动化核心
  data/                模拟测试数据
  docs/                中文教程
  runs/                每次运行的结果
  reports/             汇总报告和归档
```

## 你要达成的能力

做完并理解这个项目后，你应该能解释：

- 为什么 IC/EDA 公司大量使用 Linux
- Shell、Tcl、Python 在流程自动化里分别负责什么
- 一次 flow run 为什么必须保存日志、配置、版本和结果
- QA 自动化检查什么
- 测试数据怎么收集、统计和生成报告
- 如果以后把模拟步骤替换成真实 EDA 工具，该改哪里

