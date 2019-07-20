import BaseHTTPServer, ssl, os, time, sys, base64
from SimpleHTTPServer import SimpleHTTPRequestHandler
from threading import Thread

global key
key = None

class AuthHandler(SimpleHTTPRequestHandler, object):
  def send_header(self, keyword, value):
    if keyword not in ['Server', 'Last-Modified']:
      super(AuthHandler, self).send_header(keyword, value)

  def do_GET(self):
    if key == None or self.headers.getheader('Authorization') == 'Basic ' + key:
      SimpleHTTPRequestHandler.do_GET(self)
    else:
      self.send_response(401)
      self.send_header('WWW-Authenticate', 'Basic realm=\"example.com\"')
      self.send_header('Content-type', 'text/html')
      self.end_headers()

  def log_request(self, code='-', size='-'):
    self.log(False, '"%s" %s %s', self.requestline, str(code), str(size))

  def log_error(self, format, *args):
    self.log(True, format, *args)

  def log(self, error, format, *args):
    if error:
      sys.stderr.write('\n')
    if self.server.server_port == 443:
      sys.stderr.write('\033[%dm[HTTPS %s] %15s:%5d - %s\033[0m\n'  % (31 if error else 33, self.log_date_time_string(), self.client_address[0], self.client_address[1], format%args))
    else:
      sys.stderr.write('\033[%dm[HTTP  %s] %15s:%5d - %s\033[0m\n'  % (31 if error else 37, self.log_date_time_string(), self.client_address[0], self.client_address[1], format%args))

  def log_date_time_string(self):
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = '%02d/%02d/%04d %02d:%02d:%02d' % (day, month, year, hh, mm, ss)
    return s


def start_server(daemon):
  if daemon:
    daemon.serve_forever()


if __name__ == '__main__':
  if len(sys.argv) >= 2:
    # Usage: one.py [username:password]
    key = base64.b64encode(sys.argv[1])
  server = BaseHTTPServer.HTTPServer
  handler = AuthHandler
  http_daemon = server(('0.0.0.0', 80), handler)
  https_daemon = server(('0.0.0.0', 443), handler)
  https_daemon.socket = ssl.wrap_socket(https_daemon.socket, certfile='/path/to/fullchain.pem', keyfile='/path/to/privkey.pem', server_side=True)
  os.chdir('www')
  http_t = Thread(target=start_server, args=(http_daemon,))
  http_t.daemon = True
  https_t = Thread(target=start_server, args=(https_daemon,))
  https_t.daemon = True
  http_t.start()
  https_t.start()
  print("server started")
  while True:
    time.sleep(1)
