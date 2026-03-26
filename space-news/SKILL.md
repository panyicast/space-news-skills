---
name: space-news
description: Generate structured Chinese intelligence briefs about recent developments in the space sector, with special emphasis on artificial intelligence in space applications and research. Use when Codex needs to search the last week, last month, or a specified date range for important space news, mission updates, AI-in-space developments, open-source projects, research papers, international conferences, university/lab results, new agency programs or products, and startup/company activity, then classify, rank, and summarize them in a fixed report format.
---

# Space News

Produce a fixed-format Chinese intelligence brief for recent developments in the space sector, with priority on AI-related space developments.

## Default Scope

- Default time range: last 7 days.
- Default output count: 30 items.
- Default language: Chinese.
- Default emphasis: AI in space, remote sensing AI, mission autonomy, onboard intelligence, mission operations intelligence, space robotics, SSA/STM intelligence, simulation and validation, and space engineering toolchains.

## Coverage

Search broadly but keep the final brief tightly relevant to the space sector. Expand search breadth by default, especially when the user asks for a monthly brief, research roundup, or a topic-focused scan such as 航天 AI, 遥感基础模型, 深空自主, 小推力变轨, 月球探测, or 开源项目. Include the following when they are material and recent:

- Space news and mission events.
- AI in space applications and engineering.
- Remote sensing and Earth observation AI.
- Research papers, preprints, university and lab results.
- International conferences, workshops, calls for papers, and event agendas.
- Open-source projects and major repository updates.
- New programs, products, platforms, and initiatives from space agencies.
- Commercial space companies, especially AI-related products, partnerships, funding, and startup profiles.

Coverage must span the major space application domains when relevant:

- 军事与国防航天
- 商业航天
- 民用与公共服务航天
- 科研与学术航天
- 国际航天机构与国家项目

Reject generic AI news with no clear space relevance.

## Source Priority

Use higher-authority sources first.

1. Official sources: agencies, companies, labs, universities, conference sites, journals, arXiv, project pages, GitHub repositories.
2. High-quality media: established space and mainstream outlets.
3. Social or secondary aggregation: only as supporting context, not as the main basis for a key claim when better sources exist.

Default source mix for meaningful coverage should span multiple source families whenever possible, rather than relying on a single search provider or one media outlet:

- 官方机构站点：NASA, ESA, JAXA, ISRO, CNSA 及相关项目页、实验室、大学、会议官网。
- 行业媒体：SpaceNews, SpaceNews 类行业媒体, Spaceflight Now, Space.com，以及具备原始采访或任务报道能力的科技媒体。
- 论文与预印本：arXiv、期刊页面、会议页面、实验室论文页。
- 开源平台：GitHub 仓库、项目主页、模型页、发布说明。
- 社交与视频信号：X、YouTube、机构官方频道、任务简报视频，仅作为补充线索或交叉验证来源。

Do not treat Tavily, Brave, or any other single search surface as the only information source. Search APIs are discovery tools, not the final source base.

When multiple sources exist, prefer the original source page and keep at least one direct source link in the final brief.

## Search Principles

Search with deliberate breadth before narrowing. Expand the search surface when the topic is broad, the date range is longer than one week, or the brief is expected to capture research and open-source signals in addition to news.

Continuously improve the search logic from prior runs. When repeated searches uncover new high-value keywords, entities, repositories, journals, conferences, media outlets, official channels, or source families, add them to the default search logic for future runs. The default direction of change is expansion, not contraction.

Apply these principles:

- Use time-slicing for longer windows. For monthly or multi-week scans, split the date range into smaller windows such as 上旬 / 中旬 / 下旬 or week-by-week, then merge and deduplicate.
- Search by topic cluster, not one generic query. For example, split into 遥感基础模型 / SAR 智能处理 / 轨道动力学 / 小推力变轨 / 月球探测 / 深空探测 / 在轨自主 / 空间安全 / 空间数据网络 / 开源项目.
- Search by source family, not only by topic. Run separate searches for 官方机构, 行业媒体, 论文源, GitHub, and when useful X / YouTube.
- Expand queries iteratively. If a broad query returns generic or weakly relevant material, follow up with narrower technical phrases, mission names, program names, dataset names, model names, or organization names.
- Capture newly discovered high-value search terms. When a search run surfaces recurring mission names, paper titles, model names, datasets, systems, labs, companies, or program names, promote them into future query sets.
- Capture newly discovered high-value sources. When a search run repeatedly yields strong material from a new site, channel, repository family, conference page, or journal page, add that source to the default source pool for future runs.
- Never proactively reduce search breadth. Do not remove existing topic clusters, keyword families, or source families just because one run produced weak results. Reweighting is allowed, but silent narrowing is not.
- Prefer fewer stronger searches over one oversized vague search.
- When official or academic sources are sparse, use high-quality media or project pages to discover entities, then pivot back to original sources.

Recommended query families for 航天 AI work include combinations of the following:

