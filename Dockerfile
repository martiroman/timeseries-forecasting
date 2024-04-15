FROM python:3.8-slim

WORKDIR /app
COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
