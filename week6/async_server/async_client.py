"""
Async Client
------------
Async client to test the async server.
"""

import asyncio

async def send_request(server_host, server_port, client_id):
    """
    Send request to async server.
    """
    try:
        # Open connection (async)
        reader, writer = await asyncio.open_connection(server_host, server_port)
        
        print(f"[Client {client_id}] Connected")
        
        # Send message
        message = f"Hello from async client {client_id}"
        writer.write(message.encode('utf-8'))
        await writer.drain()
        
        # Receive response
        data = await reader.read(1024)
        response = data.decode('utf-8')
        
        print(f"[Client {client_id}] Received: {response}")
        
        # Close connection
        writer.close()
        await writer.wait_closed()
        
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")

async def main():
    """
    Create multiple concurrent client connections.
    """
    print("=" * 60)
    print("Testing Async Server")
    print("=" * 60)
    print("Sending 5 simultaneous requests...\n")
    
    # Create 5 concurrent client tasks
    tasks = []
    for i in range(1, 6):
        task = send_request('127.0.0.1', 9002, i)
        tasks.append(task)
    
    # Run all tasks concurrently
    import time
    start = time.time()
    await asyncio.gather(*tasks)
    elapsed = time.time() - start
    
    print(f"\n{'=' * 60}")
    print(f"All 5 clients completed in {elapsed:.2f} seconds")
    print("With async server, this should be ~2 seconds")
    print("(All clients handled concurrently)")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    asyncio.run(main())