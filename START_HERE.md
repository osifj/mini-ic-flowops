# START HERE: 零基础几天搞懂 mini-ic-flowops

你现在只需要抓住一个目标：

> 学会像实习生一样，在 Linux 里跑一个自动化流程、看日志、看报告、定位问题、解释脚本做了什么。

不要先追求“完全懂芯片设计”。这个项目不是让你几天内变成 IC 设计工程师，而是让你先具备岗位截图里最需要的自动化工作能力。

## 你应该按这个顺序学

1. `docs/3_day_crash_plan.md`
2. `docs/windows_to_linux_vm_steps.md`
3. `docs/every_command_explained.md`
4. `docs/project_file_walkthrough.md`
5. `docs/code_reading_guide.md`
6. `docs/final_self_test.md`

在 Linux 虚拟机里也可以直接运行：

```bash
./bin/flowctl learn
```

如果已经执行过：

```bash
source config/env.sh
```

那就可以直接运行：

```bash
flowctl learn
```

## 第一次必须跑通的命令

```bash
cd mini-ic-flowops
chmod +x bin/flowctl
source config/env.sh
flowctl doctor
flowctl run --design alu --flow testchip
flowctl status
flowctl ask "怎么看日志"
```

你第一次不懂每个词没关系。先跑通，再回头看解释。

## 你最后要能讲出来什么

你要能用自己的话讲清楚：

- `flowctl` 是一个流程自动化入口。
- `config/testchip_flow.yaml` 定义要跑哪些步骤。
- `scripts/tcl/*.tcl` 模拟 EDA 工具步骤。
- `scripts/python/flowops/flowctl.py` 负责流程编排、QA、数据分析和报告。
- `runs/run_xxx/` 保存每一次运行的日志、指标、报告和版本记录。
- `manifest.json` 记录这次运行用了哪个 commit、哪些输入文件、哪些工具版本。

如果你能把这几句话讲清楚，实习前的第一关就过了。

