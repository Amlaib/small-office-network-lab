# Project Plan

## Delivery sequence

1. Define network requirements and IPv4 addressing.
2. Build and test a basic switched LAN.
3. Create departmental VLANs.
4. Configure inter-VLAN routing.
5. Configure DHCP.
6. Configure internal DNS and web services.
7. Apply guest-network access restrictions.
8. Introduce and diagnose network faults.
9. Create a Python subnet validation utility.
10. Complete screenshots and final documentation.

### Optional later extension

11. Add dual-stack IPv6 support

After the complete IPv4 network is working and documented:

- assign one IPv6 `/64` prefix to each VLAN;
- enable IPv6 routing;
- configure client addressing using SLAAC;
- test IPv6 communication within and between VLANs;
- verify security restrictions using IPv6 traffic;
- document the main differences between IPv4 and IPv6 troubleshooting;
- update the Python validator to support IPv6 networks.

Planned documentation prefixes:

| VLAN | IPv6 network |
|---:|---|
| 10 | 2001:db8:10::/64 |
| 20 | 2001:db8:20::/64 |
| 30 | 2001:db8:30::/64 |
| 40 | 2001:db8:40::/64 |

## Current stage

The business requirements, VLAN structure and IPv4 addressing plan have been defined.