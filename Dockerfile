FROM python:3.10-slim

# Install espeak + MBROLA voices (natural speech works in container)
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    mbrola \
    mbrola-us1 mbrola-us2 mbrola-us3 \
    libespeak-ng1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose port (overridden in compose)
EXPOSE 5000

# Run server
CMD ["python", "MosesAI_Server.py"]  