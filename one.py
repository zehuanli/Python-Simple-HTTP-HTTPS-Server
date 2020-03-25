import ssl, os, time, argparse, base64, logging, re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread


# config
WEB_ROOT_DIR = './www/'
CERT_LOCATION = '/path/to/fullchain.pem'
PRIV_KEY_LOCATION = '/path/to/privkey.pem'
CA_CERT_LOCATION = '/path/to/ca_cert.pem'

# fail2ban: failregex = \[ERROR\] HTTPS? +<HOST>: *\d{1,5} - code \d{3}.*$
file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(scheme)s %(message)s', datefmt='%m/%d/%y %H:%M:%S')
console_formatter = logging.Formatter('\033[%(color)dm[%(scheme)-5s %(asctime)s] %(message)s\033[0m', datefmt='%m/%d/%y %H:%M:%S')
file_handler = logging.FileHandler('/var/log/one.log', 'w', encoding='utf-8')
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

global key, cmd_args
key = None

class AuthHandler(SimpleHTTPRequestHandler):
  def send_header(self, keyword, value):
    if keyword not in ['Server', 'Last-Modified']:
      super().send_header(keyword, value)

  def do_GET(self):
    if key == None or self.headers.getheader('Authorization') == 'Basic ' + key:
      super().do_GET(self)
    else:
      self.log(True, 'code 401, basic authentication error')
      self.send_response(401)
      self.send_header('WWW-Authenticate', 'Basic realm=\"example.com\"')
      self.send_header('Content-type', 'text/html')
      self.end_headers()

  def log_request(self, code='-', size='-'):
    self.log(False, '"%s" %s %s', self.requestline, str(code), str(size))

  def log_error(self, format, *args):
    self.log(True, format, *args)

  def log(self, error, format, *args):
    is_https = self.server.server_port == cmd_args.https_port
    log_string = '%15s:%5d - %s'  % (self.client_address[0], self.client_address[1], format%args)
    log_extra = {'color': 31 if error else (33 if is_https else 37), 'scheme': 'HTTPS' if is_https else 'HTTP'}
    if error:
      logger.error(log_string, extra=log_extra)
    else:
      logger.info(log_string, extra=log_extra)

def start_server(daemon):
  if daemon:
    daemon.serve_forever()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Simple HTTP & HTTPS server in one.py')
  parser.add_argument('--http', dest='http', action='store_true', help='enable HTTP, which is disabled by default')
  parser.add_argument('--ip', dest='local_ip', type=str, help='local IP that listens for HTTP/HTTPS, default 0.0.0.0', default='0.0.0.0')
  parser.add_argument('--http-port', dest='http_port', type=int, help='HTTP port, default 80', default=80)
  parser.add_argument('--https-port', dest='https_port', type=int, help='HTTPS port, default 443', default=443)
  parser.add_argument('-u', '--user', dest='username', help='username for HTTP basic authentication')
  parser.add_argument('-p', '--pass', dest='password', help='password for HTTP basic authentication')
  parser.add_argument('-c', '--client-auth', dest='client_auth', action='store_true', help='require SSL client certificate authentication')
  cmd_args = parser.parse_args()
  if not re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', cmd_args.local_ip):
    parser.error('--ip should be a valid IPv4 address.')
  if cmd_args.http_port != 80 and not cmd_args.http:
    parser.error('--http-port specified while --http not set enabled.')
  if (cmd_args.username is None) ^ (cmd_args.password is None):
    parser.error('Either --user or --pass missing for HTTP basic authentication.')
  if cmd_args.username and cmd_args.password:
    key = base64.b64encode(cmd_args.username + ':' + cmd_args.password)
  if cmd_args.http and cmd_args.client_auth:
    parser.error('For security reasons, HTTP is not supported when SSL client certification authentication is enabled.')

  if cmd_args.http:
    http_daemon = HTTPServer((cmd_args.local_ip, cmd_args.http_port), AuthHandler)
  https_daemon = HTTPServer((cmd_args.local_ip, cmd_args.https_port), AuthHandler)
  ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  if cmd_args.client_auth:
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_verify_locations(cafile=CA_CERT_LOCATION)
  ssl_context.load_cert_chain(certfile=CERT_LOCATION, keyfile=PRIV_KEY_LOCATION)
  https_daemon.socket = ssl_context.wrap_socket(https_daemon.socket, server_side=True)

  os.chdir(WEB_ROOT_DIR)
  if cmd_args.http:
    http_t = Thread(target=start_server, args=(http_daemon,))
    http_t.daemon = True
    http_t.start()
  https_t = Thread(target=start_server, args=(https_daemon,))
  https_t.daemon = True
  https_t.start()
  logger.info('Server started, listening on ' + cmd_args.local_ip + ' port ' + str(cmd_args.https_port) + ' for HTTPS' + ((' and port ' + str(cmd_args.http_port) + ' for HTTP') if cmd_args.http else ''), extra={'color': 37, 'scheme': 'START'})
  # Keep running
  https_t.join()
