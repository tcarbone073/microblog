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
The recommended way to start the application is using the `flask run` command. The command starts a **development** server, loads environment variables from the `.flaskenv` file, and runs the python file defined by the `FLASK_APP` environment variable in `.flaskenv`. See reference (a)for further reading on `flask run`.
```
# .flaskenv
export FLASK_APP=microblog.py          # Name of application file
export FLASK=[development|production]  # Toggle development or production mode (among others)
export SERVER_NAME=x.x.x.x:p           # Set server:port. Default is localhost:5000. Use 0.0.0.0 to run on remote server. 
```
In this case, `microblog.py` imports the `app` module, calling `app/__init__.py`. This file will create the application object; import configuration data from `config.py`; initialize database and migrations objects; initialize the login manager; setup the mail server and application logging; and import `routes.py`, `models.py`, and `errors.py`.

### Configuration Data
Application configuration data is stored in `config.py`. For some configuration information, the file will first look check if any environment variables are set matching the configuration item. If not, `config.py` sets it. Other configuration information is located here for convenience.
