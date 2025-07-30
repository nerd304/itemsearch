# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on (default Flask port is 5000)
EXPOSE 5000

# Define the command to run your application
# Assuming your Flask app is in main.py and has an app instance named 'app'
CMD ["flask", "run", "--host", "0.0.0.0"]
