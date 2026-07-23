# Troubleshooting Log

## Objective

Document realistic troubleshooting scenarios encountered while building the small office network lab.

The purpose is to show a structured investigation method: observe the symptom, isolate the likely layer or component, verify the root cause, apply a fix and retest.

---

## Scenario 1 - Same switch, different IP networks, no router

### Symptom

Admin-PC1 could not ping Admin-PC2 after Admin-PC2 was temporarily changed to `192.168.20.102/24`.

### Investigation

Admin-PC1 remained in `192.168.10.0/24`, while Admin-PC2 was moved to `192.168.20.0/24`.

Both devices were physically connected to the same switch, but no router or default gateway was configured at that stage.

### Root cause

The devices were in different IPv4 networks.

A Layer 2 switch can forward frames inside the same local network, but it cannot route traffic between different IP networks.

### Fix

Admin-PC2 was restored to:

```text
192.168.10.102/24
```
### Verification

Ping from Admin-PC1 to Admin-PC2 succeeded again with zero packet loss.

### Lesson learned

Physical connectivity through a switch is not enough when devices are in different IP networks. Routing is required for communication outside the local subnet.
___
## Scenario 2 - Same IP subnet, different VLANs

### Symptom

Admin-PC1 could not reach Support-PC1 after Support-PC1 was temporarily assigned an address from the Administration subnet.

Support-PC1 used:
```text
192.168.10.103/24
```

but remained connected to VLAN 20.

### Investigation

Admin-PC1 was in VLAN 10. Support-PC1 was physically connected to the same switch but assigned to VLAN 20.

Admin-PC1 sent ARP broadcasts inside VLAN 10, but Support-PC1 did not receive them because it was isolated in a different VLAN.

### Root cause

The devices were in different Layer 2 broadcast domains.

Even though the IP addressing was temporarily in the same subnet, VLAN separation prevented direct communication.

### Fix

Support-PC1 was restored to:
```text
192.168.20.101/24
```

### Verification

Same-VLAN communication worked inside VLAN 10 and VLAN 20. Cross-VLAN communication remained blocked until routing was configured.

### Lesson learned

VLAN membership and IP addressing are separate concepts. Devices must be in the same VLAN and compatible IP subnet to communicate directly without routing.
___
## Scenario 3 - Trunk configured but not operational
### Symptom

After configuring GigabitEthernet0/1 on SW1 as a trunk, the command:
```text
show interfaces trunk
```

showed no active trunk.

### Investigation

The switch configuration showed:
```text
switchport mode trunk
```

but the port status was:
```text
notconnect
```

The router-side physical interface was checked and found to be administratively down.

### Root cause

The trunk was configured correctly on the switch, but the physical router interface was shut down.

### Fix

The connected router interface was enabled with:
```text
no shutdown
```

### Verification

The link turned green and show interfaces trunk showed `GigabitEthernet0/1` as trunking with `802.1Q` encapsulation.

### Lesson learned

A correct logical configuration is not enough if the physical or operational interface state is down. Always check both configuration and interface status.
___
## Scenario 4 - Missing default gateway blocks inter-VLAN traffic
### Symptom

A client could communicate inside its own subnet but could not reach the Internal Server in VLAN 40 when the default gateway was missing or incorrect.

### Investigation

The client had a valid local IP address and subnet mask, but traffic to `192.168.40.10` required routing through the VLAN gateway.

Without a default gateway, the client had no path to send traffic outside its local subnet.

### Root cause

The client did not have the correct default gateway configured.

### Fix

The correct gateway was restored for the client VLAN.

Example for Administration VLAN:
```text
192.168.10.1
```
### Verification

The client could ping the Internal Server after the gateway was restored.

### Lesson learned

A default gateway is required when a device needs to communicate outside its own IP network.
___
## Scenario 5 - DNS record entered but not saved
### Symptom

Clients could ping the Internal Server by IP address:
```text
192.168.40.10
```

but could not resolve or ping:
```text
intranet.office.test
```

## Investigation

IP connectivity to the server worked, so routing, VLANs and gateways were not the issue.

The problem was isolated to name resolution. The DNS record had been entered on the server interface but was not saved into the DNS entries list.

## Root cause

The DNS A record was not saved correctly in the Packet Tracer server DNS service.

@@ Fix

The DNS record was added and saved properly:

| Hostname | Type | IP address |
|---|---|---|
| `intranet.office.test` | A | `192.168.40.10` |

## Verification

Clients could resolve `intranet.office.test` to `192.168.40.10`.

The internal web page opened successfully using:
```text
http://intranet.office.test
```

### Lesson learned

If IP access works but hostname access fails, investigate DNS before changing routing or VLAN configuration.
___
## Scenario 6 - Guest ACL blocks replies as well as requests
### Symptom

After applying Guest VLAN restrictions, Admin or Support initiated pings to Guest-PC1 failed.

At first this seemed unexpected because the ACL was designed to restrict Guest access to internal networks.

### Investigation

The ACL was applied inbound on the Guest router subinterface:
```text
GigabitEthernet0/0.30
```

Ping is bidirectional:

Admin-PC1 → Guest-PC1  ICMP echo request
Guest-PC1 → Admin-PC1  ICMP echo reply

The reply from Guest-PC1 entered the router through the Guest subinterface and was checked by the inbound ACL.

### Root cause

The ACL is stateless. It does not automatically recognise that Guest traffic is a reply to a request started by Admin or Support.

The ICMP reply matched the internal-network deny rules and was blocked.

### Fix

No change was required for the current lab goal.

Guest isolation from internal networks is acceptable behaviour for this project.

### Verification

The intended security tests passed:

-  Guest could not access Administration devices.  
- Guest could not access Technical Support devices.
- Guest could not access the Internal Server.
- Administration and Technical Support could still access the Internal Server.
### Lesson learned

Basic router ACLs are stateless. Direction, source, destination, protocol and rule order must be considered carefully during testing.

## General troubleshooting method used

Across the lab, the troubleshooting approach was:

- Confirm the symptom.
- Check whether the problem is physical, Layer 2, Layer 3, DNS or access control.
- Test the simplest path first.
- Compare working and failing cases.
- Change one thing at a time.
- Retest after each correction.
- Document the root cause and verification result.