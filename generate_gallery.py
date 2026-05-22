import argparse
import html
import os
from pathlib import Path


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def find_images(root: Path):
    groups = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        rel_path = path.relative_to(root)
        group = str(rel_path.parent)
        groups.setdefault(group, []).append(rel_path)
    return groups


def build_html(root: Path, title: str):
    groups = find_images(root)
    sections = []

    for group, images in groups.items():
        cards = []
        for rel_path in images:
            rel_str = rel_path.as_posix()
            label = html.escape(rel_path.name)
            cards.append(
                f"""
                <a class="card" href="{html.escape(rel_str)}" target="_blank">
                  <img src="{html.escape(rel_str)}" alt="{label}" loading="lazy">
                  <div class="caption">{label}</div>
                </a>
                """
            )

        group_title = html.escape(group if group != "." else "root")
        sections.append(
            f"""
            <section class="group">
              <h2>{group_title}</h2>
              <div class="grid">
                {''.join(cards)}
              </div>
            </section>
            """
        )

    body = "".join(sections) if sections else "<p>No images found.</p>"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f6f3ee;
      --panel: #fffdf9;
      --text: #1e1b18;
      --muted: #6b6259;
      --line: #d7cec2;
      --accent: #9a3412;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background:
        radial-gradient(circle at top left, #fff7ed 0, transparent 28%),
        linear-gradient(180deg, #f8f5ef 0%, var(--bg) 100%);
      color: var(--text);
    }}
    .page {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 40px 24px 80px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(32px, 4vw, 56px);
      line-height: 1;
      letter-spacing: -0.03em;
    }}
    .intro {{
      margin: 0 0 28px;
      color: var(--muted);
      font-size: 18px;
    }}
    .group {{
      margin-top: 34px;
      padding-top: 18px;
      border-top: 2px solid var(--line);
    }}
    h2 {{
      margin: 0 0 18px;
      font-size: 24px;
      color: var(--accent);
      word-break: break-word;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 18px;
    }}
    .card {{
      display: block;
      text-decoration: none;
      color: inherit;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 12px 30px rgba(62, 39, 23, 0.08);
      transition: transform 180ms ease, box-shadow 180ms ease;
    }}
    .card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 18px 40px rgba(62, 39, 23, 0.14);
    }}
    img {{
      display: block;
      width: 100%;
      height: 220px;
      object-fit: contain;
      background: #fff;
      padding: 10px;
    }}
    .caption {{
      padding: 12px 14px 14px;
      border-top: 1px solid var(--line);
      font-size: 14px;
      color: var(--muted);
      word-break: break-word;
    }}
  </style>
</head>
<body>
  <main class="page">
    <h1>{html.escape(title)}</h1>
    <p class="intro">Auto-generated image gallery grouped by subfolder.</p>
    {body}
  </main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate a static HTML image gallery for a folder tree."
    )
    parser.add_argument("root", help="Folder containing images and subfolders")
    parser.add_argument(
        "--title",
        default="Figure Gallery",
        help="Page title for the generated gallery",
    )
    parser.add_argument(
        "--output",
        default="index.html",
        help="Output HTML file path",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Input folder does not exist or is not a directory: {root}")

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(root, args.title), encoding="utf-8")

    print(f"Gallery written to: {output}")
    print(f"Image root: {root}")


if __name__ == "__main__":
    main()
