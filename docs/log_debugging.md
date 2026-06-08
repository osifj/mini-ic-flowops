# 日志与失败排查

日志是流程自动化里最重要的线索。你不用一开始看懂所有脚本，但要学会先找日志。

## 一次 run 的主日志

```bash
tail -n 80 runs/run_001/logs/flow.log
```

如果不知道最新 run 是哪个：

```bash
flowctl status
```

也可以使用项目里的小工具：

```bash
scripts/shell/show_latest_log.sh
```

## 看日志的顺序

1. 先看终端最后输出。
2. 再看 `runs/run_xxx/logs/flow.log`。
3. 找第一个失败步骤。
4. 打开对应报告，例如 `runs/run_xxx/reports/route.rpt`。
5. 再看 `manifest.json`，确认输入、配置、commit 有没有变化。

## 常见失败类型

- 输入缺失：缺 RTL、缺 SDC、缺 ip.yaml。
- 环境问题：找不到命令、环境变量没 source。
- 工具问题：真实公司里可能是 license、版本、服务器路径。
- 结果问题：DRC/LVS/timing 指标不达标。

## 新手记住一句话

不要只说“它失败了”。要说清楚：

- 哪个 run 失败
- 哪个步骤失败
- 日志路径是什么
- 第一个错误是什么
- 你已经检查过什么

