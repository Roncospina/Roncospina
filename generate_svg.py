import requests
import os
import xml.etree.ElementTree as ET

# ── CONFIG ────────────────────────────────────────────────────────────────────
USERNAME = "Roncospina"

LOCATION  = "Colombia"
OS_INFO   = "Windows"
IDE_INFO  = "VS Code / WebStorm"
ROLE      = "Full Stack Developer"
FOCUS     = "Scalable Web Apps"

CONTACT = [
    ("GitHub",    f"github.com/{USERNAME}"),
    ("Email",     "manuel.ospina2004@gmail.com"),
    #("LinkedIn",  "# tu-linkedin"),
]

HOBBIES = [
    ("Hobbies.Software", "Exploring scalable backend patterns,"),
    ("",                 "  improving system design & new tech."),
    ("Hobbies.Other",    "Music, football, contact sports,"),
    ("",                 "  and competitive video games."),
]

STACK = {
    "Frontend":  "React, TypeScript, Tailwind, HTML, CSS",
    "Backend":   "NestJS, Node.js, Laravel",
    "API":       "GraphQL, Apollo, REST",
    "Database":  "PostgreSQL",
}

ABOUT = [
    "Full-stack dev focused on scalable, clean architecture.",
    "ERP & financial systems — precision and performance first.",
    "Open to full-time roles & long-term collaborations.",
]
# ──────────────────────────────────────────────────────────────────────────────


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fetch_github_stats(username, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    base = "https://api.github.com"
    try:
        user = requests.get(f"{base}/users/{username}", headers=headers, timeout=10).json()
        repos_data = requests.get(
            f"{base}/users/{username}/repos?per_page=100&type=owner", headers=headers, timeout=10
        ).json()
        stars = sum(r.get("stargazers_count", 0) for r in repos_data if isinstance(r, dict))
        public_repos = user.get("public_repos", 0)
        followers = user.get("followers", 0)
        commits_resp = requests.get(
            f"{base}/search/commits?q=author:{username}&per_page=1",
            headers={**headers, "Accept": "application/vnd.github.cloak-preview"},
            timeout=10,
        ).json()
        commits = commits_resp.get("total_count", 0)

        lines_added, lines_deleted = 0, 0
        for repo in repos_data:
            if not isinstance(repo, dict): continue
            repo_name = repo.get("full_name", "")
            if not repo_name: continue
            stats_url = f"{base}/repos/{repo_name}/stats/contributors"
            r = requests.get(stats_url, headers=headers, timeout=15)
            if r.status_code == 202:
                import time; time.sleep(3)
                r = requests.get(stats_url, headers=headers, timeout=15)
            if r.status_code != 200: continue
            contributors = r.json()
            if not isinstance(contributors, list): continue
            for contributor in contributors:
                if not isinstance(contributor, dict): continue
                author = contributor.get("author", {})
                if author and author.get("login", "").lower() == username.lower():
                    for week in contributor.get("weeks", []):
                        lines_added   += week.get("a", 0)
                        lines_deleted += week.get("d", 0)

        return {
            "repos": public_repos, "stars": stars, "commits": commits, "followers": followers,
            "lines_added": lines_added, "lines_deleted": lines_deleted,
            "lines_total": lines_added - lines_deleted,
        }
    except Exception as e:
        print(f"Stats error: {e}")
        return {"repos": 0, "stars": 0, "commits": 0, "followers": 0,
                "lines_added": 0, "lines_deleted": 0, "lines_total": 0}


def fmt(n):
    return f"{n:,}"


def make_svg(stats):
    ascii_raw = [
        "                                                                                          ",
        "                                                                                          ",
        "                                                                                          ",
        "                                                                                          ",
        "                                           .  .:::.....:...                               ",
        "                                         :::::..:::..........::..                         ",
        "                                    ..::.::....................:::::..                    ",
        "                                  ............::..................:::::..                 ",
        "                               ..:.............::.........::..............                ",
        "                             ::::.......................:.................:...            ",
        "                            :...............................:...................          ",
        "                          :..:::...........::::...............::::....:.::....::::.       ",
        "                        ::....:.::.....:::..................::::.::...::...........:.     ",
        "                       ......................:..:::-::::....... ...:......:::......:.     ",
        "                     :.................::::::::::::::::....   ...........::::..:...:.     ",
        "                     ..... .......:::==+===**+**+==-====-:-=-:....::...............:::    ",
        "                    ...........::==+-:....::::=+#%#%%@@@%%%%%##*=:-:...:.::.........:.    ",
        "                    ..........:-==-::-===-:..::::::=*#@@@@@@@%##%%#=::....::::......::    ",
        "                    ........:-=====+#######*+=-:::::-=#@@@@@@@%%@%%%%#+===+=-:.......:.   ",
        "                   .......::======*#######%%@%#*===-=+#@@@@@@@@@@%%@@@%####+=:......::    ",
        "                  .......::===+*######**##%@@@@@#**++##%%%@@@@@%*+=+#%@@%###*=:.....::    ",
        "                 .......::-=+*######*-::..::=#%@%#***####%%%#%##+-::::-=*###**=:.::::     ",
        "               .......::::=++###%%%%#***++=-#%=+%#**###%@@%%%####*=-:::::::-*#*=:....     ",
        "              .::--:.::.:==+*###%%@@@@@%%%%@@%%########%%@@%%%%#####**====-:=##=-:.:      ",
        "            ...=+=+#+:::-==+*###%%%@@@@@@@%%%%%#####*#%%%%%%%%%%%%@@@%%##++===#=::::      ",
        "            ..=%*=-==-::-==+*####%%%@@@@@@@@@%%%###+*#%%%%@%%%++*#%@@@@%%%##+=#=:::.      ",
        "           ..-%%##+:-:::-==++*###%@@@@@@@@@@@%%####**##%%@@%%%*:...:+%%%%%%%##%+::.       ",
        "           ..*%#*#=-:::-=-==+##%@@@%@@@@@@@@@%###**##%%%%%%%%%%%%*-*#:=##%%####+::        ",
        "           . =#+#+:.-::=====*#%%%@@@@@@@@@@@#**#####%%@@@@%%%@@@%%%%#+==#%%%#%#=::        ",
        "            ..=**-.:::-====+##%%@@@@@@@@@%#==+*######@@@@@@%%@@@@@@@@@@@@%%%%%*=          ",
        "           ....**=-:.:-===+*##%%@@@@@@@%###=:-+=:::-*#%@@@@@%@@@@@@@@@@@@@@@@#=-          ",
        "           ....##-::.:-==+*##%@@@@@@%%#*######*=---=+*###%%@@@@@@@@@@@@@@@@@@#=           ",
        "           ....=+=::::-=++*##%%%@@#%%########%%%%%%%%%##=:-#%@@@@@@@@@@@@@@@@%            ",
        "           .....:-:.:::-==+##%%@@%%%##*###%%%%%@@@@%%@@%#*###@@@@@@@@@@@@@@@%             ",
        "           .........:::-==+##%@@@@@%#===+*#####%@@@@%@@@%%%%@@@@@@@@@@@@@@@%              ",
        "            ........:::::===*#@@@@@@@#=..-==++*##%@@@@@@@%%%%%@@%@@@@@@%%%@@              ",
        "              .......::.::-+#%%@@@@@%%%#**+*@@@@#**##%%@@@@%#%@@@%@@@@@@@%#@              ",
        "              ........::::-+##%@@@@@%#%%%###*#%@@@@@@#*##%@%##%@@@@%%%@@%%@               ",
        "              ..........::-+*###%@@@%%%%%@@%######%###*=-*###%%%@@@%%%%%%%#               ",
        "               ..........:-=++###%%@%%%%%%@@@@%%%%%###*--=+#%@%%@@@@%%@%%%                ",
        "               ...........::-=++#%%@@@%%%%%%###%@@@@@@@@@@@@@@@@@@@@@@%+=                 ",
        "                ...::......::::=*#%@@@@%%%##*==##%@@@@@@@@@@@@@@@@@%%#=-:                 ",
        "                  .::::.....:.:-=*#%#%%%@%#*=-=*#%@@@@@@@@@@@@@%####*=-:                  ",
        "                  ::--:::......:-+*######%#*+=+*##%@@@@@@@@@@@@###+===-                   ",
        "                  :::--::::....:::-=*#####**+#####@@@@@@@@@@@@%*=-:::::                   ",
        "                  :::----:::....::-=+***+=+**#####%@%@@@@%%@%#+-:::::                     ",
        "                 ::::----:::::....::==++*++**###%%%%%%######*=::::::                      ",
        "                 :::-----::::-::..:::-====++*###%#%##**+=+==::..:::                       ",
        "                 .::--:--::----===:...::::--==++***+==-=:::..::::                         ",
        "              ...::::----::----=====:.....::::::----:::::::::::                           ",
        "           .   .::::----:--:--==========-:......:::::::::=**#                             ",
        "       .........::::---------======+++++++=::-::::-==*#+#%%%-:                            ",
        "     ............::==++++++=++*####**++++*#####%%%%%%%%%@%%#:........:.                   ",
        " ..............::::==*####****###%@@@@@@@@@@@@@@@@@@@@@@%%%=..............                ",
        "...............:=::==+############%@@@@@@@@@@@@@@@@@@@@@%%*:...............               ",
        "...............:=-:==+*############%%@@%%@%%@@@@@@@@@@@%%*:....................    ....   ",
        "................:--==+*########%%%%%%%%@@@@@@@@@@@@@@@@%#:........................ .......  ",
        ".................:-=++*####%%%%%%@@@@%@@@@@@@@@@@@@@@@%=.......................... ....... ",
        "..................:-++*####%%%%%%@@@@@@@@@@@@@@@@@@@%*:............................. ..... ",
        "....................:=**##%%%%%%@@@@@@@@@@@@@@@@@@%+:.....................................  ",
        "......................:=+##%%%%%%@@@@@@@@@@@@@%#=:................................... ....  ",
        "..........................::-=+#####%%%##*=-::............................................  ",
        "................................................................................. ........  ",
        "...................................................................................  .....  ",
    ]
    ascii_lines = [esc(l) for l in ascii_raw]

    # ── Info panel ────────────────────────────────────────────────────────────
    la = stats['lines_added']
    ld = stats['lines_deleted']
    lt = stats['lines_total']

    info_lines = []
    info_lines.append(("header",    "manuel@ospina"))
    info_lines.append(("separator", "─" * 40))
    for line in ABOUT:
        info_lines.append(("about", esc(line)))
    info_lines.append(("blank", ""))
    info_lines.append(("separator", "─" * 40))
    info_lines.append(("kv", ("Role",     esc(ROLE))))
    info_lines.append(("kv", ("Location", esc(LOCATION))))
    info_lines.append(("kv", ("OS",       esc(OS_INFO))))
    info_lines.append(("kv", ("IDE",      esc(IDE_INFO))))
    info_lines.append(("kv", ("Focus",    esc(FOCUS))))
    info_lines.append(("blank", ""))
    for cat, techs in STACK.items():
        info_lines.append(("kv", (f"Stack.{cat}", esc(techs))))
    info_lines.append(("blank", ""))
    for label, value in HOBBIES:
        if label == "":
            info_lines.append(("continuation", esc(value)))
        else:
            info_lines.append(("kv", (esc(label), esc(value))))
    info_lines.append(("blank", ""))
    info_lines.append(("section",   "Contact"))
    info_lines.append(("separator", "─" * 40))
    for label, value in CONTACT:
        info_lines.append(("kv", (esc(label), esc(value))))
    info_lines.append(("blank", ""))
    info_lines.append(("section",   "GitHub Stats"))
    info_lines.append(("separator", "─" * 40))
    info_lines.append(("stat2", (f"Repos: {fmt(stats['repos'])}", f"Stars: {fmt(stats['stars'])}")))
    info_lines.append(("stat2", (f"Commits: {fmt(stats['commits'])}", f"Followers: {fmt(stats['followers'])}")))
    info_lines.append(("lines", (f"Lines of Code: {fmt(lt)}", f"+{fmt(la)}", f"-{fmt(ld)}")))

    # ── Dimensiones dinámicas ─────────────────────────────────────────────────
    ASCII_FONT   = 6.5
    ASCII_LINE_H = 8.8
    INFO_FONT    = 12.5
    INFO_LINE_H  = 20.0

    n_ascii  = len(ascii_lines)
    ASCII_H  = n_ascii * ASCII_LINE_H

    info_h = 0.0
    for item in info_lines:
        k = item[0]
        if k == "blank":          info_h += INFO_LINE_H * 0.55
        elif k == "header":       info_h += INFO_LINE_H * 1.4
        elif k == "section":      info_h += INFO_LINE_H * 0.9
        elif k == "about":        info_h += INFO_LINE_H * 0.95
        elif k == "continuation": info_h += INFO_LINE_H * 0.9
        else:                     info_h += INFO_LINE_H

    PAD         = 20
    ASCII_COL_W = 390
    INFO_X      = ASCII_COL_W + PAD + 10
    DIVIDER     = ASCII_COL_W + PAD // 2
    W           = INFO_X + 560
    H           = int(max(ASCII_H, info_h) + PAD * 5)

    MONO        = "JetBrains Mono, Fira Code, Consolas, monospace"
    ASCII_COLOR = "#5bafd6"

    BG          = "#0d1117"
    BORDER      = "#21262d"
    ACCENT      = "#58a6ff"
    TEXT_DIM    = "#8b949e"
    TEXT_MAIN   = "#c9d1d9"
    TEXT_BRIGHT = "#ffffff"
    TEXT_ABOUT  = "#a8d8ea"
    GREEN       = "#3fb950"
    ORANGE      = "#d29922"
    RED         = "#f85149"

    p = []

    p.append(
        '<defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#161b22"/>'
        '<stop offset="100%" stop-color="#0d1117"/>'
        '</linearGradient>'
        f'<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.8"/>'
        f'<stop offset="100%" stop-color="{GREEN}" stop-opacity="0.3"/>'
        '</linearGradient>'
        '<filter id="glow">'
        '<feGaussianBlur stdDeviation="2.5" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
        '</defs>'
    )

    p.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    p.append(f'<rect width="{W}" height="{H}" rx="14" fill="none" stroke="url(#bd)" stroke-width="1.5"/>')
    p.append(f'<line x1="{DIVIDER}" y1="{PAD}" x2="{DIVIDER}" y2="{H-PAD}" stroke="{BORDER}" stroke-width="1"/>')

    # ── ASCII centrado verticalmente ──────────────────────────────────────────
    ascii_y0 = (H - ASCII_H) / 2.0 + ASCII_LINE_H
    for i, line in enumerate(ascii_lines):
        y = ascii_y0 + i * ASCII_LINE_H
        p.append(
            f'<text x="{PAD}" y="{y:.1f}" font-family="{MONO}" '
            f'font-size="{ASCII_FONT}" fill="{ASCII_COLOR}" '
            f'xml:space="preserve">{line}</text>'
        )

    # ── Info panel ────────────────────────────────────────────────────────────
    y = float(PAD) + 18.0
    for item in info_lines:
        k = item[0]

        if k == "blank":
            y += INFO_LINE_H * 0.55

        elif k == "header":
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="17" '
                     f'font-weight="bold" fill="{TEXT_BRIGHT}" filter="url(#glow)">{item[1]}</text>')
            y += INFO_LINE_H * 1.4

        elif k == "separator":
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{BORDER}">{item[1]}</text>')
            y += INFO_LINE_H

        elif k == "section":
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{TEXT_DIM}">&#x2500; {item[1]}</text>')
            y += INFO_LINE_H * 0.9

        elif k == "about":
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="11.5" '
                     f'fill="{TEXT_ABOUT}" opacity="0.85" font-style="italic">{item[1]}</text>')
            y += INFO_LINE_H * 0.95

        elif k == "continuation":
            p.append(f'<text x="{INFO_X + 14}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{TEXT_MAIN}" opacity="0.8">{item[1]}</text>')
            y += INFO_LINE_H * 0.9

        elif k == "kv":
            label, value = item[1]
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{ACCENT}">{label}:</text>')
            lw = len(label) * 7.4 + 14
            p.append(f'<text x="{INFO_X + lw:.0f}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{TEXT_MAIN}">{value}</text>')
            y += INFO_LINE_H

        elif k == "stat2":
            left, right = item[1]
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{GREEN}">{left}</text>')
            p.append(f'<text x="{INFO_X + 240}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{GREEN}">{right}</text>')
            y += INFO_LINE_H

        elif k == "lines":
            total_txt, added_txt, deleted_txt = item[1]
            base_w = len(total_txt) * 7.4 + 26
            add_w  = len(added_txt) * 7.4 + 8
            del_w  = len(deleted_txt) * 7.4 + 20
            p.append(f'<text x="{INFO_X}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{GREEN}">{total_txt}  (</text>')
            p.append(f'<text x="{INFO_X + base_w:.0f}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{GREEN}">{added_txt}</text>')
            p.append(f'<text x="{INFO_X + base_w + add_w:.0f}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{RED}">  {deleted_txt}</text>')
            p.append(f'<text x="{INFO_X + base_w + add_w + del_w:.0f}" y="{y:.1f}" font-family="{MONO}" font-size="{INFO_FONT}" '
                     f'fill="{GREEN}"> )</text>')
            y += INFO_LINE_H

    # ── Barra decorativa ──────────────────────────────────────────────────────
    palette = [ACCENT, GREEN, ORANGE, "#bc8cff", "#ff7b72", "#79c0ff"]
    bw = (W - PAD * 2) // len(palette)
    by = H - 12
    for i, c in enumerate(palette):
        p.append(f'<rect x="{PAD + i*bw}" y="{by}" width="{bw}" height="4" rx="2" fill="{c}" opacity="0.75"/>')

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        + "\n".join(p) + "\n</svg>"
    )


if __name__ == "__main__":
    token = os.environ.get("GH_TOKEN", "")
    print("Fetching GitHub stats...")
    stats = fetch_github_stats(USERNAME, token)
    print("Stats:", stats)

    svg = make_svg(stats)

    try:
        ET.fromstring(svg)
        print("XML valido")
    except ET.ParseError as e:
        print("XML ERROR:", e)

    with open("profile.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    size_kb = len(svg) // 1024
    print("Listo: profile.svg (" + str(size_kb) + " KB)")
