import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ijionxqqbadvfc:94f779624969db0fd8bcd094b485e4bd5197d0e9f24f8dbabcdd6a9dcafc944c@ec2-52-87-135-240.compute-1.amazonaws.com:5432/depl9ide9dik0r"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()