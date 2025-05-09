# Use Python slim image
FROM python:3.13-slim

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy dependency definition files
COPY pyproject.toml ./ 

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy alembic python-dotenv pydantic pydantic-settings

# Copy application code
COPY ./app /app/app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST="0.0.0.0"
ENV PORT="8000"

# Expose the port Uvicorn will run on
EXPOSE 8000

# Change to non-root user
USER appuser

# Command to run the application using Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
