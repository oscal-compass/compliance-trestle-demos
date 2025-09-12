# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Copy the requirements.txt file first to leverage Docker's build cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the Python script into the container
COPY work/xlsx_to_catalog.py /app/work/xlsx_to_catalog.py

# Copy the data directory into the container
COPY data/ /app/data/

# Define the command to run the script with the specified arguments
CMD ["python", "work/xlsx_to_catalog.py", "--input", "data/cprt_SP800_66_2_0_0_08-02-2025.xlsx", "--output", "data/catalog.json", "--title", "HIPAA Cybersecurity Resource Guide", "--version", "2.0.0", "--oscal-version", "1.1.3"]