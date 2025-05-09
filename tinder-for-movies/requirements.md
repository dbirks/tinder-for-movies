# Tinder for Movies – Requirements

## Document Info
- **Project**: Tinder for Movies  
- **Phases**: MVP → Phase 2 → Phase 3 → Phase 4 → Phase 5
- **Date**: 2024-06-XX  
- **Author**: _Your Name / Team_

---

## Phase 1 – MVP
_Basic movie discovery with swipe interface; session only (no persistence)_

### Purpose & Scope
- Frontend connects to backend (Python + FastAPI) streaming live movie data from TMDb API (using Python SDK).
- Two main flows:
  1. **Swipe Page**: User swipes yes/no (like/dislike) to movies.
  2. **Recommendations Page**: Recommend movies during session based on yes/no's.
- No database, no accounts, no storage—state is in browser/session only.

### Backend
- **Python + FastAPI**
- **TMDb API** (using Python SDK)
  - Includes anime via TMDb genre/keyword queries.
- **Endpoints:**
  - GET /api/v1/movies?limit=20&page=1  — popular movies
  - GET /api/v1/movies/{id}              — movie details
  - POST /api/v1/temp-preferences        — temp store likes/dislikes for the session
  - GET /api/v1/recommendations/basic    — basic same-session recommendations

### Frontend
- **Vite + React + TypeScript + shadcn-ui + Tailwind (mobile-first, pastel palette)**
- **Views:**
  - Swipe cards (like/dislike, with animations)
  - Button to see session recommendations (genre/year-based)
- Mobile-first responsive layout.  
- Simple, modern UI—no registration, onboarding, or storage.

---

## Phase 2 – Data Persistence & External Embeddings
_Add persistent user accounts and use pre-existing movie embeddings for recs._

### Features
- Email/password registration, persistent storage of likes/dislikes/watchlist (SQLite).
- Use published/precomputed embeddings (e.g. MovieLens) to improve cold-start recs.
- Personalized recs on Recommendations page.

### Backend
- **Add SQLite (SQLModel + Pydantic)**
- **JWT auth**
- **Models:**
  - User, Swipe, WatchlistItem, MovieEmbedding (pre-existing)
- **Endpoints:**
  - Auth/user CRUD (register, login, logout, update)
  - POST /api/v1/swipe           — record like/dislike
  - Watchlist CRUD endpoints
  - GET /api/v1/recommendations  — now enhanced with embeddings/user history

---

## Phase 3 – Scraping TMDb, Custom OpenAI Embeddings & Vector DB
_Bulk fetch data from TMDb (including anime), generate your own embeddings, move to a real vector DB._

### Features
- Use TMDb API via Python SDK to fetch large collection of movies + anime.
- Use OpenAI (small model, e.g. ada) to generate text embeddings (titles, overviews, etc).
- Store movie embeddings, user profiles, and enable vector similarity search for personalized recs.

### Backend
- **Periodic data pipeline**: fetch from TMDb, create embeddings via OpenAI.
- **Vector DB**: Unsure—prefer one with good UI for inspecting/managing vectors.
    - (Pinecone and Qdrant are popular and have web UIs. [Qdrant](https://qdrant.tech/) especially is praised for its UI.)

- **Models:**
  - MovieEmbedding { movie_id, vector, generation_method }
  - UserEmbedding { user_id, vector, updated_at }
- **Endpoints:**
  - GET /api/v1/recommendations?approach=vector
  - GET /api/v1/movies/similar/{id}

- **Frontend**: improvements for viewing/exploring movie recommendations powered by real similarity.

---

## Phase 4 – Social & Advanced Features
_Social, sharing, and improved recommendation controls._

### Features
- Friends, suggested users with similar taste, sharing lists
- Group watchlists and collaborative recommendations
- Ratings/comments per movie/user
- Advanced filtering and sorting in UI

### Technical
- OAuth2 social login if desired  
- Push notifications (optional)  
- Background jobs for periodic rec pre-compute

---

## Phase 5 – Scalability & Analytics
_Hardening, scaling, analytics for learning/insight._

### Features
- Production-grade deployment (Kubernetes, CI/CD)
- Analytics dashboard (user engagement, rec accuracy, swipes, etc)
- Performance monitoring, error logging (Grafana, Sentry)
- Optional: Personal dashboards ("Your movie taste profile graph", etc)

---

## Key Tech Decisions (context from previous chat)
- **Movie data**: TMDb (with Python SDK), supports both regular movies and anime.
- **Embeddings**: OpenAI small models (e.g. `text-embedding-ada-002`).
- **Vector DB**: Undecided; want a solution with a good inspector UI (Qdrant, Pinecone both good—Qdrant especially for UI).
- **No internationalization needed.**
- **Mobile-first design.**
- **Private/learning only; no commercial/legal/data compliance constraints.**

---

## Open Questions
1. Confirm vector DB choice: Qdrant or Pinecone or ...?
2. Define your user data privacy policy for learning/sharing.
3. (In later phases) Add non-English/anime-specific filters if you wish.
4. Any special UI features for inspecting recommendations/embeddings for learning purposes?
5. Would you want explainability ("here’s why we recommended this") in UI?

> This doc reflects your latest requirements and technology preferences.





```mermaid
erDiagram
    User {
        INTEGER    id PK
        TEXT       name
        TEXT       email UNIQUE
        TEXT       password_hash
        DATETIME   created_at
    }
    Movie {
        INTEGER    id PK
        INTEGER    tmdb_id UNIQUE
        TEXT       title
        TEXT       overview
        TEXT       poster_url
        INTEGER    release_year
        TEXT       genres_json    "JSON-encoded array"
    }
    Swipe {
        INTEGER    id PK
        INTEGER    user_id FK
        INTEGER    movie_id FK
        TEXT       action         "like or dislike"
        DATETIME   timestamp
    }
    WatchlistItem {
        INTEGER    id PK
        INTEGER    user_id FK
        INTEGER    movie_id FK
        DATETIME   timestamp
    }

    User          ||--o{ Swipe           : makes
    User          ||--o{ WatchlistItem   : has
    Movie         ||--o{ Swipe           : referenced_by
    Movie         ||--o{ WatchlistItem   : in
```
