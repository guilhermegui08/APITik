# APITik

## Overview

**APITik** is an application designed to function as an SDN (Software-Defined Networking) controller to manage one or more Mikrotik routers running RouterOS. This project was developed as part of a laboratory assignment for Information Technologies 23/24, focusing on creating a comprehensive management tool using the Mikrotik REST API.

## Features

APITik offers a range of functionalities to facilitate the management and monitoring of Mikrotik network devices. Key features include:

- **Multi-Device Control**: Manage multiple Mikrotik devices using a single application.
- **Interface Management**:
  - List all device interfaces.
  - List only wireless interfaces.
  - List, create, edit, and delete bridge interfaces and their associated ports.
- **Wireless Networks**:
  - Create, edit, and delete security profiles for wireless networks.
  - Activate, deactivate, and configure wireless networks.
- **Routing Management**:
  - List, create, edit, and delete static routes.
- **IP Address Management**:
  - List, create, edit, and delete IP addresses.
- **DHCP Server Management**:
  - List, create, edit, and delete DHCP servers.
- **DNS Server Management**:
  - Activate, deactivate, and configure the DNS server.

The application directly communicates with Mikrotik devices via the RouterOS REST API, ensuring efficient and real-time management capabilities.

## VPN Management

In addition to the core features, APITik also supports VPN configuration and management:
- **WireGuard VPN**:
  - Implement a server/client VPN setup using WireGuard.
  - Configure and manage the VPN entirely through the APITik application.
  - Support for various clients including Windows, Linux, and other devices.

## Technical Details

- **Programming Language**: Python
- **Graphical User Interface**: Tkinter

## Documentation

For detailed information on using the Mikrotik REST API, please refer to the official Mikrotik documentation: [Mikrotik REST API Documentation](https://help.mikrotik.com/docs/display/ROS/REST+API).

## Getting Started

To get started with APITik, follow the instructions below:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/APITik.git```

2. **Navigate to the project directory**:
   ```bash
   cd APITik```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt```

4. **Run the application**:
   ```bash
   python main.py```

## License
This project is licensed under the GPL-3.0 License. See the `LICENSE` file for details.
