FROM python:3.7@sha256:c1e36afba1c3c230a6846801fb284cf4383a8a0080fcf32c2ec625c066c56361

WORKDIR /APP

COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt"]

COPY . .
CMD ["python", "main.py"]