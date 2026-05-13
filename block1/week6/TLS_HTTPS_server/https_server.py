"""
Complete HTTPS Server
---------------------
A functional HTTPS server using async + TLS.
Combines async efficiency with TLS security.
"""

import asyncio
import ssl

HOST = '127.0.0.1'
PORT = 8443
CERT_FILE = 'server-cert.pem'
KEY_FILE = 'server-key.pem'

async def handle_http_request(reader, writer):
    """
    Handle HTTP request and send HTML response.
    """
    addr = writer.get_extra_info('peername')
    print(f"\nHTTPS request from {addr[0]}:{addr[1]}")
    
    try:
        # Read HTTP request
        request_data = await reader.read(4096)
        request = request_data.decode('utf-8', errors='ignore')
        
        # Parse first line to get method and path
        lines = request.split('\r\n')
        if lines:
            request_line = lines[0]
            print(f"  Request: {request_line}")
        
        # Prepare HTTP response
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure HTTPS Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2a5298; }
        .secure { color: #28a745; font-weight: bold; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>HTTPS Server Running</h1>
        <p class="secure">Connection is encrypted with TLS/SSL</p>
        <div class="info">
            <h3>Server Information:</h3>
            <ul>
                <li>Protocol: HTTPS (HTTP + TLS)</li>
                <li>Server: Python AsyncIO</li>
                <li>Status: Running successfully</li>
            </ul>
        </div>
        <p>This is a secure connection. Your data is encrypted in transit.</p>
    </div>
</body>
</html>
"""
        
        # Build HTTP response
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += html_content
        
        # Send response
        writer.write(response.encode('utf-8'))
        await writer.drain()
        
        print(f"  Response sent")
        
    except Exception as e:
        print(f"  Error: {e}")
    
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    """
    Start HTTPS server with TLS.
    """
    print("=" * 60)
    print("HTTPS Server (Async + TLS)")
    print("=" * 60)
    
    # Create SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    try:
        ssl_context.load_cert_chain(CERT_FILE, KEY_FILE)
    except FileNotFoundError:
        print("ERROR: Certificate files not found!")
        print("Run generate_certificates.sh first")
        return
    
    # Configure TLS
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    print(f"Certificate: {CERT_FILE}")
    print(f"Starting server on https://{HOST}:{PORT}")
    print("\nOpen your browser to: https://127.0.0.1:8443")
    print("(You'll see a security warning for self-signed cert - click 'Advanced' and proceed)")
    print("\nPress Ctrl+C to stop\n")
    
    # Start async server with TLS
    server = await asyncio.start_server(
        handle_http_request,
        HOST,
        PORT,
        ssl=ssl_context  # This enables TLS!
    )
    
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nServer stopped")