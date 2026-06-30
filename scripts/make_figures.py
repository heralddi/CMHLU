"""Generate the small SVG figures used in the README.

The script uses only the Python standard library plus the local RSA code so the
figures can be regenerated even before installing plotting libraries.
"""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.hope_wh_scenario import (
    L2_ASSUMPTION,
    NATIVE_ASSUMPTION,
    cost_sweep,
    make_model,
    marked_speaker_probability,
    prior_sweep,
)

FIGURE_DIR = PROJECT_ROOT / "figures"


def _svg_header(width: int = 760, height: int = 430) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]


def _axis(title: str, x_label: str, y_label: str) -> list[str]:
    return [
        f'<text x="380" y="32" text-anchor="middle" font-family="Arial" font-size="22">{title}</text>',
        '<line x1="80" y1="340" x2="700" y2="340" stroke="black"/>',
        '<line x1="80" y1="80" x2="80" y2="340" stroke="black"/>',
        '<text x="390" y="405" text-anchor="middle" font-family="Arial" font-size="15">' + x_label + '</text>',
        '<text x="24" y="220" transform="rotate(-90 24,220)" text-anchor="middle" font-family="Arial" font-size="15">' + y_label + '</text>',
        '<text x="70" y="345" text-anchor="end" font-family="Arial" font-size="12">0</text>',
        '<text x="70" y="220" text-anchor="end" font-family="Arial" font-size="12">0.5</text>',
        '<text x="70" y="95" text-anchor="end" font-family="Arial" font-size="12">1.0</text>',
    ]


def write_speaker_comparison() -> None:
    native_value = marked_speaker_probability(make_model(NATIVE_ASSUMPTION))
    l2_value = marked_speaker_probability(make_model(L2_ASSUMPTION))
    values = [
        ("Native", native_value, "#4c78a8"),
        ("L2", l2_value, "#f58518"),
    ]
    lines = _svg_header()
    lines.extend(_axis("Speaker choice for the marked message", "Speaker assumption", "S1(hope_what_S | desire_positive_S)"))
    for index, (label, value, color) in enumerate(values):
        x = 230 + index * 210
        bar_height = value * 250
        y = 340 - bar_height
        lines.append(f'<rect x="{x}" y="{y:.1f}" width="90" height="{bar_height:.1f}" fill="{color}"/>')
        lines.append(f'<text x="{x + 45}" y="365" text-anchor="middle" font-family="Arial" font-size="15">{label}</text>')
        lines.append(f'<text x="{x + 45}" y="{y - 8:.1f}" text-anchor="middle" font-family="Arial" font-size="13">{value:.2f}</text>')
    lines.append("</svg>")
    (FIGURE_DIR / "speaker_choice.svg").write_text("\n".join(lines) + "\n")


def write_line_plot(rows: list[tuple[float, float]], title: str, x_label: str, output_name: str, x_max: float) -> None:
    lines = _svg_header()
    lines.extend(_axis(title, x_label, "S1(hope_what_S | desire_positive_S)"))
    points = []
    for x_value, y_value in rows:
        x = 80 + (x_value / x_max) * 620
        y = 340 - y_value * 250
        points.append(f"{x:.1f},{y:.1f}")
    lines.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#4c78a8" stroke-width="3"/>')
    for x_value, y_value in rows[:: max(1, len(rows) // 8)]:
        x = 80 + (x_value / x_max) * 620
        y = 340 - y_value * 250
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#4c78a8"/>')
    lines.append("</svg>")
    (FIGURE_DIR / output_name).write_text("\n".join(lines) + "\n")


def main() -> None:
    FIGURE_DIR.mkdir(exist_ok=True)
    write_speaker_comparison()
    write_line_plot(cost_sweep(), "Cost sensitivity", "Cost assigned to hope_what_S", "cost_sweep.svg", 3.0)
    write_line_plot(prior_sweep(), "Prior sensitivity", "Prior assigned to hope_what_S", "prior_sweep.svg", 0.40)


if __name__ == "__main__":
    main()
