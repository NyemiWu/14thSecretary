#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 Word 97-2003 老格式 .doc（OLE2）提取成 Markdown。

pandoc 不支持 .doc，本机也没有 LibreOffice。这里直接按 MS-DOC 规范读
WordDocument 流的文本片段表（piece table）取正文。

代价：拿不到标题层级、表格、加粗等格式，只能出段落。
拿到 .docx 原件后应重跑 import_kb.py 替换。

    python scripts/import_doc.py
"""

import io
import os
import re
import struct
import sys

import olefile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"C:\Users\ROG\Documents\项目文档\14th\十四号城项目20260921打包"
REPORT = os.path.join(ROOT, "scripts", "import_doc_report.txt")


def read_stream(ole, name):
    try:
        return ole.openstream(name).read()
    except Exception:
        return None


def extract_text(path):
    ole = olefile.OleFileIO(path)
    wd = read_stream(ole, "WordDocument")
    if wd is None:
        raise ValueError("没有 WordDocument 流")

    flags = struct.unpack_from("<H", wd, 0x0A)[0]
    tbl_name = "1Table" if (flags >> 9) & 1 else "0Table"
    tbl = read_stream(ole, tbl_name)
    if tbl is None:
        tbl = read_stream(ole, "1Table") or read_stream(ole, "0Table") or b""

    fc_clx = struct.unpack_from("<I", wd, 0x01A2)[0]
    lcb_clx = struct.unpack_from("<I", wd, 0x01A6)[0]
    ccp_text = struct.unpack_from("<I", wd, 0x004C)[0]

    clx = tbl[fc_clx:fc_clx + lcb_clx]
    if not clx:
        raise ValueError("CLX 为空（fcClx=%d lcbClx=%d）" % (fc_clx, lcb_clx))

    # 跳过 Prc，找到 Pcdt (0x02)
    i = 0
    pcdt = None
    while i < len(clx):
        t = clx[i]
        if t == 0x01:
            cb = struct.unpack_from("<H", clx, i + 1)[0]
            i += 3 + cb
        elif t == 0x02:
            lcb = struct.unpack_from("<I", clx, i + 1)[0]
            pcdt = clx[i + 5:i + 5 + lcb]
            break
        else:
            break
    if pcdt is None:
        raise ValueError("CLX 里没有找到 Pcdt")

    n = (len(pcdt) - 4) // 12
    cps = [struct.unpack_from("<I", pcdt, j * 4)[0] for j in range(n + 1)]
    base = (n + 1) * 4

    chunks = []
    for j in range(n):
        if cps[j] >= ccp_text:          # 正文之后的页眉页脚脚注不要
            break
        pcd = pcdt[base + j * 8: base + j * 8 + 8]
        fc = struct.unpack_from("<I", pcd, 2)[0]
        compressed = bool(fc & 0x40000000)
        fc &= 0x3FFFFFFF
        ln = cps[j + 1] - cps[j]
        if compressed:
            raw = wd[fc // 2: fc // 2 + ln]
            chunks.append(raw.decode("cp1252", "replace"))
        else:
            raw = wd[fc: fc + ln * 2]
            chunks.append(raw.decode("utf-16-le", "replace"))

    text = "".join(chunks)
    ole.close()
    return text


def to_markdown(text, title):
    text = text.replace("\x07", "\t")      # 单元格结束
    text = text.replace("\x0b", "\n")      # 软换行
    text = text.replace("\x0c", "\n")      # 分页
    text = text.replace("\r", "\n")
    text = text.replace("\x1e", "-")
    text = text.replace("\x1f", "\u00a0")
    text = re.sub(r"[\x00-\x08\x0e-\x1a\x1c-\x1d]", "", text)

    lines = []
    for ln in text.split("\n"):
        s = ln.replace("\t", " ").rstrip()
        s = re.sub(r"[ \u00a0]{2,}", " ", s)
        lines.append(s)

    # 连续空行压成一个
    out = []
    blank = 0
    for s in lines:
        if not s.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(s)
    md = "\n".join(out).strip()

    head = "# " + title + "\n\n"
    if md.startswith("#"):
        return md + "\n"
    return head + md + "\n"


def main():
    report = []
    # 源分类 -> 目标（按 import_kb.py 的 MAP 走）
    jobs = [
        (os.path.join(SRC, "世界观", "意识交互方法集.doc"), "text/worldview"),
        (os.path.join(SRC, "人物角色相关", "女二设定.doc"), "text/characters"),
        (os.path.join(SRC, "人物角色相关", "人物角色名单（过期）.doc"), "text/characters"),
        (os.path.join(SRC, "剧情", "其他文本", "环状雨楼群.doc"), "text/story/misc"),
    ]

    for src, out_dir in jobs:
        name = os.path.splitext(os.path.basename(src))[0]
        name = name.replace("&", "-").replace("：", "-").replace(":", "-")
        name = re.sub(r'[\\/*?"<>|]', "-", name).strip()
        if not os.path.isfile(src):
            report.append("MISSING %s" % src)
            continue
        try:
            text = extract_text(src)
            md = to_markdown(text, name)
        except Exception as exc:
            report.append("FAIL   %-40s %s" % (os.path.basename(src), exc))
            continue
        dest = os.path.join(ROOT, "docs", out_dir, name + ".md")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        front = "---\ntitle: %s\n---\n\n" % name
        with io.open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(front + md)
        report.append("OK     %-40s %6d 字 -> %s"
                      % (os.path.basename(src), len(md), os.path.join("docs", out_dir, name + ".md")))

    with io.open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
