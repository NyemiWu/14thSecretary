---
title: 可交互叙事分区
---

# 可交互叙事分区

能"玩"的内容。跑得起来的工具、能点进去的叙事 —— 一切有交互的部分。

!!! warning "同样只放已通过群审的内容"
    新稿子先进 [缓冲分区](../buffer/index.md)。工具类稿件的审核重点是
    **它会不会崩、有没有外链、能不能离线跑**，不只是文字。

---

## 已有板块

<div class="grid cards" markdown>

-   :material-tools:{ .lg .middle } __工具__

    ---

    单文件 HTML，直接内嵌在页面里跑。目前有测名台。

    [:octicons-arrow-right-24: 进入](tools/index.md)

</div>

---

## 后续下分

| 板块 | 建议路径 | 内容 | 状态 |
|---|---|---|---|
| 工具 | `interactive/tools/` | 单文件 HTML 工具（介绍页 + 同名 HTML 并排） | 已开 |
| 模组 | `interactive/modules/` | 跑团模组、章节结构 | 待开 |
| 分支叙事 | `interactive/branches/` | 树状叙事、抉择节点、结局收束 | 待开 |
| 交互场景 | `interactive/scenes/` | 可操作的场景演示 | 待开 |

---

## 工具类稿件的额外审核项

文字之外，审核人还要确认：

- [ ] **单文件**：CSS/JS 全内联，无外链 CDN（离线可用）
- [ ] **路径**：HTML 与介绍页并排、同名，iframe 写 `../文件名.html`
- [ ] **不污染站点**：没有全局 CSS 覆盖、没有 `document.body` 级改写
- [ ] **可退出**：全屏、音效之类有明确开关或边界
- [ ] **无遥测**：不发任何外部请求

!!! danger "工具 HTML 不进 `assets/`"
    放 `assets/` 就得按下标深度数 `../`，很容易错。
    和介绍页并排，路径恒为 `../文件名.html`。
    详见 [条目模板](../buffer/entries.md)。
