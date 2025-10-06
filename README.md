# KMTronic USB 4 RELAY v1.0 Python API

Python library for controlling KMTronic USB 4 relay boards with property-based control.

## Installation

### From PyPI (once published)

```bash
pip install kmtronic-relay
```

### From source

```bash
git clone git@github.com:HWS-XMS/KMtronicUSBRelay.git
cd KMtronicUSBRelay
pip install -e .
```

## Quick Start

```python
from kmtronic_relay import KMTronicUSB4Relay, RelayState

# Auto-detect and initialize
relay = KMTronicUSB4Relay()

# Control individual relays using properties
relay.relay_0.state = RelayState.NO  # Energize relay 0 (Normally Open)
relay.relay_1.state = RelayState.NC  # De-energize relay 1 (Normally Closed)

# Read state
print(relay.relay_2.state)  # RelayState.NO or RelayState.NC

# Close connection when done
relay.close()
```

## Context Manager Usage (Recommended)

```python
from kmtronic_relay import KMTronicUSB4Relay, RelayState

with KMTronicUSB4Relay() as relay:
    relay.relay_0.state = RelayState.NO
    relay.relay_1.state = RelayState.NO
    # Connection automatically closed on exit
```

## API Reference

### KMTronicUSB4Relay

Main controller class for the KMTronic USB 4 RELAY v1.0.

#### Initialization

```python
relay = KMTronicUSB4Relay()  # Auto-detects relay board
```

**Raises:**
- `ValueError`: If relay board cannot be auto-detected
- `ConnectionError`: If connection to relay board fails

#### Relay Properties

- `relay.relay_0` - Relay channel 0 (0-indexed)
- `relay.relay_1` - Relay channel 1
- `relay.relay_2` - Relay channel 2
- `relay.relay_3` - Relay channel 3

Each relay has a `state` property that can be read or set:

```python
relay.relay_0.state = RelayState.NO  # Set state
current_state = relay.relay_0.state   # Read state
```

#### RelayState Enum

- `RelayState.NO` - Normally Open (energized/closed)
- `RelayState.NC` - Normally Closed (de-energized/open)

#### Methods

- `close()` - Close the serial connection

#### Context Manager Support

The class supports context manager protocol for automatic cleanup:

```python
with KMTronicUSB4Relay() as relay:
    # Your code here
    pass
# Connection automatically closed
```

## Examples

### Toggle a Relay

```python
from kmtronic_relay import KMTronicUSB4Relay, RelayState
import time

with KMTronicUSB4Relay() as relay:
    relay.relay_0.state = RelayState.NO
    time.sleep(0.5)
    relay.relay_0.state = RelayState.NC
```

### Control All Relays

```python
from kmtronic_relay import KMTronicUSB4Relay, RelayState

with KMTronicUSB4Relay() as relay:
    # Turn all relays on
    relay.relay_0.state = RelayState.NO
    relay.relay_1.state = RelayState.NO
    relay.relay_2.state = RelayState.NO
    relay.relay_3.state = RelayState.NO

    # Turn all relays off
    relay.relay_0.state = RelayState.NC
    relay.relay_1.state = RelayState.NC
    relay.relay_2.state = RelayState.NC
    relay.relay_3.state = RelayState.NC
```

## Hardware Details

### Supported Devices

- KMTronic USB 4 RELAY v1.0

### Auto-Detection

The library auto-detects the relay board by scanning for:
1. FTDI devices with custom VID/PID (0x1337:0x0088)
2. Generic FTDI, CH340, or USB-Serial devices

### Serial Communication Parameters

- Baud rate: 9600
- Data bits: 8
- Stop bits: 1
- Parity: None

### Protocol

Each command consists of 3 bytes: `[0xFF, relay_number, state]`

- Byte 1: `0xFF` (command prefix)
- Byte 2: Relay number (1-4, hardware addressing)
- Byte 3: State (`0x01` for NO/energized, `0x00` for NC/de-energized)

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Building Package

```bash
python -m build
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Marvin Sass
