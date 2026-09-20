---
title: 提交指南
tags:
  - 元
---

# 提交指南

给提交人看的。三步：建稿 → 提 PR → 等审。

## 1. 建稿

在 `docs/buffer/submissions/` 下新建文件，文件名 `编号-英文短名.md`，
编号三位数、顺延不复用。

```bash
git checkout main && git pull
git checkout -b submit/012-xxx
# 新建 docs/buffer/submissions/012-xxx.md
```

头部字段这样填：

```yaml
---
title: 稿件标题
submitter: 你的代号
submitted: 2026-09-21
target: text/canon/xxx.md      # 通过后并入哪
scope: 新增                     # 新增 | 修订 | 删除
quorum: 3                       # 需要几个绿灯
mode: unanimous                 # unanimous | lazy
deadline:                       # 仅 lazy 模式填，YYYY-MM-DD
reviews:
  - who: 审核人甲
    verdict: pending
    date:
    note:
  - who: 审核人乙
    verdict: pending
    date:
    note:
tags:
  - 待审
---
```

!!! danger "三条必须遵守"
    1. **`verdict` 一律留 `pending`。** 审核人的判定由审核人自己填，你填了等于伪造。
    2. **`target` 必须指向正式分区**（`text/` 或 `interactive/`），不能指向另一个待审稿。
    3. **正文按目标分区的正式模板写。** 通过后是整段搬过去，不做二次改写 ——
       你写成什么样，上线就是什么样。

## 2. 提 PR

```bash
git add docs/buffer/submissions/012-xxx.md
git commit -m "submit(012): 稿件标题"
git push -u origin submit/012-xxx
```

然后在 GitHub 上开 PR，用默认模板填：稿件编号、目标分区、审核人名单。

## 3. 等审 / 处理打回

- **通过** → 维护者执行并入，你什么都不用做。
- **打回（有 `reject`）** → 按 `note` 里的理由改稿，然后：

```yaml
# 改完必须把所有判定重置，重新计时
reviews:
  - who: 审核人甲
    verdict: pending      # ← 从 approve / reject 改回 pending
    date:                 # ← 清空
    note:
```

!!! warning "别忘了重置"
    修订后不重置，等于用旧审核放行新内容。维护者会直接打回。

## 命名约定

| 项 | 规则 | 例 |
|---|---|---|
| 文件名 | `编号-英文短名.md` | `012-ember-pact.md` |
| 编号 | 三位数，顺延 | `012` |
| 目录 | 全 ASCII，小写，短横线分隔 | `text/canon/` |

**中文只出现在 `title` 和正文里，不进程路径。**

## 跑一次看板

改完稿子，本地跑一次让 [审核看板](index.md) 同步：

```bash
python scripts/gen_board.py
```

!!! tip "本地预览是有的，线上不会有"
    待审稿件配了 `draft_docs`，语义是「**只在 `mkdocs serve` 时构建，`mkdocs build` 不发布**」。

    - 本地：`mkdocs serve` 后访问 `/buffer/submissions/你的文件名/` 能看渲染效果。
    - 线上：**不存在**。没通过群审的内容不会上线，也搜不到。

    所以上线后的审核看板里，稿件链接指向 GitHub 原文；本地预览时可以直接点开看。
