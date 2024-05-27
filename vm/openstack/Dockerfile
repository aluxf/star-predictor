# Use an official Ubuntu runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install Python, pip, and Ansible
RUN apt-get update && apt-get install -y \
    python3-openstackclient \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run start_instances.py when the container launches
CMD ["python3 start_instances.py"]