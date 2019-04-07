FROM python:3.5
MAINTAINER gureuso <wyun13043@gmail.com>

USER root
WORKDIR /root

#base
RUN apt-get -y update
RUN apt-get -y install python3-pip

#django
RUN git clone https://github.com/gureuso/turnthepage.git
WORKDIR /root/turnthepage
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations;python manage.py migrate;python manage.py runserver 0.0.0.0:8000 --insecure
