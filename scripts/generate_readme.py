from datetime import datetime, timedelta, timezone
from pathlib import Path
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
    title = folder_name.replace("_", " ").title()
    replacements = {
        " Ii": " II",
        " Iii": " III",
        " Iv": " IV",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


problems = []
counts = {difficulty: 0 for difficulty in DIFFICULTIES}

for difficulty in DIFFICULTIES:
    base = ROOT / difficulty
    if not base.exists():
        continue

    folders = sorted(path for path in base.iterdir() if path.is_dir())
    counts[difficulty] = len(folders)

    for folder in folders:
        slug = folder.name.replace("_", "-")
        problems.append(
            {
                "title": display_title(folder.name),
                "slug": slug,
                "difficulty": difficulty,
                "path": folder.as_posix(),
                "solved": solved_date(folder),
            }
        )

total = sum(counts.values())

lines = [
    "# LeetCode",
    "",
    "My algorithm and data structures practice from [LeetCode](https://leetcode.com). Every solution here was written by hand.",
    "",
    f"**{total}** solved · {counts['easy']} easy · {counts['medium']} medium · {counts['hard']} hard",
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
