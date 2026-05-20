# Defender Advanced Hunting Queries

KQL queries for Microsoft Defender XDR Advanced Hunting,
organized by MITRE ATT&CK tactic.

## Usage

1. Browse to the tactic folder matching your investigation
2. Open the relevant .kql file
3. Customise let variables at the top (time range, exclusions, thresholds)
4. Paste into: Microsoft Defender XDR > Hunting > Advanced Hunting

## Folder Structure

| Folder                 | MITRE Tactic           | Tactic ID |
|------------------------|------------------------|-----------|
| 01-InitialAccess       | Initial Access         | TA0001    |
| 02-Execution           | Execution              | TA0002    |
| 03-Persistence         | Persistence            | TA0003    |
| 04-PrivilegeEscalation | Privilege Escalation   | TA0004    |
| 05-DefenseEvasion      | Defense Evasion        | TA0005    |
| 06-CredentialAccess    | Credential Access      | TA0006    |
| 07-Discovery           | Discovery              | TA0007    |
| 08-LateralMovement     | Lateral Movement       | TA0008    |
| 09-Collection          | Collection             | TA0009    |
| 10-CommandAndControl   | Command & Control      | TA0011    |
| 11-Exfiltration        | Exfiltration           | TA0010    |
| 12-Impact              | Impact                 | TA0040    |

## Data Sources

Queries use tables including:
- DeviceProcessEvents
- DeviceNetworkEvents
- DeviceFileEvents
- DeviceLogonEvents
- DeviceRegistryEvents
- EmailEvents
- IdentityLogonEvents
- AADSignInEventsBeta
- CloudAppEvents

## Contributing

PRs welcome. Every query must use the header template
found in /templates/query-header.kql

## References

- MITRE ATT&CK: https://attack.mitre.org
- Microsoft Defender Advanced Hunting:
  https://learn.microsoft.com/en-us/microsoft-365/security/defender/advanced-hunting-overview

## License

MIT
