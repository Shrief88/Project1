

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Author(db.Model):
    __tablename__="authors"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    books = db.relationship('Book', backref='author')


#many to many relation between books and users
adding_Book = db.Table('add_book',
       db.Column('user_id',db.Integer, db.ForeignKey("users.id") ,nullable=False),
       db.Column('book_id',db.Integer, db.ForeignKey("books.id") ,nullable=False) 
)

#many to many relation between books and users
class Review(db.Model):
    __tablename__="reviews"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"),primary_key=True, nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    rating = db.Column(db.Float,nullable=False)
    book = db.relationship("Book")

    def __init__(self, book, rating , body):
        self.book = book
        self.rating = rating
        self.body = body


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True) 
    isbn = db.Column(db.String(10),unique=True,nullable=False)
    title = db.Column(db.String(100),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey("authors.id"),nullable=False)  #one to many relation between books and authors
    year = db.Column(db.String(4), nullable=False)
    users= db.relationship('User', secondary='add_book', backref='books')



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)  
    password = db.Column(db.String(100), nullable=False) 
    reviews = db.relationship("Review", backref="books")
  
    



    





    