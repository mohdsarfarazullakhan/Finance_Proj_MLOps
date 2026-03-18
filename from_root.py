from pathlib import Path
from typing import Union


def from_root(*path_parts: str, mkdirs: bool = False) -> Path:
    """Return a path relative to the project root.

    The project root is assumed to be the directory containing this file.

    Example:
        >>> from_root('logs', 'app.log')
        Path('<project_root>/logs/app.log')

    Args:
        *path_parts: path components to join to the root.
        mkdirs: if True, create directories for the resulting path.

    Returns:
        A pathlib.Path pointing to the requested location.
    """

    root = Path(__file__).resolve().parent
    out = root.joinpath(*path_parts) if path_parts else root

    if mkdirs:
        out.parent.mkdir(parents=True, exist_ok=True)

    return out
