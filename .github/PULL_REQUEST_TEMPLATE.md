## 稿件信息

| 项 | 值 |
|---|---|
| 稿件编号 | |
| 文件 | `docs/buffer/pending/___-___.md` |
| 目标分区 | `docs/text/...` 或 `docs/interactive/...` |
| 范围 | 新增 / 修订 / 删除 |

## 改了什么

## 为什么改

## 需要重点看哪几段

## 提交人自查

- [ ] 稿件放在 `docs/buffer/pending/`，路径全 ASCII，中文只在 `title` 和正文里
- [ ] `target` 指向**正式分区**，不是另一份缓冲稿
- [ ] 正文结构照 `docs/buffer/entries.md` 的模板写
- [ ] 已在 `mkdocs serve` 里确认稿件渲染正常
- [ ] 已跑 `python scripts/gen_board.py`

---

**管理者看这里**

两个动作二选一：

**通过** → 进公示

```bash
git mv docs/buffer/pending/012-xxx.md docs/buffer/public/012-xxx.md
# 抬头补 reviewed_by / reviewed_on / public_until，tags 改成 公示
python scripts/gen_board.py
```

再开一个 `[公示] 012 标题` 的 Issue 供大家 👍 / 👎。

**要求更改** → 删掉稿件，在下面写清要改什么，提交人改完重新提交。

完整流程见 [`docs/buffer/rules.md`](../blob/main/docs/buffer/rules.md)。
