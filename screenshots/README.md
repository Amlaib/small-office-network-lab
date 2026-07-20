# Screenshots

This directory contains visual evidence for the Packet Tracer network lab.

## Evidence index

| File | Purpose |
|---|---|
| `01-basic-lan-topology.png` | Shows the initial two-PC switched LAN topology. |
| `02-basic-lan-successful-ping.png` | Shows successful bidirectional connectivity in the basic LAN. |
| `03-switch-mac-table.png` | Shows dynamically learned MAC addresses on the switch. |
| `04-vlan-topology.png` | Shows the expanded topology with Administration, Technical Support, Guest and Server devices. |
| `05-vlan-brief.png` | Shows VLANs 10, 20, 30 and 40 with switch ports assigned correctly. |
| `06-vlan-isolation-test.png` | Shows failed communication between separated VLANs, confirming VLAN isolation. |
| `07-inter-vlan-routing-topology.png` | Shows the router connected to SW1 for inter-VLAN routing. |
| `08-router-subinterfaces.png` | Shows router subinterfaces configured as gateways for VLANs 10, 20, 30 and 40. |
| `09-inter-vlan-routing-success.png` | Shows successful communication between different VLANs after routing was configured. |
| `10-router-routing-table.png` | Shows directly connected routes for all four VLAN networks. |

## Notes

The screenshots are used as supporting evidence only. The main technical explanation is stored in the `documentation/` directory.

Related documents:

- `documentation/basic-switched-lan.md`
- `documentation/vlan-configuration.md`
- `documentation/inter-vlan-routing.md`