import os, json, requests 


from models import *
from flask import Flask, session, redirect, render_template, request, jsonify,url_for
from flask_session import Session
from sqlalchemy import or_
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash


# Configure session to use filesystem
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'redsfsfsfsfis'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ijionxqqbadvfc:94f779624969db0fd8bcd094b485e4bd5197d0e9f24f8dbabcdd6a9dcafc944c@ec2-52-87-135-240.compute-1.amazonaws.com:5432/depl9ide9dik0r"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
Session(app)


@app.route("/")
def index():
    return redirect("/login")

@app.route("/login" , methods=["GET", "POST"])
def login():
    if request.method == "POST" :
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password :
            return render_template("error.html", message="must provide all required information")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return render_template("error.html", message="You Must sign up First")  
    
        if not check_password_hash(user.password,password):
            return render_template("error.html", message="Password is incorrect")
        session['user_id'] = user.id
        session["user_name"] = user.username
        return redirect("/search" )
    else :
        if 'user_id' in session:
            return redirect("/search" )
        return render_template("login.html")


@app.route("/register" , methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST" :
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confrim_password")
        if not username or not password or not confirm_password :
            return render_template("error.html", message="must provide all required information")
        if password != confirm_password :
             return render_template("error.html", message="Please insert the same password in confirm password cell")
        check = User.query.filter_by(username=username).count()     
        if check != 0 :
            return render_template("error.html", message="Username is taken")

        hashedPassword = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8) 
        user = User(username=username , password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
    else:
         return render_template("register.html")    

@app.route("/search" , methods=["GET", "POST"])
def search():
    if request.method == "POST" :
        search_input = request.form.get("search_input")
        if not search_input:
            return render_template("error.html", message="must provide all required information")
        search_input = search_input.title() #Capitalize all words of input for search    
        book = Book.query.filter(or_(Book.isbn==search_input,Book.title==search_input)).first()
        author = Author.query.filter_by(name=search_input).first()

        if book is None and author is None:
            return render_template("error.html", message="we can't find books with that description.")

        if author is None and book is not None:
            return redirect(url_for('book',book_isbn = book.isbn))

        if author is not None and book is None:
            books = author.books
            return render_template("results.html", books=books , search_input=search_input) 

        ##if author is not None and book is not None: 
        ##    books = author.books
        ##    books.append()    


    else:
        if 'user_id' in session:
            return render_template("index.html" , user_name = session["user_name"])
        return redirect("/login")      

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/search/<book_isbn>" ,  methods=["GET", "POST"])
def book(book_isbn):
    if  'user_id' not in session:
            return render_template("index.html")
    book = Book.query.filter_by(isbn=book_isbn).first()
    
    if book is None:
        return render_template("error.html", message="No such book.")
    if request.method == "POST" :
        user_id = session['user_id']
        book_id = book[0].id
        reviews = db.execute("SELECT * FROM reviews WHERE user_id = :user_id and book_id= :book_id" , {"user_id": user_id,"book_id":book_id}).rowcount
        if reviews != 0 :
           return render_template("error.html", message="you have reviewed this book before") 
        else:    
          body = request.form.get("review")
          rating = request.form.get("rating")
          if not body or not rating :
                return render_template("error.html", message="must provide all required information")
          db.execute("INSERT INTO reviews(body,user_id,book_id,rating)VALUES(:body,:user_id,:book_id,:rating)",{"body":body,"user_id":user_id,"book_id":book_id,"rating":rating}) 
          db.commit()
          return redirect(url_for('book',book_isbn = book_isbn))
    KEY = "fX6308bR8BeCJQH44PoRg"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": book_isbn})
    res = res.json()
    res = res['books'][0]

    reviews = Review.query.filter_by(book_id = book.id).all()
    return render_template("book.html", book=book , res=res , reviews=reviews , user_name=session["user_name"], user_id =session['user_id'])


app.run(debug=True)
