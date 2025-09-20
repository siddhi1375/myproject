
import requests
from bs4 import BeautifulSoup


url = "https://www.goodreads.com/list/show/7.Best_Travel_Books"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

books = []

for row in soup.select("tr"):
    title_tag = row.select_one("a.bookTitle")
    author_tag = row.select_one("a.authorName")
    rating_tag = row.select_one("span.minirating")
    
    if title_tag and author_tag:
        title = title_tag.get_text(strip=True)
        author = author_tag.get_text(strip=True)
        link = "https://www.goodreads.com" + title_tag["href"]
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        books.append({
            "title": title,
            "author": author,
            "rating": rating,
            "link": link
        })

for book in books[:10]:
    print(book)


for i  in range (1,10)

gluffy  
 
















































