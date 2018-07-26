# image-converter-demo
Flask microservice that resizes images


## Installation
1. To run the project locally, install Docker for Mac/Windows and run:

```$ docker-compose up --build -d```

2. Go to http://0.0.0.0:8000/health in your local browser to check that it works. You should see the text is "OK".

## Usage


## Tech Stack
<center>
```
+--------------------------------------------+
| Docker                                     |
|                                            |
|   +----------------------------------+     |
|   | Web Application container        |     |
|   |                                  |     |
|   | +-----------------------------+  |     |
|   | |                             |  |     |
|   | |  Flask app with Gunicorn    |  |     |
|   | |                             |  |     |
|   | +-----------------------------+  |     |
|   +----------------------------------+     |
|                                            |
|   +----------------------------------+     |
|   |                                  |     |
|   | Nginx container                  |     |
|   |                                  |     |
|   +----------------------------------+     |
+--------------------------------------------+
```
</center>

### Environment: Docker
I chose Docker for this simple demo as it makes it easy for anyone interested to test the demo locally, or to deploy to production.

I chose [python:3.7.0-alpine3.8](https://alpinelinux.org/about/) for the Python dependency since the resulting docker images take up very little space.

### Web Server: Nginx
I chose Nginx as the web server, since it has good performance and is easy to set up. Flask does come with a built-in server, but it doesn't scale well and is intended for development only.

### Application Server: Flask and Gunicorn
I chose Flask as the application framework since it is well-maintained, light-weight and suitable for API development, such as this demo project.

Nginx cannot run the Flask app directly. We need a WSGI application server like Gunicorn that takes the HTTP requests from Nginx and converts them into the [WSGI format](https://wsgi.readthedocs.io/) and feeds them to the Flask application.

### Image processing
I have used Pillow before for image processing in Django. It's easy to use and still maintained.

 
## Problems encountered
### Makefile
I want to be able to run commands for testing, like PEP8, mypy and unit testing. It took a while to figure out that you need to use docker-compose down --remove-orphans to clean up containers between the test runs. 
