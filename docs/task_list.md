# 项目任务单

## 阶段 1：环境

- 安装 Linux 虚拟机或使用 WSL
- 安装 `git`、`tcl`、`python3`
- 执行 `flowctl doctor`

## 阶段 2：跑通 Reference Flow

```bash
flowctl run --design alu --flow ref
```

你需要看懂：

- `config/ref_flow.yaml`
- `runs/run_001/logs/flow.log`
- `runs/run_001/manifest.json`
- `runs/run_001/reports/flow_report.html`

## 阶段 3：跑通 Testchip Flow

```bash
flowctl run --design alu --flow testchip
```

你需要看懂：

- IP QA 报告
- Testchip 数据分析报告
- `data/testchip_results.csv`

## 阶段 4：修改参数并比较

改一个 Tcl 脚本里的指标，再跑一次：

```bash
flowctl run --design alu --flow ref
flowctl compare run_001 run_003
```

重点不是指标真假，而是学会“变更后如何比较结果”。

## 阶段 5：模拟新增一个 IP

复制 `designs/alu` 为 `designs/myip`，然后故意删掉 README，再执行：

```bash
flowctl qa --design myip
```

观察 QA 如何报错。

