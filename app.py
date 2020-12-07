import os, json, requests


from flask import Flask, session, redirect, render_template, request, jsonify,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
 #  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
engine = create_engine("postgres://ijionxqqbadvfc:94f779624969db0fd8bcd094b485e4bd5197d0e9f24f8dbabcdd6a9dcafc944c@ec2-52-87-135-240.compute-1.amazonaws.com:5432/depl9ide9dik0r")
db = scoped_session(sessionmaker(bind=engine))

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
        check =  db.execute("SELECT COUNT(*) FROM users WHERE username = :username",{"username": username})
        if check == 0:
            return render_template("error.html", message="You Must sign up First")   
        user = db.execute("SELECT * FROM users WHERE email = :email",{"email": email})
        user =user.fetchall()
        if user[0].password!=  password:
            return render_template("error.html", message="Password is incorrect")
        session['user_id'] = user[0].id
        session["user_name"] = user[0].name
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
        if not name or not email or not password :
            return render_template("error.html", message="must provide all required information")
        if password != confirm_password :
             return render_template("error.html", message="Please insert the same password in confirm password cell")
        check =  db.execute("SELECT * FROM users WHERE username = :username",{"username": username}).rowcount
        if check != 0 :
            return render_template("error.html", message="Username is taken")
        db.execute("INSERT INTO users (username,password)VALUES(:username,:password)",{"name":username,"password":password}) 
        db.commit()
        return render_template("login.html")
    else:
         return render_template("register.html")    

@app.route("/search" , methods=["GET", "POST"])
def search():
    if request.method == "POST" :
        book = request.form.get("book")
        if not book:
            return render_template("error.html", message="must provide all required information")
        book = book.title() #Capitalize all words of input for search    
        books = db.execute("SELECT * FROM books where isbn=:book or title=:book or author=:book",{"book":book})
        if books.rowcount == 0:
            return render_template("error.html", message="we can't find books with that description.")
        books=books.fetchall()    
        return render_template("results.html", books=books , book=book)    
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
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn})
    if book.rowcount == 0:
        return render_template("error.html", message="No such book.")
    book = book.fetchall()
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
    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book[0].id}).fetchall()
    return render_template("book.html", book=book , res=res , reviews=reviews , user_name=session["user_name"], user_id =session['user_id'])


app.run(debug=True)
