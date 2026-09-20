---
title: 上手
tags:
  - 元
---

# 上手

## 30 秒版

```bash
pip install -r requirements.txt     # mkdocs-material / awesome-pages / pypandoc / olefile
python scripts/gen_section_index.py # 刷新各板块落地页
python scripts/gen_board.py         # 刷新缓冲看板
python -m mkdocs serve -a 127.0.0.1:8000
# 打开 http://127.0.0.1:8000/14thSecretary/
```

改内容 → 保存 → 浏览器自动刷新。
改完 **推 `main` 就自动上线**，不需要任何人跑部署命令。

## 本机现成环境

这台机器上依赖已经装好了，直接用绝对路径调用，别重复装：

| | 路径 |
|---|---|
| Python | `C:\Users\ROG\.workbuddy\binaries\python\envs\default\Scripts\python.exe` |
| Node（只在需要语法校验 JS 时用） | `C:\Users\ROG\.workbuddy\binaries\node\versions\22.22.2-3\node.exe` |
| Git | `C:\Program Files\Git\cmd\git.exe`（**PATH 里没有 `gh`**） |

## 改完必须做的三件事

**1. 构建，并且逐行看有没有 WARNING**

```bash
python -m mkdocs build
```

`mkdocs build` **即使有坏链也返回 0**，所以别只看退出码。
有 `WARNING` 基本就是链接写错了（相对路径问题见[已知坑](pitfalls.md)）。

**2. 跑生成脚本的 `--check`**

```bash
python scripts/gen_board.py --check
python scripts/gen_section_index.py --check
```

返回 0 说明生成物和源内容一致。**不一致就说明你改了内容却忘了重跑脚本** —— CI 里会跑这两个，
但你本地先跑一遍能提前发现问题。（这两个脚本的 `--check` 是幂等的，放心跑。）

**3. 确认没有临时文件混进提交**

```bash
git status --short
```

仓库 `.gitignore` 已经挡了 `site/`、`*.log`、`_*`、`__pycache__`。
**自己造的临时文件一律用 `_` 前缀命名**，这样自动被忽略。

## 发布链路

```text
git push origin main
        ↓
.github/workflows/deploy.yml
        ↓  装依赖 → 重跑两个生成脚本 → mkdocs build → 上传产物
GitHub Pages（build_type = workflow）
        ↓
https://nyemiwu.github.io/14thSecretary/
```

- **只有这一个工作流。** 仓库里出现过 GitHub 自动塞的 Jekyll 起始工作流，
  它会和我们的部署抢同一个 `concurrency: pages` 组、随机覆盖站点。见[已知坑](pitfalls.md)。
- Pages 的 Source 必须是 `GitHub Actions`，不是 `Deploy from a branch`。
- 推送后要等 1–2 分钟才生效，不是立刻可见。

## 不需要做的

- **不要跑 `mkdocs gh-deploy`。** 那会推一个 `gh-pages` 分支和 Actions 打架。
- **不要用 `pip install mkdocs-material` 单独装。** 用 `requirements.txt`，版本要一致。
- **不要改 `site/`。** 它是构建产物，每次 build 都会被清空重建。
