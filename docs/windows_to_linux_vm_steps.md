# Windows + Linux 虚拟机操作步骤

你现在是 Windows 电脑，已经装了 Linux 虚拟机。最推荐的方式是：把项目复制进 Linux 虚拟机，在 Linux 里运行命令。

## 方式 1：复制 zip 到 Linux 虚拟机

你已经有项目压缩包：

```text
mini-ic-flowops_project.zip
```

把它拖进 Linux 虚拟机桌面，或者放到共享文件夹。

假设 zip 在 Linux 的 `~/Downloads`：

```bash
cd ~/Downloads
unzip mini-ic-flowops_project.zip
cd mini-ic-flowops
```

如果 Linux 提示没有 `unzip`：

```bash
sudo apt update
sudo apt install -y unzip
```

## 方式 2：直接用项目目录

如果你已经把整个 `mini-ic-flowops` 文件夹复制进 Linux：

```bash
cd 路径/mini-ic-flowops
```

例如：

```bash
cd ~/Desktop/mini-ic-flowops
```

## 安装必须工具

Ubuntu：

```bash
sudo apt update
sudo apt install -y python3 git make tcl
```

Rocky Linux / CentOS：

```bash
sudo dnf install -y python3 git make tcl
```

## 第一次运行

```bash
chmod +x bin/flowctl
source config/env.sh
flowctl doctor
flowctl run --design alu --flow testchip
flowctl status
```

## 每次重新打开终端后要做什么

进入项目目录：

```bash
cd ~/Desktop/mini-ic-flowops
```

重新 source 环境：

```bash
source config/env.sh
```

然后就能直接运行：

```bash
flowctl status
```

## 如果 source 后还是找不到 flowctl

先确认你在项目根目录：

```bash
pwd
ls
```

你应该能看到：

```text
bin config docs scripts runs reports
```

再执行：

```bash
source config/env.sh
echo $FLOWOPS_ROOT
echo $PATH
```

如果 `FLOWOPS_ROOT` 指向你的项目目录，就说明环境设置成功。

## Windows 和 Linux 的区别

Windows 常见路径：

```text
C:\Users\你的用户名\Desktop\mini-ic-flowops
```

Linux 常见路径：

```text
/home/你的用户名/Desktop/mini-ic-flowops
```

真实实习里，你更可能在 Linux 服务器上工作，所以本项目建议你主要在 Linux 里练。

