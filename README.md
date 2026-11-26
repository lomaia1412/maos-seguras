# Mãos Seguras em 40 segundos

Material educativo sobre **higiene das mãos** (fricção antisséptica com preparação alcoólica) para a disciplina de
Segurança do Paciente — Medicina UNISINOS, 2026/2.

Um cartaz com QR code fica ao lado do dispenser de álcool gel. O profissional escaneia **antes** de usar o produto,
joga por ~40 s (monta a sequência dos 6 movimentos + responde 1 pergunta), guarda o celular e higieniza as mãos.

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | O jogo. Arquivo único (HTML + CSS + JS), sem frameworks, backend ou login. ~30 KB. |
| `cartaz.html` | Cartaz A4 retrato (fonte do PDF). |
| `cartaz.pdf` | Cartaz pronto para imprimir e plastificar. |
| `qrcode.svg` / `qrcode.png` | QR code (correção de erro **H**) para a URL do jogo. Use o SVG na impressão. |
| `gerar_qr.py` | Gera o QR a partir da URL e atualiza a URL impressa no cartaz. |
| `ilustracoes.svg` | Fonte das 6 ilustrações (usadas no jogo e no cartaz). |
| `ferramentas/embutir_ilustracoes.py` | Copia `ilustracoes.svg` para dentro de `index.html` e `cartaz.html`. |
| `ferramentas/gerar_pdf.js` | Gera `cartaz.pdf` a partir de `cartaz.html` (Chromium headless). |
| `.nojekyll` | Faz o GitHub Pages servir os arquivos como estão. |

## 1. Publicar no GitHub Pages

Pré-requisitos: conta no GitHub e `git` instalado.

1. No GitHub, crie um repositório **público** chamado `maos-seguras` (sem README, sem .gitignore).
2. Na pasta do projeto, rode (troque `SEU-USUARIO`):

   ```bash
   git init -b main          # (pule se a pasta já for um repositório git)
   git add .
   git commit -m "Mãos Seguras: jogo, cartaz e QR"
   git remote add origin https://github.com/SEU-USUARIO/maos-seguras.git
   git push -u origin main
   ```
3. No repositório: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   Branch: **main**, pasta **/ (root)** → **Save**.
4. Aguarde 1–2 min. O jogo fica em **`https://SEU-USUARIO.github.io/maos-seguras/`**
   (abre em qualquer celular, sem login). Teste no 4G, fora do Wi-Fi do hospital.

## 2. Trocar a URL do QR (depois de saber a URL final)

```bash
pip install segno
python3 gerar_qr.py https://SEU-USUARIO.github.io/maos-seguras/
```

Ou edite a variável `URL` no topo de `gerar_qr.py` e rode `python3 gerar_qr.py`.
O script regenera `qrcode.svg`/`qrcode.png` e troca a URL impressa sob o QR em `cartaz.html`.
Em seguida **regenere o PDF** (próxima seção), faça commit/push e **teste o QR impresso com 2–3 celulares**.

> O QR aponta para a URL do GitHub Pages. Se no futuro mudar o endereço, o cartaz impresso para de funcionar —
> por isso escolha o nome do repositório antes de imprimir.

## 3. Gerar o PDF do cartaz

**Opção A — automática (Node.js):**

```bash
npm i -D playwright && npx playwright install chromium   # só na 1ª vez
node ferramentas/gerar_pdf.js
```

**Opção B — manual:** abra `cartaz.html` no Chrome → Imprimir → Destino *Salvar como PDF* →
Papel **A4**, Margens **Padrão**, marque **Gráficos de plano de fundo**.

Impressão: A4, 100 % (sem "ajustar à página"), colorida. O QR sai com ~6,2 cm de lado.

## 4. Personalizar

- **Logos:** no `cartaz.html`, troque os blocos `<div class="logo">LOGO …</div>` por
  `<div class="logo"><img src="logo-unisinos.png" alt="UNISINOS"></div>` (coloque a imagem na pasta).
- **Perguntas:** em `index.html`, edite o array `BANCO` (`q` = pergunta, `a` = `true` para Sim / `false` para Não,
  `e` = explicação curta, até ~70 caracteres para caber em 2 linhas).
- **Forçar uma pergunta** (para apresentação): `…/maos-seguras/?q=4` mostra a 4ª pergunta do banco.
- **Ilustrações:** edite `ilustracoes.svg` e rode `python3 ferramentas/embutir_ilustracoes.py`.

## Contador de jogadas

Ao chegar na tela final, o jogo soma 1 num contador público e gratuito (serviço Abacus) e mostra
"Você é a pessoa nº X a completar o Mãos Seguras". Só o número é enviado: nenhum nome, e-mail ou resposta.

- Ver o total sem somar: abra https://abacus.jasoncameron.dev/get/maos-seguras-unisinos-2026/conclusoes
  (aparece algo como `{"value": 42}`).
- Desligar: em `index.html`, deixe `CONTADOR_URL=""`.
- Se o serviço estiver fora do ar, o jogo funciona normal e só não mostra o número.
- Funciona no GitHub Pages. No link do Claude (claude.ai/artifact/…) o contador não aparece, porque
  essas páginas não podem acessar serviços externos.
- "Jogar de novo" conta outra vez: o número é de jogadas concluídas, não de pessoas diferentes.

## Privacidade

Além do contador acima, o jogo guarda no próprio celular (localStorage) só o número da última pergunta vista,
para não repeti-la. A avaliação 👍/👎 apenas mostra "Obrigado!" e não é enviada.

## Referências

- BRASIL. Ministério da Saúde. Portaria MS nº 529/2013 — Programa Nacional de Segurança do Paciente (PNSP).
- BRASIL. MS/Anvisa/Fiocruz. Protocolo para a prática de higiene das mãos em serviços de saúde (Portarias nº 1.377/2013 e nº 2.095/2013).
- BRASIL. Anvisa. RDC nº 36/2013.
- WHO. Guidelines on Hand Hygiene in Health Care, 2009.
- BRASIL. NR 32 — Segurança e saúde no trabalho em serviços de saúde.
