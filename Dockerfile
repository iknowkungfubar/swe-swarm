FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY README.md .
COPY LICENSE .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Create logs directory
RUN mkdir -p logs

# Set entrypoint to gastown CLI
ENTRYPOINT ["gastown"]
CMD ["--help"]