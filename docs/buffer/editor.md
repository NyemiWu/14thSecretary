---
title: 内容后台
tags:
  - 元
---

# 内容后台

不写 Markdown 的成员从这里进。表单式界面，图片拖拽上传，点一下提交。

**地址：`/editor/`** —— 部署后就是 `https://nyemiwu.github.io/14thSecretary/editor/`

!!! tip "零安装、零第三方"
    编辑器是一个纯静态 HTML，**不加载任何外部脚本**。
    所有请求直接打到 GitHub 的 API，不需要中转服务、不需要注册 OAuth 应用。
    代价是每位成员要一次性生成一个访问令牌。

---

## 成员第一次用：三步（只做一次）

**1. 拿到内容后台的链接**

`https://nyemiwu.github.io/14thSecretary/editor/` —— 直接打开，不用登录。

**2. 生成一个访问令牌**

打开 <https://github.com/settings/personal-access-tokens/new>（Fine-grained token）：

| 项 | 填什么 |
|---|---|
| Token name | `14thSecretary 投稿` |
| Expiration | 自选，建议 90 天 |
| Repository access | **Only select repositories** → 勾 `14thSecretary` |
| Permissions → Repository permissions | 把 **Contents** 设成 **Read and write** |

生成后复制那串 `github_pat_…`。

**3. 粘贴并保存**

在后台点右上角 **设置**，把令牌粘进去 → 保存。
会显示「已连接 · 你的用户名」表示成功。

!!! note "令牌存在哪"
    只存在**你这台浏览器的 localStorage** 里，不会上传到任何服务器。
    换电脑、清缓存、换浏览器都要重填。**不需要的时候点「断开」就能清掉。**

!!! danger "别用 Classic token 的全权限版本"
    设置里按上面选 **Fine-grained** + 只勾这一个仓库的 Contents 即可。
    不要去生成带 `repo` 全权限的 Classic token —— 那能读写你所有仓库。

---

## 怎么写一份稿

打开后台，填这些格：

| 字段 | 说明 |
|---|---|
| 稿件编号 | 三位数，顺延不重复。例 `012` |
| 英文短名 | 小写英文加短横线。例 `ember-pact`。**只用于文件名和网址**，页面不显示 |
| 标题 | 中文标题 |
| 提交人 | 你的代号 |
| 提交日期 | 默认今天 |
| 拟并入的位置 | 例 `text/canon/xxx.md`。不确定就留空 |
| 正文 | 右边实时预览，支持 Markdown |

**图片直接拖到虚线框里** —— 会自动传进仓库的 `docs/assets/uploads/`，
并把链接插到光标处。**不走外部图床。**

点「提交缓冲稿」→ 文件进 `docs/buffer/pending/`，完事。
不用开 PR，不用碰 git，剩下的等管理员标记。

## 改自己的稿

左下角「缓冲稿列表」列出 `pending/` 下所有待审稿件，点「打开」载入，
改完再点提交就是覆盖。**已经被管理员标记通过的稿子不在这个列表里** ——
那说明已经进公示了，要改得走 [缓冲流程](rules.md) 里的正常途径。

---

## 为什么不是 Decap

原本接的是 Decap CMS，实测有两个过不去的坎：

| 问题 | 说明 |
|---|---|
| **打不开** | 它的脚本从 `unpkg.com` 加载。国内网络拉不到就白屏，页面什么也没有 |
| **要一个 OAuth 代理** | GitHub 登录需要 client_secret，不能放静态站，得另开一个 Cloudflare Worker 转发 |

现在这个编辑器把这两层都去掉了：脚本内联在页面里，鉴权用成员自己的令牌直连 GitHub API。
**唯一的取舍**是每人要一次性生成令牌 —— 比配 OAuth 代理省事得多。

## 常见问题

**提示「令牌无效或已过期」**
Fine-grained token 默认有有效期。去 GitHub 重新生成一个，设置里换掉。

**提示「文件已存在，或者令牌没有写权限」**
两种可能：编号跟已有稿件撞了（换个编号），或者令牌没给 Contents 的写权限（回设置里重发）。

**上传图片报错**
传图也需要 Contents 写权限。另外单张图别超过 25MB（GitHub API 的限制）。

**能不能不用令牌**
不行。GitHub 的所有写操作都要鉴权，而鉴权需要一个凭据。
不想给令牌的话，走 [编辑规范](style-guide.md) 里那条路：让管理员代提交。
