FROM python:latest

WORKDIR /srv/app

COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

CMD [ "python", "src/manage.py", "runserver", "5000" ]