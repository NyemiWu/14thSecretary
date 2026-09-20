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

1. 把单文件 HTML 放到 `docs/assets/`，文件名用英文短横线。
2. 在 `docs/tools/` 建一个同名 `.md`，用 iframe 内嵌。
3. 在 `mkdocs.yml` 的 `nav → 工具` 下加一行。

模板见 [条目模板](../meta/templates.md)。
