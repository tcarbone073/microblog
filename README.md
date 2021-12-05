## Overview
**Flask** is a python framework that is used to build web applications. It uses the **Jinja2** templating engine to render dynamic html content. This project follows the tutorial from [this blog](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## References
   (a) [Flask basic overview](https://becominghuman.ai/full-stack-web-development-python-flask-javascript-jquery-bootstrap-802dd7d43053)<br>
   (b) [app.run() vs flask run](https://www.twilio.com/blog/how-run-flask-application)

## Discussion
The basic structure of the project is outlined below.
```
microblog/
├── .flaskenv
├── .venv/
├── microblog.py
├── config.py
├── tests.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── forms.py
│   ├── errors.py
│   └── models.py
├── templates/
│   ├── index.html
│   └── 404.html
└── logs/
```
### Server Startup
The recommended way to start the application is using the `flask run` command. The command starts a **development** server, loads environment variables from the `.flaskenv` file, and runs the python file defined by the `FLASK_APP` environment variable in `.flaskenv`. See reference (a) for further reading on `flask run`.
```
# .flaskenv
export FLASK_APP=microblog.py          # Name of application file
export FLASK=[development|production]  # Toggle development or production mode (among others)
```
If running on a remote server, use `flask run -h 0.0.0.0 -p xxxx`.

In this case, `microblog.py` imports the `app` module, calling `app/__init__.py`. This file will create the application object; import configuration data from `config.py`; initialize database and migrations objects; initialize the login manager; setup the mail server and application logging; and import `routes.py`, `models.py`, and `errors.py`.

### Configuration Data
Application configuration data is stored in `config.py`. For some configuration information, the file will first look check if any environment variables are set matching the configuration item. If not, `config.py` sets it. Other configuration information is located here for convenience.

### Application Web Pages
All of the different URLs for the application are handled in `routes.py`. Each page is handled by a **view function**, which is mapped to a URL for the pages contained in `app/templates/`. When the client's browser requests a page, flask runs the corresponding view function for the page, passing any dynamic content to the template. The template is displayed using the **Jinja2** templating engine. Each template is primarily standard html, with the expected dynamic content from `routes.py` encapsulated in double curly braces. Control statements, such as for loops or inclusion statements (e.g., `import`, `#include`) are denoted by `{% %}` markers.

### Forms
A web page often accepts input from a user in some format. Where input is required, **forms** are implemented. Forms are not only convenient building blocks, but also validate input and register succesful submission of data.

### Packages
Simply put, there are a huge number of python packages that are required to build a flask application. Each package, its dependencies, and a brief description of the purpose of the package is provided here.
| Package Name | Requires | Purpose |
| ------------ | -------- | ------- |
| alembic | 
| Babel |
| blinker |
| certifi |
| charset-normalizer |
| click |
| colorama |
| dataclasses |
| defusedxml |
| dnspython |
| dominate |
| elasticsearch |
| email-validator |
| Flask | Werkzeug, Jinja2, itsdangerous, click | Python web application framework
| Flask-Babel |
| Flask-Bootstrap |
| Flask-HTTPAuth |
| Flask-Login |
| Flask-Mail |
| Flask-Migrate |
| Flask-Moment |
| Flask-SQLAlchemy |
| Flask-WTF |
| greenlet |
| httpie |
| idna |
| importlib-metadat |
| itsdangerous | | Secure data signing<br> - Handles flasks's session cookie
| Jinja2 | 
| langdetect |
| Mako |
| MarkupSafe |
| Pygments |
| PyJWT |
| PySocks |
| python-dateutil |
| python-editor |
| pytz |
| redis |
| requests |
| requests-toolbelt |
| rq |
| six |
| SQLAlchemy |
| typing-extensions |
| urllib3 |
| visitor |
| Werkzeug | dataclasses | Python implementation of Web Server Gateway Interface (WSGI)<br> - Password hashing
| WTForms |
| zipp |
