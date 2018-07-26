# image-converter-demo
Flask microservice that resizes images


## Installation and usage
1. To run the project locally, install Docker for Mac/Windows and run:

```$ docker-compose up --build -d```

2. Go to localhost/health in your local browser to check that it works. You should see the text is "OK".

3. To resize an image, enter the address localhost/\<parameters\>?url=<image_url>, where parameters are the the width and height of the image in the form of w_\<width\> and h_\<height\>, separated by a comma, and where <image_url> is the image you want to resize.

Example:
```
http://localhost/w_150,h_500?url=https://i.imgflip.com/ujm8r.jpg
```


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

### Web Server: Nginx
I chose Nginx as the web server, since it has good performance and is easy to set up. Flask does come with a built-in server, but it doesn't scale well and is intended for development only.

### Application Server: Flask and Gunicorn
I chose Flask as the application framework since it is well-maintained, light-weight and suitable for API development, such as this demo project.

Nginx cannot run the Flask app directly. We need a WSGI application server like Gunicorn that takes the HTTP requests from Nginx and converts them into the [WSGI format](https://wsgi.readthedocs.io/) and feeds them to the Flask application.

### Image processing
I have used Pillow before for image processing in Django. It's easy to use and still maintained.

 
## Problems encountered
### Makefile
I want to be able to run commands for testing, like PEP8, mypy and unit testing. I hadn't set up these commands before and so it took some time to figure out that you need to use docker-compose down --remove-orphans to clean up containers between the test runs. 

### Choice of Docker Image
First I chose [python:3.7.0-alpine3.8](https://alpinelinux.org/about/) for the Python dependency since the resulting docker images take up very little space. Unfortunately the image processing library Pillow did not compile in that environment since there was a dependency on a library not present in Alpine Linux. Instead I chose the ```python:3.7.0``` docker image.