import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, Recipe
 
# ------------------------------------------------
# CONFIGURATION
# ------------------------------------------------
 
# Load environment variables from .env file
load_dotenv()
 
app = Flask(__name__)
 
# Secret key for session/flash messages
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
 
# PostgreSQL database connection
# On Render this is set as an environment variable (DATABASE_URL)
# Locally it reads from your .env file
app.config['SQLALCHEMY_DATABASE_URI']        = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialise the database with the app
db.init_app(app)
 
# Create all tables on startup if they don't exist yet
with app.app_context():
    db.create_all()
 
 
# ------------------------------------------------
# ROUTES
# ------------------------------------------------
 
@app.route('/')
def index():
    """
    Home page — displays a stats strip and the
    three most recently added recipes.
    """
    recent_recipes   = Recipe.query.order_by(Recipe.id.desc()).limit(3).all()
    total_recipes    = Recipe.query.count()
    total_categories = db.session.query(Recipe.category).distinct().count()
    total_favourites = Recipe.query.filter_by(is_favourite=True).count()
 
    return render_template(
        'index.html',
        recent_recipes   = recent_recipes,
        total_recipes    = total_recipes,
        total_categories = total_categories,
        total_favourites = total_favourites
    )
 
 
@app.route('/recipes')
def recipes():
    """
    Recipes page — displays all recipes with optional
    filtering by category and search query.
    """
    query    = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
 
    # Start with all recipes
    recipes_query = Recipe.query
 
    # Filter by search query if provided
    if query:
        recipes_query = recipes_query.filter(
            Recipe.title.ilike(f'%{query}%') |
            Recipe.description.ilike(f'%{query}%')
        )
 
    # Filter by category if provided
    if category:
        recipes_query = recipes_query.filter_by(category=category)
 
    all_recipes = recipes_query.order_by(Recipe.title).all()
 
    # Get distinct categories for the filter pills
    categories = [r[0] for r in db.session.query(Recipe.category).distinct().order_by(Recipe.category).all()]
 
    return render_template(
        'recipes.html',
        recipes    = all_recipes,
        categories = categories
    )
 