- `space AI`
- `satellite AI`
- `space autonomy`
- `on-orbit autonomy`
- `space robotics`
- `mission planning spacecraft`
- `orbital dynamics AI`
- `space rendezvous trajectory optimization`
- `low-thrust orbit transfer AI`
- `reinforcement learning spacecraft`
- `lunar exploration AI`
- `moon robotics spacecraft autonomy`
- `deep space probe autonomy`
- `Mars powered descent guidance learning`
- `remote sensing foundation model`
- `SAR foundation model`
- `Earth observation vision language model`
- `cross-view geo-localization satellite`
- `space situational awareness AI`
- `space data center`
- `orbital data center`
- `LEO data network`
- `space edge computing`
- `satellite stereo pipeline learning`
- `space GitHub`
- `remote sensing GitHub`

Rank by intelligence value, not only by recency.

Prioritize items that have one or more of the following:

- Major mission milestone, failure, anomaly, launch, landing, return, contract, or formal release.
- Clear AI adoption in real space missions, products, operations, engineering, simulation, testing, or data pipelines.
- Official confirmation by agencies, companies, labs, or conference organizers.
- Technical novelty, first-of-kind milestone, or unusually strong engineering relevance.
- Strong downstream impact on industry, research, mission design, operations, or open-source ecosystems.
- Cross-confirmation across multiple credible sources.

Use recency as a tie-breaker after importance and source quality.

## Deduplication Rules

Deduplicate aggressively. The nominal target count is a ceiling, not a quota.

Apply these rules before ranking the final brief:

- One source event, one item. Do not split a single official announcement, paper, conference page, or repository into multiple items with different analytical angles.
- One project, one item. The same paper, open-source repository, conference, product, platform, or program should appear at most once in the final list.
- Do not convert trend commentary into fake events. If several observations come from the same underlying source, keep one event entry and move the synthesis into `本期摘要` or a short trends section.
- Prefer fewer, higher-signal items over padded lists. It is acceptable to output 6-15 items if that is the true high-value set for the chosen time range.
- When multiple reports describe the same development, keep the highest-authority original source and collapse the rest into supporting context only.
- For open-source coverage, the same repository should only be listed once unless there are clearly separate, independently newsworthy releases within the date range.

In short: maximum count is optional; unique, source-grounded items are mandatory.

## Classification

Assign each selected item to one primary content category:

- 航天任务与任务动态
- AI 航天技术与产品
- 遥感与对地观测 AI
- 科研论文与高校成果
- 国际会议与学术活动
- 开源项目与工具生态
- 航天机构项目与新产品
- 商业航天与初创公司

Also assign one primary domain tag when possible:

- 军事与国防
- 商业航天
- 民用与公共服务
- 科研与学术
- 国际机构与国家项目

Use the content category as the main classification field in the report. Mention the domain tag naturally in the content summary or involving entities when it adds value.

If an item is mainly an anomaly, accident, or delay, make that explicit in the title or introduction.

## Report Format

Always use this fixed output structure:

1. 标题
2. 时间范围
3. 本期摘要
4. 重点事件（默认 30 条）

Use the tone and section layout from `references/output-template.md`.

For each item, always include:

- 排名
- 标题
- 分类
- 时间
- 涉及主体
- 内容摘要
- 关注点 / 影响
- 来源链接

Title handling:

- If a title is already in Chinese, keep it as is.
- If a title is pure English and a verified Chinese rendering is available, render it as `English Title（中文标题）`.
- Do not force Chinese title additions for mixed-language titles unless it clearly improves readability.

## Writing Rules

Write in Chinese, in an intelligence-brief style rather than a marketing-news style.

Treat this skill as a two-layer workflow:

- 候选层：use automation to collect, merge, deduplicate, classify, and pre-rank candidates.
- 成品层：for the final selected items, prefer reading the original source page and writing the `内容摘要` as a source-grounded Chinese synthesis rather than relying only on titles or short summaries.

For `内容摘要`:

- Write a substantive Chinese paragraph, not a title paraphrase.
- Usually target about 180 to 300 Chinese characters unless the user asks for shorter or longer output.
- Explain what happened, who is involved, what the technical or programmatic background is, and why it matters.
- Prefer source-grounded synthesis for final selected items. Do not rely only on the title or a one-sentence summary when the source page is available.
- For high-value original sources such as NASA, ESA, JAXA, ISRO, CNSA, and other major agency pages, default to reading the article body and extracting concrete facts before writing the `内容摘要`.
- For NASA items in particular, do not keep template-like summaries. The `内容摘要` should identify the specific programs, pathways, activities, systems, milestones, or opportunities described in the article.
- If the item is a paper, explain the problem, claimed contribution, and likely practical relevance.
- If the item is an open-source project, explain what it does, what changed, and why it may matter to the space ecosystem.
- If the item is a conference or call for papers, explain the theme, organizer, date, and why it is strategically relevant.
- If public information is limited, say so clearly instead of inventing details.
- If automated enrichment still contains navigation text, boilerplate, or noisy extraction, treat it only as a draft and refine the final selected items manually or semi-manually before producing the deliverable brief.
- If a NASA or other major agency page cannot be cleanly extracted, do not fall back to generic wording. Either refine the extraction, temporarily downgrade the item, or explicitly mark that the original article body was not reliably extracted.

