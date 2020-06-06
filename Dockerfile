FROM python:alpine3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src /app
CMD ["python", "./bundle-updater.py"]
