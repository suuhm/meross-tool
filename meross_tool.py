#!/usr/bin/env python3

"""
MEROSS-TOOL v.1.3
Local Meross smart-plug discovery, inspection and control.

(c) 2026 by suuhm : https://github.com/suuhm/meross-tool

Examples:
    python3 meross_tool.py
    python3 meross_tool.py 192.168.178.50 --info
    python3 meross_tool.py --discover
    python3 meross_tool.py --discover 192.168.178.0/24
    python3 meross_tool.py 192.168.178.50 --on
    python3 meross_tool.py 192.168.178.50 --off --json
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
import json
import socket
import sys
import time
import urllib.request
import uuid


print("\n\033[0;95;45m░▒\033[0;97m    \033[0;95;45m█\033[0;95m█\033[0;37m \033[0;97m \033[0;95;45m▒▓▓██\033[0;37m  \033[0;95;45m▒▒▓▓██\033[0;37m  \033[0;97m \033[0;95;45m▒▓▓██\033[0;37m  \033[0;95m▄\033[0;95;45m▓▓▓▓█\033[0;95m▄\033[0;37m \033[0;95m▄\033[0;95;45m▓▓▓▓█\033[0;95m▄\033[0;37m \033[0;35m▐\033[0;95;45m░▒▒▓▓██\033[0;95m▌\033[0;37m \033[0;97m \033[0;95;45m▒▓▓██\033[0;37m  \033[0;97m \033[0;95;45m▒▓▓██\033[0;37m  \033[0;95;45m▒▒\033[0;37m     \033[0m")
print("\033[0;97m \033[0;95;45m░▒\033[0;35m▌\033[0;95m▐\033[0;95;45m▓█\033[0;37m  \033[0;95;45m░▒\033[0;97m   \033[0;95;45m██\033[0;37m \033[0;97m \033[0;95;45m▒▒\033[0;97m  \033[0;95;45m██\033[0;37m \033[0;95;45m░▒\033[0;97m   \033[0;95;45m██\033[0;37m \033[0;95;45m▒▒\033[0;97m   \033[0;35m \033[0;95;45m█\033[0;37m \033[0;95;45m▒▒\033[0;97m   \033[0;35m \033[0;95;45m█\033[0;37m \033[0;35m   \033[0;95;45m▒▒▓\033[0;37m    \033[0;95;45m░▒\033[0;97m   \033[0;95;45m██\033[0;37m \033[0;95;45m░▒\033[0;97m   \033[0;95;45m██\033[0;37m \033[0;95;45m░▒\033[0;37m     \033[0m")
print("\033[0;97m \033[0;95;45m░░\033[0;95m▐▌\033[0;95;45m▓▓\033[0;37m  \033[0;95;45m░░\033[0;35m▄▄\033[0;37m    \033[0;97m \033[0;95;45m░▒\033[0;97m  \033[0;95;45m▓█\033[0;37m \033[0;95;45m░░\033[0;97m   \033[0;95;45m▓█\033[0;37m \033[0;95;45m░▒\033[0;95m▄▄▄▄\033[0;37m  \033[0;95;45m░▒\033[0;95m▄▄▄▄\033[0;37m  \033[0;97m   \033[0;95;45m░▒▒\033[0;37m    \033[0;95;45m░░\033[0;97m   \033[0;95;45m▓█\033[0;37m \033[0;95;45m░░\033[0;97m   \033[0;95;45m▓█\033[0;37m \033[0;95;45m░░\033[0;37m     \033[0m")
print("\033[0;97m \033[0;95;45m ░\033[0;97m  \033[0;95;45m▒▓\033[0;37m  \033[0;95;45m ░\033[0;35m▀▀\033[0;37m    \033[0;97m \033[0;95;45m░░▒▒▓\033[0;37m  \033[0;95;45m ░\033[0;97m   \033[0;95;45m▓▓\033[0;37m \033[0;35m \033[0;95m▀▀▀▀\033[0;95;45m▓▓\033[0;37m \033[0;35m \033[0;95m▀▀▀▀\033[0;95;45m▓▓\033[0;37m \033[0;97m   \033[0;95;45m ░▒\033[0;37m    \033[0;95;45m ░\033[0;97m   \033[0;95;45m▓▓\033[0;37m \033[0;95;45m ░\033[0;97m   \033[0;95;45m▓▓\033[0;37m \033[0;95;45m ░\033[0;37m     \033[0m")
print("\033[0;97m \033[0;95;45m  \033[0;97m  \033[0;95;45m▒▒\033[0;37m  \033[0;95;45m  \033[0;97m   \033[0;95;45m▒▓\033[0;37m \033[0;97m \033[0;95;45m ░\033[0;97m \033[0;95;45m▒▒\033[0;37m  \033[0;95;45m  \033[0;97m   \033[0;95;45m▒▓\033[0;37m \033[0;35m█ \033[0;97m   \033[0;95;45m▒▓\033[0;37m \033[0;35m█ \033[0;97m   \033[0;95;45m▒▓\033[0;37m \033[0;97m   \033[0;95;45m  ░\033[0;37m    \033[0;95;45m  \033[0;97m   \033[0;95;45m▒▓\033[0;37m \033[0;95;45m  \033[0;97m   \033[0;95;45m▒▓\033[0;37m \033[0;95;45m  \033[0;97m   \033[0;95;45m▒▓\033[0m")
print("\033[0;95;45m  \033[0;97m    \033[0;95;45m▒▒\033[0;37m \033[0;97m \033[0;95;45m  ░░▒\033[0;37m  \033[0;95;45m  \033[0;97m   \033[0;95;45m▒▒\033[0;37m \033[0;97m \033[0;95;45m  ░░▒\033[0;37m  \033[0;35m▀\033[0;95;45m \033[0;35m█\033[0;95;45m░░▒\033[0;35m▀\033[0;37m \033[0;35m▀\033[0;95;45m \033[0;35m█\033[0;95;45m░░▒\033[0;35m▀\033[0;37m \033[0;97m   \033[0;95;45m   \033[0;37m    \033[0;97m \033[0;95;45m  ░░▒\033[0;37m  \033[0;97m \033[0;95;45m  ░░▒\033[0;37m  \033[0;97m \033[0;95;45m  ░░▒\033[0;37m \033[0m\n")


VERSION = "1.3"

BANNER = r"""
                                                                                                                             
                          .-------------.
                         |      ON       |
                     .-  |   .------.    |
                    /    |   |\      \   |
                   |     |   | \  |  /   |
                   |     |   |  |   /    |
                   |     |   | / o /     |
                    \    |   |/___/      |
                   <-'   |               |
                         |      OFF      |
                          '-------------'


       Local API  |  Discovery  |  Device Inspector  |  Control
                              v{version}
