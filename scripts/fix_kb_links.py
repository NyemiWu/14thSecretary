#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修掉知识库导入时残留的坏链。

原 Word 文档里的交叉引用指向同目录的 .docx/.doc/.html，转换后这些路径不存在了。
本脚本按 import_kb.py 的同一套映射，把它们改成站点内的相对链接；
映射不到的（比如源包里就没有的 .wpsonline 临时文件）退化成纯文本。

    python scripts/fix_kb_links.py
"""

import io
import os
import posixpath
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from import_kb import SRC, SKIP_EXT, slugify, target_dir_for  # noqa: E402

DOCS = os.path.join(ROOT, "docs")
LINKY_EXT = (".docx", ".doc", ".html", ".wpsonline", ".mp4")


def build_maps():
    """orig 相对路径 -> docs 相对路径；反向再存一份 docs 路径 -> orig 所在目录。"""
    new_of_orig = {}
    orig_dir_of_new = {}
    used = {}
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        rel_dir = os.path.relpath(root, SRC).replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""
        tdir = target_dir_for(rel_dir)
        if tdir is None:
            continue
        tdir = tdir.replace("\\", "/")
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext in SKIP_EXT:
                continue
            stem = slugify(os.path.splitext(f)[0])
            key = (tdir, stem)
            if key in used:
                used[key] += 1
                stem = "%s-%d" % (stem, used[key])
            else:
                used[key] = 1
            new_rel = tdir + "/" + stem + (".md" if ext in (".docx", ".doc", ".html") else ext)
            # 统一成相对 docs/ 的路径，跟 main() 里 walk 出来的 rel_docs 对齐
            if new_rel.startswith("docs/"):
                new_rel = new_rel[5:]
            orig_rel = (rel_dir + "/" + f) if rel_dir else f
            new_of_orig[orig_rel] = new_rel
            orig_dir_of_new[new_rel] = rel_dir
    return new_of_orig, orig_dir_of_new


LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def main():
    new_of_orig, orig_dir_of_new = build_maps()
    fixed = 0
    stripped = 0
    touched = []

    for root, dirs, files in os.walk(os.path.join(DOCS, "text")):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            rel_docs = os.path.relpath(path, DOCS).replace("\\", "/")
            orig_dir = orig_dir_of_new.get(rel_docs)
            if orig_dir is None:
                continue

            with io.open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            original = text

            def repl(m):
                nonlocal fixed, stripped
                label, target = m.group(1), m.group(2)
                if not target.lower().endswith(LINKY_EXT):
                    return m.group(0)
                clean = target.replace("%20", " ").replace("\\", "/")
                joined = posixpath.normpath(posixpath.join(orig_dir, clean))
                new_target = new_of_orig.get(joined)
                if new_target:
                    rel = posixpath.relpath(new_target, posixpath.dirname(rel_docs))
                    fixed += 1
                    return "[%s](%s)" % (label, rel)
                stripped += 1
                return label or ""

            text = LINK_RE.sub(repl, text)
            if text != original:
                with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text)
                touched.append(rel_docs)

    print("修好链接: %d 条" % fixed)
    print("退化成纯文本: %d 条" % stripped)
    print("改动文件: %d 个" % len(touched))
    for t in touched:
        print("  " + t)


if __name__ == "__main__":
    main()
