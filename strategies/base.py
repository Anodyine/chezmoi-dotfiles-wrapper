from abc import ABC, abstractmethod
from pathlib import Path

class FileStrategy(ABC):
    @abstractmethod
    def process(self, source_file: Path, target_dir: Path, source_root: Path):
        """
        Process a single file and generate the corresponding chezmoi wrapper.
        
        :param source_file: Absolute path to the source file (in vendor/)
        :param target_dir:  Absolute path to the destination folder (in dot_config/)
        :param source_root: Absolute path to the root of the source repo (for relative calc)
        """
        pass