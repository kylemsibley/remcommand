from fabric import Connection
import winrm
import argparse
import getpass

def build_winrm_url(host, use_http):
    if host.startswith("http://") or host.startswith("https://"):
        return host
    else:
        if use_http:
            return f"http://{host}:5985/wsman"
        else:
            return f"https://{host}:5986/wsman"

def linux_ex(host, user, password, commands, sudo):
    # establish ssh connection
    conn = Connection(host=host, user=user, connect_kwargs={"password": password})
    outputs = {}

    try:
        for cmd in commands:
            if sudo:
                result = conn.sudo(cmd, hide=True, password=password)
            else:
                result = conn.run(cmd, hide=True)
            outputs[cmd]= result.stdout.strip()
    except Exception as e:
        outputs['error'] = f"Error in command execution: {str(e)}"
    return outputs

def windows_ex(host, user, password, commands, use_http):
    full_host = build_winrm_url(host, use_http)
    session = winrm.Session(full_host, auth=(user, password))
    outputs = {}

    try:
        for cmd in commands:
            result = session.run_ps(cmd)
            outputs[cmd] = result.std_out.decode('utf-8').strip()
    except Exception as e:
        outputs['error'] = f"Error in powershell command execution: {str(e)}"
    return outputs

def main():
    # argument parsing
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--linux', action='store_true', help='Target Linux server over ssh')
    group.add_argument('--windows', action='store_true', help='Target Windows server using winrm')
    parser.add_argument('--host', required=True, help='Target host')
    parser.add_argument('--user', required=True, help='Target username')
    parser.add_argument('--password', help='Target password (if not provided, you will be prompted securely)')
    parser.add_argument('--commands', required=True, help='Comma separated commands to execute on remote host')
    parser.add_argument('--http', action='store_true', help='Use HTTP (default is HTTPS) for WinRM connection')
    parser.add_argument('--sudo', action='store_true', help='Execute commands with sudo on Linux server')
    args = parser.parse_args()
    if not args.password:
        args.password = getpass.getpass("Enter password: ")
    args.commands = [cmd.strip() for cmd in args.commands.split(',')]

    if args.linux:
        outputs = linux_ex(args.host, args.user, args.password, args.commands, args.sudo)
    elif args.windows:
        outputs = windows_ex(args.host, args.user, args.password, args.commands, args.http)

    for cmd, out in outputs.items():
        print(f"Output for '{cmd}':\n{out}\n")

if __name__ == '__main__':
    main()
