---
title: 条目模板
tags:
  - 元
---

# 条目模板

复制对应的一段，改内容就行。

!!! warning "先看顺序"
    写新内容 → 用「缓冲稿」模板放进 `buffer/pending/` → 管理者标记通过 → 移进 `buffer/public/`
    进入公示 → 期满删除，内容并入下面正式分区的模板。**不要跳过缓冲区。**

## 缓冲稿（pending / public 通用）

```markdown
---
title: 稿件标题
submitter: 提交人
submitted: 2026-09-21
target: text/canon/xxx.md
tags:
  - 待审
---

# 稿件标题

正文。格式按目标分区的正式模板写，期满并入时整段搬过去，不做二次改写。

## 提交说明

- 改了什么：
- 为什么改：
- 需要重点看哪几段：
```

管理者标记通过时，把文件移进 `public/` 并补 `reviewed_by` / `reviewed_on` /
`public_until`，`tags` 改成 `公示`。字段含义见 [缓冲流程](rules.md)。

!!! warning "别跳过缓冲区"
    任何新内容都先落 `buffer/pending/`。直接写进 `text/` 或 `interactive/` 等于绕过审核。

## 设定条目（文本分区）

```markdown
---
title: 条目标题
tags:
  - 板块标签
---

# 条目标题

一句话定义。这是全站其他地方引用它时应该用的说法。

## 概述

三五句话讲清它是什么、为什么存在。

## 细则

| 项 | 说明 |
|---|---|
| — | — |

## 关联

- [相关条目](../canon/xxx.md)
```

## 赐名怪物条目（文本分区）

```markdown
---
title: 0XX 称号
tags:
  - 图鉴
---

# 0XX · 称号

<div class="entry-head">
  <div class="entry-seal">L 多神 牧 火</div>
  <div class="entry-name">赐名</div>
</div>

## 观察记录

外形描述。

!!! abstract "形态摘要"
    - 行为特征一
    - 行为特征二

## 四段秘语

| 段 | 秘语 | 判定依据 |
|---|---|---|
| 一 · 倾向 | `?` | |
| 二 · 性 | `?` | |
| 三 · 途 | `?` | |
| 四 · 显 | `?` | |

## 四段式真名

1. 第一句
2. 第二句
3. 第三句
4. 第四句（含真名）

!!! success "锚定结果"
    **赐名：—**

    干扰候选：`—` · `—` · `—`

## 测名线索池

1. 线索
2. 线索
3. 线索
4. 线索
5. 线索
6. 线索

---

[:octicons-arrow-left-24: 返回图鉴](../text/bestiary/index.md)
```

!!! tip "线索池写 6 条"
    阶级 1 释放 2 条，之后每失误一次多放一条，阶级 5 时全放。
    6 条刚好够推完四段秘语，且留一点推理余地。

## 工具页（可交互叙事分区）

介绍页与同名 HTML **并排放在 `interactive/tools/`**。

```markdown
---
title: 工具名
tags:
  - 工具
---

# 工具名

一句话说明它解决什么问题。

<iframe class="demo-frame" src="../工具文件名.html" title="工具名"></iframe>

[:octicons-link-external-24: 在新标签页中打开](工具文件名.html){ .md-button .md-button--primary target=_blank }
```

!!! danger "iframe 与 markdown 链接的基准目录不同"
    `MkDocs` 处理这两者的方式**完全相反**，写成一样必错一个：

    | 写法 | 谁解析 | 按什么算 | 同级文件该写 |
    |---|---|---|---|
    | `<iframe src="...">` | **浏览器**（MkDocs 不碰） | 页面 URL 目录 | `../文件名.html` |
    | `[文字](...)` | **MkDocs** | 源文件所在目录 | `文件名.html` |

    本库的约定：**工具 HTML 一律与介绍页并排放在 `interactive/tools/`**，
    于是 iframe 恒为 `../文件名.html`、链接恒为 `文件名.html`，不随目录嵌套变化。
    放别处就得按下标深度数 `../`，很容易错。
