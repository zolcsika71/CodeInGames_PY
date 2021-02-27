from setuptools import setup, find_packages
import pathlib
import sys

assert sys.version_info >= (3, 5, 0), "cg_pyEnv requires Python 3.5+"

current_dir = pathlib.Path(__file__).parent
here = current_dir.resolve()
sys.path.insert(0, str(current_dir))

setup(
    name="cg_pyEnv",
    version="0.1.0",
    description="CodInGame Merger (merges files from a folder",
    url="https://github.com/devYaoYH/cg_pyEnv",
    author="Yao Yiheng",
    keywords="codingame, merge",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.5, <4",
    install_requires=["chardet>=3.0.4,<4.0.0"],
    extras_require={"dev": ["check-manifest"], "test": ["coverage"], },
    entry_points={"console_scripts": ["build=cg_pyEnv.build:main", ], },
    project_urls={
        "Bug Reports": "https://github.com/devYaoYH/cg_pyEnv/issues",
        "Source": "https://github.com/devYaoYH/cg_pyEnv",
    },
)
