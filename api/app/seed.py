from datetime import datetime, UTC
import json
import csv
from pathlib import Path
from passlib.context import CryptContext
from sqlmodel import Session, select, delete
from app.db import engine
from app.models import User, Movie, Swipe, WatchlistItem

# Configure passlib with explicit bcrypt version
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Explicitly set rounds
)

def clear_database(session: Session):
    """Clear all data from the database."""
    session.exec(delete(WatchlistItem))
    session.exec(delete(Swipe))
    session.exec(delete(Movie))
    session.exec(delete(User))
    session.commit()

def load_movielens_data():
    """Load and parse MovieLens data files."""
    data_dir = Path("data/ml-latest-small")
    
    # Load movies
    movies = {}
    with open(data_dir / "movies.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract year from title (format: "Title (Year)")
            title = row["title"]
            year = None
            if "(" in title and ")" in title:
                year_str = title[title.rfind("(")+1:title.rfind(")")]
                try:
                    year = int(year_str)
                except ValueError:
                    pass
            
            # Parse genres
            genres = row["genres"].split("|")
            if "(no genres listed)" in genres:
                genres.remove("(no genres listed)")
            
            movies[row["movieId"]] = {
                "title": title,
                "year": year,
                "genres": genres
            }
    
    # Load links to get TMDb IDs
    with open(data_dir / "links.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["movieId"] in movies:
                movies[row["movieId"]]["tmdb_id"] = int(row["tmdbId"]) if row["tmdbId"] else None
    
    return movies

def seed_database():
    with Session(engine) as session:
        # Clear existing data
        clear_database(session)

        # Create test user
        test_user = User(
            name="Test User",
            email="test@example.com",
            password_hash=pwd_context.hash("password123"),
            created_at=datetime.now(UTC)
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        # Load MovieLens data
        movielens_movies = load_movielens_data()
        
        # Create Movie objects from MovieLens data
        for movie_id, movie_data in movielens_movies.items():
            if movie_data.get("tmdb_id"):  # Only add movies with TMDb IDs
                movie = Movie(
                    tmdb_id=movie_data["tmdb_id"],
                    title=movie_data["title"],
                    overview="",  # We'll need to fetch this from TMDb API later
                    poster_url="",  # We'll need to fetch this from TMDb API later
                    release_year=movie_data["year"] or 0,
                    genres_json=json.dumps(movie_data["genres"])
                )
                session.add(movie)
        
        session.commit()

        # Load ratings and convert to swipes
        ratings_file = Path("data/ml-latest-small/ratings.csv")
        if ratings_file.exists():
            with open(ratings_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert ratings to swipes (4-5 stars = like, 1-2 stars = dislike)
                    rating = float(row["rating"])
                    if rating >= 4.0:
                        action = "like"
                    elif rating <= 2.0:
                        action = "dislike"
                    else:
                        continue  # Skip neutral ratings
                    
                    # Get the movie's database ID
                    movie_id = row["movieId"]
                    if movie_id in movielens_movies and movielens_movies[movie_id].get("tmdb_id"):
                        # Find the movie in our database
                        movie = session.exec(
                            select(Movie).where(Movie.tmdb_id == movielens_movies[movie_id]["tmdb_id"])
                        ).first()
                        
                        if movie:
                            swipe = Swipe(
                                user_id=test_user.id,
                                movie_id=movie.id,
                                action=action,
                                timestamp=datetime.fromtimestamp(int(row["timestamp"]), UTC)
                            )
                            session.add(swipe)
            
            session.commit()

if __name__ == "__main__":
    seed_database() 