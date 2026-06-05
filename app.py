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
 
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)
 
 
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
   
    if request.method == 'POST':
        # Pull form data
        title       = request.form.get('title', '').strip()
        category    = request.form.get('category', '').strip()
        difficulty  = request.form.get('difficulty', '').strip()
        cook_time   = request.form.get('cook_time', '').strip()
        servings    = request.form.get('servings', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        steps       = request.form.get('steps', '').strip()
        tags        = request.form.get('tags', '').strip()
 
        # Basic validation
        if not title or not description or not ingredients or not steps:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('add_recipe'))
 
        # Create new recipe object
        new_recipe = Recipe(
            title       = title,
            category    = category,
            difficulty  = difficulty,
            cook_time   = cook_time,
            servings    = int(servings) if servings.isdigit() else 1,
            description = description,
            # Split textarea lines into lists
            ingredients = [i.strip() for i in ingredients.splitlines() if i.strip()],
            steps       = [s.strip() for s in steps.splitlines() if s.strip()],
            tags        = [t.strip() for t in tags.split(',') if t.strip()],
            colour      = '#f5e6c8'  # default card colour
        )
 
        db.session.add(new_recipe)
        db.session.commit()
 
        flash(f'"{title}" has been added to your collection!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=new_recipe.id))
 
    return render_template('add_recipe.html', recipe=None)
 
 
@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
 
    if request.method == 'POST':
        recipe.title       = request.form.get('title', '').strip()
        recipe.category    = request.form.get('category', '').strip()
        recipe.difficulty  = request.form.get('difficulty', '').strip()
        recipe.cook_time   = request.form.get('cook_time', '').strip()
        recipe.description = request.form.get('description', '').strip()
 
        servings = request.form.get('servings', '').strip()
        recipe.servings = int(servings) if servings.isdigit() else recipe.servings
 
        ingredients = request.form.get('ingredients', '').strip()
        steps       = request.form.get('steps', '').strip()
        tags        = request.form.get('tags', '').strip()
 
        recipe.ingredients = [i.strip() for i in ingredients.splitlines() if i.strip()]
        recipe.steps       = [s.strip() for s in steps.splitlines() if s.strip()]
        recipe.tags        = [t.strip() for t in tags.split(',') if t.strip()]
 
        db.session.commit()

        flash(f'"{recipe.title}" has been updated.', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
 
    return render_template('add_recipe.html', recipe=recipe)
 
 
@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    Delete a recipe — POST only (no GET) to prevent
    accidental deletion via a direct URL visit.
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    title  = recipe.title
 
    db.session.delete(recipe)
    db.session.commit()
 
    flash(f'"{title}" has been deleted.', 'success')
    return redirect(url_for('recipes'))
 
 
@app.route('/recipe/<int:recipe_id>/favourite', methods=['POST'])
def toggle_favourite(recipe_id):
    """
    Toggles the is_favourite flag on a recipe.
    Redirects back to whichever page the user came from.
    """
    recipe             = Recipe.query.get_or_404(recipe_id)
    recipe.is_favourite = not recipe.is_favourite
    db.session.commit()
 
    return redirect(request.referrer or url_for('recipes'))
 
 
@app.route('/favourites')
def favourites():
    """
    Favourites page — displays all recipes marked
    as favourite.
    """
    favourite_recipes = Recipe.query.filter_by(is_favourite=True).order_by(Recipe.title).all()
    return render_template('favourites.html', favourites=favourite_recipes)
 
 
@app.route('/about')
def about():
    """
    About page — static informational page about
    the app and its tech stack.
    """
    return render_template('about.html')
 
 
# ------------------------------------------------
# RUN
# ------------------------------------------------
 
if __name__ == '__main__':
    app.run(debug=True)