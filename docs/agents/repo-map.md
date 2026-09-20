---
title: 仓库地图
tags:
  - 元
---

# 仓库地图

## 哪些文件是**生成的**，不许手改

这是最容易犯的错。下面这些每次构建都会被脚本重写，**手改等于白改**：

| 文件 | 谁生成 | 改了会怎样 |
|---|---|---|
| `docs/text/index.md` | `gen_section_index.py` | 下次构建被覆盖 |
| `docs/text/<板块>/index.md` | `gen_section_index.py` | 同上（含 `gallery` 那个） |
| `docs/buffer/index.md` | `gen_board.py` | 同上 |
| `site/**` | `mkdocs build` | 整个目录每次被清空重建 |

想改**板块落地页的介绍文字** → 改 `scripts/gen_section_index.py` 里的 `SECTIONS`。
想改**缓冲看板的版式** → 改 `scripts/gen_board.py` 的 `render()`。

!!! tip "怎么一眼认出生成页"
    生成的页面正文里都带一个「本页自动生成」的提示块。
    站上这些页的「编辑此条目」按钮会自动换成「在此分区新建条目」。

## 根目录

```
mkdocs.yml            站点配置：主题 / 插件 / Markdown 扩展 / 两级可见性
                      ⚠ 导航不在这里维护，见下面的 .pages
requirements.txt      依赖清单，改这个而不是单独 pip install

README.md             给人类看的仓库说明
AGENTS.md             给 agent 看的精简摘要（本分区的机器可读版）
.gitignore            site/ · *.log · _* · __pycache__/
```

## `docs/` —— 站点内容

```
docs/
├─ .pages               顶层导航（4 个分区）
├─ index.md             首页（手写）
│
├─ text/                文本分区 —— 纯阅读内容
│  ├─ .pages            12 个板块的顺序与中文名
│  ├─ index.md          ⚙ 生成
│  ├─ <板块>/
│  │  ├─ index.md       ⚙ 生成（条目表 + 摘要）
│  │  ├─ xxx.md         正式条目（手写 / 从缓冲区并入）
│  │  └─ media/<slug>/  该文档的内嵌图（由 pandoc 提取）
│  └─ gallery/          特殊：index.md 里是图片网格，图在 docs/assets/gallery/
│
├─ interactive/         可交互叙事分区 —— 能玩的东西
│  ├─ .pages
│  ├─ index.md
│  └─ tools/
│     ├─ .pages
│     ├─ index.md       工具清单（手写）
│     ├─ xxx.md         介绍页
│     └─ xxx.html       工具本体（与介绍页**并排同名**，iframe 内嵌）
│
├─ buffer/              缓冲分区 —— 通道，不是仓库
│  ├─ .pages
│  ├─ index.md          ⚙ 生成：缓冲看板
│  ├─ rules.md          流程说明
│  ├─ editor.md         内容后台使用说明
│  ├─ style-guide.md    编辑规范
│  ├─ entries.md        三套条目模板
│  ├─ pending/          待审稿件 —— draft_docs，只在本地 serve 构建
│  └─ public/           公示稿件 —— 正常发布，但不进导航
│
├─ editor/              内容后台本体（单文件 HTML，零外部依赖）
│  └─ index.html
│
├─ agents/              机哥分区 —— 就是这一区
│
├─ javascripts/
│  └─ edit-entry.js     往每个内容页注入「编辑此条目」按钮
│
├─ assets/
│  ├─ gallery/          图库原图（35 张，共约 127MB）
│  ├─ uploads/          内容后台拖拽上传的图（不入库就会是空目录）
│  └─ sigil.svg         logo / favicon
│
└─ stylesheets/
   └─ extra.css         全部自定义样式
```

## `scripts/` —— 生成与导入

| 脚本 | 干什么 | 支持 `--check` |
|---|---|---|
| `gen_section_index.py` | 扫 `docs/text/*` 生成各板块落地页 + 文本分区总目录 | ✅ |
| `gen_board.py` | 扫 `docs/buffer/{pending,public}` 生成缓冲看板 | ✅ |
| `import_kb.py` | 批量把 `.docx`/`.html`/`.md` 转成站点内容（pandoc） | — |
| `import_doc.py` | 老格式 `.doc`（OLE2）提取纯文本 | — |
| `fix_kb_links.py` | 修 Word 交叉引用留下的死链 | — |

`import_*` 三个是**一次性导入工具**，只在重新导入知识库时才用。
它们吃的是 `C:\Users\ROG\Documents\项目文档\14th\十四号城项目20260921打包` 那个源包。
`*_report.txt` 是它们的运行报告，留着当记录。

## `.github/`

```
workflows/deploy.yml            唯一的部署工作流（MkDocs → Pages）
CODEOWNERS                      审核权限名单
PULL_REQUEST_TEMPLATE.md        投稿 PR 模板
```

!!! danger "workflows 目录下只允许有一个文件"
    GitHub 的 Pages 设置页会推销一个 Jekyll 起始工作流。
    一旦它进来，两个工作流抢同一个 `pages` 并发组，**站点会随机被覆盖**。
    加/改工作流后一定确认：`GET /repos/{owner}/{repo}/actions/workflows` 的 `total_count` 是 1。
    详见[已知坑](pitfalls.md)。

## 关键配置在哪

| 想改什么 | 去哪 |
|---|---|
| 站点名 / 域名 / 仓库链接 | `mkdocs.yml` 顶部 |
| 顶层导航 | `docs/.pages` |
| 板块顺序与中文名 | `docs/text/.pages` |
| 板块的简介文字 | `scripts/gen_section_index.py` 的 `SECTIONS` |
| 哪些目录不发布 / 不进导航 | `mkdocs.yml` 的 `draft_docs` / `not_in_nav` |
| 主题色 / 字体 / 自定义组件 | `docs/stylesheets/extra.css` |
| 内容页的编辑入口行为 | `docs/javascripts/edit-entry.js` |
| 投稿表单字段 | `docs/editor/index.html` |
