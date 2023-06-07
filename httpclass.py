import json

httpstatus={
    100:"100 Continue",
    200:"200 OK",
    400:"400 Bad request",
    500:"500 Internal server error",
    501:"501 Not implemented"
}

class httpmessage:
    def __init__(self) -> None:
        self._message
        self.status
        self.path
        self.start_line
        self.headers
        self.body

    def Do_get(self):
        pass
    def Do_post(self):
        self.status=httpstatus[501]
        self.make_response()
    def Do_Head(self):
        pass
    def Do_connect(self):
        self.status=httpstatus[501]
        self.make_response()
    def Do_delete(self):
        self.status=httpstatus[501]
        self.make_response()
    def make_response(self):
        self._message=f"""
HTTP/1.1 {self.status}
{self.headers}

{self.body}
        """
    def send_response(self, Socket):
        self.make_response()
        Socket.send(self._message.encode("utf-8"))