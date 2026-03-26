# 无 API Key 工作流

在没有 Brave Search API key 的情况下，仍可用这个 skill 生成航天情报简报。

## 适用场景

- 先验证简报结构与输出风格
- 手动挑选高质量候选条目
- 暂时不做大规模自动化采集

## 工作方式

1. 先用内置网页搜索、浏览器或人工检索收集候选来源。
2. 把候选信息整理成 JSON 数组。
3. 使用 `scripts/space_news_brief.py` 生成最终中文简报。

## 最小字段

每条候选项建议包含：

- `title`
- `category`
- `date`
- `entities`
- `summary`
- `impact`
- `url`
- `source_type`
- `item_type`
- `cross_confirmed`

## 推荐做法

- 优先整理官方机构页面、论文原文页、会议官网、GitHub 仓库、公司官网。
- 不要一开始追求很多条，先做 5 到 10 条高信号样例。
- 先把 `summary` 和 `impact` 写扎实，再让脚本负责统一格式与排序。

## 示例命令

```bash
uv run python scripts/space_news_brief.py --input references/real_candidates_2026-03-23.json --output references/brief.md --start-date 2026-03-17 --end-date 2026-03-23 --top-n 30
```

## 何时再接 API

当你需要下面这些能力时，再去接搜索 API：

- 定期自动跑周报 / 月报
- 扩大候选覆盖面
- 降低人工收集成本
- 做更稳定的批量追踪
