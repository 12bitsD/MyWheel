import socket
import ssl

class URL:
    def __init__(self,url):
        #identify use 80s or 443 port,depends on http/https
        #strip the host ,url,path
        self.scheme,url = url.split("://",1)
        assert self.scheme in ["http","https"]
        if self.scheme =="http":
            self.port=80
        elif self.scheme=="https":
            self.port =443

        #add / in end of url if url hasn't
        if '/' not in url:
            url = url + '/'
        #filter the url and host (ex:aosabook.org/en/500L/a-simple-web-server.html)
            #host==>aosabook.org, url= en/500L/a-simple-web-server.html
        self.host, url = url.split('/', 1)
        self.path = '/' + url

        #parse the port in url///if the port include in host, use this port to access.
        if ':' in self.host:
            self.host,port =self.host.split(":",1)
            self.port =int(port)
    def request(self):
        #create socket,if https,warp the socket.

        s=socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        #process the HTTPS SOCKET
        if self.scheme=='https':
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        #connecting
        s.connect((self.host,self.port))
        #use get method to recieved info, and make a file reading to shows
        # ...
        s.send(("GET {} HTTP/1.0\r\n".format(self.path)+"Host: {}\r\n\r\n".format(self.host)).encode("utf8"))
        respond=s.makefile('r',encoding='utf8',newline='\r\n')
        statusline=respond.readline()
        version,status,explaination=statusline.split(" ",2)

        response_header={}
        while True:
            line = respond.readline()
            if line=='\r\n': break
            header,value = line.split(":",1)
            response_header[header.lower()]=value.strip()

        assert "transfer-encoding" not in response_header
        assert  "content-encoding" not in response_header
        body = respond.read()
        s.close()

        return body

def show(body):
    in_tag=False
    for c in body:
        if c=="<":
            in_tag=True
        elif c==">":
            in_tag=False
        elif not in_tag:
            print(c,end='')
def load(url):
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))

