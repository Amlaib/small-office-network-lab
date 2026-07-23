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
| `11-dhcp-pools.png` | Shows DHCP pools configured on R1 for VLANs 10, 20 and 30. |
| `12-dhcp-client-ipconfig.png` | Shows a client receiving IPv4 configuration automatically through DHCP. |
| `13-dhcp-bindings.png` | Shows active DHCP leases assigned by R1. |
| `14-server-http-service.png` | Shows HTTP service enabled on the Internal Server. |
| `15-server-dns-record.png` | Shows the DNS A record mapping `intranet.office.test` to `192.168.40.10`. |
| `16-client-dns-resolution.png` | Shows a client resolving `intranet.office.test` to `192.168.40.10`. |
| `17-internal-web-by-hostname.png` | Shows successful browser access to the internal web page by hostname. |
| `18-guest-acl-configuration.png` | Shows the ACL configured to restrict Guest VLAN access. |
| `19-guest-access-blocked.png` | Shows Guest traffic blocked from accessing internal resources. |
| `20-authorized-access-still-works.png` | Shows authorised Admin or Support access still working after ACL configuration. |

## Notes

The screenshots are used as supporting evidence only. The main technical explanation is stored in the `documentation/` directory.

Related documents:

- `documentation/basic-switched-lan.md`
- `documentation/vlan-configuration.md`
- `documentation/inter-vlan-routing.md`
- `documentation/dhcp-configuration.md`
- `documentation/internal-services.md`
- `documentation/guest-access-restrictions.md`