# Stage 1: Build the application with uv
FROM python:3.13-slim as builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency definition files
COPY pyproject.toml poetry.lock* ./ 
# If poetry.lock is present, uv will use it. Otherwise, it uses pyproject.toml.

# Install dependencies using uv
# --system installs to the system Python, common for containers.
# We create a virtual environment first, then install into it, and then copy the venv.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache --system . # Installs from pyproject.toml/poetry.lock

# Copy the rest of the application code
COPY ./app /app/app
COPY ./wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Stage 2: Create the final lightweight image
FROM python:3.13-slim

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --from=builder /app/app /app/app
COPY --from=builder /app/wait-for-it.sh /app/wait-for-it.sh

# Set environment variables for FastAPI/Uvicorn
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV APP_MODULE="app.main:app" # Assuming your FastAPI app instance is 'app' in 'app/main.py'
ENV HOST="0.0.0.0"
ENV PORT="8000"

# Expose the port Uvicorn will run on
EXPOSE 8000

# Change to non-root user
USER appuser

# Command to run the application using Uvicorn
# The wait-for-it.sh script is optional here as SQLite is file-based.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