""".format(version=VERSION)


def send_meross_command(ip, namespace, method="GET", payload=None, timeout=4):
    """Send a JSON command to a Meross device on the local network."""
    if payload is None:
        payload = {}

    url = f"http://{ip}/config"
    message = {
        "header": {
            "from": url,
            "messageId": uuid.uuid4().hex,
            "method": method,
            "namespace": namespace,
            "payloadVersion": 1,
            "sign": "00000000000000000000000000000000",
            "timestamp": int(time.time()),
        },
        "payload": payload,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(message).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError, TimeoutError):
        return None


def get_local_subnet():
    """Guess the active local /24 network."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        return str(ipaddress.IPv4Network(f"{local_ip}/24", strict=False))
    except (OSError, ValueError):
        return "192.168.178.0/24"
    finally:
        sock.close()


def get_toggle_state(digest):
    """Return the first relay's on/off value, handling missing API data."""
    toggles = digest.get("togglex") or []
    if isinstance(toggles, dict):
        toggles = [toggles]
    return bool(toggles and toggles[0].get("onoff") == 1)


def probe_single_host(ip_str):
    """Check port 80 and query the Meross System.All namespace."""
    try:
        with socket.create_connection((ip_str, 80), timeout=0.4):
            pass
    except OSError:
        return None

    response = send_meross_command(
        ip_str, "Appliance.System.All", "GET", timeout=1.5
    )
    if not response:
        return None

    all_data = response.get("payload", {}).get("all")
    if not all_data:
        return None

    system = all_data.get("system", {})
    hardware = system.get("hardware", {})
    firmware = system.get("firmware", {})
    state = "ON" if get_toggle_state(all_data.get("digest", {})) else "OFF"

    return {
        "ip": ip_str,
        "type": hardware.get("type", "unknown"),
        "hw_version": hardware.get("version", "unknown"),
        "fw_version": firmware.get("version", "unknown"),
        "mac": hardware.get("macAddress", "unknown"),
        "uuid": hardware.get("uuid", "unknown"),
        "state": state,
    }


