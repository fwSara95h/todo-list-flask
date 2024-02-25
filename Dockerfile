# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r backend/requirements.txt
RUN apt-get update -y &&\
  apt-get install pkg-config -y &&\
  apt-get install -y python3-dev build-essential &&\
  apt-get install -y default-libmysqlclient-dev &&\
  pip install --upgrade pip &&\
  pip install -U mysqlclient &&\
  pip install -U PyMySQL &&\
  pip install -U Flask &&\
  pip install -U PyYAML
# pip install -U flask-mysqldb &&\
 
# Set environment variables for Flask
ENV FLASK_APP=backend/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]
