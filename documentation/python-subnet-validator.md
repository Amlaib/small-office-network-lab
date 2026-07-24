# Python Subnet Validator

## Objective

Create a small Python validation tool for the lab addressing plan.

The purpose is to check common IPv4 planning mistakes automatically.

## Design decision

The first simple version of this idea could have hardcoded the addressing plan directly inside the Python script.

The final version separates data from logic:

```text
data/addressing-plan.json  →  python/subnet_validator.py  →  validation report
```
This makes the validator easier to maintain, review and extend.

#### What the script validates

The script checks:

- JSON file exists and can be parsed;
- required JSON fields are present;
- VLAN IDs are unique;
- VLAN IPv4 networks do not overlap;
- gateways are valid usable host addresses;
- DHCP ranges are inside the correct VLAN subnet;
- DHCP ranges do not include gateway addresses;
- static host addresses are inside the correct VLAN subnet;
- gateway and static host addresses are not duplicated;
- DNS A records point to addresses inside known VLAN networks;
- DNS A records point to known static hosts.

#### Tool used

The script uses Python's built-in ipaddress module.

No external dependencies are required.

#### Addressing data source

The machine-readable addressing plan is stored in:
```text
data/addressing-plan.json
```

The human-readable explanation is stored in:
```text
documentation/addressing-plan.md
```

#### Addressing plan checked
| VLAN       | Name    | Network          | Gateway      | DHCP range |
|------------|---------|------------------|--------------|---|
| 10         | Administration | 192.168.10.0/24  | 192.168.10.1 | 192.168.10.100–192.168.10.199 |
| 20         | Technical Support | 192.168.20.0/24  | 192.168.20.1 | 192.168.20.100–192.168.20.199 |
| 30         | Guest   | 192.168.30.0/24  | 192.168.30.1 | 192.168.30.100–192.168.30.199 |
| 40 | Servers | 192.168.40.0/24  | 192.168.40.1 | No DHCP |

#### Static host:

| Host | IP address | VLAN |
|---|---|---|
| Internal-Server | `192.168.40.10` | 40 |

#### DNS record:

| Hostname | Type | IP address |
|---|---|---|
| intranet.office.test | A | `192.168.40.10` |

### How to run

#### From the project root:
```text
python python/subnet_validator.py
```
or:

```text
python python/subnet_validator.py data/addressing-plan.json
```

#### On Windows, if needed, cmd:
```text
py python/subnet_validator.py
```
### Expected result

#### The script should finish with:
```text
Warnings: 0
Failures: 0
Result: PASS
```

#### Deliberate negative test

A temporary incorrect change was made during testing to confirm that the validator detects errors.

Example:

- VLAN 20 network changed to overlap with VLAN 10

- The script reported a failure.

- After restoring the correct VLAN 20 network, the script returned to:
```text
Result: PASS
```

##### _The broken version was not committed._

### Future extension

The JSON structure is designed so `IPv6` data can be added later without rewriting the whole validator.

A future version could also compare the JSON addressing plan with manually exported Packet Tracer configuration snapshots.