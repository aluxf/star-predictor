# Use the official Python base image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /app/

# Expose the port the application runs on
EXPOSE 8000

# Specify the command to run on container start
# Change 'app.py' to the entry point of your application
CMD ["ray", "start", "--head", "--port=6379"]
