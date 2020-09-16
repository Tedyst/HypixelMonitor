FROM python:3.8.5

WORKDIR /APP

COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt"]

COPY . .
CMD ["python", "main.py"]