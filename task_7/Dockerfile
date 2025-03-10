FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app_bd.py .

EXPOSE 5050

CMD ["python3", "app_bd.py"]