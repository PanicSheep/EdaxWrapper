from pathlib import Path


class TempFile:

    def __init__(self, filename: Path) -> None:
        self.filename: Path = filename

    def __enter__(self):
        return self.filename

    def __exit__(self, *_):
        self.filename.unlink()
        return False
