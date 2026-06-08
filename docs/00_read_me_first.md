# 从这里开始

你现在是零基础，所以不要一上来背概念。先记住一句话：

> 这个项目是在模拟公司里“用脚本把芯片设计流程自动跑起来”的工作。

岗位截图里的关键词可以翻译成更直白的话：

- Linux：大多数 EDA 工具和服务器运行在 Linux 上。
- Shell：把很多命令串起来，一键运行。
- Tcl：很多 EDA 工具内置 Tcl，用它控制综合、布局布线、签核等步骤。
- Python：更适合做数据处理、报告、QA 检查、自动化平台。
- 版本管理：记录每次用的代码、配置、输入数据，方便追溯。
- Reference Flow：给大家复用的标准流程模板。
- Testchip Flow：用于测试芯片或验证 IP 的完整流程。
- IP QA：检查一个 IP 交付包是否完整、规范、可复现。

## 学习方式

不要急着看懂所有代码。建议按这个顺序：

1. 先跑命令。
2. 看生成了什么目录和报告。
3. 再打开脚本，看每一步是怎么做的。
4. 改一个小参数，再跑一次。
5. 用 `flowctl compare` 比较两次结果。

## 第一次运行

```bash
cd mini-ic-flowops
chmod +x bin/flowctl
./bin/flowctl doctor
./bin/flowctl init
./bin/flowctl run --design alu --flow ref
./bin/flowctl status
```

看日志：

```bash
tail -n 80 runs/run_001/logs/flow.log
```

看报告：

```bash
ls runs/run_001/reports
```

## 你要特别关注的文件

- `bin/flowctl`：命令入口，Shell 写的。
- `scripts/python/flowops/flowctl.py`：自动化核心，Python 写的。
- `scripts/tcl/*.tcl`：模拟 EDA 工具脚本，Tcl 写的。
- `config/*.yaml`：流程配置。
- `runs/run_001/manifest.json`：一次运行的版本、输入、工具、步骤记录。

