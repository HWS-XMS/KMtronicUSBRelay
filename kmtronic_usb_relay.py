"""
KMTronic USB 4 RELAY v1.0 Python API

This module provides a simple interface for controlling KMTronic USB relay boards.
The relay communicates via USB using a Virtual COM Port (VCP) with the following parameters:
- Baud rate: 9600
- Data bits: 8
- Stop bits: 1
- Parity: None
"""

import serial
import serial.tools.list_ports
from enum import Enum
from typing import Optional
import time


class RelayState(Enum):
    """Relay state enumeration."""
    NO = True   # Normally Open (energized/closed)
    NC = False  # Normally Closed (de-energized/open)


class KMTronicUSB4Relay:
    """
    KMTronic USB 4 RELAY v1.0 controller.

    Auto-detects the relay board on initialization and provides
    property-based control for 4 relay channels (relay_0 through relay_3).

    Example:
        relay = KMTronicUSB4Relay()
        relay.relay_0.state = RelayState.NO  # Energize relay 0
        relay.relay_1.state = RelayState.NC  # De-energize relay 1
        print(relay.relay_2.state)           # Read state
    """

    # Command constants
    CMD_PREFIX = 0xFF

    class _Relay:
        """Individual relay channel."""

        def __init__(self, channel: int, controller: 'KMTronicUSB4Relay'):
            self._channel = channel
            self._controller = controller
            self._state = RelayState.NC

        @property
        def state(self) -> RelayState:
            """
            Get or set the relay state.

            Returns:
                RelayState.NO (Normally Open/energized) or
                RelayState.NC (Normally Closed/de-energized)

            Example:
                relay.relay_0.state = RelayState.NO
                current_state = relay.relay_0.state
            """
            return self._state

        @state.setter
        def state(self, value: RelayState):
            """Set relay state."""
            self._controller._send_command(self._channel + 1, value.value)
            self._state = value

    def __init__(self):
        """
        Initialize and auto-detect the KMTronic USB 4 RELAY v1.0.

        Raises:
            ValueError: If relay board cannot be auto-detected
            ConnectionError: If connection to relay board fails
        """
        self._port = self._auto_detect_port()
        if self._port is None:
            raise ValueError("Could not auto-detect KMTronic USB 4 RELAY v1.0")

        # Initialize serial connection
        try:
            self._serial = serial.Serial(
                port=self._port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            time.sleep(0.1)  # Stabilize connection
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to connect to relay board on {self._port}: {e}")

        # Initialize relay channels (0-indexed)
        self.relay_0 = self._Relay(0, self)
        self.relay_1 = self._Relay(1, self)
        self.relay_2 = self._Relay(2, self)
        self.relay_3 = self._Relay(3, self)

    def _auto_detect_port(self) -> Optional[str]:
        """
        Auto-detect the relay board's serial port.

        Returns:
            Port path if found, None otherwise
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # Check for FTDI with custom VID/PID (1337:0088) first
            if port.vid == 0x1337 and port.pid == 0x0088:
                return port.device
            # Fallback to generic FTDI/CH340 detection
            if any(vendor in port.description.lower() for vendor in ['ftdi', 'ch340', 'usb serial']):
                return port.device
        return None

    def _send_command(self, relay: int, state: bool):
        """
        Send command to the relay board.

        Args:
            relay: Relay number (1-4)
            state: True for NO (energized), False for NC (de-energized)
        """
        if not self._serial or not self._serial.is_open:
            raise ConnectionError("Serial connection is not open")

        # Build command: [0xFF, relay_number, state]
        command = bytes([self.CMD_PREFIX, relay, 0x01 if state else 0x00])
        self._serial.write(command)
        self._serial.flush()

    def close(self):
        """Close the serial connection."""
        if self._serial and self._serial.is_open:
            self._serial.close()

    def __del__(self):
        """Cleanup on destruction."""
        self.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    # Example usage
    print("Initializing KMTronic USB 4 RELAY v1.0...")

    try:
        relay = KMTronicUSB4Relay()
        print(f"Connected on {relay._port}")

        # Test relay 0
        print("\nTesting relay_0...")
        relay.relay_0.state = RelayState.NO
        print(f"relay_0 state: {relay.relay_0.state}")
        time.sleep(1)
        relay.relay_0.state = RelayState.NC
        print(f"relay_0 state: {relay.relay_0.state}")

        # Test relay 1
        print("\nTesting relay_1...")
        relay.relay_1.state = RelayState.NO
        time.sleep(1)
        relay.relay_1.state = RelayState.NC

        # Test all relays
        print("\nTurning all relays ON (NO)...")
        relay.relay_0.state = RelayState.NO
        relay.relay_1.state = RelayState.NO
        relay.relay_2.state = RelayState.NO
        relay.relay_3.state = RelayState.NO
        time.sleep(1)

        print("Turning all relays OFF (NC)...")
        relay.relay_0.state = RelayState.NC
        relay.relay_1.state = RelayState.NC
        relay.relay_2.state = RelayState.NC
        relay.relay_3.state = RelayState.NC

        print("\nTest complete!")
        relay.close()

    except Exception as e:
        print(f"Error: {e}")
