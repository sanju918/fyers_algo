# Use the official Python slim image
#FROM python:3.9-alpine

# update few things
# RUN apk update && apk add make automake gcc g++ subversion python3-dev
# Use a minimal Python image as the build stage
FROM python:3.9-alpine AS builder

# Install required build dependencies
# RUN apt-get update && apt-get install -y build-essential

# Set the working directory in the container
WORKDIR /app

# copy requirements file
COPY requirements.txt .

# Install required packages using pip
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Use a smaller base image for the final stage
FROM python:3.9-alpine

# Copy only the necessary files and installed libraries from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app
# Expose the desired port
EXPOSE 4001

# Start the container with the working directory mounted
# CMD ["sh"]
CMD ["python", "./src/main.py"]