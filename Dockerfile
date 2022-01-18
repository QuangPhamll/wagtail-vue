# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# setup dependencies
RUN apt-get update
RUN apt-get install xz-utils
RUN apt-get -y install curl

# Download latest nodejs binary
RUN curl https://nodejs.org/dist/v16.13.2/node-v16.13.2-linux-x64.tar.xz -O

# Extract & install
RUN tar -xf node-v16.13.2-linux-x64.tar.xz
RUN ln -s /node-v16.13.2-linux-x64/bin/node /usr/local/bin/node
RUN ln -s /node-v16.13.2-linux-x64/bin/npm /usr/local/bin/npm
RUN ln -s /node-v16.13.2-linux-x64/bin/npx /usr/local/bin/npx

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

## Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# The folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
WORKDIR /app/vue_app
RUN npm install
RUN npm run build

WORKDIR /app
USER wagtail
RUN chmod +x wait-for-it.sh
RUN chmod +x docker-entrypoint.sh

