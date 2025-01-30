import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 4403))  # Use the correct port
    server_socket.listen(1)
    print("Server started and listening on port 4403")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Hello, client!")
        client_socket.close()

start_server()
