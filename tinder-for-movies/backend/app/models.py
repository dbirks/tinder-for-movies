from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    swipes: List["Swipe"] = Relationship(back_populates="user")
    watchlist_items: List["WatchlistItem"] = Relationship(back_populates="user")

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tmdb_id: int = Field(unique=True, index=True)
    title: str
    overview: str
    poster_url: str
    release_year: int
    genres_json: str  # JSON-encoded array of genres
    
    swipes: List["Swipe"] = Relationship(back_populates="movie")
    watchlist_items: List["WatchlistItem"] = Relationship(back_populates="movie")

class Swipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    action: str  # "like" or "dislike"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    user: User = Relationship(back_populates="swipes")
    movie: Movie = Relationship(back_populates="swipes")

class WatchlistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    user: User = Relationship(back_populates="watchlist_items")
    movie: Movie = Relationship(back_populates="watchlist_items") 