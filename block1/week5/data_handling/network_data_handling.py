"""
Network Data Handling
---------------------
Demonstrates proper handling of:
- Bytes vs Strings
- Encoding/Decoding
- JSON serialization for network transmission
- Network byte order
"""

import socket
import json
import struct


def demonstrate_bytes_vs_strings():
    """
    Show the difference between bytes and strings in Python 3.
    Critical for network programming!
    """
    print("=" * 70)
    print("Bytes vs Strings")
    print("=" * 70)
    
    # String (text for humans)
    text = "Hello, Network!"
    print(f"\nString: {text}")
    print(f"Type: {type(text)}")
    print(f"Can send over network? NO - must convert to bytes first")
    
    # Convert string to bytes (encoding)
    data = text.encode('utf-8')
    print(f"\nBytes: {data}")
    print(f"Type: {type(data)}")
    print(f"Can send over network? YES")
    print(f"Size: {len(data)} bytes")
    
    # Convert bytes back to string (decoding)
    received_text = data.decode('utf-8')
    print(f"\nDecoded back to string: {received_text}")
    
    # Show different encodings
    print("\n" + "-" * 70)
    print("Same text in different encodings:")
    print("-" * 70)
    
    encodings = ['utf-8', 'ascii', 'latin-1', 'utf-16']
    
    for encoding in encodings:
        try:
            encoded = text.encode(encoding)
            print(f"{encoding:10s}: {encoded} ({len(encoded)} bytes)")
        except UnicodeEncodeError:
            print(f"{encoding:10s}: Cannot encode this text")
    
    # Demonstrate Unicode characters
    print("\n" + "-" * 70)
    print("Unicode Characters:")
    print("-" * 70)
    
    unicode_text = "Hello 你好 Привет"
    print(f"Text: {unicode_text}")
    
    utf8_encoded = unicode_text.encode('utf-8')
    print(f"UTF-8 bytes: {utf8_encoded}")
    print(f"Size: {len(utf8_encoded)} bytes")


def demonstrate_json_serialization():
    """
    Show how to serialize Python data structures to JSON
    for network transmission.
    """
    print("\n\n" + "=" * 70)
    print("JSON Serialization for Network Data")
    print("=" * 70)
    
    # Create a complex data structure (like router status)
    router_data = {
        "hostname": "CORE-ROUTER-1",
        "ip_address": "192.168.1.1",
        "cpu_usage": 45.3,
        "memory_usage": 62.8,
        "uptime_seconds": 86400,
        "interfaces": [
        {"name": "GigabitEthernet0/0", "status": "up", "speed": 1000},
            {"name": "GigabitEthernet0/1", "status": "up", "speed": 1000},
            {"name": "GigabitEthernet0/2", "status": "down", "speed": 0}
        ],
        "is_online": True
    }
    
    print("\nOriginal Python data structure:")
    print(router_data)
    print(f"Type: {type(router_data)}")
    
    # Serialize to JSON string
    json_string = json.dumps(router_data, indent=2)
    print("\nSerialized to JSON string:")
    print(json_string)
    print(f"Type: {type(json_string)}")
    
    # Convert to bytes for network transmission
    network_data = json_string.encode('utf-8')
    print(f"\nConverted to bytes for network:")
    print(f"Size: {len(network_data)} bytes")
    print(f"Type: {type(network_data)}")
    
    # Simulate network transmission
    print("\n" + "-" * 70)
    print("Simulating network transmission...")
    print("-" * 70)
    
    # On receiving end: bytes -> string -> Python dict
    received_bytes = network_data  # Simulating received data
    
    # Decode bytes to string
    received_json = received_bytes.decode('utf-8')
    print("\nReceived and decoded to string")
    
    # Parse JSON to Python dict
    received_data = json.loads(received_json)
    print("Parsed JSON to Python dictionary")
    
    # Access the data
    print(f"\nAccessing received data:")
    print(f"  Hostname: {received_data['hostname']}")
    print(f"  CPU Usage: {received_data['cpu_usage']}%")
    print(f"  Number of interfaces: {len(received_data['interfaces'])}")
    print(f"  First interface: {received_data['interfaces'][0]['name']}")


def demonstrate_network_byte_order():
    """
    Demonstrate network byte order conversion for binary data.
    """
    print("\n\n" + "=" * 70)
    print("Network Byte Order (Endianness)")
    print("=" * 70)
    
    # Example: Converting port number
    port = 5000
    
    print(f"\nOriginal port number: {port}")
    print(f"Binary representation: {bin(port)}")
    print(f"Hexadecimal: {hex(port)}")
    
    # Convert to network byte order (big-endian)
    network_port = socket.htons(port)  # host to network short
    
    print(f"\nAfter network byte order conversion:")
    print(f"Network port: {network_port}")
    print(f"Binary: {bin(network_port)}")
    print(f"Hex: {hex(network_port)}")
    
    # Convert back to host byte order
    host_port = socket.ntohs(network_port)  # network to host short
    
    print(f"\nConverted back to host byte order:")
    print(f"Host port: {host_port}")
    
    # Pack/Unpack binary data
    print("\n" + "-" * 70)
    print("Packing binary data with struct module:")
    print("-" * 70)
    
    # Pack multiple values into binary format
    # ! = network byte order
    # H = unsigned short (2 bytes)
    # I = unsigned int (4 bytes)
    packed = struct.pack('!HI', 5000, 192*256**3 + 168*256**2 + 1*256 + 1)
    
    print(f"\nPacked data: {packed}")
    print(f"Size: {len(packed)} bytes")
    
    # Unpack
    port, ip = struct.unpack('!HI', packed)
    print(f"\nUnpacked:")
    print(f"  Port: {port}")
    print(f"  IP (as integer): {ip}")


def demonstrate_framing():
    """
    Show different message framing techniques.
    """
    print("\n\n" + "=" * 70)
    print("Message Framing Techniques")
    print("=" * 70)
    
    messages = ["Hello", "World", "This is a test"]
    
    # Method 1: Length-prefix framing
    print("\nMethod 1: Length-Prefix Framing")
    print("-" * 70)
    
    for msg in messages:
        # Pack: 4-byte length followed by message
        length = len(msg)
        framed = struct.pack('!I', length) + msg.encode('utf-8')
        print(f"Message: '{msg}'")
        print(f"  Length: {length}")
        print(f"  Framed: {framed}")
        print(f"  Total size: {len(framed)} bytes")
    
    # Method 2: Delimiter framing
    print("\nMethod 2: Delimiter Framing (newline)")
    print("-" * 70)
    
    for msg in messages:
        framed = msg + '\n'
        print(f"Message: '{msg}' -> '{framed.strip()}'")
        print(f"  With delimiter: {framed.encode('utf-8')}")
    
    # Method 3: JSON (self-delimiting)
    print("\nMethod 3: JSON Self-Delimiting")
    print("-" * 70)
    
    for msg in messages:
        json_msg = json.dumps({"message": msg})
        print(f"Message: '{msg}'")
        print(f"  As JSON: {json_msg}")


# Main execution
if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_bytes_vs_strings()
    demonstrate_json_serialization()
    demonstrate_network_byte_order()
    demonstrate_framing()