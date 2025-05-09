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

4. Rollback to a specific version:
```bash
alembic downgrade <revision_id>
```

5. View migration history:
```bash
alembic history
```

6. View current migration version:
```bash
alembic current
```

7. View migration details:
```bash
alembic show <revision_id>
```

#### Database Management

1. Reset Database (Development Only):
```bash
# Remove existing database
rm -f data/app.db

# Create fresh migrations
rm -rf migrations/versions/*
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Seed the database
python -m app.seed
```

2. Database Location:
The SQLite database is stored at `./data/app.db`. Make sure the `data` directory exists:
```bash
mkdir -p data
```

3. Seeding the Database:
To seed the database with initial data:
```bash
python -m app.seed
```

Note: The seed script will automatically clear existing data before seeding.

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

## Common Development Tasks

### Adding a New Model
1. Add the model to `app/models.py`
2. Create a new migration:
```bash
alembic revision --autogenerate -m "Add new model"
```
3. Review the generated migration in `migrations/versions/`
4. Apply the migration:
```bash
alembic upgrade head
```

### Modifying an Existing Model
1. Update the model in `app/models.py`
2. Create a new migration:
```bash
alembic revision --autogenerate -m "Modify model"
```
3. Review the generated migration in `migrations/versions/`
4. Apply the migration:
```bash
alembic upgrade head
```

### Troubleshooting Migrations
1. If a migration fails, you can rollback:
```bash
alembic downgrade -1
```

2. To check the current state:
```bash
alembic current
```

3. To view migration history:
```bash
alembic history
```

4. If you need to start fresh (Development Only):
```bash
rm -f data/app.db
rm -rf migrations/versions/*
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
python -m app.seed
```

### Best Practices
1. Always review auto-generated migrations before applying them
2. Keep migrations atomic and focused on a single change
3. Use meaningful migration messages
4. Test migrations in development before applying to production
5. Back up the database before running migrations in production
6. Use the seed script only in development environments 