"""Vypíše nejnovější zprávy z RSS feedů oblíbených webů."""
import requests
import feedparser

ZDROJE = {
    "Novinky.cz": "https://www.novinky.cz/rss",
    "Seznam Zprávy": "https://www.seznamzpravy.cz/rss",
    "Sport.cz": "https://www.sport.cz/rss",
    "Rozhlas": "https://www.irozhlas.cz/rss/irozhlas",
    "Rozbitý web": "https://www.novinky.cz/rss-neexistuje",
}
TIMEOUT = 10
POCET_ZPRAV = 4


def stahni_zpravy(url):
    """Stáhne RSS z dané adresy a vrátí seznam článků."""
    odpoved = requests.get(url, timeout=TIMEOUT)
    odpoved.raise_for_status()
    feed = feedparser.parse(odpoved.content)

    return feed.entries


def main():
    # Vypíše určený počet zpráv
    for web, url in ZDROJE.items():
        print(f"=== {web} ===")
        try:
            zpravy = stahni_zpravy(url)
        except requests.RequestException as chyba:
            print(f"Nedostupné ({type(chyba).__name__})")
            print()
            continue
        for clanek in zpravy[:POCET_ZPRAV]:
            print(clanek.title)
        print()


if __name__ == "__main__":
    main()