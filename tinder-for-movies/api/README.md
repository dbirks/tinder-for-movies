# Tinder for Movies API

## Development Setup

### Prerequisites
- Python 3.12 or higher
- `uv` package manager

### Environment Setup
1. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv sync
```

### Database Setup

The project uses SQLite with SQLModel and Alembic for database management.

#### Database Structure
- `User`: Stores user information
- `Movie`: Stores movie details
- `Swipe`: Tracks user likes/dislikes
- `WatchlistItem`: Stores user watchlists

#### Common Alembic Commands

1. Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

2. Apply pending migrations:
```bash
alembic upgrade head
```

3. Rollback last migration:
```bash
alembic downgrade -1
```

4. View migration history:
```bash
alembic history
```

5. View current migration version:
```bash
alembic current
```

#### Database Location
The SQLite database is stored at `./data/app.db`. Make sure the `data` directory exists:
```bash
mkdir -p data
```

#### Seeding the Database
To seed the database with initial data:
```bash
python -m app.seed
```

### Running the Application
```bash
uvicorn app.main:app --reload
```

## Project Structure
```
api/
├── alembic.ini           # Alembic configuration
├── migrations/           # Database migrations
│   ├── versions/        # Migration files
│   ├── env.py          # Migration environment
│   └── script.py.mako  # Migration template
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application
│   ├── models.py       # SQLModel models
│   ├── db.py          # Database configuration
│   └── seed.py        # Database seeding script
├── data/               # SQLite database directory
│   └── app.db         # SQLite database file
└── pyproject.toml     # Project configuration
```

## Database Models

### User
- `id`: Primary key
- `name`: User's name
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

### Movie
- `id`: Primary key
- `tmdb_id`: TMDb API ID
- `title`: Movie title
- `overview`: Movie description
- `poster_url`: Movie poster URL
- `release_year`: Year of release
- `genres_json`: JSON-encoded array of genres

### Swipe
- `id`: Primary key
- `user_id`: Foreign key to User
- `movie_id`: Foreign key to Movie
- `action`: "like" or "dislike"
- `timestamp`: Swipe timestamp

### WatchlistItem
- `id`: Primary key
- `user_id`: Foreign key to User
- `movie_id`: Foreign key to Movie
- `timestamp`: Addition timestamp 