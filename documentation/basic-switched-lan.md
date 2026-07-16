# Basic Switched LAN

## Objective

Build and test a simple local network with two PCs connected through one Ethernet switch.

This stage demonstrates how devices in the same IPv4 subnet communicate without a router.

## Topology

| Device | Connection |
|---|---|
| Admin-PC1 | FastEthernet0 → SW1 FastEthernet0/1 |
| Admin-PC2 | FastEthernet0 → SW1 FastEthernet0/2 |

## IPv4 configuration

| Device | IPv4 address | Subnet mask | Default gateway |
|---|---|---|---|
| Admin-PC1 | 192.168.10.101 | 255.255.255.0 | Not required |
| Admin-PC2 | 192.168.10.102 | 255.255.255.0 | Not required |

Both devices belong to the `192.168.10.0/24` network.

## Test results

Ping was tested successfully in both directions:

- Admin-PC1 → Admin-PC2
- Admin-PC2 → Admin-PC1

Result: 4 packets sent, 4 received, 0 lost.

The switch dynamically learned both PC MAC addresses on ports `Fa0/1` and `Fa0/2`.

The PCs also stored each other’s IP-to-MAC mapping in their ARP tables.

## Troubleshooting exercise

Admin-PC2 was temporarily changed to `192.168.20.102/24`.

Communication failed because the two PCs were then in different IP networks and no router or default gateway was available.

After restoring Admin-PC2 to `192.168.10.102/24`, connectivity returned.

## Evidence

- `01-basic-lan-topology.png`
- `02-basic-lan-successful-ping.png`
- `03-switch-mac-table.png`
- `03-switch-mac-table.png`