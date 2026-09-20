/* 14thSecretary · 在内容页注入「编辑此条目」入口
 *
 * 目标不是 GitHub 的网页编辑器，而是站内的内容后台（/editor/）。
 * 点进去后编辑器会拉取本文原文，改完提交进 buffer/pending/ —— 原文不受影响。
 *
 * 两个细节：
 *   1. 站点根路径从 header 的 logo 链接推出来（它相对当前页面），
 *      所以任意嵌套深度的页面都不用改代码。
 *   2. 自动生成的聚合页（板块落地页）不给「编辑」，改成「在此分区新建条目」——
 *      因为它们由 scripts/gen_section_index.py 生成，改了下次构建就被覆盖。
 */
(function () {
  "use strict";

  /* logo 的 href 是相对当前页面的站点根，例：从 /text/worldview/ 看是 "../.." */
  function siteRoot() {
    var a = document.querySelector(
      "a.md-header__button[data-md-component='logo'], a.md-header__button.md-logo"
    );
    var h = a ? (a.getAttribute("href") || "") : "";
    if (!h) return ".";
    h = h.replace(/\/+$/, "");
    return h || ".";
  }

  /* 从 Material 自动生成的「编辑此页」链接里取出源文件路径。
     例：https://github.com/o/r/edit/main/docs/text/a.md  ->  text/a.md */
  function sourceRel() {
    var a = document.querySelector("a.md-content__button[rel='edit']");
    if (!a) return null;
    var m = (a.getAttribute("href") || "").match(/\/edit\/[^/]+\/(.+)$/);
    if (!m) return null;
    var p = decodeURIComponent(m[1]);
    return p.indexOf("docs/") === 0 ? p.slice(5) : null;
  }

  /* 页面上有没有「本页自动生成」的提示块 */
  function isGenerated(article) {
    var t = article.querySelectorAll(".admonition-title"), i;
    for (i = 0; i < t.length; i++) {
      if ((t[i].textContent || "").indexOf("本页自动生成") >= 0) return true;
    }
    return false;
  }

  function mount() {
    var article = document.querySelector("article.md-content__inner");
    if (!article) return;

    var rel = sourceRel();
    if (!rel) return;
    if (/^buffer\//.test(rel)) return; /* 缓冲区稿件本身不给按钮 */

    var root = siteRoot();
    var link = document.createElement("a");
    link.className = "edit-entry";

    if (isGenerated(article)) {
      var sec = rel.match(/^text\/([^/]+)\//);
      link.href = root + "/editor/?mode=new" + (sec ? "&section=" + encodeURIComponent(sec[1]) : "");
      link.title = "本页由脚本生成，直接改会在下次构建时被覆盖 —— 在这个分区新建一条内容";
      link.innerHTML = '<span class="ee-ico">+</span>在此分区新建条目';
    } else {
      link.href = root + "/editor/?src=" + encodeURIComponent(rel);
      link.title = "用站内编辑器起草修改稿，提交后进入缓冲区等审核（不会直接改动本页）";
      link.innerHTML = '<span class="ee-ico">&#9998;</span>编辑此条目';
    }

    var h1 = article.querySelector("h1");
    if (h1 && h1.parentNode) h1.parentNode.insertBefore(link, h1.nextSibling);
    else article.insertBefore(link, article.firstChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
