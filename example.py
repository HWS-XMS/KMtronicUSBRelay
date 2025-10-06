#!/usr/bin/env python3
"""
Example script demonstrating KMTronic USB Relay API usage
"""

import time
from kmtronic_usb_relay import KMTronicUSBRelay


def main():
    print("=== KMTronic USB Relay Example ===\n")

    # List available ports
    print("Available serial ports:")
    for port in KMTronicUSBRelay.list_available_ports():
        print(f"  {port}")
    print()

    try:
        # Connect to relay board (auto-detect port)
        # Or specify manually: KMTronicUSBRelay(port='/dev/ttyUSB0')
        with KMTronicUSBRelay() as relay:
            print(f"Connected to relay board on {relay.port}\n")

            # Test individual relays
            print("Testing individual relays...")
            for i in range(1, 5):
                print(f"  Relay {i} ON")
                relay.turn_on(i)
                time.sleep(0.5)
                print(f"  Relay {i} OFF")
                relay.turn_off(i)
                time.sleep(0.5)

            print()

            # Test all relays on/off
            print("Turning all relays ON...")
            relay.turn_all_on()
            time.sleep(2)

            print("Turning all relays OFF...")
            relay.turn_all_off()
            time.sleep(1)

            # Test toggle
            print("Testing toggle on relay 1...")
            relay.toggle(1, delay=1.0)

            print("\nTest complete!")

    except ValueError as e:
        print(f"Error: {e}")
        print("\nTip: Specify the port manually if auto-detection fails:")
        print("  relay = KMTronicUSBRelay(port='/dev/ttyUSB0')  # Linux")
        print("  relay = KMTronicUSBRelay(port='COM3')          # Windows")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
