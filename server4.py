from socket import *
import os

# 1. 서버 소켓 설정 (포트 80)
s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 8080))
s.listen(10)

print("Web Server is running on port 80...")

while True:
    # 2. 클라이언트 연결 대기
    c, addr = s.accept()
    
    data = c.recv(1024)
    if not data:
        c.close()
        continue
        
    msg = data.decode()
    req = msg.split('\r\n')
    
    # 3. 요청 라인 파싱 (예: GET /index.html HTTP/1.1)
    if len(req) > 0:
        request_line = req[0].split(' ')
        if len(request_line) > 1:
            filename = request_line[1].lstrip('/')
            
            # 기본 경로 설정
            if filename == "":
                filename = "index.html"

            # 4. 파일 존재 여부 확인 및 처리
            if os.path.exists(filename):
                # MIME 타입 설정
                if filename.endswith(".html"):
                    f = open(filename, 'r', encoding='utf-8')
                    content = f.read()
                    mimeType = 'text/html; charset=utf-8'
                    header = f'HTTP/1.1 200 OK\r\nContent-Type: {mimeType}\r\n\r\n'
                    c.send(header.encode())
                    c.send(content.encode())
                    f.close()
                else:
                    # 이미지 파일 처리 (iot.png, favicon.ico)
                    f = open(filename, 'rb')
                    content = f.read()
                    if filename.endswith(".png"):
                        mimeType = 'image/png'
                    elif filename.endswith(".ico"):
                        mimeType = 'image/x-icon'
                    
                    header = f'HTTP/1.1 200 OK\r\nContent-Type: {mimeType}\r\n\r\n'
                    c.send(header.encode())
                    c.send(content) # 바이너리 데이터는 바로 전송
                    f.close()
            else:
                # 5. 파일이 없는 경우 404 Not Found 전송
                header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                body = '<HTML><HEAD><TITLE>Not Found</TITLE></HEAD><BODY>Not Found</BODY></HTML>'
                c.send(header.encode())
                c.send(body.encode())
    
    # 6. 전송 후 소켓 닫기
    c.close()