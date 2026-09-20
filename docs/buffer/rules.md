---
title: 流程
tags:
  - 元
---

# 流程

四步。没有别的。

<div class="ritual-flow">

<div class="ritual-step">
<span class="ritual-no">01</span>
<b>提交</b>
<p>把稿子放进 <code>buffer/submissions/</code>，抬头写 <code>status: submitted</code>。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">02</span>
<b>@邮箱请求审核</b>
<p>提交后发一封审核请求到 <code>review@example.com</code>。审核人过 / 不过。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">03</span>
<b>进公示</b>
<p>通过后移进 <code>buffer/public/</code>，<code>status: public</code>，站上可见。公示期自由点赞点踩。</p>
</div>

<div class="ritual-step">
<span class="ritual-no">04</span>
<b>管理员裁决</b>
<p>公示期满，管理员决定 <b>保留</b>（并入正式分区）还是 <b>去除</b>（下架）。</p>
</div>

</div>

---

## 状态

一个字段 `status` 走完全程，手动改。

| `status` | 含义 | 放哪 | 站上可见 |
|---|---|---|---|
| `submitted` | 已提交，还没发审核请求 | `submissions/` | 否 |
| `reviewing` | 审核中（已发请求） | `submissions/` | 否 |
| `public` | **公示中** | `public/` | **是** |
| `merged` | 已并入正式分区 | 稿件删除 | 正文在正式分区 |
| `removed` | 管理员去除 | 稿件删除 | 否 |

## 稿件抬头

只有这些字段：

```yaml
---
title: 稿件标题
submitter: 提交人
submitted: 2026-09-21
target: text/canon/xxx.md        # 通过后并入哪
notify: review@example.com       # 审核请求邮箱
status: submitted                # 见上表
# 审核通过后补：
reviewed_by: 审核人
reviewed_on: 2026-09-21
public_until: 2026-09-28         # 公示截止
# 公示期间由管理员从 Issue 回填：
votes_up: 12
votes_down: 3
---
```

改完状态跑一次看板：

```bash
python scripts/gen_board.py
```

## 审核请求邮件

提交后发给 `review@example.com`（改地址要同时改 `mkdocs.yml` 的 `extra.review_email`）：

```text
主题：[审核] 012 稿件标题

稿件：docs/buffer/submissions/012-xxx.md
目标：text/canon/xxx.md
范围：新增
一句话：这条补充了什么、为什么要补
```

## 公示怎么表态

静态站点收不了票，所以**票在 GitHub Issue 上**：

- 每份进入公示的稿件开一个 Issue，标题 `[公示] 012 稿件标题`
- 表态用 reaction：👍 赞成 / 👎 反对，不用打字
- 管理员公示期满把票数抄进稿件的 `votes_up` / `votes_down`，再跑看板

## 管理员裁决

| 结果 | 动作 |
|---|---|
| **保留** | 稿件移进 `target` 指定的路径 → 按 [条目模板](entries.md) 收紧格式 → 页脚加 `.review-stamp` 署名块 → 在 `mkdocs.yml` 的 `nav` 加一行 → 删掉缓冲分区的稿件 |
| **去除** | 直接删掉稿件和公示 Issue，不留档（要看历史去翻 git log） |

!!! tip "署名块"
    并入后的正式页面页脚留痕：

    ```html
    <div class="review-stamp">
      <span class="rs-label">审核通过</span>
      <span class="rs-who">甲</span>
      <span class="rs-date">2026-09-19</span>
    </div>
    ```

## 谁能审

审核人名单在 `.github/CODEOWNERS`。配合 main 分支保护
（Require PR + Require review from Code Owners）才拦得住人 ——
光在文档里写没用。

## 待审稿件不上线

`mkdocs.yml` 里 `draft_docs: buffer/submissions/` 的语义是
**只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布**。

所以提交人能本地看渲染效果，但没过审的内容不会上线、搜不到。
审核通过移进 `public/` 之后才可见 —— 公示的意义就在于能被看到。
