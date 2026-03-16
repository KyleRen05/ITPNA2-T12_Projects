# Step 1: Generate certificates (one time only)
bash generate_certificates.sh

# Step 2: Open TWO terminal windows

# Terminal 1 - Start the server:
python tls_server.py

# Terminal 2 - Run the client:
python tls_client.py

# You should see encrypted communication happening