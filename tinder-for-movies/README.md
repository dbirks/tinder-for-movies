# Tinder for Movies

This is a monorepo for the Tinder for Movies application, featuring:

- **API**: FastAPI (Python) with SQLite
- **UI**: Vite + React + TypeScript + Shadcn/ui
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions for building and pushing images to GHCR

## Structure

- `/api`: Backend service
- `/ui`: Frontend service
- `/.github/workflows`: GitHub Actions workflows
- `/docker-compose.yaml`: Docker Compose configuration

## Getting Started

1.  **Clone the repository**
2.  **Navigate to the project root**
3.  **Set up environment variables:**
    - Copy `api/.env.example` to `api/.env` and fill in any necessary values.
4.  **Build and run services:**
    ```bash
    docker-compose up --build
    ```

- API will be available at [http://localhost:8000](http://localhost:8000)
- UI will be available at [http://localhost:5173](http://localhost:5173)
