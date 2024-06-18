FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .
RUN mkdir /cert

EXPOSE 8000
EXPOSE 5432
EXPOSE 443

# Use uvicorn to serve the application with HTTPS
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/certs/privkey.pem", "--ssl-certfile", "/certs/cert.pem"]


