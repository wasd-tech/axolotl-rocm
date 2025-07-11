"""
dynamic requirements for axolotl
"""

import platform
import re
from importlib.metadata import PackageNotFoundError, version

from setuptools.command.build_py import build_py as _build_py


# pylint: disable=duplicate-code
def parse_requirements():
    _install_requires = []
    _dependency_links = []
    with open("./requirements.txt", encoding="utf-8") as requirements_file:
        lines = [r.strip() for r in requirements_file.readlines()]
        for line in lines:
            is_extras = (
                "flash-attn" in line
                or "flash-attention" in line
                or "deepspeed" in line
                or "mamba-ssm" in line
                or "lion-pytorch" in line
            )
            if line.startswith("--extra-index-url"):
                # Handle custom index URLs
                _, url = line.split()
                _dependency_links.append(url)
            elif not is_extras and line and line[0] != "#":
                # Handle standard packages
                _install_requires.append(line)
    return _install_requires, _dependency_links


class BuildPyCommand(_build_py):
    """
    custom build_py command to parse dynamic requirements
    """

    def finalize_options(self):
        super().finalize_options()
        install_requires, _ = parse_requirements()
        self.distribution.install_requires = install_requires