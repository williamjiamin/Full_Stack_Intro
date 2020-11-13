from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
from urllib.parse import parse_qs


form = '''<!DOCTYPE html>
<title>你要小心了，每个网站都在读取你的信息</title>
<p>
{}
<p>
<form method="POST">
<label>请输入你的年龄
<input type="text" name="yourage">
</label>
<br>
<button type="submit">傻乎乎的提交年龄</button>
</form>
'''

class ageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        
        data = self.rfile.read(length).decode()
        yourage = parse_qs(data)["yourage"][0]

        c = cookies.SimpleCookie()
        c['yourage'] = yourage
        c['yourage']['domain'] = 'localhost'
        c['yourage']['max-age'] = 10

        self.send_response(303)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', c['yourage'].OutputString())
        self.end_headers()

    def do_GET(self):
        message="您好，请您输入您的年龄~"

        if 'cookie' in self.headers:
            try:
                c=cookies.SimpleCookie(self.headers['cookie'])
                age=c['yourage'].value
                if int(age) > 40:
                    message="快服用XXXX，延缓衰老，您值得拥有~"
                elif int(age) > 25:
                    message="XXXX牌化妆品，美容养颜，让您焕发光彩！"
                else:
                    message="XXXX网校，好好学习天天向上，为您全面辅导！"

            except (KeyError, cookies.CookieError) as e:
                message="不好意思，我没有找到您的信息。"
                print(e)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        mesg=form.format(message)
        self.wfile.write(mesg.encode())

if __name__=='__main__':
    server_address =('',9999)
    httpd=HTTPServer(server_address,ageHandler)
    httpd.serve_forever()