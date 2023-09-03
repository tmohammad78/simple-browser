import socket

class URL:
    def __init__(self,url) -> None:
        self.scheme,url = url.split("://",1)
        assert self.scheme == "http", \
            "Unknown scheme {}".format(self.scheme)
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/",1)
        self.path = "/" + url
    
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        s.connect((self.host, 80))

        s.send(("GET {} HTTP/1.0\r\n".format(self.path) + \
                "Host: {}\r\n\r\n".format(self.host)) \
               .encode("utf8"))
    
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        assert status == "200", "{}: {}".format(status, explanation)