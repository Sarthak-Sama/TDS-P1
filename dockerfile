# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Create a writable /data directory and set permissions
RUN mkdir -p /data && chmod -R 777 /data

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
