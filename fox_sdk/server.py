from contextlib import ContextDecorator
from asgiref.sync import sync_to_async
import socket


class Server(ContextDecorator):
    ip: int
    port: str
    started = False
    socket: socket.socket
    connection = socket.socket
    buffer_size = 4096

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def start(self):
        assert not self.started, 'server is already started'
        self.started = True
        s = self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(1)

        self.conn, self.address = s.accept()

    def close(self, *exec):
        self.conn.close()

    def send(self, data: bytes):
        self.conn.send(data)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.conn.close()
        self.socket.close()
        self.started = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        recv = sync_to_async(self.conn.recv, thread_sensitive=False)
        data = await recv(self.buffer_size)
        return data
