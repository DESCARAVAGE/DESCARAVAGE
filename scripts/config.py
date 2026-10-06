"""Lecture du bloc <!-- BANNER --> du README et mise à jour des liens d'images."""
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SOCIALS = ("github", "linkedin", "x", "web")


@dataclass
class Banner:
    name: str
    greeting: str
    roles: list
    info: list      # [(libellé, valeur)]
    skills: list
    status: str
    socials: list


def load(path=README):
    m = re.search(r"<!--\s*BANNER\s*\n(.*?)-->", path.read_text(encoding="utf-8"), re.S)
    if not m:
        raise SystemExit("Bloc <!-- BANNER ... --> introuvable dans le README.")
    d = yaml.safe_load(m.group(1)) or {}
    cfg = Banner(
        name=str(d.get("name", "")),
        greeting=str(d.get("greeting", "")),
        roles=[str(r) for r in d.get("roles", [])],
        info=[(str(k), str(v)) for k, v in (d.get("info") or {}).items()],
        skills=[str(s) for s in d.get("skills", [])],
        status=str(d.get("status", "")),
        socials=[s for s in d.get("socials", []) if s in SOCIALS],
    )
    if not cfg.name or not cfg.roles:
        raise SystemExit("Le bloc BANNER doit contenir au moins « name » et « roles ».")
    for r in cfg.roles:
        if len(r) > 48:
            print(f"⚠️  rôle trop long (> 48 caractères) : {r!r}")
    if len(cfg.info) > 5:
        print("⚠️  plus de 5 lignes d'info : seules les 5 premières sont affichées")
        cfg.info = cfg.info[:5]
    return cfg


def update_readme(cfg, svgs, path=README):
    """Met ?v=<hash des SVG> sur les images (cache GitHub) et met à jour le texte alternatif."""
    txt = path.read_text(encoding="utf-8")
    ver = hashlib.sha1("".join(svgs).encode()).hexdigest()[:8]
    new = re.sub(r"(assets/(?:dark|light)\.svg)(\?v=[^\"'\s]*)?", rf"\1?v={ver}", txt)
    alt = f"{cfg.name} — {cfg.roles[0]}".replace('"', "'")
    new = re.sub(r'(<img alt=")[^"]*(" src="\./assets/dark\.svg)', rf"\g<1>{alt}\2", new)
    if new != txt:
        path.write_text(new, encoding="utf-8")
        print(f"README mis à jour (?v={ver})")