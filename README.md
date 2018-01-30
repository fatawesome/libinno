# libinno
First year bachelor's project in Innopolis University (Spring 2018)

# How to run
In docker_libinno run
    `$ docker-compose up`

If django doesn't run server automatically you need to do it manually:
    1. In new terminal `$ docker exec -it <container> /bin/sh`
    2. `/libinno # python manage.py runserver 0.0.0.0:8000`