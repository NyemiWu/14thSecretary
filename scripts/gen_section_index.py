#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 docs/text/* 生成各板块的落地页 index.md，以及文本分区的总目录。

    python scripts/gen_section_index.py
    python scripts/gen_section_index.py --check   # CI 校验

落地页是自动生成的，不要手改；改内容改文档本身，改简介改本脚本的 SECTIONS。
"""

import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# (目录名, 显示名, 一句话简介)
SECTIONS = [
    ("canon", "设定", "秘语体系、四段式真名、赐名流程 —— 整套赐名机制的规则部分。"),
    ("worldview", "世界观", "意识、意识海、仿生人、识子论、意识工学……这个世界运转的底层规则。"),
    ("society", "社会结构与体制", "十四号城的社会状况、意识形态全集、片区规划、戍卫军团。"),
    ("regions", "地区", "穹顶城内外、十三号城、西伯利亚穹顶城。"),
    ("factions", "阵营势力", "仿研所、穹顶政联、至高联合、商会、星枢学会……"),
    ("characters", "人物角色", "角色设定与设定卡。"),
    ("bestiary", "图鉴", "赐名怪物、意识生物、人工智能。"),
    ("chronicle", "编年史", "从市元前到 2058 年的时间线。"),
    ("prequel", "前传", "前传游戏的策划案、剧本、医疗与技术文档。"),
    ("story", "剧情", "主线、支线与个人篇章的剧本文本。"),
    ("gallery", "图库", "概念设定、角色设计、地图。"),
    ("project", "项目管理", "项目内部的目标与排期。"),
]

SUBDIR_LABEL = {
    "main": "主线 · 琳 & 芊",
    "northbank": "北岸篇",
    "misc": "其他文本",
    "13th": "十三号城",
    "districts": "片区规划",
    "inside": "穹顶城内",
    "outside": "穹顶城外",
    "ai": "人工智能",
    "conscious": "意识生物",
    "summoned": "赐名怪物",
    "media": None,          # None = 跳过
}

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".jfif", ".gif", ".webp", ".svg"}


def read_title_and_excerpt(path):
    """读 front matter 的 title 和正文首段做摘要。"""
    try:
        with io.open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return os.path.splitext(os.path.basename(path))[0], ""

    title = None
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            fm = text[3:end]
            m = re.search(r"^title:\s*(.+)$", fm, re.M)
            if m:
                title = m.group(1).strip().strip("'\"")
            body = text[end + 4:]

    if not title:
        m = re.search(r"^#\s+(.+)$", body, re.M)
        title = m.group(1).strip() if m else os.path.splitext(os.path.basename(path))[0]

    lines = []
    for ln in body.split("\n"):
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("!"):
            continue
        if s.startswith(("-", "*", "|", "```")):
            continue
        s = re.sub(r"[*`\[\]]", "", s)
        s = re.sub(r"\([^)]*\)", "", s)
        if len(s) < 8:
            continue
        lines.append(s)
        if len("".join(lines)) > 70:
            break
    excerpt = "".join(lines)
    excerpt = re.sub(r"\s+", " ", excerpt).strip()
    if len(excerpt) > 68:
        excerpt = excerpt[:68] + "…"
    return title, excerpt


def list_entries(folder):
    """返回 [(分组名 或 None, [(文件名, 标题, 摘要)])]，按组排序。"""
    groups = {}
    if not os.path.isdir(folder):
        return []
    for name in sorted(os.listdir(folder)):
        full = os.path.join(folder, name)
        if os.path.isdir(full):
            label = SUBDIR_LABEL.get(name, name)
            if label is None:
                continue
            items = []
            for sub in sorted(os.listdir(full)):
                if not sub.endswith(".md") or sub == "index.md":
                    continue
                t, e = read_title_and_excerpt(os.path.join(full, sub))
                items.append((name + "/" + sub, t, e))
            if items:
                groups[label] = items
        elif name.endswith(".md") and name != "index.md":
            t, e = read_title_and_excerpt(full)
            groups.setdefault(None, []).append((name, t, e))
    out = []
    if None in groups:
        out.append((None, groups.pop(None)))
    for k in sorted(groups):
        out.append((k, groups[k]))
    return out


def render_section(key, title, intro):
    folder = os.path.join(DOCS, "text", key)
    groups = list_entries(folder)
    total = sum(len(v) for _, v in groups)

    o = ["---", "title: " + title, "---", "", "# " + title, "", intro, ""]

    if key == "gallery":
        return render_gallery(title, intro, folder)

    o.append("共 **%d** 篇。" % total)
    o.append("")
    o.append('!!! info "本页自动生成"')
    o.append("    由 `scripts/gen_section_index.py` 扫描目录生成。新增文档后跑一次即可。")
    o.append("")

    if total == 0:
        o.append("本板块还没有内容。")
        o.append("")
        return "\n".join(o) + "\n"

    for label, items in groups:
        if label:
            o.append("## " + label)
        else:
            o.append("## 全部条目")
        o.append("")
        o.append("| 条目 | 摘要 |")
        o.append("|---|---|")
        for fn, t, e in items:
            o.append("| [%s](%s) | %s |" % (t.replace("|", "\\|"), fn, e.replace("|", "\\|") or "—"))
        o.append("")
    return "\n".join(o) + "\n"


def render_gallery(title, intro, folder):
    assets = os.path.join(DOCS, "assets", "gallery")
    files = []
    if os.path.isdir(assets):
        files = sorted(f for f in os.listdir(assets)
                       if os.path.splitext(f)[1].lower() in IMAGE_EXT)

    o = ["---", "title: " + title, "---", "", "# " + title, "", intro, ""]
    o.append("共 **%d** 张。" % len(files))
    o.append("")
    o.append('!!! info "本页自动生成"')
    o.append("    图片放在 `docs/assets/gallery/`，本页由 `scripts/gen_section_index.py` 扫描生成。")
    o.append("")
    o.append('<div class="gallery">')
    for f in files:
        name = os.path.splitext(f)[0]
        o.append('  <figure><img src="../../assets/gallery/%s" alt="%s" loading="lazy">'
                 '<figcaption>%s</figcaption></figure>' % (f, name, name))
    o.append("</div>")
    o.append("")
    return "\n".join(o) + "\n"


def render_text_index():
    o = ["---", "title: 文本分区", "---", "", "# 文本分区", ""]
    o.append("纯阅读内容。世界观、设定、剧情、图鉴 —— 一切「读」的部分。")
    o.append("")
    o.append('!!! warning "这里只放已放行的内容"')
    o.append("    任何新稿子先进 [缓冲分区](../buffer/index.md)，由管理者标记通过并走完公示才并入这里。")
    o.append("    直接往 `text/` 里写等于绕过缓冲。")
    o.append("")
    o.append("---")
    o.append("")
    o.append('<div class="grid cards" markdown>')
    o.append("")
    for key, title, intro in SECTIONS:
        folder = os.path.join(DOCS, "text", key)
        if key == "gallery":
            n = len([f for f in os.listdir(os.path.join(DOCS, "assets", "gallery"))
                     if os.path.splitext(f)[1].lower() in IMAGE_EXT]) \
                if os.path.isdir(os.path.join(DOCS, "assets", "gallery")) else 0
        else:
            n = sum(len(v) for _, v in list_entries(folder))
        o.append("-   __%s__（%d）" % (title, n))
        o.append("")
        o.append("    ---")
        o.append("")
        o.append("    " + intro)
        o.append("")
        o.append("    [:octicons-arrow-right-24: 进入](%s/index.md)" % key)
        o.append("")
    o.append("</div>")
    o.append("")
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    targets = {os.path.join(DOCS, "text", "index.md"): render_text_index()}
    for key, title, intro in SECTIONS:
        targets[os.path.join(DOCS, "text", key, "index.md")] = render_section(key, title, intro)

    stale = []
    for path, content in targets.items():
        old = ""
        if os.path.isfile(path):
            with io.open(path, "r", encoding="utf-8") as fh:
                old = fh.read()
        if old == content:
            continue
        if args.check:
            stale.append(os.path.relpath(path, ROOT))
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        print("已生成 %s" % os.path.relpath(path, ROOT))

    if args.check and stale:
        sys.stderr.write("以下落地页不是最新：\n  - " + "\n  - ".join(stale) + "\n")
        return 1
    if args.check:
        print("落地页都是最新")
    return 0


if __name__ == "__main__":
    sys.exit(main())
