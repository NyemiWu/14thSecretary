---
title: 任务手册
tags:
  - 元
---

# 任务手册

六种常见任务的步骤化做法。**每一步都给了验证方法** —— 别做完就跑，先验。

---

## 一、加一篇正式条目

!!! danger "不要直接写进 `text/`"
    任何新内容都要先进缓冲区。直接往正式分区写等于绕过审核，
    这是这个仓库唯一的一条硬规则。

**1. 起草**（二选一）

=== "走内容后台"

    打开 `/editor/`，填表 → 提交。稿件自动落进 `docs/buffer/pending/`。

=== "手写 Markdown"

    按 [条目模板](../buffer/entries.md) 写一份，抬头至少要有：

    ```yaml
    ---
    title: 条目标题
    submitter: 你的代号
    submitted: 2026-09-21
    target: text/<板块>/<文件名>.md
    tags:
      - 待审
    ---
    ```

    存成 `docs/buffer/pending/<三位编号>-<英文短名>.md`。

**2. 管理员通过**

```bash
# 移进公示区，并在抬头补 reviewed_by / reviewed_on / public_until
git mv docs/buffer/pending/012-xxx.md docs/buffer/public/012-xxx.md
python scripts/gen_board.py
```

**3. 期满保留**

把正文写进 `target` 指的路径 → 页脚可选加 `.review-stamp` 署名块 → 删掉缓冲稿。

**4. 验证**

```bash
python -m mkdocs build                 # 零 WARNING
python scripts/gen_board.py --check    # exit 0
```

导航**不用手改** —— 放进已有目录就自动进导航（`.pages` 驱动）。

---

## 二、新增一个板块

**1. 建目录**：`docs/text/<英文短名>/`（**只能 ASCII**），把文档放进去。

**2. 注册板块**：改 `scripts/gen_section_index.py` 的 `SECTIONS`，加一行
`("<英文短名>", "<中文名>", "<一句话简介>")`。**顺序决定导航里的顺序。**

**3. 注册导航**：改 `docs/text/.pages`，加一行 `- <中文名>: <英文短名>`。

**4. （可选）子分组标签**：新目录下如果有子文件夹，在 `gen_section_index.py` 的
`SUBDIR_LABEL` 里加中文标签；不想让它出现在落地页就标成 `None`。

**5. 生成 + 验证**

```bash
python scripts/gen_section_index.py
python -m mkdocs build
```

落地页会出现在 `docs/text/<英文短名>/index.md`（**生成物，别手改**）。

---

## 三、改导航

| 改什么 | 改哪 |
|---|---|
| 顶层四个分区 | `docs/.pages` |
| 文本分区的板块顺序 / 中文名 | `docs/text/.pages` |
| 板块内部的条目顺序 | 该目录的 `.pages`（没有就用文件名序） |
| 工具列表 | `docs/interactive/tools/.pages` |

`.pages` 的格式：

```yaml
nav:
  - index.md          # 不带标题 = 成为该层级的落地页
  - 中文名: 目录名或文件名
```

**绝大多数情况不用改导航** —— 新文档放进已有目录会自动出现。

---

## 四、加一个可交互工具

**1. 工具 HTML 和介绍页**并排放进 `docs/interactive/tools/`，**同名**：

```
docs/interactive/tools/我的工具.html     ← 工具本体
docs/interactive/tools/我的工具.md       ← 介绍页，iframe 内嵌
```

!!! danger "必须并排同名，否则相对路径必错"
    MkDocs **不会**重写 `<iframe src>`，但会重写 markdown 链接 ——
    两种写法的基准目录不一样。并排同名能让两个基准都退化成浅路径：

    ```markdown
    <!-- iframe：浏览器算，同级写 ../ -->
    <iframe class="demo-frame" src="../我的工具.html" title="我的工具"></iframe>

    <!-- markdown 按钮：MkDocs 算，同级写裸文件名 -->
    [:octicons-link-external-24: 在新标签页打开](我的工具.html){ .md-button target=_blank }
    ```

    写成一样必错一个。详见[已知坑](pitfalls.md)。

**2. 注册导航**：加进 `docs/interactive/tools/.pages`。

**3. 验证**：`mkdocs build` 零 WARNING，然后打开页面确认 iframe 真能加载。

---

## 五、改站点样式

**全部自定义样式在 `docs/stylesheets/extra.css`**，没有 theme override 目录。

- 颜色 / 字体：文件顶部的 `:root` 和 `[data-md-color-scheme="slate"]`
- 组件：按 `/* ---------- 名字 ---------- */` 分节，加在对应节或文件末尾
- **不要引入外部 CSS 框架或 CDN 字体** —— 这个站是零外部依赖的

改完 `mkdocs build`，然后**用浏览器实际看**。构建通过不代表样式对。

---

## 六、重新导入知识库文档

只在源包更新时才做。**先 commit 一个安全点**（导入脚本会覆盖大量文件）。

```bash
python scripts/import_kb.py            # .docx/.html/.md → Markdown（pandoc）
python scripts/import_doc.py           # 老格式 .doc → 纯文本
python scripts/gen_section_index.py    # 重建落地页
python scripts/fix_kb_links.py         # 修交叉引用死链
```

`import_kb.py` 支持 `--dry-run` 看计划。每次都会写 `scripts/import_*_report.txt`。

把源包路径写死在脚本里了（`C:\Users\ROG\Documents\项目文档\14th\...`），
换机器要改脚本顶部的常量。

---

## 通用收尾

不管做哪种，最后都跑一遍：

```bash
python scripts/gen_board.py
python scripts/gen_section_index.py
python -m mkdocs build            # ← 看有没有 WARNING
git status --short                # ← 确认没有临时文件
git add -A && git commit -m "..." && git push origin main
```

CI 会在服务端再跑一次两个生成脚本，所以**本地跑不跑都不影响线上正确性**，
但本地跑能提前发现坏链和遗漏。
