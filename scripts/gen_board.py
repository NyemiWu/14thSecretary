#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描缓冲分区，生成看板 docs/buffer/index.md。

缓冲区分两级，状态由稿件在哪个目录决定：
    buffer/pending/   待审（管理者还没标记）
    buffer/public/    公示中（管理者已标记通过）
公示期满 / 要求更改 → 直接从缓冲区删除。

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
PENDING_DIR = os.path.join(ROOT, "docs", "buffer", "pending")
PUBLIC_DIR = os.path.join(ROOT, "docs", "buffer", "public")
OUT_PATH = os.path.join(ROOT, "docs", "buffer", "index.md")

GITHUB_PLACEHOLDER = "YOURNAME"


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


def scan(folder):
    items = []
    if not os.path.isdir(folder):
        return items
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md") or name.startswith("_"):
            continue
        with io.open(os.path.join(folder, name), "r", encoding="utf-8") as fh:
            meta, _ = split_front_matter(fh.read())
        items.append({"file": name, "slug": name[:-3], "meta": meta})
    return items


def load_repo_url():
    """从 mkdocs.yml 读 repo_url。
    注意：mkdocs.yml 里有 `!!python/name:...` 标签，safe_load 会抛错，
    所以注册一个吞掉 python 标签的 loader。"""
    cfg = os.path.join(ROOT, "mkdocs.yml")
    if not os.path.isfile(cfg):
        return ""

    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda l, s, n: None)
    with io.open(cfg, "r", encoding="utf-8") as fh:
        try:
            data = yaml.load(fh, Loader=Loader) or {}
        except yaml.YAMLError:
            data = {}
    url = str(data.get("repo_url") or "").strip()
    if url.endswith(".git"):
        url = url[:-4]
    return url.rstrip("/")


def esc(text):
    return str(text).replace("|", "\\|")


def render(today, repo_url):
    pub = scan(PUBLIC_DIR)
    pend = scan(PENDING_DIR)
    pub.sort(key=lambda i: str(i["meta"].get("public_until") or "9999"))
    repo_ready = bool(repo_url) and GITHUB_PLACEHOLDER not in repo_url

    def gh_link(fname):
        if not repo_ready:
            return None
        return "%s/blob/main/docs/buffer/pending/%s" % (repo_url, fname)

    o = []
    o.append("---")
    o.append("title: 缓冲看板")
    o.append("tags:")
    o.append("  - 元")
    o.append("---")
    o.append("")
    o.append("# 缓冲看板")
    o.append("")
    o.append('!!! info "本页自动生成，不要手改"')
    o.append("    由 `scripts/gen_board.py` 扫描 `buffer/pending/` 与 `buffer/public/` 生成。")
    o.append("    稿件一动就跑一次：`python scripts/gen_board.py`")
    o.append("")
    o.append("    流程见 [缓冲流程](rules.md)。")
    o.append("")
    o.append("**截至 %s** —— 公示中 **%d** · 待审 **%d**"
             % (today.isoformat(), len(pub), len(pend)))
    o.append("")

    # ---------- 公示中 ----------
    o.append("## 公示中")
    o.append("")
    o.append("管理员已标记通过，正在公示期。期满后**从缓冲区删除**：")
    o.append("内容并入正式分区，或者直接丢弃。")
    o.append("")
    if not pub:
        o.append("当前没有正在公示的稿件。")
        o.append("")
    else:
        o.append("| 编号 | 标题 | 提交人 | 审核人 | 公示截止 | 点赞 | 点踩 | 状态 |")
        o.append("|---|---|---|---|---|---|---|---|")
        for it in pub:
            meta = it["meta"]
            no = it["slug"].split("-")[0]
            link = "public/%s.md" % it["slug"]
            until = as_date(meta.get("public_until"))
            if until is None:
                when, flag = "未设", "公示中"
            elif today > until:
                when, flag = "%s（已期满）" % until.isoformat(), ":material-alert: **期满 · 该处理了**"
            else:
                when, flag = "%s（剩 %d 天）" % (until.isoformat(), (until - today).days), "公示中"
            o.append("| [%s](%s) | %s | %s | %s | %s | %s | %s | %s |"
                     % (no, link, esc(meta.get("title", "—")), meta.get("submitter", "—"),
                        meta.get("reviewed_by", "—"), when,
                        meta.get("votes_up", "—"), meta.get("votes_down", "—"), flag))
        o.append("")
        o.append('!!! note "票数怎么来"')
        o.append("    站点是静态的，收不了票。点赞点踩在对应公示 Issue 的 👍 / 👎 reaction 上，")
        o.append("    由管理员回填到稿件的 `votes_up` / `votes_down`。")
        o.append("")

    # ---------- 待审 ----------
    o.append("---")
    o.append("")
    o.append("## 待审")
    o.append("")
    o.append("等管理员标记。**通过** → 移进 `public/` 并补 `public_until`；")
    o.append("**要求更改** → 直接删除，提交人重新提交。")
    o.append("")
    if not pend:
        o.append("当前没有待审稿件。")
        o.append("")
    else:
        o.append("| 编号 | 标题 | 提交人 | 提交日 | 目标 | 稿件 |")
        o.append("|---|---|---|---|---|---|")
        for it in pend:
            meta = it["meta"]
            no = it["slug"].split("-")[0]
            link = gh_link(it["file"])
            cell = "[GitHub 原文](%s)" % link if link else "`docs/buffer/pending/%s`" % it["file"]
            o.append("| %s | %s | %s | %s | `%s` | %s |"
                     % (no, esc(meta.get("title", "—")), meta.get("submitter", "—"),
                        meta.get("submitted") or "—", meta.get("target", "—"), cell))
        o.append("")
        o.append('!!! warning "待审稿件不发布到站点"')
        o.append("    `mkdocs.yml` 配了 `draft_docs: buffer/pending/` ——")
        o.append("    这些稿子只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布。")
        o.append("    管理员标记通过、移进 `public/` 之后，站上才可见。")
        o.append("")

    if not repo_ready:
        o.append("---")
        o.append("")
        o.append('!!! danger "GitHub 链接尚未可用"')
        o.append("    `mkdocs.yml` 的 `repo_url` 还是 `%s` 占位，换成真实仓库地址后重跑本脚本。"
                 % GITHUB_PLACEHOLDER)
        o.append("")

    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查看板是否最新")
    args = ap.parse_args()

    today = dt.date.today()
    content = render(today, load_repo_url())

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
