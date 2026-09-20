---
title: 已知坑
tags:
  - 元
---

# 已知坑

按**症状 → 原因 → 做法**写。报错原文保留，方便直接搜。

---

## 一、相对路径有**两个基准目录**

**症状**

```text
WARNING - Doc file 'text/bestiary/001-ash.md' contains a link
'../assets/x.html', but the target 'assets/x.html' is not found
among documentation files. Did you mean '../../assets/x.html'?
```

**原因**：MkDocs 只重写 **markdown 链接**和 `<a href>`，**完全不碰 `<iframe src>`**。

| 写法 | 谁解析 | 基准 |
|---|---|---|
| `<iframe src>` / `<img src>` | **浏览器**（MkDocs 原样输出） | **页面 URL 目录** |
| `[文字](...)` markdown 链接 | **MkDocs** | **源文件所在目录** |

`use_directory_urls` 默认开启，所以 `docs/tools/a.md` 的页面 URL 是 `/tools/a/`
—— 源文件同级的东西在 URL 里是**上一层**。

**做法**：把工具 HTML 和介绍页**并排同名**放，两个基准都退化成浅路径：

```markdown
<!-- docs/interactive/tools/demo.md + docs/interactive/tools/demo.html -->
<iframe src="../demo.html"></iframe>                        <!-- 浏览器算 -->
[打开](demo.html){ .md-button target=_blank }               <!-- MkDocs 算 -->
```

**MkDocs 建议的那个路径就是 markdown 链接该写的正确值**，照着它改。

---

## 二、`draft_docs` 的语义不是"不构建"

**症状**：本地 `mkdocs serve` 能看到待审稿，但线上访问同路径 404。

**原因**：`draft_docs` = **只在 `mkdocs serve` 构建，`mkdocs build` 不发布**。
构建日志会提示 "being built only for the preview but will be excluded from
`mkdocs build`"。

**推论**：**draft 页面的链接在线上必然 404**。所以缓冲看板里的稿件链接指向
GitHub 原文（`{repo_url}/blob/main/docs/...`），不能指向站内路径。

`exclude_docs` 才是完全排除（连本地预览都没有）。

---

## 三、`yaml.safe_load` 读不了 `mkdocs.yml`

**症状**：脚本里明明配了某个值却读出来是空 / `—`，**没有任何报错**。

**原因**：`mkdocs.yml` 里有 `!!python/name:material.extensions.emoji.twemoji`，
`safe_load` 抛 `ConstructorError` —— 而它是 `YAMLError` 的子类，
**一旦被 `except` 吞掉就静默返回空配置**。

**做法**：注册一个吞掉 python 标签的 loader：

```python
class Loader(yaml.SafeLoader):
    pass

Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda l, s, n: None)
data = yaml.load(fh, Loader=Loader)
```

---

## 四、GitHub 会往仓库里塞一个 Jekyll 工作流

**症状**：站点时好时坏 —— 有时是 MkDocs 的样子，有时是一个只剩 README 的裸页。

**原因**：在 GitHub 的 Pages 设置页选了 "GitHub Actions" 之后，
它会**推销一个 Jekyll 起始工作流**。用户点了 "Commit changes"，
于是仓库里多出 `.github/workflows/jekyll-gh-pages.yml`。
它 `push` 触发、`source: ./` 用 Jekyll 构建仓库根目录，
**并且和 `deploy.yml` 共用 `concurrency: group: pages`** ——
同一次 push 两个都跑，**谁后跑完谁覆盖站点**。

**做法**：删掉多余的那个。**页面上删不掉，要删文件。**
然后确认：

```bash
curl -s -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/NyemiWu/14thSecretary/actions/workflows
# total_count 必须是 1
```

---

## 五、`mkdocs build` 有 WARNING 也返回 0

**症状**：CI 绿了，但线上有坏链。

**做法**：**永远逐行看构建输出**，不要只看退出码。
本仓库目前保持零 WARNING，别让它退化。

---

## 六、`mkdocs build` 往 stderr 写横幅

**症状**：PowerShell 里报 `NativeCommandError`，退出码 1。

**原因**：Material 会往 stderr 打一段 "MkDocs 2.0 兼容性警告"横幅。
**这是误报**，构建其实是成功的（日志里有 `Documentation built in N seconds`）。

---

## 七、`configure-pages` 的 `enablement` 会让整个 job 挂掉

**症状**

```text
##[error]Create Pages site failed. Error: Resource not accessible by integration
```

**原因**：创建 Pages 站点需要仓库 **admin** 权限，
工作流的 `GITHUB_TOKEN` 即使显式给了 `pages: write` 也拿不到。

**做法**：**别加那个输入**。实测 deploy job 里声明
`environment: name: github-pages` 就足以让 Pages 自动启起来（`build_type=workflow`）。

---

## 八、Word 里的"标题"不是 Markdown 标题

**症状**：导入后很多页面只有 H1，没有层级。

**原因**：源文档大多用**加粗**而不是 Heading 样式，pandoc 转出来是 `**某某**`。
`import_kb.py` 里有兜底（整篇没 `^# ` 时把第一行提升为 H1），但中段的小标题没救。

**做法**：这类页面要人工过一遍。**不要试图用正则批量猜标题** —— 会误伤正文加粗。

---

## 九、`pandoc --extract-media` 写的是绝对路径

**症状**：转换后 Markdown 里出现 `C:\Users\...\media\xxx\image1.png`。

**做法**：转完必须把绝对路径替换回相对路径。`import_kb.py` 里已经处理了。
另外图片要抽到**每篇文档各自的** `media/<文档slug>/`，共用一个目录会撞名
（多篇文档都叫 `image1.png`）。

---

## 十、中文内容经 PowerShell 传 JSON 会乱码

**症状**：仓库描述、commit message 之类的中文变成 `?????????` 或 `濉叆鐪熷疄`。

**原因**：PowerShell 5.1 的 `-Body <string>` 默认不是 UTF-8。

**做法**：把 JSON 写进文件，再 `-Body ([IO.File]::ReadAllBytes($path))`。
（**只是显示乱码**的情况不用管：`git log` / Python 输出经 PowerShell 回读经常会花，
但文件里的字节是对的 —— 用 GitHub 网页或连接器确认真实值。）

---

## 十一、自测脚本比实现更容易错

这条是给自己的提醒。曾经连续两次由**验证脚本自己**得出"链接算错了"的假结论：

1. `new URL(href, base)` 的 base 用了站点根，**应该用页面自身的完整 URL**；
2. `site/` 目录的内容部署在 `/<repo>/` 下，算 base 时**漏了这段前缀**。

**经验**：验证脚本报错时，**先怀疑脚本自己**。
尤其是"看起来全都错"这种结论 —— 实现不太可能整体性错，脚本的口径更可能错。
