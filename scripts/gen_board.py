#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描缓冲分区，生成审核看板 docs/buffer/index.md。

流程只有四步：提交 → @邮箱请求审核 → 审核通过进公示（可点赞点踩）→ 管理员裁决。

    python scripts/gen_board.py            # 生成
    python scripts/gen_board.py --check    # 只校验是否最新（CI 用），不一致退出码 1
"""

import argparse
import datetime as dt
import io
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("需要 PyYAML：pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMIT_DIR = os.path.join(ROOT, "docs", "buffer", "submissions")
PUBLIC_DIR = os.path.join(ROOT, "docs", "buffer", "public")
OUT_PATH = os.path.join(ROOT, "docs", "buffer", "index.md")

GITHUB_PLACEHOLDER = "YOURNAME"

# 状态 -> 看板归到哪一组
GROUP = {
    "submitted": "review",
    "reviewing": "review",
    "public": "public",
    "merged": "done",
    "removed": "done",
}

STATUS_LABEL = {
    "submitted": "已提交",
    "reviewing": "审核中",
    "public": "公示中",
    "merged": "已并入",
    "removed": "已去除",
}


def _mkdocs_loader():
    """mkdocs.yml 里带 `!!python/name:...` 标签，safe_load 会直接报错，
    所以注册一个吞掉所有 python 标签的 loader。"""
    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor(
        "tag:yaml.org,2002:python/",
        lambda loader, suffix, node: None,
    )
    return Loader


def load_config():
    cfg = os.path.join(ROOT, "mkdocs.yml")
    if not os.path.isfile(cfg):
        return {}
    with io.open(cfg, "r", encoding="utf-8") as fh:
        try:
            return yaml.load(fh, Loader=_mkdocs_loader()) or {}
        except yaml.YAMLError:
            return {}


def split_front_matter(text):
    if not text.lstrip().startswith("---"):
        return {}, text
    body = text.lstrip()
    end = body.find("\n---", 3)
    if end < 0:
        return {}, text
    try:
        return yaml.safe_load(body[3:end]) or {}, body[end + 4:]
    except yaml.YAMLError as exc:
        raise ValueError("front matter 不是合法 YAML: %s" % exc)


def as_date(value):
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return dt.datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def collect():
    items = []
    for folder, published in ((SUBMIT_DIR, False), (PUBLIC_DIR, True)):
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if not name.endswith(".md") or name.startswith("_"):
                continue
            path = os.path.join(folder, name)
            with io.open(path, "r", encoding="utf-8") as fh:
                meta, _ = split_front_matter(fh.read())
            status = str(meta.get("status") or "submitted").strip().lower()
            if status not in GROUP:
                status = "submitted"
            items.append({
                "file": name,
                "slug": name[:-3],
                "folder": "public" if published else "submissions",
                "published": published,
                "meta": meta,
                "status": status,
                "group": GROUP[status],
            })
    return items


def link_for(it, repo_url):
    """公示稿已发布，用站内相对链接；待审稿未发布，指向 GitHub 原文。"""
    if it["published"]:
        return "%s/%s.md" % (it["folder"], it["slug"]), True
    if repo_url and GITHUB_PLACEHOLDER not in repo_url:
        return "%s/blob/main/docs/buffer/submissions/%s" % (repo_url, it["file"]), False
    return None, False


def render(items, today, cfg):
    repo_url = str(cfg.get("repo_url") or "").strip()
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]
    repo_url = repo_url.rstrip("/")
    review_email = str((cfg.get("extra") or {}).get("review_email") or "—")

    pub = [i for i in items if i["group"] == "public"]
    rev = [i for i in items if i["group"] == "review"]
    done = [i for i in items if i["group"] == "done"]
    pub.sort(key=lambda i: str(i["meta"].get("public_until") or "9999"))

    o = []
    o.append("---")
    o.append("title: 审核看板")
    o.append("tags:")
    o.append("  - 元")
    o.append("---")
    o.append("")
    o.append("# 审核看板")
    o.append("")
    o.append('!!! info "本页自动生成，不要手改"')
    o.append("    由 `scripts/gen_board.py` 扫描 `buffer/submissions/` 与 `buffer/public/` 生成。")
    o.append("    稿件状态变了就跑一次：`python scripts/gen_board.py`")
    o.append("")
    o.append("    流程说明见 [流程](rules.md)。")
    o.append("")
    o.append("**截至 %s** —— 公示中 **%d** · 待审核 **%d**"
             % (today.isoformat(), len(pub), len(rev)))
    o.append("")

    # ---------- 公示中 ----------
    o.append("## 公示中")
    o.append("")
    o.append('!!! tip "公示期怎么表态"')
    o.append("    在对应稿件的公示 Issue 上用 **👍 / 👎** reaction 表态即可，不用打字。")
    o.append("    公示期满后由管理员裁决：**保留 → 并入正式分区**，**去除 → 稿件下架**。")
    o.append("")
    if not pub:
        o.append("当前没有正在公示的稿件。")
        o.append("")
    else:
        o.append("| 编号 | 标题 | 提交人 | 审核人 | 公示截止 | 点赞 | 点踩 | 状态 |")
        o.append("|---|---|---|---|---|---|---|---|")
        for it in pub:
            meta = it["meta"]
            href, _ = link_for(it, repo_url)
            no = it["slug"].split("-")[0]
            no_cell = "[%s](%s)" % (no, href) if href else no
            until = as_date(meta.get("public_until"))
            if until is None:
                when = "未设"
                flag = STATUS_LABEL["public"]
            elif today > until:
                when = "%s（已期满）" % until.isoformat()
                flag = ":material-alert: 待裁决"
            else:
                when = "%s（剩 %d 天）" % (until.isoformat(), (until - today).days)
                flag = STATUS_LABEL["public"]
            o.append("| %s | %s | %s | %s | %s | %s | %s | %s |"
                     % (no_cell, meta.get("title", "—"), meta.get("submitter", "—"),
                        meta.get("reviewed_by", "—"), when,
                        meta.get("votes_up", "—"), meta.get("votes_down", "—"), flag))
        o.append("")
        o.append('!!! note "票数怎么来的"')
        o.append("    站点是静态的，收不了票。点赞点踩在 GitHub Issue 的 reaction 上，")
        o.append("    由管理员回填到稿件的 `votes_up` / `votes_down` 字段。")
        o.append("")

    # ---------- 待审核 ----------
    o.append("---")
    o.append("")
    o.append("## 待审核")
    o.append("")
    o.append("审核请求发至 **`%s`** —— 提交人提交后需自行发信，见 [流程](rules.md)。" % review_email)
    o.append("")
    if not rev:
        o.append("当前没有待审稿件。")
        o.append("")
    else:
        o.append("| 编号 | 标题 | 提交人 | 提交日 | 状态 | 稿件 |")
        o.append("|---|---|---|---|---|---|")
        for it in rev:
            meta = it["meta"]
            href, _ = link_for(it, repo_url)
            no = it["slug"].split("-")[0]
            if href:
                cell = "[GitHub 原文](%s)" % href
            else:
                cell = "`docs/buffer/submissions/%s`" % it["file"]
            o.append("| %s | %s | %s | %s | %s | %s |"
                     % (no, meta.get("title", "—"), meta.get("submitter", "—"),
                        meta.get("submitted") or "—",
                        STATUS_LABEL.get(it["status"], it["status"]), cell))
        o.append("")
        o.append('!!! warning "待审稿件不发布到站点"')
        o.append("    `mkdocs.yml` 配了 `draft_docs: buffer/submissions/` ——")
        o.append("    这些稿子只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布。")
        o.append("    审核通过后才移进 `buffer/public/` 进入公示，那时站上才可见。")
        o.append("")

    # ---------- 已裁决 ----------
    if done:
        o.append("---")
        o.append("")
        o.append("## 已裁决")
        o.append("")
        o.append("| 编号 | 标题 | 结果 | 裁决说明 |")
        o.append("|---|---|---|---|")
        for it in done:
            meta = it["meta"]
            o.append("| %s | %s | %s | %s |"
                     % (it["slug"].split("-")[0], meta.get("title", "—"),
                        STATUS_LABEL.get(it["status"], it["status"]),
                        (meta.get("note") or "—").replace("|", "\\|")))
        o.append("")

    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查看板是否最新")
    args = ap.parse_args()

    cfg = load_config()
    today = dt.date.today()
    content = render(collect(), today, cfg)

    if args.check:
        old = ""
        if os.path.isfile(OUT_PATH):
            with io.open(OUT_PATH, "r", encoding="utf-8") as fh:
                old = fh.read()
        norm = lambda s: re.sub(r"截至 \d{4}-\d{2}-\d{2}", "截至 <DATE>", s)
        if norm(old) != norm(content):
            sys.stderr.write("看板不是最新，跑一下 python scripts/gen_board.py\n")
            return 1
        print("看板已是最新")
        return 0

    with io.open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print("已生成 %s" % os.path.relpath(OUT_PATH, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
