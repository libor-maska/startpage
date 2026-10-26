""" Vypíše první (POCET_ZPRAV) zprávy z RSS feedu webů """
import requests
import feedparser

ZDROJE = {
    "Novinky.cz": "https://www.novinky.cz/rss",
    "Seznam Zprávy": "https://www.seznamzpravy.cz/rss",
    "Sport.cz": "https://www.sport.cz/rss",
    "Rozhlas": "https://www.irozhlas.cz/rss/irozhlas"
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
        zpravy = stahni_zpravy(url)
        for clanek in zpravy[:POCET_ZPRAV]:
            print(clanek.title)
        print()


if __name__ == "__main__":
    main()