## 稿件信息

| 项 | 值 |
|---|---|
| 稿件编号 | |
| 文件 | `docs/buffer/submissions/___-___.md` |
| 目标分区 | `docs/text/...` 或 `docs/interactive/...` |
| 范围 | 新增 / 修订 / 删除 |
| 申请审核人数 quorum | |
| 判定模式 | `unanimous`（全票） / `lazy`（沉默期） |

## 改了什么

## 为什么改

## 需要重点看哪几段

## 提交人自查

- [ ] `reviews` 里所有 `verdict` 都是 `pending` —— 我没有替审核人填判定
- [ ] 正文按目标分区的正式模板写，通过后可直接搬运，不需要二次改写
- [ ] 文件路径全 ASCII，中文只出现在 `title` 和正文里
- [ ] `target` 指向**正式分区**，不是另一份待审稿
- [ ] 已跑 `python scripts/gen_board.py`，审核看板已同步
- [ ] 已在 `mkdocs serve` 里确认稿件渲染正常

---

**审核人看这里**

在稿件头部的 `reviews` 里填**你自己**那一行：

```yaml
  - who: 你的代号
    verdict: approve     # approve 绿灯 / reject 反对 / abstain 弃权
    date: YYYY-MM-DD
    note: 一句话理由
```

然后在下方写出必要说明。判定标准见 [`docs/buffer/rules.md`](../blob/main/docs/buffer/rules.md)。

- [ ] 我不是本稿的提交人（自己不能审自己的稿）
- [ ] `reject` 时已在 `note` 里写明理由
