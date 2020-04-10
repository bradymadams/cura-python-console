import os
import setuptools

version = '0.1.0'

setuptools.setup(
    name='pyqt-console',
    version=version,
    author='Brady Adams',
    author_email='',
    packages=setuptools.find_packages(),
    package_data={
        'console': ['*.qml', '*.png']
    },
    install_requires=['PyQt5']
)
