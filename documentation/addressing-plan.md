# Network Requirements and IPv4 Addressing Plan

## Scenario

This project simulates a small office network for a fictional financial-services support organisation.

The office contains Administration staff, Technical Support staff, guest users and an internal server. The network is designed to demonstrate logical separation, automatic address assignment, routing, internal services, access control and troubleshooting.

This is a simplified educational design and does not represent the infrastructure of any real organisation.

## Business requirements

The network must:

- separate Administration, Technical Support, Guest and Server traffic;
- assign IP addresses automatically to user devices;
- provide stable addressing for internal services;
- allow authorised staff to access internal resources;
- prevent guest users from accessing internal systems;
- support systematic testing and troubleshooting;
- remain understandable and reproducible.

## VLAN plan

| VLAN ID | Name | Purpose |
|---:|---|---|
| 10 | Administration | Administrative employee devices |
| 20 | Technical Support | Technical and support devices |
| 30 | Guest | Visitor devices |
| 40 | Servers | Internal services |

## IPv4 addressing plan

| VLAN | Network | Subnet mask | Default gateway | DHCP range |
|---:|---|---|---|---|
| 10 | 192.168.10.0/24 | 255.255.255.0 | 192.168.10.1 | 192.168.10.100–192.168.10.199 |
| 20 | 192.168.20.0/24 | 255.255.255.0 | 192.168.20.1 | 192.168.20.100–192.168.20.199 |
| 30 | 192.168.30.0/24 | 255.255.255.0 | 192.168.30.1 | 192.168.30.100–192.168.30.199 |
| 40 | 192.168.40.0/24 | 255.255.255.0 | 192.168.40.1 | No initial DHCP pool |

## Address allocation convention

| Address range | Purpose |
|---|---|
| .1 | Default gateway |
| .2–.49 | Network infrastructure |
| .50–.99 | Reserved static devices |
| .100–.199 | DHCP clients |
| .200–.254 | Future use |

## Initial device plan

| Device | VLAN | Addressing |
|---|---:|---|
| Admin-PC1 | 10 | DHCP |
| Admin-PC2 | 10 | DHCP |
| Support-PC1 | 20 | DHCP |
| Support-PC2 | 20 | DHCP |
| Guest-PC1 | 30 | DHCP |
| Internal-Server | 40 | Static: 192.168.40.10 |

## Planned security behaviour

- Administration and Technical Support devices may access the internal server.
- Guest devices must not access the internal server or employee networks.
- Guest devices will later be permitted only toward simulated external services.