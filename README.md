# Gach Rud Ina Áit 🍴

*Irish for "Everything in its Place"*

A personal recipe book web application built with Flask and PostgreSQL. Store, organise, and discover your favourite recipes — from quick weeknight dinners to special occasions.

---

## Live Demo

🌐 [https://recipe-book1-gcx7.onrender.com](https://recipe-book1-gcx7.onrender.com)

---

## Features

- **Browse Recipes** — view all recipes in a responsive card grid
- **Search & Filter** — search by keyword or filter by category
- **Recipe Detail** — view full ingredients, method steps, and metadata
- **Add & Edit** — create new recipes or update existing ones
- **Delete** — remove recipes with a confirmation prompt
- **Favourites** — save and manage your favourite recipes
- **Flash Messages** — success and error feedback on all actions
- **Fully Responsive** — mobile friendly with a hamburger nav

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | PostgreSQL (Render), SQLite (local dev) |
| ORM | Flask-SQLAlchemy |
| Templating | Jinja2 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Icons | Font Awesome 6 |
| Fonts | Google Fonts (Playfair Display, Lato) |
| Hosting | Render.com |

---

## Project Structure

```
gach-rud-ina-ait-fein/
│
├── app.py              # Flask app, routes, and CRUD logic
├── models.py           # SQLAlchemy database models
├── requirements.txt    # Python dependencies
├── Procfile            # Gunicorn start command for Render
├── .env                # Local environment variables (not committed)
├── README.md
│
├── templates/
│   ├── base.html       # Base template (nav, head, footer)
│   ├── index.html      # Home page
│   ├── recipes.html    # All recipes with search and filters
│   ├── recipe_detail.html  # Single recipe view
│   ├── add_recipe.html # Add and edit recipe form
│   └── favourites.html # Saved favourites
│
└── static/
    ├── css/
    │   └── style.css   # Main stylesheet
    ├── js/
    │   └── script.js   # JavaScript functionality
    └── favicon.ico
```

---

## Local Setup

Follow these steps to run the project on your machine.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/gach-rud-ina-ait-fein.git
cd gach-rud-ina-ait-fein
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the root folder

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///dev.db
```

> For local development the app uses SQLite so no PostgreSQL installation is needed.

### 5. Run the app

```bash
python3 app.py
```

Open your browser and go to **http://127.0.0.1:5000**

---

## Deployment on Render

The app is hosted on [Render.com](https://render.com). To deploy your own instance:

### 1. Push your code to GitHub

### 2. Create a Web Service on Render
- Connect your GitHub repository
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### 3. Create a PostgreSQL database on Render
- Click **New → PostgreSQL**
- Use the same region as your web service

### 4. Add environment variables to the Web Service
- `DATABASE_URL` — Internal Database URL from your Render PostgreSQL service
- `SECRET_KEY` — any random secret string

### 5. Deploy
Render will automatically deploy on every push to your GitHub repository.

---

## Database Schema

The app uses a single `recipes` table with the following columns:

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key, auto-incremented |
| title | String(200) | Recipe name |
| category | String(100) | e.g. Pasta, Curry, Salad |
| difficulty | String(20) | Easy, Medium, or Hard |
| cook_time | String(50) | e.g. 30 min |
| servings | Integer | Number of servings |
| description | Text | Short description of the dish |
| ingredients | JSON | List of ingredient strings |
| steps | JSON | List of method step strings |
| tags | JSON | List of tag strings |
| colour | String(20) | Hex colour for card banner |
| is_favourite | Boolean | Whether saved as a favourite |

---

## CRUD Operations

| Operation | Route | Method |
|---|---|---|
| Create | `/add` | POST |
| Read (all) | `/recipes` | GET |
| Read (one) | `/recipe/<id>` | GET |
| Update | `/recipe/<id>/edit` | POST |
| Delete | `/recipe/<id>/delete` | POST |
| Toggle Favourite | `/recipe/<id>/favourite` | POST |

---

## JavaScript Features

- Mobile hamburger nav toggle
- Flash message auto-dismiss after 4 seconds
- Live search filtering without page reload
- Delete confirmation prompt
- Ingredient checkbox toggle on recipe detail page
- Smooth scroll for anchor links
- Character counter on description field

---

## Dependencies

```
Flask==3.1.3
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.12
python-dotenv==1.2.2
gunicorn==26.0.0
SQLAlchemy==2.0.49
```

---

## Author

Colin Keogh — UCD Professional Academy Databases Assignment