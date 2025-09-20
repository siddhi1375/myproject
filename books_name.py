import requests, csv, json

url = "https://openlibrary.org/search.json"

# open CSV file
headers = ["author_name", "first_publish_year", "title"]
for pag in range(1,10):
    response = requests.get(url, params={"q": "travelling", "page": pag})
    raw_data = response.json()
    data = raw_data['docs']
    for i in range(len(data)):
        books = data[i]
        req_data = {key: value for key, value in books.items() if key in headers}
        print(req_data)

        with open("books_info.csv", 'a', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerow(req_data)


print("Task Complete Successfully")
