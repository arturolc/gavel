# Use slim as per https://pythonspeed.com/articles/alpine-docker-python/
FROM python:3.8-slim

WORKDIR /opt/gavel/

# Update packages.
RUN apt-get update \
        && apt-get -y upgrade

# Install system package dependencies.
RUN apt-get -y install python3-dev \
        libpq-dev \
        gcc

# Clean up apt-get.
RUN apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Copy over just the list of Python dependencies.
COPY requirements.txt .

# Install Python dependencies.
RUN set -ex \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 80
ENV PORT=80

CMD ["sh", "-c", "python initialize.py && gunicorn -b :${PORT} -w 3 gavel:app"]

# Copy over the rest of the project files.
COPY . .
