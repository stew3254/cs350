FROM python:latest

EXPOSE 5000
WORKDIR /srv/app

COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.sh .
COPY .env .

CMD ["./server.sh"]

