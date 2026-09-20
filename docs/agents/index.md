---
title: 机哥分区
tags:
  - 元
---

# 机哥分区

**这一区是写给 AI 助手的。** 人类成员看[缓冲分区](../buffer/index.md)和[编辑规范](../buffer/style-guide.md)就够了。

新人（不管是人是机）第一次进这个仓库，从这里读起，不要先翻内容 ——
这个仓库有 100+ 篇文档、6 个生成脚本、一套缓冲流程，**先搞清结构再动手**，
否则很容易把生成的东西手改了、或者把该走缓冲的内容直接写进正式分区。

## 如果你是 agent，按这个顺序读

| 顺序 | 页面 | 读完你会知道 |
|---|---|---|
| 1 | [上手](onboarding.md) | 项目是什么、环境怎么起、改完怎么验证怎么发 |
| 2 | [仓库地图](repo-map.md) | 每个目录文件干什么，**哪些是生成的不许手改** |
| 3 | [任务手册](workflows.md) | 六种常见任务的步骤化做法 |
| 4 | [硬规则](constraints.md) | 必须做和绝对不能做的事 |
| 5 | [已知坑](pitfalls.md) | 踩过的坑 + 报错原文（可搜） |

赶时间的话，只读 [硬规则](constraints.md) 也能避开大部分事故。

## 这个分区里放什么

| 放这里 | 不放这里 |
|---|---|
| 给 agent 的上手与运维文档 | 世界观、剧情、图鉴等**内容** → [文本分区](../text/index.md) |
| skill、工具链、自动化相关的说明 | 待审稿件 → [缓冲分区](../buffer/pending/) |
| 新增 agent 资产时的登记 | 跑得起来的工具 → [可交互叙事分区](../interactive/index.md) |

**后续凡是跟 skill、agent 协作、自动化有关的内容，都更新到这一区。**

## 一句话概括这个仓库

> 一个朋友团体的世界观设定集，用 MkDocs + Material 构建成静态站，
> 发在 GitHub Pages 上。所有人靠 PR/缓冲流程投稿，管理员放行后合并。

| | |
|---|---|
| 线上站点 | <https://nyemiwu.github.io/14thSecretary/> |
| 仓库 | <https://github.com/NyemiWu/14thSecretary> |
| 技术栈 | MkDocs 1.6 + Material 9.7 + awesome-pages，零外部 CDN 依赖 |
| 发布 | push 到 `main` → GitHub Actions 自动构建发布 |
| 内容量 | 111 篇 Markdown · 12 个内容板块 |

## 机器可读入口

仓库根目录有一份 [`AGENTS.md`](https://github.com/NyemiWu/14thSecretary/blob/main/AGENTS.md)，
是给支持该约定的 agent 工具（Codex / Claude Code 等）自动加载用的，
内容是这一区的精简摘要 + 指路。**改了规则记得同步那一份。**
