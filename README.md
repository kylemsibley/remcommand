# remcommand


A Python tool to execute commands on remote Linux and Windows servers.

This tool lets you run shell commands on Linux servers over SSH (using Fabric) and PowerShell commands on Windows servers via WinRM. It supports secure password prompting and offers options for command execution with sudo privileges on Linux.

## Features

- Dual Platform Support: Execute commands on both Linux (via SSH) and Windows (via WinRM).
- Multiple Commands: Accepts a comma-separated list of commands to run on the remote host.
- Sudo Support for Linux: Optionally run commands with `sudo`.
- Secure Password Handling: Prompts securely for a password if not provided as an argument.
- Configurable Connection: For Windows, choose between HTTP and HTTPS connections for WinRM.

## Requirements

- Python: 3.6 or higher
- Dependencies:
  - [Fabric](https://www.fabfile.org/)
  - [pywinrm](https://pypi.org/project/pywinrm/)

You can install the required packages via pip:

    pip install fabric pywinrm

## Installation

Clone the repository and install the dependencies:

    git clone https://github.com/yourusername/remote-command-executor.git
    cd remote-command-executor
    pip install -r requirements.txt  # If a requirements.txt file is provided

*Note: If you don’t have a requirements.txt file, install the packages manually as shown above.*

## Usage

Run the script with the appropriate flags based on your target system.

### Command-line Options

- `--linux`: Target a Linux server over SSH.
- `--windows`: Target a Windows server using WinRM.
- `--host`: Specify the target host (IP or domain).
- `--user`: Provide the username for authentication.
- `--password`: (Optional) Provide the password. If omitted, you will be prompted securely.
- `--commands`: Comma-separated list of commands to execute.
- `--http`: Use HTTP instead of HTTPS for WinRM connections (Windows only).
- `--sudo`: Run commands with `sudo` on Linux (Linux only).

### Examples

#### Executing Commands on a Linux Server

    python remote_exec.py --linux --host 192.168.1.10 --user myuser --commands "ls -l, whoami" --sudo

If you omit the `--password` flag, the script will prompt you to enter the password securely.

#### Executing Commands on a Windows Server

    python remote_exec.py --windows --host 192.168.1.20 --user Administrator --commands "ipconfig, hostname" --http
