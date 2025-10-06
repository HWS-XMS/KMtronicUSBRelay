"""
KMTronic USB Relay Controller

Python API for controlling KMTronic USB relay boards.
"""

from .relay import KMTronicUSB4Relay, RelayState

__version__ = "1.0.0"
__all__ = ["KMTronicUSB4Relay", "RelayState"]
