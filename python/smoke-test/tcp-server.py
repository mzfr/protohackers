import asyncio, socket
from io import BytesIO


async def handle_client(reader, writer): 
    send_data = BytesIO()

    while True:
        try:
            data = await asyncio.wait_for(reader.read(8192), timeout=2.0)
            send_data.write(data)
            if reader.at_eof(): break
        except (asyncio.CancelledError, asyncio.TimeoutError):
            break

    writer.write(send_data.getvalue())
    await writer.drain()

    if writer.can_write_eof():
        writer.write_eof()

    writer.close()

async def run_server():
    server = await asyncio.start_server(
            client_connected_cb=handle_client,
            host="0.0.0.0",
            port=5999,
            family=socket.AF_INET
        )
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(run_server())
