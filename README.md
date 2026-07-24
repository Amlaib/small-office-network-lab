# Small Office Network Lab

A practical Cisco Packet Tracer project demonstrating small-office network design, VLAN segmentation, inter-VLAN routing, DHCP, internal DNS/web services, guest access restrictions, troubleshooting documentation and Python-based addressing-plan validation.

## Status

**Core lab complete. Optional extensions planned.**

The current version includes a working IPv4 small-office network with documented configuration, testing evidence and troubleshooting notes.

## Project overview

This lab simulates a small office network with separate departmental networks:

- Administration
- Technical Support
- Guest
- Servers

The network uses VLANs to separate traffic, router-on-a-stick for inter-VLAN routing, DHCP for client addressing, an internal DNS/web server, and an ACL to restrict Guest access to internal resources.

A JSON-driven Python utility validates the addressing plan and checks for common subnet-planning errors.

## Implemented features

- IPv4 addressing and subnet planning
- Ethernet switching
- VLAN configuration
- Router-on-a-stick inter-VLAN routing
- DHCP for user VLANs
- Static addressing for the internal server
- Internal DNS record for `intranet.office.test`
- Internal HTTP web service
- Guest-network access restrictions using an extended ACL
- Documented troubleshooting scenarios
- JSON-driven Python subnet validator
- Screenshots as evidence for key configuration and test results

## Current progress

- [x] Repository created
- [x] Project structure prepared
- [x] Network requirements defined
- [x] Addressing plan created
- [x] Initial LAN configured
- [x] VLANs configured
- [x] Inter-VLAN routing configured
- [x] DHCP configured
- [x] Internal DNS and web services configured
- [x] Guest access restrictions configured
- [x] Troubleshooting scenarios documented
- [x] Python subnet validator implemented

## Network design summary

| VLAN | Name | Network | Gateway | Purpose |
|---:|---|---|---|---|
| 10 | Administration | `192.168.10.0/24` | `192.168.10.1` | Office administration clients |
| 20 | Technical Support | `192.168.20.0/24` | `192.168.20.1` | Technical support clients |
| 30 | Guest | `192.168.30.0/24` | `192.168.30.1` | Restricted guest access |
| 40 | Servers | `192.168.40.0/24` | `192.168.40.1` | Internal services |

Internal server:

| Host | IP address | Services |
|---|---|---|
| Internal-Server | `192.168.40.10` | DNS, HTTP |

DNS record:

| Hostname | Type | Address |
|---|---|---|
| `intranet.office.test` | A | `192.168.40.10` |

## Guest access policy

The Guest VLAN is restricted with an extended ACL.

| Source | Destination | Result |
|---|---|---|
| Guest VLAN | Administration VLAN | Blocked |
| Guest VLAN | Technical Support VLAN | Blocked |
| Guest VLAN | Servers VLAN | Blocked |
| Guest VLAN | DNS on Internal-Server | Allowed for name resolution |
| Administration VLAN | Internal-Server | Allowed |
| Technical Support VLAN | Internal-Server | Allowed |

The ACL is applied inbound on the Guest router subinterface.

## Python subnet validator

The project includes a small Python utility:

```text
python/subnet_validator.py
```

The validator reads machine-readable addressing data from:

```text
data/addressing-plan.json
```

It checks:

- VLAN IDs are unique;
- VLAN IPv4 networks do not overlap;
- gateways are valid usable host addresses;
- DHCP ranges are inside the correct subnet;
- DHCP ranges do not include gateway addresses;
- static host addresses are inside the correct subnet;
- gateway and static host addresses are not duplicated;
- DNS A records point to known internal addresses;
- DNS A records point to known static hosts.

Run from the project root:

```text
python python/subnet_validator.py
```

Expected result:

```text
Result: PASS
```

## Repository structure

```text
small-office-network-lab/
├── data/
│   └── addressing-plan.json
├── documentation/
│   ├── addressing-plan.md
│   ├── basic-switched-lan.md
│   ├── dhcp-configuration.md
│   ├── guest-access-restrictions.md
│   ├── internal-services.md
│   ├── inter-vlan-routing.md
│   ├── project-plan.md
│   ├── python-subnet-validator.md
│   ├── troubleshooting-log.md
│   └── vlan-configuration.md
├── packet-tracer/
│   └── small-office-network-lab.pkt
├── python/
│   ├── README.md
│   └── subnet_validator.py
├── screenshots/
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md
```

## Documentation

Key documentation files:

- `documentation/addressing-plan.md` — VLANs, subnets, gateways and addressing conventions.
- `documentation/vlan-configuration.md` — VLAN setup and access-port configuration.
- `documentation/inter-vlan-routing.md` — router-on-a-stick routing configuration.
- `documentation/dhcp-configuration.md` — DHCP pools and client addressing.
- `documentation/internal-services.md` — internal DNS and web-service setup.
- `documentation/guest-access-restrictions.md` — Guest VLAN ACL design and tests.
- `documentation/troubleshooting-log.md` — real troubleshooting scenarios from the lab.
- `documentation/python-subnet-validator.md` — Python validation tool explanation.

## Evidence

Screenshots are stored in:

```text
screenshots/
```

The screenshot index is documented in:

```text
screenshots/README.md
```

Evidence includes topology views, VLAN output, routing tables, DHCP bindings, DNS records, ACL tests, browser tests and Python validator output.

## Troubleshooting approach

The lab documents several real troubleshooting scenarios, including:

- same switch but different IP networks;
- same IP subnet but different VLANs;
- trunk configured but not operational;
- missing default gateway;
- DNS record entered but not saved;
- stateless ACL behaviour affecting ICMP replies.


## Future extensions

Optional future improvements:

- dual-stack IPv6 configuration and testing;
- secure management hardening;
- SSH instead of Telnet where supported;
- unused switch-port shutdown;
- management VLAN;
- HTTPS/TLS discussion for internal services;
- comparison between JSON addressing plan and exported Packet Tracer configuration snapshots.

## Purpose

This project was built as a practical guide for those learning the fundamentals of networking, basic problem solving and example of analytics solution.