# Tai Wan Kim
# Dockerfile for FS

FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9090

CMD ["python", "app.py"]
