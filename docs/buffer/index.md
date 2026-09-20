---
title: 审核看板
tags:
  - 元
---

# 审核看板

!!! info "本页自动生成，不要手改"
    由 `scripts/gen_board.py` 扫描 `buffer/submissions/` 与 `buffer/public/` 生成。
    稿件状态变了就跑一次：`python scripts/gen_board.py`

    流程说明见 [流程](rules.md)。

**截至 2026-09-21** —— 公示中 **2** · 待审核 **1**

## 公示中

!!! tip "公示期怎么表态"
    在对应稿件的公示 Issue 上用 **👍 / 👎** reaction 表态即可，不用打字。
    公示期满后由管理员裁决：**保留 → 并入正式分区**，**去除 → 稿件下架**。

| 编号 | 标题 | 提交人 | 审核人 | 公示截止 | 点赞 | 点踩 | 状态 |
|---|---|---|---|---|---|---|---|
| [003](public/003-ashwalker.md) | 005 灰烬行者 · 图鉴条目 | 白鸦 | 乙 | 2026-09-20（已期满） | 21 | 1 | :material-alert: 待裁决 |
| [002](public/002-stillwater-order.md) | 静水教团 · 势力条目 | 灰隼 | 甲 | 2026-09-26（剩 5 天） | 12 | 3 | 公示中 |

!!! note "票数怎么来的"
    站点是静态的，收不了票。点赞点踩在 GitHub Issue 的 reaction 上，
    由管理员回填到稿件的 `votes_up` / `votes_down` 字段。

---

## 待审核

审核请求发至 **`review@example.com`** —— 提交人提交后需自行发信，见 [流程](rules.md)。

| 编号 | 标题 | 提交人 | 提交日 | 状态 | 稿件 |
|---|---|---|---|---|---|
| 001 | 秘语·显位的语义边界 | 灰隼 | 2026-09-20 | 审核中 | `docs/buffer/submissions/001-secret-boundary.md` |

!!! warning "待审稿件不发布到站点"
    `mkdocs.yml` 配了 `draft_docs: buffer/submissions/` ——
    这些稿子只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布。
    审核通过后才移进 `buffer/public/` 进入公示，那时站上才可见。

