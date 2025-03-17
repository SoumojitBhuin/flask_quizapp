from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import yaml

load_dotenv()

app = Flask(__name__)

# Database Configuration
db_path = os.path.join("/tmp", "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Importing Models and Initializing Database
from appfile.models import db
db.init_app(app)

with app.app_context():
    db.create_all()

# Importing Routes
from routes import register_routes
register_routes(app)




if __name__ == '__main__':
    app.run(debug=True)
