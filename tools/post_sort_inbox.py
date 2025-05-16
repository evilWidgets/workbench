#!/home/ben/workbench/workbench_env/bin/python
"""
post_sort_inbox.py:

Refactored to use orgparse for parsing Org entries, but manual write_subtree for file inserts.
Features:
- Urgent items → next_actions.org
- Project items → projects.org
Supports flags: --urgent, --projects (default: both).
Logs to console (Rich) and file: ~/workbench/logs/post_sort_inbox.log

Ensures reserved tags (e.g., 'urgent') are detected regardless of tag order or case.
"""
import sys
import logging
import argparse
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback
from orgparse import load

# Enable rich tracebacks
install_rich_traceback()

# === Logging Setup ===
LOG_DIR = Path('~/workbench/logs').expanduser()
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"{Path(__file__).stem}.log"

console = Console(file=sys.stdout)
logger = logging.getLogger('post_sort_inbox')
logger.setLevel(logging.INFO)
rich_handler = RichHandler(console=console, rich_tracebacks=True)
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.handlers.clear()
logger.addHandler(rich_handler)
logger.addHandler(file_handler)
logger.info(f"Logging to console and file: {LOG_FILE}")

# === Paths & Settings ===
INBOX_PATH    = Path('~/workbench/org/inbox.org').expanduser()
NEXT_ACTIONS  = Path('~/org/next_actions.org').expanduser()
PROJECTS_PATH = Path('~/workbench/org/projects.org').expanduser()
RESERVED_TAGS = ['urgent']

# === Helper Functions ===

def load_inbox():
    """Load the org file and return the 'Inbox' node."""
    doc = load(INBOX_PATH)
    inbox_node = next((n for n in doc.children if n.heading == 'Inbox'), None)
    if not inbox_node:
        logger.error("'* Inbox' heading not found.")
        sys.exit(1)
    return doc, inbox_node


def write_subtree(file_path: Path, heading: str, node) -> None:
    """Insert the node subtree under a top-level heading via text operations."""
    file_path = file_path.expanduser()
    subtree = str(node).rstrip() + '\n'
    # Read existing content or start empty
    lines = file_path.read_text().splitlines(keepends=True) if file_path.exists() else []
    # Ensure heading exists
    buf = []
    found = False
    for line in lines:
        buf.append(line)
        if line.strip().lower() == f"* {heading}".lower():
            found = True
    if not found:
        buf.append(f"\n* {heading}\n")
        logger.info(f"Created heading '{heading}' in {file_path}")
    # Insert subtree after heading
    updated, inserted = [], False
    for line in buf:
        updated.append(line)
        if not inserted and line.strip().lower() == f"* {heading}".lower():
            updated.append(subtree)
            inserted = True
            logger.info(f"Inserted entry under '{heading}' in {file_path}")
    # Write back
    file_path.write_text(''.join(updated))


def process_entries(doc, inbox_node, do_urgent: bool, do_projects: bool) -> None:
    """Process each TODO node under the Inbox heading and remove processed."""
    processed = []
    for node in list(inbox_node.children):
        if not node.todo:
            continue
        tags = [t.lower() for t in node.tags]
        is_urgent = 'urgent' in tags
        projects = [t for t in node.tags if t.lower() not in RESERVED_TAGS]
        # Urgent
        if do_urgent and is_urgent:
            if projects:
                for proj in projects:
                    write_subtree(NEXT_ACTIONS, proj.title(), node)
            else:
                write_subtree(NEXT_ACTIONS, 'Next Actions', node)
            processed.append(node)
        # Projects
        if do_projects and projects:
            for proj in projects:
                write_subtree(PROJECTS_PATH, proj.title(), node)
            if node not in processed:
                processed.append(node)
    # Remove processed
    for node in processed:
        logger.info(f"Removing processed entry: {node.heading}")
        inbox_node.children.remove(node)
    # Save inbox
    INBOX_PATH.write_text(str(doc))
    logger.info("Inbox updated.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--urgent', action='store_true')
    p.add_argument('--projects', action='store_true')
    args = p.parse_args()
    do_urgent = args.urgent or not args.projects
    do_projects = args.projects or not args.urgent
    logger.info(f"Running urgent={do_urgent}, projects={do_projects}")
    doc, inbox = load_inbox()
    process_entries(doc, inbox, do_urgent, do_projects)
    logger.info("Done.")


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Error running script")
        sys.exit(1)

