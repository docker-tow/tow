### [Back: 1. First step](step-1-first-step.md)

2. Deal with dynamic configuration
==================================

## Static files and mapping.py

Nginx keeps its site configurations in `/etc/nginx/sites-available` directory. We need to create `site-example.conf` in this directory and put simple site configuration in it. Tow provides an ability to do this. Create new file `files/site-example.conf`

```Nginx
server {
  listen 80 default_server;
  listen [::]:80 default_server ipv6only=on;

  root /usr/share/nginx/html;
  index index.html index.htm;

  # Make site accessible from http://localhost/
  server_name localhost;

  location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    try_files $uri $uri/ /index.html;
    # Uncomment to enable naxsi on this location
    # include /etc/nginx/naxsi.rules
  }
}
```

Add record into `mapping.py` with local file specification and path to place file inside the container. Open `mapping.py` with your favorite text editor and update it this way.

```python
mapping = [
    ("site-example.conf", "/etc/nginx/sites-available/site-example.conf")
]
```

Let's build container and check how it works.

```console
$ tow build -t tow-nginx-example
...
Successfully built 2ac717478a38
$ docker run -d -p 8080:80 tow-nginx-example
$ curl localhost:8080
...
<h1>Welcome to nginx on Debian!</h1>
...
```

Now we got Nginx up and running and default webpage served. Let's add our custom webpage with a little bit of dynamic content.

## Add some dynamics content

To add any dynamics content Tow provides templates and attributes. Attributes store any values in declared variables in `.py` files inside `attributes` directory. By default Tow creates `attributes/default.py` file for storing attributes.

Open `attributes/default.py` and add variable for our webpage header.

```python
header = "Tow Demo Webpage"
```

Now let's go and create simple webpage template. Create `templates/index.html.tmpl`

```html
<!DOCTYPE html>
<html>

<head>
  <title>{{header}}</title>
</head>

<body>
  <h1>{{header}}</h1>
</body>

</html>
```

In this template we used `header` attribute to set title and header of our webpage. To pass this template inside container add it to `mapping.py` as we did it for static files. By default Nginx uses `/var/www/html` to store site content, so modify `mapping.py` this way:

```python
mapping = [
    ("site-example.conf", "/etc/nginx/sites-available/site-example.conf"),
    ("index.html.tmpl", "/var/www/html/index.html")
]

```

Attributes and templates provide simple, but powerful way to store configuration variables and configuration files templates structured and separately.

## Using environment variables

To modify attributes while running container from image we need to use environment variables. First of all modify `Dockerfile`:

```Dockerfile
FROM debian:jessie

RUN apt-get update && \
    apt-get install -y nginx

RUN rm -rf /var/lib/apt/lists/* && \
    chown -R www-data:www-data /var/lib/nginx

VOLUME /var/www/html
WORKDIR /etc/nginx
EXPOSE 80

ENV CONTENT This text from the CONTENT variable

CMD ["nginx", "-g", "daemon off;"]
```

Let's add additional attribute for webpage content which will use value of `CONTENT` environment variable. Open `attributes/default.py`.

```python
header = "Tow Demo Webpage"
content = env["CONTENT"]
```

Modify webpage template `templates/index.html.tmpl`

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{header}}</title>
</head>

<body>
  <h1>{{header}}</h1>
  <p>{{content}}</p>
</body>

</html>
```

## Run and override

Finally build and try out our latest image.

```console
$ tow build -t tow-nginx-example
$ tow run -d -p 8080:80 --name tow-nginx-example tow-nginx-example
$ curl localhost:8080
<!DOCTYPE html>
<html>
<head>
  <title>Tow Demo Webpage</title>
</head>

<body>
  <h1>Tow Demo Webpage</h1>
  <p>This text from the CONTENT variable</p>
</body>

</html>
```

Well done! We got processed `index.html` with values from `header` and `content` attributes. Try out to override `CONTENT` environment variable.

```console
$ docker rm -f tow-nginx-example
$ tow run -d -p 8080:80 -e CONTENT="Override default CONTENT" --name tow-nginx-example tow-nginx-example
$ curl localhost:8080
<!DOCTYPE html>
<html>
<head>
  <title>Tow Demo Webpage</title>
</head>

<body>
  <h1>Tow Demo Webpage</h1>
  <p>Override default CONTENT</p>
</body>

</html>
```

And we've got a webpage with new content set in CONTENT env variable on `tow run` command. Now you can create Tow project by yourself and make configuration management for containers much easier.

If you want to get deep understanding of how `tow build` and `tow run` works checkout the next step.

### [Next: 3. Understanding Build and Run Commands](#)





