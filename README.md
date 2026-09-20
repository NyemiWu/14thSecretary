# 14thSecretary

设定集 wiki。基于 **MkDocs + Material**，内容全是 Markdown，构建成一堆静态页面发布到 GitHub Pages。

## 本地跑起来

```bash
# 安装（只做一次）
pip install -r requirements.txt

# 本地预览 —— 浏览器打开 http://127.0.0.1:8000，改文件即时刷新
mkdocs serve

# 构建到 site/ 检查产物
mkdocs build
```

## 内容怎么上线

**推送到 `main` 就自动发布**，不需要任何人跑命令。

`.github/workflows/deploy.yml` 会在每次 main 更新时：刷新看板与板块落地页 → 构建 → 发布到 Pages。
所以成员通过 `/editor/` 提交稿件后，直接 commit 到 main 就已经触发上线链路。

本地跑 `mkdocs build` 只是为了**在推之前自查**（有没有坏链、页面渲染正不正常）。

首次需要手动开一次：仓库 `Settings → Pages → Build and deployment → Source` 选 **GitHub Actions**。

## 目录

```
mkdocs.yml                   站点配置（导航由各目录的 .pages 驱动，不在这里维护）
requirements.txt             依赖清单
scripts/                     导入与生成脚本（见下）
.github/                     CODEOWNERS（审核权限名单）+ PR 模板
docs/
├─ index.md                  首页
├─ text/                     文本分区 —— 12 个板块
│  ├─ canon/                 设定：秘语体系、四段式真名、赐名流程
│  ├─ worldview/             世界观
│  ├─ society/               社会结构与体制
│  ├─ regions/               地区（含外城与城际）
│  ├─ factions/              阵营势力
│  ├─ characters/            人物角色
│  ├─ bestiary/              图鉴（赐名怪物 / 意识生物 / 人工智能）
│  ├─ chronicle/             编年史
│  ├─ prequel/               前传
│  ├─ story/                 剧情（主线 / 北岸篇 / 其他文本）
│  ├─ gallery/               图库
│  └─ project/               项目管理
├─ interactive/              可交互叙事分区
│  └─ tools/                 工具：介绍页 + 同名 HTML 并排
├─ buffer/                   缓冲分区 —— 通道，不是仓库
│  ├─ index.md               缓冲看板（脚本生成，勿手改）
│  ├─ rules.md               流程：提交 / 标记 / 公示 / 删除
│  ├─ editor.md              内容后台说明
│  ├─ style-guide.md         编辑规范
│  ├─ entries.md             条目模板
│  ├─ pending/               待审（只在本地预览构建，不发布）
│  └─ public/                公示中（站上可见，不进导航）
├─ editor/                   内容后台本体（纯静态单文件，零外部依赖）
├─ agents/                   机哥分区 —— 给 AI 助手的文档（见下）
├─ javascripts/              edit-entry.js：内容页的「编辑此条目」入口
├─ assets/                   gallery（图库原图）/ uploads（后台上传）
└─ stylesheets/              样式微调
```

## 给 AI 助手

仓库根目录的 **`AGENTS.md`** 是机器可读入口（支持该约定的工具会自动加载）。
完整版在站上 **`/agents/`** 或源码 `docs/agents/`：

| 页面 | 内容 |
|---|---|
| [上手](docs/agents/onboarding.md) | 环境、构建、验证、发布链路 |
| [仓库地图](docs/agents/repo-map.md) | 每个目录文件干什么，**哪些是生成的不许手改** |
| [任务手册](docs/agents/workflows.md) | 六种常见任务的步骤化做法 |
| [硬规则](docs/agents/constraints.md) | 必须做和绝对不能做的事 |
| [已知坑](docs/agents/pitfalls.md) | 踩过的坑 + 报错原文（可搜） |
| [skill 登记](docs/agents/skills.md) | skill 与 agent 资产的落点 |

**后续 skill、agent 协作、自动化相关的内容都更新到这一区。**

## 脚本

| 脚本 | 干什么 |
|---|---|
| `scripts/import_kb.py` | `.docx` / `.html` 批量转 Markdown（走 pandoc） |
| `scripts/import_doc.py` | 老格式 `.doc` 提取纯文本（pandoc 不支持 OLE2） |
| `scripts/fix_kb_links.py` | 修 Word 里残留的交叉引用死链 |
| `scripts/gen_section_index.py` | 生成 `docs/text/*/index.md` 落地页 |
| `scripts/gen_board.py` | 生成 `docs/buffer/index.md` 缓冲看板 |

## 内容怎么进正式分区

**状态 = 稿件在哪个目录**，移动文件就是改状态：

```text
放进 buffer/pending/  →  管理者标记通过  →  移进 buffer/public/ 公示（点赞点踩）
                      →  期满删除：内容并入 text/ 或 interactive/，或者直接丢弃
```

管理者也可以直接**要求更改** —— 删掉稿件，提交人改完重新提交。

**任何新内容都必须先落缓冲分区**，不能直接写进 `text/` 或 `interactive/`。
审核人名单靠 `.github/CODEOWNERS` + main 分支保护强制，见
[缓冲流程](docs/buffer/rules.md)。

公示期的点赞点踩走 GitHub Issue 的 👍/👎 reaction（静态站收不了票）。

## 写内容前先读

- [缓冲流程](docs/buffer/rules.md) —— 提交 / 标记 / 公示 / 删除
- [内容后台](docs/buffer/editor.md) —— 不写 Markdown 的人从这里进
- [编辑规范](docs/buffer/style-guide.md) —— 目录规则、命名规则、提示块用法
- [条目模板](docs/buffer/entries.md) —— 直接复制粘贴

一句话规则：**目录和文件名用 ASCII，中文只出现在标题里。**
（知识库导入时有意破例 —— 一百多篇文档保持原文件名才和你手上的包对得上。）

## 发布方式

**GitHub Actions 自动构建**（`.github/workflows/deploy.yml`）。
推 `main` 就触发：刷新生成页 → `mkdocs build` → 发布到 Pages。
成员从 `/editor/` 提交的内容走的就是这条链路，**不需要任何人在本地跑命令**。

仓库 `Settings → Pages → Source` 必须选 **GitHub Actions**（不是 `Deploy from a branch`）。

备选：本地 `mkdocs gh-deploy` 推 `gh-pages` 分支，但**两种方式不能同时用**，
切换时记得同步改 Pages 的 Source。

## 内容状态

| 分区 / 板块 | 状态 |
|---|---|
| 文本 · 全部 12 个板块 | **已导入知识库**（100+ 篇，从原始 .docx 批量转换） |
| —— 格式 | ⚠ Word 里的加粗标题不会变成 Markdown 标题，层级可能不齐 |
| 文本 · 4 个老格式 .doc | ⚠ 纯文本提取，表格与格式有损失 |
| 可交互 · 测名台 | 可用 |
| 可交互 · COC7 车卡 / 战图 | 已搬入 3 个单文件工具 |
| 图库 | 35 张原图已入库（含一张 22MB 的大地图） |
| 缓冲 · 提交 / 标记 / 公示 | 已启用（1 份待审、2 份公示示例） |
| 内容后台 | 可用（`/editor/`，需成员自备 GitHub 令牌） |
