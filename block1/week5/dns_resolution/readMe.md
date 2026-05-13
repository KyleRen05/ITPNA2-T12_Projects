python dns_resolution.py
```

### **Expected Output:**
```
======================================================================
Resolving: google.com:80
======================================================================

Found 1 address(es):

Result 1:
  Address Family: IPv4
  IP Address: 142.250.185.46
  Port: 80
  Socket Type: STREAM (TCP)

======================================================================
Resolving: github.com:443
======================================================================

Found 1 address(es):

Result 1:
  Address Family: IPv4
  IP Address: 140.82.121.4
  Port: 443
  Socket Type: STREAM (TCP)

======================================================================
Getting canonical name for: www.google.com
======================================================================

Canonical name: www.google.com

======================================================================
IPv4 vs IPv6 for: google.com
======================================================================

IPv4 Addresses:
  142.250.185.46

IPv6 Addresses:
  2607:f8b0:4004:c07::71
  2607:f8b0:4004:c07::8a
  2607:f8b0:4004:c07::66
  2607:f8b0:4004:c07::8b