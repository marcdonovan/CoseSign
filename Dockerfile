FROM python:3.11-slim

WORKDIR /app
COPY cose_signer.py .

RUN pip install --no-cache-dir pycose==0.10.4 cryptography

ENTRYPOINT ["python", "cose_signer.py"]
