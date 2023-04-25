import subprocess
import secrets
from collections.abc import Iterable
from pathlib import Path
from .line import Line
from .file import TempFile


class Edax:

    def __init__(self, exe_path, hash_table_size: int|None = None, tasks: int|None = None, level: int|None = None):
        self.exe: Path = Path(exe_path)
        self.hash_table_size: int|None = hash_table_size
        self.tasks: int|None = tasks
        self.level: int|None = level

    @property
    def name(self) -> str:
        result = subprocess.run([self.exe, '-v', '-h'], capture_output = True, text = True)
        return ' '.join(result.stderr.split()[0:3])
            
    def solve(self, pos) -> list[Line]:
        if isinstance(pos, str) or not isinstance(pos, Iterable):
            pos = [pos]

        token = secrets.token_hex(16)
        with TempFile(self.exe.parent / f'tmp_{token}.script') as tmp_file:
            tmp_file.write_text('\n'.join(str(p) for p in pos))
        
            cmd = [self.exe, '-solve', tmp_file]
            if self.hash_table_size is not None:
                cmd += ['-h', str(self.hash_table_size)]
            if self.tasks is not None:
                cmd += ['-n', str(self.tasks)]
            if self.level is not None:
                cmd += ['-l', str(self.level)]

            result = subprocess.run(
                cmd,
                cwd = self.exe.parent,
                capture_output = True,
                text = True)

        return [Line(l) for l in result.stdout.split('\n')[2:-4]]

    def choose_move(self, pos) -> list[int]:
        result = self.solve(pos)
        return [(r.pv[0] if r.pv else 64) for r in result]