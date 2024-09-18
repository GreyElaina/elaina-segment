from setuptools import setup, Extension
from os import environ
from Cython.Build import cythonize

if environ.get("NO_CYTHON"):
    setup(
        package_dir={"": "src"},
        packages=["elaina_segment"],
        include_package_data=True,
        exclude_package_data={"": ["*.c"]},
    )
    exit()

setup(
    ext_modules=cythonize("src/elaina_segment/*.pyx"),
    include_package_data=True,
)
