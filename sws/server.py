import cgi
import json
import logging
from email.parser import Parser
from functools import lru_cache
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlparse
from app import controller
import threading
import app.templates
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
    class пока не используется
    """
    def __init__(self, headers):
        self.headers = headers
        self.set_cookies = None

    def _parse_cookies(self, cookie_str, dictionary) -> dict:
        """Tries to parse any key-value pairs of cookies in a string,
        then updates the the dictionary with any key-value pairs found.

        **Example**::
            dictionary = {}
            _parse_cookies('my=value', dictionary)
            # Now the following is True
            dictionary['my'] == 'value'

        :param cookie_str: A string containing "key=value" pairs from an HTTP "Set-Cookie" header.
        :type cookie_str: ``str``
        :param dictionary: A dictionary to update with any found key-value pairs.
        :type dictionary: ``dict``
        """
        parsed_cookie = SimpleCookie(cookie_str)
        for cookie in parsed_cookie.values():
            dictionary[cookie.key] = cookie.coded_value
        return dictionary


class Request:
    def __init__(self, method, target, version, headers, rcookies, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile
        self.rcookies = rcookies
        self.cookies_modyficate = False

    @property
    def path(self):
        return self.url.path

    # def get_cookies(self):
    #     print(type(self.headers))

    @property
    def get_content(self):
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
    def __init__(self, status, reason, headers=None, body=None, rcookies=None, cookies_modyficate=False):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
        self.rcookies = rcookies
        self.cookies_modyficate = cookies_modyficate


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
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        logger.debug(headers)
        host = headers.get('Host')
        """
        Cookies
        1.
        В переменную rcookies кладется str(массив) с токеном киента 
        и всеми имеющимися куками сервиса 
        пример:
        csrftoken=op9bz4JTvT5LLHjv0FSNsXMWGgNS4aHG58t2kwA6rvctrbbA6gk; auth_key=asdf12334
        """
        rcookies = headers.get('Cookie')
        if not host:
            raise HTTPError(400, 'Bad request',
                            'Host header is missing')
        if method not in ('POST', 'GET'):
            raise HTTPError(400, 'Bad request',
                            f"can not handle {method} request")
        # if host not in (self._server_name,
        #                 f'{self._server_name}:{self._port}'):
        #     print('тут мб ошибка')
        #     raise HTTPError(404, 'Not found')
        """
        Cookies
        2. Переменная rcookies кладется в объект Request, чтобы внутренний клиент фреймворка мог
        ориентировать логику, например авторизации на контроллере, как частный случай и для отладки
        
        """
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
            print(type(line))
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                logger.debug(f"req_line {headers}")
                raise HTTPError(494, 'Too many headers')
        # print(SimpleCookie().value_encode(headers))

        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        """
        Cookies
        3.Здесь я, как внутренний клиент, вызвавший объект request, могу постучаться
        в него и взаимодействовать с атрибутом req.rcookies, обогощая его
        на текущий момент обязательно под формат headers, где это массив тюплов.
        пример из контроллера:
        request.rcookies = [
                ('Set-cookie', 'auth_key=asdf12334'),
                ('Set-cookie', 'any_key=123355; Domain=example.com; Expires=Thu, 12-Jan-2017 13:55:08 GMT; Path=/'')
                ]

        Необходимо учитывать, что в объекте req.rcookies до обогащения изначально лежит
        неразделенная строка, преподалагется реализация некого метода, который будет
        валидировать и принимать решения

        На текущий момент для принятия решения есть булевый флаг у объектов Response и Request,
        который изменяется на контроллере
        пример:
        request.cookies_modyficate = True

        этот фллаг в send_response запустит перебор объектов кукисов по аналогии,
        как перебираются заголовки
        """
        body = self.response(path=req.path, method=req.method, request=req)
        """
        Cookies
        4.объявляем rcookies для объекта Response
        """
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
            cookies_modyficate=req.cookies_modyficate
        )
        return resp

    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        logger.debug(f"status_line response {status_line}")
        wfile.write(status_line.encode('iso-8859-1'))

        if resp.headers:
            for (key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))
        """
        Повтор инструкции:
        Cookies
        5. Если внутренний клиент фреймворка что-либо кладет в кукисы, для отправки на клиента нужно заполнить флаг"""
        if resp.cookies_modyficate:
            for (key, value) in resp.rcookies:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if resp.body:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def response(self, path, method, request):
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
