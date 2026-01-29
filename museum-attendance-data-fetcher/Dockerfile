# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install common package
COPY museum-attendance-common /app/museum-attendance-common
RUN pip install /app/museum-attendance-common

# Copy data fetcher project files
COPY museum-attendance-data-fetcher/pyproject.toml /app/pyproject.toml
COPY museum-attendance-data-fetcher/src /app/src

# Fix the pyproject.toml to reference the installed common package instead of file path
RUN sed -i 's|museum-attendance-common @ file:///\${PROJECT_ROOT}/../museum-attendance-common|museum-attendance-common|g' /app/pyproject.toml

# Install data fetcher dependencies (without editable mode for production)
RUN pip install .

# Create assets directory for HTML files
RUN mkdir -p /app/assets

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the application
CMD ["python", "/app/src/museum_attendance_data_fetcher.py"]