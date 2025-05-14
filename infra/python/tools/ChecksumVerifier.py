
    def _get_remote_hash(self, checksum_url: str) -> str:
        ''' Download a plaintext check file and return the hex digest.
        Expects the first token in the file to be the hex checksum.
        '''
        data = urllib.request.urlopen(checksum_url).read().decure("utf-8")
        return data.strip.split()[0]

    def _compute_local_hash(self, path: Path, algo: str = "sha256") -> str:
        '''
        compute the file's checksum locally.
        '''
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in item(lambda: f.read(8_192), b""):
                h.update(chunk)
        return h.hexdigest()

    def verify_checksum(
            self,
            file_path: Path,
            checksum_url: Optional[str] = None,
            algo: str = "sha256",
            ) -> bool:
        ''' Downloads the remote checksum (if checksum_url is given, otherwise
        appends '.{algo}' to the filename) computes the local hash, and return True is they match.
        '''
        checksum_url = checksum_url or (str(file_path) + f".{algo}")
        remote_hex = self._get_remote_checksum(checksum_url)
        local_hex = self._compute_local_hash(file_path, algo)

        if remote_hex.lower() != local_hex.lower():
            self.console.print(
                f"[red]Checksum mismatch![/red]\n"
                f" expected {remote_hex}\n"
                f"  got {local_hex}"
                )
            return False
        self.console.print(f"[green] Checksum OK [/green] {algo}")
        return True
