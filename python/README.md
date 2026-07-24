# Python Tools

This folder contains Python tools related to the Small Office Network Lab.

## Subnet validator

`subnet_validator.py` validates the lab addressing plan from a machine-readable JSON file.

The addressing data is stored in:

```text
data/addressing-plan.json
```
#### The script checks:

- VLAN IDs;
- VLAN IPv4 networks;
- gateway addresses;
- DHCP ranges;
- static host addresses;
- duplicate gateway/static host addresses;
- DNS A records.

#### Run from the project root:
```text
python python/subnet_validator.py
```

or:
```text
python python/subnet_validator.py data/addressing-plan.json
```

#### Expected result:
```annotation
Result: PASS
```

The script uses only Python's built-in standard library.