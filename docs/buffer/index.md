---
title: 缓冲看板
tags:
  - 元
---

# 缓冲看板

!!! info "本页自动生成，不要手改"
    由 `scripts/gen_board.py` 扫描 `buffer/pending/` 与 `buffer/public/` 生成。
    稿件一动就跑一次：`python scripts/gen_board.py`

    成员投稿走 [内容后台](editor.md)（表单式，不用写 Markdown），
    或者直接往 `buffer/pending/` 放文件。流程见 [缓冲流程](rules.md)。

**截至 2026-09-21** —— 公示中 **2** · 待审 **1**

## 公示中

管理员已标记通过，正在公示期。期满后**从缓冲区删除**：
内容并入正式分区，或者直接丢弃。

| 编号 | 标题 | 提交人 | 审核人 | 公示截止 | 点赞 | 点踩 | 状态 |
|---|---|---|---|---|---|---|---|
| [003](public/003-ashwalker.md) | 005 灰烬行者 · 图鉴条目 | 白鸦 | 乙 | 2026-09-20（已期满） | 21 | 1 | :material-alert: **期满 · 该处理了** |
| [002](public/002-stillwater-order.md) | 静水教团 · 势力条目 | 灰隼 | 甲 | 2026-09-26（剩 5 天） | 12 | 3 | 公示中 |

!!! note "票数怎么来"
    站点是静态的，收不了票。点赞点踩在对应公示 Issue 的 👍 / 👎 reaction 上，
    由管理员回填到稿件的 `votes_up` / `votes_down`。

---

## 待审

等管理员标记。**通过** → 移进 `public/` 并补 `public_until`；
**要求更改** → 直接删除，提交人重新提交。

| 编号 | 标题 | 提交人 | 提交日 | 目标 | 稿件 |
|---|---|---|---|---|---|
| 001 | 秘语·显位的语义边界 | 灰隼 | 2026-09-20 | `text/canon/secrets.md` | `docs/buffer/pending/001-secret-boundary.md` |

!!! warning "待审稿件不发布到站点"
    `mkdocs.yml` 配了 `draft_docs: buffer/pending/` ——
    这些稿子只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布。
    管理员标记通过、移进 `public/` 之后，站上才可见。

---

!!! danger "GitHub 链接尚未可用"
    `mkdocs.yml` 的 `repo_url` 还是 `YOURNAME` 占位，换成真实仓库地址后重跑本脚本。

