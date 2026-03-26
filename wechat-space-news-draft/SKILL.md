---
name: wechat-space-news-draft
description: Upload a generated `space-news` monthly or weekly Markdown brief to the WeChat Official Account draft box as a draft article. Use when the user wants to turn a local `space-news` Markdown file into a WeChat draft, especially for files like `space-news-monthly-*.md` or `space-news-weekly-*.md`, with cover image, title, digest, source URL, and optional image uploading.
---

# WeChat Space News Draft

Use this skill when the user wants to upload a local `space-news` Markdown brief into the WeChat Official Account draft box.

This skill is for **draft creation only**. It does **not** publish articles.

## When To Use

Use this skill when the user asks to:

- 上传月报到公众号草稿箱
- 上传周报到公众号草稿箱
- 把 `space-news` Markdown 转成微信公众号草稿
- 用本地 `.md` 生成公众号草稿
- 给月报创建微信草稿

Typical input files include:

- `D:\Spark\openclaw\space-news-monthly-*.md`
- `D:\Spark\openclaw\space-news-weekly-*.md`
- other local Markdown files produced by the `space-news` workflow

## Workflow

1. Confirm the source Markdown file path.
2. Confirm the cover image path, or use the default cover `D:\Spark\openclaw\cover.jpeg` if the user is following the standard publication workflow.
3. Read the Markdown and derive:
   - title from the first `#` heading unless the user overrides it
   - digest from the `本期摘要` section when available
   - source URL only when the user explicitly overrides it; for a compiled monthly/weekly brief, do not automatically use the first event link as the article-level original URL
4. Convert the Markdown into WeChat-compatible HTML.
5. Upload the cover image as permanent material.
6. Upload local inline images when needed.
7. Create a WeChat draft via the official draft API.
8. Report the created draft title and `media_id` back to the user.

## Required Environment

This workflow requires WeChat Official Account credentials via either:

- `WECHAT_APPID`
- `WECHAT_SECRET`

or explicit CLI arguments.

If credentials are missing, stop and tell the user what is missing.

## Default Behavior

- Create draft only, never publish.
- Preserve the article body as local Markdown rendered into HTML.
- Use the default cover `D:\Spark\openclaw\cover.jpeg` unless the user overrides it.
- Keep plain reference links at the end unless the user asks not to.
- Prefer the Markdown first heading as the draft title.
- For compiled monthly/weekly briefs, do not automatically assign the first event link as the article-level `content_source_url`; only set it when the user explicitly provides one.

## Space-News Specific Rules

For `space-news` monthly or weekly briefs:

- Keep the Chinese report structure intact.
- Do not rewrite the report body unless the user explicitly asks.
- If the Markdown contains many source links, keeping a references block is acceptable for traceability.
- Before uploading, it is acceptable to do a quick sanity check that the latest rendered Markdown version is the intended one.
- If the current `space-news` brief was recently regenerated multiple times (`v18`, `v19`, `v24`, etc.), prefer the latest explicitly confirmed version.

## Scripts

- `scripts/upload_wechat_draft.py`: Generic Markdown → WeChat draft uploader.
- `scripts/upload_space_news_monthly_draft.py`: Wrapper for `space-news` monthly/weekly reports; auto-infers a cleaner title and digest from the report.
- `scripts/upload_latest_space_news_draft.py`: Finds the latest generated monthly or weekly `space-news` markdown file and uploads it as a draft.

## Example

Preferred for `space-news` reports:

```bash
uv run python scripts/upload_space_news_monthly_draft.py \
  --md "D:\\Spark\\openclaw\\space-news-monthly-2026-03-01_to_2026-03-25-v24.md" \
  --author "Space AI Weekly"
```

One-click latest monthly draft:

```bash
uv run python scripts/upload_latest_space_news_draft.py \
  --kind monthly \
  --dir "D:\\Spark\\openclaw" \
  --author "Space AI Weekly"
```

Generic mode:

```bash
uv run python scripts/upload_wechat_draft.py \
  --md "D:\\Spark\\openclaw\\space-news-monthly-2026-03-01_to_2026-03-25-v24.md" \
  --author "Space AI Weekly"
```

## Notes

- This skill should be used for deterministic draft creation, not for browser automation.
- If the user wants a polished WeChat-specific layout later, that can be a follow-up refinement, but the base workflow should stay stable and reproducible.
