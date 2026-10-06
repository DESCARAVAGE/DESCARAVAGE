"""Génère assets/dark.svg et assets/light.svg à partir du bloc <!-- BANNER --> du README.

Usage : python3 scripts/build.py
Dépendances (Ubuntu) : sudo apt install python3-opencv python3-yaml
"""
import config
from banner import render
from portrait import to_ascii

AVATAR = config.ROOT / "scripts" / "avatar.png"
OUT = config.ROOT / "assets"


def main():
    cfg = config.load()
    lines = to_ascii(AVATAR)
    OUT.mkdir(exist_ok=True)
    svgs = []
    for mode in ("dark", "light"):
        svg = render(cfg, lines, mode)
        (OUT / f"{mode}.svg").write_text(svg, encoding="utf-8")
        print(f"{mode}.svg  {len(svg.encode()) // 1024} Ko")
        svgs.append(svg)
    config.update_readme(cfg, svgs)


if __name__ == "__main__":
    main()