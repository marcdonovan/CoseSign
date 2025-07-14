# Use a minimal Python image
FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir pycose cryptography

# Copy the signer script into the container
COPY cose_signer.py /app/cose_signer.py

# Set working directory
WORKDIR /app

# Default command to run the signer
ENTRYPOINT ["python", "cose_signer.py"]
