# Pick the python version
FROM python:3.11-slim

# Create a folder for the code to live in
WORKDIR /app

# Copy the requirements over
COPY requirements.txt /app/requirements.txt

# Run the command to install the libraries
RUN pip install -r requirements.txt

# Copy everything else into the folder
COPY . /app

# The port we want to use
EXPOSE 8000

# Run the uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]