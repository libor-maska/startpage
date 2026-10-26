"""Vypíše nejnovější zprávy z RSS feedů oblíbených webů do HTML."""

import html
from pathlib import Path
import requests
import feedparser

VYSTUP = Path(__file__).parent / "startpage.html"
ZDROJE = {
    "Novinky.cz": "https://www.novinky.cz/rss",
    "Seznam Zprávy": "https://www.seznamzpravy.cz/rss",
    "Sport.cz": "https://www.sport.cz/rss",
    "Rozhlas": "https://www.irozhlas.cz/rss/irozhlas",
}
TIMEOUT = 10
POCET_ZPRAV = 4

def html_sekce(web, zpravy):
    """Vrátí HTML jedné sekce: nadpis webu a seznam odkazů na články"""
    polozky = []
    for clanek in zpravy[:POCET_ZPRAV]:
        titulek = html.escape(clanek.title)
        odkaz = html.escape(clanek.link)
        polozky.append(f'<li><a href="{odkaz}">{titulek}</a></li>')

    seznam = "".join(polozky)
    return f"<h2>{html.escape(web)}</h2><ul>{seznam}</ul>"


def stahni_zpravy(url):
    """Stáhne RSS z dané adresy a vrátí seznam článků."""
    odpoved = requests.get(url, timeout=TIMEOUT)
    odpoved.raise_for_status()
    feed = feedparser.parse(odpoved.content)

    return feed.entries


def main():
    sekce = []
    for web, url in ZDROJE.items():
        try:
            zpravy = stahni_zpravy(url)
        except requests.RequestException as chyba:
            sekce.append(f"<h2>{html.escape(web)}</h2>\n" f"<p>Nedostupné ({type(chyba).__name__})</p>")
            continue
        sekce.append(html_sekce(web, zpravy))

    stranka  = f"""<!DOCTYPE html>
            <html lang="cs">
            <head>
            <meta charset="utf-8>
            <title>Startpage</title>
            </head>
            <body>
            <h1>Startpage</h1>
            {'\n'.join(sekce)}
            </body>
            </html>
            """
    VYSTUP.write_text(stranka, encoding="utf-8")
    print(f"Hotovo: {VYSTUP.as_uri()}")


if __name__ == "__main__":
    main()