from pathlib import Path
from .base import FileStrategy

class SymlinkStrategy(FileStrategy):
    def process(self, source_file: Path, target_dir: Path, source_root: Path):
        # For symlinks, we want the path relative to the submodule root
        # so we can construct {{ .chezmoi.sourceDir }}/vendor/...
        rel_path = source_file.relative_to(source_root.parent)

        dest_filename = f"symlink_{source_file.name}.tmpl"
        dest_path = target_dir / dest_filename

        with open(dest_path, 'w') as f:
            f.write(f'{{{{ .chezmoi.sourceDir }}}}/{rel_path}\n')
            
        print(f"   [Symlink] Generated {dest_filename}")