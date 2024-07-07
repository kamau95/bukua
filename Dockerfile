# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
build-essential \
default-libmysqlclient-dev \
&& rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV FLASK_APP=website:create_app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which Gunicorn will listen
EXPOSE $PORT

# Run Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT "website:create_app()"
