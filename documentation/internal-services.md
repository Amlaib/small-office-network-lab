# Internal DNS and Web Services

## Objective

Configure the Internal Server to provide a simple internal web page and DNS name resolution for client devices.

This stage demonstrates access to an internal service by hostname rather than only by IP address.

## Server configuration

The Internal Server remains statically addressed.

| Device | IP address | Default gateway | DNS client setting |
|---|---|---|---|
| Internal-Server | 192.168.40.10 | 192.168.40.1 | Not required for this lab |

The server provides DNS service to clients, but its own DNS client setting is not required for this lab.

HTTP service was enabled on the server.

DNS service was also enabled with the following A record:

| Hostname | Record type | IP address |
|---|---|---|
| intranet.office.test | A | 192.168.40.10 |

## DHCP update

R1 DHCP pools were updated to provide the internal DNS server address to client devices.

| VLAN | DHCP DNS server |
|---:|---|
| 10 | 192.168.40.10 |
| 20 | 192.168.40.10 |
| 30 | 192.168.40.10 |

## Test results

Client devices successfully resolved `intranet.office.test` to `192.168.40.10` using the internal DNS server configured through DHCP.

Clients could access the internal web page using:

```text
http://intranet.office.test
```

 ℹ️ _Guest access is currently allowed because access-control rules have not yet been applied. Guest restrictions will be configured in a later stage._

## Troubleshooting example

The DNS record was initially entered on the server but not saved in the DNS service entries list.

Clients could still reach the server by IP address, but hostname resolution failed.

After saving the DNS record correctly, clients resolved intranet.office.test to 192.168.40.10 and hostname-based access worked.

This demonstrated the difference between IP connectivity and DNS resolution.

### Security note

HTTP is used in this lab to demonstrate basic internal web-service reachability and DNS name resolution.

In a real production or financial-services environment, internal web services should normally use HTTPS with properly managed certificates. HTTPS/TLS would provide encryption, server identity verification and protection against traffic tampering.

Secure access controls are handled later in this project through guest-network restrictions.

## Evidence
- `14-server-http-service.png`
- `15-server-dns-record.png`
- `16-client-dns-resolution.png`
- `17-internal-web-by-hostname.png`