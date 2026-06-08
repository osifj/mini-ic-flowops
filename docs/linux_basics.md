# Linux 基础速记

## 常用命令

```bash
pwd        # 我在哪里
ls         # 当前目录有什么
ls -l      # 详细列表
cd docs    # 进入 docs
cd ..      # 回到上一级
mkdir a    # 创建目录
rm file    # 删除文件，慎用
cat file   # 看文件内容
less file  # 分页看文件
tail file  # 看文件末尾
tail -f file # 持续看日志
```

## 权限

```bash
chmod +x bin/flowctl
```

意思是给 `bin/flowctl` 增加可执行权限。

## 环境变量

```bash
echo $PATH
echo $HOME
echo $FLOWOPS_ROOT
```

`PATH` 决定你输入一个命令时，Linux 去哪些目录找它。

## 重定向和管道

```bash
flowctl status > status.txt
cat runs/run_001/logs/flow.log | tail -n 20
```

- `>` 把输出写进文件。
- `|` 把前一个命令的输出交给后一个命令。

