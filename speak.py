"""
Very simple HTTP server to get speak request

Usage::
    ./speak.py [<port>]

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import subprocess
import glob
import logging
import logging.handlers


LOG_FILENAME = 'log-speak.log'

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*5, backupCount=5)
handler.setFormatter(formatter)

my_logger.addHandler(handler)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed = dict(urlparse.parse_qsl(urlparse.urlsplit(self.path).query))
        if 'speak' in parsed:
            my_logger.info('speak => "%s"' % parsed['speak'])
            subprocess.Popen("./tts.sh '%s'" % parsed['speak'], shell=True)
   
        self._set_headers()
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print 'Starting httpd...'
    httpd.serve_forever()
    print 'Httpd stopped...'


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
