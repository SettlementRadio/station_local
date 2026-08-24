"""Where the imaging audio is today, which is not yet where §9 says it will live.

§9 puts imaging audio on the external volume under `imaging/` and out of git, the rule music
follows. What exists today is the 56 files carried over from the previous attempt, still sitting in
`music/jingles/approved/`, and moving them is I-06's job rather than any command's. So every
imaging command reads whichever of the two folders holds audio and says which one it read.

This is one module rather than a helper in `cli.py` because the fact is about the pile, not about
any one command, and because it is temporary: when I-06 moves the files, `IMAGING_DIRS` loses its
second entry and nothing else in the project has to notice.
"""

from __future__ import annotations

from pathlib import Path

from station.imaging.analyse import audio_files

IMAGING_DIRS = (Path("imaging"), Path("music") / "jingles" / "approved")


def find(piece: str | None = None) -> tuple[Path, list[Path]]:
    """The folder holding imaging audio, and the pieces in it, narrowed by name.

    An empty list is not an error here — the caller says whether nothing was found at all or
    nothing matched the name — but it is never a silent one (§25).
    """
    roots = [Path.cwd() / directory for directory in IMAGING_DIRS]
    found = [(root, audio_files(root)) for root in roots if root.is_dir()]
    root, paths = next(((r, p) for r, p in found if p), (roots[0], []))
    return root, [path for path in paths if piece is None or piece in path.stem]


def looked_in() -> str:
    """The folders `find` would have read, for the message when neither holds anything."""
    return " and ".join(str(directory) for directory in IMAGING_DIRS)
