---
title: 工具
---

# 工具

可交互的页面。都是单文件 HTML，不依赖后端，直接放进 `docs/assets/` 就能跑。

<div class="grid cards" markdown>

-   :material-eye-check-outline:{ .lg .middle } __测名台__

    ---

    赐名流程的可玩演示。观察 → 匹配 → 揭秘 → 锚定，完整跑一遍。

    [:octicons-arrow-right-24: 打开](naming-demo.md)

</div>

---

## 加新工具的方式

1. 把单文件 HTML 放到 `docs/interactive/tools/`，**和它的介绍页并排、同名**。
2. 建一个同名 `.md`，用 iframe 内嵌（`src` 永远写 `../文件名.html`）。
3. 在 `mkdocs.yml` 的 `nav → 可交互叙事分区 → 工具` 下加一行。

为什么不放 `assets/`：iframe 的相对路径是**浏览器**算的，页面嵌套越深 `../` 越多。
和 `.md` 并排，路径永远是 `../`，不会错。详见 [条目模板](../../buffer/entries.md)。