For `关注点 / 影响`:

- Keep it concise.
- State why the item deserves attention from a strategic, technical, industrial, or research perspective.

## Recommended Workflow

1. Determine the date range.
2. Identify the user’s optional focus, if any, such as a region, organization, or subdomain.
3. Expand the search space first: split long date ranges into smaller windows and split broad themes into topic clusters.
4. Search for candidate items across official, academic, open-source, and media sources.
5. Run at least one search pass aimed specifically at papers / preprints and at least one pass aimed specifically at GitHub / open-source when the topic involves 航天 AI, 遥感 AI, or research trends.
6. When possible, add one discovery pass from social/video surfaces such as X or YouTube for conference briefings, launch briefings, demos, and official talks, then confirm against stronger sources.
7. Remove duplicates and low-value items.
8. Keep only items with clear space relevance.
9. Classify items into the predefined categories.
10. Rank them by intelligence value.
11. For the final selected items, read the original source pages when possible and refine the `内容摘要` into a source-grounded Chinese synthesis.
12. Write the Chinese brief in the fixed format.

## Reference Files

Read these references as needed:

- `references/search-playbook.md`: source map, search angles, and collection workflow.
- `references/output-template.md`: fixed Chinese output template.
- `references/category-guidance.md`: category definitions and tagging hints.
- `references/no-api-workflow.md`: fallback workflow when no search API key is available.
- `references/future-enhancements.md`: optional future upgrades for collection, ranking, and automation.

## Scripts

- `scripts/collect_space_news.py`: collect candidate items from Brave Search into normalized JSON candidates.
- `scripts/collect_spaceflightnewsapi.py`: collect recent structured space news from Spaceflight News API as one candidate source.
- `scripts/merge_space_news_candidates.py`: merge and deduplicate multiple candidate JSON files.
- `scripts/rewrite_space_news_candidates.py`: rewrite mixed-language summaries into Chinese intelligence-brief style.
- `scripts/enrich_space_news_candidates.py`: fetch source pages for top candidates and generate more detailed Chinese summaries.
- `scripts/space_news_overrides.py`: maintain high-priority title, summary, and impact overrides for known high-value or high-frequency items.
- `scripts/space_news_brief.py`: rank candidate items and render the fixed-format Chinese intelligence brief.

Typical flow:

1. Collect candidate items into JSON.
2. Merge and deduplicate multiple sources when needed.
3. Rewrite mixed-language summaries into Chinese baseline style when needed.
4. Fetch source pages for the top selected candidates and enrich them into draft Chinese summaries.
5. Apply high-priority overrides for known high-value titles when repeated extraction quality is unstable or when a hand-verified summary should take precedence.
6. For the final selected items, refine the content summaries against the original source content when quality matters.
7. Render the final ranked markdown brief.
8. After rendering, re-read the current final markdown and verify that each selected item’s title, `内容摘要`, and `来源链接` still refer to the same source event. If ranking drift or reordering caused a mismatch, fix the source data first and re-render.

If no search API key is available, follow `references/no-api-workflow.md` and use a manual or browser-assisted collection step first.

Override policy:

- Use `scripts/space_news_overrides.py` for items that repeatedly regress into template-like summaries, especially high-value original-source items from NASA, ESA, or other major agencies.
- Keep overrides narrowly scoped to known titles or stable recurring items; do not use overrides as a substitute for broad extraction quality improvements.
- Prefer source-grounded overrides that were verified against the original page, and update or remove them if the underlying source pattern changes.

Example:

```bash
uv run python scripts/collect_space_news.py --output references/candidates.json --freshness-days 7
uv run python scripts/collect_spaceflightnewsapi.py --output references/news_candidates.json --days 7 --limit 50
uv run python scripts/merge_space_news_candidates.py references/candidates.json references/news_candidates.json --output references/merged_candidates.json
uv run python scripts/rewrite_space_news_candidates.py --input references/merged_candidates.json --output references/rewritten_candidates.json
uv run python scripts/enrich_space_news_candidates.py --input references/rewritten_candidates.json --output references/enriched_candidates.json --limit 10
uv run python scripts/space_news_brief.py --input references/enriched_candidates.json --output references/brief.md --start-date 2026-03-17 --end-date 2026-03-23 --top-n 30
```

## Notes

- Users may specify a time range, geography, organization, or subdomain, but the default mode is broad tracking across the whole space sector.
- Unless the user asks otherwise, optimize for high-signal recent developments rather than exhaustive completeness.
- When a result set is crowded, prefer quality over quantity even if the nominal target is 20 items.
- See `examples/weekly-brief-example.md` for a concrete example of the expected final writing style and structure.
