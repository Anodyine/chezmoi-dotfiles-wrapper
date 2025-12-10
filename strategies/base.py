# strategies/base.py
from abc import ABC, abstractmethod
from pathlib import Path

class FileStrategy(ABC):
    @abstractmethod
    def process(self, source_file: Path, repo_root: Path):
        """
        :param source_file: Absolute path to the source file
        :param repo_root:   Absolute path to the repository root (wrapper repo)
        """
        pass