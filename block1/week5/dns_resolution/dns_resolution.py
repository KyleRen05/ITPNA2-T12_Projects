"""
DNS Resolution with getaddrinfo()
----------------------------------
Demonstrates how to resolve hostnames to IP addresses
and get all socket information needed for connections.

This replaces the old gethostbyname() which only supported IPv4.
"""

import socket
import sys

def resolve_hostname(hostname, port=80):
    """
    Resolve a hostname and display all available addresses.
    Shows both IPv4 and IPv6 addresses if available.
    """
    print("=" * 70)
    print(f"Resolving: {hostname}:{port}")
    print("=" * 70)
    
    try:
        # Get address information
        # Parameters: host, port, family (0=any), type (0=any)
        results = socket.getaddrinfo(hostname, port, 0, socket.SOCK_STREAM)
        
        print(f"\nFound {len(results)} address(es):\n")
        
        for i, result in enumerate(results, 1):
            # Unpack the result tuple
            family, socktype, proto, canonname, sockaddr = result
            
            # Determine address family name
            family_name = "IPv4" if family == socket.AF_INET else "IPv6"
            
            # sockaddr format differs: IPv4 is (ip, port), IPv6 is (ip, port, flow, scope)
            ip_address = sockaddr[0]
            port_num = sockaddr[1]
            
            print(f"Result {i}:")
            print(f"  Address Family: {family_name}")
            print(f"  IP Address: {ip_address}")
            print(f"  Port: {port_num}")
            print(f"  Socket Type: {'STREAM (TCP)' if socktype == socket.SOCK_STREAM else 'DGRAM (UDP)'}")
            print()
        
        # Return first result for use in connections
        return results[0]
        
    except socket.gaierror as e:
        print(f"\nDNS Resolution Failed: {e}")
        print("Possible reasons:")
        print("  - Hostname does not exist")
        print("  - No internet connection")
        print("  - DNS server unreachable")
        return None
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return None


def get_canonical_name(hostname):
    """
    Get the canonical (official) hostname.
    A host may have multiple names (aliases), but one canonical name.
    """
    print("\n" + "=" * 70)
    print(f"Getting canonical name for: {hostname}")
    print("=" * 70)
    
    try:
        # Use AI_CANONNAME flag to request canonical name
        results = socket.getaddrinfo(hostname, 80, 
                                     flags=socket.AI_CANONNAME)
        
        # Canonical name is in the 4th element of the first result
        canonical = results[0][3]
        
        if canonical:
            print(f"\nCanonical name: {canonical}")
        else:
            print(f"\nNo canonical name returned (using numeric address?)")
            
    except socket.gaierror as e:
        print(f"\nError: {e}")


def compare_ipv4_ipv6(hostname):
    """
    Compare IPv4 and IPv6 addresses for a hostname.
    """
    print("\n" + "=" * 70)
    print(f"IPv4 vs IPv6 for: {hostname}")
    print("=" * 70)
    
    # Get IPv4 addresses only
    try:
        ipv4_results = socket.getaddrinfo(hostname, 80, socket.AF_INET)
        print(f"\nIPv4 Addresses:")
        for result in ipv4_results:
            print(f"  {result[4][0]}")
    except socket.gaierror:
        print("\nNo IPv4 addresses found")
    
    # Get IPv6 addresses only
    try:
        ipv6_results = socket.getaddrinfo(hostname, 80, socket.AF_INET6)
        print(f"\nIPv6 Addresses:")
        for result in ipv6_results:
            print(f"  {result[4][0]}")
    except socket.gaierror:
        print("\nNo IPv6 addresses found")


# Main execution
if __name__ == "__main__":
    # Example 1: Resolve google.com
    resolve_hostname("google.com", 80)
    
    # Example 2: Resolve with different port
    resolve_hostname("github.com", 443)
    
    # Example 3: Get canonical name
    get_canonical_name("www.google.com")
    
    # Example 4: Compare IPv4 and IPv6
    compare_ipv4_ipv6("google.com")
    
    # Example 5: Try resolving invalid hostname
    print("\n" + "=" * 70)
    print("Testing error handling with invalid hostname:")
    print("=" * 70)
    resolve_hostname("this-does-not-exist-12345.com", 80)
