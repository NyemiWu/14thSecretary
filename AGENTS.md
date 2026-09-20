# AGENTS.md

给 AI 助手的入口。**详细文档在站点上：<https://nyemiwu.github.io/14thSecretary/agents/>**
（源文件在 `docs/agents/`）。这一份是精简摘要，改了规则请同步。

## 这是什么

一个朋友团体的世界观设定集（TRPG / 游戏项目），用 **MkDocs + Material** 构建成静态站，
发布在 GitHub Pages。约 111 篇 Markdown、12 个内容板块。

- 站点：<https://nyemiwu.github.io/14thSecretary/>
- 仓库：<https://github.com/NyemiWu/14thSecretary>
- 技术栈：MkDocs 1.6 + Material 9.7 + mkdocs-awesome-pages-plugin，**零外部 CDN 依赖**

## 四个分区

| 分区 | 目录 | 放什么 |
|---|---|---|
| 文本分区 | `docs/text/` | 设定、剧情、图鉴等**纯阅读内容**（12 个板块） |
| 可交互叙事分区 | `docs/interactive/` | 跑得起来的工具（介绍页 + 同名 HTML 并排） |
| 缓冲分区 | `docs/buffer/` | 投稿通道：`pending/` 待审 → `public/` 公示 → 期满删除 |
| 机哥分区 | `docs/agents/` | 给 agent 的文档（就是这一区） |

## 六条硬规则

1. **新内容一律先进 `docs/buffer/pending/`**，管理员放行后才并入正式分区。
   改已有条目也一样 —— 产出带 `revises` 字段的修改稿，不要直接编辑原文。
2. **绝对不要用 `git rm`。** 实测会导致 `docs/` 下全部文件（含未跟踪的新文件）一起消失。
   用 `[System.IO.File]::Delete()` 再 `git add -A`。
3. **不许手改生成物**：`docs/text/index.md`、`docs/text/*/index.md`、`docs/buffer/index.md`、`site/**`。
   改生成它们的脚本。
4. **前端代码约定**：只用 `var`，不用箭头函数 / 模板字符串 / `class` / `async`。不引外部 CDN。
5. **目录和文件名用 ASCII**（知识库导入的历史文件是有意保留中文名的，不要"顺手"改）。
6. **`.github/workflows/` 下只能有一个工作流**，不要用 `mkdocs gh-deploy`。

## 常用命令

```bash
pip install -r requirements.txt
python scripts/gen_section_index.py     # 刷新板块落地页（--check 可校验）
python scripts/gen_board.py             # 刷新缓冲看板（--check 可校验）
python -m mkdocs build                  # 构建，**逐行看有没有 WARNING**
python -m mkdocs serve -a 127.0.0.1:8000
```

本地预览：<http://127.0.0.1:8000/14thSecretary/>

## 改完必须做

1. `python -m mkdocs build` —— **有 WARNING 就是有坏链**（即使返回 0）
2. `python scripts/gen_board.py --check` 和 `gen_section_index.py --check` —— 必须 exit 0
3. `git status --short` —— 确认没有临时文件混进来（临时文件用 `_` 前缀，已被 gitignore）

推送 `main` 即自动发布（GitHub Actions），构建约 1–2 分钟生效。

## 最容易踩的三个坑

1. **相对路径有两个基准**：`<iframe src>` 由浏览器算（基准 = 页面 URL 目录），
   markdown 链接由 MkDocs 算（基准 = 源文件目录）。工具 HTML 与介绍页**并排同名**可规避。
2. **`draft_docs` = 只在 `mkdocs serve` 构建**，`mkdocs build` 不发布。
   所以 `buffer/pending/` 里的稿件在线上是 404，链接要指向 GitHub 原文。
3. **`mkdocs build` 有 WARNING 也返回 0**，别只看退出码。

更多（含报错原文）：<https://nyemiwu.github.io/14thSecretary/agents/pitfalls/>

## 这台机器上的操作约束（Windows）

| 约束 | 替代做法 |
|---|---|
| PowerShell 的 stdout 不回传 | 输出 `Out-File` 写文件再读 |
| `.ps1` 跑不了（策略 `Restricted`） | 只用 `-Command` 内联，**控制在 1.5KB 以内** |
| PowerShell 变量名**不区分大小写** | `$A`/`$a` 是同一个变量，用长名字 |
| 不要用 `Remove-Item` | 有 safe-delete shim，中文路径会静默失败 |
| Bash 工具缺 `ls`/`cat`/`dirname` | 但 `git push` 可靠 → 推送走 Bash + 重定向 |
| Bash 里别用 `&&` 串联 git | 会被当字面参数，用 `;` |

## 相关 skill

`mkdocs-wiki-setup`（`~/.workbuddy/skills/`）—— 本仓库的全部踩坑经验沉淀在这里。
改站点做法前先读它。详见 <https://nyemiwu.github.io/14thSecretary/agents/skills/>
