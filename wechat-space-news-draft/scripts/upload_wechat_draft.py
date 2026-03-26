import argparse
import codecs
import html
import json
import os
import re
from pathlib import Path

try:
    import requests
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Missing dependency: requests. Install it with `uv pip install --system requests` or run in an environment where requests is available."
    ) from exc


def request_wechat(method: str, url: str, **kwargs) -> dict:
    resp = requests.request(method, url, timeout=30, **kwargs)
    resp.raise_for_status()
    data = resp.json()
    if "errcode" in data and data["errcode"] != 0:
        raise RuntimeError(
            f"WeChat API error {data['errcode']}: {data.get('errmsg', 'unknown error')}"
        )
    return data


def request_wechat_json_utf8(method: str, url: str, payload: dict) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    return request_wechat(method, url, data=body, headers=headers)


def get_access_token(appid: str, secret: str) -> str:
    url = (
        "https://api.weixin.qq.com/cgi-bin/token"
        f"?grant_type=client_credential&appid={appid}&secret={secret}"
    )
    data = request_wechat("GET", url)
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"Token response missing access_token: {data}")
    return token


def upload_thumb_material(token: str, img_path: Path) -> str:
    url = (
        "https://api.weixin.qq.com/cgi-bin/material/add_material"
        f"?access_token={token}&type=image"
    )
    with img_path.open("rb") as media_file:
        data = request_wechat("POST", url, files={"media": media_file})
    media_id = data.get("media_id")
    if not media_id:
        raise RuntimeError(f"Upload thumb response missing media_id: {data}")
    return media_id


def upload_content_image(token: str, img_path: Path) -> str:
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    with img_path.open("rb") as media_file:
        data = request_wechat("POST", url, files={"media": media_file})
    img_url = data.get("url")
    if not img_url:
        raise RuntimeError(f"Upload content image response missing url: {data}")
    return img_url


