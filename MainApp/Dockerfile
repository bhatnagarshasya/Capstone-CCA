# Use an official base image with Python (replace python:3.8 with the desired version)
FROM python:3.9-buster

# Set the working directory
WORKDIR /Routes

# Copy the entire project into the container
COPY . /Routes

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

CMD ["python", "-m", "Routes"]