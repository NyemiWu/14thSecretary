---
title: 审核看板
tags:
  - 元
---

# 审核看板

!!! info "本页自动生成，不要手改"
    由 `scripts/gen_board.py` 扫描 `buffer/submissions/` 生成。
    提交或修订稿件后跑一次：`python scripts/gen_board.py`

    判定规则见 [群审规则](rules.md)，字段写法见 [提交指南](submit.md)。

!!! warning "待审稿件不会发布到站点"
    `mkdocs.yml` 里配了 `draft_docs: buffer/submissions/` ——
    这些稿子**只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布**。
    所以上线的看板里，稿件链接指向 GitHub 原文；本地预览时可以直接读渲染稿。

**截至 2026-09-21** —— 待审 **1** · 待并入 **1** · 已打回 **1**

!!! danger "GitHub 链接尚未可用"
    `mkdocs.yml` 里的 `repo_url` 还是 `YOURNAME` 占位，换成真实仓库地址后重跑本脚本，稿件直链才会生效。

## 总览

| 编号 | 标题 | 提交人 | 目标 | 模式 | 门槛 | 状态 |
|---|---|---|---|---|---|---|
| 002 | 静水教团 · 势力条目 | 灰隼 | `text/canon/factions/stillwater.md`（新增） | 沉默期 | 0/2 | :material-arrow-u-left-top: 已打回 |
| 001 | 秘语·显位的语义边界 | 灰隼 | `text/canon/secrets.md`（修订） | 全票 | 1/3 | :material-progress-clock: 待审 |
| 003 | 005 灰烬行者 · 图鉴条目 | 白鸦 | `text/bestiary/005-ashwalker.md`（新增） | 全票 | 3/3 | :material-check-decagram: 待并入 |

---

## 明细

### 002 · 静水教团 · 势力条目

**状态：:material-arrow-u-left-top: 已打回** —— 有反对票，打回重审

| 项 | 值 |
|---|---|
| 提交人 | 灰隼 |
| 提交日 | 2026-09-19 |
| 目标 | `text/canon/factions/stillwater.md` |
| 范围 | 新增 |
| 沉默期截止 | 2026-09-26 |
| 稿件原文 | `docs/buffer/submissions/002-stillwater-order.md` |
| 本地预览 | `mkdocs serve` 后访问 `/buffer/submissions/002-stillwater-order/` |

| 审核人 | 判定 | 日期 | 意见 |
|---|---|---|---|
| 甲 | :material-close: 反对 | 2026-09-20 | 与 002 号图鉴条目「静水之下」的定位冲突。这里写教团主动驯养沉钟，但图鉴里它是受更深处的存在牵引、无自主意志的。先和图鉴组对齐「谁在牵线」再提交。 |
| 乙 | :material-dots-horizontal: 待审 | — | — |

### 001 · 秘语·显位的语义边界

**状态：:material-progress-clock: 待审** —— 全票模式，1/3 绿灯

| 项 | 值 |
|---|---|
| 提交人 | 灰隼 |
| 提交日 | 2026-09-18 |
| 目标 | `text/canon/secrets.md` |
| 范围 | 修订 |
| 稿件原文 | `docs/buffer/submissions/001-secret-boundary.md` |
| 本地预览 | `mkdocs serve` 后访问 `/buffer/submissions/001-secret-boundary/` |

| 审核人 | 判定 | 日期 | 意见 |
|---|---|---|---|
| 甲 | :material-check: 绿灯 | 2026-09-19 | 边界定义清楚，与四段式真名的对应关系没问题。 |
| 乙 | :material-dots-horizontal: 待审 | — | — |
| 丙 | :material-dots-horizontal: 待审 | — | — |

### 003 · 005 灰烬行者 · 图鉴条目

**状态：:material-check-decagram: 待并入** —— 全员绿灯 3/3

| 项 | 值 |
|---|---|
| 提交人 | 白鸦 |
| 提交日 | 2026-09-19 |
| 目标 | `text/bestiary/005-ashwalker.md` |
| 范围 | 新增 |
| 稿件原文 | `docs/buffer/submissions/003-ashwalker.md` |
| 本地预览 | `mkdocs serve` 后访问 `/buffer/submissions/003-ashwalker/` |

| 审核人 | 判定 | 日期 | 意见 |
|---|---|---|---|
| 甲 | :material-check: 绿灯 | 2026-09-20 | 六条线索递进合理，判位都能从线索反推。真名藏在第四句，符合写作规范。 |
| 乙 | :material-check: 绿灯 | 2026-09-20 | 牧 / 祝 的区分沿用 001 号稿件的边界规则，判为「牧」是对的。 |
| 丙 | :material-check: 绿灯 | 2026-09-21 | 无异议。 |

