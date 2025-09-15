import http.server
import socketserver

PORT = 8080

def run_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving web GUI at http://localhost:" + str(PORT))
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()