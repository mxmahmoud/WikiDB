# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /

# Copy the requirements.txt file into the container
COPY requirements.txt .
COPY .env .

# Install the required dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev

# Install the Python dependencies
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the application will run on
EXPOSE 8000
