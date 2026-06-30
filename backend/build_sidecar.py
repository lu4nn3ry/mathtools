#!/usr/bin/env python3
"""
Build the Tauri sidecar binary from the Python backend.

Usage:
    python backend/build_sidecar.py          # build + copy to src-tauri/binaries/
    python backend/build_sidecar.py --dev     # dev mode (copy without building)

Steps:
  1. Run PyInstaller to build a single binary from the FastAPI app.
  2. Copy the binary to src-tauri/binaries/ with the correct
     target-triple suffix so Tauri can find it.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "backend" / "pyinstaller.spec"
BINARIES_DIR = ROOT / "src-tauri" / "binaries"
DIST_DIR = ROOT / "dist"


def get_target_triple() -> str:
    """Return the Rust target-triple for the current platform."""
    machine = platform.machine().lower()

    if sys.platform.startswith("win"):
        arch = "x86_64" if machine in ("amd64", "x86_64") else "aarch64"
        return f"{arch}-pc-windows-msvc"
    elif sys.platform.startswith("darwin"):
        arch = "aarch64" if machine == "arm64" else "x86_64"
        return f"{arch}-apple-darwin"
    elif sys.platform.startswith("linux"):
        arch = "x86_64" if machine in ("x86_64", "amd64") else "aarch64"
        return f"{arch}-unknown-linux-gnu"
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")


def build():
    """Run PyInstaller to build the backend executable."""
    print(f"[sidecar] Building backend from spec: {SPEC}")
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(SPEC), "--clean", "--noconfirm"],
        check=True,
    )
    print("[sidecar] Build complete.")


def copy_binary(dev: bool = False):
    """Copy the built binary to src-tauri/binaries/ with target-triple name."""
    suffix = get_target_triple()
    ext = ".exe" if sys.platform.startswith("win") else ""

    BINARIES_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old binaries for this sidecar
    for old in BINARIES_DIR.glob(f"backend-*"):
        old.unlink()

    src = DIST_DIR / "backend" / f"backend{ext}"
    dst = BINARIES_DIR / f"backend-{suffix}{ext}"

    if dev:
        print(f"[sidecar] Dev mode: copying Python launcher instead of binary")
        # In dev mode, create a simple script that runs uvicorn directly
        dev_script = (
            ROOT
            / "scripts"
            / ("dev-sidecar.ps1" if sys.platform.startswith("win") else "dev-sidecar.sh")
        )
        print(f"[sidecar] Use: {dev_script}")
        return

    if not src.exists():
        raise FileNotFoundError(
            f"Built binary not found at {src}. Run without --dev first."
        )

    shutil.copy2(src, dst)
    print(f"[sidecar] Copied: {src} -> {dst}")


def main():
    parser = argparse.ArgumentParser(description="Build MathTools backend sidecar")
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Dev mode: skip PyInstaller, just link the Python source",
    )
    args = parser.parse_args()

    if not args.dev:
        build()

    copy_binary(dev=args.dev)


if __name__ == "__main__":
    main()
