import os
import subprocess
import logging
from datetime import datetime


from apscheduler.schedulers.blocking import BlockingScheduler

# configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    )

# paths
SOURCE_DIR = os.path.expanduser("~/.emacs.d/")
TARGET_DIR = os.path.join(os.getcwd(), "profiles/benchmacs/")

# git repo
REPO_ROOT = os.getcwd()

def backup_and_push():
    try:
        logging.info("Starting rsync from %s to %s", SOURCE_DIR, TARGET_DIR)
        subprocess.run(
            ["rsync", "-a", "--delete", SOURCE_DIR, TARGET_DIR],
            check=True
            )

        # change into the repo to run Git commands
        os.chdir(REPO_ROOT)

        logging.info("Staging changes...")
        subprocess.run(["git", "add", "profiles/benchmacs/"], check=True)

        commit_msg = f"Automated Emacs backup: {datetime.now().isoformat()}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg]
            )

        logging.info("Pushing to remote...")
        subprocess.run(["git", "push"], check=True)

        logging.info("Backup & sync cycle complete.")
    except subprocess.CalledProcessError as e:
        logging.error("Command failed: %s", e)
    except Exception as exc:
        logging.error("Unexpected error: %s", exc)



        
if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Schedule the job every 2 minutes
    scheduler.add_job(backup_and_push, 'interval', minutes=2, next_run_time=datetime.now())
    logging.info("Scheduler started—running every 2 minutes.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped by user.")
