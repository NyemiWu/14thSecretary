---
title: 工具
---

# 工具

可交互的页面。都是单文件 HTML，不依赖后端，跟介绍页并排放在 `docs/interactive/tools/`。

<div class="grid cards" markdown>

-   :material-eye-check-outline:{ .lg .middle } __测名台__

    ---

    赐名流程的可玩演示。观察 → 匹配 → 揭秘 → 锚定，完整跑一遍。

    [:octicons-arrow-right-24: 打开](naming-demo.md)

-   :material-account-multiple-plus-outline:{ .lg .middle } __COC7 版车卡工具__

    ---

    第七版角色卡创建与修改。属性掷骰、技能分配、角色码导入导出。

    [:octicons-arrow-right-24: 打开](COC7版车卡工具.md)

-   :material-map-outline:{ .lg .middle } __战图工具 · KP 端__

    ---

    战斗场景的地图与棋子管理，守秘人这一侧。

    [:octicons-arrow-right-24: 打开](COC7版战图工具-KP端.md)

-   :material-eye-settings-outline:{ .lg .middle } __战图工具 · 玩家端__

    ---

    受限视野的战图视图，看不见 KP 没让看见的东西。

    [:octicons-arrow-right-24: 打开](COC7版战图工具-玩家端.md)

</div>

---

## 加新工具的方式

1. 把单文件 HTML 放到 `docs/interactive/tools/`，**和它的介绍页并排、同名**。
2. 建一个同名 `.md`，用 iframe 内嵌（`src` 永远写 `../文件名.html`）。
3. 导航会自动长出来（`docs/interactive/tools/.pages` 里加一行就行）。

为什么不放 `assets/`：iframe 的相对路径是**浏览器**算的，页面嵌套越深 `../` 越多。
和 `.md` 并排，路径永远是 `../`，不会错。详见 [条目模板](../../buffer/entries.md)。
