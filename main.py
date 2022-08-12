from contextlib import asynccontextmanager
import datetime
import sys
import asyncio
import command
from server import Server

ip = '0.0.0.0'
port = 8001


async def stdin(reader, server: Server):
    async for data in reader:
        print('outgoing', data)
        server.send(command.encode('AFSTATUS'))
        print('sent')


async def connect_stdin():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


@asynccontextmanager
async def start_std(server: Server):
    reader = await connect_stdin()
    loop = asyncio.get_running_loop()
    task = loop.create_task(stdin(reader, server))

    try:
        yield reader
    finally:
        task.cancel()


async def main():
    server = Server(ip=ip, port=port)
    async with start_std(server):
        print('server started')
        with server as stream, open('{}.game'.format(datetime.datetime.now().isoformat()), 'w') as infile:
            async for data in stream:
                if data == b'':
                    return
                infile.write(data.decode())
                print('incoming', data)

asyncio.run(main())
