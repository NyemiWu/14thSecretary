## 稿件信息

| 项 | 值 |
|---|---|
| 稿件编号 | |
| 文件 | `docs/buffer/submissions/___-___.md` |
| 目标分区 | `docs/text/...` 或 `docs/interactive/...` |
| 范围 | 新增 / 修订 / 删除 |

## 改了什么

## 为什么改

## 需要重点看哪几段

## 提交人自查

- [ ] 文件路径全 ASCII，中文只在 `title` 和正文里
- [ ] `target` 指向**正式分区**，不是另一份待审稿
- [ ] `status` 是 `submitted` 或 `reviewing`
- [ ] **已发审核请求邮件到 `review@example.com`**
- [ ] 已跑 `python scripts/gen_board.py`，审核看板已同步
- [ ] 已在 `mkdocs serve` 里确认稿件渲染正常

---

**审核人看这里**

1. 读稿件本身（`docs/buffer/submissions/` 下的文件）。
2. 通过 / 不通过。
3. 通过的：把稿件移进 `docs/buffer/public/`，抬头补
   `status: public`、`reviewed_by`、`reviewed_on`、`public_until`，
   并开一个 `[公示] 编号 标题` 的 Issue 供大家点赞点踩。
4. 不通过的：在 PR 里说明理由。

完整流程见 [`docs/buffer/rules.md`](../blob/main/docs/buffer/rules.md)。

- [ ] 我不是本稿的提交人
