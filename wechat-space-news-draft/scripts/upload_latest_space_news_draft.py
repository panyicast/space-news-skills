import argparse
import re
from pathlib import Path
import subprocess


def version_key(path: Path):
    name = path.name
    match = re.search(r"-v(\d+)\.md$", name, re.I)
    if match:
        return (1, int(match.group(1)))
    return (0, 0)


def find_latest_markdown(directory: Path, pattern: str) -> Path:
    files = sorted(directory.glob(pattern), key=version_key, reverse=True)
    if not files:
        raise FileNotFoundError(f"No files matched {pattern} in {directory}")
    return files[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find the latest space-news monthly/weekly markdown file and upload it as a WeChat draft."
    )
    parser.add_argument(
        "--dir",
        default=r"D:\Spark\openclaw",
        help="Directory containing generated space-news markdown files",
    )
    parser.add_argument(
        "--kind",
        choices=["monthly", "weekly"],
        default="monthly",
        help="Whether to pick the latest monthly or weekly report",
    )
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
    base_dir = Path(args.dir).resolve()
    if not base_dir.exists():
        raise FileNotFoundError(f"Directory not found: {base_dir}")

    if args.kind == "monthly":
        pattern = "space-news-monthly-*.md"
    else:
        pattern = "space-news-weekly-*.md"

    md_path = find_latest_markdown(base_dir, pattern)
    wrapper = Path(__file__).resolve().parent / "upload_space_news_monthly_draft.py"

    import sys

    command = [
        sys.executable,
        str(wrapper),
        "--md",
        str(md_path),
        "--thumb",
        str(Path(args.thumb).resolve()),
        "--author",
        args.author,
        "--show-cover-pic",
        str(args.show_cover_pic),
    ]
    if args.source_url.strip():
        command.extend(["--source-url", args.source_url.strip()])
    if args.title.strip():
        command.extend(["--title", args.title.strip()])
    if args.digest.strip():
        command.extend(["--digest", args.digest.strip()])
    if args.no_upload_images:
        command.append("--no-upload-images")
    if args.no_reference_links:
        command.append("--no-reference-links")

    print(f"Using markdown: {md_path}")
    result = subprocess.run(command, check=False)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
