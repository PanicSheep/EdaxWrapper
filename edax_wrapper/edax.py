import subprocess
import secrets
import multiprocessing
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


def split(lst: list, num_sections: int) -> list:
    s, rem = divmod(len(lst), num_sections)
    return [lst[i*(s+1):(i+1)*(s+1)] if i < rem else lst[rem+i*s:rem+(i+1)*s] for i in range(num_sections)]


class MultiEdax:

    def __init__(self, exe_path, hash_table_size: int|None = None, tasks: int|None = None, level: int|None = None, chunksize: int = multiprocessing.cpu_count() * 4):
        self.edax = Edax(exe_path, hash_table_size, tasks, level)
        self.chunksize = chunksize

    @property
    def name(self) -> str:
        return self.edax.name
    
    def solve(self, pos) -> list[Line]:
        if isinstance(pos, str) or not isinstance(pos, Iterable):
            pos = [pos]

        pool = pool.ThreadPool()
        results = pool.map(self.edax.solve, split(pos, self.chunksize))
        pool.close()
        return [r for result in results for r in result]

    def choose_move(self, pos) -> list[int]:
        result = self.solve(pos)
        return [(r.pv[0] if r.pv else 64) for r in result]
