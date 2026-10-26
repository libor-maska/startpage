# Vypíše první 3 (POCET_ZPRAV) zprávy z RSS feedu novinky.cz
import requests
import feedparser


RSS_URL = "https://www.novinky.cz/rss"
TIMEOUT = 10
POCET_ZPRAV = 3

def stahni_zpravy(url):
    """Stáhne RSS z dané adresy a vrátí seznam článků."""
    odpoved = requests.get(url, timeout=TIMEOUT)
    odpoved.raise_for_status()
    feed = feedparser.parse(odpoved.content)

    return feed.entries


def main():
    zpravy = stahni_zpravy(RSS_URL)

    # Vypíše určený počet zpráv
    for clanek in zpravy[:POCET_ZPRAV]:
        print(clanek.title)
        print(f"    {clanek.link}")


if __name__ == "__main__":
    main()