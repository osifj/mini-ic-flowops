# 每条命令逐行解释

这篇文档只讲命令，不讲代码。

## 进入项目目录

```bash
cd mini-ic-flowops
```

意思：进入项目文件夹。

如果报错：

```text
No such file or directory
```

说明你当前位置不对。先用：

```bash
pwd
ls
```

确认当前在哪、当前目录有什么。

## 给脚本执行权限

```bash
chmod +x bin/flowctl
```

意思：允许 Linux 执行 `bin/flowctl` 这个脚本。

如果不做这一步，可能会报：

```text
Permission denied
```

## 加载环境变量

```bash
source config/env.sh
```

意思：执行环境配置脚本，让当前终端知道项目在哪里，并把 `bin/` 加入 `PATH`。

执行后你会看到类似：

```text
FLOWOPS_ROOT=/home/you/mini-ic-flowops
flowctl 已加入 PATH，可以直接运行：flowctl doctor
```

## 检查环境

```bash
flowctl doctor
```

它会检查：

- Python 是否可用
- Git 是否可用
- Tcl 是否可用
- 项目根目录是否正确

如果 Tcl 缺失，项目仍然能跑，因为 Python 有 fallback 模拟。但你最好安装 Tcl。

## 初始化项目

```bash
flowctl init
```

它会确认这些目录存在：

```text
runs/
reports/
work/
```

这些目录用于保存运行结果。

## 运行 Reference Flow

```bash
flowctl run --design alu --flow ref
```

意思：

- `run`：运行流程
- `--design alu`：使用 `designs/alu` 这个示例设计
- `--flow ref`：使用 `config/ref_flow.yaml` 这套流程

Reference Flow 包含：

```text
precheck -> synth -> floorplan -> place -> route -> signoff -> report
```

## 运行 Testchip Flow

```bash
flowctl run --design alu --flow testchip
```

Testchip Flow 比 Reference Flow 更完整，包含：

```text
precheck -> synth -> floorplan -> place -> route -> signoff -> ip_qa -> data_collect -> report
```

所以你实习前最应该跑熟的是这个。

## 查看所有运行记录

```bash
flowctl status
```

你会看到类似：

```text
Run ID    Status   Design   Flow      Start Time
run_001   PASS     alu      testchip  2026-06-08 14:10:55
```

重点看：

- Run ID：这次运行编号
- Status：PASS 或 FAIL
- Design：跑哪个设计
- Flow：跑哪套流程

## 查看日志

```bash
tail -n 80 runs/run_001/logs/flow.log
```

意思：查看 `flow.log` 最后 80 行。

为什么看最后？因为失败原因通常在日志后面。

## 查看报告

```bash
ls runs/run_001/reports
```

你会看到：

```text
flow_report.html
ip_qa_report.html
testchip_analysis.md
synth.rpt
route.rpt
signoff.rpt
```

`.html` 可以用浏览器打开，`.md` 和 `.rpt` 可以用文本编辑器打开。

## 单独运行 IP QA

```bash
flowctl qa --design alu
```

它会检查：

- 有没有 README
- 有没有 ip.yaml
- 有没有 RTL 文件
- 有没有 SDC 约束
- 有没有空文件
- 有没有硬编码绝对路径

## 比较两次运行

```bash
flowctl compare run_001 run_002
```

它会比较两次 run 的 metrics。

真实公司里经常需要回答：

> 为什么这次面积、功耗、时序变了？

`compare` 就是这个思路的简化版。

## 搜索文档

```bash
flowctl ask "怎么看日志"
```

它会在 `docs/` 里做关键词搜索。

这是一个很简单的内部知识库检索模拟。

## 打包归档

```bash
flowctl archive --run latest
```

意思：把最新 run 打包成 zip，方便交付或保存。

## 清理生成结果

先预览：

```bash
flowctl clean
```

确认清理：

```bash
flowctl clean --yes
```

注意：这个命令会删除生成的 `runs/run_*`，但不会删除源码和文档。

## 查看学习路线

```bash
flowctl learn
```

它会告诉你先读哪些文档、每天做哪些命令。

