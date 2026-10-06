from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import subprocess

import requests

ROOT = Path("problems")
DIFFICULTIES = ("easy", "medium", "hard")
MSK = timezone(timedelta(hours=3))
GRAPHQL_URL = "https://leetcode.com/graphql/"
FALLBACK_TOTALS = {"easy": 966, "medium": 2117, "hard": 977}


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


def fetch_problem_totals(solved_counts):
    query = """
    query problemCounts {
      allQuestionsCount {
        difficulty
        count
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/problemset/",
        "User-Agent": "Mozilla/5.0",
    }

    session = os.getenv("LEETCODE_SESSION")
    csrf = os.getenv("CSRFTOKEN")
    if session and csrf:
        headers["Cookie"] = f"LEETCODE_SESSION={session}; csrftoken={csrf}"
        headers["x-csrftoken"] = csrf

    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query},
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
        items = response.json()["data"]["allQuestionsCount"]

        totals = {}
        for item in items:
            difficulty = item["difficulty"].lower()
            if difficulty in DIFFICULTIES:
                totals[difficulty] = int(item["count"])

        if all(totals.get(d, 0) >= solved_counts[d] for d in DIFFICULTIES):
            return totals
    except Exception as exc:
        print(f"Could not refresh LeetCode totals: {exc}")

    return {
        difficulty: max(FALLBACK_TOTALS[difficulty], solved_counts[difficulty])
        for difficulty in DIFFICULTIES
    }


def generate_coverage_svg(solved_counts, totals):
    width = 880
    left = 20
    right = 860
    cell = 5
    gap = 2
    pitch = cell + gap
    columns = 118
    section_gap = 18
    label_to_grid = 8
    top = 24

    labels = {
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
    }
    classes = {
        "easy": "e",
        "medium": "m",
        "hard": "h",
    }

    section_data = []
    cursor = top

    for difficulty in DIFFICULTIES:
        total = totals[difficulty]
        rows = max(1, (total + columns - 1) // columns)
        label_y = cursor
        grid_y = label_y + label_to_grid
        section_data.append((difficulty, total, rows, label_y, grid_y))
        cursor = grid_y + rows * pitch + section_gap

    footer_y = cursor + 2
    height = footer_y + 24
    solved_total = sum(solved_counts.values())
    problem_total = sum(totals.values())

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="LeetCode coverage: {solved_total} of {problem_total} problems solved">',
        """<style>
  .bg{fill:#0d1117}.tx{fill:#e6edf3}.dim{fill:#7d8590}.none{fill:#21262d}
  .e{fill:#3fb950}.m{fill:#d29922}.h{fill:#f85149}
</style>""",
        f'<rect width="{width}" height="{height}" class="bg"/>',
    ]

    for difficulty, total, rows, label_y, grid_y in section_data:
        solved = solved_counts[difficulty]
        parts.append(
            f'<text x="{left}" y="{label_y}" class="tx" font-size="11" '
            f'font-family="ui-monospace,monospace">{labels[difficulty]}</text>'
        )
        parts.append(
            f'<text x="{right}" y="{label_y}" class="dim" font-size="11" '
            f'text-anchor="end" font-family="ui-monospace,monospace">{solved}/{total}</text>'
        )

        for index in range(total):
            row = index // columns
            col = index % columns
            x = left + col * pitch
            y = grid_y + row * pitch
            css_class = classes[difficulty] if index < solved else "none"
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'rx="1.25" class="{css_class}"/>'
            )

    parts.append(
        f'<text x="{left}" y="{footer_y}" class="dim" font-size="11" '
        f'font-family="ui-monospace,monospace">{solved_total} of {problem_total} problems solved on LeetCode</text>'
    )
    parts.append("</svg>")

    Path("coverage.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


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
        "_Synced nightly at 00:00 MSK via GitHub Actions. Progress and this grid regenerate automatically._",
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


problems, solved_counts = collect_problems()
totals = fetch_problem_totals(solved_counts)
generate_coverage_svg(solved_counts, totals)
generate_readme(problems, solved_counts)
