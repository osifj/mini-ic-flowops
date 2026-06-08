# 最终自测清单

这篇文档用来判断你是否真的搞懂了。

## A. 命令自测

不看 README，独立完成：

```bash
cd mini-ic-flowops
source config/env.sh
flowctl doctor
flowctl run --design alu --flow testchip
flowctl status
flowctl qa --design alu
flowctl ask "怎么看日志"
flowctl archive --run latest
```

如果你能独立跑完，说明操作层过关。

## B. 目录自测

回答这些问题：

1. `config/` 放什么？
2. `designs/alu/rtl/alu.v` 是什么？
3. `scripts/tcl/` 为什么存在？
4. `runs/run_001/logs/flow.log` 是什么？
5. `runs/run_001/manifest.json` 是什么？
6. `reports/` 和 `runs/run_001/reports/` 有什么区别？

## C. 流程自测

回答：

1. Reference Flow 包含哪些步骤？
2. Testchip Flow 比 Reference Flow 多了什么？
3. `precheck` 做什么？
4. `synth` 模拟什么？
5. `signoff` 模拟什么？
6. `ip_qa` 检查什么？
7. `data_collect` 分析什么？

## D. 故障排查自测

做一个小实验。

### 第一步：复制一个坏 IP

```bash
cp -r designs/alu designs/badip
rm designs/badip/README.md
flowctl qa --design badip
```

你应该看到 QA 失败。

### 第二步：修复

```bash
cp designs/alu/README.md designs/badip/README.md
flowctl qa --design badip
```

现在应该通过。

### 第三步：清理

```bash
rm -rf designs/badip
```

## E. 版本管理自测

运行：

```bash
git status
git log --oneline -5
```

回答：

1. 当前是否有未提交修改？
2. 最近一次 commit 是什么？
3. `manifest.json` 里为什么要记录 commit？

## F. 口头表达自测

用 1 分钟讲这个项目：

```text
我做了一个 mini IC flow 自动化练习项目。它用 Shell 作为命令入口，用 YAML 定义 Reference Flow 和 Testchip Flow，用 Tcl 模拟 EDA 工具步骤，用 Python 做流程编排、IP QA、测试数据分析、报告生成和版本记录。每次运行都会生成独立的 run 目录，里面包含日志、metrics、reports 和 manifest，方便定位失败、追踪输入和比较结果。
```

如果你能不看稿讲出 70%，就可以去实习了。

## G. 面向实习岗位的自测

岗位要求里有 7 类工作，你要能对应上：

| 岗位要求 | 本项目对应内容 |
| --- | --- |
| 数据版本管理自动化 | `manifest.json`、Git commit、输入 hash |
| 模拟电路设计流程自动化 | flow 编排思想，步骤模拟 |
| Reference Flow/Testchip | `config/ref_flow.yaml`、`config/testchip_flow.yaml` |
| 版图设计流程自动化 | `floorplan/place/route/signoff` 模拟 |
| IP QA | `flowctl qa`、`run_ip_qa()` |
| 流片测试数据管理分析 | `data/testchip_results.csv`、`analyze_testchip_data()` |
| AI 工具部署支持 | `flowctl ask`、`docs/ai_tool_deploy_notes.md` |

