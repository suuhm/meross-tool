# MEROSS-TOOL

### Local Meross Smart Plug Controller · Discovery · Inspector · Security Research

A lightweight Python CLI tool to discover, inspect and control Meross smart plugs directly over your local network — without relying on the Meross Cloud.

<img width="384" height="256" alt="Glossy MEROSS-TOOL Tech-Logo mit Smart-Plug" src="https://github.com/user-attachments/assets/a608cad5-cfd4-4d08-88ef-5bf97ddcb9a3" />

---

## Overview

**MEROSS-TOOL** is a command-line utility for communicating with Meross smart plugs through their local HTTP-based API.

It provides device discovery, hardware and firmware inspection, relay control and access to additional device capabilities.

Beyond device management, this project also explores the security characteristics of Meross IoT devices, particularly their local API implementation, authentication mechanisms and network exposure.

No external Python packages are required.

### Features

| Feature                | Description                                                |
| :--------------------- | :--------------------------------------------------------- |
| 🔍 Device Discovery    | Automatically scan your local IPv4 subnet                  |
| 📡 Device Inspector    | Retrieve hardware and firmware information                 |
| 🟢 Relay Control       | Switch your smart plug ON or OFF                           |
| 🧩 API Discovery       | Query supported API namespaces                             |
| 🌙 LED Control         | Enable or disable the device status LED                    |
| 📊 Runtime Information | Retrieve available runtime and Wi-Fi information           |
| 📄 JSON Output         | Export device information in JSON format                   |
| ⚡ Multithreading       | Scan multiple network hosts concurrently                   |
| 🔬 Security Research   | Investigate local API security and authentication behavior |

---

## Getting Started

### Requirements

- Python 3.9 or newer
- A Meross smart plug supporting the local HTTP API
- Computer and smart plug connected to the same reachable network
- Network access to the device on TCP port `80`

### Installation

Clone the repository:

```bash
git clone https://github.com/suuhm/MEROSS-TOOL.git
```

Navigate into the directory:

```bash
cd MEROSS-TOOL
```

Run the tool:

```bash
python3 meross_tool.py
```

No additional dependencies or package installations are necessary.

---

## 🎮 Usage

### Interactive Mode

```bash
python3 meross_tool.py
```

### Discover Devices

Automatically detect your local IPv4 `/24` subnet:

```bash
python3 meross_tool.py --discover
```

Specify a subnet manually:

```bash
python3 meross_tool.py --discover 192.168.178.0/24
```

### Device Information

```bash
python3 meross_tool.py 192.168.178.50 --info
```

### Relay Control

Switch ON:

```bash
python3 meross_tool.py 192.168.178.50 --on
```

Switch OFF:

```bash
python3 meross_tool.py 192.168.178.50 --off
```

### LED Control

Disable the physical status LED:

```bash
python3 meross_tool.py 192.168.178.50 --led-off
```

Enable the physical status LED:

```bash
python3 meross_tool.py 192.168.178.50 --led-on
```

### Inspect Additional Capabilities

```bash
python3 meross_tool.py 192.168.178.50 --scan
```

---

## Command Reference

| Argument           | Description                      |
| :----------------- | :------------------------------- |
| `-d`, `--discover` | Discover Meross devices          |
| `-i`, `--info`     | Display device information       |
| `--on`             | Switch relay ON                  |
| `--off`            | Switch relay OFF                 |
| `-s`, `--scan`     | Inspect capabilities and runtime |
| `--led-off`        | Disable status LED               |
| `--led-on`         | Enable status LED                |
| `-j`, `--json`     | Output results as JSON           |
| `-q`, `--quiet`    | Suppress ASCII banner            |
| `-h`, `--help`     | Display help information         |

---

## How It Works

MEROSS-TOOL communicates directly with Meross devices over the local network.

It sends JSON-formatted HTTP POST requests to:

```text
http://DEVICE_IP/config
```

The communication uses Meross API namespaces, including:

```text
Appliance.System.All
Appliance.Control.ToggleX
Appliance.System.Ability
Appliance.System.DNDMode
Appliance.System.Runtime
```

### Communication Structure

A typical request consists of two main components:

**Header**

- `messageId`
- `method`
- `namespace`
- `payloadVersion`
- `timestamp`
- `sign`

**Payload**

Contains the parameters required for the requested operation.

The API uses its own application-level message structure on top of HTTP.

---

# Security Research & Vulnerability Analysis

## 1. Background

Internet of Things (IoT) devices increasingly combine cloud connectivity, local network interfaces and third-party smart home integrations.

While these integrations improve interoperability, they also introduce additional attack surfaces.

A device may implement several communication mechanisms simultaneously. Consequently, the security of one integration does not automatically guarantee the security of another.

MEROSS-TOOL provides functionality to inspect the local API behavior of Meross smart plugs and investigate these interfaces in a controlled environment.

## 2. Previously Documented Security Research

### Hochschule der Medien Stuttgart (2021)

