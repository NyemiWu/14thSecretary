---
title: 首页
---

# 14thSecretary

!!! warning "刚导入知识库，正文还在校对"
    11 个板块、100+ 篇文档已从原始 `.docx` 批量转换进来。
    **Word 里的加粗标题大多不会变成 Markdown 标题**，层级可能不齐；
    4 个老格式 `.doc` 是纯文本提取，表格和格式有损失。
    读到不对的地方直接在页面上改（右上角有编辑入口）。

---

## 四个分区

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } __文本分区__

    ---

    世界观、社会、地区、阵营、人物、图鉴、编年史、剧情 —— 一切「读」的内容。

    [:octicons-arrow-right-24: 进入](text/index.md)

-   :material-gamepad-variant-outline:{ .lg .middle } __可交互叙事分区__

    ---

    跑得起来的工具。测名台、COC7 车卡与战图。

    [:octicons-arrow-right-24: 进入](interactive/index.md)

-   :material-inbox-arrow-down:{ .lg .middle } __缓冲分区__

    ---

    新内容一律先进这里。**状态 = 它在哪个目录**：待审 → 标记通过 → 公示 → 期满删除。

    [:octicons-arrow-right-24: 进入](buffer/index.md)

-   :material-robot-outline:{ .lg .middle } __机哥分区__

    ---

    写给 AI 助手的：上手、仓库地图、任务手册、硬规则、已知坑。
    **后续 skill 与 agent 相关的内容都更新在这里。**

    [:octicons-arrow-right-24: 进入](agents/index.md)

</div>

---

## 文本分区的十二个板块

| 板块 | 里面有什么 |
|---|---|
| [设定](text/canon/index.md) | 秘语体系、四段式真名、赐名流程 |
| [世界观](text/worldview/index.md) | 意识、意识海、仿生人、识子论、意识工学 |
| [社会结构与体制](text/society/index.md) | 社会状况、意识形态、片区规划、食品 |
| [地区](text/regions/index.md) | 穹顶城内外、十三号城、西伯利亚穹顶城 |
| [阵营势力](text/factions/index.md) | 仿研所、穹顶政联、至高联合、商会…… |
| [人物角色](text/characters/index.md) | 角色设定与设定卡 |
| [图鉴](text/bestiary/index.md) | 赐名怪物、意识生物、人工智能 |
| [编年史](text/chronicle/index.md) | 从市元前到 2058 年 |
| [前传](text/prequel/index.md) | 前传游戏的策划案、剧本、医疗与技术文档 |
| [剧情](text/story/index.md) | 主线、北岸篇、其他文本 |
| [图库](text/gallery/index.md) | 概念设定、角色设计、地图 |
| [项目管理](text/project/index.md) | 内部目标与排期 |

每个板块的落地页会自动列出该板块全部条目和摘要。

---

## 两条硬规则

**一、内容先进缓冲区。**
任何新稿子都放 `buffer/pending/`，由管理者标记通过、走完公示才并入正式分区。
[不写 Markdown 的成员走内容后台](buffer/editor.md)，表单式 + 拖拽传图。

**二、目录和文件名用 ASCII，中文只出现在标题里。**
这条在知识库导入时**有意破例**了 —— 一百多篇文档保持原文件名才能和你手上的包对上。
新写的文档请遵守。

## 仓库怎么长

```
docs/
├─ index.md              首页
├─ text/                 文本分区（12 个板块）
│  └─ <板块>/             index.md（自动生成）+ 各篇文档 + media/
├─ interactive/          可交互叙事分区
│  └─ tools/              介绍页 + 同名 HTML 并排
├─ buffer/               缓冲分区 —— 通道，不是仓库
│  ├─ index.md            缓冲看板（脚本生成）
│  ├─ rules.md            流程
│  ├─ editor.md           内容后台说明
│  ├─ pending/            待审（不发布）
│  └─ public/             公示中（站上可见）
├─ editor/               内容后台本体（纯静态，零外部依赖）
├─ agents/               机哥分区 —— 给 AI 助手的上手与运维文档
├─ javascripts/          edit-entry.js（内容页的编辑入口按钮）
├─ assets/               gallery（图库原图）/ uploads（后台上传）
└─ stylesheets/
```

## 会用到的脚本

| 脚本 | 干什么 |
|---|---|
| `scripts/import_kb.py` | `.docx` / `.html` 批量转 Markdown（pandoc） |
| `scripts/import_doc.py` | 老格式 `.doc` 提取纯文本（无 pandoc 支持） |
| `scripts/fix_kb_links.py` | 修 Word 里残留的交叉引用死链 |
| `scripts/gen_section_index.py` | 生成各板块落地页 |
| `scripts/gen_board.py` | 生成缓冲看板 |
