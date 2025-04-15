import requests
from bs4 import BeautifulSoup
import csv
import re  # For using regex to filter out non-numeric characters

origin_url = "https://deuscustoms.eu/collections/all?page={x}"

def get_total_pages(url):
    response = requests.get(url.format(x=1))  # Load the first page to find the pagination
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the pagination <ol> and get the second-to-last <li> for the page count
    pagination = soup.find("ol", class_="pagination")
    if not pagination:
        return 1  # If no pagination is found, assume only one page

    # Find all <li> elements, get the second-to-last, and extract the text from <a> inside
    try:
        last_page_li = pagination.find_all("li")[-2]
        last_page_text = last_page_li.find("a", class_="pagination__page-link").get_text(strip=True)

        # Use regex to extract only numbers
        total_pages = int(re.search(r'\d+', last_page_text).group())
        return total_pages
    except (AttributeError, ValueError, IndexError):
        print("Error: Could not determine the total number of pages.")
        return 1  # Fallback to 1 page if extraction fails

def get_product_urls():
    total_pages = get_total_pages(origin_url)
    print(f"Total pages found: {total_pages}")
    
    product_links = []

    for page_num in range(1, total_pages + 1):
        print(f"Scraping page {page_num}...")
        response = requests.get(origin_url.format(x=page_num))
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all <a> elements under <div class="product-card__image">
        page_links = [
            a["href"] for a in soup.select("div.product-card__image a")
        ]
        
        # Convert to absolute URLs
        page_links = [requests.compat.urljoin(origin_url, link) for link in page_links]
        product_links.extend(page_links)

    # Write URLs to a CSV file
    with open("product_urls.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["product_url"])  # CSV header
        for link in product_links:
            writer.writerow([link])

    print(f"Saved {len(product_links)} product URLs to product_urls.csv")

# Run the function to scrape all product URLs
get_product_urls()
