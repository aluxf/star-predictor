FROM rayproject/ray:latest

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["ray start --address=$RAY_HOST:6379"]