**Research:** [Why It's So Easy to Hack Your Smart Home](https://blog.mi.hdm-stuttgart.de/index.php/2021/09/09/why-its-so-easy-to-hack-your-smart-home/)

Author: Martin Bock
Institution: Hochschule der Medien Stuttgart
Publication date: September 9, 2021

The research documents security weaknesses in a Meross MSS210 smart plug.

The investigation describes:

- An accessible local HTTP service on TCP port 80.
- A web-based administration interface.
- Exposure of sensitive configuration information.
- Communication through the `/config` endpoint.
- Retrieval of hardware, firmware and device information.
- Local relay manipulation through the `Appliance.Control.ToggleX` namespace.

The research demonstrates that weaknesses in a manufacturer's local API can undermine the security assumptions of otherwise secure smart home ecosystems.

**Important:** The tested device used hardware revision 4.0.0 and firmware 4.1.7. These findings must not automatically be generalized to every subsequent hardware and firmware revision.

### CVE-2021-35067 – Meross MSG100

[Official CVE Record](https://www.cve.org/CVERecord?id=CVE-2021-35067)

Published: October 7, 2021
Classification: CWE-294 – Authentication Bypass by Capture-Replay

This vulnerability concerns Meross MSG100 garage door opener devices running firmware versions before 3.2.3.

The documented weakness allows replay of previously captured or similar messages. For example, an attacker may be able to replay a captured closing command as an opening command.

**Important distinction:** CVE-2021-35067 concerns the MSG100. It is not a CVE assigned to the MSS210.

It is included here as additional evidence of previously documented security problems in the Meross product ecosystem, not as proof that the MSS210 is affected by this specific CVE.

## 3. Local API Security Investigation

The local Meross API is particularly interesting from a security perspective.

The current MEROSS-TOOL implementation constructs requests using the following structure:

```json
{
  "header": {
    "method": "GET",
    "namespace": "Appliance.System.All",
    "payloadVersion": 1,
    "sign": "00000000000000000000000000000000"
  },
  "payload": {}
}
```

The implementation uses a constant zero-filled signature value.

This behavior makes signature validation an important subject for further investigation.

The following security properties are relevant:

| Security Property      | Research Question                                          |
| :--------------------- | :--------------------------------------------------------- |
| Authentication         | Does the device require authentication for local requests? |
| Authorization          | Are operations restricted to authorized clients?           |
| Signature Validation   | Is the message signature actually verified?                |
| Replay Protection      | Are previously transmitted messages rejected?              |
| Transport Security     | Is local communication protected against interception?     |
| Information Disclosure | What device information is exposed through the API?        |

A successful response to a request containing an invalid signature would be an indication that the signature is not being enforced for that particular operation and firmware configuration.

Such a result should be documented separately for every tested device revision.

## 4. Hardware and Firmware Observations

### Test Device

| Property          | Observed Configuration |
| :---------------- | :--------------------- |
| Manufacturer      | Meross                 |
| Model             | MSS210                 |
| Hardware Revision | v7.0.0                 |
| Firmware Version  | 7.3.2                  |
| Firmware Date     | August 2023            |
| Interface         | Local HTTP API         |
| Endpoint          | `/config`              |
| Port              | TCP 80                 |

The device configuration above represents an individual test environment.

### Research Objective

The primary objective is to determine whether security behavior documented in earlier MSS210 research can also be reproduced on newer hardware and firmware.

In particular:

1. Determine whether local API requests require authentication.
2. Examine how the device handles invalid signature values.
3. Verify whether relay operations are subject to authorization checks.
4. Investigate whether replay protection is implemented.
5. Compare observed behavior with previously published research.

**Research limitation:** The 2021 MSS210 publication does not establish the security status of firmware 7.3.2. The newer hardware and firmware combination requires independent testing. No claim of an unpatched vulnerability should be made without reproducible evidence.

## 5. Responsible Disclosure

Security findings should be reported responsibly to the manufacturer before public disclosure.

Meross provides an official vulnerability disclosure process:

[Meross Security Advisory Policy](https://www.meross.com/en-gc/security-advisory-policy)

According to its published policy:

- Reports should contain product, hardware and firmware details.
- Reproduction steps and technical evidence should be provided.
- Research should use the latest available firmware.
- Reports should be submitted in English.
- Meross does not operate a vulnerability bounty program.
- Researchers are asked to coordinate disclosure and allow 180 calendar days after acknowledgment before public disclosure.

Security research should be limited to devices owned by the researcher or systems for which explicit authorization exists.

---

## References & Further Reading

1. **Bock, M. (2021).** *Why It's So Easy to Hack Your Smart Home.* Hochschule der Medien Stuttgart.
   [https://blog.mi.hdm-stuttgart.de/index.php/2021/09/09/why-its-so-easy-to-hack-your-smart-home/](https://blog.mi.hdm-stuttgart.de/index.php/2021/09/09/why-its-so-easy-to-hack-your-smart-home/)

2. **CVE-2021-35067.** Meross MSG100 Capture-Replay Vulnerability.
   [https://www.cve.org/CVERecord?id=CVE-2021-35067](https://www.cve.org/CVERecord?id=CVE-2021-35067)

3. **Meross.** Security Advisory Policy.
   [https://www.meross.com/en-gc/security-advisory-policy](https://www.meross.com/en-gc/security-advisory-policy)

4. **Meross.** Security Advisory Submission Portal.
   [https://www.meross.com/en-gc/support/security-advisory](https://www.meross.com/en-gc/support/security-advisory)

---

## ⚠️ Compatibility & Disclaimer

- Not every Meross device supports all local API namespaces.
- Available functions depend on the individual device model and firmware.
- LED and runtime features may not be supported by every device.
- Device discovery only identifies devices responding to the expected local API.
- Automatic subnet detection assumes a `/24` network.
- Security research findings must be verified independently for each device revision.

**Security Notice:** This tool communicates over HTTP without transport encryption. Use it only on trusted networks and with devices you own or are authorized to manage.

MEROSS-TOOL is an independent research and development project. It is not affiliated with, endorsed by, or supported by Meross.


