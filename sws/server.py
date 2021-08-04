import json
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
from app import controller
import app.templates
import socket

MAX_LINE = 64 * 1024
MAX_HEADERS = 100


class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class Server:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._users = {}

    def serve_forever(self):
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.server_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def server_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            req.rfile.close()
            conn.close()

    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Bad request',
                            'Host header is missing')
        # if host not in (self._server_name,
        #                 f'{self._server_name}:{self._port}'):
        #     print('тут мб ошибка')
        #     raise HTTPError(404, 'Not found')
        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise HTTPError(400, 'Bad request',
                            'Request line is too long')

        req_line = str(raw, 'iso-8859-1')
        words = req_line.split()
        if len(words) != 3:
            raise HTTPError(400, 'Bad request',
                            'Malformed request line')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')
        return method, target, ver

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(494, 'Request header too large')

            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise HTTPError(494, 'Too many headers')

        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        """
        диспетчеризация запросов
        """
        print('я в диспейтчерской')
        body = self.response(path=req.path, method=req.method)
        # print('даже тело есть:')
        # print(body)
        body = body.encode('utf-8')
        contentType = 'text/html; charset=utf-8'
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]

        resp = Response(200, 'OK', headers=headers, body=body)
        return resp

    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        print(status_line)
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            print('if resp headers OK')
            print(resp.headers)
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                print(header_line)
                wfile.write(header_line.encode('iso-8859-1'))
                print(wfile)
        wfile.write(b'\r\n')

        if resp.body:
            # print('if resp body OK')
            # print(resp.body)
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def response(self, path, method):
        key_func = f'{method} {path}'
        with open('path.json', 'r') as outfile:
            rout = json.load(outfile)
        if key_func in rout:
            print('я в бизнес логику уйти попробую')
            f = getattr(controller, rout[key_func])
            return f()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(conn, resp)


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self.rfile.read(size)


if __name__ == '__main__':
    # host = sys.argv[1]
    # port = int(sys.argv[2])
    # name = sys.argv[3]

    serv = Server(host='127.0.0.1', port=9000, server_name='some')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
    # serv = Server(host='127.0.0.1', port=9000, server_name='some')
    # print(serv.response(path='/auth', method='GET'))
