---
title: 内容后台
tags:
  - 元
---

# 内容后台

不写 Markdown 的成员从这里进。表单式界面，图片拖拽上传，保存即提交。

**后台地址：`/admin/`** —— 部署后就是 `https://YOURNAME.github.io/14thSecretary/admin/`

!!! warning "一次性配置，三步"
    这套东西不能开箱即用 —— GitHub 的登录要一个中转服务，而那个服务需要你自己的账号。
    配完之后成员就只需要点一个链接。步骤在下面。

---

## 一、建 GitHub OAuth App

打开 <https://github.com/settings/developers> → **New OAuth App**：

| 字段 | 填什么 |
|---|---|
| Application name | `14thSecretary CMS` |
| Homepage URL | `https://YOURNAME.github.io/14thSecretary/` |
| Authorization callback URL | `https://<你的代理地址>/callback` |

创建后拿到 **Client ID**，再点 **Generate a new client secret** 拿到 **Client Secret**。
两个都留着，下一步用。**Client Secret 绝不能写进仓库。**

## 二、部署 OAuth 代理

用 Cloudflare Workers（免费额度足够）。新建一个 Worker，粘这段：

```js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const base = "https://" + url.host;

    if (url.pathname === "/auth") {
      const p = new URLSearchParams({
        client_id: env.GITHUB_CLIENT_ID,
        redirect_uri: base + "/callback",
        scope: "public_repo",
        state: crypto.randomUUID(),
      });
      return Response.redirect("https://github.com/login/oauth/authorize?" + p, 302);
    }

    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      if (!code) return new Response("missing code", { status: 400 });

      const res = await fetch("https://github.com/login/oauth/access_token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code: code,
        }),
      });
      const data = await res.json();
      const token = data.access_token || "";
      const payload = JSON.stringify({ token: token, provider: "github" });

      const html =
        '<!doctype html><html><body><script>' +
        '(function(){' +
        'function receiveMessage(e){' +
        'window.opener.postMessage("authorization:github:success:" + ' +
        JSON.stringify(payload) + ', e.origin);' +
        'window.removeEventListener("message", receiveMessage, false);' +
        '}' +
        'window.addEventListener("message", receiveMessage, false);' +
        'window.opener.postMessage("authorizing:github", "*");' +
        '})();' +
        '<\/script></body></html>';

      return new Response(html, {
        headers: { "Content-Type": "text/html;charset=utf-8" },
      });
    }

    return new Response("14thSecretary OAuth proxy — use /auth", { status: 200 });
  },
};
```

然后在 Worker 的 **Settings → Variables** 里加两个**加密变量**：

| 名称 | 值 |
|---|---|
| `GITHUB_CLIENT_ID` | 第一步拿到的 Client ID |
| `GITHUB_CLIENT_SECRET` | 第一步拿到的 Client Secret |

部署后你会得到一个地址，形如 `https://xxx.yyy.workers.dev`。
把第一步 OAuth App 的 callback URL 改成 `https://xxx.yyy.workers.dev/callback`。

!!! note "scope 说明"
    上面用的是 `public_repo`（只能读写公开仓库）。**GitHub Pages 免费账号本来就要求公开仓库**，
    所以够用。如果仓库以后转私有，把 `public_repo` 改成 `repo`。

!!! tip "不想用 Cloudflare"
    任何能跑一个 HTTP 函数的地方都行：Vercel、Deno Deploy、甚至自己的服务器。
    只要提供 `/auth` 和 `/callback` 两个端点。

## 三、填 `docs/admin/config.yml`

改这四处，把 `YOURNAME` / `YOUR-PROXY` 换成真实值：

```yaml
backend:
  repo: YOURNAME/14thSecretary
  base_url: https://YOUR-PROXY.workers.dev     # 上一步的 Worker 地址

site_url: https://YOURNAME.github.io/14thSecretary/
display_url: https://YOURNAME.github.io/14thSecretary/
logo_url: https://YOURNAME.github.io/14thSecretary/assets/sigil.svg

media_folder: docs/assets/uploads
public_folder: /14thSecretary/assets/uploads
```

推上去，打开 `/admin/`，用 GitHub 登录。**完了。**

!!! danger "成员必须先被加为协作者"
    `Settings → Collaborators` 里把每位成员加进来（Write 权限）。
    没有写权限的人能登录，但保存会失败。

---

## 成员怎么用

打开 `/admin/` → GitHub 登录 → 左侧 **缓冲稿** → **New 缓冲稿**。

要填的就六个格：

| 字段 | 说明 |
|---|---|
| 稿件编号 | 三位数，顺延。例 `012` |
| 英文短名 | 小写英文加短横线。例 `ember-pact`。只用于文件名和网址 |
| 标题 | 中文标题 |
| 提交人 | 你的代号 |
| 提交日期 | 选一个 |
| 拟并入的位置 | 例 `text/canon/xxx.md` |
| 正文 | 富文本编辑器，右侧有实时预览 |

图片直接拖进编辑器 —— 会提交进 `docs/assets/uploads/`，**不进外部图床**。

保存 = 提交一份缓冲稿到 `docs/buffer/pending/`，PR 都不用开。
之后就是管理者的活了，见 [缓冲流程](rules.md)。

---

## 几个必须知道的坑

**1. 站点不再是纯静态了。**
后台依赖 `unpkg.com` 加载 Decap CMS。**只有 `/admin/` 这一个页面受影响** ——
正文页面、测名台这些还是零外链。但如果 unpkg 被墙，后台就打不开（站点本身没事）。

**2. 跟分支保护冲突。**
现在是 `publish_mode: simple`，保存直接 commit 到 `main`。
如果你之后给 `main` 开了「必须走 PR」的分支保护，保存会报权限错误 ——
那时要把配置改成 `publish_mode: editorial_workflow`，让后台自己开 PR。
（见 `docs/admin/config.yml` 里的注释。）

**3. 后台只暴露了缓冲分区。**
没有把 `text/` 和 `interactive/` 挂进去 —— 直接编辑正式内容等于绕过缓冲，
正是 [编辑规范](style-guide.md) 里定的红线。正式内容的修订走 GitHub 网页编辑（管理者用）。

**4. 换域名要改 `public_folder`。**
图片链接是写死的 `/14thSecretary/assets/uploads/`。绑自定义域名时记得同步改，
否则所有图片会 404。

**5. `docs/admin/` 会被构建进站点。**
它是个静态 HTML，谁都能打开看到登录页 —— 但没登录什么也做不了，
真正的权限在 GitHub 那边。加 `noindex` 只是不让搜索引擎收录。
