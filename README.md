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
docs/
├─ index.md             首页
├─ canon/               设定：秘语体系、四段式真名、赐名流程
├─ bestiary/            怪物图鉴（每只一页）
├─ tools/               工具介绍页
├─ meta/                编辑规范与条目模板
├─ assets/              图片、附件、单文件 HTML
└─ stylesheets/         样式微调
```

## 写内容前先读

- [编辑规范](docs/meta/style-guide.md) —— 目录规则、命名规则、提示块用法
- [条目模板](docs/meta/templates.md) —— 直接复制粘贴

一句话规则：**目录和文件名用 ASCII，中文只出现在标题和 `nav` 里。**

## 发布方式

当前默认用 `mkdocs gh-deploy`（本地构建后推到 `gh-pages` 分支）。
如果以后想让 GitHub 替你构建，可以改成 GitHub Actions 工作流，
并把 Pages 的 Source 切成 `GitHub Actions` —— 两种方式不能同时用。

## 内容状态

| 板块 | 状态 |
|---|---|
| 秘语体系 / 四段式真名 / 赐名流程 | 已定稿 |
| 怪物图鉴 | 4 条演示条目，待替换 |
| 世界设定 | 目录已留位，待补 |
| 测名台 | 可用 |
