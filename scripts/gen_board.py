#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描缓冲分区的待审稿件，生成审核看板 docs/buffer/index.md。

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
SUB_DIR = os.path.join(ROOT, "docs", "buffer", "submissions")
OUT_PATH = os.path.join(ROOT, "docs", "buffer", "index.md")

STATUS_LABEL = {
    "pending": ":material-progress-clock: 待审",
    "approved": ":material-check-decagram: 待并入",
    "changes": ":material-arrow-u-left-top: 已打回",
}

ORDER = {"changes": 0, "pending": 1, "approved": 2}

GITHUB_PLACEHOLDER = "YOURNAME"


def load_repo_url():
    """从 mkdocs.yml 读 repo_url，用来拼 GitHub 直链。"""
    cfg = os.path.join(ROOT, "mkdocs.yml")
    if not os.path.isfile(cfg):
        return ""
    with io.open(cfg, "r", encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh) or {}
        except yaml.YAMLError:
            return ""
    url = str(data.get("repo_url") or "").strip()
    if url.endswith(".git"):
        url = url[:-4]
    return url.rstrip("/")


def source_link(repo_url, filename):
    """待审稿件不发布到站点，所以一律指向 GitHub 原文。"""
    if not repo_url or GITHUB_PLACEHOLDER in repo_url:
        return None
    return "%s/blob/main/docs/buffer/submissions/%s" % (repo_url, filename)



def split_front_matter(text):
    if not text.lstrip().startswith("---"):
        return {}, text
    body = text.lstrip()
    end = body.find("\n---", 3)
    if end < 0:
        return {}, text
    raw = body[3:end]
    rest = body[end + 4:]
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        raise ValueError("front matter 不是合法 YAML: %s" % exc)
    return meta, rest


def as_date(value):
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return dt.datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def compute_status(meta, today):
    """返回 (status, detail)。"""
    reviews = meta.get("reviews") or []
    verdicts = [(r.get("verdict") or "pending").strip() for r in reviews]
    quorum = meta.get("quorum")
    quorum = int(quorum) if quorum else max(len(reviews), 1)
    mode = str(meta.get("mode") or "unanimous").strip().lower()

    if "reject" in verdicts:
        return "changes", "有反对票，打回重审"

    approved = verdicts.count("approve")

    if mode == "lazy":
        deadline = as_date(meta.get("deadline"))
        if deadline is None:
            return "pending", "lazy 模式缺 deadline，无法判定"
        if today < deadline:
            left = (deadline - today).days
            return "pending", "沉默期剩 %d 天（需 %d 绿灯，现有 %d）" % (left, quorum, approved)
        if approved >= quorum:
            return "approved", "沉默期届满，无异议，%d/%d 绿灯" % (approved, quorum)
        return "changes", "沉默期届满但绿灯不足（%d/%d）" % (approved, quorum)

    if reviews and approved == len(reviews):
        return "approved", "全员绿灯 %d/%d" % (approved, len(reviews))
    return "pending", "全票模式，%d/%d 绿灯" % (approved, len(reviews))


def collect(today):
    items = []
    if not os.path.isdir(SUB_DIR):
        return items
    for name in sorted(os.listdir(SUB_DIR)):
        if not name.endswith(".md") or name.startswith("_"):
            continue
        path = os.path.join(SUB_DIR, name)
        with io.open(path, "r", encoding="utf-8") as fh:
            meta, _ = split_front_matter(fh.read())
        status, detail = compute_status(meta, today)
        items.append({
            "file": name,
            "slug": name[:-3],
            "meta": meta,
            "status": status,
            "detail": detail,
        })
    items.sort(key=lambda it: (ORDER.get(it["status"], 9), it["file"]))
    return items


