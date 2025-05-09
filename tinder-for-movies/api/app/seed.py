from datetime import datetime, UTC
import json
from passlib.context import CryptContext
from sqlmodel import Session, select
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
    session.exec(select(WatchlistItem)).delete()
    session.exec(select(Swipe)).delete()
    session.exec(select(Movie)).delete()
    session.exec(select(User)).delete()
    session.commit()

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

        # Create sample movies with diverse genres and eras
        movies = [
            # Modern Classics
            Movie(
                tmdb_id=1,
                title="The Shawshank Redemption",
                overview="Two imprisoned men bond over a number of years...",
                poster_url="https://example.com/shawshank.jpg",
                release_year=1994,
                genres_json=json.dumps(["Drama"])
            ),
            Movie(
                tmdb_id=2,
                title="The Godfather",
                overview="The aging patriarch of an organized crime dynasty...",
                poster_url="https://example.com/godfather.jpg",
                release_year=1972,
                genres_json=json.dumps(["Crime", "Drama"])
            ),
            Movie(
                tmdb_id=3,
                title="The Dark Knight",
                overview="When the menace known as the Joker...",
                poster_url="https://example.com/darkknight.jpg",
                release_year=2008,
                genres_json=json.dumps(["Action", "Crime", "Drama"])
            ),
            
            # Black & White Classics
            Movie(
                tmdb_id=4,
                title="Casablanca",
                overview="A cynical expatriate American cafe owner...",
                poster_url="https://example.com/casablanca.jpg",
                release_year=1942,
                genres_json=json.dumps(["Drama", "Romance", "War"])
            ),
            Movie(
                tmdb_id=5,
                title="Citizen Kane",
                overview="Following the death of publishing tycoon Charles Foster Kane...",
                poster_url="https://example.com/citizenkane.jpg",
                release_year=1941,
                genres_json=json.dumps(["Drama", "Mystery"])
            ),
            Movie(
                tmdb_id=6,
                title="Psycho",
                overview="A Phoenix secretary embezzles $40,000 from her employer's client...",
                poster_url="https://example.com/psycho.jpg",
                release_year=1960,
                genres_json=json.dumps(["Horror", "Mystery", "Thriller"])
            ),
            
            # Anime
            Movie(
                tmdb_id=7,
                title="Spirited Away",
                overview="During her family's move to the suburbs, a sullen 10-year-old girl...",
                poster_url="https://example.com/spiritedaway.jpg",
                release_year=2001,
                genres_json=json.dumps(["Animation", "Adventure", "Family", "Fantasy"])
            ),
            Movie(
                tmdb_id=8,
                title="Akira",
                overview="A secret military project endangers Neo-Tokyo when it turns a biker gang member...",
                poster_url="https://example.com/akira.jpg",
                release_year=1988,
                genres_json=json.dumps(["Animation", "Action", "Sci-Fi"])
            ),
            Movie(
                tmdb_id=9,
                title="Your Name",
                overview="Two strangers find themselves linked in a bizarre way...",
                poster_url="https://example.com/yourname.jpg",
                release_year=2016,
                genres_json=json.dumps(["Animation", "Drama", "Fantasy", "Romance"])
            ),
            
            # International Classics
            Movie(
                tmdb_id=10,
                title="Seven Samurai",
                overview="A poor village under attack by bandits recruits seven unemployed samurai...",
                poster_url="https://example.com/sevensamurai.jpg",
                release_year=1954,
                genres_json=json.dumps(["Action", "Adventure", "Drama"])
            ),
            Movie(
                tmdb_id=11,
                title="The 400 Blows",
                overview="A young boy, left without attention, delves into a life of petty crime...",
                poster_url="https://example.com/400blows.jpg",
                release_year=1959,
                genres_json=json.dumps(["Crime", "Drama"])
            ),
            Movie(
                tmdb_id=12,
                title="8½",
                overview="A harried movie director retreats into his memories and fantasies...",
                poster_url="https://example.com/8andhalf.jpg",
                release_year=1963,
                genres_json=json.dumps(["Drama", "Fantasy"])
            ),
            
            # Modern Anime
            Movie(
                tmdb_id=13,
                title="Demon Slayer: Mugen Train",
                overview="Tanjiro and his comrades investigate the mysterious disappearances...",
                poster_url="https://example.com/demonslayer.jpg",
                release_year=2020,
                genres_json=json.dumps(["Animation", "Action", "Adventure", "Fantasy"])
            ),
            Movie(
                tmdb_id=14,
                title="Jujutsu Kaisen 0",
                overview="Yuta Okkotsu gains control of an extremely powerful cursed spirit...",
                poster_url="https://example.com/jjk0.jpg",
                release_year=2021,
                genres_json=json.dumps(["Animation", "Action", "Fantasy"])
            ),
            Movie(
                tmdb_id=15,
                title="Weathering With You",
                overview="A high-school boy who has run away to Tokyo befriends a girl...",
                poster_url="https://example.com/weathering.jpg",
                release_year=2019,
                genres_json=json.dumps(["Animation", "Drama", "Fantasy", "Romance"])
            )
        ]

        # Add user
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        # Add movies
        for movie in movies:
            session.add(movie)
        session.commit()

        # Add some swipes (more diverse preferences)
        swipes = [
            Swipe(user_id=test_user.id, movie_id=1, action="like"),  # Shawshank
            Swipe(user_id=test_user.id, movie_id=2, action="like"),  # Godfather
            Swipe(user_id=test_user.id, movie_id=3, action="like"),  # Dark Knight
            Swipe(user_id=test_user.id, movie_id=4, action="like"),  # Casablanca
            Swipe(user_id=test_user.id, movie_id=5, action="dislike"),  # Citizen Kane
            Swipe(user_id=test_user.id, movie_id=6, action="like"),  # Psycho
            Swipe(user_id=test_user.id, movie_id=7, action="like"),  # Spirited Away
            Swipe(user_id=test_user.id, movie_id=8, action="like"),  # Akira
            Swipe(user_id=test_user.id, movie_id=9, action="dislike"),  # Your Name
            Swipe(user_id=test_user.id, movie_id=10, action="like"),  # Seven Samurai
            Swipe(user_id=test_user.id, movie_id=11, action="dislike"),  # 400 Blows
            Swipe(user_id=test_user.id, movie_id=12, action="like"),  # 8½
            Swipe(user_id=test_user.id, movie_id=13, action="like"),  # Demon Slayer
            Swipe(user_id=test_user.id, movie_id=14, action="like"),  # Jujutsu Kaisen
            Swipe(user_id=test_user.id, movie_id=15, action="dislike")  # Weathering With You
        ]
        for swipe in swipes:
            session.add(swipe)

        # Add some watchlist items
        watchlist_items = [
            WatchlistItem(user_id=test_user.id, movie_id=1),  # Shawshank
            WatchlistItem(user_id=test_user.id, movie_id=4),  # Casablanca
            WatchlistItem(user_id=test_user.id, movie_id=7),  # Spirited Away
            WatchlistItem(user_id=test_user.id, movie_id=10),  # Seven Samurai
            WatchlistItem(user_id=test_user.id, movie_id=13)  # Demon Slayer
        ]
        for item in watchlist_items:
            session.add(item)

        session.commit()

if __name__ == "__main__":
    seed_database() 