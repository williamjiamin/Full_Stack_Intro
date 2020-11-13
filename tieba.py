from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

memory=[]

form = '''
    <!DOCTYPE html>
    <title>威廉的测试小论坛</title>
    <form method="POST">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">按我发布帖子</button>
    </form>
    <pre>
    {}
    </pre>
'''


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        data = self.rfile.read(length).decode()
        message = parse_qs(data)["message"][0]
        message = message.replace("<", "&lt;")
        memory.append(message)

        self.send_response(303)
        self.send_header('Location','/')
        self.end_headers()



    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        mesg=form.format("\n".join(memory))
        self.wfile.write(mesg.encode())

if __name__ =='__main__':
	server_address=('',9999)
	httpd=HTTPServer(server_address,Handler)
	httpd.serve_forever()