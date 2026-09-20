# 14thSecretary

设定集 wiki。基于 **MkDocs + Material**，内容全是 Markdown，构建成一堆静态页面发布到 GitHub Pages。

## 本地跑起来

```bash
# 安装（只做一次）
pip install mkdocs-material

# 本地预览 —— 浏览器打开 http://127.0.0.1:8000，改文件即时刷新
mkdocs serve

# 构建到 site/ 检查产物
mkdocs build

# 发布上线（自动建 gh-pages 分支并开启 Pages）
mkdocs gh-deploy
```

## 首次发布前要改的三处

`mkdocs.yml` 里这几处现在是占位值，换成真实值再推：

```yaml
site_url:  https://YOURNAME.github.io/14thSecretary/
repo_url:  https://github.com/YOURNAME/14thSecretary
repo_name: YOURNAME/14thSecretary
```

另需在 GitHub 仓库页面 `Settings → Pages` 确认 Source 为
`Deploy from a branch` / `gh-pages` / `root`（`mkdocs gh-deploy` 首次执行时会自动设置）。

## 目录

```
mkdocs.yml              站点配置：导航、主题、Markdown 扩展
scripts/gen_board.py    审核看板生成脚本
.github/                CODEOWNERS（群审权限名单）+ PR 模板
docs/
├─ index.md             首页
├─ text/                文本分区 —— 纯阅读内容
│  ├─ canon/            设定：秘语体系、四段式真名、赐名流程
│  └─ bestiary/         图鉴（每只一页）
├─ interactive/         可交互叙事分区 —— 能玩的内容
│  └─ tools/            工具：介绍页 + 同名 HTML 并排
├─ buffer/              缓冲分区 —— 群审入口
│  ├─ index.md          审核看板（脚本生成，勿手改）
│  ├─ rules.md          群审规则
│  ├─ submit.md         提交指南
│  ├─ style-guide.md    编辑规范
│  ├─ entries.md        条目模板
│  └─ submissions/      待审稿件（只在本地预览构建，不发布）
├─ assets/              图片 / 图标
└─ stylesheets/         样式微调
```

## 内容怎么进正式分区

```text
写稿 → buffer/submissions/ → 群审（GitHub PR） → 维护者并入 → text/ 或 interactive/
```

**任何新内容都必须先落缓冲分区**，不能直接写进 `text/` 或 `interactive/`。
权限靠 `.github/CODEOWNERS` + main 分支保护强制，见
[群审规则](docs/buffer/rules.md)。

## 写内容前先读

- [编辑规范](docs/buffer/style-guide.md) —— 目录规则、命名规则、提示块用法
- [条目模板](docs/buffer/entries.md) —— 直接复制粘贴
- [群审规则](docs/buffer/rules.md) —— 谁能审、门槛怎么算、通过后怎么并入
- [提交指南](docs/buffer/submit.md) —— 提交人三步走

一句话规则：**目录和文件名用 ASCII，中文只出现在标题和 `nav` 里。**

## 发布方式

当前默认用 `mkdocs gh-deploy`（本地构建后推到 `gh-pages` 分支）。
如果以后想让 GitHub 替你构建，可以改成 GitHub Actions 工作流，
并把 Pages 的 Source 切成 `GitHub Actions` —— 两种方式不能同时用。

## 内容状态

| 分区 / 板块 | 状态 |
|---|---|
| 文本 · 秘语体系 / 四段式真名 / 赐名流程 | 已定稿 |
| 文本 · 图鉴 | 4 条演示条目，待替换 |
| 文本 · 世界 / 势力 / 人物 / 编年 | 待开 |
| 可交互 · 测名台 | 可用 |
| 缓冲 · 群审机制 | 已启用（3 份示例稿件） |
