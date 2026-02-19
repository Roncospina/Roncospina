import requests
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
USERNAME = "Roncospina"
NAME     = "Manuel Ospina"
ROLE     = "Full Stack Developer"

LOCATION  = "Colombia"
OS_INFO   = "Windows"
IDE_INFO  = "VS Code / WebStorm"
FOCUS     = "Scalable Web Apps"

CONTACT = [
    ("GitHub",    f"github.com/{USERNAME}"),
    ("Email",     "manuel.ospina2004@gmail.com"),
    # ("LinkedIn",  "# tu-linkedin"),
    # ("Twitter", "# tu-twitter"),
    # ("Discord",  "# tu-discord"),
]

HOBBIES = [
    ("Hobbies.Software", "Exploring scalable backend patterns, improving system design, and experimenting with new technologies."),
    ("Hobbies.Other", "Listening to music, playing football, boxing training, and competitive video games."),
]

STACK = {
    "Frontend":  "React, TypeScript, Tailwind, HTML, CSS",
    "Backend":   "NestJS, Node.js, Laravel",
    "API":       "GraphQL, Apollo, REST",
    "Database":  "PostgreSQL",
}

# About — 3 líneas cortas que se muestran bajo el header
ABOUT = [
    "Full-stack dev focused on scalable, clean architecture.",
    "ERP & financial systems — precision and performance first.",
    "Open to full-time roles & long-term collaborations.",
]
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
    ascii_lines = [
        r"xxxxxxxxxxxxxxxxXXXXXXXXXXXXXXXXXXX$XXXXXXXXXXXXXXXXXXX",
        r"xxxxxXxxXXXXXXXXXXXXXXXXXXX$X$$$$$$$$$$$$$$$$$$$$$XXXXX",
        r"XXXXXXXXXXXXXXXXXXXXXXX$X$$X$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        r"XXXXXXXXXXXXXXXXXXX$$X$X$Xxxx;;.;++xX$$$$$$$$$$$$$$$$$$",
        r"XXXXXXXXXXXXXX$$$$XXXX+;:.............:;+xX$$$$$$$$$$$$",
        r"XXXXXXXXX$$$$$$$$$$$x......................:x$$$$$$$$$$",
        r"XXX$$$$$$$$$$$$$$$:..........................;xX$$$$$$$",
        r"$X$$$$$$$$$$$$$$;...............................:+X$$$$",
        r"$$$$$$$$$$$$$$X.......................:............;$$$",
        r"$$$$$$$$$$$$$x..........;:;:::::::.................;X$$",
        r"$$$$$$$$$$$$x.......;+;...;;xX$$$$$XXx+::..........;$$$",
        r"$$$$$$$$$X+:......;;;;+xx+;:...:x$$$$$$$$x;::;;.....X$$",
        r"$$$$$$$x;::.....:;;;+xXXX$$$Xx+;x$$$&$&$$$$$Xx+.....X$$",
        r"$$$$$x;:::......;+xXXXx;:;+$$$xxxX$$$$X+;:;xXxx+:..;$$$",
        r"$$$x;::::......;+xX$$$$XxxxXxXXxxX$$$$XXx;::::;x;..x$$$",
        r"$$X;:::..;;xx.:;+xX$$$$$$$$$$XXxx$$$$$$$$$$$xx+x+:;$$$$",
        r"$Xx;:::.;$x;;::;+xxX$$$$$$$$$XxxX$$$$$;.;x$$$$XX+:x$$$$",
        r"$x;:::..xXx;.:;;;x$$$$$&&&$$xxxX$$$$$$$$xx:+$$XX+;$$$$$",
        r"x;::::..:x+.::;;+x$$$&$$$$x+xxxX$&&$$$$$$$$$$$$Xx$$$$$$",
        r";::::....x+;.:;+xX$$$&$$xXxx;::;xX$$$$$$$$$$$$$X$$$$$$$",
        r":::::....:;:.:;+x$$$$$XxxXX$$$$$$$X+X$&&&$$$$$$$$$$$$$$",
        r"::...........:;;xX$$$$x;+xXX$$$$$$$$$$$$&&$$$$$$$$$$$$$",
        r":..............:;x$$&&$X+;x$xxx$$$$$$$$$$$$$$$$$$$$$$$$",
        r"................;x$$$$$$$$Xx$$&&$xX$$$$$$$$$$$$$$$$$$$$",
        r"................;+xX$$$$$$$$$$$$Xx;+X$$$$$$$$$$$$$$$$$$",
        r".................:;xX$$$$$Xxx$$&&$&&$$$$$$$+X$$$$$$$$$$",
        r"............;:.....;xX$$$$x;;x$$$$$&&$$XXx+x$$$$$$$$$$$",
        r"...........::;;:....:+xXXXx+XX$$$&$$$$X+:;x$$$$$$$$$$$$",
        r"...........::;;;:....:+x++xxX$$$$$$$$x;.:x$$$$$$$$$$$$$",
        r"...........:;;;;;:;:.::;;+xxxXXXx+;;:...X$$$$$$$&$$$$$$",
        r"...........:;;;:;;;;;;.....:;;;;;:..:;x$$$$$$$$$$$$$$$$",
        r"...........:;;;;;;;;+++++;....::;;+XX$$$$$$&&&&$$$$$$$$",
        r"...........:+xxx++xXXXxxxX$X$$$$$$$$x....;xx$$$&$&$$$$$",
        r".........:;:+xXXxxxX$$$&$$$$$$$$$$$X.........X&$$$&$$$$",
        r"..........;;+xXXXXX$$$$$$$$$$$$$$$$;............+x+;;:;",
        r"...........;+xxX$$$$$$$$$$$$$$$$$x.....................",
        r"............;xxX$$$$$$$$$$$$$$$X.......................",
        r"..............:;xX$$$$$$$$$x+:.........................",
    ]

    # ── Info panel ────────────────────────────────────────────────────────────
    info_lines = []
    info_lines.append(("header",    "manuel@ospina"))
    info_lines.append(("separator", "─" * 42))
    # About
    for line in ABOUT:
        info_lines.append(("about", line))
    info_lines.append(("blank", ""))
    info_lines.append(("separator", "─" * 42))
    info_lines.append(("kv",        ("Role",     ROLE)))
    info_lines.append(("kv",        ("Location", LOCATION)))
    info_lines.append(("kv",        ("OS",       OS_INFO)))
    info_lines.append(("kv",        ("IDE",      IDE_INFO)))
    info_lines.append(("kv",        ("Focus",    FOCUS)))
    info_lines.append(("blank", ""))
    for cat, techs in STACK.items():
        info_lines.append(("kv", (f"Stack.{cat}", techs)))
    info_lines.append(("blank", ""))
    for label, value in HOBBIES:
        info_lines.append(("kv", (label, value)))
    info_lines.append(("blank", ""))
    info_lines.append(("section",   "Contact"))
    info_lines.append(("separator", "─" * 42))
    for label, value in CONTACT:
        info_lines.append(("kv", (label, value)))
    info_lines.append(("blank", ""))
    info_lines.append(("section",   "GitHub Stats"))
    info_lines.append(("separator", "─" * 42))
    info_lines.append(("stat", (f"Repos: {stats['repos']}", f"Stars: {stats['stars']}")))
    info_lines.append(("stat", (f"Commits: {stats['commits']:,}", f"Followers: {stats['followers']}")))

    # ── Dimensiones ───────────────────────────────────────────────────────────
    ASCII_FONT   = 8.2
    ASCII_LINE_H = 10.5
    INFO_FONT    = 12.5
    INFO_LINE_H  = 20

    n_ascii       = len(ascii_lines)
    ASCII_BLOCK_H = n_ascii * ASCII_LINE_H

    info_h = 0
    for item in info_lines:
        if item[0] == "blank":       info_h += INFO_LINE_H * 0.55
        elif item[0] == "header":    info_h += INFO_LINE_H * 1.4
        elif item[0] == "section":   info_h += INFO_LINE_H * 0.9
        elif item[0] == "about":     info_h += INFO_LINE_H * 0.95
        else:                        info_h += INFO_LINE_H

    PAD    = 28
    W      = 980
    H      = int(max(ASCII_BLOCK_H, info_h) + PAD * 3.2)
    H      = max(H, 540)

    INFO_X  = 400
    DIVIDER = INFO_X - 16
    MONO    = "JetBrains Mono, Fira Code, Consolas, monospace"

    BG          = "#0d1117"
    BORDER      = "#30363d"
    ACCENT      = "#58a6ff"
    TEXT_DIM    = "#8b949e"
    TEXT_MAIN   = "#c9d1d9"
    TEXT_BRIGHT = "#ffffff"
    TEXT_ABOUT  = "#a8d8ea"
    GREEN       = "#3fb950"
    ORANGE      = "#d29922"

    parts = []

    parts.append(f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="#161b22"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="{ACCENT}" stop-opacity="0.8"/>
    <stop offset="100%" stop-color="{GREEN}"  stop-opacity="0.3"/>
  </linearGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>""")

    parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    parts.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="url(#borderGrad)" stroke-width="1.5"/>')
    parts.append(f'<line x1="{DIVIDER}" y1="{PAD}" x2="{DIVIDER}" y2="{H-PAD}" stroke="{BORDER}" stroke-width="1" opacity="0.5"/>')

    # ── ASCII (izquierda) ──────────────────────────────────────────────────────
    ascii_y_start = (H - ASCII_BLOCK_H) / 2 + ASCII_LINE_H
    for i, aline in enumerate(ascii_lines):
        y   = ascii_y_start + i * ASCII_LINE_H
        esc = aline.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        mid  = n_ascii / 2
        dist = abs(i - mid) / mid
        if dist < 0.25:
            fill, alpha = ACCENT, 1.0
        elif dist < 0.5:
            fill, alpha = "#79c0ff", 0.85
        elif dist < 0.75:
            fill, alpha = TEXT_DIM, 0.65
        else:
            fill, alpha = TEXT_DIM, 0.4
        parts.append(
            f'<text x="{PAD}" y="{y:.1f}" font-family="{MONO}" font-size="{ASCII_FONT}" '
            f'fill="{fill}" opacity="{alpha:.2f}" xml:space="preserve">{esc}</text>'
        )

    # ── Info (derecha) ─────────────────────────────────────────────────────────
    y = PAD + 18.0
    for item in info_lines:
        kind = item[0]

        if kind == "blank":
            y += INFO_LINE_H * 0.55
            continue

        elif kind == "header":
            parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="17" '
                f'font-weight="bold" fill="{TEXT_BRIGHT}" filter="url(#glow)">{item[1]}</text>'
            )
            y += INFO_LINE_H * 1.4

        elif kind == "separator":
            parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                f'fill="{BORDER}" opacity="0.7">{item[1]}</text>'
            )
            y += INFO_LINE_H

        elif kind == "section":
            parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                f'fill="{TEXT_DIM}">─ {item[1]}</text>'
            )
            y += INFO_LINE_H * 0.9

        elif kind == "about":
            parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="11.5" '
                f'fill="{TEXT_ABOUT}" opacity="0.85" font-style="italic">{item[1]}</text>'
            )
            y += INFO_LINE_H * 0.95

        elif kind == "kv":
            label, value = item[1]
            parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{ACCENT}">'
                f'{label}:</text>'
            )
            lw = len(label) * 7.4 + 12
            parts.append(
                f'<text x="{INFO_X + lw:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{TEXT_MAIN}">'
                f'{value}</text>'
            )
            y += INFO_LINE_H

        elif kind == "stat":
            left, right = item[1]
            parts.append(
                f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{GREEN}">{left}</text>'
            )
            parts.append(
                f'<text x="{INFO_X + 250}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" fill="{GREEN}">{right}</text>'
            )
            y += INFO_LINE_H

    # ── Barra decorativa ──────────────────────────────────────────────────────
    palette = [ACCENT, GREEN, ORANGE, "#bc8cff", "#ff7b72", "#79c0ff"]
    bw = (W - PAD * 2) // len(palette)
    by = H - 12
    for i, c in enumerate(palette):
        parts.append(
            f'<rect x="{PAD + i*bw}" y="{by}" width="{bw}" height="4" rx="2" fill="{c}" opacity="0.75"/>'
        )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        + "\n".join(parts)
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
