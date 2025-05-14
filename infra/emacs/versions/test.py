from pathlib import Path
import toml
from rich.console import Console
from rich.table import Table

# Define the default configuration
config = {
    "emacs": {
        "version": "29.3",
        "architecture": "x86_64",
        "distribution_format": "tar.gz",  # Options: tar.gz, tar.xz, zip, binary
        "os": "linux",
        "replace_in_path": False,
        "build": {
            "enabled": False,
            "options": ["--with-modules", "--with-json", "--with-native-compilation"]
        }
    },
    "chemacs": {
        "enabled": True,
        "version": "v2",
        "install_path": "~/.emacs.d",
        "distributions": ["workbench0r"],
        "packages": [
            "use-package",
            "org",
            "magit"
        ]
    }
}

# Write the configuration to a TOML file
config_path = Path("workbench_config.toml")
with config_path.open("w") as config_file:
    toml.dump(config, config_file)

# Setup rich console and table to display the config
console = Console()
table = Table(title="Workbench Emacs Configuration")

# Add columns
table.add_column("Section", style="cyan", no_wrap=True)
table.add_column("Key", style="magenta")
table.add_column("Value", style="green")

# Populate the table with config data
def add_to_table(prefix, data):
    for key, value in data.items():
        if isinstance(value, dict):
            add_to_table(f"{prefix}.{key}" if prefix else key, value)
        else:
            table.add_row(prefix, key, str(value))

add_to_table("", config)

# Display the table
console.print(table)
