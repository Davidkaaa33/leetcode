from datetime import datetime, timedelta, timezone
from pathlib import Path
import html
import subprocess

ROOT = Path("problems")
DIFFICULTIES = ("easy", "medium", "hard")
MSK = timezone(timedelta(hours=3))


def solved_date(path: Path) -> str:
    try:
        output = subprocess.check_output(
            ["git", "log", "--reverse", "--format=%cs", "--", str(path)],
            text=True,
        ).strip()
        if output:
            return output.splitlines()[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return datetime.now(MSK).date().isoformat()


def display_title(folder_name: str) -> str:
    words = folder_name.replace("_", " ").split()
    roman = {"ii": "II", "iii": "III", "iv": "IV", "vi": "VI"}
    return " ".join(roman.get(word.lower(), word.capitalize()) for word in words)


def collect_problems():
    problems = []
    counts = {difficulty: 0 for difficulty in DIFFICULTIES}

    for difficulty in DIFFICULTIES:
        base = ROOT / difficulty
        if not base.exists():
            continue

        folders = sorted(path for path in base.iterdir() if path.is_dir())
        counts[difficulty] = len(folders)

        for folder in folders:
            problems.append(
                {
                    "title": display_title(folder.name),
                    "slug": folder.name.replace("_", "-"),
                    "difficulty": difficulty,
                    "path": folder.as_posix(),
                    "solved": solved_date(folder),
                }
            )

    return problems, counts


def generate_coverage_svg(counts):
    total = sum(counts.values())
    easy = counts["easy"]
    medium = counts["medium"]
    hard = counts["hard"]

    width = 920
    height = 180
    bar_x = 40
    bar_y = 125
    bar_w = 840
    bar_h = 14

    def segment_width(value):
        return 0 if total == 0 else round(bar_w * value / total, 2)

    easy_w = segment_width(easy)
    medium_w = segment_width(medium)
    hard_w = segment_width(hard)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="LeetCode progress: {total} solved">
<style>
  .bg {{ fill: #ffffff; }}
  .border {{ fill: none; stroke: #d0d7de; }}
  .title {{ fill: #1f2328; font: 600 18px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; }}
  .label {{ fill: #656d76; font: 13px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; }}
  .value {{ fill: #1f2328; font: 600 24px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; }}
  .track {{ fill: #eaeef2; }}
  .easy {{ fill: #2da44e; }}
  .medium {{ fill: #bf8700; }}
  .hard {{ fill: #cf222e; }}
  @media (prefers-color-scheme: dark) {{
    .bg {{ fill: #0d1117; }}
    .border {{ stroke: #30363d; }}
    .title, .value {{ fill: #f0f6fc; }}
    .label {{ fill: #8b949e; }}
    .track {{ fill: #21262d; }}
  }}
</style>
<rect class="bg" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="10"/>
<rect class="border" x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="10"/>
<text class="title" x="40" y="34">LeetCode progress</text>

<text class="label" x="40" y="64">Solved</text>
<text class="value" x="40" y="92">{total}</text>

<text class="label" x="230" y="64">Easy</text>
<text class="value" x="230" y="92">{easy}</text>

<text class="label" x="420" y="64">Medium</text>
<text class="value" x="420" y="92">{medium}</text>

<text class="label" x="610" y="64">Hard</text>
<text class="value" x="610" y="92">{hard}</text>

<rect class="track" x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7"/>
<rect class="easy" x="{bar_x}" y="{bar_y}" width="{easy_w}" height="{bar_h}" rx="7"/>
<rect class="medium" x="{bar_x + easy_w}" y="{bar_y}" width="{medium_w}" height="{bar_h}"/>
<rect class="hard" x="{bar_x + easy_w + medium_w}" y="{bar_y}" width="{hard_w}" height="{bar_h}" rx="7"/>
<text class="label" x="40" y="158">Easy / Medium / Hard distribution across solved problems</text>
</svg>
"""
    Path("coverage.svg").write_text(svg, encoding="utf-8")


def generate_readme(problems, counts):
    total = sum(counts.values())

    lines = [
        "# LeetCode",
        "",
        "My algorithms and data structures practice from [LeetCode](https://leetcode.com). Every solution here was written by hand.",
        "",
        f"**{total}** solved · {counts['easy']} easy · {counts['medium']} medium · {counts['hard']} hard",
        "",
        "![Coverage](./coverage.svg)",
        "",
        "## Problems",
        "",
        "| | Difficulty | Solved | |",
        "| --- | --- | --- | --- |",
    ]

    for problem in problems:
        lines.append(
            f"| [{problem['title']}](https://leetcode.com/problems/{problem['slug']}/) "
            f"| {problem['difficulty']} | {problem['solved']} "
            f"| [solution]({problem['path']}) |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "_This file is regenerated automatically after every LeetCode sync._",
            "",
        ]
    )

    Path("README.md").write_text("\n".join(lines), encoding="utf-8")


problems, counts = collect_problems()
generate_coverage_svg(counts)
generate_readme(problems, counts)
