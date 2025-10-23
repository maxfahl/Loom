
import argparse
import os
import re
import shutil

def get_system_ram_gb(default_ram_gb=8):
    """
    Attempts to get system RAM in GB. If psutil is not available, returns a default.
    In a real-world scenario, you'd use psutil.virtual_memory().total / (1024**3).
    """
    try:
        import psutil
        return psutil.virtual_memory().total / (1024**3)
    except ImportError:
        print(f"Warning: psutil not found. Using default RAM of {default_ram_gb} GB. "
              "Install psutil (pip install psutil) for accurate system RAM detection.")
        return default_ram_gb

def calculate_pg_params(total_ram_gb):
    """
    Calculates suggested PostgreSQL parameters based on total system RAM.
    These are general recommendations and may need fine-tuning.
    """
    params = {}

    # shared_buffers: Typically 25% of total RAM
    params['shared_buffers'] = f"{int(total_ram_gb * 0.25)}GB"

    # work_mem: For sorts and hash tables. Start with 4MB, adjust based on workload.
    # This is per-operation, so keep it reasonable.
    params['work_mem'] = "4MB"

    # maintenance_work_mem: For VACUUM, CREATE INDEX, ALTER TABLE. Typically 10-25% of RAM.
    params['maintenance_work_mem'] = f"{int(total_ram_gb * 0.1)}GB"

    # effective_cache_size: Estimate of total memory available for disk caching by the OS and database.
    # Typically 50-75% of total RAM.
    params['effective_cache_size'] = f"{int(total_ram_gb * 0.5)}GB"

    # max_connections: Depends on workload. Start with 100, adjust as needed.
    params['max_connections'] = "100"

    # wal_buffers: Typically 1/32 of shared_buffers, up to 16MB.
    shared_buffers_mb = int(total_ram_gb * 0.25 * 1024)
    wal_buffers_mb = min(shared_buffers_mb // 32, 16)
    params['wal_buffers'] = f"{wal_buffers_mb}MB"

    # min_wal_size and max_wal_size: For WAL file management.
    params['min_wal_size'] = "1GB"
    params['max_wal_size'] = "4GB"

    # checkpoint_timeout: How often checkpoints are forced.
    params['checkpoint_timeout'] = "5min"

    # autovacuum settings (basic)
    params['autovacuum'] = "on"
    params['log_autovacuum_min_duration'] = "1s" # Log autovacuum actions taking longer than 1 second

    return params

def parse_config_file(config_path):
    """Parses a postgresql.conf file into a dictionary."""
    current_params = {}
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(r"(\w+)\s*=\s*(\S+)", line)
            if match:
                key, value = match.groups()
                current_params[key] = value
    return current_params

def update_config_content(original_content, suggested_params):
    """
    Updates the content of postgresql.conf with suggested parameters.
    Preserves comments and structure for unchanged lines.
    """
    updated_lines = []
    param_keys_to_update = set(suggested_params.keys())

    for line in original_content.splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('#'):
            updated_lines.append(line)
            continue

        match = re.match(r"(\w+)\s*=\s*(\S+)", stripped_line)
        if match:
            key, current_value = match.groups()
            if key in param_keys_to_update:
                updated_lines.append(f"{key} = {suggested_params[key]}")
                param_keys_to_update.remove(key)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # Add any new parameters that weren't in the original file
    if param_keys_to_update:
        updated_lines.append("\n# Suggested new parameters by pg_config_optimizer\n")
        for key in sorted(list(param_keys_to_update)):
            updated_lines.append(f"{key} = {suggested_params[key]}")

    return "\n".join(updated_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Optimizes PostgreSQL configuration (postgresql.conf) based on system resources.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "config_path",
        help="Absolute path to the postgresql.conf file."
    )
    parser.add_argument(
        "--ram",
        type=int,
        default=None,
        help="Total system RAM in GB (e.g., 16 for 16GB). "
             "If not provided, attempts to detect or uses a default of 8GB."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show suggested changes without modifying the file."
    )
    parser.add_argument(
        "--output",
        help="Path to save the optimized configuration file. "
             "If not provided, and not in dry-run mode, the original file will be backed up and modified."
    )

    args = parser.parse_args()

    if not os.path.exists(args.config_path):
        print(f"Error: Configuration file not found at '{args.config_path}'")
        return

    total_ram_gb = args.ram if args.ram is not None else get_system_ram_gb()
    print(f"Analyzing system with {total_ram_gb:.1f} GB RAM...")

    suggested_params = calculate_pg_params(total_ram_gb)
    current_params = parse_config_file(args.config_path)

    print("\n--- PostgreSQL Configuration Optimization ---")
    print("Parameter                | Current Value | Suggested Value")
    print("-------------------------|---------------|----------------")

    changes_made = False
    for key, suggested_value in suggested_params.items():
        current_value = current_params.get(key, "N/A")
        if current_value != suggested_value:
            print(f"{key:<24} | {current_value:<13} | {suggested_value}")
            changes_made = True
        else:
            print(f"{key:<24} | {current_value:<13} | {suggested_value} (No Change)")

    if not changes_made:
        print("\nNo significant changes suggested based on current configuration and system resources.")
        return

    if args.dry_run:
        print("\n--- Dry Run: No changes applied. ---")
        with open(args.config_path, 'r') as f:
            original_content = f.read()
        updated_content = update_config_content(original_content, suggested_params)
        print("\n--- Suggested postgresql.conf content (dry run) ---")
        print(updated_content)
    else:
        with open(args.config_path, 'r') as f:
            original_content = f.read()

        updated_content = update_config_content(original_content, suggested_params)

        output_path = args.output
        if not output_path:
            backup_path = f"{args.config_path}.bak"
            print(f"Backing up original config to '{backup_path}'...")
            shutil.copyfile(args.config_path, backup_path)
            output_path = args.config_path
            print(f"Applying optimized configuration to '{output_path}'...")
        else:
            print(f"Saving optimized configuration to '{output_path}'...")

        with open(output_path, 'w') as f:
            f.write(updated_content.replace("\n", "\n")) # Ensure newlines are correctly written

        print(f"Optimization complete. Please restart your PostgreSQL server for changes to take effect.")
        if not args.output:
            print(f"Original file backed up to '{backup_path}'.")

if __name__ == "__main__":
    main()
