#!/usr/bin/env python3
"""Copia as ilustrações de ilustracoes.svg para dentro de index.html e cartaz.html
(entre os marcadores ILUSTRACOES:INICIO / ILUSTRACOES:FIM), mantendo o jogo em arquivo único.
Rode depois de editar ilustracoes.svg:  python3 ferramentas/embutir_ilustracoes.py
"""
import re, pathlib
raiz = pathlib.Path(__file__).resolve().parent.parent
svg = (raiz / "ilustracoes.svg").read_text(encoding="utf-8").strip()
svg = re.sub(r"<!--.*?-->\s*", "", svg, flags=re.S)          # remove comentários
svg = re.sub(r"\n\s+", "\n", svg)                               # compacta indentação
padrao = re.compile(r"(<!-- ILUSTRACOES:INICIO[^>]*-->).*?(<!-- ILUSTRACOES:FIM -->)", re.S)
for nome in ("index.html", "cartaz.html"):
    arq = raiz / nome
    if not arq.exists():
        continue
    html = arq.read_text(encoding="utf-8")
    novo, n = padrao.subn(lambda m: m.group(1) + "\n" + svg + "\n" + m.group(2), html)
    if n != 1:
        raise SystemExit(f"Marcadores não encontrados em {nome}")
    arq.write_text(novo, encoding="utf-8")
    print(f"ok: ilustrações embutidas em {nome}")
