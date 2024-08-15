# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /code

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /code
COPY . /code/

# Set environment variables
ENV ENVIRONMENT=prod

# Command to run the application
CMD ["python", "main.py"]