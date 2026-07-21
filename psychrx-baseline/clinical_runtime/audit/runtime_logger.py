"""Console runtime logger."""

from __future__ import annotations


class RuntimeLogger:
    """Internal console logger with no external providers."""

    def log(self, message: str) -> str:
        line = f"[clinical-runtime] {message}"
        print(line)
        return line
