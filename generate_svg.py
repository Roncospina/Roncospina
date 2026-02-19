import requests
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
USERNAME = "Roncospina"
NAME     = "Manuel Ospina"
ROLE     = "Full Stack Developer"

# ─── PERSONAL INFO ────────────────────────────────────────────────────────────
LOCATION  = "Colombia"
OS_INFO   = "macOS / Windows"
IDE_INFO  = "VS Code"
FOCUS     = "Scalable Web Apps"

# Redes sociales — pon tus datos reales aquí
CONTACT = [
    ("LinkedIn",  "# tu-linkedin"),        # ← pon tu usuario
    ("GitHub",    f"github.com/{USERNAME}"),
    ("Email",     "# tu@email.com"),        # ← pon tu email
    # ("Twitter", "# tu-twitter"),
    # ("Discord",  "# tu-discord"),
]

# Hobbies — personaliza estas líneas
HOBBIES = [
    ("Hobbies.Software", "# pon tus hobbies de software"),  # ← edita
    ("Hobbies.Other",    "# pon tus otros hobbies"),        # ← edita
]

# Stack tecnológico
STACK = {
    "Frontend":  "React, TypeScript, Tailwind, HTML, CSS",
    "Backend":   "NestJS, Node.js, Laravel",
    "API":       "GraphQL, Apollo, REST",
    "Database":  "PostgreSQL",
}
# ──────────────────────────────────────────────────────────────────────────────


