---
title: 首页
---

# 14thSecretary

!!! warning "骨架版本"
    分区结构、群审流程、写作规范已经定型，但**设定正文大部分是占位稿**。
    秘语体系 / 四段式真名 / 赐名流程三页来自设计表，其余等实际设定补上后替换。

---

## 三个分区

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } __文本分区__

    ---

    世界观、规则、条目。一切"读"的内容。

    [:octicons-arrow-right-24: 进入](text/index.md)

-   :material-gamepad-variant-outline:{ .lg .middle } __可交互叙事分区__

    ---

    跑得起来的工具、点得进去的叙事。一切有交互的内容。

    [:octicons-arrow-right-24: 进入](interactive/index.md)

-   :material-inbox-arrow-down:{ .lg .middle } __缓冲分区__

    ---

    待审稿件与群审看板。**新内容一律先进这里**，通过后才并入上面两个分区。

    [:octicons-arrow-right-24: 进入](buffer/index.md)

</div>

---

## 快入口

<div class="grid cards" markdown>

-   __秘语体系__

    ---

    14 条秘语、四组划分。整套赐名机制的原子单位。

    [:octicons-arrow-right-24: 进入](text/canon/secrets.md)

-   __四段式真名__

    ---

    四个秘语 + 一个真名。定位一只对象的完整写法。

    [:octicons-arrow-right-24: 进入](text/canon/true-name.md)

-   __赐名流程__

    ---

    观察 → 匹配 → 揭秘 → 锚定。

    [:octicons-arrow-right-24: 进入](text/canon/ritual.md)

-   __怪物图鉴__

    ---

    已归档的赐名怪物条目，一只一页。

    [:octicons-arrow-right-24: 进入](text/bestiary/index.md)

-   __测名台__

    ---

    可交互的测名玩法演示，直接在页面里跑。

    [:octicons-arrow-right-24: 进入](interactive/tools/naming-demo.md)

-   __群审规则__

    ---

    谁能审、门槛怎么算、通过后怎么并入。

    [:octicons-arrow-right-24: 进入](buffer/rules.md)

</div>

---

## 站点状态

| 分区 / 板块 | 状态 | 备注 |
|---|---|---|
| 文本 · 秘语体系 | :material-check-circle:{ .md .middle } 已定稿 | 来自设计表 |
| 文本 · 四段式真名 | :material-check-circle:{ .md .middle } 已定稿 | 来自设计表 |
| 文本 · 赐名流程 | :material-check-circle:{ .md .middle } 已定稿 | 来自设计表 |
| 文本 · 图鉴 | :material-progress-clock:{ .md .middle } 占位 | 4 条演示条目 |
| 可交互 · 测名台 | :material-check-circle:{ .md .middle } 可用 | 单文件 HTML，内嵌 |
| 缓冲 · 群审机制 | :material-check-circle:{ .md .middle } 已启用 | 3 份示例稿件 |
| 文本 · 世界 / 势力 / 人物 / 编年 | :material-progress-clock:{ .md .middle } 待开 | 见文本分区页 |

## 仓库怎么长

```
docs/
├─ index.md              首页
├─ text/                 文本分区 —— 纯阅读内容
│  ├─ canon/             设定：规则与体系
│  └─ bestiary/          图鉴：条目型内容
├─ interactive/          可交互叙事分区 —— 能玩的内容
│  └─ tools/             工具：介绍页 + 同名 HTML 并排
├─ buffer/               缓冲分区 —— 群审的入口
│  ├─ index.md           审核看板（脚本生成）
│  ├─ rules.md           群审规则
│  ├─ submit.md          提交指南
│  ├─ style-guide.md     编辑规范
│  ├─ entries.md         条目模板
│  └─ submissions/       待审稿件（不进导航、不进搜索）
├─ assets/               图片 / 图标
└─ stylesheets/          样式微调
```

一条内容从写到上线的完整路径：

```text
写稿 → buffer/submissions/ → 群审 → 维护者并入 → text/ 或 interactive/
```

内容只会越写越多，所以**每条设定一个文件**，不要往单页里堆。
目录名一律 ASCII，中文只出现在 `nav` 和页面标题里。
