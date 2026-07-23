# Guest Access Restrictions

## Objective

Restrict Guest VLAN access to internal office networks while preserving authorised access for Administration and Technical Support users.

This stage demonstrates basic traffic filtering with an extended access control list.

## Security design

Guest devices are located in VLAN 30.

| Source | Destination | Result |
|---|---|---|
| Guest VLAN | Administration VLAN | Blocked |
| Guest VLAN | Technical Support VLAN | Blocked |
| Guest VLAN | Servers VLAN | Blocked |
| Guest VLAN | DNS on Internal-Server | Allowed for name resolution |
| Administration VLAN | Internal-Server | Allowed |
| Technical Support VLAN | Internal-Server | Allowed |

The ACL is applied inbound on router subinterface `GigabitEthernet0/0.30`, close to the Guest source network.

## ACL logic

The ACL permits DNS traffic from the Guest VLAN to the Internal Server, then blocks Guest access to internal office and server networks.

A final permit statement allows other Guest traffic for future external-network simulation.

ACL rules are processed from top to bottom, and the first matching rule is applied.

## Test results

After applying the ACL:

- Guest-PC1 could no longer reach Administration devices.
- Guest-PC1 could no longer reach Technical Support devices.
- Guest-PC1 could no longer access the Internal Server by IP address.
- Guest-PC1 could resolve `intranet.office.test`, but HTTP access to the internal web page was blocked.
- Administration and Technical Support devices could still access the Internal Server.

This confirmed that the restriction affected Guest traffic only.

## Stateless ACL note

The ACL is stateless.

Admin or Support initiated pings to Guest-PC1 may also fail because the ICMP reply from Guest-PC1 is checked by the inbound Guest ACL and blocked by the internal-network deny rules.

This behaviour is acceptable for this lab because the goal is Guest isolation from internal networks.

## Troubleshooting note

The ACL was applied inbound on the Guest router subinterface.

If authorised traffic is unexpectedly blocked, the first checks are:

- ACL rule order;
- wildcard masks;
- interface direction;
- whether the ACL is applied to the correct subinterface;
- whether the traffic is a new request or a reply blocked by the stateless ACL.

## Production note

This is a simplified lab example.

In a production guest network, Guest users would normally use separate DNS and internet access paths rather than internal DNS services. Internal services would also normally require HTTPS and stronger firewall policy enforcement.

## Evidence

- `18-guest-acl-configuration.png`
- `19-guest-access-blocked.png`
- `20-authorized-access-still-works.png`