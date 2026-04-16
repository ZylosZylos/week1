# Python Week 1 工程管理流程总结

这份 README 主要整理我当前使用 `Linux + VS Code + Git + GitHub` 的基础工程管理流程，方便自己后续重复使用，也方便上传到 GitHub 后直接查看。

## 1. 我的目标

这一周我主要想提升两部分能力：

- Python 语法和练习能力
- 使用 `VS Code + Python + Linux + Git + GitHub` 进行项目工程管理的能力

## 2. 新项目的标准启动流程

在 Linux 终端中进入自己的项目目录：

```bash
cd ~/projects
mkdir myproject
cd myproject
```

初始化 Git 仓库：

```bash
git init
```

创建 Python 虚拟环境：

```bash
python3 -m venv .venv
```

激活虚拟环境：

```bash
source .venv/bin/activate
```

用 VS Code 打开当前项目：

```bash
code .
```

建议在项目刚创建时就先写好 `.gitignore`，避免把虚拟环境和缓存文件提交到 GitHub：

```gitignore
.venv/
__pycache__/
*.pyc
```

## 3. 日常开发流程

平时开发时，我通常按下面的顺序操作：

1. 进入项目目录
2. 激活虚拟环境
3. 用 `code .` 打开项目
4. 编写或修改代码
5. 用 Git 查看改动并提交

常用命令如下：

```bash
cd ~/projects/myproject
source .venv/bin/activate
code .
git status
git add .
git commit -m "完成某个功能或修复某个问题"
git push
```

## 4. 第一次连接 GitHub 仓库

如果这是一个刚创建的新项目，需要先把本地仓库和 GitHub 仓库绑定。

先查看当前分支名：

```bash
git branch --show-current
```

如果你想统一使用 `main`，可以执行：

```bash
git remote add origin 你的仓库地址
git branch -M main
git add .
git commit -m "init project"
git push -u origin main
```

如果你当前仓库仍然使用 `master`，也可以不改分支名，直接执行：

```bash
git remote add origin 你的仓库地址
git add .
git commit -m "init project"
git push -u origin master
```

说明：

- `git remote add origin ...`：绑定远程仓库
- `git branch -M main`：把默认分支统一成 `main`
- `git push -u origin main` 或 `git push -u origin master`：第一次推送并建立本地分支和远程分支的跟踪关系

## 5. 打开旧项目的流程

如果是已经存在的项目，就不需要重新 `git init`，只需要：

```bash
cd ~/projects/已有项目名
source .venv/bin/activate
code .
```

然后继续开发即可。

## 6. 最常用的 Git 命令

下面几个命令是最基础、最常用的：

```bash
git status
git add .
git commit -m "提交说明"
git push
git pull
```

它们的作用分别是：

- `git status`：查看当前文件状态
- `git add .`：把当前改动加入暂存区
- `git commit -m "..."`：生成一次本地提交
- `git push`：把本地提交推送到 GitHub
- `git pull`：拉取远程仓库的最新内容

## 7. VS Code + Linux 的建议用法

为了减少路径、权限和编码问题，建议尽量在 Linux 环境里操作项目：

```bash
cd ~/projects/myproject
code .
```

这样通常会比直接从 Windows 文件管理器打开 WSL 路径更稳定。

如果 Git 提示下面这种错误：

```bash
fatal: detected dubious ownership in repository
```

可以执行：

```bash
git config --global --add safe.directory "$(pwd)"
```

这表示把当前目录标记为安全仓库。

## 8. 这次 GitHub README 显示为空的原因

这次上传到 GitHub 后看不到文字，不是因为中文不能显示，而是因为仓库里同时存在两个文件：

- `readme.md`
- `README.md`

其中原来真正有内容的是小写的 `readme.md`，而大写的 `README.md` 是空文件。GitHub 首页优先展示的是 `README.md`，所以看起来像是一个空文件。

我这次已经把内容整理到正确的 `README.md` 中，并删除了重复的小写文件。以后建议统一只保留一个：

```bash
README.md
```

## 9. 避免 README 再次出问题

以后写 README 时，建议注意这几点：

- 文件名统一用 `README.md`
- 文件编码尽量保存为 `UTF-8`
- 不要同时保留 `readme.md` 和 `README.md`
- 提交前先用 `git status` 检查一下实际被提交的是哪个文件

## 10. 现阶段我对工程管理流程的理解

对我来说，一个 Python 项目的基础工程管理流程可以概括为：

1. 在 Linux 中创建项目目录
2. 用 `git init` 管理项目版本
3. 用 `.venv` 隔离项目环境
4. 用 `.gitignore` 忽略不该提交的文件
5. 用 `code .` 进入 VS Code 开发
6. 用 `git status / add / commit / push` 管理开发过程
7. 用 GitHub 保存远程仓库和项目记录

这套流程虽然基础，但非常重要。只要把这套流程练熟，后面学习更复杂的 Python 项目、多人协作和部署流程都会顺很多。


void func_C(int internal, int duration) {
    system("grep 'MemTotal' /proc/meminfo | awk '{print "计算机配置的内存数量: "2}'");
    system("grep 'MemAvailable' /proc/meminfo | awk '{print "当前可用的内存数量: "2}'");
    printf("平均负载列表 (每 %d 秒采样一次，总计 %d 秒):n", internal, duration);

    time_t start_time = time(NULL); // 记录整个监控开始的时间
    time_t last_sample_time = 0;    // 记录上一次打印的时间

    // 循环：只要当前时间 - 开始时间 = 我们设置的间隔（internal）
        // 或者这是第一次采样（last_sample_time == 0）
        if (current_time - last_sample_time >= internal) {
            system("cat /proc/loadavg | cut -d ' ' -f 1"); // 打印负载
            last_sample_time = current_time;               // 更新采样时间
        }
        
        // 注意：这里没有 sleep，CPU 会在这里拼命循环检查时间
    }
    printf("监控结束。n");
}