import requests
KEY = "AIzaSyCRyv79bp9XdhdY4fW46dKAwwWZLznorIA"
isbn = "1451648537"
link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
link = link+isbn;
print(link)


res = requests.get(link)
res = res.json()
res = res['items'][0]

print(res['volumeInfo']['averageRating'])