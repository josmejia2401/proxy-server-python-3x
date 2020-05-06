#!/usr/bin/python3
import sys
from providers.proxy import ProxyServer

if __name__ == '__main__':
    try:
        server = ProxyServer(port = 8080)
        server.run()
    except KeyboardInterrupt as e:
        print ("Ctrl C - Stopping server", e)
        sys.exit(1)
    except Exception as e:
        print ("Stopping server", e)
        sys.exit(1)
