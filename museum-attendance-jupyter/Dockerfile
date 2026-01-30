# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install common package
COPY museum-attendance-common /app/museum-attendance-common
RUN pip install /app/museum-attendance-common

# Copy and install data-fetcher package (for extraction functionality)
COPY museum-attendance-data-fetcher /app/museum-attendance-data-fetcher
RUN pip install /app/museum-attendance-data-fetcher

# Copy jupyter project files
COPY museum-attendance-jupyter/pyproject.toml /app/pyproject.toml

# Install jupyter dependencies
RUN pip install .

# Create notebooks directory
RUN mkdir -p /app/notebooks

# Expose Jupyter port
EXPOSE 8888

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
