# Use the official Python Alpine image
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Install required packages using pip
RUN pip install --no-cache-dir python-dotenv fyers-apiv2 flask

# Expose the desired port
EXPOSE 4001

# Start the container with the working directory mounted
CMD ["sh"]