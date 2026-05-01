# syntax=docker/dockerfile:1

# Use uv base image for faster dependency management
FROM ghcr.io/astral-sh/uv:latest as uv

# Use Python 3.12 slim as the final base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=uv /uv /usr/local/bin/uv

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv and make them available system-wide
RUN uv sync --frozen --no-dev && \
    uv pip install --system -e .
RUN uv pip install pytest
# Copy the rest of the application
COPY . .

# Create models directory if it doesn't exist
RUN mkdir -p models

# Generate the pre-trained model if it doesn't exist
RUN python generate_model.py || echo "Model generation completed or failed - continuing..."

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Create a non-root user for better security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Default command - interactive shell
CMD ["bash"]
