"""Setup configuration for kmtronic-relay package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="kmtronic-relay",
    version="1.0.0",
    author="Marvin Sass",
    author_email="marvin.sass@dismail.de",
    description="Python API for KMTronic USB relay boards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HWS-XMS/KMtronicUSBRelay",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyserial>=3.5",
    ],
    keywords="kmtronic relay usb hardware automation",
    project_urls={
        "Bug Reports": "https://github.com/HWS-XMS/KMtronicUSBRelay/issues",
        "Source": "https://github.com/HWS-XMS/KMtronicUSBRelay",
    },
)
