import cgi
import json
import logging
from email.parser import Parser
from functools import lru_cache
from http import cookies
from urllib.parse import parse_qs, urlparse
from app import controller
import threading
import socket

MAX_LINE = 64 * 1024
MAX_HEADERS = 100

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body


class Cookies:
    """
    Объект, в котором хранятся и модифицируются кукисы
    в рамках клиент-серверного взаимодействия;
    """

    def __init__(self, cookies):
        self.cookies = cookies
        self.set_cookies = False


class Request:
    def __init__(self, method, target, version, headers, rcookies, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile
        self.rcookies = rcookies

    @property
    def path(self):
        return self.url.path

    @property
    def get_content(self):
        """
        Возвращает параметры только из multipart/form-data;
        """
        logger.debug('get_content')
        content = {}
        try:
            logger.debug(f"Content-type: {self.headers['Content-type']}")
            ctype, pdict = cgi.parse_header(self.headers['Content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT_LENGTH'] = content_len
            logger.debug(f'ctype, pdict: {ctype, pdict}')
            if ctype == 'multipart/form-data':
                logger.debug(f'if ctype == multipart/form-data success')
                content = cgi.parse_multipart(fp=self.rfile, pdict=pdict)
                logger.debug(f'fields: {content}')
        except Exception as exc:
            logger.debug(f"Error with parse request content {exc}")
        return content

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


class Response:
    def __init__(self, status, reason, rcookies, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
        self.rcookies = rcookies


class Server:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._users = {}

    def create_server(self):
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)
        serv_sock.bind((self._host, self._port))
        serv_sock.listen()
        return serv_sock

    def serve_forever(self):
        cid = 0
        try:
            serv_sock = self.create_server()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    t = threading.Thread(target=self.server_client,
                                         args=(conn, cid))
                    t.start()
                    cid += 1
                except Exception as e:
                    logger.debug('Client serving failed', e)
        finally:
            serv_sock.close()

    def server_client(self, conn, cid):
        """
        Основные клиент-серверные взаимодействия;
        """
        try:
            logger.debug(f'create connect in server_client {cid}')
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
        """
        Глобально ф-я парсит заголовок запроса и заполняет объект Request;

        Но также отрабатывает обработчик кукисов:
        Переменная rcookies принимает class Cookies;
        В class Cookies кладутся кукисы из заголовка:
        headers.get('Cookie') -> csrftoken=op9bz4JTvT5LG58t2kwA6rvctrbbA6gk; auth_key=asdf12334; any_key=123355
        rcookies кладется в объект Request и передается дальше;
        """
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        logger.debug(headers)
        host = headers.get('Host')
        rcookies = Cookies(cookies=headers.get('Cookie'))
        if not host:
            raise HTTPError(400, 'Bad request',
                            'Host header is missing')
        if method not in ('POST', 'GET'):
            raise HTTPError(400, 'Bad request',
                            f"can not handle {method} request")
        # if host not in (self._server_name,
        #                 f'{self._server_name}:{self._port}'):
        #     raise HTTPError(404, 'Not found')
        return Request(method=method,
                       target=target,
                       version=ver,
                       headers=headers,
                       rcookies=rcookies,
                       rfile=rfile)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        logger.debug(f'parse_request_line: {raw}')
        if len(raw) > MAX_LINE:
            raise HTTPError(400, 'Bad request',
                            'Request line is too long')

        req_line = str(raw, 'iso-8859-1')
        logger.debug(f"req_line {req_line}")
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
                logger.debug(f"req_line {headers}")
                raise HTTPError(494, 'Too many headers')

        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        """
        В ф-ю возвращается контент сервиса;
        На стороне контроллера можно произвести также взаимодействия с кукисами;
        Подгатавливаются заголовки;
        Возвращает объект Response;
        """
        body = self.response(path=req.path, method=req.method, request=req)
        rcookies = req.rcookies
        body = body.encode('utf-8')
        contentType = 'text/html; charset=utf-8'

        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))
                   ]

        resp = Response(
            200,
            'OK',
            headers=headers,
            body=body,
            rcookies=rcookies,
        )
        return resp

    def send_response(self, conn, resp):
        """
        Если внутренний клиент фреймворка что-либо кладет в кукисы -
        request.rcookies.cookies = [('Set-cookie', 'some_key=123355')]
        Если булевй флаг выставлен в True - request.rcookies.set_cookies = True
        Помимо ответа с контентом будет произведена запись кукисов в бразузер;
        """
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        logger.debug(f"status_line response {status_line}")
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        if resp.rcookies.set_cookies:
            for (key, value) in resp.rcookies.cookies:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def response(self, path, method, request):
        """
        Читает json с маршрутами и запускает ф-ю на контроллере;
        """
        key_func = f'{method} {path}'
        with open('path.json', 'r') as outfile:
            rout = json.load(outfile)
        if key_func in rout:
            logger.debug("go to routing")
            f = getattr(controller, rout[key_func])
            return f(request)

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
