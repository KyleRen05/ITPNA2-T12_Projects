# Make sure you have certificates (from Example 1)
# If not, run: bash generate_certificates.sh

# Start the HTTPS server:
python https_server.py

# Open your web browser to:
# https://127.0.0.1:8443

# You'll see a security warning (because self-signed certificate)
# Click "Advanced" and "Proceed" to see the page

# The connection is encrypted even though browser shows warning!