"""
Async/Await Server
------------------
Modern Python approach using asyncio.
Handles many clients efficiently with single thread.
Best for: I/O-bound operations, high concurrency, modern applications.
"""

import asyncio

HOST = '127.0.0.1'
PORT = 9002

async def handle_client(reader, writer):
    """
    Handle a client connection asynchronously.
    
    Args:
        reader: StreamReader for receiving data
        writer: StreamWriter for sending data
    """
    # Get client address
    addr = writer.get_extra_info('peername')
    print(f"\nClient connected: {addr[0]}:{addr[1]}")
    
    try:
        # Receive data (asynchronously, doesn't block other clients)
        data = await reader.read(1024)
        message = data.decode('utf-8')
        print(f"  [{addr[0]}:{addr[1]}] Received: {message}")
        
        # Simulate slow processing (asynchronously)
        print(f"  [{addr[0]}:{addr[1]}] Processing (2 seconds)...")
        await asyncio.sleep(2)  # This doesn't block other clients!
        
        # Send response
        response = f"Processed: {message}"
        writer.write(response.encode('utf-8'))
        await writer.drain()  # Ensure data is sent
        
        print(f"  [{addr[0]}:{addr[1]}] Response sent")
        
    except Exception as e:
        print(f"  [{addr[0]}:{addr[1]}] Error: {e}")
    
    finally:
        # Close connection
        writer.close()
        await writer.wait_closed()
        print(f"  [{addr[0]}:{addr[1]}] Connection closed")

async def main():
    """
    Main async server loop.
    Creates server and runs forever.
    """
    print("=" * 60)
    print("Async/Await Server")
    print("=" * 60)
    print(f"Starting async server on {HOST}:{PORT}")
    print("Handles multiple clients concurrently with single thread")
    print("Press Ctrl+C to stop\n")
    
    # Create async server
    # start_server creates a server that calls handle_client for each connection
    server = await asyncio.start_server(
        handle_client,  # Function to call for each client
        HOST,
        PORT
    )
    
    # Get server address
    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr[0]}:{addr[1]}\n")
    
    # Run server forever
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        # Run the async event loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")