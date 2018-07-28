# image-converter-demo
Flask microservice that resizes images


## Installation and usage
1. To run the project locally, install Docker for Mac/Windows and run:

```$ docker-compose up --build -d```

2. Go to localhost/health in your local browser to check that it works. You should see the text is "OK".

3. To resize an image, enter the address `localhost/<parameters>?url=<image_url>`, where parameters are the the width and height of the image in the form of `w_<width>` and `h_<height>`, separated by a comma, and where `<image_url>` is the image you want to resize.

Example:
`http://localhost/w_150,h_500?url=https://i.imgflip.com/ujm8r.jpg`


## Tech Stack

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

It is of course possible to create a new Linux image from Alpine where zlib is installed, but that is a bit out of scope of this simple demo.

### Performance
Below is the web server performance with the Gunicorn sync worker class. Please note that I run the tests in a virtualenv instead of using docker-compose to start the docker stack so avoid caching in nginx.

```
$ ab -k -n 100 -c 100 http://127.0.0.1:8000/w_150,h_500?url=https://i.imgflip.com/ujm8r.jpg
This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        gunicorn/19.9.0
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /w_150,h_500?url=https://i.imgflip.com/ujm8r.jpg
Document Length:        42038 bytes

Concurrency Level:      100
Time taken for tests:   5.583 seconds
Complete requests:      100
Failed requests:        0
Keep-Alive requests:    0
Total transferred:      4223600 bytes
HTML transferred:       4203800 bytes
Requests per second:    17.91 [#/sec] (mean)
Time per request:       5582.976 [ms] (mean)
Time per request:       55.830 [ms] (mean, across all concurrent requests)
Transfer rate:          738.78 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   0.6      3       4
Processing:   212 2456 1355.1   2485    4754
Waiting:      212 2456 1355.2   2485    4754
Total:        217 2459 1354.6   2488    4757

Percentage of the requests served within a certain time (ms)
  50%   2488
  66%   3195
  75%   3680
  80%   3897
  90%   4334
  95%   4591
  98%   4670
  99%   4757
 100%   4757 (longest request)
 ```

 A total of 17.91 requests per second isn't that great. What happens is that a single Gunicorn `sync` worker can only handle one request at a time, and anything that takes a long time to process (like IO) will take up very precious worker resources. The solution is to switch to [asynchronous `gevent` workers](http://docs.gunicorn.org/en/stable/design.html#async-workers) which use cooperative multi-threading. Result below:

 ```
 $ ab -k -n 100 -c 100 http://127.0.0.1:8000/w_150,h_500?url=https://i.imgflip.com/ujm8r.jpg
This is ApacheBench, Version 2.3 <$Revision: 1826891 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        gunicorn/19.9.0
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /w_150,h_500?url=https://i.imgflip.com/ujm8r.jpg
Document Length:        42038 bytes

Concurrency Level:      100
Time taken for tests:   2.110 seconds
Complete requests:      100
Failed requests:        0
Keep-Alive requests:    0
Total transferred:      4223600 bytes
HTML transferred:       4203800 bytes
Requests per second:    47.39 [#/sec] (mean)
Time per request:       2109.985 [ms] (mean)
Time per request:       21.100 [ms] (mean, across all concurrent requests)
Transfer rate:          1954.81 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   0.7      4       4
Processing:   496  941 272.1    913    1614
Waiting:      489  941 272.3    913    1614
Total:        496  944 272.1    916    1617
WARNING: The median and mean for the initial connection time are not within a normal deviation
        These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
  50%    916
  66%   1016
  75%   1092
  80%   1156
  90%   1380
  95%   1513
  98%   1591
  99%   1617
 100%   1617 (longest request)
 ```

 47.39 requests per second is a definite improvement. One problem with this solution is that when I switched from the `sync` worker to the `gevent` worker I was unable to start gunicorn inside the web container. I got an error message like this:
 
 ```
 gunicorn.errors.HaltServer: <HaltServer 'Worker failed to boot.' 3>
  ```

 It turned out that the Python version used to build the `web` image was different from my system version. I did not spend time investigating compatibility between gevent and Python 3.8.0, instead I simply switched to Python version 3.6.5.