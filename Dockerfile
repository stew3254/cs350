FROM python:latest

<<<<<<< HEAD
=======
EXPOSE 5000
>>>>>>> origin/dev
WORKDIR /srv/app

COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

<<<<<<< HEAD
CMD [ "python", "src/manage.py", "runserver", "0.0.0.0:5000" ]
=======
#CMD [ "python", "src/manage.py", "makemigrations", "migrate", "&&", "python", "src/manage.py", "runserver", "5000" ]
CMD python src/manage.py makemigrations 
CMD python src/manage.py migrate
CMD python src/manage.py runserver 0.0.0.0:5000
>>>>>>> origin/dev
