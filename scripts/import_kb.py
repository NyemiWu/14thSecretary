#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「十四号城项目」知识库包转换成 MkDocs 站点内容。

    python scripts/import_kb.py            # 正式导入
    python scripts/import_kb.py --dry-run  # 只打印计划，不写文件

源：C:/Users/ROG/Documents/项目文档/14th/十四号城项目20260921打包
"""

import argparse
import io
import os
import re
import shutil
import sys

import pypandoc

SRC = r"C:\Users\ROG\Documents\项目文档\14th\十四号城项目20260921打包"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
REPORT = os.path.join(ROOT, "scripts", "import_kb_report.txt")

# 源一级目录 -> docs 下的目标目录
MAP = {
    "世界观": "text/worldview",
    "人物角色相关": "text/characters",
    "前传": "text/prequel",
    "剧情": "text/story",
    "图库": None,                    # 图片走 assets/gallery，单独处理
    "地区": "text/regions",
    "外城与城际": "text/regions/outer",
    "工具": None,                    # HTML 走 interactive/tools，单独处理
    "生物设定": "text/bestiary",
    "社会结构与体制": "text/society",
    "编年史": "text/chronicle",
    "阵营势力": "text/factions",
    "项目管理": "text/project",
    "食品": "text/society",
}

# 源二级目录 -> 目标子目录名
SUBMAP = {
    "剧情/北岸篇": "northbank",
    "剧情/其他文本": "misc",
    "剧情/主线-琳&芊": "main",
    "外城与城际/十三号城": "13th",
    "社会结构与体制/片区规划": "districts",
    "社会结构与体制/片区规划/穹顶城内": "districts/inside",
    "社会结构与体制/片区规划/穹顶城外": "districts/outside",
    "生物设定/人工智能": "ai",
    "生物设定/意识生物": "conscious",
}

SKIP_EXT = {".crswap", ".wpsonline", ".tmp", ".lock"}

report = []


def note(msg):
    report.append(msg)


def slugify(name):
    n = name.strip()
    n = n.replace("&", "-").replace("：", "-").replace(":", "-")
    n = n.replace(" ", "-").replace("、", "-").replace("　", "-")
    n = re.sub(r'[\\/*?"<>|]', "-", n)
    n = re.sub(r"-{2,}", "-", n)
    return n.strip("-.")


def target_dir_for(rel_dir):
    """rel_dir 是相对源根的分目录路径（用 / 分隔，可能是 ''）。"""
    if not rel_dir:
        return None
    parts = rel_dir.split("/")
    top = parts[0]
    base = MAP.get(top)
    if base is None:
        return None
    sub = SUBMAP.get(rel_dir)
    if sub:
        return os.path.join("docs", base, sub)
    # 未登记的二级目录：直接拼在 base 下
    rest = parts[1:]
    return os.path.join("docs", base, *[slugify(r) for r in rest])


def ensure_h1(md, fallback):
    for ln in md.split("\n"):
        if ln.startswith("# "):
            return md
    lines = md.split("\n")
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            continue
        plain = re.sub(r"^\*\*(.+?)\*\*$", r"\1", s).strip()
        plain = plain.replace("\\", "").strip()
        if plain and len(plain) <= 40 and not plain.startswith("#"):
            lines[i] = "# " + plain
            return "\n".join(lines)
        break
    return "# " + fallback + "\n\n" + md


def tidy(md):
    out = []
    for ln in md.split("\n"):
        s = ln.strip()
        # pandoc 会把单独一行转义星号渲染成 **\** 这种残渣，去掉
        if s in ("**\\**", "\\", "**\\**\\", "*\\*"):
            continue
        out.append(ln.rstrip())
    md = "\n".join(out)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def convert_any(path, out_dir, out_name, dry, fmt):
    """docx / html 都走 pandoc，只是输入格式不同。"""
    slug = os.path.splitext(out_name)[0]
    media_rel = "media/" + slug
    media_abs = os.path.join(ROOT, out_dir, "media", slug)
    if dry:
        return "ok", os.path.join(out_dir, out_name)
    try:
        md = pypandoc.convert_file(
            path, "gfm", format=fmt,
            extra_args=["--wrap=none", "--extract-media=" + media_abs],
        )
    except Exception as exc:
        return "fail", str(exc)
    md = md.replace(media_abs.replace("\\", "/"), media_rel)
    md = md.replace(media_abs, media_rel)
    title = os.path.splitext(out_name)[0]
    md = tidy(ensure_h1(md, title))
    front = "---\ntitle: %s\n---\n\n" % title
    dest = os.path.join(ROOT, out_dir, out_name)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with io.open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(front + md)
    return "ok", os.path.join(out_dir, out_name)


def convert_docx(path, out_dir, out_name, dry):
    return convert_any(path, out_dir, out_name, dry, "docx")


def copy_plain(path, out_dir, out_name, dry):
    if dry:
        return "ok", os.path.join(out_dir, out_name)
    dest = os.path.join(ROOT, out_dir, out_name)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(path, dest)
    return "ok", os.path.join(out_dir, out_name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    used = {}
    counts = {"docx": 0, "doc": 0, "md": 0, "html": 0, "asset": 0, "skip": 0}

    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        rel_dir = os.path.relpath(root, SRC).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""
        for f in sorted(files):
            src_path = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()

            if ext in SKIP_EXT:
                counts["skip"] += 1
                continue

            tdir = target_dir_for(rel_dir)
            if tdir is None:
                # 图库 / 工具 单独处理
                note("SKIP(另行处理) %s" % os.path.join(rel_dir, f))
                continue

            stem = slugify(os.path.splitext(f)[0])
            key = (tdir, stem)
            if key in used:
                used[key] += 1
                stem = "%s-%d" % (stem, used[key])
            else:
                used[key] = 1

            if ext == ".docx":
                status, info = convert_docx(src_path, tdir, stem + ".md", args.dry_run)
                counts["docx"] += 1
            elif ext == ".html":
                status, info = convert_any(src_path, tdir, stem + ".md", args.dry_run, "html")
                counts["html"] += 1
            elif ext == ".doc":
                note("TODO(.doc 老格式，需单独提取) %s" % os.path.join(rel_dir, f))
                counts["doc"] += 1
                continue
            elif ext == ".md":
                status, info = copy_plain(src_path, tdir, stem + ".md", args.dry_run)
                counts["md"] += 1
            else:
                # 文档旁边夹带的图片 / 视频之类的附件，原样搬过去
                counts["asset"] += 1
                status, info = copy_plain(src_path, tdir, stem + ext, args.dry_run)
                note("%-6s %-46s -> %s" % (status.upper(), os.path.join(rel_dir, f), info))
                continue

            note("%-6s %-46s -> %s" % (status.upper(), os.path.join(rel_dir, f), info))

    note("")
    note("统计: %s" % counts)
    with io.open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(report))
    print("report written: %s" % REPORT)
    print(counts)


if __name__ == "__main__":
    main()
