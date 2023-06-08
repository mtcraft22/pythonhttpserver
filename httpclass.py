import json
import socket

#levantamos el socket tcp para cominicanos con el navegador via http
servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor.bind(("localhost",8080))
servidor.listen(5)

# codigos de etado http 
httpstatus={
    100:"100 Continue",
    200:"200 OK",
    400:"400 Bad request",
    500:"500 Internal server error",
    501:"501 Not implemented"
}
# extenciones de archivos mimes 
httpmimes={
    #text files
    "txt":"text/plain",
    "js":"text/javascript",
    "html":"text/html",
    "css":"text/css",
    #images formts
    "jpeg":"image/jpeg",
    "gif":"image/gif",
    "png":"image/png",
    "svg":"image/svg+xml",
    "ico":"image/x-incon",
    #binary partition
    "byte_range":"multipart/byteranges",
    "formulario_multiparte":"multipart/form-data",
    #audio
    "waw":"audio/waw",
    "ogg":"audio/ogg",
    "webm":"audio/webm",
    "midi":"audio/midi",
    #video
    "webm":"video/webm",
    "ogg":"video/ogg",
    "mp4":"video/mp4",
    #binario
    "otro":"application/octet-stream",
    "pkcs12":"application/pkcs12",
    "vnd.mspowerpoint":"application/vnd.mspowerpoints",
    "xhtml":"application/xhtml+xml",
    "xml":"application/xml",
    "pdf":"application/pdf",

     
    
}

class httpmessage:
    def __init__(self) -> None:
        self._message
        self.status
        self.path
        self.start_line
        self.headers
        self.body
    def send_status_code(self,code):
        self._message=f"""
HTTP/1.1 {code}\r\n
        """
    def send_header(self,key,value):
        pass
    def send_body(self,body):
        pass
    def end_header(self):
        self._message+=" \r\n"

    def Do_Options(self):
        self.send_response(httpstatus[501])
    def Do_patch(self):
        self.send_response(httpstatus[501])
    def Do_Put(self):
        self.send_response(httpstatus[501])
    def Do_Trace(self):
        self.send_response(httpstatus[501])
    def Do_get(self):
        pass
    def Do_post(self):
        self.send_response(httpstatus[501])
    def Do_Head(self):
        pass
    def Do_connect(self):
        self.send_response(httpstatus[501])
    def Do_delete(self):
        self.send_response(httpstatus[501])

    
    def make_response(self):
        self._message=f"""
HTTP/1.1 {self.status}
{self.headers}

{self.body}
        """
    def send_response(self, Socket):
        self.make_response()
        Socket.send(self._message.encode("utf-8"))
    def run_forever(self):
        while True:
            enchufe, direcion = servidor.accept()
            self._message=enchufe.recv(1024).decode("utf-8")

            comamd=self._message.split(" ")[0]

            match comamd:
                case "CONNECT":
                    self.Do_connect()
                case "DELETE":
                    self.Do_delete()
                
            
            self.send_response()
            enchufe.close()
