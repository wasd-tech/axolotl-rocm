"""setup.py for axolotl"""

import ast
import os
import platform
import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from setuptools import find_packages, setup


def parse_requirements(extras_require_map):
    _install_requires = []
    _dependency_links = []
    with open("./requirements.txt", encoding="utf-8") as requirements_file:
        lines = [r.strip() for r in requirements_file.readlines()]
        for line in lines:
            is_extras = "deepspeed" in line or "mamba-ssm" in line
            if line.startswith("--extra-index-url"):
                # Handle custom index URLs
                _, url = line.split()
                _dependency_links.append(url)
            elif not is_extras and line and line[0] != "#":
                # Handle standard packages
                _install_requires.append(line)
    return _install_requires, _dependency_links, extras_require_map

def get_package_version():
    with open(
        Path(os.path.dirname(os.path.abspath(__file__)))
        / "src"
        / "axolotl"
        / "__init__.py",
        "r",
        encoding="utf-8",
    ) as fin:
        version_match = re.search(r"^__version__\s*=\s*(.*)$", fin.read(), re.MULTILINE)
    version_ = ast.literal_eval(version_match.group(1))
    return version_


extras_require = {
    "flash-attn": [
        "flash-attn==2.8.0.post2"
    ],
    "ring-flash-attn": [
        "flash-attn==2.8.2",
        "ring-flash-attn>=0.1.7",
        "yunchang==0.6.0",
    ],
    "deepspeed": [
        "deepspeed==0.17.2",
        "deepspeed-kernels",
    ],
    "mamba-ssm": [
        "mamba-ssm==1.2.0.post1",
        "causal_conv1d",
    ],
    "auto-gptq": [
        "auto-gptq==0.5.1",
    ],
    "mlflow": [
        "mlflow",
    ],
    "galore": [
        "galore_torch",
    ],
    "apollo": [
        "apollo-torch",
    ],
    "optimizers": [
        "galore_torch",
        "apollo-torch",
        "lomo-optim==0.1.1",
        "torch-optimi==0.2.1",
        "came_pytorch==0.1.3",
    ],
    "ray": [
        "ray[train]",
    ],
    "llmcompressor": [
        "llmcompressor==0.5.1",
    ],
}
install_requires, dependency_links, extras_require_build = parse_requirements(
    extras_require
)

setup(
    version=get_package_version(),
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        "console_scripts": [
            "axolotl=axolotl.cli.main:main",
        ],
    },
    extras_require=extras_require_build,
)
