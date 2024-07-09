# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY app /app

# Install any needed packages specified in requirements.txt
RUN pip install flask requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run server.py when the container launches
CMD ["python", "node.py"]
