# 实习表达模板

这篇文档帮你把项目讲得像真的做过，而不是背名词。

## 30 秒版本

```text
我最近做了一个 mini IC flow 自动化项目，用来训练脚本工具和流程自动化能力。它用 Shell 做统一入口，用 YAML 配置 Reference Flow 和 Testchip Flow，用 Tcl 模拟 EDA 工具步骤，用 Python 做流程编排、IP QA、测试数据分析和报告生成。每次运行都会保留日志、报告、metrics 和 manifest，方便排查失败和追踪版本。
```

## 1 分钟版本

```text
这个项目模拟了芯片团队内部常见的 flow 工具。用户运行 flowctl run 后，程序会读取 flow 配置，创建独立的 run 目录，然后按 precheck、synth、floorplan、place、route、signoff、ip_qa、data_collect、report 的顺序执行。Tcl 脚本负责模拟 EDA 工具报告，Python 负责调度流程、检查 IP 交付质量、分析 testchip CSV 数据，并生成 HTML/Markdown 报告。manifest.json 会记录 git commit、工具版本、输入文件 hash 和每个步骤状态，所以结果可以追溯和比较。
```

## 如果导师问：你会 Linux 吗？

你可以说：

```text
我会基本 Linux 操作，比如 cd、ls、pwd、chmod、source、tail、环境变量 PATH。我也练过在 Linux 里配置项目环境、运行脚本、查看日志和定位失败。
```

## 如果导师问：Shell、Tcl、Python 分别干什么？

你可以说：

```text
Shell 更适合做命令入口、环境配置和流程串联；Tcl 在 EDA 工具里很常见，常用于控制综合、布局布线、时序签核等工具命令；Python 更适合做复杂逻辑，比如解析配置、QA 检查、CSV 数据分析、报告生成和版本记录。
```

## 如果导师问：什么是 Reference Flow？

你可以说：

```text
Reference Flow 是一套标准参考流程，目的是让团队复用稳定的步骤和配置。本项目里 ref flow 包含 precheck、synth、floorplan、place、route、signoff 和 report。
```

## 如果导师问：什么是 Testchip Flow？

你可以说：

```text
Testchip Flow 比基础 Reference Flow 更完整，会在设计流程之后增加 IP QA、测试数据收集和分析，用来支持 testchip 或 IP 验证相关工作。
```

## 如果导师问：IP QA 检查什么？

你可以说：

```text
IP QA 主要检查交付包是否完整和规范，比如 README、ip.yaml、RTL、SDC 约束、版本字段、空文件、硬编码绝对路径等。这样可以减少后续集成时因为输入不规范导致的流程失败。
```

## 如果导师问：你怎么排查 flow 失败？

你可以说：

```text
我会先看终端输出和 flow.log，找到第一个失败步骤；再看对应步骤的 report，比如 route.rpt 或 signoff.rpt；然后检查 manifest.json 里的输入文件、配置和 commit 是否变化。这样可以判断是环境问题、输入问题、配置问题还是脚本问题。
```

## 如果导师问：为什么要记录 manifest？

你可以说：

```text
因为 flow 结果必须可追溯。manifest 记录 git commit、工具版本、输入文件 hash、flow 配置、每个步骤状态和时间。以后结果变化时，可以判断是代码变了、配置变了、输入数据变了，还是工具环境变了。
```

## 你不要这样说

不要说：

```text
我已经完全掌握 IC 设计流程。
```

这太大，也不真实。

建议说：

```text
我还在学习真实 EDA 工具和芯片设计细节，但我已经通过项目练过 Linux 环境、Shell/Tcl/Python 脚本、流程编排、日志排查、QA 和数据分析，能比较快接手流程自动化类任务。
```

