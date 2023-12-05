# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask application
CMD ["poetry", "run", "python", "app.py"]
