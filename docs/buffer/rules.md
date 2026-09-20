---
title: 群审规则
tags:
  - 元
---

# 群审规则

所有新内容先进**缓冲分区**，群审通过才并入正式分区。

<div class="ritual-flow">

<div class="ritual-step">
<span class="ritual-no">01</span>
<b>提交</b>
<p>提交人把稿子放到 <code>buffer/submissions/</code>，按模板写好头部字段，<code>verdict</code> 全部留 <code>pending</code>。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">02</span>
<b>群审</b>
<p>名单内的审核人各自读稿，在自己的那一行填 <code>approve</code> / <code>reject</code> / <code>abstain</code>，并留一句理由。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">03</span>
<b>判定</b>
<p>达到门槛即通过；出现任一 <code>reject</code> 即打回，提交人修订后所有判定重置、重新审。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">04</span>
<b>并入</b>
<p>维护者把稿件挪进正式分区，去掉审核字段，页脚留下审核人署名。</p>
</div>

</div>

---

## 三种角色

| 角色 | 权限 | 能做 | 不能做 |
|---|---|---|---|
| **提交人** | 仓库写权限 | 往 `buffer/submissions/` 建稿、修订自己的稿 | 填自己的 `verdict`；直接改正式分区 |
| **审核人** | 名单内（见 `.github/CODEOWNERS`） | 填自己的 `verdict`；在 PR 上 review | 审自己提交的稿 |
| **维护者** | 审核人之一 | 执行并入、改 `nav`、合并 PR | 跳过门槛强行并入 |

!!! danger "权限是**双保险**"
    文档里写的规则是**约定**；真正拦住人的是 GitHub 那一侧：
    分支保护 + CODEOWNERS 强制审查。两边都要配，只配一边等于没配。

## 判定字段

稿件头部的 `reviews` 是审核台账，一人一行：

```yaml
reviews:
  - who: 审核人甲
    verdict: approve
    date: 2026-09-21
    note: 秘语四段判定没问题
```

| `verdict` | 含义 |
|---|---|
| `pending` | 未审（默认值） |
| `approve` | 绿灯 |
| `reject` | 反对，必须写 `note` 说明理由 |
| `abstain` | 弃权，不计入通过数也不阻断 |

## 通过门槛

头部用 `mode` 选一种：

=== "unanimous · 全票通过"

    **名单内所有审核人都 `approve`** 才算通过。只要有一人还是 `pending`，就是没通过 ——
    不设沉默期。

    适合：会改动既有设定、影响面大的稿件。

=== "lazy · 沉默期通过"

    到 `deadline` 时，**没人 `reject`** 且 `approve` 数 ≥ `quorum` 即通过。
    `deadline` 到期前没人表态，视为无异议。

    适合：新增条目、措辞修订这类低风险改动。

!!! warning "`abstain` 不算通过数"
    弃权既不加分也不扣分。全票模式下弃权者视为已表态，不阻断；
    沉默期模式下弃权不计入 `quorum`。

## 状态推导

```text
有任意 reject            → changes   （打回，判定全部重置）
approve 数 ≥ quorum 且满足模式条件 → approved  （待并入）
其余                     → pending
```

!!! tip "修订后要重置"
    打回后提交人改了稿，**所有 `verdict` 必须重置回 `pending`**、
    `date` 清空、重新计时。否则会出现"用旧绿灯放行新内容"。

## 并入动作（维护者）

```bash
# 1. 确认状态 approved（看板 + PR 双绿）
# 2. 挪到正式分区
git mv docs/buffer/submissions/012-xxx.md docs/text/canon/xxx.md

# 3. 去掉群审字段，只留 title / tags，并在页脚加审核署名块
# 4. 在 mkdocs.yml 的 nav 加一行
# 5. 提交
git commit -m "merge(review): 稿件标题 · 审核 甲/乙/丙 (#12)"
```

## 审核署名

并入后的正式页面，**页脚必须留下审核人**：

```html
<div class="review-stamp">
  <span class="rs-label">群审通过</span>
  <span class="rs-who">甲 · 乙 · 丙</span>
  <span class="rs-date">2026-09-23</span>
</div>
```

对应 `head` 里保留：

```yaml
reviewed_by:
  - 甲
  - 乙
  - 丙
reviewed_on: 2026-09-23
```

## 稿件可见性

| 位置 | 本地 `mkdocs serve` | 线上站点 | 谁能看见 |
|---|---|---|---|
| `buffer/submissions/*.md` | ✅ 可读渲染稿 | ❌ **不发布** | 仓库成员 |
| `buffer/index.md` 审核看板 | ✅ | ✅ | 所有人 |
| `buffer/rules.md` 等规则页 | ✅ | ✅ | 所有人 |
| `text/` `interactive/` 正式条目 | ✅ | ✅ | 所有人 |

!!! note "为什么要这样"
    `mkdocs.yml` 里配了 `draft_docs: buffer/submissions/`，它的语义是
    **「只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布」**。

    于是：提交人能本地看渲染效果 → 未过审的内容不会上线、搜不到 →
    上线后的看板里，稿件链接指向 GitHub 原文，代码评审就在那里做。

## GitHub 侧配置

**1. `.github/CODEOWNERS`** —— 定义谁有权限审哪些路径（本库已附）：

```text
/docs/buffer/                 @维护者
/docs/text/                   @维护者
/docs/interactive/            @维护者
```

**2. 分支保护** —— `Settings → Branches → Add rule`，对 `main`：

- ✅ Require a pull request before merging
- ✅ Require approvals：**1**（或按 `quorum` 调）
- ✅ Require review from Code Owners
- ✅ Dismiss stale pull request approvals when new commits are pushed
  —— 这条最关键，对应上面「修订后重置」
- ✅ Do not allow bypassing the above settings

**3. PR 模板** —— `.github/PULL_REQUEST_TEMPLATE.md`（本库已附），
让提交人自己填稿件编号、目标分区、审核人名单。

!!! note "看板是自动生成的"
    [审核看板](index.md) 由 `scripts/gen_board.py` 扫描
    `buffer/submissions/` 的头部字段生成。改完稿件跑一次：

    ```bash
    python scripts/gen_board.py
    ```

    它只写 `docs/buffer/index.md` 这一个文件。
