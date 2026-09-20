---
title: 缓冲流程
tags:
  - 元
---

# 缓冲流程

**状态 = 稿件在哪个目录。** 没有别的状态字段，移动文件就是改状态。

<div class="ritual-flow">

<div class="ritual-step">
<span class="ritual-no">01</span>
<b>提交</b>
<p>新稿子一律放进 <code>buffer/pending/</code>。不发布到站点，只有仓库里能看到。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">02</span>
<b>管理者标记</b>
<p>通过 → 移进 <code>buffer/public/</code>，补上公示截止日，进入公示。<br>
要求更改 → 直接删掉稿件，提交人改完重新提交。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">03</span>
<b>公示</b>
<p>公示期挂在对应 Issue 上，大家用 👍 / 👎 表态。这时稿件在站上可见。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">04</span>
<b>期满删除</b>
<p>公示期满，<b>从缓冲区删除</b>：内容并入正式分区，或者直接丢弃。</p>
</div>

</div>

---

## 稿件在哪 = 什么状态

| 位置 | 状态 | 站上可见 | 谁能动 |
|---|---|---|---|
| `buffer/pending/` | 待审 | 否 | 提交人写，管理者标记 |
| `buffer/public/` | 公示中 | **是** | 管理者 |
| 已删除 | 流程结束 | — | — |

!!! tip "只有一条硬规则"
    正式分区（`text/` / `interactive/`）**只接受管理者从缓冲区放行的内容**。
    别直接往里写。

## 稿件抬头

```yaml
---
title: 稿件标题
submitter: 提交人
submitted: 2026-09-21
target: text/canon/xxx.md          # 期满后并入哪
tags:
  - 待审
---
```

管理者标记通过时，**在移到 `public/` 的同时补上**：

```yaml
reviewed_by: 甲                    # 审核人，会显示在看板和署名块上
reviewed_on: 2026-09-21
public_until: 2026-09-28           # 公示截止
tags:
  - 公示
```

公示期间由管理者从 Issue 回填票数（可选）：

```yaml
votes_up: 12
votes_down: 3
```

正文结构照 [条目模板](entries.md) 写。

## 两种稿件：新建 / 修改

| 类型 | 抬头里有什么 | 正文是什么 | 期满保留时怎么做 |
|---|---|---|---|
| **新建** | 只有 `target` | 新条目的完整内容 | 写入 `target` 那个路径 |
| **修改** | 多一个 `revises` | 该条目的**完整新版本** | **替换** `target` 指向的文件 |

```yaml
# 修改稿多的这一行，记的是它改的是哪一篇
revises: text/bestiary/001-ash.md
```

!!! important "修改稿不会自动改动原文"
    原文在审核放行之前**一个字都不会动**。这是有意的 ——
    谁都能提改动，但改动要经管理者确认才生效。

    成员从站上点「编辑此条目」进编辑器时，这一整套（拉原文、填 `revises`、
    把新版本落进 `pending/`）都是自动的，不用手写。

## 管理者的三个动作

**通过** —— 移进 `public/`，补 `reviewed_by` / `reviewed_on` / `public_until`，
开一个 `[公示] 编号 标题` 的 Issue，然后跑一次看板：

```bash
git mv docs/buffer/pending/012-xxx.md docs/buffer/public/012-xxx.md
# 编辑抬头
python scripts/gen_board.py
```

**要求更改** —— 直接删掉稿件，在 PR 里说明改什么。提交人改完重新提交。

**期满处理** —— 二选一，然后从缓冲区删除：

| 结果 | 动作 |
|---|---|
| **保留 · 新建稿** | 内容写进 `target` 指定的路径 → 页脚加 `.review-stamp` 署名块 → 删除缓冲稿 |
| **保留 · 修改稿** | 用稿件正文**替换** `target` 指向的文件（留意保留原文的 `media/` 等附属资源）→ 删除缓冲稿 |
| **丢弃** | 直接删除缓冲稿和公示 Issue，不留档（要看历史去翻 git log） |

!!! tip "导航不用手改"
    `nav` 由各目录的 `.pages` 驱动，新文件放进已有目录就会自动进导航。
    只有**新开一个目录**时才需要在 `docs/text/.pages` 里加一行。

!!! tip "署名块"
    并入后的正式页面页脚留痕：

    ```html
    <div class="review-stamp">
      <span class="rs-label">审核人</span>
      <span class="rs-who">甲</span>
      <span class="rs-date">2026-09-19</span>
    </div>
    ```

## 几个说明

**成员不写 Markdown 的话走 [内容后台](editor.md)。** 表单式界面，图片拖拽上传，
提交后文件直接落进 `pending/`，不用碰 git。

**待审稿不上线。** `mkdocs.yml` 里 `draft_docs: buffer/pending/` 的语义是
「只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布」。
所以提交人能本地看渲染效果，但没过审的内容不会上线、搜不到。

**票在 GitHub Issue 上。** 站点是静态的收不了票，用 Issue 的
👍 / 👎 reaction，管理员回填到稿件的 `votes_up` / `votes_down`。

**删了就没了。** 缓冲区是通道不是仓库。要走历史去翻 `git log`。
