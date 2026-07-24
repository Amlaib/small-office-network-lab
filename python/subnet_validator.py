from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
from typing import Any, Optional

@dataclass(frozen=True)
class DHCPRange:
    start: IPv4Address
    end: IPv4Address


@dataclass(frozen=True)
class StaticHost:
    name: str
    ipv4_address: IPv4Address


@dataclass(frozen=True)
class VLANPlan:
    vlan_id: int
    name: str
    network: IPv4Network
    gateway: IPv4Address
    dhcp_range: Optional[DHCPRange]
    static_hosts: list[StaticHost]


@dataclass(frozen=True)
class DNSRecord:
    hostname: str
    record_type: str
    address: IPv4Address


@dataclass(frozen=True)
class AddressingPlan:
    vlans: list[VLANPlan]
    dns_records: list[DNSRecord]


class PlanFormatError(ValueError):
    pass


class Report:
    def __init__(self) -> None:
        self.failures = 0
        self.warnings = 0
        self.passes = 0

    def pass_(self, message: str) -> None:
        self.passes += 1
        print(f"PASS: {message}")

    def warn(self, message: str) -> None:
        self.warnings += 1
        print(f"WARN: {message}")

    def fail(self, message: str) -> None:
        self.failures += 1
        print(f"FAIL: {message}")


def require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PlanFormatError(f"{context} must be an object")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise PlanFormatError(f"{context} must be a list")
    return value


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PlanFormatError(f"{context} must be a non-empty string")
    return value.strip()


def parse_ipv4_address(value: Any, context: str) -> IPv4Address:
    text = require_string(value, context)

    try:
        return IPv4Address(text)
    except ValueError as exc:
        raise PlanFormatError(f"{context} must be a valid IPv4 address: {text}") from exc


def parse_ipv4_network(value: Any, context: str) -> IPv4Network:
    text = require_string(value, context)

    try:
        return IPv4Network(text, strict=True)
    except ValueError as exc:
        raise PlanFormatError(
            f"{context} must be a valid IPv4 network in CIDR format: {text}"
        ) from exc


def parse_vlan(raw_vlan: Any, index: int) -> VLANPlan:
    vlan = require_dict(raw_vlan, f"vlans[{index}]")

    try:
        vlan_id = int(vlan["vlan_id"])
    except KeyError as exc:
        raise PlanFormatError(f"vlans[{index}].vlan_id is required") from exc
    except (TypeError, ValueError) as exc:
        raise PlanFormatError(f"vlans[{index}].vlan_id must be an integer") from exc

    name = require_string(vlan.get("name"), f"VLAN {vlan_id} name")
    ipv4 = require_dict(vlan.get("ipv4"), f"VLAN {vlan_id} ipv4")

    network = parse_ipv4_network(
        ipv4.get("network_cidr"),
        f"VLAN {vlan_id} ipv4.network_cidr",
    )
    gateway = parse_ipv4_address(
        ipv4.get("gateway"),
        f"VLAN {vlan_id} ipv4.gateway",
    )

    raw_dhcp = ipv4.get("dhcp_range")

    if raw_dhcp is None:
        dhcp_range = None
    else:
        dhcp = require_dict(raw_dhcp, f"VLAN {vlan_id} ipv4.dhcp_range")
        dhcp_range = DHCPRange(
            start=parse_ipv4_address(
                dhcp.get("start"),
                f"VLAN {vlan_id} ipv4.dhcp_range.start",
            ),
            end=parse_ipv4_address(
                dhcp.get("end"),
                f"VLAN {vlan_id} ipv4.dhcp_range.end",
            ),
        )

    static_hosts: list[StaticHost] = []

    for host_index, raw_host in enumerate(
        require_list(vlan.get("static_hosts", []), f"VLAN {vlan_id} static_hosts")
    ):
        host = require_dict(raw_host, f"VLAN {vlan_id} static_hosts[{host_index}]")

        host_name = require_string(
            host.get("name"),
            f"VLAN {vlan_id} static_hosts[{host_index}].name",
        )
        host_ip = parse_ipv4_address(
            host.get("ipv4_address"),
            f"VLAN {vlan_id} static_hosts[{host_index}].ipv4_address",
        )

        static_hosts.append(
            StaticHost(
                name=host_name,
                ipv4_address=host_ip,
            )
        )

    return VLANPlan(
        vlan_id=vlan_id,
        name=name,
        network=network,
        gateway=gateway,
        dhcp_range=dhcp_range,
        static_hosts=static_hosts,
    )


