# Use the official Python base image from the Docker Hub
FROM rayproject/ray:latest

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /app/

# Specify the command to run on container start
# Change 'app.py' to the entry point of your application
CMD ["ray", "start", "--head", "--block", "--port=6379"]
