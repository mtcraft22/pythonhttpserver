import socket

servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind(("localhost",8080))

servidor.listen(5)

with open("hola.html","r") as html:
    Html=html.read()

while True:
    enchufe, direcion = servidor.accept()
    solicitud=enchufe.recv(1024).decode("utf-8")
    try:
        if solicitud.splitlines()[0].split(" ")[1] != "/":
            print(f".{solicitud.splitlines()[0].split(' ')[1]}")
            with open(f".{solicitud.splitlines()[0].split(' ')[1]}","r") as html:
                Html=html.read()
        else:
            with open(f"hola.html","r") as html:
                Html=html.read()
        if solicitud.splitlines()[0].split(' ')[1].split(".")[1]=="html":
            tipo='text/html'
        else:
            tipo='text/css'
        respuesta=f"""
HTTP/1.1 200 OK
Content-Type: {tipo}

{Html}
        """
    except Exception:
        respuesta="""
HTTP/1.1 400 Bad request
Recurso: No encontrado o no tienes permisos
        """

    print(solicitud)
    enchufe.send(respuesta.encode('utf-8'))
    enchufe.close()