def parse_dns_record(raw_record: Any, index: int) -> DNSRecord:
    record = require_dict(raw_record, f"dns_records[{index}]")

    hostname = require_string(
        record.get("hostname"),
        f"dns_records[{index}].hostname",
    )
    record_type = require_string(
        record.get("type"),
        f"dns_records[{index}].type",
    ).upper()
    address = parse_ipv4_address(
        record.get("address"),
        f"dns_records[{index}].address",
    )

    return DNSRecord(
        hostname=hostname,
        record_type=record_type,
        address=address,
    )


def load_addressing_plan(path: Path) -> AddressingPlan:
    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PlanFormatError(f"Plan file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PlanFormatError(f"Plan file is not valid JSON: {exc}") from exc

    root = require_dict(raw_data, "root JSON value")

    raw_vlans = require_list(root.get("vlans"), "vlans")
    raw_dns_records = require_list(root.get("dns_records", []), "dns_records")

    vlans = [
        parse_vlan(raw_vlan, index)
        for index, raw_vlan in enumerate(raw_vlans)
    ]

    dns_records = [
        parse_dns_record(raw_record, index)
        for index, raw_record in enumerate(raw_dns_records)
    ]

    return AddressingPlan(
        vlans=vlans,
        dns_records=dns_records,
    )


def is_usable_host(address: IPv4Address, network: IPv4Network) -> bool:
    return address in network and address not in {
        network.network_address,
        network.broadcast_address,
    }


def address_in_range(address: IPv4Address, dhcp_range: DHCPRange) -> bool:
    return int(dhcp_range.start) <= int(address) <= int(dhcp_range.end)


def find_vlan_for_address(
    address: IPv4Address,
    vlans: list[VLANPlan],
) -> Optional[VLANPlan]:
    for vlan in vlans:
        if address in vlan.network:
            return vlan

    return None


def build_static_host_index(vlans: list[VLANPlan]) -> dict[IPv4Address, StaticHost]:
    hosts: dict[IPv4Address, StaticHost] = {}

    for vlan in vlans:
        for host in vlan.static_hosts:
            hosts[host.ipv4_address] = host

    return hosts


def validate_vlan_ids_are_unique(vlans: list[VLANPlan], report: Report) -> None:
    failures_before = report.failures
    seen: dict[int, str] = {}

    for vlan in vlans:
        if vlan.vlan_id in seen:
            report.fail(
                f"Duplicate VLAN ID {vlan.vlan_id}: "
                f"{seen[vlan.vlan_id]} and {vlan.name}"
            )
        else:
            seen[vlan.vlan_id] = vlan.name

    if report.failures == failures_before:
        report.pass_("VLAN IDs are unique")


def validate_networks_do_not_overlap(vlans: list[VLANPlan], report: Report) -> None:
    failures_before = report.failures

    for index, left_vlan in enumerate(vlans):
        for right_vlan in vlans[index + 1:]:
            if left_vlan.network.overlaps(right_vlan.network):
                report.fail(
                    f"VLAN {left_vlan.vlan_id} network {left_vlan.network} overlaps "
                    f"with VLAN {right_vlan.vlan_id} network {right_vlan.network}"
                )

    if report.failures == failures_before:
        report.pass_("VLAN networks do not overlap")


def validate_duplicate_addresses(vlans: list[VLANPlan], report: Report) -> None:
    failures_before = report.failures
    seen: dict[IPv4Address, str] = {}

    for vlan in vlans:
        labels = [
            (vlan.gateway, f"VLAN {vlan.vlan_id} gateway"),
        ]

        for host in vlan.static_hosts:
            labels.append(
                (host.ipv4_address, f"{host.name} in VLAN {vlan.vlan_id}")
            )

        for address, label in labels:
            if address in seen:
                report.fail(f"Duplicate address {address}: {seen[address]} and {label}")
            else:
                seen[address] = label

    if report.failures == failures_before:
        report.pass_("Gateways and static hosts do not contain duplicate addresses")


def validate_vlan_plan(vlan: VLANPlan, report: Report) -> None:
    print(f"\nVLAN {vlan.vlan_id} - {vlan.name} ({vlan.network})")

    if is_usable_host(vlan.gateway, vlan.network):
        report.pass_(f"Gateway {vlan.gateway} is a usable host address in {vlan.network}")
    else:
        report.fail(f"Gateway {vlan.gateway} is not a usable host address in {vlan.network}")

    if vlan.dhcp_range is None:
        report.pass_("No DHCP range configured for this VLAN")
    else:
        if int(vlan.dhcp_range.start) > int(vlan.dhcp_range.end):
            report.fail(
                f"DHCP range start {vlan.dhcp_range.start} "
                f"is after end {vlan.dhcp_range.end}"
            )
        else:
            report.pass_(
                f"DHCP range order is valid: "
                f"{vlan.dhcp_range.start} - {vlan.dhcp_range.end}"
            )

        if (
            is_usable_host(vlan.dhcp_range.start, vlan.network)
            and is_usable_host(vlan.dhcp_range.end, vlan.network)
        ):
            report.pass_(f"DHCP range is inside {vlan.network}")
        else:
            report.fail(
                f"DHCP range {vlan.dhcp_range.start} - {vlan.dhcp_range.end} "
                f"is not fully inside {vlan.network}"
            )

        if address_in_range(vlan.gateway, vlan.dhcp_range):
            report.fail(f"Gateway {vlan.gateway} is inside the DHCP range")
        else:
            report.pass_(f"Gateway {vlan.gateway} is outside the DHCP range")

    for host in vlan.static_hosts:
        if is_usable_host(host.ipv4_address, vlan.network):
            report.pass_(
                f"Static host {host.name} ({host.ipv4_address}) "
                f"is inside {vlan.network}"
            )
        else:
            report.fail(
                f"Static host {host.name} ({host.ipv4_address}) "
                f"is not a usable host in {vlan.network}"
            )

        if host.ipv4_address == vlan.gateway:
            report.fail(f"Static host {host.name} uses the gateway address {vlan.gateway}")

        if vlan.dhcp_range is not None:
            if address_in_range(host.ipv4_address, vlan.dhcp_range):
                report.fail(
                    f"Static host {host.name} ({host.ipv4_address}) "
                    f"is inside the DHCP range"
                )
            else:
                report.pass_(
                    f"Static host {host.name} ({host.ipv4_address}) "
                    f"is outside the DHCP range"
                )


def validate_dns_records(
    dns_records: list[DNSRecord],
    vlans: list[VLANPlan],
    report: Report,
) -> None:
    print("\nDNS records")

    static_host_index = build_static_host_index(vlans)

    if not dns_records:
        report.warn("No DNS records defined")
        return

    for record in dns_records:
        if record.record_type != "A":
            report.warn(
                f"DNS record {record.hostname} has unsupported type "
                f"{record.record_type}; only A records are validated"
            )
            continue

        vlan = find_vlan_for_address(record.address, vlans)

        if vlan is None:
            report.fail(
                f"DNS A record {record.hostname} points to {record.address}, "
                "which is outside all VLAN networks"
            )
        else:
            report.pass_(
                f"DNS A record {record.hostname} points to {record.address} "
                f"in VLAN {vlan.vlan_id} ({vlan.name})"
            )

        if record.address in static_host_index:
            report.pass_(
                f"DNS A record {record.hostname} points to known static host "
                f"{static_host_index[record.address].name}"
            )
        else:
            report.warn(
                f"DNS A record {record.hostname} points to {record.address}, "
                "but that address is not listed as a static host"
            )


def validate_plan(plan: AddressingPlan) -> Report:
    report = Report()

    validate_vlan_ids_are_unique(plan.vlans, report)
    validate_networks_do_not_overlap(plan.vlans, report)
    validate_duplicate_addresses(plan.vlans, report)

    for vlan in plan.vlans:
        validate_vlan_plan(vlan, report)

    validate_dns_records(plan.dns_records, plan.vlans, report)

    return report


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the Small Office Network Lab IPv4 addressing plan."
    )

    default_plan_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "addressing-plan.json"
    )

    parser.add_argument(
        "plan_file",
        nargs="?",
        default=str(default_plan_path),
        help="Path to the addressing-plan JSON file",
    )

    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    plan_path = Path(args.plan_file)

    print("Small Office Network Addressing Plan Validation")
    print("=" * 48)
    print(f"Plan file: {plan_path}")

    try:
        plan = load_addressing_plan(plan_path)
    except PlanFormatError as exc:
        print(f"FAIL: {exc}")
        print("\nResult: FAIL")
        return 1

    report = validate_plan(plan)

    print("\nValidation summary")
    print("-" * 18)
    print(f"Passes:   {report.passes}")
    print(f"Warnings: {report.warnings}")
    print(f"Failures: {report.failures}")

    if report.failures == 0:
        print("Result: PASS")
        return 0

    print("Result: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
