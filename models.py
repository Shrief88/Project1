import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True) 
    isbn = db.Column(db.String(10),unique=True,nullable=False)
    title = db.Column(db.String(100),nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey("author_id"),nullable=False)
    year = db.Column(db.String(4), nullable=False)

class Autor(db.Model):
    __tablename__="authors"
    id = db.Column(db.Integer,perimary_key=True)
    name = db.Column(db.String(100),nullable=False)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(100), unique = True, nullable=False)  
    password = db.Column(db.String(100), nullable=False) 

class Checkout(db.Model):
    __tablename__="checkouts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") ,nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id") ,nullable=False)    

class Review(db.Model):
    __tablename__ = "reviews"   
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(100), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=True)   
    rating = db.Column(db.String(1), nullable=False)
