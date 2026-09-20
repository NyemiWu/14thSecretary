---
title: 首页
---

# 14thSecretary · 设定集

!!! warning "骨架版本"
    目录结构与写作规范已经定型，但**设定正文全部是占位稿**。
    秘语体系一节直接取自设计表，其余内容等实际设定补上后替换即可。

---

## 从哪儿开始

<div class="grid cards" markdown>

-   :material-book-cipher:{ .lg .middle } __秘语体系__

    ---

    14 条秘语、四组划分。整套赐名机制的原子单位都在这里。

    [:octicons-arrow-right-24: 进入](canon/secrets.md)

-   :material-format-letter-case:{ .lg .middle } __四段式真名__

    ---

    四个秘语 + 一个真名。定位一只怪物的完整写法与格式规范。

    [:octicons-arrow-right-24: 进入](canon/true-name.md)

-   :material-eye-outline:{ .lg .middle } __赐名流程__

    ---

    观察对象 → 匹配秘语 → 揭秘真名 → 锚定赐名。

    [:octicons-arrow-right-24: 进入](canon/ritual.md)

-   :material-book-open-page-variant:{ .lg .middle } __怪物图鉴__

    ---

    已归档的赐名怪物条目。

    [:octicons-arrow-right-24: 进入](bestiary/index.md)

-   :material-tools:{ .lg .middle } __测名台__

    ---

    可交互的测名玩法演示，直接在页面里跑。

    [:octicons-arrow-right-24: 进入](tools/naming-demo.md)

-   :material-pencil-ruler:{ .lg .middle } __编辑规范__

    ---

    目录规则、命名规则、条目模板。写新页面前先读这页。

    [:octicons-arrow-right-24: 进入](meta/style-guide.md)

</div>

---

## 站点状态

| 板块 | 状态 | 备注 |
|---|---|---|
| 秘语体系 | :material-check-circle:{ .md .middle } 已定稿 | 直接来自设计表 |
| 四段式真名 | :material-check-circle:{ .md .middle } 已定稿 | 直接来自设计表 |
| 赐名流程 | :material-check-circle:{ .md .middle } 已定稿 | 直接来自设计表 |
| 怪物图鉴 | :material-progress-clock:{ .md .middle } 占位 | 4 条演示条目 |
| 世界设定 | :material-progress-clock:{ .md .middle } 待补 | 目录已留位 |
| 测名台 | :material-check-circle:{ .md .middle } 可用 | 单文件 HTML，内嵌 |

## 这个仓库怎么长

```
docs/
├─ index.md              首页
├─ canon/                设定：从原子规则往上搭
├─ bestiary/             图鉴：已归档的怪物条目
├─ tools/                工具：可交互页面
├─ meta/                 编辑规范与模板
├─ assets/               图片 / 附件 / 独立 HTML
└─ stylesheets/          样式微调
```

内容只会越写越多，所以**每条设定一个文件**，不要往单页里堆。目录名用英文，中文标题写在 `mkdocs.yml` 的 `nav` 和页面的 `# 标题` 里。
