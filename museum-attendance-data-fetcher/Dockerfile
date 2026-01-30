# Use Python 3.11 slim image
FROM python:3.11-slim


# Copy and install common package
COPY museum-attendance-common /app/museum-attendance-common
RUN pip install /app/museum-attendance-common

# Copy data fetcher project files
COPY museum-attendance-data-fetcher/pyproject.toml /app/pyproject.toml
COPY museum-attendance-data-fetcher/src /app/src

WORKDIR /app

# Install data fetcher dependencies (production only, excludes [dev] extras)
RUN pip install .

# Create assets directory for HTML files
RUN mkdir -p /app/assets

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the application
CMD ["python", "/app/src/museum_attendance_data_fetcher.py"]