from setuptools import setup, find_packages
import pathlib
import sys

assert sys.version_info >= (3, 5, 0), "cg_py_class_merger requires Python 3.5+"

current_dir = pathlib.Path(__file__).parent
here = current_dir.resolve()
sys.path.insert(0, str(current_dir))

setup(
    name='cg_py_class_merger',
    version='0.1.0',
    description='CG Merger (merges files from import',
    url='https://github.com/zolcsika71/cg_py_class_merger',
    author='zolcsika71',
    keywords='codingame, merge',
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.5, <4",
    install_requires=['chardet>=3.0.4,<4.0.0'],
    extras_require={'dev': ["check-manifest"], "test": ["coverage"], },
    entry_points={'console_scripts': ['build=cg_py_class_merger.build:main', ], },
    project_urls={
        'Bug Reports': 'https://github.com/zolcsika71/cg_py_class_merger/issues',
        'Source': 'https://github.com/zolcsika71/cg_py_class_merger',
    },
)
