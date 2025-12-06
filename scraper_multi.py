print("Test")
import requests
from bs4 import BeautifulSoup
import json
import time

# ---------- SCRAPER INSTANT GAMING ----------
def scrape_instantgaming(url):
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        # Titre
        title_raw = soup.select_one("h1.product-name")
        if not title_raw:
            raise Exception("Titre introuvable")
        title = title_raw.get_text(strip=True)

        # Prix
        price_raw = soup.select_one("span.price-new")
        if not price_raw:
            raise Exception("Prix introuvable")
        price = float(
            price_raw.get_text(strip=True)
            .replace("€", "")
            .replace(",", ".")
            .replace(" ", "")
        )

        # Ancien prix (si dispo)
        old_price = None
        old_price_raw = soup.select_one("span.price-old")
        if old_price_raw:
            old_price = float(
                old_price_raw.get_text(strip=True)
                .replace("€", "")
                .replace(",", ".")
                .replace(" ", "")
            )

        # Image
        img = soup.select_one("img.product-image")
        image_url = img["src"] if img else None

        # Plateforme (ex: PC, PS4, etc.)
        platform = "pc"  # Par défaut

        return {
            "title": title,
            "url": url,
            "source": "Instant Gaming",
            "timestamp": int(time.time() * 1000),
            "price": price,
            "old_price": old_price,
            "platform": platform,
            "type": "game",
            "tags": ["gaming", platform, "key"],
            "image": image_url
        }
    except Exception as e:
        print(f"[ERREUR Instant Gaming] {url} -> {e}")
        return None

# ---------- LISTE DES PRODUITS À SCRAPER ----------
PRODUCT_URLS = [
    "https://www.instant-gaming.com/fr/1000-elden-ring-pc-jeu-steam/",
    "https://www.instant-gaming.com/fr/1001-fifa-23-ps5-jeu-psn/",
    # Ajoute d'autres URLs ici
]

# ---------- ROUTAGE VERS LE BON SCRAPER ----------
def scrape_url(url):
    if "instant-gaming.com" in url:
        return scrape_instantgaming(url)
    else:
        print(f"❌ Aucun scraper pour : {url}")
        return None

# ---------- MAIN ----------
def main():
    deals = []
    for url in PRODUCT_URLS:
        print(f"Scraping : {url}")
        data = scrape_url(url)
        if data:
            deals.append(data)
    # Sauvegarde
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4, ensure_ascii=False)
    print("\n✔ Scraping terminé ! deals.json mis à jour.\n")

if __name__ == "__main__":
    main()