def discover_devices(subnet=None, as_json=False):
    """Scan a subnet concurrently for devices responding to the Meross API."""
    subnet = subnet or get_local_subnet()

    try:
        network = ipaddress.IPv4Network(subnet, strict=False)
    except ValueError as error:
        message = f"Invalid subnet: {error}"
        print(json.dumps({"error": message}) if as_json else f"[!] {message}")
        return []

    if not as_json:
        print(f"\n[*] Scanning {network} for local Meross devices...")

    found = []
    hosts = [str(address) for address in network.hosts()]

    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = [executor.submit(probe_single_host, host) for host in hosts]
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception:
                result = None
            if result:
                found.append(result)

    found.sort(key=lambda device: ipaddress.IPv4Address(device["ip"]))

    if as_json:
        print(json.dumps({"subnet": str(network), "devices": found}, indent=2))
    elif not found:
        print("[-] No Meross HTTP devices found in this subnet.")
    else:
        print(f"\n[+] Found {len(found)} Meross device(s):\n")
        print(
            f"  {'IP ADDRESS':<16} {'MODEL':<12} {'HW/FW':<18} "
            f"{'STATE':<6} MAC ADDRESS"
        )
        print("  " + "-" * 76)
        for device in found:
            hw_fw = f"v{device['hw_version']} / v{device['fw_version']}"
            print(
                f"  {device['ip']:<16} {device['type']:<12} "
                f"{hw_fw:<18} {device['state']:<6} {device['mac']}"
            )

    return found


def print_system_info(ip, as_json=False):
    """Fetch and display hardware, firmware, network and relay information."""
    if not as_json:
        print(f"\n[*] Fetching device information from {ip}...")

    response = send_meross_command(ip, "Appliance.System.All", "GET")
    if not response or "payload" not in response:
        error = {"error": f"Failed to reach {ip}"}
        print(json.dumps(error) if as_json else f"[!] {error['error']}.")
        return

    all_data = response["payload"].get("all", {})
    system = all_data.get("system", {})
    hardware = system.get("hardware", {})
    firmware = system.get("firmware", {})
    online = system.get("online", {})
    digest = all_data.get("digest", {})
    is_on = get_toggle_state(digest)

    if as_json:
        print(json.dumps({
            "ip": ip,
            "state": "ON" if is_on else "OFF",
            "onoff": int(is_on),
            "hardware": hardware,
            "firmware": firmware,
            "online": online,
            "digest": digest,
        }, indent=2))
        return

    print("\n" + "=" * 64)
    print(f"  DEVICE OVERVIEW — {hardware.get('type', 'UNKNOWN').upper()}")
    print("=" * 64)
    print(f"  Relay State      : {'ON' if is_on else 'OFF'}")
    print(f"  Hardware         : v{hardware.get('version', 'N/A')}")
    print(f"  Chip             : {hardware.get('chipType', 'N/A')}")
    print(f"  Firmware         : v{firmware.get('version', 'N/A')}")
    print(f"  Build            : {firmware.get('compileTime', 'N/A')}")
    print(f"  HomeKit Version  : {firmware.get('homekitVersion', 'N/A')}")
    print("-" * 64)
    print(f"  Internal IP      : {firmware.get('innerIp', 'N/A')}")
    print(f"  MAC Address      : {hardware.get('macAddress', 'N/A')}")
    print(f"  Wi-Fi MAC        : {firmware.get('wifiMac', 'N/A')}")
    print(f"  Device UUID      : {hardware.get('uuid', 'N/A')}")
    print("-" * 64)
    print(f"  Cloud Server     : {firmware.get('server', 'N/A')}:{firmware.get('port', 'N/A')}")
    print(f"  Cloud User ID    : {firmware.get('userId', 'N/A')}")
    print(f"  Online Status    : {online.get('status', 'N/A')} (2 = connected)")
    print("=" * 64)


