# Inter-VLAN Routing

## Objective

Configure routing between the Administration, Technical Support, Guest and Server VLANs.

This stage uses a router-on-a-stick design with one physical link between the switch and router.

## Router-on-a-stick design

The switch port connected to the router was configured as an 802.1Q trunk.

The router uses one physical interface with four logical subinterfaces, one for each VLAN.

| VLAN | Router subinterface | Gateway address |
|---:|---|---|
| 10 | GigabitEthernet0/0.10 | 192.168.10.1 |
| 20 | GigabitEthernet0/0.20 | 192.168.20.1 |
| 30 | GigabitEthernet0/0.30 | 192.168.30.1 |
| 40 | GigabitEthernet0/0.40 | 192.168.40.1 |

Each end device was configured with the appropriate default gateway for its VLAN.

## Test results

Gateway reachability was tested successfully from each VLAN.

Inter-VLAN communication was then tested successfully:

- Administration to Technical Support
- Administration to Internal Server
- Guest to Internal Server

Guest access is currently allowed because no access-control rules have been applied yet. Guest restrictions will be configured in a later stage.

## Troubleshooting example

The default gateway was temporarily removed from Admin-PC1.

Admin-PC1 could still belong to its local subnet, but it could not reach the Internal Server in VLAN 40.

After restoring the default gateway to `192.168.10.1`, inter-VLAN communication worked again.

This demonstrated that devices need a default gateway to communicate outside their local IP network.

## Evidence

- `07-inter-vlan-routing-topology.png`
- `08-router-subinterfaces.png`
- `09-inter-vlan-routing-success.png`
- `10-router-routing-table.png`