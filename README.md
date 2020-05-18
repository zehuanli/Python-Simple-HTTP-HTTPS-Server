# Python Simple HTTP HTTPS Server

**[Python3 is required](https://pythonclock.org/), but should be easy to make it work with Python2**

## Installation
1. Change the following constants in the "config" block in `one.py`:
    - `WEB_ROOT_DIR`: Web root directory. Make sure that the folder exists and **does not contain any sensitive data that you don't want to share**.
    - `CERT_LOCATION`: Server certificate chain file.
    - `PRIV_KEY_LOCATION`: Private key to server certificate.
    - `CA_CERT_LOCATION`: (optional) CA certificate for client certificate authentication.

    For example:
    ~~~python
    WEB_ROOT_DIR = './www'
    CERT_LOCATION = '/etc/letsencrypt/live/example.com/fullchain.pem'
    PRIV_KEY_LOCATION = '/etc/letsencrypt/live/example.com/privkey.pem'
    CA_CERT_LOCATION = '/path/to/ca_cert.pem'
    ~~~

1. Run `one.py` following the usage below.

## Usage
~~~
python3 one.py [-h] [--http] [--ip LOCAL_IP] [--http-port HTTP_PORT]
              [--https-port HTTPS_PORT] [-u USERNAME] [-p PASSWORD] [-c]

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
  -c, --client-auth     require SSL client certificate authentication
~~~

## Features implemented

- HTTP and HTTPS in one Python script
- HTTP disabled by default for better security
- Options to change source IP, HTTP and/or HTTPS ports
- Basic authentication
- Client certificate authentication
- Remove headers that may contain sensitive information (`Server`, `Last-Modified` etc.)
- Errors are logged, but never sent out
- Better(-ish) logging format
- Store fail2ban-friendly logs stored in `/var/log/one.log`
