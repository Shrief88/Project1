import os

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
Review=db.Table('review',
    db.Column('user_id',db.Integer, db.ForeignKey("users.id"), nullable=True), 
    db.Column('book_id',db.Integer, db.ForeignKey("books.id"), nullable=True), 
    db.Column('body',db.String(100), nullable=False),
    db.Column('rating',db.Float, nullable=False)
)
     


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True) 
    isbn = db.Column(db.String(10),unique=True,nullable=False)
    title = db.Column(db.String(100),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey("authors.id"),nullable=False)  #one to many relation between books and authors
    year = db.Column(db.String(4), nullable=False)
    users= db.relationship('User', secondary='add_book', backref='books')
    reviews = db.relationship('User', secondary='review', backref='reviews')


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)  
    password = db.Column(db.String(100), nullable=False) 
    



    





    