def toggle_plug(ip, state, as_json=False):
    """Switch relay channel 0 ON (1) or OFF (0)."""
    payload = {"togglex": {"channel": 0, "onoff": state}}
    response = send_meross_command(
        ip, "Appliance.Control.ToggleX", "SET", payload
    )
    success = bool(
        response and response.get("header", {}).get("method") == "SETACK"
    )
    status = "ON" if state == 1 else "OFF"

    if as_json:
        print(json.dumps({
            "ip": ip,
            "action": "toggle",
            "state": status,
            "success": success,
        }, indent=2))
    elif success:
        print(f"\n[+] Smart plug switched {status}.")
    else:
        print("\n[-] Switch command rejected or device unreachable.")


def check_hidden_features(ip, as_json=False):
    """Query additional namespaces and device capabilities."""
    if not as_json:
        print(f"\n[*] Checking capabilities on {ip}...")

    ability_response = send_meross_command(
        ip, "Appliance.System.Ability", "GET"
    )
    abilities = []
    if ability_response:
        abilities = sorted(
            ability_response.get("payload", {})
            .get("ability", {}).keys()
        )

    dnd_response = send_meross_command(
        ip, "Appliance.System.DNDMode", "GET"
    )
    dnd_mode = None
    if dnd_response:
        dnd_mode = (
            dnd_response.get("payload", {})
            .get("DNDMode", {}).get("mode")
        )

    runtime_response = send_meross_command(
        ip, "Appliance.System.Runtime", "GET"
    )
    runtime = {}
    if runtime_response:
        runtime = (
            runtime_response.get("payload", {}).get("runtime", {})
        )

    if as_json:
        print(json.dumps({
            "ip": ip,
            "abilities": abilities,
            "dnd_led_off": dnd_mode == 1 if dnd_mode is not None else None,
            "runtime": runtime,
        }, indent=2))
        return

    if abilities:
        print("\n[+] Supported API namespaces:")
        for namespace in abilities:
            print(f"    • {namespace}")
    else:
        print("[-] No capability list returned.")

    if dnd_mode is not None:
        led_state = "OFF (stealth/night mode)" if dnd_mode == 1 else "ON (normal)"
        print(f"\n[+] Status LED: {led_state}")

    if runtime:
        print(f"[+] Wi-Fi signal: {runtime.get('signal', 'N/A')}%")


def set_dnd_led(ip, disable_led, as_json=False):
    """Set DND mode: 1 disables the status LED, 0 enables it."""
    payload = {"DNDMode": {"mode": 1 if disable_led else 0}}
    response = send_meross_command(
        ip, "Appliance.System.DNDMode", "SET", payload
    )
    success = bool(
        response and response.get("header", {}).get("method") == "SETACK"
    )

    if as_json:
        print(json.dumps({
            "ip": ip,
            "action": "led_dnd",
            "led_off": disable_led,
            "success": success,
        }, indent=2))
    elif success:
        state = "DISABLED (stealth)" if disable_led else "ENABLED (normal)"
        print(f"\n[+] Status LED {state}.")
    else:
        print("\n[-] Failed to change LED mode.")


