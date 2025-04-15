import csv
import requests
from bs4 import BeautifulSoup

def scrape_product_data():
    # Read URLs from product_urls.csv
    with open("product_urls.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        product_data = []

        for row in reader:
            url = row["product_url"]

            # Log the URL being scraped
            print(f"Scraping product: {url}")

            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract product title
            title_tag = soup.find("h1", class_="h2 product__title")
            product_title = title_tag.get_text(strip=True) if title_tag else "N/A"

            # Extract product price
            price_tag = soup.find("span", class_="product__price")
            product_price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Extract product description
            desc_tag = soup.find("div", class_="product__description rte")
            product_description = desc_tag.get_text(strip=True) if desc_tag else "N/A"

            # Add product data to the list
            product_data.append({
                "product_url": url,
                "product_title": product_title,
                "product_price": product_price,
                "product_description": product_description,
            })

    # Write product data to CSV
    with open("product_data.csv", "w", newline="") as csvfile:
        fieldnames = ["product_url", "product_title", "product_price", "product_description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)

    print("Scraping complete. Saved product details to product_data.csv")

# Call the function to start scraping product data
scrape_product_data()
