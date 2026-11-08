"""Builds the two SVGs in this folder. Standard library only, deterministic.

    python3 docs/img/make.py

score-by-run.svg is read from results.tsv (all 215 rows; tab separated, with a header;
`composite` is the score, `eval_ver` the eval version). loop.svg is a fixed diagram.

Every shape is a filled rect, circle or polygon and every label is a plain <text>, so the files
render the same in a browser and in ImageMagick's built-in SVG reader.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

NAVY = "#001B3B"
SAND = "#EDE7DC"
TERRA = "#8C5348"
OLIVE = "#59591D"
HEAD = "#F2EDE2"
SECOND = "#D8D3CA"
SERIF = "Georgia, 'Playfair Display', serif"
SANS = "-apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif"
EM_DASH = chr(0x2014)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def n(v):
    v = round(v, 1)
    return str(int(v)) if v == int(v) else str(v)


def rect(x, y, w, h, fill, extra=""):
    tail = f" {extra}" if extra else ""
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="{fill}"{tail}/>'


def circle(cx, cy, r, fill):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"/>'


def text(x, y, s, size=16, family=SANS, fill=SECOND, weight=None, anchor=None):
    attrs = [f'x="{n(x)}"', f'y="{n(y)}"', f'font-family="{family}"', f'font-size="{size}"',
             f'fill="{fill}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    return f"<text {' '.join(attrs)}>{esc(s)}</text>"


def frame(x, y, w, h, outer, inner):
    """A 1px border drawn as two filled rects, so no renderer has to draw a stroke."""
    return rect(x, y, w, h, outer) + rect(x + 1, y + 1, w - 2, h - 2, inner)


def arrow_right(x1, x2, y, color=TERRA):
    head = 14
    return (rect(x1, y - 2, x2 - x1 - head + 1, 4, color)
            + f'<polygon points="{n(x2 - head)},{n(y - 9)} {n(x2)},{n(y)} {n(x2 - head)},{n(y + 9)}" fill="{color}"/>')


def svg(w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">\n'
            f'<title id="t">{esc(title)}</title>\n<desc id="d">{esc(desc)}</desc>\n'
            + "\n".join(body) + "\n</svg>\n")


def write(name, content):
    if EM_DASH in content:
        raise SystemExit(f"{name}: em dash in output")
    (HERE / name).write_text(content, encoding="utf-8")
    print(f"wrote docs/img/{name} ({len(content)} bytes)")


def score_by_run(tsv):
    with open(tsv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 215:
        raise SystemExit(f"expected 215 runs in {tsv.name}, found {len(rows)}")
    runs = [(i, float(r["composite"]), r["eval_ver"]) for i, r in enumerate(rows, 1)]

    best = 0.0
    best_run = 0
    for i, score, _ in runs:
        if score > best:
            best, best_run = score, i

    counts = {v: sum(1 for _, _, e in runs if e == v) for v in ("v2", "v3", "v4")}
    colors = {"v2": SAND, "v3": TERRA, "v4": OLIVE}
    v4_max = max(s for _, s, e in runs if e == "v4")

    W, H = 1200, 520
    left, right, top, bottom = 110, 1140, 150, 420

    def px(i):
        return left + (i - 1) / (len(runs) - 1) * (right - left)

    def py(score):
        return bottom - score / 100 * (bottom - top)

    body = [frame(0, 0, W, H, SAND, NAVY)]
    body.append(text(60, 62, "Score by run. 215 runs, March 20 to 28, 2026.", size=32,
                     family=SERIF, fill=HEAD))
    body.append(text(60, 94, "One knob per run, keep or revert. Each point is one run, colored by "
                     "eval version.", size=16))
    body.append(text(left, top - 18, "Composite score", size=14))
    for g in (0, 20, 40, 60, 80, 100):
        y = py(g)
        if g:
            body.append(rect(left, y - 0.5, right - left, 1, SAND, 'fill-opacity="0.16"'))
        body.append(text(left - 12, y + 5, str(g), size=14, anchor="end"))
    body.append(rect(left, bottom - 0.5, right - left, 1.5, SAND, 'fill-opacity="0.6"'))
    for t in (1, 50, 100, 150, 200, 215):
        x = px(t)
        body.append(rect(x - 0.5, bottom + 1, 1, 6, SAND, 'fill-opacity="0.6"'))
        body.append(text(x, bottom + 26, str(t), size=14, anchor="middle"))
    body.append(text((left + right) / 2, bottom + 50, "Run number", size=14, anchor="middle"))

    # The best kept score: the bar every later run had to beat.
    yb = py(best)
    body.append(rect(left, yb - 1, right - left, 2, HEAD, 'fill-opacity="0.85"'))
    body.append(text(right, yb - 10, f"Best kept score: {best:.2f}, run {best_run}", size=15,
                     fill=HEAD, anchor="end"))

    # Run 9, the one-line system prompt: ring and leader behind the points.
    r9 = runs[8]
    x9, y9 = px(r9[0]), py(r9[1])
    body.append(rect(x9 - 1, top + 24, 2, y9 - top - 34, HEAD))
    body.append(circle(x9, y9, 10, HEAD))
    body.append(circle(x9, y9, 8, NAVY))
    body.append(text(x9 - 4, top + 16, "Run 9: system prompt cut to one line, quality 73 to 100",
                     size=16, fill=HEAD, weight=700))

    # A faint sand ring under each point keeps the darker accents legible on navy.
    for i, score, ver in runs:
        body.append(f'<circle cx="{n(px(i))}" cy="{n(py(score))}" r="5.8" fill="{SAND}" fill-opacity="0.45"/>')
        body.append(circle(px(i), py(score), 4.5, colors[ver]))

    legend = [
        ("v2", f"eval v2, {counts['v2']} run"),
        ("v3", f"eval v3, {counts['v3']} runs, Qwen 3.5 27B"),
        ("v4", f"eval v4, {counts['v4']} runs, Opus-distilled model, never above {v4_max:.2f}"),
    ]
    lx = left
    for ver, label in legend:
        body.append(f'<circle cx="{n(lx + 6)}" cy="496" r="7.3" fill="{SAND}" fill-opacity="0.45"/>')
        body.append(circle(lx + 6, 496, 6, colors[ver]))
        body.append(text(lx + 18, 501, label, size=14))
        lx += 18 + len(label) * 7.4 + 34

    desc = (f"Composite score for each of the {len(runs)} runs, colored by eval version: run 9 "
            f"cut the system prompt to one line and took quality from 73 to 100, the best kept "
            f"score is {best:.2f} from run {best_run}, and no eval v4 run scored above "
            f"{v4_max:.2f}.")
    return svg(W, H, "Score by run. 215 runs, March 20 to 28, 2026.", desc, body)


def loop():
    W, H = 1200, 400
    steps = [
        ("Edit", ["The agent changes", "one knob in", "config.py"]),
        ("Commit", ["git commit", "before the", "eval runs"]),
        ("Eval", ["evaluate.py, locked", "10 prompts, shuffled,", "5-minute budget"]),
        ("Keep or revert", ["Above the best", "kept score? Keep.", "If not, revert."]),
        ("Log", ["One row in", "results.tsv", "for every run"]),
    ]
    body = [frame(0, 0, W, H, SAND, NAVY)]
    body.append(text(40, 62, "The loop", size=34, family=SERIF, fill=HEAD))
    body.append(text(40, 94, "program.md tells the agent what to do. Nobody edits evaluate.py "
                     "or run.py.", size=16))
    gap, bx, by, bh = 44, 40, 124, 196
    bw = (W - 80 - gap * 4) / 5
    for i, (head, lines) in enumerate(steps):
        x = bx + i * (bw + gap)
        body.append(frame(x, by, bw, bh, SAND, NAVY))
        body.append(text(x + 20, by + 36, str(i + 1), size=16))
        body.append(text(x + 20, by + 74, head, size=24 if len(head) > 8 else 28, family=SERIF,
                         fill=HEAD))
        for j, line in enumerate(lines):
            body.append(text(x + 20, by + 110 + j * 24, line, size=16))
        if i < len(steps) - 1:
            body.append(arrow_right(x + bw + 6, x + bw + gap - 6, by + bh / 2))
    # The return path: from the last box back to the first, under the row.
    first_c = bx + bw / 2
    last_c = bx + 4 * (bw + gap) + bw / 2
    ry = by + bh + 44
    body.append(rect(last_c - 2, by + bh, 4, ry - by - bh + 2, TERRA))
    body.append(rect(first_c - 2, ry - 2, last_c - first_c + 4, 4, TERRA))
    body.append(rect(first_c - 2, by + bh + 14, 4, ry - by - bh - 12, TERRA))
    body.append(f'<polygon points="{n(first_c - 9)},{n(by + bh + 15)} {n(first_c)},{n(by + bh + 1)} '
                f'{n(first_c + 9)},{n(by + bh + 15)}" fill="{TERRA}"/>')
    body.append(text((first_c + last_c) / 2, ry - 12, "repeat, one knob at a time, until you stop it",
                     size=15, anchor="middle"))
    desc = ("The experiment loop in five steps: the agent edits one knob in config.py, commits, "
            "runs the locked eval, keeps or reverts against the best kept score, and logs the run "
            "to results.tsv, then repeats.")
    return svg(W, H, "The loop", desc, body)


if __name__ == "__main__":
    write("score-by-run.svg", score_by_run(ROOT / "results.tsv"))
    write("loop.svg", loop())
