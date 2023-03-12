# Rudderstack Backend

The first thing to do is to clone the repository:

```sh
$ https://github.com/manavchawla2012/rudderstack.git
$ cd rudderstack
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv venv/
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pipenv install
```

Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `python3`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd project
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```

Run UI Project in NEXT.Js to Experience UI. This is a REST Project built using 
[DJANGO](https://www.djangoproject.com/) and [DRF](https://www.django-rest-framework.org/)

### Database
Default DB is `Postgres` 

```sh
Update settings.py to configure DB credentials
Default Credentials: 
$ username: myuser
$ password: mypass
$ database_name: rudderstack
```

```sh
To run Test cases
(venv)$ cd project
(venv)$ source venv/bin/activate
(venv)$ python manage.py test
```
