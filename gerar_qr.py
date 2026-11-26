#!/usr/bin/env python3
"""Gera qrcode.png e qrcode.svg (correção de erro nível H) apontando para a URL do jogo,
e atualiza a URL impressa no cartaz.html.

Uso:
    pip install segno
    python3 gerar_qr.py                                    # usa a URL abaixo
    python3 gerar_qr.py https://fulana.github.io/maos-seguras/

Depois, regenere o PDF do cartaz (veja README.md):  node ferramentas/gerar_pdf.js
"""
import re, sys, pathlib

# >>> TROQUE AQUI pela URL final do GitHub Pages (ou passe como argumento) <<<
URL = "https://claude.ai/artifact/3ar7oDL4k57JZteQ7sLQxR"

try:
    import segno
except ImportError:
    sys.exit("Falta a biblioteca 'segno'. Instale com:  pip install segno")

raiz = pathlib.Path(__file__).resolve().parent
url = sys.argv[1] if len(sys.argv) > 1 else URL
if not re.match(r"^https?://", url):
    sys.exit("A URL precisa começar com http:// ou https://")

# boost_error=False garante o nível H exatamente (não troca por outro).
qr = segno.make_qr(url, error="h", boost_error=False)
largura_modulos = qr.symbol_size(border=4)[0]

# PNG: ~1600 px de lado -> 4 cm a 1000 dpi / 6 cm a ~680 dpi: imprime nítido em qualquer tamanho >= 4 cm.
escala = max(10, round(1600 / largura_modulos))
qr.save(raiz / "qrcode.png", scale=escala, border=4, dark="#0b2e2c", light="#ffffff")
# SVG vetorial (preferido para impressão): escala infinita.
qr.save(raiz / "qrcode.svg", scale=10, border=4, dark="#0b2e2c", light="#ffffff", xmldecl=False, svgns=True)

# Atualiza a URL exibida no cartaz.
cartaz = raiz / "cartaz.html"
if cartaz.exists():
    html = cartaz.read_text(encoding="utf-8")
    exib = re.sub(r"^https?://", "", url).rstrip("/")
    html = re.sub(r'(<span id="url-qr">).*?(</span>)', lambda m: m.group(1) + exib + m.group(2), html)
    cartaz.write_text(html, encoding="utf-8")

print(f"URL: {url}")
print(f"QR versão {qr.version}, correção de erro {qr.error}, {largura_modulos} módulos (com margem)")
print(f"qrcode.png: {largura_modulos*escala}px de lado | qrcode.svg: vetorial")
print("Próximo passo: regenerar o cartaz.pdf (node ferramentas/gerar_pdf.js) e conferir lendo o QR com o celular.")
