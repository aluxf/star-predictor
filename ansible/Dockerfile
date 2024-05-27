# Use an official Ubuntu runtime as a parent image
FROM ubuntu:20.04

# Set the working directory in the container to /app
WORKDIR /app

# Install Python, pip, and Ansible
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ansible \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run start_instances.py when the container launches
CMD ["./initialize.sh"]