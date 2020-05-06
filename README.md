# ms-proxy

Servidor Proxy en Python 3.8, basado en SOCKET, ayudando a centralizar todas las solicitudes entrantes en un solo punto, lo cual puede mejorar en cierto punto los niveles de seguridad de una aplicación. 
Al implementar o usar un proxy permite la apertura de un solo puerto, es decir, que se pueden tener a nivel de servidor muchas aplicaciones, pero solo se podrá acceder a ellas por medio del proxy.
El objetivo de esta publicación es crear un Servidor Proxy Web con las siguientes características:
```
Por cada petición entrante, el servidor crea una nueva conexión al servidor destino.
La solicitud entrante será enviada al servidor destino.
La solicitud entrante recibirá una respuesta por parte del servidor destino.
El Proxy aceptará muchas peticiones simultaneas.
El Proxy debe responder en los menores tiempos, es decir, manejar alto rendimiento y responder todas las peticiones.
El Proxy debe consumir pocos recursos máquina.
```


# Running 
El proxy fue construido en Python 3.7.

### Ejecución

Para ejecutar cualquiera de los dos comandos:
```
python3 app.py
```
nohup python3 -u ./app.py > ./output.log &
```
