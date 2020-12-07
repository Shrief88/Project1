import csv

from flask import Flask,request,render_template
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ijionxqqbadvfc:94f779624969db0fd8bcd094b485e4bd5197d0e9f24f8dbabcdd6a9dcafc944c@ec2-52-87-135-240.compute-1.amazonaws.com:5432/depl9ide9dik0r"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
   f = open("books.csv")
   reader = csv.reader(f)
   next(reader)
   for isbn, title, author,year in reader:
      check = Author.query.filter_by(name=author).count()
      if  check == 0 :
         author_obj = Author(name=author)
         db.session.add(author_obj)
         db.session.commit() 
      author_id = Author.query.filter_by(name=author).first()
      book = Book(isbn=isbn ,title=title , author = author_id , year=year)
      db.session.add(book)
   db.session.commit()   
      

if __name__ == "__main__":
   with app.app_context():
      main()
