# SPDX-License-Identifier: MIT
"""Build the GitHub Pages site with Python's standard library only."""
from pathlib import Path
import html
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"


def inline(value):
    value = html.escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*(.+?)\*", r"<em>\1</em>", value)
    return value


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name in ("emblem.svg", "cosmos.svg", "candles.svg"):
        shutil.copyfile(ROOT / "art" / name, ASSETS / name)
    for source, name in (("poster.jpg", "painted-poster.jpg"), ("narration.vtt", "painted-narration.vtt")):
        shutil.copyfile(ROOT / "art" / "film" / "painted" / source, ASSETS / name)
    story = (ROOT / "founding-story" / "README.md").read_text(encoding="utf-8")
    narrative = story.split("Before there were stars", 1)[1].split("## Reading the story", 1)[0]
    narrative = "Before there were stars" + narrative
    story_html = "\n".join("<p>" + inline(p.strip()) + "</p>" for p in narrative.strip().split("\n\n"))
    faq = (ROOT / "faq" / "README.md").read_text(encoding="utf-8")
    faq_html = []
    for section in re.split(r"(?m)^## ", faq)[1:]:
        heading, rest = section.split("\n", 1)
        faq_html.append('<h3 class="faq-group-label">' + html.escape(heading) + "</h3>")
        for entry in re.split(r"(?m)^### ", rest)[1:]:
            question, answer = entry.split("\n", 1)
            answer = answer.strip().split("\n\nRead the [", 1)[0]
            faq_html.append("<details><summary>" + html.escape(question) + "</summary><p>" + inline(answer) + "</p></details>")
    template = (ROOT / "website" / "index.template.html").read_text(encoding="utf-8")
    result = template.replace("{{STORY}}", story_html).replace("{{FAQ}}", "\n".join(faq_html))
    assert "{{" not in result, "Unresolved template content"
    assert result.count("<details>") == 12, "Expected 12 FAQ questions"
    (DOCS / "index.html").write_text(result, encoding="utf-8")
    (DOCS / ".nojekyll").touch()
    print("Built docs/index.html, 12 FAQ answers, and local artwork and captions.")


if __name__ == "__main__":
    main()
