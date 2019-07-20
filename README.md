# Python-Simple-HTTP-HTTPS-Server

## Installation

1. Set path to HTTPS certificate chain `certfile` and private key `keyfile` in `one.py`.
1. Make a `./www/` directory, which will be the web root.
1. Usage: `python one.py [username:password]`

## Features implemented

- HTTP and HTTPS in one
- Basic authentication
- Remove headers that may contain sensitive information (`Server`, `Last-Modified` etc.)
- Better(-ish) logging format
