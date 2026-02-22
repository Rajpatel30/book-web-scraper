import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

books_info = []

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 51):
    url = base_url.format(page)
    print(f"Scraping Page {page}...")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in books:
            name_tag = book.find("h3").find("a")
            book_name = name_tag.text.strip()
            book_link = "https://books.toscrape.com/catalogue/" + name_tag["href"]
            price = book.find("p", class_="price_color").text.strip()

            books_info.append({
                "Name": book_name,
                "Price": price,
                "Link": book_link
            })

        time.sleep(1)  # polite scraping

    except Exception as e:
        print(f"Error on page {page}: {e}")

df = pd.DataFrame(books_info)
df.to_csv("Books_Info.csv", index=False)

print("Scraping Completed and Data Saved!")
