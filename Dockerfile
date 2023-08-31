# Use the official Python slim image
FROM python:3.9-slim

# update few things
# RUN apk update && apk add make automake gcc g++ subversion python3-dev

# Set the working directory in the container
WORKDIR /app

# copy requirements file
COPY requirements.txt .

# Install required packages using pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the desired port
EXPOSE 4001

# Start the container with the working directory mounted
#CMD ["sh"]
CMD ["python", "orchestrator.py"]