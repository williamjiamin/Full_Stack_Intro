from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

form = '''<!DOCTYPE html>
  <title>我的小贴吧</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">点我发布帖子</button>
  </form>
'''


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        #预判信息长度
        length = int(self.headers.get('Content-length', 0))

        #从request中读取数据.
        data = self.rfile.read(length).decode()

        #提取"message".
        message = parse_qs(data)["message"][0]

        #发送"message".
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self):
        # 发送200 OK.
        self.send_response(200)

        # 发送headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 加码并发送表格
        self.wfile.write(form.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
