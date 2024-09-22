from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize


setup(
    ext_modules=cythonize(
        [
            Extension(
                "elaina_segment.segment_c",
                sources=["elaina_segment/segment_c.pyx"],
            ),
            Extension(
                "elaina_segment.buffer_c",
                sources=["elaina_segment/buffer_c.pyx"],
            ),
        ]
    ),
    include_package_data=True,  # 包含包内的数据
    packages=["elaina_segment"],  # 查找包
    exclude_package_data={"": ["*.c"]},  # 排除 .c 文件
)
