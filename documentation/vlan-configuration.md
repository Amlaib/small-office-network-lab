# VLAN Configuration

## Objective

Separate Administration, Technical Support, Guest and Server devices into independent logical networks on one physical switch.

## VLAN and port plan

| VLAN | Name | Switch ports | Connected devices |
|---:|---|---|---|
| 10 | Administration | Fa0/1–Fa0/2 | Admin-PC1, Admin-PC2 |
| 20 | Technical Support | Fa0/3–Fa0/4 | Support-PC1, Support-PC2 |
| 30 | Guest | Fa0/5 | Guest-PC1 |
| 40 | Servers | Fa0/6 | Internal-Server |

All connected ports were configured as access ports.

## Test results

Communication succeeded between devices in the same VLAN:

- Admin-PC1 → Admin-PC2
- Support-PC1 → Support-PC2

Communication failed between different VLANs because no inter-VLAN routing was configured.

## VLAN isolation test

Support-PC1 was temporarily assigned `192.168.10.103/24` while remaining connected to VLAN 20.

Admin-PC1 could not reach it, even though both devices then used addresses from the same IPv4 subnet.

This demonstrated that Layer-2 broadcasts and Ethernet frames remain isolated within their assigned VLANs.

Support-PC1 was restored to `192.168.20.101/24` after the test.

## Evidence

- `04-vlan-topology.png`
- `05-vlan-brief.png`
- `06-vlan-isolation-test.png`