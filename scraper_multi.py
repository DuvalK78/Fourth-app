import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_instantgaming(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Arrête si la requête échoue

        soup = BeautifulSoup(response.text, "html.parser")

        # Titre
        title_element = soup.select_one("h1.product-name")
        if not title_element:
            print("Titre non trouvé")
            return None
        title = title_element.get_text(strip=True)

        # Prix
        price_element = soup.select_one("span.price-new")
        if not price_element:
            print("Prix non trouvé")
            return None
        price = float(price_element.get_text(strip=True).replace("€", "").replace(",", ".").strip())

        # Ancien prix (optionnel)
        old_price = None
        old_price_element = soup.select_one("span.price-old")
        if old_price_element:
            old_price = float(old_price_element.get_text(strip=True).replace("€", "").replace(",", ".").strip())

        # Image
        image_element = soup.select_one("img.product-image")
        image_url = image_element["src"] if image_element else None

        return {
            "title": title,
            "url": url,
            "source": "Instant Gaming",
            "timestamp": int(time.time() * 1000),
            "price": price,
            "old_price": old_price,
            "platform": "pc",
            "type": "game",
            "tags": ["gaming", "pc", "key"],
            "image": image_url
        }
    except Exception as e:
        print(f"Erreur lors du scraping de {url}: {e}")
        return None

# URLs à scraper
PRODUCT_URLS = [
    "https://www.instant-gaming.com/fr/1000-elden-ring-pc-jeu-steam/",
    "https://www.instant-gaming.com/fr/1001-fifa-23-ps5-jeu-psn/",
]

def main():
    deals = []
    for url in PRODUCT_URLS:
        print(f"Scraping: {url}")
        data = scrape_instantgaming(url)
        if data:
            deals.append(data)
    print(f"Offres trouvées: {len(deals)}")

    # Sauvegarde
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=4, ensure_ascii=False)
    print("Fichier deals.json mis à jour.")

if __name__ == "__main__":
    main()
