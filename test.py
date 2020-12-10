import requests
KEY = "fX6308bR8BeCJQH44PoRg"
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": "1416949658"})
print(res)