def read_text_auto(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Cannot decode markdown file: {path}")


def decode_unicode_escapes_if_needed(text: str) -> str:
    if len(re.findall(r"\\u[0-9a-fA-F]{4}", text)) < 3:
        return text
    try:
        decoded = codecs.decode(text, "unicode_escape")
    except Exception:
        return text
    return decoded if decoded else text


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        match = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def extract_urls(markdown_text: str) -> list[str]:
    urls = re.findall(r"https?://[^\s<>)]+", markdown_text)
    unique_urls = []
    seen = set()
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    return unique_urls


def append_reference_links(markdown_text: str, urls: list[str]) -> str:
    if not urls:
        return markdown_text
    if (
        "## 参考链接" in markdown_text
        or "## 附录链接" in markdown_text
        or "## References" in markdown_text
    ):
        return markdown_text
    block = "\n".join(f"- {url}" for url in urls)
    return f"{markdown_text.rstrip()}\n\n## References\n{block}\n"


def _inline_format(text: str) -> str:
    raw = text.strip()
    raw = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r"\1（\2）", raw)
    escaped = html.escape(raw)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def markdown_to_html(markdown_text: str, token: str, md_path: Path, upload_images: bool = True) -> str:
    lines = markdown_text.splitlines()
    out = []
    in_code = False
    para_buf = []
    ol_index = 0
    in_ol = False
    in_summary_box = False
    current_event_open = False

    def flush_para() -> None:
        nonlocal para_buf
        if para_buf:
            joined = " ".join(x.strip() for x in para_buf if x.strip())
            if joined:
                style = 'margin:0 0 16px;line-height:1.95;color:#1f2329;font-size:16px;text-align:justify;'
                if joined.startswith('本期摘要') or in_summary_box:
                    style = 'margin:0 0 12px;line-height:1.9;color:#243447;font-size:15px;text-align:justify;'
                out.append(f'<p style="{style}">{_inline_format(joined)}</p>')
        para_buf = []

    def close_lists() -> None:
        nonlocal in_ol, ol_index
        in_ol = False
        ol_index = 0

    def close_event_card() -> None:
        nonlocal current_event_open
        if current_event_open:
            out.append('</section>')
            current_event_open = False

    for raw in lines:
        line = raw.rstrip()

        if line.strip().startswith("```"):
            flush_para()
            close_lists()
            if not in_code:
                out.append('<pre style="background:#f6f8fa;padding:14px 16px;border-radius:10px;overflow:auto;margin:18px 0;"><code>')
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            continue

        if in_code:
            out.append(html.escape(line))
            continue

        if not line.strip():
            flush_para()
            close_lists()
            continue

        img_match = re.match(r'^\s*!\[(.*?)\]\((.+?)\)\s*$', line)
        if img_match:
            flush_para()
            close_lists()
            alt_text = img_match.group(1).strip()
            img_src = img_match.group(2).strip()
            local_img = (md_path.parent / img_src).resolve()
            if upload_images and local_img.exists():
                remote_url = upload_content_image(token, local_img)
                out.append(
                    f'<p style="margin:22px 0;"><img src="{html.escape(remote_url)}" alt="{html.escape(alt_text)}" style="max-width:100%;height:auto;border-radius:10px;box-shadow:0 6px 18px rgba(15,35,65,.10);" /></p>'
                )
            else:
                out.append(f'<p style="margin:0 0 14px;color:#667085;font-size:14px;">[图片: {html.escape(img_src)}]</p>')
            continue

        heading = re.match(r"^\s*(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            flush_para()
            close_lists()
            level = len(heading.group(1))
            content_raw = heading.group(2).strip()
            content = _inline_format(content_raw)

            if level == 1:
                close_event_card()
                out.append(f'<h1 style="font-size:28px;line-height:1.35;margin:8px 0 18px;font-weight:800;color:#0b2545;letter-spacing:.2px;">{content}</h1>')
            elif level == 2:
                close_event_card()
                if '本期摘要' in content_raw:
                    in_summary_box = True
                    out.append('<section style="margin:22px 0 28px;padding:16px 18px;border-radius:12px;background:linear-gradient(180deg,#f5f9ff 0%,#eef6ff 100%);border:1px solid #d9e8ff;">')
                    out.append(f'<h2 style="font-size:20px;line-height:1.4;margin:0 0 12px;font-weight:800;color:#123b6d;">{content}</h2>')
                else:
                    if in_summary_box:
                        out.append('</section>')
                        in_summary_box = False
                    out.append(f'<h2 style="font-size:21px;line-height:1.4;margin:30px 0 14px;font-weight:800;color:#123b6d;border-left:4px solid #2f6fed;padding-left:10px;">{content}</h2>')
            elif level == 3:
                if in_summary_box:
                    out.append('</section>')
                    in_summary_box = False
                close_event_card()
                current_event_open = True
                out.append('<section style="margin:18px 0 24px;padding:18px 16px 16px;border:1px solid #e8edf5;border-radius:14px;background:#ffffff;box-shadow:0 3px 12px rgba(15,23,42,.035);">')
                out.append(f'<h3 style="font-size:18px;line-height:1.55;margin:0 0 12px;font-weight:800;color:#0f172a;">{content}</h3>')
            else:
                out.append(f'<h{min(level + 1, 6)} style="line-height:1.5;margin:18px 0 10px;font-weight:700;color:#7a4d00;">{content}</h{min(level + 1, 6)}>')
            continue

        meta_match = re.match(r'^\s*-\s*(分类|领域标签|时间|涉及主体)：\s*(.+?)\s*$', line)
        if meta_match:
            flush_para()
            label = meta_match.group(1)
            value = meta_match.group(2)
            out.append(
                f'<p style="margin:0 0 6px;font-size:13px;line-height:1.7;color:#7b8794;">'
                f'<span style="display:inline-block;min-width:68px;color:#526071;font-weight:700;">{html.escape(label)}：</span>'
                f'<span>{_inline_format(value)}</span></p>'
            )
            continue

        impact_match = re.match(r'^\s*-\s*(内容摘要|关注点 / 影响|来源链接)：\s*(.+?)\s*$', line)
        if impact_match:
            flush_para()
            label = impact_match.group(1)
            value = impact_match.group(2)
            if label == '内容摘要':
                out.append(
                    f'<p style="margin:8px 0 14px;line-height:1.95;color:#1f2937;font-size:16px;text-align:justify;">'
                    f'<span style="display:block;margin-bottom:4px;font-weight:800;color:#0b2545;">内容摘要</span>{_inline_format(value)}</p>'
                )
            elif label == '关注点 / 影响':
                out.append(
                    f'<div style="margin:14px 0 10px;padding:12px 14px;border-radius:10px;background:#f8fbff;border-left:4px solid #2f6fed;">'
                    f'<p style="margin:0;line-height:1.9;color:#243447;font-size:15px;text-align:justify;">'
                    f'<span style="display:block;margin-bottom:4px;font-weight:800;color:#123b6d;">关注点 / 影响</span>{_inline_format(value)}</p></div>'
                )
            else:
                out.append(
                    f'<p style="margin:10px 0 0;font-size:12px;line-height:1.7;color:#98a2b3;word-break:break-all;">'
                    f'<span style="font-weight:700;color:#667085;">来源链接：</span>{_inline_format(value)}</p>'
                )
            continue

        ul_match = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if ul_match:
            flush_para()
            close_lists()
            out.append(f'<p style="margin:0 0 10px;line-height:1.85;padding-left:1.2em;text-indent:-0.9em;color:#243447;">• {_inline_format(ul_match.group(1))}</p>')
            continue

        ol_match = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
        if ol_match:
            flush_para()
            if not in_ol:
                in_ol = True
                ol_index = 0
            ol_index += 1
            out.append(f'<p style="margin:0 0 10px;line-height:1.85;padding-left:1.4em;text-indent:-1.1em;color:#243447;">{ol_index}. {_inline_format(ol_match.group(1))}</p>')
            continue

        para_buf.append(line)

    flush_para()
    close_event_card()
    if in_summary_box:
        out.append('</section>')
    if in_code:
        out.append("</code></pre>")
    body = "\n".join(out)
    return (
        '<section style="font-size:16px;color:#1f2329;line-height:1.9;word-break:break-word;background:#ffffff;">'
        f"{body}</section>"
    )


def create_draft(
    token: str,
    title: str,
    content_html: str,
    thumb_media_id: str,
    author: str,
    digest: str,
    content_source_url: str,
    show_cover_pic: int,
) -> str:
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content_html,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
                "show_cover_pic": show_cover_pic,
            }
        ]
    }
    data = request_wechat_json_utf8("POST", url, payload)
    media_id = data.get("media_id")
    if not media_id:
        raise RuntimeError(f"Draft response missing media_id: {data}")
    return media_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload local Markdown to WeChat MP draft box (no publishing).")
    parser.add_argument("--md", required=True, help="Path to markdown file")
    parser.add_argument(
        "--thumb",
        default=r"D:\\Spark\\openclaw\\cover.jpeg",
        help="Path to cover image (default: D:\\Spark\\openclaw\\cover.jpeg)",
    )
    parser.add_argument("--title", default="", help="Override article title")
    parser.add_argument("--author", default="Space AI Weekly", help="Article author")
    parser.add_argument("--digest", default="", help="Article digest/summary")
    parser.add_argument("--source-url", default="", help="Original source URL")
    parser.add_argument("--show-cover-pic", type=int, choices=[0, 1], default=1)
    parser.add_argument("--appid", default=os.getenv("WECHAT_APPID", ""))
    parser.add_argument("--secret", default=os.getenv("WECHAT_SECRET", ""))
    parser.add_argument("--no-upload-images", action="store_true")
    parser.add_argument("--no-reference-links", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    md_path = Path(args.md).resolve()
    thumb_path = Path(args.thumb).resolve()

    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")
    if not thumb_path.exists():
        raise FileNotFoundError(f"Cover image not found: {thumb_path}")
    if not args.appid or not args.secret:
        raise RuntimeError("Missing appid/secret. Use --appid --secret or env vars.")

    md_text = read_text_auto(md_path)
    md_text = decode_unicode_escapes_if_needed(md_text)
    urls_in_doc = extract_urls(md_text)
    if not args.no_reference_links:
        md_text = append_reference_links(md_text, urls_in_doc)

    title = args.title.strip() or extract_title(md_text, md_path.stem)
    source_url = args.source_url.strip()

    token = get_access_token(args.appid, args.secret)
    thumb_media_id = upload_thumb_material(token, thumb_path)
    content_html = markdown_to_html(
        md_text, token, md_path, upload_images=(not args.no_upload_images)
    )
    draft_media_id = create_draft(
        token=token,
        title=title,
        content_html=content_html,
        thumb_media_id=thumb_media_id,
        author=args.author,
        digest=args.digest,
        content_source_url=source_url,
        show_cover_pic=args.show_cover_pic,
    )

    print("Draft created successfully.")
    print(f"Title: {title}")
    print(f"Draft media_id: {draft_media_id}")
    if source_url:
        print(f"Read-original URL: {source_url}")
    print("This script does NOT publish articles.")


if __name__ == "__main__":
    main()