def fetch_github_stats(username, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    base = "https://api.github.com"
    user = requests.get(f"{base}/users/{username}", headers=headers).json()
    repos_data = requests.get(
        f"{base}/users/{username}/repos?per_page=100&type=owner", headers=headers
    ).json()
    stars = sum(r.get("stargazers_count", 0) for r in repos_data if isinstance(r, dict))
    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    commits_resp = requests.get(
        f"{base}/search/commits?q=author:{username}&per_page=1",
        headers={**headers, "Accept": "application/vnd.github.cloak-preview"},
    ).json()
    commits = commits_resp.get("total_count", 0)
    return {"repos": public_repos, "stars": stars, "commits": commits, "followers": followers}


def make_svg(stats):
    # ── Tu ASCII art ──────────────────────────────────────────────────────────
    ascii_lines = [
        r"................................:;+x$$$$$$$Xx;:......",
        r".............................;x$$$$$$$$$$$$$$$$$$;:..",
        r"..........................:x$$$$$$$$$$$$$$$$$$$$$$$$;",
        r"........................;$$$$$$$$$$$$$$$$$$$$$$$$$$$$$x",
        r"......................;$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$x:",
        r"....................;X$$$$$$$$$$$$$$$$$$$$$$$X$$$$$$$$$$$$;",
        r"..................:x$$$$$$$$$$XXXXXXXXXXXXXXXXXXX$$$$$$$$$$X:",
        r".................:$$$$$$$$XXXXXXXXXXXxXXxXXXXXXXXXXXX$$$$$$$$+",
        r"................+$$$$$XXXXXXXXXXxxxxxxxxxxxxxxxxXXXXXXXX$$$$$$x",
        r"...............x$$$$$XXXXXXxxxxxxxxxxxxxxxxxxxxxxxxxXXXXXX$$$$$$;",
        r".............:X$$$$XXXXXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxXXXXX$$$$$;",
        r"............:X$$$$XXXXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxXXXXX$$$$;",
        r"...........:x$$$XXXXXxxxxxxx+;;;::...........:::;;+xxxxxxxxXXXX$$XX;",
        r"..........:x$$$XXXXxxx;;:...             .;xXXXx:    ..:;+xxXXXX$$$X;",
        r".........:x$$$$XXx;:.  .x&&&&X.        .x&&&&&&&&&;        .;+XXX$$$X;",
        r".........x$$$Xx;.     ;&&&&&&&&;      .$&&&&&&&&&&&;          .;xX$$$x:",
        r"........;$$$$;.      :$&&&&&&&&&.     x&&&&&$X&&&&&$.            :X$$$+",
        r".......:x$$$;.       +&&$x+++&&&x    :$&&&+;X$;$&&&&;             :x$$X;",
        r".......;X$$x.       .x&$:.  .+&&$    ;&&&X.    .&&&&x             .;$$$;",
        r".......;x$$+.       .x&$:    .&&$ ..:x&&&x.   ..&&&&x              ;$$$;",
        r".......:x$$x.        ;&&+  . .&&&$$$$$$&&$.   .:&&&&;             .;$$X;",
        r"........;X$X:        .x&&;...x$$$$$$$$$$$$$$;..&&&&&.             .x$$+",
        r"........:x$$x.         ;$&&&$$$$$$$$$$$$$$$$$$&&&&&x             .;X$X;",
        r".........;X$X;.        .x&$$$$$$$$$$$$$$$$$$$$$$$$x.             :XXX+",
        r"..........+X$X;       ;$$$$$$$$$$$&$$&$$$&$$&$$$$$$$;           .XX$x",
        r"...........+XXX;.    :X$$$$$$$&$$$$$$$$$$$$$$$$$$&$$x.         .XX$x:",
        r"............xXXX;    .x$$&$$$$$$$$$$$$$&$$$$$$&&X;xX;         .XXXx:",
        r".............xXXX+    :x$x+$&$$$&$$&$$$$$$&&X;;$$$x.         :XXXx:",
        r"..............xXXX+.   .x$$Xx;+$&$$&&&$x;+XX$$$$;.          ;xXXx:",
        r"...............+XXXx.    .+$$$$$XxxxXXX$$$$$$x:            ;XXXx.",
        r"................;XXXx:     ..;$$$$$$$$$$$$x:.            .+XXXx.",
        r".................;xXXx;.       .:;x$$$x;:.              :xXXX;",
        r"..................:+XXX+.                             .;xXXx:",
        r"....................;x$Xx;.                         .:xX$X;",
        r".....................:+X$$x;.                     ..xX$$x:",
        r".......................:xX$X;:.                  .+xX$x;",
        r".........................;xx+;X;.             .;xX+;+;",
        r"...........................;xx+X$x;.       .:+$$xxx;",
        r".............................:+;X$$$$x;:;+X$$$$x;;",
        r"................................;X$$$$$$$$$$$$x:",
        r".................................;;x$$$$$$$$;;:",
    ]

    # ── Info panel ────────────────────────────────────────────────────────────
    info_lines = []
    info_lines.append(("header",    f"manuel@ospina"))
    info_lines.append(("separator", "─" * 44))
    info_lines.append(("kv",        ("Role",     ROLE)))
    info_lines.append(("kv",        ("Location", LOCATION)))
    info_lines.append(("kv",        ("OS",       OS_INFO)))
    info_lines.append(("kv",        ("IDE",      IDE_INFO)))
    info_lines.append(("kv",        ("Focus",    FOCUS)))
    info_lines.append(("blank",     ""))
    for cat, techs in STACK.items():
        info_lines.append(("kv", (f"Stack.{cat}", techs)))
    info_lines.append(("blank", ""))
    for label, value in HOBBIES:
        info_lines.append(("kv", (label, value)))
    info_lines.append(("blank", ""))
    info_lines.append(("section",   "Contact"))
    info_lines.append(("separator", "─" * 44))
    for label, value in CONTACT:
        info_lines.append(("kv", (label, value)))
    info_lines.append(("blank", ""))
    info_lines.append(("section",   "GitHub Stats"))
    info_lines.append(("separator", "─" * 44))
    info_lines.append(("stat", (f"Repos: {stats['repos']}", f"Stars: {stats['stars']}")))
    info_lines.append(("stat", (f"Commits: {stats['commits']:,}", f"Followers: {stats['followers']}")))

    # ── Dimensiones ───────────────────────────────────────────────────────────
    # El ASCII tiene 41 líneas × ~7.5px = ~308px de alto
    # Necesitamos suficiente alto para ambos lados
    ASCII_FONT   = 7.5    # font-size del ASCII (pequeño para que quepa)
    ASCII_LINE_H = 9.5
    INFO_FONT    = 13.0
    INFO_LINE_H  = 21

    n_ascii  = len(ascii_lines)
    n_info   = len(info_lines)

    ASCII_BLOCK_H = n_ascii * ASCII_LINE_H
    # calcular alto info
    info_h = 0
    for item in info_lines:
        if item[0] == "blank":     info_h += INFO_LINE_H * 0.55
        elif item[0] == "header":  info_h += INFO_LINE_H * 1.3
        elif item[0] == "section": info_h += INFO_LINE_H * 0.9
        else:                      info_h += INFO_LINE_H

    PAD  = 30
    W    = 960
    H    = int(max(ASCII_BLOCK_H, info_h) + PAD * 3)
    H    = max(H, 520)

    INFO_X  = 370
    DIVIDER = INFO_X - 18
    MONO    = "JetBrains Mono, Fira Code, Consolas, monospace"

    # Colores
    BG          = "#0d1117"
    BORDER      = "#30363d"
    ACCENT      = "#58a6ff"
    TEXT_DIM    = "#8b949e"
    TEXT_MAIN   = "#c9d1d9"
    TEXT_BRIGHT = "#ffffff"
    GREEN       = "#3fb950"
    ORANGE      = "#d29922"

    svg_parts = []

    # defs
    svg_parts.append(f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="#161b22"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="{ACCENT}" stop-opacity="0.7"/>
    <stop offset="100%" stop-color="{GREEN}"  stop-opacity="0.3"/>
  </linearGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>""")

    # fondo + borde
    svg_parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    svg_parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="url(#borderGrad)" stroke-width="1.5"/>')
    # divisor vertical
    svg_parts.append(f'<line x1="{DIVIDER}" y1="{PAD}" x2="{DIVIDER}" y2="{H-PAD}" stroke="{BORDER}" stroke-width="1" opacity="0.6"/>')

    # ── ASCII (izquierda, centrado verticalmente) ──────────────────────────────
    ascii_y_start = (H - ASCII_BLOCK_H) / 2 + ASCII_LINE_H
    for i, aline in enumerate(ascii_lines):
        y   = ascii_y_start + i * ASCII_LINE_H
        esc = aline.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        # gradiente de color: las líneas centrales (cara) más brillantes
        mid   = n_ascii / 2
        dist  = abs(i - mid) / mid          # 0=centro, 1=extremo
        alpha = max(0.35, 1.0 - dist * 0.5)
        # color: centro azul brillante, bordes más apagados
        if dist < 0.3:
            fill = ACCENT
        elif dist < 0.6:
            fill = "#79c0ff"
        else:
            fill = TEXT_DIM
        svg_parts.append(
            f'<text x="{PAD}" y="{y:.1f}" font-family="{MONO}" font-size="{ASCII_FONT}" '
            f'fill="{fill}" opacity="{alpha:.2f}" xml:space="preserve">{esc}</text>'
        )

    # ── Info panel (derecha) ───────────────────────────────────────────────────
    y = PAD + 16.0
    for item in info_lines:
        kind = item[0]

        if kind == "blank":
            y += INFO_LINE_H * 0.55
            continue

        if kind == "header":
            svg_parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="16" '
                f'font-weight="bold" fill="{TEXT_BRIGHT}" filter="url(#glow)">{item[1]}</text>'
            )
            y += INFO_LINE_H * 1.3

        elif kind == "separator":
            svg_parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                f'fill="{BORDER}" opacity="0.8">{item[1]}</text>'
            )
            y += INFO_LINE_H

        elif kind == "section":
            svg_parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                f'fill="{TEXT_DIM}">─ {item[1]}</text>'
            )
            y += INFO_LINE_H * 0.9

        elif kind == "kv":
            label, value = item[1]
            svg_parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{ACCENT}">'
                f'{label}:</text>'
            )
            lw  = len(label) * 7.6 + 12
            svg_parts.append(
                f'<text x="{INFO_X + lw:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{TEXT_MAIN}">'
                f'{value}</text>'
            )
            y += INFO_LINE_H

        elif kind == "stat":
            left, right = item[1]
            svg_parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{GREEN}">{left}</text>'
            )
            svg_parts.append(
                f'<text x="{INFO_X + 240}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{GREEN}">{right}</text>'
            )
            y += INFO_LINE_H

    # ── Barra de colores decorativa ───────────────────────────────────────────
    palette = [ACCENT, GREEN, ORANGE, "#bc8cff", "#ff7b72", "#79c0ff"]
    bw = (W - PAD * 2) // len(palette)
    by = H - 14
    for i, c in enumerate(palette):
        svg_parts.append(
            f'<rect x="{PAD + i*bw}" y="{by}" width="{bw}" height="4" rx="2" fill="{c}" opacity="0.75"/>'
        )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        + "\n".join(svg_parts)
        + "\n</svg>"
    )
    return svg


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN", "")
    print("Fetching GitHub stats...")
    try:
        stats = fetch_github_stats(USERNAME, token)
        print(f"Stats: {stats}")
    except Exception as e:
        print(f"Could not fetch stats: {e}")
        stats = {"repos": 0, "stars": 0, "commits": 0, "followers": 0}

    svg = make_svg(stats)
    with open("profile.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("SVG generado: profile.svg")