def interactive_menu(ip):
    """Run the interactive command-line menu."""
    while True:
        print(f"\n{'─' * 48}")
        print(f"  MEROSS-TOOL  |  Target: {ip}")
        print(f"{'─' * 48}")
        print("  [1] Show device information")
        print("  [2] Switch plug ON")
        print("  [3] Switch plug OFF")
        print("  [4] Scan capabilities / hidden namespaces")
        print("  [5] Turn status LED OFF")
        print("  [6] Turn status LED ON")
        print("  [7] Discover devices / change target")
        print("  [0] Exit")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            print_system_info(ip)
        elif choice == "2":
            toggle_plug(ip, 1)
        elif choice == "3":
            toggle_plug(ip, 0)
        elif choice == "4":
            check_hidden_features(ip)
        elif choice == "5":
            set_dnd_led(ip, True)
        elif choice == "6":
            set_dnd_led(ip, False)
        elif choice == "7":
            devices = discover_devices()
            if devices:
                new_ip = input(
                    "\n  Enter target IP (Enter keeps current target): "
                ).strip()
                if new_ip:
                    ip = new_ip
        elif choice == "0":
            print("\n[*] MEROSS-TOOL closed.")
            break
        else:
            print("[!] Invalid selection.")


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "MEROSS-TOOL — Local Meross smart-plug controller, "
            "inspector and discovery"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s\n"
            "  %(prog)s 192.168.178.50 --info\n"
            "  %(prog)s --discover\n"
            "  %(prog)s --discover 192.168.178.0/24\n"
            "  %(prog)s 192.168.178.50 --on"
        ),
    )

    parser.add_argument(
        "ip", nargs="?",
        help="Target IP address of the Meross device",
    )
    parser.add_argument(
        "-d", "--discover", nargs="?", const="AUTO", metavar="SUBNET",
        help="Discover devices (optional CIDR subnet; default: auto)",
    )
    parser.add_argument(
        "-i", "--info", action="store_true",
        help="Display device, hardware and network information",
    )
    parser.add_argument("--on", action="store_true", help="Switch plug ON")
    parser.add_argument("--off", action="store_true", help="Switch plug OFF")
    parser.add_argument(
        "-s", "--scan", action="store_true",
        help="Scan supported namespaces and runtime information",
    )
    parser.add_argument(
        "--led-off", action="store_true",
        help="Disable the physical status LED (DND mode)",
    )
    parser.add_argument(
        "--led-on", action="store_true",
        help="Enable the physical status LED (normal mode)",
    )
    parser.add_argument(
        "-j", "--json", action="store_true",
        help="Print JSON output and suppress the banner",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Suppress the ASCII banner",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.quiet and not args.json:
        print(BANNER)

    if args.on and args.off:
        message = "Cannot use --on and --off simultaneously."
        print(json.dumps({"error": message}) if args.json else f"[!] {message}")
        sys.exit(1)

    if args.led_on and args.led_off:
        message = "Cannot use --led-on and --led-off simultaneously."
        print(json.dumps({"error": message}) if args.json else f"[!] {message}")
        sys.exit(1)

    if args.discover is not None:
        subnet = None if args.discover == "AUTO" else args.discover
        discover_devices(subnet=subnet, as_json=args.json)
        if not args.ip:
            return

    ip = args.ip
    if not ip:
        if args.json:
            print(json.dumps({"error": "No IP address provided"}))
            sys.exit(1)

        ip = input(
            "Enter Meross device IP address (or 'd' to discover): "
        ).strip()

        if ip.lower() == "d":
            devices = discover_devices()
            if not devices:
                sys.exit(1)
            ip = input("\nSelect target IP address: ").strip()

    if not ip:
        print("[!] No IP address provided. Exiting.")
        sys.exit(1)

    actions = (
        args.info or args.on or args.off or args.scan
        or args.led_off or args.led_on
    )

    if not actions:
        if args.json:
            print_system_info(ip, as_json=True)
        else:
            interactive_menu(ip)
        return

    if args.info:
        print_system_info(ip, as_json=args.json)
    if args.on:
        toggle_plug(ip, 1, as_json=args.json)
    if args.off:
        toggle_plug(ip, 0, as_json=args.json)
    if args.led_off:
        set_dnd_led(ip, True, as_json=args.json)
    if args.led_on:
        set_dnd_led(ip, False, as_json=args.json)
    if args.scan:
        check_hidden_features(ip, as_json=args.json)


if __name__ == "__main__":
    main()
