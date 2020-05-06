#!/usr/bin/python3
import os
import sys
import threading
import socket
import ssl

LISTEN = 200  # max
MAX_DATA_RECV = 999999  # bytes
BLOCKED = []
TIME_OUT = 20  # seconds

ALLOWED = {
    'ms-session': ('http', 'localhost', 8989, 'localhost')
}


class ProxyServer:

    def __init__(self, host='', port=8080):
        """
        inicializa el servidor socket
        """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen(LISTEN)
            print("listening [*] on {}:{}".format(host, port))
        except socket.error as e:
            print(e)
            if self.server:
                self.server.close()
            sys.exit(1)
        except Exception as e:
            print(e)
            if self.server:
                self.server.close()
            sys.exit(1)

    def run(self):
        """
        Se reciben y procesan las peticiones entrantes.
        """
        try:
            print("starting listening")
            while True:
                conn, client_addr = self.server.accept()
                request = conn.recv(MAX_DATA_RECV)
                backend_found = self.get_backend(request) # se busca el servidor backend con respecto a la url de entrada
                if not backend_found: # En el caso que no exista la url a procesar, se cierra el socket
                    conn.close()
                else:
                    #Se crea un hilo para procesar la petición y dar respecta al cliente.
                    threadx = threading.Thread(target=self.proxy_thread, args=(conn, client_addr, request, backend_found),)
                    threadx.start()
        except Exception as e:
            print(e)
            if self.server:
                self.server.close()
            sys.exit(1)

    def get_backend(self, request):
        """
        Busca el servidor back respecto a la url de procesamiento
        """
        if not request:
            return None
        first_line = str(request).split('\n')[0]
        url = first_line.split(' ')[1]
        port = None
        webserver = None
        protocol = None
        hostname = None
        for key in ALLOWED:
            if key in url:
                protocol = ALLOWED[key][0]
                webserver = ALLOWED[key][1]
                port = ALLOWED[key][2]
                hostname = ALLOWED[key][3]
                break
        return (protocol, webserver, port, hostname)

    def proxy_thread(self, conn, client_addr, request, backend_found):
        """
        Al iniciar el hilo, se invoca este metodo, valida si el back es http o https y redirecciona.
        """
        protocol = backend_found[0]
        if protocol == 'http':
            self.http(conn, client_addr, request, backend_found)
        elif protocol == 'https':
            self.https(conn, client_addr, request, backend_found)
        else:
            conn.close()
        

    def http(self, conn, client_addr, request, backend_found):
        """
        Procesa la peticion http y da respuesta al cliente
        """
        print("is HTTP")
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.resolve(s, conn, request, backend_found)
        except socket.error as e:
            print(e)
            if s:
                s.close()
            if conn:
                conn.close()
        except Exception as e:
            print(e)
            if s:
                s.close()
            if conn:
                conn.close()
        finally:
            return "http"

    def https(self, conn, client_addr, request, backend_found):
        """
        Procesa la peticion http y da respuesta al cliente
        """
        print("is HTTPS")
        hostname = backend_found[3]

        server_cert = 'server.crt'
        client_cert = 'client.crt'
        client_key = 'client.key'

        ss = None
        s = None
        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
            context.load_cert_chain(certfile=client_cert, keyfile=client_key)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss = context.wrap_socket(s, server_side=False, server_hostname=hostname)
            self.resolve(ss, conn, request, backend_found)
        except socket.error as e:
            print(e)
            if ss:
                ss.close()
            if conn:
                conn.close()
        except Exception as e:
            print(e)
            if ss:
                ss.close()
            if conn:
                conn.close()
        finally:
            return "https"

    def resolve(self, s, conn, request, backend_found):
        """
        Resuelve la petición
        """
        try:
            webserver = backend_found[1]
            port = backend_found[2]

            s.settimeout(TIME_OUT)
            s.connect((webserver, port))
            print("SOCKET established. Peer: {}".format(s.getpeername()))
            s.send(request)
            while 1:
                data = s.recv(MAX_DATA_RECV)
                if (len(data) > 0):
                    conn.send(data)
                else:
                    break
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            conn.close()
        except socket.error as e:
            print(e)
            if s:
                s.close()
            if conn:
                conn.close()
        except Exception as e:
            print(e)
            if s:
                s.close()
            if conn:
                conn.close()