def render(items, today, repo_url):
    counts = {"pending": 0, "approved": 0, "changes": 0}
    for it in items:
        counts[it["status"]] = counts.get(it["status"], 0) + 1
    repo_ready = bool(repo_url) and GITHUB_PLACEHOLDER not in repo_url

    out = []
    out.append("---")
    out.append("title: 审核看板")
    out.append("tags:")
    out.append("  - 元")
    out.append("---")
    out.append("")
    out.append("# 审核看板")
    out.append("")
    out.append('!!! info "本页自动生成，不要手改"')
    out.append("    由 `scripts/gen_board.py` 扫描 `buffer/submissions/` 生成。")
    out.append("    提交或修订稿件后跑一次：`python scripts/gen_board.py`")
    out.append("")
    out.append("    判定规则见 [群审规则](rules.md)，字段写法见 [提交指南](submit.md)。")
    out.append("")
    out.append('!!! warning "待审稿件不会发布到站点"')
    out.append("    `mkdocs.yml` 里配了 `draft_docs: buffer/submissions/` ——")
    out.append("    这些稿子**只在 `mkdocs serve` 本地预览时构建，`mkdocs build` 不发布**。")
    out.append("    所以上线的看板里，稿件链接指向 GitHub 原文；本地预览时可以直接读渲染稿。")
    out.append("")
    out.append("**截至 %s** —— 待审 **%d** · 待并入 **%d** · 已打回 **%d**"
               % (today.isoformat(), counts["pending"], counts["approved"], counts["changes"]))
    out.append("")

    if not repo_ready:
        out.append('!!! danger "GitHub 链接尚未可用"')
        out.append("    `mkdocs.yml` 里的 `repo_url` 还是 `%s` 占位，"
                   "换成真实仓库地址后重跑本脚本，稿件直链才会生效。"
                   % GITHUB_PLACEHOLDER)
        out.append("")

    if not items:
        out.append("当前缓冲分区没有待审稿件。")
        out.append("")
        return "\n".join(out) + "\n"

    out.append("## 总览")
    out.append("")
    out.append("| 编号 | 标题 | 提交人 | 目标 | 模式 | 门槛 | 状态 |")
    out.append("|---|---|---|---|---|---|---|")
    for it in items:
        meta = it["meta"]
        no = it["slug"].split("-")[0]
        reviews = meta.get("reviews") or []
        approved = len([r for r in reviews if (r.get("verdict") or "") == "approve"])
        quorum = meta.get("quorum") or len(reviews) or 1
        mode = str(meta.get("mode") or "unanimous")
        mode_label = "全票" if mode.strip().lower() != "lazy" else "沉默期"
        scope = meta.get("scope") or "—"
        link = source_link(repo_url, it["file"])
        no_cell = "[%s](%s)" % (no, link) if link else no
        out.append("| %s | %s | %s | `%s`（%s） | %s | %s/%s | %s |"
                   % (no_cell, meta.get("title", "—"), meta.get("submitter", "—"),
                      meta.get("target", "—"), scope, mode_label, approved, quorum,
                      STATUS_LABEL.get(it["status"], it["status"])))
    out.append("")
    out.append("---")
    out.append("")
    out.append("## 明细")
    out.append("")

    for it in items:
        meta = it["meta"]
        no = it["slug"].split("-")[0]
        out.append("### %s · %s" % (no, meta.get("title", "—")))
        out.append("")
        out.append("**状态：%s** —— %s" % (STATUS_LABEL.get(it["status"], it["status"]), it["detail"]))
        out.append("")
        out.append("| 项 | 值 |")
        out.append("|---|---|")
        out.append("| 提交人 | %s |" % meta.get("submitter", "—"))
        out.append("| 提交日 | %s |" % (meta.get("submitted") or "—"))
        out.append("| 目标 | `%s` |" % meta.get("target", "—"))
        out.append("| 范围 | %s |" % (meta.get("scope") or "—"))
        if str(meta.get("mode") or "").strip().lower() == "lazy":
            out.append("| 沉默期截止 | %s |" % (meta.get("deadline") or "—"))
        link = source_link(repo_url, it["file"])
        if link:
            out.append("| 稿件原文 | [GitHub · %s](%s) |" % (it["file"], link))
        else:
            out.append("| 稿件原文 | `docs/buffer/submissions/%s` |" % it["file"])
        out.append("| 本地预览 | `mkdocs serve` 后访问 `/buffer/submissions/%s/` |" % it["slug"])
        out.append("")
        out.append("| 审核人 | 判定 | 日期 | 意见 |")
        out.append("|---|---|---|---|")
        for r in (meta.get("reviews") or []):
            v = (r.get("verdict") or "pending").strip()
            mark = {"approve": ":material-check: 绿灯",
                    "reject": ":material-close: 反对",
                    "abstain": ":material-minus: 弃权"}.get(v, ":material-dots-horizontal: 待审")
            note = (r.get("note") or "").replace("|", "\\|") or "—"
            out.append("| %s | %s | %s | %s |"
                       % (r.get("who", "—"), mark, r.get("date") or "—", note))
        out.append("")

    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查看板是否最新")
    args = ap.parse_args()

    today = dt.date.today()
    content = render(collect(today), today, load_repo_url())

    if args.check:
        old = ""
        if os.path.isfile(OUT_PATH):
            with io.open(OUT_PATH, "r", encoding="utf-8") as fh:
                old = fh.read()
        # 生成日期每天都在变，比对时抹掉
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
