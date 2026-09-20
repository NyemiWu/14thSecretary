---
title: 条目模板
tags:
  - 元
---

# 条目模板

复制对应的一段，改内容就行。

## 设定条目

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

## 赐名怪物条目

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

[:octicons-arrow-left-24: 返回图鉴](../bestiary/index.md)
```

!!! tip "线索池写 6 条"
    阶级 1 释放 2 条，之后每失误一次多放一条，阶级 5 时全放。
    6 条刚好够推完四段秘语，且留一点推理余地。

## 工具页

```markdown
---
title: 工具名
tags:
  - 工具
---

# 工具名

一句话说明它解决什么问题。

<iframe class="demo-frame" src="../../assets/工具文件名.html" title="工具名"></iframe>

[:octicons-link-external-24: 在新标签页中打开](../assets/工具文件名.html){ .md-button .md-button--primary target=_blank }
```

!!! danger "iframe 的路径要用 `../../`"
    MkDocs 只会重写 **markdown 链接**（`[文字](../x.md)`）和 `<a href>`，
    **不会碰 `<iframe src>`**。

    本页 URL 是 `/tools/工具名/`，所以 iframe 里的相对路径是**浏览器**在算，
    要写 `../../assets/x.html` 才能回到站点根。

    同一页里的 markdown 按钮链接则相反 —— 那个交给 MkDocs 解析，
    写 `../assets/x.html` 才对。
    **两者写法不同，但都是对的。**
