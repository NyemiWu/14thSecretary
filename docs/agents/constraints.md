---
title: 硬规则
tags:
  - 元
---

# 硬规则

**赶时间只读这一页。** 每条都配了"为什么"，因为只写"不许"的规则会被绕过。

---

## 一、内容：新东西一律先进缓冲区

```text
新内容 → docs/buffer/pending/ → 管理员标记 → public/ 公示 → 期满 → 并入 text/ 或 interactive/
```

**为什么**：这是一个多人协作的设定集，稿子要经审核才生效。
直接往 `text/` 写等于绕过审核，且会让缓冲看板和实际内容对不上。

**改已有条目也一样** —— 不要直接编辑原文，而是产出一份带 `revises` 字段的修改稿。
站上的「编辑此条目」按钮会自动做这件事。

## 二、绝对不要用 `git rm`

用 `[System.IO.File]::Delete()` / `[System.IO.Directory]::Delete()`（Windows）
或普通 `rm`（Unix），然后 `git add -A` 让 git 记录删除。

**为什么**：2026-09-21 实测，在这个仓库执行 `git rm -r docs/admin` 之后，
**`docs/` 下所有已跟踪文件 + 全部未跟踪新文件一起消失**（约 160 个），
包括刚导入的知识库和一个刚写完的编辑器。
`git restore --source=HEAD --worktree docs/` 只能救回已提交的部分，
未提交的新文件**永久丢失**，只能重写。

这是这个仓库发生过的最严重的事故，一次也不要再试。

## 三、生成物不许手改

`docs/text/index.md`、`docs/text/*/index.md`、`docs/buffer/index.md`、`site/**` ——
每次构建都会被脚本覆盖。要改就改生成它的脚本。详见 [仓库地图](repo-map.md)。

## 四、前端代码约定

这个站（以及使用者所有的 TRPG 工具）统一遵守：

| 不用 | 用 |
|---|---|
| 箭头函数 `=>` | `function () {}` |
| 模板字符串 `` ` `` | `"a" + b` |
| `class` | 构造函数 + 原型，或直接写函数 |
| `async` / `await` | `Promise.then()` |

**为什么**：使用者的运行环境不保证支持这些语法，他自己的工具全系列都是这个写法。
新增 JS 请保持一致 —— 这不只是风格问题，是兼容性问题。

另外：**站点零外部 CDN 依赖**。不要引入外部字体、CSS 框架、JS 库。
Material 的 CSS/JS 是打包进 `site/` 的，`/editor/` 也是纯内联的。

## 五、目录和文件名用 ASCII

中文只出现在**标题**（`# 标题`）、`mkdocs.yml`、`.pages` 里。

**为什么**：中文路径会变成 `%E7%A7%98%E8%AF%AD` 这种 URL，跨平台同步容易炸。

!!! warning "一个有意破例"
    知识库导入进来的 100+ 篇文档**保留了原中文文件名**，因为要和用户手上的源包对得上。
    这是当时权衡的结果，**不要"顺手"把它们拼音化** —— 那会让人对不上文件。
    新写的文档请遵守 ASCII 规则。

## 六、发布：只有一个工作流，不用 gh-deploy

- **不要跑 `mkdocs gh-deploy`** —— 它会推 `gh-pages` 分支，和 Actions 打架。
- **`.github/workflows/` 下只允许一个文件。** 加完确认
  `GET /repos/{owner}/{repo}/actions/workflows` 的 `total_count` 是 1。
- **不要在部署工作流里加 `actions/configure-pages` + `enablement: true`** ——
  那一步必然失败并让整个 build job 挂掉。

## 七、操作这个仓库的机器环境约束

在这台 Windows 机器上干活时：

| 约束 | 原因 / 替代做法 |
|---|---|
| **PowerShell 的 stdout 不回传** | 命令输出一律 `Out-File` 写文件再 Read |
| **`.ps1` 文件跑不了**（执行策略 `Restricted`） | 只用 `-Command` 内联，且**控制在 1.5KB 以内**（超了沙箱起不来） |
| **PowerShell 变量名不区分大小写** | `$A` 和 `$a` 是同一个变量。用 `$URL`/`$LINES` 这种长名字 |
| **不要用 `Remove-Item`** | 有 safe-delete shim，遇中文路径会静默失败。用 `[System.IO.File]::Delete()` |
| **Bash 工具缺 `ls`/`dirname`/`cat`** | 但**跑 `git push` 是可靠的**（PowerShell 反而捕获不到 git 输出）→ 推送走 Bash + 重定向 |
| **Bash 里别用 `&&` 串联 git 命令** | 会被当字面参数，用 `;` 分隔 |

## 八、改流程之前先想清楚

这个缓冲流程已经被**砍过三轮**（多级审批矩阵 → 单字段状态机 → 目录即状态）。

**每加一个字段或状态，先问一次"不加会怎样"。**
前面两轮都是往上堆规则被否掉，第三轮砍到「状态 = 文件在哪个目录」才收敛。

同样地，**自动生成的聚合页不要给「编辑」按钮** ——
改了会被构建覆盖，给个"在此分区新建条目"更有用。
