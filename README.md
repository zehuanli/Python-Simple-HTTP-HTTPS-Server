# Python Simple HTTP HTTPS Server

## Installation

1. Set path to HTTPS certificate chain `certfile` and private key `keyfile` in `one.py`. For example: 
   *`certfile='/etc/letsencrypt/live/example.com/fullchain.pem'`*
   *`keyfile='/etc/letsencrypt/live/example.com/privkey.pem'`*
1. Make a `./www/` directory, which will be the web root.

## Usage
~~~
python one.py [-h] [--http] [--ip LOCAL_IP] [--http-port HTTP_PORT]
              [--https-port HTTPS_PORT] [-u USERNAME] [-p PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  --http                enable HTTP, which is disabled by default
  --ip LOCAL_IP         local IP that listens for HTTP/HTTPS, default 0.0.0.0
  --http-port HTTP_PORT
                        HTTP port, default 80
  --https-port HTTPS_PORT
                        HTTPS port, default 443
  -u USERNAME, --user USERNAME
                        username for HTTP basic authentication
  -p PASSWORD, --pass PASSWORD
                        password for HTTP basic authentication
~~~

## Features implemented

- HTTP and HTTPS in one Python script
- HTTP disabled by default for better security
- Options to change source IP, HTTP and/or HTTPS ports
- Optional basic authentication
- Remove headers that may contain sensitive information (`Server`, `Last-Modified` etc.)
- Better(-ish) logging format
- Store fail2ban-friendly logs stored in `/var/log/one.log`
