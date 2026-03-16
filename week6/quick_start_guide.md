Example 1: TLS/SSL Basics

Shows how to create TLS server and client
Demonstrates certificate loading
Explains TLS handshake

Example 2: Server Architecture Comparison

Single-threaded: Simple but slow (6 seconds for 3 clients)
Threaded: Fast but resource-heavy (~2 seconds for 3 clients)
Includes test client to demonstrate difference

Example 3: Async Server

Modern approach using asyncio
Best performance with low memory
Recommended for new projects

Example 4: Complete HTTPS Server

Combines async + TLS
Full HTTP server with HTML responses
Production-ready pattern


# Setup (one time):
bash generate_certificates.sh

# Test TLS communication:
python tls_server.py     # Terminal 1
python tls_client.py     # Terminal 2

# Compare server types:
python single_threaded_server.py  # Terminal 1
python test_clients.py            # Terminal 2
# (Then switch to threaded_server.py)

# Test modern async:
python async_server.py   # Terminal 1
python async_client.py   # Terminal 2

# Run HTTPS server:
python https_server.py
# Open browser to https://127.0.0.1:8443