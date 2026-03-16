#!/bin/bash
# Generate self-signed certificate for testing

# DO NOT use self-signed certificates in production!


echo "Generating SSL certificate for testing..."


openssl req -x509 -newkey rsa:4096 -nodes -keyout server-key.pem -out server-cert.pem -days 365 -subj "//CN=localhost"

echo "Certificate generated successfully!"

echo "Files created:"

echo "  - server-key.pem (private key)"

echo "  - server-cert.pem (certificate)" 