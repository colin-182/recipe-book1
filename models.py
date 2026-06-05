"""
models.py — Gach Rud Ina Áit
Defines the SQLAlchemy database models for the application.
Each class maps directly to a table in the PostgreSQL database.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialise SQLAlchemy — this instance is imported
# into app.py and bound to the Flask app there
db = SQLAlchemy()


class Recipe(db.Model):
    """
    Represents a single recipe in the database.

    Columns:
        id          -- primary key, auto-incremented
        title       -- name of the recipe (required)
        category    -- e.g. Pasta, Curry, Salad
        difficulty  -- Easy, Medium, or Hard
        cook_time   -- human readable string e.g. '30 min'
        servings    -- number of servings as an integer
        description -- short summary of the dish
        ingredients -- list of ingredient strings (stored as JSON)
        steps       -- list of method step strings (stored as JSON)
        tags        -- list of tag strings e.g. ['Italian', 'Quick']
        colour      -- hex colour string for the card banner
        is_favourite -- whether the recipe is saved as a favourite
    """

    __tablename__ = 'recipes'

    # ------------------------------------------------
    # COLUMNS
    # ------------------------------------------------

    id          = db.Column(db.Integer,     primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(100), nullable=False)
    difficulty  = db.Column(db.String(20),  nullable=False, default='Easy')
    cook_time   = db.Column(db.String(50),  nullable=False)
    servings    = db.Column(db.Integer,     nullable=False, default=2)
    description = db.Column(db.Text,        nullable=False)

    # Lists are stored as JSON arrays in PostgreSQL
    ingredients = db.Column(db.JSON, nullable=False, default=list)
    steps       = db.Column(db.JSON, nullable=False, default=list)
    tags        = db.Column(db.JSON, nullable=False, default=list)

    colour      = db.Column(db.String(20),  nullable=False, default='#f5e6c8')
    is_favourite = db.Column(db.Boolean,    nullable=False, default=False)

    # ------------------------------------------------
    # METHODS
    # ------------------------------------------------

    def __repr__(self):
        """
        String representation of a Recipe object —
        useful when debugging in the terminal.
        """
        return f'<Recipe {self.id}: {self.title}>'

    def to_dict(self):
        """
        Returns the recipe as a plain dictionary.
        Useful if you later want to build a JSON API
        endpoint on top of the app.
        """
        return {
            'id':           self.id,
            'title':        self.title,
            'category':     self.category,
            'difficulty':   self.difficulty,
            'cook_time':    self.cook_time,
            'servings':     self.servings,
            'description':  self.description,
            'ingredients':  self.ingredients,
            'steps':        self.steps,
            'tags':         self.tags,
            'colour':       self.colour,
            'is_favourite': self.is_favourite,
        }