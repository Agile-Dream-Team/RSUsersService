# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /code

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /code
COPY . /code/

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
