# DHCP Configuration

## Objective

Configure automatic IPv4 address assignment for user devices in the Administration, Technical Support and Guest VLANs.

The Internal Server remains statically addressed because infrastructure services require stable IP addresses.

## DHCP design

| VLAN | Network | Gateway | DHCP range |
|---:|---|---|---|
| 10 | 192.168.10.0/24 | 192.168.10.1 | 192.168.10.100–192.168.10.199 |
| 20 | 192.168.20.0/24 | 192.168.20.1 | 192.168.20.100–192.168.20.199 |
| 30 | 192.168.30.0/24 | 192.168.30.1 | 192.168.30.100–192.168.30.199 |

VLAN 40 does not use DHCP in this stage. The Internal Server remains statically configured as `192.168.40.10`.

## Router DHCP configuration

R1 was configured with three DHCP pools:

- `VLAN10_ADMINISTRATION`
- `VLAN20_TECH_SUPPORT`
- `VLAN30_GUEST`

Addresses outside the intended DHCP ranges were excluded to protect gateways, infrastructure addresses and future-use ranges.

## Test results

Client devices were changed from static addressing to DHCP.

Each client received an address from the correct VLAN range and the correct default gateway.

Connectivity was tested successfully after DHCP assignment.

## Troubleshooting example

Guest-PC1 was temporarily changed from DHCP to an incorrect static configuration.

The device could not communicate normally until DHCP was restored.

This demonstrated that correct IP address, subnet mask and default gateway assignment are required for normal network communication.

## Evidence

- `11-dhcp-pools.png`
- `12-dhcp-client-ipconfig.png`
- `13-dhcp-bindings.png`