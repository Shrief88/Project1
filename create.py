from flask import Flask
from models import *
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ijionxqqbadvfc:94f779624969db0fd8bcd094b485e4bd5197d0e9f24f8dbabcdd6a9dcafc944c@ec2-52-87-135-240.compute-1.amazonaws.com:5432/depl9ide9dik0r"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()