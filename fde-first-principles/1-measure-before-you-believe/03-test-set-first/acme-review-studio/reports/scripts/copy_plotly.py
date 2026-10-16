"""Quarto pre-render step: copy plotly.js from the installed plotly package next to the pages.

Pages load it with <script src="plotly.min.js">, so charts work offline and without a CDN.
"""
from pathlib import Path

from plotly.offline import get_plotlyjs

target = Path(__file__).resolve().parents[1] / "plotly.min.js"
js = get_plotlyjs()
if not target.exists() or target.stat().st_size != len(js.encode("utf-8")):
    target.write_text(js, encoding="utf-8")
