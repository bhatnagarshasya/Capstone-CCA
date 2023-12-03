# Use the same base image as the main application
FROM python:3.9-buster

# Set the working directory
WORKDIR /Routes

# Copy the entire project into the container
COPY . /Routes

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_RUN_HOST=127.0.0.1

EXPOSE 8080

# Specify the command to run the prediction service
CMD ["python", "-m", "Routes"]
