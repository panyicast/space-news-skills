import argparse
import re
from pathlib import Path

from upload_wechat_draft import extract_title, read_text_auto


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "").replace("\u3000", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def infer_digest(markdown_text: str, fallback: str = "航天 AI 情报简报") -> str:
    lines = [clean_text(line) for line in markdown_text.splitlines() if clean_text(line)]
    for idx, line in enumerate(lines):
        if line in {"## 本期摘要", "# 本期摘要"}:
            collected = []
            for follow in lines[idx + 1 : idx + 10]:
                if follow.startswith("#"):
                    break
                follow = re.sub(r"^[-*]\s+", "", follow).strip()
                if follow:
                    collected.append(follow)
                if len(" ".join(collected)) >= 90:
                    break
            if collected:
                return clean_text(" ".join(collected))[:120]
    for line in lines[:12]:
        if line.startswith("- ") or re.match(r"^\d+\.", line):
            return clean_text(re.sub(r"^[-*]\s+", "", line))[:120]
    return fallback


def infer_title(markdown_text: str, md_path: Path) -> str:
    title = clean_text(extract_title(markdown_text, md_path.stem))
    title = title.replace("：AI 相关月度动态", "")
    return title


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Helper wrapper for uploading a space-news monthly/weekly Markdown file to WeChat draft box."
    )
    parser.add_argument("--md", required=True, help="Path to monthly/weekly markdown file")
    parser.add_argument(
        "--thumb",
        default=r"D:\\Spark\\openclaw\\cover.jpeg",
        help="Path to cover image (default: D:\\Spark\\openclaw\\cover.jpeg)",
    )
    parser.add_argument("--author", default="Space AI Weekly", help="Article author")
    parser.add_argument("--source-url", default="", help="Override source URL")
    parser.add_argument("--show-cover-pic", type=int, choices=[0, 1], default=1)
    parser.add_argument("--no-upload-images", action="store_true")
    parser.add_argument("--no-reference-links", action="store_true")
    parser.add_argument("--title", default="", help="Override article title")
    parser.add_argument("--digest", default="", help="Override article digest")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    md_path = Path(args.md).resolve()
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    markdown_text = read_text_auto(md_path)
    title = args.title.strip() or infer_title(markdown_text, md_path)
    digest = args.digest.strip() or infer_digest(markdown_text)

    script_path = Path(__file__).resolve().parent / "upload_wechat_draft.py"
    import sys

    command = [
        sys.executable,
        str(script_path),
        "--md",
        str(md_path),
        "--thumb",
        str(Path(args.thumb).resolve()),
        "--author",
        args.author,
        "--title",
        title,
        "--digest",
        digest,
        "--show-cover-pic",
        str(args.show_cover_pic),
    ]
    if args.source_url.strip():
        command.extend(["--source-url", args.source_url.strip()])
    if args.no_upload_images:
        command.append("--no-upload-images")
    if args.no_reference_links:
        command.append("--no-reference-links")

    import subprocess

    result = subprocess.run(command, check=False)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
