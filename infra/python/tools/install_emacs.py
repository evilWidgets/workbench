import argparse
import sys
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError
import tomllib
from typing import Optional 
from functools import cached_property
import subprocess
import json
import hashlib


from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
import logging 

# set up Rich‐styled logging (optional, but keeps everything consistent)
logging.basicConfig(
    level="DEBUG", 
    format="%(message)s", 
    datefmt="[%X]", 
    handlers=[RichHandler()]
)
logger = logging.getLogger("download")

class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def _load_toml(self) -> dict:
        """Internal helper to parse the TOML file."""
        with open(self.config_path, "rb") as f:
            return tomllib.load(f)

    @cached_property
    def data(self) -> dict:
        """Public API: lazily load & cache the parsed TOML on first access."""
        return self._load_toml()


class Download:
    def __init__(self, site_dir: str = "."):
        self.site_dir = Path(site_dir)
        self.site_dir.mkdir(parents=True, exist_ok=True)

        self.console = Console() 

    def download_url(self, url: str, filename: Optional[str] = None) -> Path:
        """
        Download any file by URL into site_dir
        """
        filename = filename or url.split("/")[-1]
        out_path = self.site_dir / filename
        print(f"Downloading {url} -> {out_path}")

        try:
            logging.info(f"Downloading {url} -> {out_path}")
            urllib.request.urlretrieve(url, out_path)
        except HTTPError as e:
            logging.error("Server could'nt fulfill the request: %s %s", e.code, e.reason)
            raise
        except URLError as e:
            logging.error("Failed to reach server.")
            raise
        except OSError as e:
            logging.error("Failed writing to disk.")
            raise
        except KeyboardInterrupt:
           logging.warning("Download cancelled by user!")
           raise
        else:
            logging.info("Download succeeded: %s", out_path)
            return out_path

    def get_latest_emacs_url(self) -> str:
        """
        (stub) Return the download URL for the latest emacs 
        """
        return "http://ftp.gnu.org/gnu/emacs/emacs-29.1.tar.gz"
    
    def download_emacs(self,url:Optional[str] = None) -> Path:
        url = url or self.get_latest_emacs_url()
        filename = url.split("/")[-1]
        out_path = self.site_dir / filename
        
        with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=self.console,
                ) as progress:
            task = progress.add_task(f"[green]Downloading Emacs[/green]", total=None)
            def reporthook(block_num: int, block_size: int, total_size: int):
                if total_size and total_size > 0:
                    progress.update(task, total=total_size)
                progress.update(task, advance=block_size)

            try:
                urllib.request.urlretrieve(url, out_path, reporthook)
            except HTTPError as e:
                logger.error("Server error: %s %s", e.code, e.reason)
                raise
            except URLError as e:
                logger.error("Network error: %s", e.reason)
                raise
            except OSError as e:
                logger.error("Disk error: %s", e)
                raise
            except KeyboardInterrupt:
                logger.warning("Download cancelled by user")
                raise
            
            logger.info(f":white_check_mark: Emacs downloaded to {out_path}")
            return out_path
    
    
        
def main():

    p = argparse.ArgumentParser(
        description="Install Emacs using the given configuration file."
        )
 
    # delicious args! 
    p.add_argument("--config", help="Path to your config file.")
    #p.add_argument("--validate", help="Validate your config filez.")
    
    args = p.parse_args()

    # default message if you run the tool without args 
    if args.config:
        cfg_path = Path(args.config)
    else:
        logger.error(f"No args defined! Best thing for you to do: re-run with -h")
        return 1
    # ensure the config file we are passing exists 
    if not cfg_path.is_file():
        p.error(f"config file '{cfg_path}' does not exist!")         
    
    cfg = Config(args.config)
    dl = Download(site_dir=cfg.data["site"]["root"])
    emacs_pkg = dl.download_emacs(cfg.data["site"]["url"])
    # import ChecksumVerifier as chksum
if __name__=="__main__":
    main()
    
