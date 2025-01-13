# Start from Python Alpine image
FROM python:3.12-alpine

# Set environment variables
ENV HOME /root

# Copy your project to the image
COPY ./python-simple-auth/ /app

# Make the app directory and its contents executable
RUN chmod -R 755 /app

# Set working directory for commands in the container
WORKDIR /app

# Install required tools
RUN pip install poetry
RUN poetry install --no-root

# Expose port 8000 for running application
EXPOSE 8000

# Command to run when container starts up
CMD ["sh", "-c", "poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]