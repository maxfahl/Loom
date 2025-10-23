#!/bin/bash

# vps-initial-setup.sh
# Description: Automates the initial security and user setup for a new Ubuntu/Debian Virtual Private Server.
# Purpose: Standardizes and accelerates the provisioning of new VPS instances, ensuring a secure baseline configuration.

# Usage: ./vps-initial-setup.sh --user <new-user> --ssh-key <path-to-pub-key> [--port <ssh-port>] [--disable-root-login] [--help]

# Configuration:
# DEFAULT_SSH_PORT: Default SSH port if not specified (default: 22)

# Error handling:
# Exits with 1 if required arguments are missing, user creation fails, or commands fail.

# --- Script Start ---

# Set default values
DEFAULT_SSH_PORT=22
NEW_USER=""
SSH_PUB_KEY_PATH=""
SSH_PORT="$DEFAULT_SSH_PORT"
DISABLE_ROOT_LOGIN=false

# Function to display help message
display_help() {
    echo "Usage: $0 --user <new-user> --ssh-key <path-to-pub-key> [--port <ssh-port>] [--disable-root-login] [--help]"
    echo ""
    echo "Automates initial security and user setup for a new Ubuntu/Debian VPS."
    echo ""
    echo "Arguments:"
    echo "  --user <new-user>          Specify the username for the new non-root user."
    echo "  --ssh-key <path-to-pub-key>  Path to the SSH public key file (e.g., ~/.ssh/id_rsa.pub) for the new user."
    echo ""
    echo "Options:"
    echo "  --port <ssh-port>          Specify a custom SSH port (default: 22)."
    echo "  --disable-root-login       Disable direct root login via SSH (recommended)."
    echo "  --help                     Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 --user deployuser --ssh-key ~/.ssh/id_rsa.pub --port 2222 --disable-root-login"
    echo "  $0 --user admin --ssh-key /tmp/my_key.pub"
    exit 0
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --user)
            NEW_USER="$2"
            shift
            ;;
        --ssh-key)
            SSH_PUB_KEY_PATH="$2"
            shift
            ;;
        --port)
            SSH_PORT="$2"
            shift
            ;;
        --disable-root-login)
            DISABLE_ROOT_LOGIN=true
            ;;
        --help)
            display_help
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            display_help
            ;;
        *)
            echo "Error: Positional arguments are not allowed. Use --user and --ssh-key." >&2
            display_help
            ;;
    esac
    shift
done

# Validate required arguments
if [[ -z "$NEW_USER" || -z "$SSH_PUB_KEY_PATH" ]]; then
    echo "Error: --user and --ssh-key are required arguments." >&2
    display_help
fi

if [[ ! -f "$SSH_PUB_KEY_PATH" ]]; then
    echo "Error: SSH public key file not found at '$SSH_PUB_KEY_PATH'." >&2
    exit 1
fi

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root." >&2
   exit 1
fi

echo "--- VPS Initial Setup ---"
echo "New User: $NEW_USER"
echo "SSH Public Key: $SSH_PUB_KEY_PATH"
echo "SSH Port: $SSH_PORT"
echo "Disable Root Login: $DISABLE_ROOT_LOGIN"
echo "-------------------------"

# 1. Update system
echo "Updating system packages..."
apt update -y && apt upgrade -y || { echo "Error: System update failed." >&2; exit 1; }

# 2. Create new user and grant sudo privileges
echo "Creating new user '$NEW_USER'..."
adduser --gecos "" --disabled-password "$NEW_USER" || { echo "Error: Failed to create user '$NEW_USER'." >&2; exit 1; }
usermod -aG sudo "$NEW_USER" || { echo "Error: Failed to add user '$NEW_USER' to sudo group." >&2; exit 1; }
echo "User '$NEW_USER' created and added to sudo group."

# 3. Set up SSH key for the new user
echo "Setting up SSH key for '$NEW_USER'..."
mkdir -p /home/"$NEW_USER"/.ssh || { echo "Error: Failed to create .ssh directory." >&2; exit 1; }
chmod 700 /home/"$NEW_USER"/.ssh || { echo "Error: Failed to set permissions on .ssh directory." >&2; exit 1; }
cat "$SSH_PUB_KEY_PATH" > /home/"$NEW_USER"/.ssh/authorized_keys || { echo "Error: Failed to copy SSH public key." >&2; exit 1; }
chmod 600 /home/"$NEW_USER"/.ssh/authorized_keys || { echo "Error: Failed to set permissions on authorized_keys." >&2; exit 1; }
chown -R "$NEW_USER":"$NEW_USER" /home/"$NEW_USER"/.ssh || { echo "Error: Failed to set ownership of .ssh directory." >&2; exit 1; }
echo "SSH public key added for '$NEW_USER'."

# 4. Configure SSH daemon
echo "Configuring SSH daemon..."
SSH_CONFIG_FILE="/etc/ssh/sshd_config"

# Change SSH Port
if [[ "$SSH_PORT" -ne "$DEFAULT_SSH_PORT" ]]; then
    sed -i "s/^#*Port .*/Port $SSH_PORT/" "$SSH_CONFIG_FILE"
    echo "SSH port changed to $SSH_PORT."
fi

# Disable root login
if $DISABLE_ROOT_LOGIN; then
    sed -i "s/^#*PermitRootLogin .*/PermitRootLogin no/" "$SSH_CONFIG_FILE"
    echo "Direct root login disabled."
fi

# Disable password authentication (rely on key-based)
sed -i "s/^#*PasswordAuthentication .*/PasswordAuthentication no/" "$SSH_CONFIG_FILE"
echo "Password authentication disabled."

# Restart SSH service
systemctl restart sshd || { echo "Error: Failed to restart SSH service." >&2; exit 1; }
echo "SSH daemon reconfigured and restarted."

# 5. Configure UFW firewall
echo "Configuring UFW firewall..."
apt install ufw -y || { echo "Error: Failed to install UFW." >&2; exit 1; }
ufw allow "$SSH_PORT"/tcp || { echo "Error: Failed to allow SSH port in UFW." >&2; exit 1; }
ufw allow http || { echo "Error: Failed to allow HTTP in UFW." >&2; exit 1; }
ufw allow https || { echo "Error: Failed to allow HTTPS in UFW." >&2; exit 1; }
ufw --force enable || { echo "Error: Failed to enable UFW." >&2; exit 1; }
echo "UFW firewall configured and enabled."

echo "--- VPS Initial Setup Complete ---"
echo "You can now log in as '$NEW_USER' using your SSH key on port $SSH_PORT."
echo "Remember to disable root login and password authentication for SSH if you haven't already."
exit 0
